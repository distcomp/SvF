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
SvF.mngF = 'MNG-short.mng'
SvF.CVNumOfIter = 0
Table ( 'Spring5.dat','curentTabl','*' )
t = Set('t',SvF.curentTabl.dat('t')[:].min(),SvF.curentTabl.dat('t')[:].max(),0.025,'','t')
K = Tensor('K',[])
def fK() : return K.F([])
muu = Tensor('muu',[])
def fmuu() : return muu.F([])
xr = Tensor('xr',[])
def fxr() : return xr.F([])
x = smbFun('x',[t])
def fx(t) : return x.F([t])
def x_smbF(Args) :
   t = Args[0]
   return py.sin(py.sqrt(fK())*t)*py.exp(-fmuu()/2*t)+fxr()
x.smbF = x_smbF
def x_smbFx(Args) :
   t = Args[0]
   return py.sqrt(fK())*py.exp(-fmuu()*t/2)*py.cos(py.sqrt(fK())*t) - fmuu()*py.exp(-fmuu()*t/2)*py.sin(py.sqrt(fK())*t)/2 
x.smbFx = x_smbFx
def x_smbFxx(Args) :
   t = Args[0]
   return -py.sqrt(fK())*fmuu()*py.exp(-fmuu()*t/2)*py.cos(py.sqrt(fK())*t) - fK()*py.exp(-fmuu()*t/2)*py.sin(py.sqrt(fK())*t) + fmuu()**2*py.exp(-fmuu()*t/2)*py.sin(py.sqrt(fK())*t)/4 
x.smbFxx = x_smbFxx
CVmakeSets ( CV_NumSets=21 )
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    K.var = py.Var ( domain=Reals )
    Gr.K =  K.var

    muu.var = py.Var ( domain=Reals )
    Gr.muu =  muu.var

    xr.var = py.Var ( domain=Reals )
    Gr.xr =  xr.var

    x.var = py.Var ( x.A[0].NodS,domain=Reals )
    Gr.x =  x.var

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('x'))
    if x.mu is None : x.mu = Gr.mu0
    x.ValidationSets = SvF.ValidationSets
    x.notTrainingSets = SvF.notTrainingSets
    x.TrainingSets = SvF.TrainingSets
 											# x.MSD()+x.Complexity([Penal[0]])
    def obj_expression(Gr):  
        return (
             x.MSD()+x.Complexity([Penal[0]])
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x = Task.Funs[3]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (x.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.MSD() ='+ stmp+'\n')
    tmp = (x.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.Complexity([Penal[0]]) ='+ stmp+'\n')

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