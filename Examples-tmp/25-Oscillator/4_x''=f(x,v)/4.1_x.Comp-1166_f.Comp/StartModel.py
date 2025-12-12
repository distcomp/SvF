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
SvF.mngF = 'MNG-dif-2-OptPar.mng'
SvF.CVNumOfIter = 1
Table ( 'Spring5.dat','curentTabl','t,x' )
t = Set('t',SvF.curentTabl.dat('t')[:].min(),SvF.curentTabl.dat('t')[:].max(),0.025,'','t')
X = Set('X',-0.1,2.2,0.1,'','X')
V = Set('V',-1,1.5,0.1,'','V')
x = Fun('x',[t])
def fx(t) : return x.F([t])
v = Fun('v',[t])
def fv(t) : return v.F([t])
f = pFun('f',[X,V], Degree=6)
def ff(X,V) : return f.F([X,V])
Px = 0.16
SvF.Penalty.append(Px)
Pfx = 0.006
SvF.Penalty.append(Pfx)
Pfv = .008
SvF.Penalty.append(Pfv)
SvF.resF=None
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

    f.var = py.Var ( range (f.sizeP) )
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