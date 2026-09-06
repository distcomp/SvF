# -*- coding: UTF-8 -*-
import sys
sys.path.append("/home/sokol/D/SvF/SvFlib")
sys.path.append( "/home/sokol/D/SvF/pyomo-everest/python-api")
sys.path.append( "/home/sokol/D/SvF/pyomo-everest/ssop")
import COMMON as SvF
SvF.tmpFileDir = "/home/sokol/D/SvF/TMP/"
from CVSets import *
from Table  import *
from Task   import *
from MakeModel import *
from GIS import *

SvF.Task = TaskClass()
Task = SvF.Task
SvF.mngF = 'RESID_E_hours.mng'
SvF.Compile = False

currentTab = Table ( 'RESID_E_hours.dat','currentTab','*' )
hours = Set('hours',SvF.currentTab.dat('hours')[:].min(),SvF.currentTab.dat('hours')[:].max(),-50,'','hours')
Residual_E = Fun('Residual_E',[hours])
def fResidual_E(hours) : return Residual_E.F([hours])
CVmakeSets (  CV_NumSets=7, GroupBy="Dat" )
SvF.CVNumOfIter=11; 
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    Residual_E.var = py.Var ( Residual_E.A[0].NodS,domain=Reals )
    Residual_E.gr =  Residual_E.var
    Gr.Residual_E =  Residual_E.var

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('Residual_E'))
    if Residual_E.mu is None : Residual_E.mu = Gr.mu0
    Residual_E.ValidationSets = SvF.ValidationSets
    Residual_E.notTrainingSets = SvF.notTrainingSets
    Residual_E.TrainingSets = SvF.TrainingSets
 											# Residual_E.MSD()+Residual_E.Complexity([Penal[0]])
    def obj_expression(Gr):  
        return (
             Residual_E.MSD()+Residual_E.Complexity([Penal[0]])
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    Residual_E = Task.Funs[0]

    OBJ_ = SvF.optOBJ
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (Residual_E.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tResidual_E.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tResidual_E.MSD() ='+ stmp+'\n')
    tmp = (Residual_E.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tResidual_E.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tResidual_E.Complexity([Penal[0]]) ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
P1 = Polyline([0,Residual_E.A[0].max],[0,0], None, "P1")
Plot( [ [ Residual_E, 'dms=1'], [P1, 'c=green'] ] )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")
if SvF.addStrToRes != '':
    with open(SvF.resF, 'a') as f:  # RES filewrite
        f.write('addStrToRes: ' + SvF.addStrToRes)