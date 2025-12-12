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
SvF.mngF = 'MNG-dif-2.mng'
SvF.OptStep=[0,0.0001,0.0001]
currentTab = Table ( 'Spring5.dat','currentTab','t,x' )
t = Set('t',SvF.currentTab.dat('t')[:].min(),SvF.currentTab.dat('t')[:].max(),0.025,'','t')
X = Set('X',-0.1,2.2,0.1,'','X')
V = Set('V',-1,1.5,0.1,'','V')
x = Fun('x',[t])
def fx(t) : return x.F([t])
v = Fun('v',[t])
def fv(t) : return v.F([t])
f = smbFun('f',[X,V], SymbolInteg=False)
def ff(X,V) : return f.F([X,V])
c = Tensor('c',[28])
def fc(i) : return c.F([i])
def f_smbF00(Args) :
   X = Args[0]
   V = Args[1]
   SvF.F_Arg_Type = "N"
   ret =  ( fc(0)+fc(1)*V+fc(2)*X+fc(3)*V**2+fc(4)*X*V+fc(5)*X**2+fc(6)*V**3+fc(7)*X*V**2+fc(8)*X**2*V+fc(9)*X**3+fc(10)*V**4+fc(11)*X*V**3+fc(12)*X**2*V**2+fc(13)*X**3*V+fc(14)*X**4+fc(15)*V**5+fc(16)*X*V**4+fc(17)*X**2*V**3+fc(18)*X**3*V**2+fc(19)*X**4*V+fc(20)*X**5+fc(21)*V**6+fc(22)*X*V**5+fc(23)*X**2*V**4+fc(24)*X**3*V**3+fc(25)*X**4*V**2+fc(26)*X**5*V+fc(27)*X**6 ) 
   SvF.F_Arg_Type = ""
   return ret
f.smbF = f_smbF00
CVmakeSets (  CV_NumSets=21 )
SvF.CVNumOfIter=0; 
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

    c.var = py.Var ( range (c.Sizes[0]),domain=Reals )
    c.gr =  c.var
    Gr.c =  c.var
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

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('x'))
    if x.mu is None : x.mu = Gr.mu0
    x.ValidationSets = SvF.ValidationSets
    x.notTrainingSets = SvF.notTrainingSets
    x.TrainingSets = SvF.TrainingSets
 											# x.Complexity([Penal[0]])+f.Complexity([Penal[1],Penal[2]])/x.V.sigma2+x.MSD()
    def obj_expression(Gr):  
        return (
             x.Complexity([Penal[0]])+f.Complexity([Penal[1],Penal[2]])/x.V.sigma2+x.MSD()
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x = Task.Funs[0]

    f = Task.Funs[2]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (x.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.Complexity([Penal[0]]) ='+ stmp+'\n')
    tmp = (f.Complexity([Penal[1],Penal[2]])/x.V.sigma2)
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tf.Complexity([Penal[1],Penal[2]])/x.V.sigma2 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tf.Complexity([Penal[1],Penal[2]])/x.V.sigma2 ='+ stmp+'\n')
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
Region = Polyline([-1,-1,2.5,2.5,-1],[-0.1,2.2,2.2,-0.1,-0.1], None, "Region")
Plot( [ [ Region, 'c=green', 'ls=dashed'], [x, 'c=r', 'ls=solid'] ] )
Trajectory = Polyline(x.grd[:-1],v.grd[:-1], None, "Trajectory")
Plot( [ [ f], [Trajectory, 'c=red', 'lw=1.2'] ] )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")