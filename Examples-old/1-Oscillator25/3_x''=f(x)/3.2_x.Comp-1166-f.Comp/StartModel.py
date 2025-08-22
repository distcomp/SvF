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
SvF.CVNumOfIter = 1
SvF.OptStep=[0.0001,0.0001]
Table ( 'Spring5.dat','curentTabl','t,x' )
t = Set('t',SvF.curentTabl.dat('t')[:].min(),SvF.curentTabl.dat('t')[:].max(),0.025,'','t')
X = Set('X',-0.1,2.2,0.1,'','X')
x = Fun('x',[t])
def fx(t) : return x.F([t])
f = smbFun('f',[X])
def ff(X) : return f.F([X])
c_f = Tensor('c_f',[7])
def fc_f(i) : return c_f.F([i])
def f_smbF(Args) :
   X = Args[0]
   return fc_f(0)+fc_f(1)*X+fc_f(2)*X**2+fc_f(3)*X**3+fc_f(4)*X**4+fc_f(5)*X**5+fc_f(6)*X**6
f.smbF = f_smbF
def f_smbFx(Args) :
   X = Args[0]
   return 6*X**5*fc_f(6) + 5*X**4*fc_f(5) + 4*X**3*fc_f(4) + 3*X**2*fc_f(3) + 2*X*fc_f(2) + fc_f(1) 
f.smbFx = f_smbFx
def f_smbFxx(Args) :
   X = Args[0]
   return 30*X**4*fc_f(6) + 20*X**3*fc_f(5) + 12*X**2*fc_f(4) + 6*X*fc_f(3) + 2*fc_f(2) 
f.smbFxx = f_smbFxx
def f_Int_smbFxx_2(Args) :
   X = Args[0]
   return 100*X**9*fc_f(6)**2 + 150*X**8*fc_f(5)*fc_f(6) + X**7*(720*fc_f(4)*fc_f(6)/7 + 400*fc_f(5)**2/7) + X**6*(60*fc_f(3)*fc_f(6) + 80*fc_f(4)*fc_f(5)) + X**5*(24*fc_f(2)*fc_f(6) + 48*fc_f(3)*fc_f(5) + 144*fc_f(4)**2/5) + X**4*(20*fc_f(2)*fc_f(5) + 36*fc_f(3)*fc_f(4)) + X**3*(16*fc_f(2)*fc_f(4) + 12*fc_f(3)**2) + 12*X**2*fc_f(2)*fc_f(3) + 4*X*fc_f(2)**2
f.Int_smbFxx_2 = f_Int_smbFxx_2
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

    c_f.var = py.Var ( range (c_f.Sizes[0]),domain=Reals )
    Gr.c_f =  c_f.var

    f.var = py.Var ( f.A[0].NodS,domain=Reals )
    Gr.f =  f.var
 								# d2/dt2(x)==f(x)
    def EQ0 (Gr,_it) :
        return (
          ((fx((_it+t.step))+fx((_it-t.step))-2*fx(_it))/t.step**2)==ff(fx(_it))
        )
    Gr.conEQ0 = py.Constraint(t.mFlNodSm,rule=EQ0 )

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('x'))
    if x.mu is None : x.mu = Gr.mu0
    x.ValidationSets = SvF.ValidationSets
    x.notTrainingSets = SvF.notTrainingSets
    x.TrainingSets = SvF.TrainingSets
 											# x.Complexity([Penal[0]])+f.Complexity([Penal[1]])+x.MSD()
    def obj_expression(Gr):  
        return (
             x.Complexity([Penal[0]])+f.Complexity([Penal[1]])+x.MSD()
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
    tmp = (x.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.Complexity([Penal[0]]) ='+ stmp+'\n')
    tmp = (f.Complexity([Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tf.Complexity([Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tf.Complexity([Penal[1]]) ='+ stmp+'\n')
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
f.A[0].oname='x'
Task.Draw ( 'f' )