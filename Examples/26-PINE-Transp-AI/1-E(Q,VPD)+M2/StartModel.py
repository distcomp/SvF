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
SvF.mngF = 'MNG.mng'
SvF.Compile = False

currentTab = Table ( '../Pine_Petr-08.xlsx','currentTab','Q,T,E,VPD,Dat' )
Q = Set('Q',SvF.currentTab.dat('Q')[:].min(),SvF.currentTab.dat('Q')[:].max(),-50,'','Q')
VPD = Set('VPD',SvF.currentTab.dat('VPD')[:].min(),SvF.currentTab.dat('VPD')[:].max(),-50,'','VPD')
E = Fun('E',[Q,VPD])
def fE(Q,VPD) : return E.F([Q,VPD])
CVmakeSets (  CV_NumSets=7, GroupBy='Dat' )
SvF.CVNumOfIter=21; 
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    E.var = py.Var ( E.A[0].NodS,E.A[1].NodS,domain=Reals )
    E.gr =  E.var
    Gr.E =  E.var

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('E'))
    if E.mu is None : E.mu = Gr.mu0
    E.ValidationSets = SvF.ValidationSets
    E.notTrainingSets = SvF.notTrainingSets
    E.TrainingSets = SvF.TrainingSets
 											# E.Complexity([Penal[0],Penal[1]])+E.MSD()
    def obj_expression(Gr):  
        return (
             E.Complexity([Penal[0],Penal[1]])+E.MSD()
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    E = Task.Funs[0]

    OBJ_ = SvF.optOBJ
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (E.Complexity([Penal[0],Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tE.Complexity([Penal[0],Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tE.Complexity([Penal[0],Penal[1]]) ='+ stmp+'\n')
    tmp = (E.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tE.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tE.MSD() ='+ stmp+'\n')

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