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
SvF.TaskName="Oscillator"; 
currentTab = Table ( 'Spring5.dat','currentTab','*' )
t = Set('t',SvF.currentTab.dat('t')[:].min(),SvF.currentTab.dat('t')[:].max(),0.025,'','t')
X = Set('X',-0.1,2.2,0.1,'','X')
V = Set('V',-1,1.5,0.1,'','V')
x = Fun('x',[t])
def fx(t) : return x.F([t])
v = Fun('v',[t])
def fv(t) : return v.F([t])
f = smbFun('f',[X,V], SymbolInteg=True)
def ff(X,V) : return f.F([X,V])
c = Tensor('c',[28])
def fc(i) : return c.F([i])
def f_smbF00(Args) :
   X = Args[0]
   V = Args[1]
   SvF.F_Arg_Type = "N"
   ret =  ( fc(0)+fc(1)*V+fc(2)*X+fc(3)*V**2+fc(4)*X*V+fc(5)*X**2+fc(6)*V**3+fc(7)*X*V**2+fc(8)*X**2*V+fc(9)*X**3+fc(10)*V**4+fc(11)*X*V**3+fc(12)*X**2*V**2+fc(13)*X**3*V+fc(14)*X**4+fc(15)*V**5+fc(16)*X*V**4+fc(17)*X**2*V**3+fc(18)*X**3*V**2+fc(19)*X**4*V+fc(20)*X**5+fc(21)*V**6+fc(22)*X*V**5+fc(23)*X**2*V**4+fc(24)*X**3*V**3+fc(25)*X**4*V**2+fc(26)*X**5*V+fc(27)*X**6 ) 
   SvF.F_Arg_Type = ""
   return ret
