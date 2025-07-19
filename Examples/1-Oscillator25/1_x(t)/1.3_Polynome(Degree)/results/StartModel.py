# -*- coding: UTF-8 -*-
import sys
path_SvF = "/home/vvv/git_work_dev/SvF/"
sys.path.append("/home/vvv/git_work_dev/SvF/SvFlib")
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
SvF.mngF = 'MNG-short-8.mng'
SvF.CVNumOfIter = 31
Table ( 'Spring5.dat','curentTabl','*' )
t = Set('t',SvF.curentTabl.dat('t')[:].min(),SvF.curentTabl.dat('t')[:].max(),0.025,'','t')
b = Tensor('b',[9])
def fb(i) : return b.F([i])
x = smbFun('x',[t])
def fx(t) : return x.F([t])
def x_smbF(Args) :
   t = Args[0]
   return fb(0)+fb(1)*t+fb(2)*t**2+fb(3)*t**3+fb(4)*t**4+fb(5)*t**5+fb(6)*t**6+fb(7)*t**7+fb(8)*t**8
x.smbF = x_smbF
def x_smbFx(Args) :
   t = Args[0]
   return 8*t**7*fb(8) + 7*t**6*fb(7) + 6*t**5*fb(6) + 5*t**4*fb(5) + 4*t**3*fb(4) + 3*t**2*fb(3) + 2*t*fb(2) + fb(1) 
x.smbFx = x_smbFx
def x_smbFxx(Args) :
   t = Args[0]
   return 56*t**6*fb(8) + 42*t**5*fb(7) + 30*t**4*fb(6) + 20*t**3*fb(5) + 12*t**2*fb(4) + 6*t*fb(3) + 2*fb(2) 
x.smbFxx = x_smbFxx
def x_Int_smbFxx_2(Args) :
   t = Args[0]
   return 3136*t**13*fb(8)**2/13 + 392*t**12*fb(7)*fb(8) + t**11*(3360*fb(6)*fb(8)/11 + 1764*fb(7)**2/11) + t**10*(224*fb(5)*fb(8) + 252*fb(6)*fb(7)) + t**9*(448*fb(4)*fb(8)/3 + 560*fb(5)*fb(7)/3 + 100*fb(6)**2) + t**8*(84*fb(3)*fb(8) + 126*fb(4)*fb(7) + 150*fb(5)*fb(6)) + t**7*(32*fb(2)*fb(8) + 72*fb(3)*fb(7) + 720*fb(4)*fb(6)/7 + 400*fb(5)**2/7) + t**6*(28*fb(2)*fb(7) + 60*fb(3)*fb(6) + 80*fb(4)*fb(5)) + t**5*(24*fb(2)*fb(6) + 48*fb(3)*fb(5) + 144*fb(4)**2/5) + t**4*(20*fb(2)*fb(5) + 36*fb(3)*fb(4)) + t**3*(16*fb(2)*fb(4) + 12*fb(3)**2) + 12*t**2*fb(2)*fb(3) + 4*t*fb(2)**2
x.Int_smbFxx_2 = x_Int_smbFxx_2
CVmakeSets ( CV_NumSets=21 )
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    b.var = py.Var ( range (b.Sizes[0]),domain=Reals )
    Gr.b =  b.var

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

    x = Task.Funs[1]

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