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
SvF.CVNumOfIter = 41
SvF.CVstep = 21
Table ( '../Spring5.dat','curentTabl','x,t' )
t=Grid('t',-1.0,2.5,0.025,'i__t','t')
x = Fun('x',[t],False,-1,1, '') 
def fx(t) : return x.F([t])
K = Fun('K',[],False,-1,1, '') 
K.grd = 1
def fK() : return K.F([])
xr = Fun('xr',[],False,-1,1, '') 
xr.grd = 1
def fxr() : return xr.F([])
SvF.SchemeD1 = "Central"
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

    K.var = py.Var ( domain=Reals, initialize = 1 )
    Gr.K =  K.var
    K.InitByData()
    def fK() : return K.F([])

    xr.var = py.Var ( domain=Reals, initialize = 1 )
    Gr.xr =  xr.var
    xr.InitByData()
    def fxr() : return xr.F([])
 								# d2/dt2(x)==-K*(x-xr)
    def EQ0 (Gr,i__t) :
        return (
          ((fx((i__t+t.step))+fx((i__t-t.step))-2*fx(i__t))/t.step**2)==-fK()*(fx(i__t)-fxr())
        )
    Gr.conEQ0 = py.Constraint(t.mFlNodSm,rule=EQ0 )

    SvF.testSet, SvF.teachSet = MakeSets_byParts(SvF.curentTabl.NoR, SvF.CVstep)

    Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('x'))
    x.mu = Gr.mu0
    x.testSet = SvF.testSet
    x.teachSet = SvF.teachSet
 											# x.Complexity([Penal[0]])+x.MSD()
    def obj_expression(Gr):  
        return (
             x.Complexity([Penal[0]])+x.MSD()
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x = Task.Funs[0]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (x.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.Complexity([Penal[0]]) ='+ stmp+'\n')
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