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
currentTab = Table ( 'Spring5.dat','currentTab','*' )
t = Set('t',SvF.currentTab.dat('t')[:].min(),SvF.currentTab.dat('t')[:].max(),0.025,'','t')
X = Set('X',0.,2.0,0.1,'','X')
x = smbFun('x',[t])
def fx(t) : return x.F([t])
c_x = Tensor('c_x',[7])
def fc_x(i) : return c_x.F([i])
def x_smbF00(Args) :
   t = Args[0]
   SvF.F_Arg_Type = "N"
   ret =  ( fc_x(0)+fc_x(1)*t+fc_x(2)*t**2+fc_x(3)*t**3+fc_x(4)*t**4+fc_x(5)*t**5+fc_x(6)*t**6 ) 
   SvF.F_Arg_Type = ""
   return ret
x.smbF = x_smbF00
f = smbFun('f',[X])
def ff(X) : return f.F([X])
c_f = Tensor('c_f',[7])
def fc_f(i) : return c_f.F([i])
def f_smbF00(Args) :
   X = Args[0]
   SvF.F_Arg_Type = "N"
   ret =  ( fc_f(0)+fc_f(1)*X+fc_f(2)*X**2+fc_f(3)*X**3+fc_f(4)*X**4+fc_f(5)*X**5+fc_f(6)*X**6 ) 
   SvF.F_Arg_Type = ""
   return ret
f.smbF = f_smbF00
CVmakeSets (  CV_NumSets=7 )
SvF.CVNumOfIter=1; SvF.RunMode="P&P"; 
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    c_x.var = py.Var ( range (c_x.Sizes[0]),domain=Reals )
    c_x.gr =  c_x.var
    Gr.c_x =  c_x.var

    c_f.var = py.Var ( range (c_f.Sizes[0]),domain=Reals )
    c_f.gr =  c_f.var
    Gr.c_f =  c_f.var
 								# d2/dt2(x)-f(x)>-.01
    def EQ0 (Gr,_it) :
        return (
          x.by_xx(_it)-ff(fx(_it))>=-.01
        )
    Gr.conEQ0 = py.Constraint(t.mFlNodSm,rule=EQ0 )
 								# x''-f(x)<.01
    def EQ1 (Gr,_it) :
        return (
          x.by_xx(_it)-ff(fx(_it))<=.01
        )
    Gr.conEQ1 = py.Constraint(t.mFlNodSm,rule=EQ1 )

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('x'))
    if x.mu is None : x.mu = Gr.mu0
    x.ValidationSets = SvF.ValidationSets
    x.notTrainingSets = SvF.notTrainingSets
    x.TrainingSets = SvF.TrainingSets
 											# f.Complexity([Penal[0]])+x.MSD()
    def obj_expression(Gr):  
        return (
             f.Complexity([Penal[0]])+x.MSD()
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x = Task.Funs[0]

    f = Task.Funs[2]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (f.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tf.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tf.Complexity([Penal[0]]) ='+ stmp+'\n')
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
Plot( [ [ x] ] )
Plot( [ [ f] ] )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")