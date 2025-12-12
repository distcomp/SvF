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
SvF.CVNumOfIter = 1
Table ( 'Spring5.dat','curentTabl','t,x' )
t = Set('t',SvF.curentTabl.dat('t')[:].min(),SvF.curentTabl.dat('t')[:].max(),0.025,'','t')
X = Set('X',-0.1,2.2,0.1,'','X')
V = Set('V',-1,1.5,0.1,'','V')
x = Fun('x',[t])
def fx(t) : return x.F([t])
v = Fun('v',[t])
def fv(t) : return v.F([t])
f = smbFun('f',[X,V])
def ff(X,V) : return f.F([X,V])
c_f = Tensor('c_f',[28])
def fc_f(i) : return c_f.F([i])
def f_smbF(Args) :
   X = Args[0]
   V = Args[1]
   return fc_f(0)+fc_f(1)*V+fc_f(2)*X+fc_f(3)*V**2+fc_f(4)*X*V+fc_f(5)*X**2+fc_f(6)*V**3+fc_f(7)*X*V**2+fc_f(8)*X**2*V+fc_f(9)*X**3+fc_f(10)*V**4+fc_f(11)*X*V**3+fc_f(12)*X**2*V**2+fc_f(13)*X**3*V+fc_f(14)*X**4+fc_f(15)*V**5+fc_f(16)*X*V**4+fc_f(17)*X**2*V**3+fc_f(18)*X**3*V**2+fc_f(19)*X**4*V+fc_f(20)*X**5+fc_f(21)*V**6+fc_f(22)*X*V**5+fc_f(23)*X**2*V**4+fc_f(24)*X**3*V**3+fc_f(25)*X**4*V**2+fc_f(26)*X**5*V+fc_f(27)*X**6
f.smbF = f_smbF
def f_smbFx(Args) :
   X = Args[0]
   V = Args[1]
   return V**5*fc_f(22) + 2*V**4*X*fc_f(23) + V**4*fc_f(16) + 3*V**3*X**2*fc_f(24) + 2*V**3*X*fc_f(17) + V**3*fc_f(11) + 4*V**2*X**3*fc_f(25) + 3*V**2*X**2*fc_f(18) + 2*V**2*X*fc_f(12) + V**2*fc_f(7) + 5*V*X**4*fc_f(26) + 4*V*X**3*fc_f(19) + 3*V*X**2*fc_f(13) + 2*V*X*fc_f(8) + V*fc_f(4) + 6*X**5*fc_f(27) + 5*X**4*fc_f(20) + 4*X**3*fc_f(14) + 3*X**2*fc_f(9) + 2*X*fc_f(5) + fc_f(2) 
f.smbFx = f_smbFx
def f_smbFxx(Args) :
   X = Args[0]
   V = Args[1]
   return 2*V**4*fc_f(23) + 6*V**3*X*fc_f(24) + 2*V**3*fc_f(17) + 12*V**2*X**2*fc_f(25) + 6*V**2*X*fc_f(18) + 2*V**2*fc_f(12) + 20*V*X**3*fc_f(26) + 12*V*X**2*fc_f(19) + 6*V*X*fc_f(13) + 2*V*fc_f(8) + 30*X**4*fc_f(27) + 20*X**3*fc_f(20) + 12*X**2*fc_f(14) + 6*X*fc_f(9) + 2*fc_f(5) 
