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
SvF.mngF = 'Eq_Evpd.mng'
SvF.Compile = False

DB = Table ( '../Pine_Petr-08.xlsx','DB','ROWNUM as t,Q,T,VPD,E,Dat,hours' )
sQ = Set('sQ',SvF.currentTab.dat("Q")[:].min(),SvF.currentTab.dat("Q")[:].max(),-50,'',"Q")
sVPD = Set('sVPD',SvF.currentTab.dat("VPD")[:].min(),SvF.currentTab.dat("VPD")[:].max(),-50,'',"VPD")
t = Set('t',SvF.currentTab.dat('t')[:].min(),SvF.currentTab.dat('t')[:].max(),1,'','t')
Q = Fun('Q',[t], param=True)
def fQ(t) : return Q.F([t])
VPD = Fun('VPD',[t], param=True)
def fVPD(t) : return VPD.F([t])
E = Fun('E',[t])
def fE(t) : return E.F([t])
Gq = Fun('Gq',[sQ])
def fGq(sQ) : return Gq.F([sQ])
Gvpd = Fun('Gvpd',[sVPD])
def fGvpd(sVPD) : return Gvpd.F([sVPD])
G0 = Tensor('G0',[])
def fG0() : return G0.F([])
CVmakeSets (  CV_NumSets=7, GroupBy='Dat' )
SvF.CVNumOfIter=1; 
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    E.var = py.Var ( E.A[0].NodS,domain=Reals )
    E.gr =  E.var
    Gr.E =  E.var

    Gq.var = py.Var ( Gq.A[0].NodS,domain=Reals )
    Gq.gr =  Gq.var
    Gr.Gq =  Gq.var
 								# Gq(sQ.middle)=1
    def EQ0 (Gr) :
        return (
          fGq(sQ.middle)==1
        )
    Gr.conEQ0 = py.Constraint(rule=EQ0 )

    Gvpd.var = py.Var ( Gvpd.A[0].NodS,domain=Reals )
    Gvpd.gr =  Gvpd.var
    Gr.Gvpd =  Gvpd.var
 								# Gvpd(sVPD.middle)=1
    def EQ1 (Gr) :
        return (
          fGvpd(sVPD.middle)==1
        )
    Gr.conEQ1 = py.Constraint(rule=EQ1 )

    G0.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    G0.gr =  G0.var
    Gr.G0 =  G0.var
 								# E(t)=G0*Gq(Q)*Gvpd(VPD)*0.010017*VPD
    def EQ2 (Gr,_it) :
        return (
          fE(_it)==fG0()*fGq(fQ(_it))*fGvpd(fVPD(_it))*0.010017*fVPD(_it)
        )
    Gr.conEQ2 = py.Constraint(t.FlNodS,rule=EQ2 )

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('E'))
    if E.mu is None : E.mu = Gr.mu0
    E.ValidationSets = SvF.ValidationSets
    E.notTrainingSets = SvF.notTrainingSets
    E.TrainingSets = SvF.TrainingSets
 											# E.MSD()+Gq.Complexity([Penal[0]])+Gvpd.Complexity([Penal[1]])
    def obj_expression(Gr):  
        return (
             E.MSD()+Gq.Complexity([Penal[0]])+Gvpd.Complexity([Penal[1]])
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    E = Task.Funs[2]

    Gq = Task.Funs[3]

    Gvpd = Task.Funs[4]

    OBJ_ = SvF.optOBJ
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (E.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tE.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tE.MSD() ='+ stmp+'\n')
    tmp = (Gq.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tGq.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tGq.Complexity([Penal[0]]) ='+ stmp+'\n')
    tmp = (Gvpd.Complexity([Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tGvpd.Complexity([Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tGvpd.Complexity([Penal[1]]) ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
DB.AddField ("Residual_E")
for rr in DB.sR:
  DB.dat('Residual_E')[rr] = DB.dat('E')[rr] - fE(DB.dat('t')[rr])
DB.WriteSvFtbl("RESID_E_hours//RESID_E_hours.dat")
DB.KillField ("Residual_E")
Task.PlotAll ( )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")
if SvF.addStrToRes != '':
    with open(SvF.resF, 'a') as f:  # RES filewrite
        f.write('addStrToRes: ' + SvF.addStrToRes)