f.smbF = f_smbF00
def f_IntegDer200(Args) :
   X = Args[0]
   V = Args[1]
   SvF.F_Arg_Type = "N"
   ret = 4*V**9*X*fc(23)**2/9 + V**8*(3*X**2*fc(23)*fc(24)/2 + X*fc(17)*fc(23)) + V**7*(16*X**3*fc(23)*fc(25)/7 + 12*X**3*fc(24)**2/7 + 12*X**2*fc(17)*fc(24)/7 + 12*X**2*fc(18)*fc(23)/7 + 8*X*fc(12)*fc(23)/7 + 4*X*fc(17)**2/7) + V**6*(10*X**4*fc(23)*fc(26)/3 + 6*X**4*fc(24)*fc(25) + 8*X**3*fc(17)*fc(25)/3 + 4*X**3*fc(18)*fc(24) + 8*X**3*fc(19)*fc(23)/3 + 2*X**2*fc(12)*fc(24) + 2*X**2*fc(13)*fc(23) + 2*X**2*fc(17)*fc(18) + 4*X*fc(8)*fc(23)/3 + 4*X*fc(12)*fc(17)/3) + V**5*(24*X**5*fc(23)*fc(27)/5 + 48*X**5*fc(24)*fc(26)/5 + 144*X**5*fc(25)**2/25 + 4*X**4*fc(17)*fc(26) + 36*X**4*fc(18)*fc(25)/5 + 36*X**4*fc(19)*fc(24)/5 + 4*X**4*fc(20)*fc(23) + 16*X**3*fc(12)*fc(25)/5 + 24*X**3*fc(13)*fc(24)/5 + 16*X**3*fc(14)*fc(23)/5 + 16*X**3*fc(17)*fc(19)/5 + 12*X**3*fc(18)**2/5 + 12*X**2*fc(8)*fc(24)/5 + 12*X**2*fc(9)*fc(23)/5 + 12*X**2*fc(12)*fc(18)/5 + 12*X**2*fc(13)*fc(17)/5 + 8*X*fc(5)*fc(23)/5 + 8*X*fc(8)*fc(17)/5 + 4*X*fc(12)**2/5) + V**4*(15*X**6*fc(24)*fc(27) + 20*X**6*fc(25)*fc(26) + 6*X**5*fc(17)*fc(27) + 12*X**5*fc(18)*fc(26) + 72*X**5*fc(19)*fc(25)/5 + 12*X**5*fc(20)*fc(24) + 5*X**4*fc(12)*fc(26) + 9*X**4*fc(13)*fc(25) + 9*X**4*fc(14)*fc(24) + 5*X**4*fc(17)*fc(20) + 9*X**4*fc(18)*fc(19) + 4*X**3*fc(8)*fc(25) + 6*X**3*fc(9)*fc(24) + 4*X**3*fc(12)*fc(19) + 6*X**3*fc(13)*fc(18) + 4*X**3*fc(14)*fc(17) + 3*X**2*fc(5)*fc(24) + 3*X**2*fc(8)*fc(18) + 3*X**2*fc(9)*fc(17) + 3*X**2*fc(12)*fc(13) + 2*X*fc(5)*fc(17) + 2*X*fc(8)*fc(12)) + V**3*(240*X**7*fc(25)*fc(27)/7 + 400*X**7*fc(26)**2/21 + 20*X**6*fc(18)*fc(27) + 80*X**6*fc(19)*fc(26)/3 + 80*X**6*fc(20)*fc(25)/3 + 8*X**5*fc(12)*fc(27) + 16*X**5*fc(13)*fc(26) + 96*X**5*fc(14)*fc(25)/5 + 16*X**5*fc(18)*fc(20) + 48*X**5*fc(19)**2/5 + 20*X**4*fc(8)*fc(26)/3 + 12*X**4*fc(9)*fc(25) + 20*X**4*fc(12)*fc(20)/3 + 12*X**4*fc(13)*fc(19) + 12*X**4*fc(14)*fc(18) + 16*X**3*fc(5)*fc(25)/3 + 16*X**3*fc(8)*fc(19)/3 + 8*X**3*fc(9)*fc(18) + 16*X**3*fc(12)*fc(14)/3 + 4*X**3*fc(13)**2 + 4*X**2*fc(5)*fc(18) + 4*X**2*fc(8)*fc(13) + 4*X**2*fc(9)*fc(12) + 8*X*fc(5)*fc(12)/3 + 4*X*fc(8)**2/3) + V**2*(75*X**8*fc(26)*fc(27) + 360*X**7*fc(19)*fc(27)/7 + 400*X**7*fc(20)*fc(26)/7 + 30*X**6*fc(13)*fc(27) + 40*X**6*fc(14)*fc(26) + 40*X**6*fc(19)*fc(20) + 12*X**5*fc(8)*fc(27) + 24*X**5*fc(9)*fc(26) + 24*X**5*fc(13)*fc(20) + 144*X**5*fc(14)*fc(19)/5 + 10*X**4*fc(5)*fc(26) + 10*X**4*fc(8)*fc(20) + 18*X**4*fc(9)*fc(19) + 18*X**4*fc(13)*fc(14) + 8*X**3*fc(5)*fc(19) + 8*X**3*fc(8)*fc(14) + 12*X**3*fc(9)*fc(13) + 6*X**2*fc(5)*fc(13) + 6*X**2*fc(8)*fc(9) + 4*X*fc(5)*fc(8)) + V*(100*X**9*fc(27)**2 + 150*X**8*fc(20)*fc(27) + 720*X**7*fc(14)*fc(27)/7 + 400*X**7*fc(20)**2/7 + 60*X**6*fc(9)*fc(27) + 80*X**6*fc(14)*fc(20) + 24*X**5*fc(5)*fc(27) + 48*X**5*fc(9)*fc(20) + 144*X**5*fc(14)**2/5 + 20*X**4*fc(5)*fc(20) + 36*X**4*fc(9)*fc(14) + 16*X**3*fc(5)*fc(14) + 12*X**3*fc(9)**2 + 12*X**2*fc(5)*fc(9) + 4*X*fc(5)**2)
   SvF.F_Arg_Type = ""
   return ret