f.smbFxx = f_smbFxx
def f_Int_smbFxx_2(Args) :
   X = Args[0]
   V = Args[1]
   return 100*X**9*fc_f(27)**2 + X**8*(150*V*fc_f(26)*fc_f(27) + 150*fc_f(20)*fc_f(27)) + X**7*(720*V**2*fc_f(25)*fc_f(27)/7 + 400*V**2*fc_f(26)**2/7 + 720*V*fc_f(19)*fc_f(27)/7 + 800*V*fc_f(20)*fc_f(26)/7 + 720*fc_f(14)*fc_f(27)/7 + 400*fc_f(20)**2/7) + X**6*(60*V**3*fc_f(24)*fc_f(27) + 80*V**3*fc_f(25)*fc_f(26) + 60*V**2*fc_f(18)*fc_f(27) + 80*V**2*fc_f(19)*fc_f(26) + 80*V**2*fc_f(20)*fc_f(25) + 60*V*fc_f(13)*fc_f(27) + 80*V*fc_f(14)*fc_f(26) + 80*V*fc_f(19)*fc_f(20) + 60*fc_f(9)*fc_f(27) + 80*fc_f(14)*fc_f(20)) + X**5*(24*V**4*fc_f(23)*fc_f(27) + 48*V**4*fc_f(24)*fc_f(26) + 144*V**4*fc_f(25)**2/5 + 24*V**3*fc_f(17)*fc_f(27) + 48*V**3*fc_f(18)*fc_f(26) + 288*V**3*fc_f(19)*fc_f(25)/5 + 48*V**3*fc_f(20)*fc_f(24) + 24*V**2*fc_f(12)*fc_f(27) + 48*V**2*fc_f(13)*fc_f(26) + 288*V**2*fc_f(14)*fc_f(25)/5 + 48*V**2*fc_f(18)*fc_f(20) + 144*V**2*fc_f(19)**2/5 + 24*V*fc_f(8)*fc_f(27) + 48*V*fc_f(9)*fc_f(26) + 48*V*fc_f(13)*fc_f(20) + 288*V*fc_f(14)*fc_f(19)/5 + 24*fc_f(5)*fc_f(27) + 48*fc_f(9)*fc_f(20) + 144*fc_f(14)**2/5) + X**4*(20*V**5*fc_f(23)*fc_f(26) + 36*V**5*fc_f(24)*fc_f(25) + 20*V**4*fc_f(17)*fc_f(26) + 36*V**4*fc_f(18)*fc_f(25) + 36*V**4*fc_f(19)*fc_f(24) + 20*V**4*fc_f(20)*fc_f(23) + 20*V**3*fc_f(12)*fc_f(26) + 36*V**3*fc_f(13)*fc_f(25) + 36*V**3*fc_f(14)*fc_f(24) + 20*V**3*fc_f(17)*fc_f(20) + 36*V**3*fc_f(18)*fc_f(19) + 20*V**2*fc_f(8)*fc_f(26) + 36*V**2*fc_f(9)*fc_f(25) + 20*V**2*fc_f(12)*fc_f(20) + 36*V**2*fc_f(13)*fc_f(19) + 36*V**2*fc_f(14)*fc_f(18) + 20*V*fc_f(5)*fc_f(26) + 20*V*fc_f(8)*fc_f(20) + 36*V*fc_f(9)*fc_f(19) + 36*V*fc_f(13)*fc_f(14) + 20*fc_f(5)*fc_f(20) + 36*fc_f(9)*fc_f(14)) + X**3*(16*V**6*fc_f(23)*fc_f(25) + 12*V**6*fc_f(24)**2 + 16*V**5*fc_f(17)*fc_f(25) + 24*V**5*fc_f(18)*fc_f(24) + 16*V**5*fc_f(19)*fc_f(23) + 16*V**4*fc_f(12)*fc_f(25) + 24*V**4*fc_f(13)*fc_f(24) + 16*V**4*fc_f(14)*fc_f(23) + 16*V**4*fc_f(17)*fc_f(19) + 12*V**4*fc_f(18)**2 + 16*V**3*fc_f(8)*fc_f(25) + 24*V**3*fc_f(9)*fc_f(24) + 16*V**3*fc_f(12)*fc_f(19) + 24*V**3*fc_f(13)*fc_f(18) + 16*V**3*fc_f(14)*fc_f(17) + 16*V**2*fc_f(5)*fc_f(25) + 16*V**2*fc_f(8)*fc_f(19) + 24*V**2*fc_f(9)*fc_f(18) + 16*V**2*fc_f(12)*fc_f(14) + 12*V**2*fc_f(13)**2 + 16*V*fc_f(5)*fc_f(19) + 16*V*fc_f(8)*fc_f(14) + 24*V*fc_f(9)*fc_f(13) + 16*fc_f(5)*fc_f(14) + 12*fc_f(9)**2) + X**2*(12*V**7*fc_f(23)*fc_f(24) + 12*V**6*fc_f(17)*fc_f(24) + 12*V**6*fc_f(18)*fc_f(23) + 12*V**5*fc_f(12)*fc_f(24) + 12*V**5*fc_f(13)*fc_f(23) + 12*V**5*fc_f(17)*fc_f(18) + 12*V**4*fc_f(8)*fc_f(24) + 12*V**4*fc_f(9)*fc_f(23) + 12*V**4*fc_f(12)*fc_f(18) + 12*V**4*fc_f(13)*fc_f(17) + 12*V**3*fc_f(5)*fc_f(24) + 12*V**3*fc_f(8)*fc_f(18) + 12*V**3*fc_f(9)*fc_f(17) + 12*V**3*fc_f(12)*fc_f(13) + 12*V**2*fc_f(5)*fc_f(18) + 12*V**2*fc_f(8)*fc_f(13) + 12*V**2*fc_f(9)*fc_f(12) + 12*V*fc_f(5)*fc_f(13) + 12*V*fc_f(8)*fc_f(9) + 12*fc_f(5)*fc_f(9)) + X*(4*V**8*fc_f(23)**2 + 8*V**7*fc_f(17)*fc_f(23) + 8*V**6*fc_f(12)*fc_f(23) + 4*V**6*fc_f(17)**2 + 8*V**5*fc_f(8)*fc_f(23) + 8*V**5*fc_f(12)*fc_f(17) + 8*V**4*fc_f(5)*fc_f(23) + 8*V**4*fc_f(8)*fc_f(17) + 4*V**4*fc_f(12)**2 + 8*V**3*fc_f(5)*fc_f(17) + 8*V**3*fc_f(8)*fc_f(12) + 8*V**2*fc_f(5)*fc_f(12) + 4*V**2*fc_f(8)**2 + 8*V*fc_f(5)*fc_f(8) + 4*fc_f(5)**2)
