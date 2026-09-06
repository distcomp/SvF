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
SvF.mngF = 'Water-dynamics.mng'
SvF.Compile = False

SvF.TaskName="PINE_Water_dynamics"; 
Wmin=68.0
Wmax=75.0
Wdel=Wmax-Wmin
Sneedles=32.0/2.0
Emult=Sneedles*6.48e-2
Dt=0.5
DB = Table ( '../Pine_Petr-08.xlsx','DB','ROWNUM,Q,T,VPD,E,Dat,hours' )
t = Set('t',SvF.currentTab.dat("ROWNUM")[:].min(),SvF.currentTab.dat("ROWNUM")[:].max(),1,'',"ROWNUM")
sQ = Set('sQ',SvF.currentTab.dat("Q")[:].min(),SvF.currentTab.dat("Q")[:].max(),-50,'',"Q")
sVPD = Set('sVPD',SvF.currentTab.dat("VPD")[:].min(),SvF.currentTab.dat("VPD")[:].max(),-50,'',"VPD")
sWD = Set('sWD',0,Wdel,-40,'','sWD')
Q = Fun('Q',[t], param=True)
def fQ(t) : return Q.F([t])
VPD = Fun('VPD',[t], param=True)
def fVPD(t) : return VPD.F([t])
T = Fun('T',[t], param=True)
def fT(t) : return T.F([t])
Gq = Fun('Gq',[sQ])
def fGq(sQ) : return Gq.F([sQ])
Gvpd = smbFun('Gvpd',[sVPD])
def fGvpd(sVPD) : return Gvpd.F([sVPD])
c_Gvpd = Tensor('c_Gvpd',[5])
def fc_Gvpd(i) : return c_Gvpd.F([i])
def Gvpd_smbF00(Args) :
   sVPD = Args[0]
   SvF.F_Arg_Type = "N"
   ret =  ( fc_Gvpd(0)+fc_Gvpd(1)*sVPD+fc_Gvpd(2)*sVPD**2+fc_Gvpd(3)*sVPD**3+fc_Gvpd(4)*sVPD**4 ) 
   SvF.F_Arg_Type = ""
   return ret
Gvpd.smbF = Gvpd_smbF00
Gwd = smbFun('Gwd',[sWD])
def fGwd(sWD) : return Gwd.F([sWD])
c_Gwd = Tensor('c_Gwd',[6])
def fc_Gwd(i) : return c_Gwd.F([i])
def Gwd_smbF00(Args) :
   sWD = Args[0]
   SvF.F_Arg_Type = "N"
   ret =  ( fc_Gwd(0)+fc_Gwd(1)*sWD+fc_Gwd(2)*sWD**2+fc_Gwd(3)*sWD**3+fc_Gwd(4)*sWD**4+fc_Gwd(5)*sWD**5 ) 
   SvF.F_Arg_Type = ""
   return ret
Gwd.smbF = Gwd_smbF00
G0 = Tensor('G0',[])
def fG0() : return G0.F([])
WFwd = smbFun('WFwd',[sWD])
def fWFwd(sWD) : return WFwd.F([sWD])
c_WFwd = Tensor('c_WFwd',[2])
def fc_WFwd(i) : return c_WFwd.F([i])
def WFwd_smbF00(Args) :
   sWD = Args[0]
   SvF.F_Arg_Type = "N"
   ret =  ( fc_WFwd(0)+fc_WFwd(1)*sWD ) 
   SvF.F_Arg_Type = ""
   return ret
