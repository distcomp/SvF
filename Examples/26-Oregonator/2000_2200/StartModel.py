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
SvF.mngF = 'MAN.mng'
SvF.TaskName="Oregonator"; 
def where_condition ( t, X, Y, Z ):
    return (t<2200)
DB = Table ( '../oregonator_results_noisy.xlsx','DB','t,X,Y,Z',where_condition )
t = Set('t',SvF.currentTab.dat('t')[:].min(),SvF.currentTab.dat('t')[:].max(),0.175,'','t')
X = Fun('X',[t])
def fX(t) : return X.F([t])
Y = Fun('Y',[t])
def fY(t) : return Y.F([t])
Z = Fun('Z',[t])
def fZ(t) : return Z.F([t])
k1 = Tensor('k1',[])
def fk1() : return k1.F([])
k2 = Tensor('k2',[])
def fk2() : return k2.F([])
k3 = Tensor('k3',[])
def fk3() : return k3.F([])
k4 = Tensor('k4',[])
def fk4() : return k4.F([])
k5 = Tensor('k5',[])
def fk5() : return k5.F([])
A=0.016406707120152755
alpha=2
SvF.CVNumOfIter=1; 
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    X.var = py.Var ( X.A[0].NodS,domain=Reals )
    X.gr =  X.var
    Gr.X =  X.var

    Y.var = py.Var ( Y.A[0].NodS,domain=Reals )
    Y.gr =  Y.var
    Gr.Y =  Y.var

    Z.var = py.Var ( Z.A[0].NodS,domain=Reals )
    Z.gr =  Z.var
    Gr.Z =  Z.var

    k1.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    k1.gr =  k1.var
    Gr.k1 =  k1.var

    k2.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    k2.gr =  k2.var
    Gr.k2 =  k2.var

    k3.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    k3.gr =  k3.var
    Gr.k3 =  k3.var

    k4.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    k4.gr =  k4.var
    Gr.k4 =  k4.var

    k5.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    k5.gr =  k5.var
    Gr.k5 =  k5.var
 								# d/dt(X)=k1*A*Y-k2*X*Y+k3*A*X-2.0*k4*X**2
    def EQ0 (Gr,_it) :
        return (
          X.by_x(_it)==fk1()*A*fY(_it)-fk2()*fX(_it)*fY(_it)+fk3()*A*fX(_it)-2.0*fk4()*fX(_it)**2
        )
    Gr.conEQ0 = py.Constraint(t.FlNodSm,rule=EQ0 )
 								# d/dt(Y)=-k1*A*Y-k2*X*Y+(k5/alpha)*Z
    def EQ1 (Gr,_it) :
        return (
          Y.by_x(_it)==-fk1()*A*fY(_it)-fk2()*fX(_it)*fY(_it)+(fk5()/alpha)*fZ(_it)
        )
    Gr.conEQ1 = py.Constraint(t.FlNodSm,rule=EQ1 )
 								# d/dt(Z)=2.0*k3*A*X-k5*Z
    def EQ2 (Gr,_it) :
        return (
          Z.by_x(_it)==2.0*fk3()*A*fX(_it)-fk5()*fZ(_it)
        )
    Gr.conEQ2 = py.Constraint(t.FlNodSm,rule=EQ2 )

    make_CV_Sets(0, SvF.CVstep)

    if len (SvF.CV_NoRs) > 0 :

       Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('X'))
    if X.mu is None : X.mu = Gr.mu0
    X.ValidationSets = SvF.ValidationSets
    X.notTrainingSets = SvF.notTrainingSets
    X.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('Y'))
    if Y.mu is None : Y.mu = Gr.mu0
    Y.ValidationSets = SvF.ValidationSets
    Y.notTrainingSets = SvF.notTrainingSets
    Y.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('Z'))
    if Z.mu is None : Z.mu = Gr.mu0
    Z.ValidationSets = SvF.ValidationSets
    Z.notTrainingSets = SvF.notTrainingSets
    Z.TrainingSets = SvF.TrainingSets
 											# X.MSD()+Y.MSD()+Z.MSD()
    def obj_expression(Gr):  
        return (
             X.MSD()+Y.MSD()+Z.MSD()
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    X = Task.Funs[0]

    Y = Task.Funs[1]

    Z = Task.Funs[2]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (X.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tX.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tX.MSD() ='+ stmp+'\n')
    tmp = (Y.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tY.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tY.MSD() ='+ stmp+'\n')
    tmp = (Z.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tZ.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tZ.MSD() ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
Plot( [ [ X], [Y], [Z] ] )
Plot( [ [ X] ] )
Plot( [ [ Y] ] )
Plot( [ [ Z] ] )
Plot( [ [ DB.dat('X'), DB.dat('Z'), 'lw=0', 'c=green', "marker='.'", 'ms=3', "label='XZ data'"], [X.grd, Z.grd, 'c=red', 'lw=2', "label='X(t),Z(t)'", "xlab='X'", 'xlab_x=1.06', "ylab='Z'"] ] )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")