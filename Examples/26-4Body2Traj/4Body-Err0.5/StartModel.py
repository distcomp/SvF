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
DB = Table ( '../4bdn-1_0.9_0.2_0.06-abc.xlsx','DB','t,x1,y1,z1,x2,y2,z2,x1a,y1a,z1a,x2a,y2a,z2a,x3a as x3,y3a as y3,z3a as z3,x4a as x4,y4a as y4,z4a as z4' )
DB.dat('x1')[:]=(DB.dat('x1')[:]+DB.dat('x1a')[:])*.5
DB.dat('y1')[:]=(DB.dat('y1')[:]+DB.dat('y1a')[:])*.5
DB.dat('z1')[:]=(DB.dat('z1')[:]+DB.dat('z1a')[:])*.5
DB.dat('x2')[:]=(DB.dat('x2')[:]+DB.dat('x2a')[:])*.5
DB.dat('y2')[:]=(DB.dat('y2')[:]+DB.dat('y2a')[:])*.5
DB.dat('z2')[:]=(DB.dat('z2')[:]+DB.dat('z2a')[:])*.5
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
x3 = Fun('x3',[t])
def fx3(t) : return x3.F([t])
y3 = Fun('y3',[t])
def fy3(t) : return y3.F([t])
z3 = Fun('z3',[t])
def fz3(t) : return z3.F([t])
x4 = Fun('x4',[t])
def fx4(t) : return x4.F([t])
y4 = Fun('y4',[t])
def fy4(t) : return y4.F([t])
z4 = Fun('z4',[t])
def fz4(t) : return z4.F([t])
G=1
m1 = Tensor('m1',[])
def fm1() : return m1.F([])
m2 = Tensor('m2',[])
def fm2() : return m2.F([])
m3 = Tensor('m3',[])
def fm3() : return m3.F([])
m4 = Tensor('m4',[])
def fm4() : return m4.F([])
CVmakeSets (  CV_NumSets=7 )
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

    x3.var = py.Var ( x3.A[0].NodS,domain=Reals )
    x3.gr =  x3.var
    Gr.x3 =  x3.var

    y3.var = py.Var ( y3.A[0].NodS,domain=Reals )
    y3.gr =  y3.var
    Gr.y3 =  y3.var

    z3.var = py.Var ( z3.A[0].NodS,domain=Reals )
    z3.gr =  z3.var
    Gr.z3 =  z3.var

    x4.var = py.Var ( x4.A[0].NodS,domain=Reals )
    x4.gr =  x4.var
    Gr.x4 =  x4.var

    y4.var = py.Var ( y4.A[0].NodS,domain=Reals )
    y4.gr =  y4.var
    Gr.y4 =  y4.var

    z4.var = py.Var ( z4.A[0].NodS,domain=Reals )
    z4.gr =  z4.var
    Gr.z4 =  z4.var

    m1.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    m1.gr =  m1.var
    Gr.m1 =  m1.var

    m2.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    m2.gr =  m2.var
    Gr.m2 =  m2.var

    m3.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    m3.gr =  m3.var
    Gr.m3 =  m3.var

    m4.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    m4.gr =  m4.var
    Gr.m4 =  m4.var
 								# x1''=G*m2*(x2-x1)/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)**(3/2)+G*m3*(x3-x1)/((x3-x1)**2+(y3-y1)**2+(z3-z1)**2)**(3/2)+G*m4*(x4-x1)/((x4-x1)**2+(y4-y1)**2+(z4-z1)**2)**(3/2)
    def EQ0 (Gr,_it) :
        return (
          x1.by_xx(_it)==G*fm2()*(fx2(_it)-fx1(_it))/((fx2(_it)-fx1(_it))**2+(fy2(_it)-fy1(_it))**2+(fz2(_it)-fz1(_it))**2)**(3/2)+G*fm3()*(fx3(_it)-fx1(_it))/((fx3(_it)-fx1(_it))**2+(fy3(_it)-fy1(_it))**2+(fz3(_it)-fz1(_it))**2)**(3/2)+G*fm4()*(fx4(_it)-fx1(_it))/((fx4(_it)-fx1(_it))**2+(fy4(_it)-fy1(_it))**2+(fz4(_it)-fz1(_it))**2)**(3/2)
        )
    Gr.conEQ0 = py.Constraint(t.mFlNodSm,rule=EQ0 )
 								# y1''=G*m2*(y2-y1)/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)**(3/2)+G*m3*(y3-y1)/((x3-x1)**2+(y3-y1)**2+(z3-z1)**2)**(3/2)+G*m4*(y4-y1)/((x4-x1)**2+(y4-y1)**2+(z4-z1)**2)**(3/2)
    def EQ1 (Gr,_it) :
        return (
          y1.by_xx(_it)==G*fm2()*(fy2(_it)-fy1(_it))/((fx2(_it)-fx1(_it))**2+(fy2(_it)-fy1(_it))**2+(fz2(_it)-fz1(_it))**2)**(3/2)+G*fm3()*(fy3(_it)-fy1(_it))/((fx3(_it)-fx1(_it))**2+(fy3(_it)-fy1(_it))**2+(fz3(_it)-fz1(_it))**2)**(3/2)+G*fm4()*(fy4(_it)-fy1(_it))/((fx4(_it)-fx1(_it))**2+(fy4(_it)-fy1(_it))**2+(fz4(_it)-fz1(_it))**2)**(3/2)
        )
    Gr.conEQ1 = py.Constraint(t.mFlNodSm,rule=EQ1 )
 								# z1''=G*m2*(z2-z1)/((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)**(3/2)+G*m3*(z3-z1)/((x3-x1)**2+(y3-y1)**2+(z3-z1)**2)**(3/2)+G*m4*(z4-z1)/((x4-x1)**2+(y4-y1)**2+(z4-z1)**2)**(3/2)
    def EQ2 (Gr,_it) :
        return (
          z1.by_xx(_it)==G*fm2()*(fz2(_it)-fz1(_it))/((fx2(_it)-fx1(_it))**2+(fy2(_it)-fy1(_it))**2+(fz2(_it)-fz1(_it))**2)**(3/2)+G*fm3()*(fz3(_it)-fz1(_it))/((fx3(_it)-fx1(_it))**2+(fy3(_it)-fy1(_it))**2+(fz3(_it)-fz1(_it))**2)**(3/2)+G*fm4()*(fz4(_it)-fz1(_it))/((fx4(_it)-fx1(_it))**2+(fy4(_it)-fy1(_it))**2+(fz4(_it)-fz1(_it))**2)**(3/2)
        )
    Gr.conEQ2 = py.Constraint(t.mFlNodSm,rule=EQ2 )
 								# x2''=G*m1*(x1-x2)/((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**(3/2)+G*m3*(x3-x2)/((x3-x2)**2+(y3-y2)**2+(z3-z2)**2)**(3/2)+G*m4*(x4-x2)/((x4-x2)**2+(y4-y2)**2+(z4-z2)**2)**(3/2)
    def EQ3 (Gr,_it) :
        return (
          x2.by_xx(_it)==G*fm1()*(fx1(_it)-fx2(_it))/((fx1(_it)-fx2(_it))**2+(fy1(_it)-fy2(_it))**2+(fz1(_it)-fz2(_it))**2)**(3/2)+G*fm3()*(fx3(_it)-fx2(_it))/((fx3(_it)-fx2(_it))**2+(fy3(_it)-fy2(_it))**2+(fz3(_it)-fz2(_it))**2)**(3/2)+G*fm4()*(fx4(_it)-fx2(_it))/((fx4(_it)-fx2(_it))**2+(fy4(_it)-fy2(_it))**2+(fz4(_it)-fz2(_it))**2)**(3/2)
        )
    Gr.conEQ3 = py.Constraint(t.mFlNodSm,rule=EQ3 )
 								# y2''=G*m1*(y1-y2)/((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**(3/2)+G*m3*(y3-y2)/((x3-x2)**2+(y3-y2)**2+(z3-z2)**2)**(3/2)+G*m4*(y4-y2)/((x4-x2)**2+(y4-y2)**2+(z4-z2)**2)**(3/2)
    def EQ4 (Gr,_it) :
        return (
          y2.by_xx(_it)==G*fm1()*(fy1(_it)-fy2(_it))/((fx1(_it)-fx2(_it))**2+(fy1(_it)-fy2(_it))**2+(fz1(_it)-fz2(_it))**2)**(3/2)+G*fm3()*(fy3(_it)-fy2(_it))/((fx3(_it)-fx2(_it))**2+(fy3(_it)-fy2(_it))**2+(fz3(_it)-fz2(_it))**2)**(3/2)+G*fm4()*(fy4(_it)-fy2(_it))/((fx4(_it)-fx2(_it))**2+(fy4(_it)-fy2(_it))**2+(fz4(_it)-fz2(_it))**2)**(3/2)
        )
    Gr.conEQ4 = py.Constraint(t.mFlNodSm,rule=EQ4 )
 								# z2''=G*m1*(z1-z2)/((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**(3/2)+G*m3*(z3-z2)/((x3-x2)**2+(y3-y2)**2+(z3-z2)**2)**(3/2)+G*m4*(z4-z2)/((x4-x2)**2+(y4-y2)**2+(z4-z2)**2)**(3/2)
    def EQ5 (Gr,_it) :
        return (
          z2.by_xx(_it)==G*fm1()*(fz1(_it)-fz2(_it))/((fx1(_it)-fx2(_it))**2+(fy1(_it)-fy2(_it))**2+(fz1(_it)-fz2(_it))**2)**(3/2)+G*fm3()*(fz3(_it)-fz2(_it))/((fx3(_it)-fx2(_it))**2+(fy3(_it)-fy2(_it))**2+(fz3(_it)-fz2(_it))**2)**(3/2)+G*fm4()*(fz4(_it)-fz2(_it))/((fx4(_it)-fx2(_it))**2+(fy4(_it)-fy2(_it))**2+(fz4(_it)-fz2(_it))**2)**(3/2)
        )
    Gr.conEQ5 = py.Constraint(t.mFlNodSm,rule=EQ5 )
 								# x3''=G*m1*(x1-x3)/((x1-x3)**2+(y1-y3)**2+(z1-z3)**2)**(3/2)+G*m2*(x2-x3)/((x2-x3)**2+(y2-y3)**2+(z2-z3)**2)**(3/2)+G*m4*(x4-x3)/((x4-x3)**2+(y4-y3)**2+(z4-z3)**2)**(3/2)
    def EQ6 (Gr,_it) :
        return (
          x3.by_xx(_it)==G*fm1()*(fx1(_it)-fx3(_it))/((fx1(_it)-fx3(_it))**2+(fy1(_it)-fy3(_it))**2+(fz1(_it)-fz3(_it))**2)**(3/2)+G*fm2()*(fx2(_it)-fx3(_it))/((fx2(_it)-fx3(_it))**2+(fy2(_it)-fy3(_it))**2+(fz2(_it)-fz3(_it))**2)**(3/2)+G*fm4()*(fx4(_it)-fx3(_it))/((fx4(_it)-fx3(_it))**2+(fy4(_it)-fy3(_it))**2+(fz4(_it)-fz3(_it))**2)**(3/2)
        )
    Gr.conEQ6 = py.Constraint(t.mFlNodSm,rule=EQ6 )
 								# y3''=G*m1*(y1-y3)/((x1-x3)**2+(y1-y3)**2+(z1-z3)**2)**(3/2)+G*m2*(y2-y3)/((x2-x3)**2+(y2-y3)**2+(z2-z3)**2)**(3/2)+G*m4*(y4-y3)/((x4-x3)**2+(y4-y3)**2+(z4-z3)**2)**(3/2)
    def EQ7 (Gr,_it) :
        return (
          y3.by_xx(_it)==G*fm1()*(fy1(_it)-fy3(_it))/((fx1(_it)-fx3(_it))**2+(fy1(_it)-fy3(_it))**2+(fz1(_it)-fz3(_it))**2)**(3/2)+G*fm2()*(fy2(_it)-fy3(_it))/((fx2(_it)-fx3(_it))**2+(fy2(_it)-fy3(_it))**2+(fz2(_it)-fz3(_it))**2)**(3/2)+G*fm4()*(fy4(_it)-fy3(_it))/((fx4(_it)-fx3(_it))**2+(fy4(_it)-fy3(_it))**2+(fz4(_it)-fz3(_it))**2)**(3/2)
        )
    Gr.conEQ7 = py.Constraint(t.mFlNodSm,rule=EQ7 )
 								# z3''=G*m1*(z1-z3)/((x1-x3)**2+(y1-y3)**2+(z1-z3)**2)**(3/2)+G*m2*(z2-z3)/((x2-x3)**2+(y2-y3)**2+(z2-z3)**2)**(3/2)+G*m4*(z4-z3)/((x4-x3)**2+(y4-y3)**2+(z4-z3)**2)**(3/2)
    def EQ8 (Gr,_it) :
        return (
          z3.by_xx(_it)==G*fm1()*(fz1(_it)-fz3(_it))/((fx1(_it)-fx3(_it))**2+(fy1(_it)-fy3(_it))**2+(fz1(_it)-fz3(_it))**2)**(3/2)+G*fm2()*(fz2(_it)-fz3(_it))/((fx2(_it)-fx3(_it))**2+(fy2(_it)-fy3(_it))**2+(fz2(_it)-fz3(_it))**2)**(3/2)+G*fm4()*(fz4(_it)-fz3(_it))/((fx4(_it)-fx3(_it))**2+(fy4(_it)-fy3(_it))**2+(fz4(_it)-fz3(_it))**2)**(3/2)
        )
    Gr.conEQ8 = py.Constraint(t.mFlNodSm,rule=EQ8 )
 								# x4''=G*m1*(x1-x4)/((x1-x4)**2+(y1-y4)**2+(z1-z4)**2)**(3/2)+G*m2*(x2-x4)/((x2-x4)**2+(y2-y4)**2+(z2-z4)**2)**(3/2)+G*m3*(x3-x4)/((x3-x4)**2+(y3-y4)**2+(z3-z4)**2)**(3/2)
    def EQ9 (Gr,_it) :
        return (
          x4.by_xx(_it)==G*fm1()*(fx1(_it)-fx4(_it))/((fx1(_it)-fx4(_it))**2+(fy1(_it)-fy4(_it))**2+(fz1(_it)-fz4(_it))**2)**(3/2)+G*fm2()*(fx2(_it)-fx4(_it))/((fx2(_it)-fx4(_it))**2+(fy2(_it)-fy4(_it))**2+(fz2(_it)-fz4(_it))**2)**(3/2)+G*fm3()*(fx3(_it)-fx4(_it))/((fx3(_it)-fx4(_it))**2+(fy3(_it)-fy4(_it))**2+(fz3(_it)-fz4(_it))**2)**(3/2)
        )
    Gr.conEQ9 = py.Constraint(t.mFlNodSm,rule=EQ9 )
 								# y4''=G*m1*(y1-y4)/((x1-x4)**2+(y1-y4)**2+(z1-z4)**2)**(3/2)+G*m2*(y2-y4)/((x2-x4)**2+(y2-y4)**2+(z2-z4)**2)**(3/2)+G*m3*(y3-y4)/((x3-x4)**2+(y3-y4)**2+(z3-z4)**2)**(3/2)
    def EQ10 (Gr,_it) :
        return (
          y4.by_xx(_it)==G*fm1()*(fy1(_it)-fy4(_it))/((fx1(_it)-fx4(_it))**2+(fy1(_it)-fy4(_it))**2+(fz1(_it)-fz4(_it))**2)**(3/2)+G*fm2()*(fy2(_it)-fy4(_it))/((fx2(_it)-fx4(_it))**2+(fy2(_it)-fy4(_it))**2+(fz2(_it)-fz4(_it))**2)**(3/2)+G*fm3()*(fy3(_it)-fy4(_it))/((fx3(_it)-fx4(_it))**2+(fy3(_it)-fy4(_it))**2+(fz3(_it)-fz4(_it))**2)**(3/2)
        )
    Gr.conEQ10 = py.Constraint(t.mFlNodSm,rule=EQ10 )
 								# z4''=G*m1*(z1-z4)/((x1-x4)**2+(y1-y4)**2+(z1-z4)**2)**(3/2)+G*m2*(z2-z4)/((x2-x4)**2+(y2-y4)**2+(z2-z4)**2)**(3/2)+G*m3*(z3-z4)/((x3-x4)**2+(y3-y4)**2+(z3-z4)**2)**(3/2)
    def EQ11 (Gr,_it) :
        return (
          z4.by_xx(_it)==G*fm1()*(fz1(_it)-fz4(_it))/((fx1(_it)-fx4(_it))**2+(fy1(_it)-fy4(_it))**2+(fz1(_it)-fz4(_it))**2)**(3/2)+G*fm2()*(fz2(_it)-fz4(_it))/((fx2(_it)-fx4(_it))**2+(fy2(_it)-fy4(_it))**2+(fz2(_it)-fz4(_it))**2)**(3/2)+G*fm3()*(fz3(_it)-fz4(_it))/((fx3(_it)-fx4(_it))**2+(fy3(_it)-fy4(_it))**2+(fz3(_it)-fz4(_it))**2)**(3/2)
        )
    Gr.conEQ11 = py.Constraint(t.mFlNodSm,rule=EQ11 )

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
P3 = Polyline([x3.grd[0]],[y3.grd[0]], None, "P3")
P4 = Polyline([x4.grd[0]],[y4.grd[0]], None, "P4")
Plot( [ [ DB.dat('x1'), DB.dat('y1'), 'lw=0', 'c=red', "marker='o'", 'ms=2', "label='Data1'", "xlab='x'", 'xlab_x=1.01', "ylab='y'"], [DB.dat('x2'), DB.dat('y2'), 'lw=0', 'c=green', "marker='o'", 'ms=2', "label='Data2'"], [DB.dat('x3'), DB.dat('y3'), 'lw=0', 'c=blue', "marker='o'", 'ms=1', "label='Data3'"], [DB.dat('x4'), DB.dat('y4'), 'lw=0', 'c=gray', "marker='o'", 'ms=1', "label='Data4'"], [x1.grd, y1.grd, 'c=red', 'lw=2', "label='Planet1'", 'ms=0'], [P1, 'ms=5', "label=''"], [x2.grd, y2.grd, 'c=green', 'lw=2', "label='Planet2'", 'ms=0'], [P2, 'ms=5', "label=''"], [x3.grd, y3.grd, 'c=blue', 'lw=2', "label='Planet3'", 'ms=0'], [P3, 'ms=5', "label=''"], [x4.grd, y4.grd, 'c=gray', 'lw=2', "label='Planet4'", 'ms=0'], [P4, 'ms=5', "label=''"] ] )
Plot( [ [ x1, 'c=r'], [y1, 'c=g'], [z1, 'c=b', "ylab='x1,y1,z1'", 'ylab_x=.02'] ] )
Plot( [ [ x2, 'c=r'], [y2, 'c=g'], [z2, 'c=b', "ylab='x2,y2,z2'", 'ylab_x=.02'] ] )
Plot( [ [ x3, 'c=r', 'dms=0.5'], [y3, 'c=g'], [z3, 'c=b', "ylab='x3,y3,z3'", 'ylab_x=.02'] ] )
Plot( [ [ x4, 'c=r', 'dms=0.5'], [y4, 'c=g'], [z4, 'c=b', "ylab='x4,y4,z4'", 'ylab_x=.02'] ] )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")