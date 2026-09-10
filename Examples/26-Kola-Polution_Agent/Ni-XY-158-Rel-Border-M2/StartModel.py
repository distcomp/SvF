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
SvF.mngF = 'Ni_distribution.mng'
SvF.Compile = False

SvF.TaskName="Ni_field_XY_Kola"; 
Data = Table ( 'EXP_LAKE.xlsx','Data','X,Y,nP,Avg-TNi AS Ni' )
X = Set('X',-100,100,-50,'','X')
Y = Set('Y',-100,100,-50,'','Y')
Ni = Fun('Ni',[X,Y])
def fNi(X,Y) : return Ni.F([X,Y])
CVmakeSets (  CV_NumSets=7, GroupBy='nP' )
SvF.CVNumOfIter=21; 
SvF.lenPenalty = 3
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    Ni.var = py.Var ( Ni.A[0].NodS,Ni.A[1].NodS,domain=Reals, bounds=(0,None) )
    Ni.gr =  Ni.var
    Gr.Ni =  Ni.var

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('Ni'))
    if Ni.mu is None : Ni.mu = Gr.mu0
    Ni.ValidationSets = SvF.ValidationSets
    Ni.notTrainingSets = SvF.notTrainingSets
    Ni.TrainingSets = SvF.TrainingSets
 											# Ni.MSDrel(2.0)+Ni.Complexity([Penal[0],Penal[1]])+Ni.Norma_L2mL2Border()*Penal[2]*0.01
    def obj_expression(Gr):  
        return (
             Ni.MSDrel(2.0)+Ni.Complexity([Penal[0],Penal[1]])+Ni.Norma_L2mL2Border()*Penal[2]*0.01
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    Ni = Task.Funs[0]

    OBJ_ = SvF.optOBJ
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (Ni.MSDrel(2.0))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tNi.MSDrel(2.0) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tNi.MSDrel(2.0) ='+ stmp+'\n')
    tmp = (Ni.Complexity([Penal[0],Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tNi.Complexity([Penal[0],Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tNi.Complexity([Penal[0],Penal[1]]) ='+ stmp+'\n')
    tmp = (Ni.Norma_L2mL2Border()*Penal[2]*0.01)
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tNi.Norma_L2mL2Border()*Penal[2]*0.01 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tNi.Norma_L2mL2Border()*Penal[2]*0.01 ='+ stmp+'\n')

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
if SvF.addStrToRes != '':
    with open(SvF.resF, 'a') as f:  # RES filewrite
        f.write('addStrToRes: ' + SvF.addStrToRes)