f.IntegDer2[0][0] = f_IntegDer200
def f_IntegDer201(Args) :
   X = Args[0]
   V = Args[1]
   SvF.F_Arg_Type = "N"
   ret = 25*V**9*X*fc(22)**2/9 + V**8*(5*X**2*fc(22)*fc(23) + 5*X*fc(16)*fc(22)) + V**7*(30*X**3*fc(22)*fc(24)/7 + 64*X**3*fc(23)**2/21 + 32*X**2*fc(16)*fc(23)/7 + 30*X**2*fc(17)*fc(22)/7 + 30*X*fc(11)*fc(22)/7 + 16*X*fc(16)**2/7) + V**6*(10*X**4*fc(22)*fc(25)/3 + 6*X**4*fc(23)*fc(24) + 4*X**3*fc(16)*fc(24) + 16*X**3*fc(17)*fc(23)/3 + 10*X**3*fc(18)*fc(22)/3 + 4*X**2*fc(11)*fc(23) + 10*X**2*fc(12)*fc(22)/3 + 4*X**2*fc(16)*fc(17) + 10*X*fc(7)*fc(22)/3 + 4*X*fc(11)*fc(16)) + V**5*(2*X**5*fc(22)*fc(26) + 128*X**5*fc(23)*fc(25)/25 + 81*X**5*fc(24)**2/25 + 16*X**4*fc(16)*fc(25)/5 + 27*X**4*fc(17)*fc(24)/5 + 24*X**4*fc(18)*fc(23)/5 + 2*X**4*fc(19)*fc(22) + 18*X**3*fc(11)*fc(24)/5 + 64*X**3*fc(12)*fc(23)/15 + 2*X**3*fc(13)*fc(22) + 16*X**3*fc(16)*fc(18)/5 + 12*X**3*fc(17)**2/5 + 16*X**2*fc(7)*fc(23)/5 + 2*X**2*fc(8)*fc(22) + 18*X**2*fc(11)*fc(17)/5 + 16*X**2*fc(12)*fc(16)/5 + 2*X*fc(4)*fc(22) + 16*X*fc(7)*fc(16)/5 + 9*X*fc(11)**2/5) + V**4*(10*X**6*fc(23)*fc(26)/3 + 6*X**6*fc(24)*fc(25) + 2*X**5*fc(16)*fc(26) + 24*X**5*fc(17)*fc(25)/5 + 27*X**5*fc(18)*fc(24)/5 + 16*X**5*fc(19)*fc(23)/5 + 3*X**4*fc(11)*fc(25) + 9*X**4*fc(12)*fc(24)/2 + 3*X**4*fc(13)*fc(23) + 2*X**4*fc(16)*fc(19) + 9*X**4*fc(17)*fc(18)/2 + 3*X**3*fc(7)*fc(24) + 8*X**3*fc(8)*fc(23)/3 + 3*X**3*fc(11)*fc(18) + 4*X**3*fc(12)*fc(17) + 2*X**3*fc(13)*fc(16) + 2*X**2*fc(4)*fc(23) + 3*X**2*fc(7)*fc(17) + 2*X**2*fc(8)*fc(16) + 3*X**2*fc(11)*fc(12) + 2*X*fc(4)*fc(16) + 3*X*fc(7)*fc(11)) + V**3*(30*X**7*fc(24)*fc(26)/7 + 64*X**7*fc(25)**2/21 + 10*X**6*fc(17)*fc(26)/3 + 16*X**6*fc(18)*fc(25)/3 + 4*X**6*fc(19)*fc(24) + 2*X**5*fc(11)*fc(26) + 64*X**5*fc(12)*fc(25)/15 + 18*X**5*fc(13)*fc(24)/5 + 16*X**5*fc(17)*fc(19)/5 + 12*X**5*fc(18)**2/5 + 8*X**4*fc(7)*fc(25)/3 + 3*X**4*fc(8)*fc(24) + 2*X**4*fc(11)*fc(19) + 4*X**4*fc(12)*fc(18) + 3*X**4*fc(13)*fc(17) + 2*X**3*fc(4)*fc(24) + 8*X**3*fc(7)*fc(18)/3 + 8*X**3*fc(8)*fc(17)/3 + 2*X**3*fc(11)*fc(13) + 16*X**3*fc(12)**2/9 + 2*X**2*fc(4)*fc(17) + 8*X**2*fc(7)*fc(12)/3 + 2*X**2*fc(8)*fc(11) + 2*X*fc(4)*fc(11) + 4*X*fc(7)**2/3) + V**2*(5*X**8*fc(25)*fc(26) + 30*X**7*fc(18)*fc(26)/7 + 32*X**7*fc(19)*fc(25)/7 + 10*X**6*fc(12)*fc(26)/3 + 4*X**6*fc(13)*fc(25) + 4*X**6*fc(18)*fc(19) + 2*X**5*fc(7)*fc(26) + 16*X**5*fc(8)*fc(25)/5 + 16*X**5*fc(12)*fc(19)/5 + 18*X**5*fc(13)*fc(18)/5 + 2*X**4*fc(4)*fc(25) + 2*X**4*fc(7)*fc(19) + 3*X**4*fc(8)*fc(18) + 3*X**4*fc(12)*fc(13) + 2*X**3*fc(4)*fc(18) + 2*X**3*fc(7)*fc(13) + 8*X**3*fc(8)*fc(12)/3 + 2*X**2*fc(4)*fc(12) + 2*X**2*fc(7)*fc(8) + 2*X*fc(4)*fc(7)) + V*(25*X**9*fc(26)**2/9 + 5*X**8*fc(19)*fc(26) + 30*X**7*fc(13)*fc(26)/7 + 16*X**7*fc(19)**2/7 + 10*X**6*fc(8)*fc(26)/3 + 4*X**6*fc(13)*fc(19) + 2*X**5*fc(4)*fc(26) + 16*X**5*fc(8)*fc(19)/5 + 9*X**5*fc(13)**2/5 + 2*X**4*fc(4)*fc(19) + 3*X**4*fc(8)*fc(13) + 2*X**3*fc(4)*fc(13) + 4*X**3*fc(8)**2/3 + 2*X**2*fc(4)*fc(8) + X*fc(4)**2)
   SvF.F_Arg_Type = ""
   return ret
