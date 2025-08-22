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
SvF.mngF = 'MNG-Fourier.mng'
SvF.CVNumOfIter = 31
Table ( 'Spring5.dat','curentTabl','*' )
t = Set('t',SvF.curentTabl.dat('t')[:].min(),SvF.curentTabl.dat('t')[:].max(),0.025,'','t')
c = Tensor('c',[5])
def fc(i) : return c.F([i])
ω = Tensor('ω',[])
def fω() : return ω.F([])
x = smbFun('x',[t])
def fx(t) : return x.F([t])
def x_smbF(Args) :
   t = Args[0]
   return fc(0)/2+fc(1)*py.cos(fω()*1*t)+fc(2)*py.sin(fω()*1*t)+fc(3)*py.cos(fω()*2*t)+fc(4)*py.sin(fω()*2*t)
x.smbF = x_smbF
def x_smbFx(Args) :
   t = Args[0]
   return -fω()*fc(1)*py.sin(t*fω()) + fω()*fc(2)*py.cos(t*fω()) - 2*fω()*fc(3)*py.sin(2*t*fω()) + 2*fω()*fc(4)*py.cos(2*t*fω()) 
x.smbFx = x_smbFx
def x_smbFxx(Args) :
   t = Args[0]
   return -fω()**2*fc(1)*py.cos(t*fω()) - fω()**2*fc(2)*py.sin(t*fω()) - 4*fω()**2*fc(3)*py.cos(2*t*fω()) - 4*fω()**2*fc(4)*py.sin(2*t*fω()) 
x.smbFxx = x_smbFxx
def x_Int_smbFxx_2(Args) :
   t = Args[0]
   return t*fω()**4*fc(1)**2*py.sin(t*fω())**2/2 + t*fω()**4*fc(1)**2*py.cos(t*fω())**2/2 + t*fω()**4*fc(2)**2*py.sin(t*fω())**2/2 + t*fω()**4*fc(2)**2*py.cos(t*fω())**2/2 + 8*t*fω()**4*fc(3)**2*py.sin(2*t*fω())**2 + 8*t*fω()**4*fc(3)**2*py.cos(2*t*fω())**2 + 8*t*fω()**4*fc(4)**2*py.sin(2*t*fω())**2 + 8*t*fω()**4*fc(4)**2*py.cos(2*t*fω())**2 + fω()**3*fc(1)**2*py.sin(t*fω())*py.cos(t*fω())/2 - fω()**3*fc(1)*fc(2)*py.cos(t*fω())**2 - 8*fω()**3*fc(1)*fc(3)*py.sin(t*fω())*py.cos(2*t*fω())/3 + 16*fω()**3*fc(1)*fc(3)*py.sin(2*t*fω())*py.cos(t*fω())/3 - 8*fω()**3*fc(1)*fc(4)*py.sin(t*fω())*py.sin(2*t*fω())/3 - 16*fω()**3*fc(1)*fc(4)*py.cos(t*fω())*py.cos(2*t*fω())/3 - fω()**3*fc(2)**2*py.sin(t*fω())*py.cos(t*fω())/2 + 16*fω()**3*fc(2)*fc(3)*py.sin(t*fω())*py.sin(2*t*fω())/3 + 8*fω()**3*fc(2)*fc(3)*py.cos(t*fω())*py.cos(2*t*fω())/3 - 16*fω()**3*fc(2)*fc(4)*py.sin(t*fω())*py.cos(2*t*fω())/3 + 8*fω()**3*fc(2)*fc(4)*py.sin(2*t*fω())*py.cos(t*fω())/3 + 4*fω()**3*fc(3)**2*py.sin(2*t*fω())*py.cos(2*t*fω()) + 8*fω()**3*fc(3)*fc(4)*py.sin(2*t*fω())**2 - 4*fω()**3*fc(4)**2*py.sin(2*t*fω())*py.cos(2*t*fω())
x.Int_smbFxx_2 = x_Int_smbFxx_2
CVmakeSets ( CV_NumSets=21 )
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    c.var = py.Var ( range (c.Sizes[0]),domain=Reals )
    Gr.c =  c.var

    ω.var = py.Var ( domain=Reals )
    Gr.ω =  ω.var

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

    x = Task.Funs[2]

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