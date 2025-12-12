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
currentTab = Table ( 'Spring5.dat','currentTab','*' )
t = Set('t',SvF.currentTab.dat('t')[:].min(),SvF.currentTab.dat('t')[:].max(),0.025,'','t')
c = Tensor('c',[5])
def fc(i) : return c.F([i])
ω = Tensor('ω',[])
def fω() : return ω.F([])
b = Tensor('b',[6])
def fb(i) : return b.F([i])
x = smbFun('x',[t], SymbolInteg=False)
def fx(t) : return x.F([t])
def x_smbF00(Args) :
   t = Args[0]
   SvF.F_Arg_Type = "N"
   ret =  ( fc(0)/2+fc(1)*py.cos(fω()*1*t)+fc(2)*py.sin(fω()*1*t)+fc(3)*py.cos(fω()*2*t)+fc(4)*py.sin(fω()*2*t) ) + ( fb(0)+fb(1)*t+fb(2)*t**2+fb(3)*t**3+fb(4)*t**4+fb(5)*t**5 ) 
   SvF.F_Arg_Type = ""
   return ret
x.smbF = x_smbF00
CVmakeSets (  CV_NumSets=21 )
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    c.var = py.Var ( range (c.Sizes[0]),domain=Reals )
    c.gr =  c.var
    Gr.c =  c.var

    ω.var = py.Var ( domain=Reals, bounds=(0,None) )
    ω.gr =  ω.var
    Gr.ω =  ω.var

    b.var = py.Var ( range (b.Sizes[0]),domain=Reals )
    b.gr =  b.var
    Gr.b =  b.var

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

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")