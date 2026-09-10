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

SvF.TaskName="Ni_field_XY_Kola_with_fon"; 
Data = Table ( 'EXP_LAKE.xlsx','Data','Year as t,X,Y,nP,Avg-TNi AS Ni' )
X = Set('X',-100,100,-50,'','X')
Y = Set('Y',-100,100,-50,'','Y')
t = Set('t',SvF.currentTab.dat('t')[:].min(),SvF.currentTab.dat('t')[:].max(),1,'','t')
Ni_field = Fun('Ni_field',[X,Y], ArgNorm=False)
def fNi_field(X,Y) : return Ni_field.F([X,Y])
Ni_t = Fun('Ni_t',[t], ArgNorm=False)
def fNi_t(t) : return Ni_t.F([t])
fon = Tensor('fon',[])
def ffon() : return fon.F([])
Ni = smbFun('Ni',[X,Y,t], ArgNorm=False)
def fNi(X,Y,t) : return Ni.F([X,Y,t])
def Ni_smbF00(Args) :
   X = Args[0]
   Y = Args[1]
   t = Args[2]
   ret = fNi_field(X,Y)*fNi_t(t)+ffon()
   return ret
Ni.smbF = Ni_smbF00
CVmakeSets (  CV_NumSets=7, GroupBy='t' )
SvF.CVNumOfIter=1; SvF.RunMode="S&S"; 
SvF.lenPenalty = 3
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    Ni_field.var = py.Var ( Ni_field.A[0].NodS,Ni_field.A[1].NodS,domain=Reals, bounds=(0,None) )
    Ni_field.gr =  Ni_field.var
    Gr.Ni_field =  Ni_field.var

    Ni_t.var = py.Var ( Ni_t.A[0].NodS,domain=Reals, bounds=(0,None) )
    Ni_t.gr =  Ni_t.var
    Gr.Ni_t =  Ni_t.var
 								# Ni_t(1995)=1
    def EQ0 (Gr) :
        return (
          fNi_t(1995)==1
        )
    Gr.conEQ0 = py.Constraint(rule=EQ0 )

    fon.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    fon.gr =  fon.var
    Gr.fon =  fon.var
 								# Ni(X,Y,t)>=0
    def EQ1 (Gr,_iX,_iY,_it) :
        return (
          fNi(_iX,_iY,_it)>=0
        )
    Gr.conEQ1 = py.Constraint(X.FlNodS,Y.FlNodS,t.FlNodS,rule=EQ1 )

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('Ni'))
    if Ni.mu is None : Ni.mu = Gr.mu0
    Ni.ValidationSets = SvF.ValidationSets
    Ni.notTrainingSets = SvF.notTrainingSets
    Ni.TrainingSets = SvF.TrainingSets
 											# Ni.MSDrel(2.0)+Ni_field.Complexity([Penal[0],Penal[1]])+Ni_t.Complexity([Penal[2]])+Ni_field.Norma_L2mL2Border()*0.0001
    def obj_expression(Gr):  
        return (
             Ni.MSDrel(2.0)+Ni_field.Complexity([Penal[0],Penal[1]])+Ni_t.Complexity([Penal[2]])+Ni_field.Norma_L2mL2Border()*0.0001
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    Ni_field = Task.Funs[0]

    Ni_t = Task.Funs[1]

    Ni = Task.Funs[3]

    OBJ_ = SvF.optOBJ
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (Ni.MSDrel(2.0))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tNi.MSDrel(2.0) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tNi.MSDrel(2.0) ='+ stmp+'\n')
    tmp = (Ni_field.Complexity([Penal[0],Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tNi_field.Complexity([Penal[0],Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tNi_field.Complexity([Penal[0],Penal[1]]) ='+ stmp+'\n')
    tmp = (Ni_t.Complexity([Penal[2]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tNi_t.Complexity([Penal[2]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tNi_t.Complexity([Penal[2]]) ='+ stmp+'\n')
    tmp = (Ni_field.Norma_L2mL2Border()*0.0001)
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tNi_field.Norma_L2mL2Border()*0.0001 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tNi_field.Norma_L2mL2Border()*0.0001 ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
Plot( [ [ Ni_t] ] )
Plot( [ [ Ni_field] ] )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")
if SvF.addStrToRes != '':
    with open(SvF.resF, 'a') as f:  # RES filewrite
        f.write('addStrToRes: ' + SvF.addStrToRes)