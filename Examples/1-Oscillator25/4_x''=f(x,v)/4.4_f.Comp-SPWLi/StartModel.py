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
SvF.CVNumOfIter = 0
SvF.CVstep = 21
Table ( 'Spring5.dat','curentTabl','t,x' )
t = Set('t',SvF.curentTabl.dat('t')[:].min(),SvF.curentTabl.dat('t')[:].max(),0.025,'','t')
X = Set('X',-0.1,2.3,0.3,'','X')
V = Set('V',-1,1.7,0.3,'','V')
x = Fun('x',[t])
def fx(t) : return x.F([t])
v = Fun('v',[t])
def fv(t) : return v.F([t])
f = SPWLFun('f',[X,V], Type='SPWLi')
def ff(X,V) : return f.F([X,V])
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

    f.var = py.Var ( f.A[0].NodS,f.A[1].NodS,domain=Reals )
    Gr.f =  f.var
 								# v==d/dt(x)
    def EQ0 (Gr,_it) :
        return (
          fv(_it)==((fx((_it+t.step))-fx(_it))/t.step)
        )
    Gr.conEQ0 = py.Constraint(t.FlNodSm,rule=EQ0 )
 								# d2/dt2(x)==f(x,v)
    def EQ1 (Gr,_it) :
        return (
          ((fx((_it+t.step))+fx((_it-t.step))-2*fx(_it))/t.step**2)==ff(fx(_it),fv(_it))
        )
    Gr.conEQ1 = py.Constraint(t.mFlNodSm,rule=EQ1 )

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
Task.Draw ( 'x' )
Pl = Polyline (x, v, None, 'Trajectory')
Pl.Y[0]=Pl.Y[1]
Pl.Y[-1]=Pl.Y[-2]
Task.Draw ( 'f Trajectory;LC:red' )