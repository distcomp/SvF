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
SvF.mngF = 'RESID_Ni_t.mng'
SvF.Compile = False

currentTab = Table ( 'RESID_Ni_t.dat','currentTab','*' )
t = Set('t',SvF.currentTab.dat('t')[:].min(),SvF.currentTab.dat('t')[:].max(),-50,'','t')
Residual_Ni = Fun('Residual_Ni',[t])
def fResidual_Ni(t) : return Residual_Ni.F([t])
CVmakeSets (  CV_NumSets=7 )
SvF.CVNumOfIter=11; 
SvF.lenPenalty = 1
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    Residual_Ni.var = py.Var ( Residual_Ni.A[0].NodS,domain=Reals )
    Residual_Ni.gr =  Residual_Ni.var
    Gr.Residual_Ni =  Residual_Ni.var

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('Residual_Ni'))
    if Residual_Ni.mu is None : Residual_Ni.mu = Gr.mu0
    Residual_Ni.ValidationSets = SvF.ValidationSets
    Residual_Ni.notTrainingSets = SvF.notTrainingSets
    Residual_Ni.TrainingSets = SvF.TrainingSets
 											# Residual_Ni.MSDrel(2.0)+Residual_Ni.Complexity([Penal[0]])
    def obj_expression(Gr):  
        return (
             Residual_Ni.MSDrel(2.0)+Residual_Ni.Complexity([Penal[0]])
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    Residual_Ni = Task.Funs[0]

    OBJ_ = SvF.optOBJ
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (Residual_Ni.MSDrel(2.0))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tResidual_Ni.MSDrel(2.0) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tResidual_Ni.MSDrel(2.0) ='+ stmp+'\n')
    tmp = (Residual_Ni.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tResidual_Ni.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tResidual_Ni.Complexity([Penal[0]]) ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
P1 = Polyline([Residual_Ni.A[0].min,Residual_Ni.A[0].max],[0,0], None, "P1")
Plot( [ [ Residual_Ni, 'dms=1'], [P1, 'c=green'] ] )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")
if SvF.addStrToRes != '':
    with open(SvF.resF, 'a') as f:  # RES filewrite
        f.write('addStrToRes: ' + SvF.addStrToRes)