f.IntegDer2[0][1] = f_IntegDer201
def f_IntegDer211(Args) :
   X = Args[0]
   V = Args[1]
   SvF.F_Arg_Type = "N"
   ret = 100*V**9*X*fc(21)**2 + V**8*(75*X**2*fc(21)*fc(22) + 150*X*fc(15)*fc(21)) + V**7*(240*X**3*fc(21)*fc(23)/7 + 400*X**3*fc(22)**2/21 + 400*X**2*fc(15)*fc(22)/7 + 360*X**2*fc(16)*fc(21)/7 + 720*X*fc(10)*fc(21)/7 + 400*X*fc(15)**2/7) + V**6*(15*X**4*fc(21)*fc(24) + 20*X**4*fc(22)*fc(23) + 80*X**3*fc(15)*fc(23)/3 + 80*X**3*fc(16)*fc(22)/3 + 20*X**3*fc(17)*fc(21) + 40*X**2*fc(10)*fc(22) + 30*X**2*fc(11)*fc(21) + 40*X**2*fc(15)*fc(16) + 60*X*fc(6)*fc(21) + 80*X*fc(10)*fc(15)) + V**5*(24*X**5*fc(21)*fc(25)/5 + 48*X**5*fc(22)*fc(24)/5 + 144*X**5*fc(23)**2/25 + 12*X**4*fc(15)*fc(24) + 72*X**4*fc(16)*fc(23)/5 + 12*X**4*fc(17)*fc(22) + 6*X**4*fc(18)*fc(21) + 96*X**3*fc(10)*fc(23)/5 + 16*X**3*fc(11)*fc(22) + 8*X**3*fc(12)*fc(21) + 16*X**3*fc(15)*fc(17) + 48*X**3*fc(16)**2/5 + 24*X**2*fc(6)*fc(22) + 12*X**2*fc(7)*fc(21) + 144*X**2*fc(10)*fc(16)/5 + 24*X**2*fc(11)*fc(15) + 24*X*fc(3)*fc(21) + 48*X*fc(6)*fc(15) + 144*X*fc(10)**2/5) + V**4*(10*X**6*fc(22)*fc(25)/3 + 6*X**6*fc(23)*fc(24) + 4*X**5*fc(15)*fc(25) + 36*X**5*fc(16)*fc(24)/5 + 36*X**5*fc(17)*fc(23)/5 + 4*X**5*fc(18)*fc(22) + 9*X**4*fc(10)*fc(24) + 9*X**4*fc(11)*fc(23) + 5*X**4*fc(12)*fc(22) + 5*X**4*fc(15)*fc(18) + 9*X**4*fc(16)*fc(17) + 12*X**3*fc(6)*fc(23) + 20*X**3*fc(7)*fc(22)/3 + 12*X**3*fc(10)*fc(17) + 12*X**3*fc(11)*fc(16) + 20*X**3*fc(12)*fc(15)/3 + 10*X**2*fc(3)*fc(22) + 18*X**2*fc(6)*fc(16) + 10*X**2*fc(7)*fc(15) + 18*X**2*fc(10)*fc(11) + 20*X*fc(3)*fc(15) + 36*X*fc(6)*fc(10)) + V**3*(16*X**7*fc(23)*fc(25)/7 + 12*X**7*fc(24)**2/7 + 8*X**6*fc(16)*fc(25)/3 + 4*X**6*fc(17)*fc(24) + 8*X**6*fc(18)*fc(23)/3 + 16*X**5*fc(10)*fc(25)/5 + 24*X**5*fc(11)*fc(24)/5 + 16*X**5*fc(12)*fc(23)/5 + 16*X**5*fc(16)*fc(18)/5 + 12*X**5*fc(17)**2/5 + 6*X**4*fc(6)*fc(24) + 4*X**4*fc(7)*fc(23) + 4*X**4*fc(10)*fc(18) + 6*X**4*fc(11)*fc(17) + 4*X**4*fc(12)*fc(16) + 16*X**3*fc(3)*fc(23)/3 + 8*X**3*fc(6)*fc(17) + 16*X**3*fc(7)*fc(16)/3 + 16*X**3*fc(10)*fc(12)/3 + 4*X**3*fc(11)**2 + 8*X**2*fc(3)*fc(16) + 12*X**2*fc(6)*fc(11) + 8*X**2*fc(7)*fc(10) + 16*X*fc(3)*fc(10) + 12*X*fc(6)**2) + V**2*(3*X**8*fc(24)*fc(25)/2 + 12*X**7*fc(17)*fc(25)/7 + 12*X**7*fc(18)*fc(24)/7 + 2*X**6*fc(11)*fc(25) + 2*X**6*fc(12)*fc(24) + 2*X**6*fc(17)*fc(18) + 12*X**5*fc(6)*fc(25)/5 + 12*X**5*fc(7)*fc(24)/5 + 12*X**5*fc(11)*fc(18)/5 + 12*X**5*fc(12)*fc(17)/5 + 3*X**4*fc(3)*fc(24) + 3*X**4*fc(6)*fc(18) + 3*X**4*fc(7)*fc(17) + 3*X**4*fc(11)*fc(12) + 4*X**3*fc(3)*fc(17) + 4*X**3*fc(6)*fc(12) + 4*X**3*fc(7)*fc(11) + 6*X**2*fc(3)*fc(11) + 6*X**2*fc(6)*fc(7) + 12*X*fc(3)*fc(6)) + V*(4*X**9*fc(25)**2/9 + X**8*fc(18)*fc(25) + 8*X**7*fc(12)*fc(25)/7 + 4*X**7*fc(18)**2/7 + 4*X**6*fc(7)*fc(25)/3 + 4*X**6*fc(12)*fc(18)/3 + 8*X**5*fc(3)*fc(25)/5 + 8*X**5*fc(7)*fc(18)/5 + 4*X**5*fc(12)**2/5 + 2*X**4*fc(3)*fc(18) + 2*X**4*fc(7)*fc(12) + 8*X**3*fc(3)*fc(12)/3 + 4*X**3*fc(7)**2/3 + 4*X**2*fc(3)*fc(7) + 4*X*fc(3)**2)
   SvF.F_Arg_Type = ""
   return ret
