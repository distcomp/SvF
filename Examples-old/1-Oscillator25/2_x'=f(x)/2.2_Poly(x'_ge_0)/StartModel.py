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
SvF.mngF = 'MNG-dif-1.mng'
SvF.CVNumOfIter = 0
Table ( 'Spring5.dat','curentTabl','*' )
t = Set('t',SvF.curentTabl.dat('t')[:].min(),SvF.curentTabl.dat('t')[:].max(),0.025,'','t')
X = Set('X',-0.1,2.0,0.1,'','X')
x = Fun('x',[t])
def fx(t) : return x.F([t])
f = pFun('f',[X], Degree=5)
def ff(X) : return f.F([X])
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

    f.var = py.Var ( range (f.sizeP) )
    Gr.f =  f.var
 								# d/dt(x)=f(x)
    def EQ0 (Gr,_it) :
        return (
          ((fx((_it+t.step))-fx(_it))/t.step)==ff(fx(_it))
        )
    Gr.conEQ0 = py.Constraint(t.FlNodSm,rule=EQ0 )

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('x'))
    if x.mu is None : x.mu = Gr.mu0
    x.ValidationSets = SvF.ValidationSets
    x.notTrainingSets = SvF.notTrainingSets
    x.TrainingSets = SvF.TrainingSets
 											# x.MSD()+f.Complexity([Penal[0]])
    def obj_expression(Gr):  
        return (
             x.MSD()+f.Complexity([Penal[0]])
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x = Task.Funs[0]

    f = Task.Funs[1]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (x.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.MSD() ='+ stmp+'\n')
    tmp = (f.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tf.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tf.Complexity([Penal[0]]) ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
t21 = Set('t21',SvF.curentTabl.dat('t')[:].min(),SvF.curentTabl.dat('t')[:].max(),0.175,'','t')
x_f = Fun('x_f',[t21], param=True)
def fx_f(t21) : return x_f.F([t21])
sqrt_x_f__x=sqrt ( sum((fx_f(va)-fx(va))**2 for va in x_f.A[0].Val)/SvF.curentTabl.NoR)/x.V.sigma*100
print('\nSDz= ',sqrt_x_f__x,'NoR',SvF.curentTabl.NoR)
SvF.addStrToRes='SDz= '+str(sqrt_x_f__x)
x2 = Fun('x2',[t], param=True, ReadFrom="x2(t).sol")
def fx2(t) : return x2.F([t])
X2 = Set('X2',1.2,1.5,0.1,'','X2')
f2 = Fun('f2',[X2], param=True, ReadFrom="f2(X).sol")
def ff2(X2) : return f2.F([X2])
Reg=Polyline([-1,-1,2.5,2.5,-1],[-0.1,2.2,2.2,-0.1,-0.1],None,'Region')
x.V.oname="x1: (x'>0)"
x2.V.oname="x2: (x'<0)"
x2.V.draw_name='x'
Task.Draw ( 'Region;LC:green;LSt:dashed x;LC:r;LSt:solid x2;LC:b' )
f.V.oname="f1: (x'>0)"
f2.V.oname="f2: (x'<0)"
f2.V.draw_name='f'
f2.A[0].oname="x"
Line0=Polyline([-0.1,2],[0,0],None,'f=0')
Task.Draw ( 'f=0;LC:green;LSt:dashed f;LC:r;LSt:solid f2;LC:b' )