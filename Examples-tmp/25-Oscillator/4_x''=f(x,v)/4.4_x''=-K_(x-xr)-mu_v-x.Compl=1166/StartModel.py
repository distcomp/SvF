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
SvF.mngF = 'MNG-CVerr.mng'
currentTab = Table ( 'Spring5.dat','currentTab','x,t' )
t = Set('t',-1.,2.5,0.025,'','t')
x = Fun('x',[t])
def fx(t) : return x.F([t])
v = Fun('v',[t])
def fv(t) : return v.F([t])
K = Tensor('K',[])
def fK() : return K.F([])
muu = Tensor('muu',[])
def fmuu() : return muu.F([])
xr = Tensor('xr',[])
def fxr() : return xr.F([])
SvF.SchemeD1 = "Central"
CVmakeSets (  CV_NumSets=21 )
SvF.CVNumOfIter=1; 
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

    K.var = py.Var ( range (1), domain=Reals )
    K.gr =  K.var
    Gr.K =  K.var

    muu.var = py.Var ( range (1), domain=Reals )
    muu.gr =  muu.var
    Gr.muu =  muu.var

    xr.var = py.Var ( range (1), domain=Reals )
    xr.gr =  xr.var
    Gr.xr =  xr.var
 								# d2/dt2(x)==-K*(x-xr)-muu*v
    def EQ0 (Gr,_it) :
        return (
          x.by_xx(_it)==-fK()*(fx(_it)-fxr())-fmuu()*fv(_it)
        )
    Gr.conEQ0 = py.Constraint(t.mFlNodSm,rule=EQ0 )
 								# v==d/dt(x)
    def EQ1 (Gr,_it) :
        return (
          fv(_it)==x.by_x(_it)
        )
    Gr.conEQ1 = py.Constraint(t.mFlNodSm,rule=EQ1 )

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('x'))
    if x.mu is None : x.mu = Gr.mu0
    x.ValidationSets = SvF.ValidationSets
    x.notTrainingSets = SvF.notTrainingSets
    x.TrainingSets = SvF.TrainingSets
 											# x.Complexity([Penal[0]])/x.V.sigma2+x.MSD()
    def obj_expression(Gr):  
        return (
             x.Complexity([Penal[0]])/x.V.sigma2+x.MSD()
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x = Task.Funs[0]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (x.Complexity([Penal[0]])/x.V.sigma2)
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.Complexity([Penal[0]])/x.V.sigma2 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.Complexity([Penal[0]])/x.V.sigma2 ='+ stmp+'\n')
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
CVer = Polyline(x.A[0].dat,x.CVerr, "CVer")
P0 = Polyline([x.A[0].dat[0],x.A[0].dat[-1]],[0,0], "P0")
Plot( [ [ x], [CVer, 'c=c'], [P0, 'c=gray', 'ls=-.'] ] )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")