f.IntegDer2[1][1] = f_IntegDer211
CVmakeSets (  CV_NumSets=7 )
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

    c.var = py.Var ( range (c.Sizes[0]),domain=Reals )
    c.gr =  c.var
    Gr.c =  c.var
 								# x''=f(x,v)
    def EQ0 (Gr,_it) :
        return (
          x.by_xx(_it)==ff(fx(_it),fv(_it))
        )
    Gr.conEQ0 = py.Constraint(t.mFlNodSm,rule=EQ0 )
 								# v=x'
    def EQ1 (Gr,_it) :
        return (
          fv(_it)==x.by_x(_it)
        )
    Gr.conEQ1 = py.Constraint(t.FlNodSm,rule=EQ1 )

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('x'))
    if x.mu is None : x.mu = Gr.mu0
    x.ValidationSets = SvF.ValidationSets
    x.notTrainingSets = SvF.notTrainingSets
    x.TrainingSets = SvF.TrainingSets
 											# f.Complexity([Penal[0],Penal[1]])+x.MSD()
    def obj_expression(Gr):  
        return (
             f.Complexity([Penal[0],Penal[1]])+x.MSD()
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
    tmp = (f.Complexity([Penal[0],Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tf.Complexity([Penal[0],Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tf.Complexity([Penal[0],Penal[1]]) ='+ stmp+'\n')
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
Task.PlotAll ( )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")