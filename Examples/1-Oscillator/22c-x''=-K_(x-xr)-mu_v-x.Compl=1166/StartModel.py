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
SvF.mngF = 'Oscillator_x''=-K_(x-xr)-μ_v_ChDir.odt'
SvF.CVNumOfIter = 1
SvF.CVstep = 21
SvF.SchemeD1 = "Central"
Table ( '../Spring5.dat','curentTabl','x,t' )
t=Grid('t',-1.0,2.5,0.025,'i__t','t')
x = Fun('x',[t],False,-1,1, '') 
def fx(t) : return x.F([t])
v = Fun('v',[t],False,-1,1, '') 
def fv(t) : return v.F([t])
K = Fun('K',[],False,-1,1, '') 
K.grd = 1
def fK() : return K.F([])
Deltax = Fun('Deltax',[],False,-1,1, '') 
Deltax.grd = 1
def fDeltax() : return Deltax.F([])
muu = Fun('muu',[],False,-1,1, '') 
muu.grd = 1
def fmuu() : return muu.F([])
SvF.resF="MNG.res"
from  numpy import *

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    x.var = py.Var ( x.A[0].NodS,domain=Reals, initialize = 1 )
    Gr.x =  x.var
    x.InitByData()
    def fx(t) : return x.F([t])

    v.var = py.Var ( v.A[0].NodS,domain=Reals, initialize = 1 )
    Gr.v =  v.var
    v.InitByData()
    def fv(t) : return v.F([t])

    K.var = py.Var ( domain=Reals, initialize = 1 )
    Gr.K =  K.var
    K.InitByData()
    def fK() : return K.F([])

    Deltax.var = py.Var ( domain=Reals, initialize = 1 )
    Gr.Deltax =  Deltax.var
    Deltax.InitByData()
    def fDeltax() : return Deltax.F([])

    muu.var = py.Var ( domain=Reals, initialize = 1 )
    Gr.muu =  muu.var
    muu.InitByData()
    def fmuu() : return muu.F([])
 								# \frac{d^2}{dt^2}(x)==-K*(x-Deltax)-muu*v
    def EQ0 (Gr,i__t) :
        return (
          ((fx((i__t+t.step))+fx((i__t-t.step))-2*fx(i__t))/t.step**2)==-fK()*(fx(i__t)-fDeltax())-fmuu()*fv(i__t)
        )
    Gr.conEQ0 = py.Constraint(t.mFlNodSm,rule=EQ0 )
 								# v==\frac{d}{dt}(x)
    def EQ1 (Gr,i__t) :
        return (
          fv(i__t)==((fx((i__t+t.step))-fx((i__t-t.step)))/t.step *0.5)
        )
    Gr.conEQ1 = py.Constraint(t.mFlNodSm,rule=EQ1 )

    SvF.testSet, SvF.teachSet = MakeSets_byParts(SvF.curentTabl.NoR, SvF.CVstep)

    Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('x'))
    x.mu = Gr.mu0
    x.testSet = SvF.testSet
    x.teachSet = SvF.teachSet
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

SvF.lenPenalty = 1

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
Task.Draw ('')