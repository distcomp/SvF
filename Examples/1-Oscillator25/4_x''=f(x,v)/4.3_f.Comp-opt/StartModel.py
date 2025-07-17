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
SvF.CVNumOfIter = 91
Table ( 'Spring5.dat','curentTabl','t,x' )
t = Set('t',SvF.curentTabl.dat('t')[:].min(),SvF.curentTabl.dat('t')[:].max(),0.025,'','t')
X = Set('X',-0.1,2.2,0.1,'','X')
V = Set('V',-1,1.5,0.1,'','V')
x = Fun('x',[t])
def fx(t) : return x.F([t])
v = Fun('v',[t])
def fv(t) : return v.F([t])
f = smbFun('f',[X,V])
def ff(X,V) : return f.F([X,V])
c = Tensor('c',[28])
def fc(i) : return c.F([i])
def f_smbF(Args) :
   X = Args[0]
   V = Args[1]
   return fc(0)+fc(1)*V+fc(2)*X+fc(3)*V**2+fc(4)*X*V+fc(5)*X**2+fc(6)*V**3+fc(7)*X*V**2+fc(8)*X**2*V+fc(9)*X**3+fc(10)*V**4+fc(11)*X*V**3+fc(12)*X**2*V**2+fc(13)*X**3*V+fc(14)*X**4+fc(15)*V**5+fc(16)*X*V**4+fc(17)*X**2*V**3+fc(18)*X**3*V**2+fc(19)*X**4*V+fc(20)*X**5+fc(21)*V**6+fc(22)*X*V**5+fc(23)*X**2*V**4+fc(24)*X**3*V**3+fc(25)*X**4*V**2+fc(26)*X**5*V+fc(27)*X**6
f.smbF = f_smbF
def f_smbFx(Args) :
   X = Args[0]
   V = Args[1]
   return V**5*fc(22) + 2*V**4*X*fc(23) + V**4*fc(16) + 3*V**3*X**2*fc(24) + 2*V**3*X*fc(17) + V**3*fc(11) + 4*V**2*X**3*fc(25) + 3*V**2*X**2*fc(18) + 2*V**2*X*fc(12) + V**2*fc(7) + 5*V*X**4*fc(26) + 4*V*X**3*fc(19) + 3*V*X**2*fc(13) + 2*V*X*fc(8) + V*fc(4) + 6*X**5*fc(27) + 5*X**4*fc(20) + 4*X**3*fc(14) + 3*X**2*fc(9) + 2*X*fc(5) + fc(2) 
f.smbFx = f_smbFx
def f_smbFxx(Args) :
   X = Args[0]
   V = Args[1]
   return 2*V**4*fc(23) + 6*V**3*X*fc(24) + 2*V**3*fc(17) + 12*V**2*X**2*fc(25) + 6*V**2*X*fc(18) + 2*V**2*fc(12) + 20*V*X**3*fc(26) + 12*V*X**2*fc(19) + 6*V*X*fc(13) + 2*V*fc(8) + 30*X**4*fc(27) + 20*X**3*fc(20) + 12*X**2*fc(14) + 6*X*fc(9) + 2*fc(5) 
f.smbFxx = f_smbFxx
def f_smbFy(Args) :
   X = Args[0]
   V = Args[1]
   return 6*V**5*fc(21) + 5*V**4*X*fc(22) + 5*V**4*fc(15) + 4*V**3*X**2*fc(23) + 4*V**3*X*fc(16) + 4*V**3*fc(10) + 3*V**2*X**3*fc(24) + 3*V**2*X**2*fc(17) + 3*V**2*X*fc(11) + 3*V**2*fc(6) + 2*V*X**4*fc(25) + 2*V*X**3*fc(18) + 2*V*X**2*fc(12) + 2*V*X*fc(7) + 2*V*fc(3) + X**5*fc(26) + X**4*fc(19) + X**3*fc(13) + X**2*fc(8) + X*fc(4) + fc(1) 
f.smbFy = f_smbFy
def f_smbFxy(Args) :
   X = Args[0]
   V = Args[1]
   return 5*V**4*fc(22) + 8*V**3*X*fc(23) + 4*V**3*fc(16) + 9*V**2*X**2*fc(24) + 6*V**2*X*fc(17) + 3*V**2*fc(11) + 8*V*X**3*fc(25) + 6*V*X**2*fc(18) + 4*V*X*fc(12) + 2*V*fc(7) + 5*X**4*fc(26) + 4*X**3*fc(19) + 3*X**2*fc(13) + 2*X*fc(8) + fc(4) 
f.smbFxy = f_smbFxy
def f_smbFyy(Args) :
   X = Args[0]
   V = Args[1]
   return 30*V**4*fc(21) + 20*V**3*X*fc(22) + 20*V**3*fc(15) + 12*V**2*X**2*fc(23) + 12*V**2*X*fc(16) + 12*V**2*fc(10) + 6*V*X**3*fc(24) + 6*V*X**2*fc(17) + 6*V*X*fc(11) + 6*V*fc(6) + 2*X**4*fc(25) + 2*X**3*fc(18) + 2*X**2*fc(12) + 2*X*fc(7) + 2*fc(3) 
f.smbFyy = f_smbFyy
f.ArgNormalition=True
CVmakeSets ( CV_NumSets=21 )
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    x.var = py.Var ( x.A[0].NodS,domain=Reals )
    Gr.x =  x.var

    v.var = py.Var ( v.A[0].NodS,domain=Reals )
    Gr.v =  v.var

    c.var = py.Var ( range (c.Sizes[0]),domain=Reals )
    Gr.c =  c.var

    f.var = py.Var ( f.A[0].NodS,f.A[1].NodS,domain=Reals )
    Gr.f =  f.var
 								# d2/dt2(x)==f(x,v)
    def EQ0 (Gr,_it) :
        return (
          ((fx((_it+t.step))+fx((_it-t.step))-2*fx(_it))/t.step**2)==ff(fx(_it),fv(_it))
        )
    Gr.conEQ0 = py.Constraint(t.mFlNodSm,rule=EQ0 )
 								# v==d/dt(x)
    def EQ1 (Gr,_it) :
        return (
          fv(_it)==((fx((_it+t.step))-fx(_it))/t.step)
        )
    Gr.conEQ1 = py.Constraint(t.FlNodSm,rule=EQ1 )

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('x'))
    if x.mu is None : x.mu = Gr.mu0
    x.ValidationSets = SvF.ValidationSets
    x.notTrainingSets = SvF.notTrainingSets
    x.TrainingSets = SvF.TrainingSets
 											# f.Complexity([Penal[0],Penal[1]])/x.V.sigma2+x.MSD()
    def obj_expression(Gr):  
        return (
             f.Complexity([Penal[0],Penal[1]])/x.V.sigma2+x.MSD()
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
    tmp = (f.Complexity([Penal[0],Penal[1]])/x.V.sigma2)
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tf.Complexity([Penal[0],Penal[1]])/x.V.sigma2 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tf.Complexity([Penal[0],Penal[1]])/x.V.sigma2 ='+ stmp+'\n')
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