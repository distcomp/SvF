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
Data = Table ( 'EXP_LAKE.xlsx','Data','X,Y,nP,Avg-TNi AS Ni,Year as t' )
X = Set('X',-100,100,-50,'','X')
Y = Set('Y',-100,100,-50,'','Y')
Ni_xy = Fun('Ni_xy',[X,Y])
def fNi_xy(X,Y) : return Ni_xy.F([X,Y])
fon = Tensor('fon',[])
def ffon() : return fon.F([])
Ni = smbFun('Ni',[X,Y])
def fNi(X,Y) : return Ni.F([X,Y])
def Ni_smbF00(Args) :
   X = Args[0]
   Y = Args[1]
   SvF.F_Arg_Type = "N"
   ret = fNi_xy(X,Y)+ffon()
   SvF.F_Arg_Type = ""
   return ret
Ni.smbF = Ni_smbF00
CVmakeSets (  CV_NumSets=7, GroupBy='nP' )
SvF.CVNumOfIter=-1; 
SvF.lenPenalty = 3
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    Ni_xy.var = py.Var ( Ni_xy.A[0].NodS,Ni_xy.A[1].NodS,domain=Reals, bounds=(0,None) )
    Ni_xy.gr =  Ni_xy.var
    Gr.Ni_xy =  Ni_xy.var

    fon.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    fon.gr =  fon.var
    Gr.fon =  fon.var
 								# Ni(X,Y)>=0
    def EQ0 (Gr,_iX,_iY) :
        return (
          fNi(_iX,_iY)>=0
        )
    Gr.conEQ0 = py.Constraint(X.FlNodS,Y.FlNodS,rule=EQ0 )

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('Ni'))
    if Ni.mu is None : Ni.mu = Gr.mu0
    Ni.ValidationSets = SvF.ValidationSets
    Ni.notTrainingSets = SvF.notTrainingSets
    Ni.TrainingSets = SvF.TrainingSets
 											# Ni.MSDrel(2.0)+Ni_xy.Complexity([Penal[0],Penal[1]])+Ni_xy.Norma_L2mL2Border()*Penal[2]*0.01
    def obj_expression(Gr):  
        return (
             Ni.MSDrel(2.0)+Ni_xy.Complexity([Penal[0],Penal[1]])+Ni_xy.Norma_L2mL2Border()*Penal[2]*0.01
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    Ni_xy = Task.Funs[0]

    Ni = Task.Funs[2]

    OBJ_ = SvF.optOBJ
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (Ni.MSDrel(2.0))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tNi.MSDrel(2.0) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tNi.MSDrel(2.0) ='+ stmp+'\n')
    tmp = (Ni_xy.Complexity([Penal[0],Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tNi_xy.Complexity([Penal[0],Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tNi_xy.Complexity([Penal[0],Penal[1]]) ='+ stmp+'\n')
    tmp = (Ni_xy.Norma_L2mL2Border()*Penal[2]*0.01)
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tNi_xy.Norma_L2mL2Border()*Penal[2]*0.01 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tNi_xy.Norma_L2mL2Border()*Penal[2]*0.01 ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
Data.AddField ("Residual_Ni")
for rr in Data.sR:
  Data.dat('Residual_Ni')[rr] = Data.dat('Ni')[rr] - fNi(Data.dat('X')[rr], Data.dat('Y')[rr])
Data.WriteSvFtbl("RESID_Ni_t//RESID_Ni_t.dat")
Data.KillField ("Residual_Ni")
Task.PlotAll ( )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")
if SvF.addStrToRes != '':
    with open(SvF.resF, 'a') as f:  # RES filewrite
        f.write('addStrToRes: ' + SvF.addStrToRes)