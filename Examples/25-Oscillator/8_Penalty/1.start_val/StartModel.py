# -*- coding: UTF-8 -*-
import sys
path_SvF = "/home/sokol/D/SvF/"
sys.path.append("/home/sokol/D/SvF/SvFlib")
sys.path.append(path_SvF + "pyomo-everest/python-api")
sys.path.append(path_SvF + "pyomo-everest/ssop")
import COMMON as SvF
SvF.path_SvF = path_SvF
SvF.tmpFileDir = SvF.path_SvF + 'TMP/'
from CVSets import *
from Table  import *
from Task   import *
from MakeModel import *
from GIS import *

SvF.Task = TaskClass()
Task = SvF.Task
SvF.mngF = 'MNG.mng'
SvF.CVNumOfIter = 1
currentTab = Table ( 'Spring5.dat','currentTab','t,x' )
t = Set('t',SvF.currentTab.dat('t')[:].min(),SvF.currentTab.dat('t')[:].max(),0.025,'','t')
X = Set('X',-0.1,2.2,0.1,'','X')
V = Set('V',-1,1.5,0.1,'','V')
x = Fun('x',[t])
def fx(t) : return x.F([t])
v = Fun('v',[t])
def fv(t) : return v.F([t])
f = smbFun('f',[X,V])
def ff(X,V) : return f.F([X,V])
c_f = Tensor('c_f',[28])
def fc_f(i) : return c_f.F([i])
def f_smbF00(Args) :
   X = Args[0]
   V = Args[1]
   SvF.F_Arg_Type = "N"
   ret =  ( fc_f(0)+fc_f(1)*V+fc_f(2)*X+fc_f(3)*V**2+fc_f(4)*X*V+fc_f(5)*X**2+fc_f(6)*V**3+fc_f(7)*X*V**2+fc_f(8)*X**2*V+fc_f(9)*X**3+fc_f(10)*V**4+fc_f(11)*X*V**3+fc_f(12)*X**2*V**2+fc_f(13)*X**3*V+fc_f(14)*X**4+fc_f(15)*V**5+fc_f(16)*X*V**4+fc_f(17)*X**2*V**3+fc_f(18)*X**3*V**2+fc_f(19)*X**4*V+fc_f(20)*X**5+fc_f(21)*V**6+fc_f(22)*X*V**5+fc_f(23)*X**2*V**4+fc_f(24)*X**3*V**3+fc_f(25)*X**4*V**2+fc_f(26)*X**5*V+fc_f(27)*X**6 ) 
   SvF.F_Arg_Type = ""
   return ret
f.smbF = f_smbF00
Px = 0.16
SvF.Penalty.append(Px)
Pfx = 0.006
SvF.Penalty.append(Pfx)
Pfv = .008
SvF.Penalty.append(Pfv)
SvF.resF=None
CVmakeSets (  CV_NumSets=21 )
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    x.var = py.Var ( x.A[0].NodS,domain=Reals )
    x.gr =  x.var
    Gr.x =  x.var

    v.var = py.Var ( v.A[0].NodS,domain=Reals )
    v.gr =  v.var
    Gr.v =  v.var

    c_f.var = py.Var ( range (c_f.Sizes[0]),domain=Reals )
    c_f.gr =  c_f.var
    Gr.c_f =  c_f.var
 								# d2/dt2(x)==f(x,v)
    def EQ0 (Gr,_it) :
        return (
          x.by_xx(_it)==ff(fx(_it),fv(_it))
        )
    Gr.conEQ0 = py.Constraint(t.mFlNodSm,rule=EQ0 )
 								# v==d/dt(x)
    def EQ1 (Gr,_it) :
        return (
          fv(_it)==x.by_x(_it)
        )
    Gr.conEQ1 = py.Constraint(t.FlNodSm,rule=EQ1 )
    Px = Penal[0]
    Pfx = Penal[1]
    Pfv = Penal[2]

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('x'))
    if x.mu is None : x.mu = Gr.mu0
    x.ValidationSets = SvF.ValidationSets
    x.notTrainingSets = SvF.notTrainingSets
    x.TrainingSets = SvF.TrainingSets
 											# x.Complexity([Px])+f.Complexity([Pfx,Pfv])/x.V.sigma2+x.MSD()
    def obj_expression(Gr):  
        return (
             x.Complexity([Px])+f.Complexity([Pfx,Pfv])/x.V.sigma2+x.MSD()
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Px = Penal[0]
    Pfx = Penal[1]
    Pfv = Penal[2]
    Gr = Task.Gr

    x = Task.Funs[0]

    f = Task.Funs[2]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (x.Complexity([Px]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.Complexity([Px]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.Complexity([Px]) ='+ stmp+'\n')
    tmp = (f.Complexity([Pfx,Pfv])/x.V.sigma2)
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tf.Complexity([Pfx,Pfv])/x.V.sigma2 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tf.Complexity([Pfx,Pfv])/x.V.sigma2 ='+ stmp+'\n')
    tmp = (x.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.MSD() ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
Reg=Polyline([-1,-1,2.5,2.5,-1],[-0.1,2.2,2.2,-0.1,-0.1],None,'Region')
Task.Draw ( 'Region;LC:green;LSt:dashed x;LC:r;LSt:solid' )
Pl = Polyline (x, v, None, 'Trajectory')
Pl.Y[0]=Pl.Y[1]
Pl.Y[-1]=Pl.Y[-2]
Task.Draw ( 'f Trajectory;LC:red' )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")