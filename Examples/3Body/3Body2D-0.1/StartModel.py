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
SvF.mngF = '3Body2D.mng'
DB = Table ( '3Body2D.dat','DB','t,x1,y1,x2,y2,x3,y3' )
t = Set('t',SvF.currentTab.dat('t')[:].min(),SvF.currentTab.dat('t')[:].max(),0.1,'','t')
x1 = Fun('x1',[t])
def fx1(t) : return x1.F([t])
y1 = Fun('y1',[t])
def fy1(t) : return y1.F([t])
x2 = Fun('x2',[t])
def fx2(t) : return x2.F([t])
y2 = Fun('y2',[t])
def fy2(t) : return y2.F([t])
x3 = Fun('x3',[t])
def fx3(t) : return x3.F([t])
y3 = Fun('y3',[t])
def fy3(t) : return y3.F([t])
G_const=1
m1 = Tensor('m1',[])
def fm1() : return m1.F([])
m2 = Tensor('m2',[])
def fm2() : return m2.F([])
m3 = Tensor('m3',[])
def fm3() : return m3.F([])
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

    x2.var = py.Var ( x2.A[0].NodS,domain=Reals )
    x2.gr =  x2.var
    Gr.x2 =  x2.var

    y2.var = py.Var ( y2.A[0].NodS,domain=Reals )
    y2.gr =  y2.var
    Gr.y2 =  y2.var

    x3.var = py.Var ( x3.A[0].NodS,domain=Reals )
    x3.gr =  x3.var
    Gr.x3 =  x3.var

    y3.var = py.Var ( y3.A[0].NodS,domain=Reals )
    y3.gr =  y3.var
    Gr.y3 =  y3.var

    m1.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    m1.gr =  m1.var
    Gr.m1 =  m1.var

    m2.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    m2.gr =  m2.var
    Gr.m2 =  m2.var

    m3.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    m3.gr =  m3.var
    Gr.m3 =  m3.var
 								# x1''=G_const*m2*(x2-x1)/((x2-x1)**2+(y2-y1)**2)**(3/2)+G_const*m3*(x3-x1)/((x3-x1)**2+(y3-y1)**2)**(3/2)
    def EQ0 (Gr,_it) :
        return (
          x1.by_xx(_it)==G_const*fm2()*(fx2(_it)-fx1(_it))/((fx2(_it)-fx1(_it))**2+(fy2(_it)-fy1(_it))**2)**(3/2)+G_const*fm3()*(fx3(_it)-fx1(_it))/((fx3(_it)-fx1(_it))**2+(fy3(_it)-fy1(_it))**2)**(3/2)
        )
    Gr.conEQ0 = py.Constraint(t.mFlNodSm,rule=EQ0 )
 								# y1''=G_const*m2*(y2-y1)/((x2-x1)**2+(y2-y1)**2)**(3/2)+G_const*m3*(y3-y1)/((x3-x1)**2+(y3-y1)**2)**(3/2)
    def EQ1 (Gr,_it) :
        return (
          y1.by_xx(_it)==G_const*fm2()*(fy2(_it)-fy1(_it))/((fx2(_it)-fx1(_it))**2+(fy2(_it)-fy1(_it))**2)**(3/2)+G_const*fm3()*(fy3(_it)-fy1(_it))/((fx3(_it)-fx1(_it))**2+(fy3(_it)-fy1(_it))**2)**(3/2)
        )
    Gr.conEQ1 = py.Constraint(t.mFlNodSm,rule=EQ1 )
 								# x2''=G_const*m1*(x1-x2)/((x1-x2)**2+(y1-y2)**2)**(3/2)+G_const*m3*(x3-x2)/((x3-x2)**2+(y3-y2)**2)**(3/2)
    def EQ2 (Gr,_it) :
        return (
          x2.by_xx(_it)==G_const*fm1()*(fx1(_it)-fx2(_it))/((fx1(_it)-fx2(_it))**2+(fy1(_it)-fy2(_it))**2)**(3/2)+G_const*fm3()*(fx3(_it)-fx2(_it))/((fx3(_it)-fx2(_it))**2+(fy3(_it)-fy2(_it))**2)**(3/2)
        )
    Gr.conEQ2 = py.Constraint(t.mFlNodSm,rule=EQ2 )
 								# y2''=G_const*m1*(y1-y2)/((x1-x2)**2+(y1-y2)**2)**(3/2)+G_const*m3*(y3-y2)/((x3-x2)**2+(y3-y2)**2)**(3/2)
    def EQ3 (Gr,_it) :
        return (
          y2.by_xx(_it)==G_const*fm1()*(fy1(_it)-fy2(_it))/((fx1(_it)-fx2(_it))**2+(fy1(_it)-fy2(_it))**2)**(3/2)+G_const*fm3()*(fy3(_it)-fy2(_it))/((fx3(_it)-fx2(_it))**2+(fy3(_it)-fy2(_it))**2)**(3/2)
        )
    Gr.conEQ3 = py.Constraint(t.mFlNodSm,rule=EQ3 )
 								# x3''=G_const*m1*(x1-x3)/((x1-x3)**2+(y1-y3)**2)**(3/2)+G_const*m2*(x2-x3)/((x2-x3)**2+(y2-y3)**2)**(3/2)
    def EQ4 (Gr,_it) :
        return (
          x3.by_xx(_it)==G_const*fm1()*(fx1(_it)-fx3(_it))/((fx1(_it)-fx3(_it))**2+(fy1(_it)-fy3(_it))**2)**(3/2)+G_const*fm2()*(fx2(_it)-fx3(_it))/((fx2(_it)-fx3(_it))**2+(fy2(_it)-fy3(_it))**2)**(3/2)
        )
    Gr.conEQ4 = py.Constraint(t.mFlNodSm,rule=EQ4 )
 								# y3''=G_const*m1*(y1-y3)/((x1-x3)**2+(y1-y3)**2)**(3/2)+G_const*m2*(y2-y3)/((x2-x3)**2+(y2-y3)**2)**(3/2)
    def EQ5 (Gr,_it) :
        return (
          y3.by_xx(_it)==G_const*fm1()*(fy1(_it)-fy3(_it))/((fx1(_it)-fx3(_it))**2+(fy1(_it)-fy3(_it))**2)**(3/2)+G_const*fm2()*(fy2(_it)-fy3(_it))/((fx2(_it)-fx3(_it))**2+(fy2(_it)-fy3(_it))**2)**(3/2)
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
    SvF.fun_with_mu.append(getFun('x3'))
    if x3.mu is None : x3.mu = Gr.mu0
    x3.ValidationSets = SvF.ValidationSets
    x3.notTrainingSets = SvF.notTrainingSets
    x3.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('y3'))
    if y3.mu is None : y3.mu = Gr.mu0
    y3.ValidationSets = SvF.ValidationSets
    y3.notTrainingSets = SvF.notTrainingSets
    y3.TrainingSets = SvF.TrainingSets
 											# x1.MSD()+y1.MSD()+x2.MSD()+y2.MSD()+x3.MSD()+y3.MSD()+x1.Complexity([Penal[0]])+y1.Complexity([Penal[1]])+x2.Complexity([Penal[2]])+y2.Complexity([Penal[3]])+x3.Complexity([Penal[4]])+y3.Complexity([Penal[5]])
    def obj_expression(Gr):  
        return (
             x1.MSD()+y1.MSD()+x2.MSD()+y2.MSD()+x3.MSD()+y3.MSD()+x1.Complexity([Penal[0]])+y1.Complexity([Penal[1]])+x2.Complexity([Penal[2]])+y2.Complexity([Penal[3]])+x3.Complexity([Penal[4]])+y3.Complexity([Penal[5]])
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x1 = Task.Funs[0]

    y1 = Task.Funs[1]

    x2 = Task.Funs[2]

    y2 = Task.Funs[3]

    x3 = Task.Funs[4]

    y3 = Task.Funs[5]

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
    tmp = (x2.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx2.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx2.MSD() ='+ stmp+'\n')
    tmp = (y2.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty2.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty2.MSD() ='+ stmp+'\n')
    tmp = (x3.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx3.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx3.MSD() ='+ stmp+'\n')
    tmp = (y3.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty3.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty3.MSD() ='+ stmp+'\n')
    tmp = (x1.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx1.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx1.Complexity([Penal[0]]) ='+ stmp+'\n')
    tmp = (y1.Complexity([Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty1.Complexity([Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty1.Complexity([Penal[1]]) ='+ stmp+'\n')
    tmp = (x2.Complexity([Penal[2]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx2.Complexity([Penal[2]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx2.Complexity([Penal[2]]) ='+ stmp+'\n')
    tmp = (y2.Complexity([Penal[3]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty2.Complexity([Penal[3]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty2.Complexity([Penal[3]]) ='+ stmp+'\n')
    tmp = (x3.Complexity([Penal[4]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx3.Complexity([Penal[4]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx3.Complexity([Penal[4]]) ='+ stmp+'\n')
    tmp = (y3.Complexity([Penal[5]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty3.Complexity([Penal[5]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty3.Complexity([Penal[5]]) ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
Plot( [ [ DB.dat('x1'), DB.dat('y1'), 'lw=0', 'c=gray', "marker='o'", 'ms=3', 'label=Date'], [DB.dat('x2'), DB.dat('y2'), 'label=""'], [DB.dat('x3'), DB.dat('y3')], [x1.grd, y1.grd, 'c=red', 'ms=0', 'lw=1', 'label=Alpha'], [x2.grd, y2.grd, 'c=b', 'label=Betta'], [x3.grd, y3.grd, 'c=green', 'label=Gamma'] ] )
Plot( [ [ x1, 'c=b'], [y1] ] )
Plot( [ [ x2], [y2] ] )
Plot( [ [ x3], [y3] ] )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")