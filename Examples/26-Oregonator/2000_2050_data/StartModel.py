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
SvF.TaskName="Oregonator_Trajectories"; 
def where_condition ( t, X, Y, Z ):
    return (t<2050)
DB = Table ( '../oregonator_results_noisy.xlsx','DB','t,X,Y,Z',where_condition )
t = Set('t',SvF.currentTab.dat('t')[:].min(),2050,0.175,'','t')
X = Fun('X',[t])
def fX(t) : return X.F([t])
Y = Fun('Y',[t])
def fY(t) : return Y.F([t])
Z = Fun('Z',[t])
def fZ(t) : return Z.F([t])
CVmakeSets (  CV_NumSets=7 )
SvF.CVNumOfIter=-1; 
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    X.var = py.Var ( X.A[0].NodS,domain=Reals, bounds=(0,None) )
    X.gr =  X.var
    Gr.X =  X.var

    Y.var = py.Var ( Y.A[0].NodS,domain=Reals, bounds=(0,None) )
    Y.gr =  Y.var
    Gr.Y =  Y.var

    Z.var = py.Var ( Z.A[0].NodS,domain=Reals, bounds=(0,None) )
    Z.gr =  Z.var
    Gr.Z =  Z.var

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
 											# X.MSD()+Y.MSD()+Z.MSD()+X.Complexity([Penal[0]])+Y.Complexity([Penal[1]])+Z.Complexity([Penal[2]])
    def obj_expression(Gr):  
        return (
             X.MSD()+Y.MSD()+Z.MSD()+X.Complexity([Penal[0]])+Y.Complexity([Penal[1]])+Z.Complexity([Penal[2]])
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
    tmp = (X.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tX.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tX.Complexity([Penal[0]]) ='+ stmp+'\n')
    tmp = (Y.Complexity([Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tY.Complexity([Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tY.Complexity([Penal[1]]) ='+ stmp+'\n')
    tmp = (Z.Complexity([Penal[2]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tZ.Complexity([Penal[2]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tZ.Complexity([Penal[2]]) ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
Plot( [ [ DB.dat('t'), DB.dat('X'), 'lw=0', 'c=blue', 'mfc=none', "marker='o'", 'ms=3', "label='X data'", "xlab='t'", 'xlab_x=1.06', "ylab='X'"] ] )
Plot( [ [ DB.dat('t'), DB.dat('Y'), 'lw=0', 'c=blue', 'mfc=none', "marker='o'", 'ms=3', "label='Y data'", "xlab='t'", 'xlab_x=1.06', "ylab='Y'"] ] )
Plot( [ [ DB.dat('t'), DB.dat('Z'), 'lw=0', 'c=blue', 'mfc=none', "marker='o'", 'ms=3', "label='Z data'", "xlab='t'", 'xlab_x=1.06', "ylab='Z'"] ] )
Plot( [ [ DB.dat('X'), DB.dat('Z'), 'lw=0', 'c=green', "marker='.'", 'ms=3', "label='XZ data'", "xlab='X'", 'xlab_x=1.06', "ylab='Z'"] ] )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")