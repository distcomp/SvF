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
DB = Table ( '../4bdn-1_0.9_0.2_0.06-abc.xlsx','DB','t,x1,y1,z1,x2,y2,z2' )
t = Set('t',SvF.currentTab.dat('t')[:].min(),SvF.currentTab.dat('t')[:].max(),0.01,'','t')
x1 = Fun('x1',[t], param=True, ReadFrom="x1(t).sol")
def fx1(t) : return x1.F([t])
y1 = Fun('y1',[t], param=True, ReadFrom="y1(t).sol")
def fy1(t) : return y1.F([t])
z1 = Fun('z1',[t], param=True, ReadFrom="z1(t).sol")
def fz1(t) : return z1.F([t])
x2 = Fun('x2',[t], param=True, ReadFrom="x2(t).sol")
def fx2(t) : return x2.F([t])
y2 = Fun('y2',[t], param=True, ReadFrom="y2(t).sol")
def fy2(t) : return y2.F([t])
z2 = Fun('z2',[t], param=True, ReadFrom="z2(t).sol")
def fz2(t) : return z2.F([t])
for nt,tt in enumerate(x1.A[0].dat):
  DB.dat('x1')[nt]-=fx1(tt)
  DB.dat('y1')[nt]-=fy1(tt)
  DB.dat('z1')[nt]-=fz1(tt)
  DB.dat('x2')[nt]-=fx2(tt)
  DB.dat('y2')[nt]-=fy2(tt)
  DB.dat('z2')[nt]-=fz2(tt)
x1r = Fun('x1r',[t], Data=['x1','t'])
def fx1r(t) : return x1r.F([t])
y1r = Fun('y1r',[t], Data=['y1','t'])
def fy1r(t) : return y1r.F([t])
z1r = Fun('z1r',[t], Data=['z1','t'])
def fz1r(t) : return z1r.F([t])
x2r = Fun('x2r',[t], Data=['x2','t'])
def fx2r(t) : return x2r.F([t])
y2r = Fun('y2r',[t], Data=['y2','t'])
def fy2r(t) : return y2r.F([t])
z2r = Fun('z2r',[t], Data=['z2','t'])
def fz2r(t) : return z2r.F([t])
CVmakeSets (  CV_NumSets=7 )
SvF.CVNumOfIter=1; 
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    x1r.var = py.Var ( x1r.A[0].NodS,domain=Reals )
    x1r.gr =  x1r.var
    Gr.x1r =  x1r.var

    y1r.var = py.Var ( y1r.A[0].NodS,domain=Reals )
    y1r.gr =  y1r.var
    Gr.y1r =  y1r.var

    z1r.var = py.Var ( z1r.A[0].NodS,domain=Reals )
    z1r.gr =  z1r.var
    Gr.z1r =  z1r.var

    x2r.var = py.Var ( x2r.A[0].NodS,domain=Reals )
    x2r.gr =  x2r.var
    Gr.x2r =  x2r.var

    y2r.var = py.Var ( y2r.A[0].NodS,domain=Reals )
    y2r.gr =  y2r.var
    Gr.y2r =  y2r.var

    z2r.var = py.Var ( z2r.A[0].NodS,domain=Reals )
    z2r.gr =  z2r.var
    Gr.z2r =  z2r.var

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('x1r'))
    if x1r.mu is None : x1r.mu = Gr.mu0
    x1r.ValidationSets = SvF.ValidationSets
    x1r.notTrainingSets = SvF.notTrainingSets
    x1r.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('y1r'))
    if y1r.mu is None : y1r.mu = Gr.mu0
    y1r.ValidationSets = SvF.ValidationSets
    y1r.notTrainingSets = SvF.notTrainingSets
    y1r.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('z1r'))
    if z1r.mu is None : z1r.mu = Gr.mu0
    z1r.ValidationSets = SvF.ValidationSets
    z1r.notTrainingSets = SvF.notTrainingSets
    z1r.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('x2r'))
    if x2r.mu is None : x2r.mu = Gr.mu0
    x2r.ValidationSets = SvF.ValidationSets
    x2r.notTrainingSets = SvF.notTrainingSets
    x2r.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('y2r'))
    if y2r.mu is None : y2r.mu = Gr.mu0
    y2r.ValidationSets = SvF.ValidationSets
    y2r.notTrainingSets = SvF.notTrainingSets
    y2r.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('z2r'))
    if z2r.mu is None : z2r.mu = Gr.mu0
    z2r.ValidationSets = SvF.ValidationSets
    z2r.notTrainingSets = SvF.notTrainingSets
    z2r.TrainingSets = SvF.TrainingSets
 											# x1r.MSD()+x1r.Complexity([Penal[0]])+y1r.MSD()+y1r.Complexity([Penal[0]])+z1r.MSD()+z1r.Complexity([Penal[0]])+x2r.MSD()+x2r.Complexity([Penal[0]])+y2r.MSD()+y2r.Complexity([Penal[0]])+z2r.MSD()+z2r.Complexity([Penal[0]])
    def obj_expression(Gr):  
        return (
             x1r.MSD()+x1r.Complexity([Penal[0]])+y1r.MSD()+y1r.Complexity([Penal[0]])+z1r.MSD()+z1r.Complexity([Penal[0]])+x2r.MSD()+x2r.Complexity([Penal[0]])+y2r.MSD()+y2r.Complexity([Penal[0]])+z2r.MSD()+z2r.Complexity([Penal[0]])
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x1r = Task.Funs[6]

    y1r = Task.Funs[7]

    z1r = Task.Funs[8]

    x2r = Task.Funs[9]

    y2r = Task.Funs[10]

    z2r = Task.Funs[11]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (x1r.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx1r.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx1r.MSD() ='+ stmp+'\n')
    tmp = (x1r.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx1r.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx1r.Complexity([Penal[0]]) ='+ stmp+'\n')
    tmp = (y1r.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty1r.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty1r.MSD() ='+ stmp+'\n')
    tmp = (y1r.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty1r.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty1r.Complexity([Penal[0]]) ='+ stmp+'\n')
    tmp = (z1r.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tz1r.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tz1r.MSD() ='+ stmp+'\n')
    tmp = (z1r.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tz1r.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tz1r.Complexity([Penal[0]]) ='+ stmp+'\n')
    tmp = (x2r.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx2r.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx2r.MSD() ='+ stmp+'\n')
    tmp = (x2r.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx2r.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx2r.Complexity([Penal[0]]) ='+ stmp+'\n')
    tmp = (y2r.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty2r.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty2r.MSD() ='+ stmp+'\n')
    tmp = (y2r.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty2r.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty2r.Complexity([Penal[0]]) ='+ stmp+'\n')
    tmp = (z2r.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tz2r.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tz2r.MSD() ='+ stmp+'\n')
    tmp = (z2r.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tz2r.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tz2r.Complexity([Penal[0]]) ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
P0 = Polyline([x1r.A[0].min,x1r.A[0].max],[0,0], None, "P0")
Plot( [ [ x1r, 'dms=1'], [P0, 'c=green', 'lab="Err=0"'] ] )
Plot( [ [ y1r, 'dms=1'], [P0, 'c=green', 'lab="Err=0"'] ] )
Plot( [ [ z1r, 'dms=1'], [P0, 'c=green', 'lab="Err=0"'] ] )
Plot( [ [ x2r, 'dms=1'], [P0, 'c=green', 'lab="Err=0"'] ] )
Plot( [ [ y2r, 'dms=1'], [P0, 'c=green', 'lab="Err=0"'] ] )
Plot( [ [ z2r, 'dms=1'], [P0, 'c=green', 'lab="Err=0"'] ] )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")