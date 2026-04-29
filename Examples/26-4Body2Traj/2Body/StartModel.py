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
SvF.TaskName="2Body3D"; 
DB = Table ( '../4bdn-1_0.9_0.2_0.06-abc.xlsx','DB','t,x1,y1,z1,x2,y2,z2' )
t = Set('t',SvF.currentTab.dat('t')[:].min(),SvF.currentTab.dat('t')[:].max(),0.01,'','t')
x1 = Fun('x1',[t])
def fx1(t) : return x1.F([t])
y1 = Fun('y1',[t])
def fy1(t) : return y1.F([t])
z1 = Fun('z1',[t])
def fz1(t) : return z1.F([t])
x2 = Fun('x2',[t])
def fx2(t) : return x2.F([t])
y2 = Fun('y2',[t])
def fy2(t) : return y2.F([t])
z2 = Fun('z2',[t])
def fz2(t) : return z2.F([t])
G_const=1
m1 = Tensor('m1',[])
def fm1() : return m1.F([])
m2 = Tensor('m2',[])
def fm2() : return m2.F([])
CVmakeSets (  CV_NumSets=5 )
SvF.CVNumOfIter=1; 
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    x1.var = py.Var ( x1.A[0].NodS,domain=Reals )
    x1.gr =  x1.var
    Gr.x1 =  x1.var

    y1.var = py.Var ( y1.A[0].NodS,domain=Reals )
    y1.gr =  y1.var
    Gr.y1 =  y1.var

    z1.var = py.Var ( z1.A[0].NodS,domain=Reals )
    z1.gr =  z1.var
    Gr.z1 =  z1.var

    x2.var = py.Var ( x2.A[0].NodS,domain=Reals )
    x2.gr =  x2.var
    Gr.x2 =  x2.var

    y2.var = py.Var ( y2.A[0].NodS,domain=Reals )
    y2.gr =  y2.var
    Gr.y2 =  y2.var

    z2.var = py.Var ( z2.A[0].NodS,domain=Reals )
    z2.gr =  z2.var
    Gr.z2 =  z2.var

    m1.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    m1.gr =  m1.var
    Gr.m1 =  m1.var

    m2.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    m2.gr =  m2.var
    Gr.m2 =  m2.var
 								# x1''=G_const*m2*(x2-x1)/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)**(3/2)
    def EQ0 (Gr,_it) :
        return (
          x1.by_xx(_it)==G_const*fm2()*(fx2(_it)-fx1(_it))/((fx2(_it)-fx1(_it))**2+(fy2(_it)-fy1(_it))**2+(fz2(_it)-fz1(_it))**2)**(3/2)
        )
    Gr.conEQ0 = py.Constraint(t.mFlNodSm,rule=EQ0 )
 								# y1''=G_const*m2*(y2-y1)/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)**(3/2)
    def EQ1 (Gr,_it) :
        return (
          y1.by_xx(_it)==G_const*fm2()*(fy2(_it)-fy1(_it))/((fx2(_it)-fx1(_it))**2+(fy2(_it)-fy1(_it))**2+(fz2(_it)-fz1(_it))**2)**(3/2)
        )
    Gr.conEQ1 = py.Constraint(t.mFlNodSm,rule=EQ1 )
 								# z1''=G_const*m2*(z2-z1)/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)**(3/2)
    def EQ2 (Gr,_it) :
        return (
          z1.by_xx(_it)==G_const*fm2()*(fz2(_it)-fz1(_it))/((fx2(_it)-fx1(_it))**2+(fy2(_it)-fy1(_it))**2+(fz2(_it)-fz1(_it))**2)**(3/2)
        )
    Gr.conEQ2 = py.Constraint(t.mFlNodSm,rule=EQ2 )
 								# x2''=G_const*m1*(x1-x2)/((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**(3/2)
    def EQ3 (Gr,_it) :
        return (
          x2.by_xx(_it)==G_const*fm1()*(fx1(_it)-fx2(_it))/((fx1(_it)-fx2(_it))**2+(fy1(_it)-fy2(_it))**2+(fz1(_it)-fz2(_it))**2)**(3/2)
        )
    Gr.conEQ3 = py.Constraint(t.mFlNodSm,rule=EQ3 )
 								# y2''=G_const*m1*(y1-y2)/((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**(3/2)
    def EQ4 (Gr,_it) :
        return (
          y2.by_xx(_it)==G_const*fm1()*(fy1(_it)-fy2(_it))/((fx1(_it)-fx2(_it))**2+(fy1(_it)-fy2(_it))**2+(fz1(_it)-fz2(_it))**2)**(3/2)
        )
    Gr.conEQ4 = py.Constraint(t.mFlNodSm,rule=EQ4 )
 								# z2''=G_const*m1*(z1-z2)/((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**(3/2)
    def EQ5 (Gr,_it) :
        return (
          z2.by_xx(_it)==G_const*fm1()*(fz1(_it)-fz2(_it))/((fx1(_it)-fx2(_it))**2+(fy1(_it)-fy2(_it))**2+(fz1(_it)-fz2(_it))**2)**(3/2)
        )
    Gr.conEQ5 = py.Constraint(t.mFlNodSm,rule=EQ5 )

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('x1'))
    if x1.mu is None : x1.mu = Gr.mu0
    x1.ValidationSets = SvF.ValidationSets
    x1.notTrainingSets = SvF.notTrainingSets
    x1.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('y1'))
    if y1.mu is None : y1.mu = Gr.mu0
    y1.ValidationSets = SvF.ValidationSets
    y1.notTrainingSets = SvF.notTrainingSets
    y1.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('z1'))
    if z1.mu is None : z1.mu = Gr.mu0
    z1.ValidationSets = SvF.ValidationSets
    z1.notTrainingSets = SvF.notTrainingSets
    z1.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('x2'))
    if x2.mu is None : x2.mu = Gr.mu0
    x2.ValidationSets = SvF.ValidationSets
    x2.notTrainingSets = SvF.notTrainingSets
    x2.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('y2'))
    if y2.mu is None : y2.mu = Gr.mu0
    y2.ValidationSets = SvF.ValidationSets
    y2.notTrainingSets = SvF.notTrainingSets
    y2.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('z2'))
    if z2.mu is None : z2.mu = Gr.mu0
    z2.ValidationSets = SvF.ValidationSets
    z2.notTrainingSets = SvF.notTrainingSets
    z2.TrainingSets = SvF.TrainingSets
 											# x1.MSD()+y1.MSD()+z1.MSD()+x2.MSD()+y2.MSD()+z2.MSD()
    def obj_expression(Gr):  
        return (
             x1.MSD()+y1.MSD()+z1.MSD()+x2.MSD()+y2.MSD()+z2.MSD()
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x1 = Task.Funs[0]

    y1 = Task.Funs[1]

    z1 = Task.Funs[2]

    x2 = Task.Funs[3]

    y2 = Task.Funs[4]

    z2 = Task.Funs[5]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (x1.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx1.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx1.MSD() ='+ stmp+'\n')
    tmp = (y1.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty1.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty1.MSD() ='+ stmp+'\n')
    tmp = (z1.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tz1.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tz1.MSD() ='+ stmp+'\n')
    tmp = (x2.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx2.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx2.MSD() ='+ stmp+'\n')
    tmp = (y2.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty2.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty2.MSD() ='+ stmp+'\n')
    tmp = (z2.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tz2.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tz2.MSD() ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
P1 = Polyline([x1.grd[0]],[y1.grd[0]], None, "P1")
P2 = Polyline([x2.grd[0]],[y2.grd[0]], None, "P2")
Plot( [ [ DB.dat('x1'), DB.dat('y1'), 'lw=0', 'c=red', "marker='o'", 'ms=2', "label='Data1'", "xlab='x'", 'xlab_x=1.01', "ylab='y'"], [P1, 'ms=5', "label=''"], [DB.dat('x2'), DB.dat('y2'), 'lw=0', 'c=green', "marker='o'", 'ms=2', "label='Data2'"], [P2, 'ms=5', "label=''"], [x1.grd, y1.grd, 'c=red', 'lw=2', "label='Planet1'", 'ms=0'], [x2.grd, y2.grd, 'c=green', 'lw=2', "label='Planet2'"] ] )
Plot( [ [ x1, 'c=r'], [y1, 'c=g'], [z1, 'c=b', "ylab='x1,y1,z1'", 'ylab_x=.02'] ] )
Plot( [ [ x2, 'c=r'], [y2, 'c=g'], [z2, 'c=b', "ylab='x2,y2,z2'", 'ylab_x=.02'] ] )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")