f.Int_smbFxx_2 = f_Int_smbFxx_2
def f_smbFy(Args) :
   X = Args[0]
   V = Args[1]
   return 6*V**5*fc_f(21) + 5*V**4*X*fc_f(22) + 5*V**4*fc_f(15) + 4*V**3*X**2*fc_f(23) + 4*V**3*X*fc_f(16) + 4*V**3*fc_f(10) + 3*V**2*X**3*fc_f(24) + 3*V**2*X**2*fc_f(17) + 3*V**2*X*fc_f(11) + 3*V**2*fc_f(6) + 2*V*X**4*fc_f(25) + 2*V*X**3*fc_f(18) + 2*V*X**2*fc_f(12) + 2*V*X*fc_f(7) + 2*V*fc_f(3) + X**5*fc_f(26) + X**4*fc_f(19) + X**3*fc_f(13) + X**2*fc_f(8) + X*fc_f(4) + fc_f(1) 
f.smbFy = f_smbFy
def f_smbFxy(Args) :
   X = Args[0]
   V = Args[1]
   return 5*V**4*fc_f(22) + 8*V**3*X*fc_f(23) + 4*V**3*fc_f(16) + 9*V**2*X**2*fc_f(24) + 6*V**2*X*fc_f(17) + 3*V**2*fc_f(11) + 8*V*X**3*fc_f(25) + 6*V*X**2*fc_f(18) + 4*V*X*fc_f(12) + 2*V*fc_f(7) + 5*X**4*fc_f(26) + 4*X**3*fc_f(19) + 3*X**2*fc_f(13) + 2*X*fc_f(8) + fc_f(4) 
f.smbFxy = f_smbFxy
def f_smbFyy(Args) :
   X = Args[0]
   V = Args[1]
   return 30*V**4*fc_f(21) + 20*V**3*X*fc_f(22) + 20*V**3*fc_f(15) + 12*V**2*X**2*fc_f(23) + 12*V**2*X*fc_f(16) + 12*V**2*fc_f(10) + 6*V*X**3*fc_f(24) + 6*V*X**2*fc_f(17) + 6*V*X*fc_f(11) + 6*V*fc_f(6) + 2*X**4*fc_f(25) + 2*X**3*fc_f(18) + 2*X**2*fc_f(12) + 2*X*fc_f(7) + 2*fc_f(3) 
f.smbFyy = f_smbFyy
try: Px
except NameError: Px = None
SvF.Penalty.append(Px)
try: Pfx
except NameError: Pfx = None
SvF.Penalty.append(Pfx)
try: Pfv
except NameError: Pfv = None
SvF.Penalty.append(Pfv)
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

    v.var = py.Var ( v.A[0].NodS,domain=Reals )
    Gr.v =  v.var

    c_f.var = py.Var ( range (c_f.Sizes[0]),domain=Reals )
    Gr.c_f =  c_f.var

    f.var = py.Var ( f.A[0].NodS,f.A[1].NodS,domain=Reals )
    Gr.f =  f.var
 								# d2/dt2(x)==f(x,v)
    def EQ0 (Gr,_it) :
        return (
          ((fx((_it+t.step))+fx((_it-t.step))-2*fx(_it))/t.step**2)==ff(fx(_it),fv(_it))
        )
    Gr.conEQ0 = py.Constraint(t.mFlNodSm,rule=EQ0 )
 								# v==d/dt(x)
    def EQ1 (Gr,_it) :
        return (
          fv(_it)==((fx((_it+t.step))-fx(_it))/t.step)
        )
    Gr.conEQ1 = py.Constraint(t.FlNodSm,rule=EQ1 )
    Px = Penal[0]
    Pfx = Penal[1]
    Pfv = Penal[2]

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('x'))
    if x.mu is None : x.mu = Gr.mu0
    x.ValidationSets = SvF.ValidationSets
    x.notTrainingSets = SvF.notTrainingSets
    x.TrainingSets = SvF.TrainingSets
 											# x.Complexity([Px])+f.Complexity([Pfx,Pfv])/x.V.sigma2+x.MSD()
    def obj_expression(Gr):  
        return (
             x.Complexity([Px])+f.Complexity([Pfx,Pfv])/x.V.sigma2+x.MSD()
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Px = Penal[0]
    Pfx = Penal[1]
    Pfv = Penal[2]
    Gr = Task.Gr

    x = Task.Funs[0]

    f = Task.Funs[2]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (x.Complexity([Px]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.Complexity([Px]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.Complexity([Px]) ='+ stmp+'\n')
    tmp = (f.Complexity([Pfx,Pfv])/x.V.sigma2)
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tf.Complexity([Pfx,Pfv])/x.V.sigma2 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tf.Complexity([Pfx,Pfv])/x.V.sigma2 ='+ stmp+'\n')
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
Pl = Polyline (x, v, None, 'Trajectory')
Pl.Y[0]=Pl.Y[1]
Pl.Y[-1]=Pl.Y[-2]
Task.Draw ( 'f Trajectory;LC:red' )