WFwd.smbF = WFwd_smbF00
W = Fun('W',[t])
def fW(t) : return W.F([t])
E = Fun('E',[t])
def fE(t) : return E.F([t])
WD = Fun('WD',[t])
def fWD(t) : return WD.F([t])
WF = Fun('WF',[t])
def fWF(t) : return WF.F([t])
G = Fun('G',[t])
def fG(t) : return G.F([t])
CVmakeSets (  CV_NumSets=7, GroupBy='Dat' )
SvF.CVNumOfIter=1; SvF.RunMode="L&S"; 
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    Gq.var = py.Var ( Gq.A[0].NodS,domain=Reals )
    Gq.gr =  Gq.var
    Gr.Gq =  Gq.var
 								# Gq'>0
    def EQ0 (Gr,_isQ) :
        return (
          Gq.by_x(_isQ)>=0
        )
    Gr.conEQ0 = py.Constraint(sQ.FlNodSm,rule=EQ0 )
 								# Gq(sQ.middle)=1
    def EQ1 (Gr) :
        return (
          fGq(sQ.middle)==1
        )
    Gr.conEQ1 = py.Constraint(rule=EQ1 )

    c_Gvpd.var = py.Var ( range (c_Gvpd.Sizes[0]),domain=Reals )
    c_Gvpd.gr =  c_Gvpd.var
    Gr.c_Gvpd =  c_Gvpd.var
 								# Gvpd(sVPD.middle)=1
    def EQ2 (Gr) :
        return (
          fGvpd(sVPD.middle)==1
        )
    Gr.conEQ2 = py.Constraint(rule=EQ2 )

    c_Gwd.var = py.Var ( range (c_Gwd.Sizes[0]),domain=Reals )
    c_Gwd.gr =  c_Gwd.var
    Gr.c_Gwd =  c_Gwd.var
 								# Gwd(sWD)<=1
    def EQ3 (Gr,_isWD) :
        return (
          fGwd(_isWD)<=1
        )
    Gr.conEQ3 = py.Constraint(sWD.FlNodS,rule=EQ3 )
 								# Gwd(0.)=1
    def EQ4 (Gr) :
        return (
          fGwd(0.)==1
        )
    Gr.conEQ4 = py.Constraint(rule=EQ4 )

    G0.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    G0.gr =  G0.var
    Gr.G0 =  G0.var

    c_WFwd.var = py.Var ( range (c_WFwd.Sizes[0]),domain=Reals )
    c_WFwd.gr =  c_WFwd.var
    Gr.c_WFwd =  c_WFwd.var
 								# WFwd(sWD)>=0
    def EQ5 (Gr,_isWD) :
        return (
          fWFwd(_isWD)>=0
        )
    Gr.conEQ5 = py.Constraint(sWD.FlNodS,rule=EQ5 )

    W.var = py.Var ( W.A[0].NodS,domain=Reals )
    W.gr =  W.var
    Gr.W =  W.var

    E.var = py.Var ( E.A[0].NodS,domain=Reals )
    E.gr =  E.var
    Gr.E =  E.var

    WD.var = py.Var ( WD.A[0].NodS,domain=Reals, bounds=(0,Wdel) )
    WD.gr =  WD.var
    Gr.WD =  WD.var

    WF.var = py.Var ( WF.A[0].NodS,domain=Reals )
    WF.gr =  WF.var
    Gr.WF =  WF.var

    G.var = py.Var ( G.A[0].NodS,domain=Reals )
    G.gr =  G.var
    Gr.G =  G.var
 								# d/dt(W)=(WF-E(t)*Emult)*Dt
    def EQ6 (Gr,_it) :
        return (
          W.by_x(_it)==(fWF(_it)-fE(_it)*Emult)*Dt
        )
    Gr.conEQ6 = py.Constraint(t.FlNodSm,rule=EQ6 )
 								# W(0)=Wmax-1.0
    def EQ7 (Gr) :
        return (
          fW(0)==Wmax-1.0
        )
    Gr.conEQ7 = py.Constraint(rule=EQ7 )
 								# WF=WFwd(WD)
    def EQ8 (Gr,_it) :
        return (
          fWF(_it)==fWFwd(fWD(_it))
        )
    Gr.conEQ8 = py.Constraint(t.FlNodS,rule=EQ8 )
 								# WD=Wmax-W
    def EQ9 (Gr,_it) :
        return (
          fWD(_it)==Wmax-fW(_it)
        )
    Gr.conEQ9 = py.Constraint(t.FlNodS,rule=EQ9 )
 								# E=G*VPD*0.010017
    def EQ10 (Gr,_it) :
        return (
          fE(_it)==fG(_it)*fVPD(_it)*0.010017
        )
    Gr.conEQ10 = py.Constraint(t.FlNodS,rule=EQ10 )
 								# G=G0*Gq(Q)*Gvpd(VPD)*Gwd(WD)
    def EQ11 (Gr,_it) :
        return (
          fG(_it)==fG0()*fGq(fQ(_it))*fGvpd(fVPD(_it))*fGwd(fWD(_it))
        )
    Gr.conEQ11 = py.Constraint(t.FlNodS,rule=EQ11 )

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('E'))
    if E.mu is None : E.mu = Gr.mu0
    E.ValidationSets = SvF.ValidationSets
    E.notTrainingSets = SvF.notTrainingSets
    E.TrainingSets = SvF.TrainingSets
 											# E.MSD()+Gq.Complexity([Penal[0]])+Gwd.Complexity([Penal[1]])+Gvpd.Complexity([Penal[2]])
    def obj_expression(Gr):  
        return (
             E.MSD()+Gq.Complexity([Penal[0]])+Gwd.Complexity([Penal[1]])+Gvpd.Complexity([Penal[2]])
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    Gq = Task.Funs[3]

    Gvpd = Task.Funs[4]

    Gwd = Task.Funs[6]

    E = Task.Funs[12]

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
    tmp = (Gwd.Complexity([Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tGwd.Complexity([Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tGwd.Complexity([Penal[1]]) ='+ stmp+'\n')
    tmp = (Gvpd.Complexity([Penal[2]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tGvpd.Complexity([Penal[2]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tGvpd.Complexity([Penal[2]]) ='+ stmp+'\n')

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
  DB.dat('Residual_E')[rr] = DB.dat('E')[rr] - fE(DB.dat('ROWNUM')[rr])
DB.WriteSvFtbl("RESID_E_hours//RESID_E_hours.dat")
DB.KillField ("Residual_E")
DB.AddField ("Residual_E")
for rr in DB.sR:
  DB.dat('Residual_E')[rr] = DB.dat('E')[rr] - fE(DB.dat('ROWNUM')[rr])
DB.WriteSvFtbl("RESID_E_T//RESID_E_T.dat")
DB.KillField ("Residual_E")
DB.AddField ("Residual_E")
for rr in DB.sR:
  DB.dat('Residual_E')[rr] = DB.dat('E')[rr] - fE(DB.dat('ROWNUM')[rr])
DB.WriteSvFtbl("RESID_E_VPD//RESID_E_VPD.dat")
DB.KillField ("Residual_E")
DB.AddField ("Residual_E")
for rr in DB.sR:
  DB.dat('Residual_E')[rr] = DB.dat('E')[rr] - fE(DB.dat('ROWNUM')[rr])
DB.WriteSvFtbl("RESID_E_Q//RESID_E_Q.dat")
DB.KillField ("Residual_E")
Task.PlotAll ( )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")
if SvF.addStrToRes != '':
    with open(SvF.resF, 'a') as f:  # RES filewrite
        f.write('addStrToRes: ' + SvF.addStrToRes)