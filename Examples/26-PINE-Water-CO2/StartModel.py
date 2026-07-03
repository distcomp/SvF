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
SvF.mngF = 'Water-CO2.mng'
SvF.TaskName="PINE_Water_dynamics"; 
Wmin=68.0
Wmax=75.0
Wdel=Wmax-Wmin
Sneedles=32.0/2.0
Emult=Sneedles*6.48e-2
Dt=0.5
DB = Table ( 'Pine_Petr.xlsx','DB','ROWNUM,Q,VPD,E,Dat,H,T,hours,A' )
t = Set('t',SvF.currentTab.dat("ROWNUM")[:].min(),SvF.currentTab.dat("ROWNUM")[:].max(),1,'',"ROWNUM")
sQ = Set('sQ',SvF.currentTab.dat("Q")[:].min(),SvF.currentTab.dat("Q")[:].max(),-50,'',"Q")
sT = Set('sT',SvF.currentTab.dat("T")[:].min(),SvF.currentTab.dat("T")[:].max(),-50,'',"T")
sWD = Set('sWD',0,Wdel,-40,'','sWD')
Q = Fun('Q',[t], param=True)
def fQ(t) : return Q.F([t])
VPD = Fun('VPD',[t], param=True)
def fVPD(t) : return VPD.F([t])
Gq = Fun('Gq',[sQ])
def fGq(sQ) : return Gq.F([sQ])
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
Kwf = Tensor('Kwf',[])
def fKwf() : return Kwf.F([])
W = Fun('W',[t])
def fW(t) : return W.F([t])
E = Fun('E',[t])
def fE(t) : return E.F([t])
WD = Fun('WD',[t])
def fWD(t) : return WD.F([t])
WF = Fun('WF',[t])
def fWF(t) : return WF.F([t])
Gh2o = Fun('Gh2o',[t])
def fGh2o(t) : return Gh2o.F([t])
sCm = Set('sCm',215,370,-40,'','sCm')
sHours = Set('sHours',0,24,0.5,'',"hours")
hours = Fun('hours',[t], param=True)
def fhours(t) : return hours.F([t])
A = Fun('A',[t])
def fA(t) : return A.F([t])
Ci = Fun('Ci',[t])
def fCi(t) : return Ci.F([t])
Gci = Fun('Gci',[t])
def fGci(t) : return Gci.F([t])
P0 = Tensor('P0',[])
def fP0() : return P0.F([])
Pq = Fun('Pq',[sQ])
def fPq(sQ) : return Pq.F([sQ])
Pt = Fun('Pt',[sT])
def fPt(sT) : return Pt.F([sT])
Pcm = smbFun('Pcm',[sCm])
def fPcm(sCm) : return Pcm.F([sCm])
c_Pcm = Tensor('c_Pcm',[10])
def fc_Pcm(i) : return c_Pcm.F([i])
def Pcm_smbF00(Args) :
   sCm = Args[0]
   SvF.F_Arg_Type = "N"
   ret =  ( fc_Pcm(0)+fc_Pcm(1)*sCm+fc_Pcm(2)*sCm**2+fc_Pcm(3)*sCm**3+fc_Pcm(4)*sCm**4+fc_Pcm(5)*sCm**5+fc_Pcm(6)*sCm**6+fc_Pcm(7)*sCm**7+fc_Pcm(8)*sCm**8+fc_Pcm(9)*sCm**9 ) 
   SvF.F_Arg_Type = ""
   return ret
Pcm.smbF = Pcm_smbF00
Br = Tensor('Br',[])
def fBr() : return Br.F([])
T = Fun('T',[t], param=True)
def fT(t) : return T.F([t])
Cm = Fun('Cm',[t])
def fCm(t) : return Cm.F([t])
P = Fun('P',[t])
def fP(t) : return P.F([t])
Gcm = CycleFun('Gcm',[sHours])
def fGcm(sHours) : return Gcm.F([sHours])
CVmakeSets (  CV_NumSets=7, GroupBy='Dat' )
SvF.CVNumOfIter=1; 
SvF.OptStep=[0.,0.,0.,0,0.00001,0.00001]
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
 								# Gq(sQ.middle)=1
    def EQ0 (Gr) :
        return (
          fGq(sQ.middle)==1
        )
    Gr.conEQ0 = py.Constraint(rule=EQ0 )
 								# Gq'>0
    def EQ1 (Gr,_isQ) :
        return (
          Gq.by_x(_isQ)>=0
        )
    Gr.conEQ1 = py.Constraint(sQ.FlNodSm,rule=EQ1 )

    c_Gwd.var = py.Var ( range (c_Gwd.Sizes[0]),domain=Reals )
    c_Gwd.gr =  c_Gwd.var
    Gr.c_Gwd =  c_Gwd.var
 								# Gwd(sWD)<=1
    def EQ2 (Gr,_isWD) :
        return (
          fGwd(_isWD)<=1
        )
    Gr.conEQ2 = py.Constraint(sWD.FlNodS,rule=EQ2 )
 								# Gwd(0.)=1
    def EQ3 (Gr) :
        return (
          fGwd(0.)==1
        )
    Gr.conEQ3 = py.Constraint(rule=EQ3 )

    G0.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    G0.gr =  G0.var
    Gr.G0 =  G0.var

    Kwf.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    Kwf.gr =  Kwf.var
    Gr.Kwf =  Kwf.var

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

    Gh2o.var = py.Var ( Gh2o.A[0].NodS,domain=Reals )
    Gh2o.gr =  Gh2o.var
    Gr.Gh2o =  Gh2o.var
 								# d/dt(W)=(WF-E(t)*Emult)*Dt
    def EQ4 (Gr,_it) :
        return (
          W.by_x(_it)==(fWF(_it)-fE(_it)*Emult)*Dt
        )
    Gr.conEQ4 = py.Constraint(t.FlNodSm,rule=EQ4 )
 								# W(0)=Wmax-1.0
    def EQ5 (Gr) :
        return (
          fW(0)==Wmax-1.0
        )
    Gr.conEQ5 = py.Constraint(rule=EQ5 )
 								# WF=Kwf*WD
    def EQ6 (Gr,_it) :
        return (
          fWF(_it)==fKwf()*fWD(_it)
        )
    Gr.conEQ6 = py.Constraint(t.FlNodS,rule=EQ6 )
 								# WD=Wmax-W
    def EQ7 (Gr,_it) :
        return (
          fWD(_it)==Wmax-fW(_it)
        )
    Gr.conEQ7 = py.Constraint(t.FlNodS,rule=EQ7 )
 								# E=Gh2o*VPD*0.010017
    def EQ8 (Gr,_it) :
        return (
          fE(_it)==fGh2o(_it)*fVPD(_it)*0.010017
        )
    Gr.conEQ8 = py.Constraint(t.FlNodS,rule=EQ8 )
 								# Gh2o=G0*Gq(Q)*Gwd(WD)
    def EQ9 (Gr,_it) :
        return (
          fGh2o(_it)==fG0()*fGq(fQ(_it))*fGwd(fWD(_it))
        )
    Gr.conEQ9 = py.Constraint(t.FlNodS,rule=EQ9 )

    A.var = py.Var ( A.A[0].NodS,domain=Reals )
    A.gr =  A.var
    Gr.A =  A.var

    Ci.var = py.Var ( Ci.A[0].NodS,domain=Reals )
    Ci.gr =  Ci.var
    Gr.Ci =  Ci.var

    Gci.var = py.Var ( Gci.A[0].NodS,domain=Reals )
    Gci.gr =  Gci.var
    Gr.Gci =  Gci.var

    P0.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    P0.gr =  P0.var
    Gr.P0 =  P0.var

    Pq.var = py.Var ( Pq.A[0].NodS,domain=Reals, bounds=(0,None) )
    Pq.gr =  Pq.var
    Gr.Pq =  Pq.var
 								# Pq(0)=0
    def EQ10 (Gr) :
        return (
          fPq(0)==0
        )
    Gr.conEQ10 = py.Constraint(rule=EQ10 )
 								# Pq(sQ.middle)=1
    def EQ11 (Gr) :
        return (
          fPq(sQ.middle)==1
        )
    Gr.conEQ11 = py.Constraint(rule=EQ11 )
 								# Pq'>=0
    def EQ12 (Gr,_isQ) :
        return (
          Pq.by_x(_isQ)>=0
        )
    Gr.conEQ12 = py.Constraint(sQ.FlNodSm,rule=EQ12 )

    Pt.var = py.Var ( Pt.A[0].NodS,domain=Reals, bounds=(0,None) )
    Pt.gr =  Pt.var
    Gr.Pt =  Pt.var
 								# Pt(sT.middle)=1
    def EQ13 (Gr) :
        return (
          fPt(sT.middle)==1
        )
    Gr.conEQ13 = py.Constraint(rule=EQ13 )
 								# Pt'>=0
    def EQ14 (Gr,_isT) :
        return (
          Pt.by_x(_isT)>=0
        )
    Gr.conEQ14 = py.Constraint(sT.FlNodSm,rule=EQ14 )

    c_Pcm.var = py.Var ( range (c_Pcm.Sizes[0]),domain=Reals )
    c_Pcm.gr =  c_Pcm.var
    Gr.c_Pcm =  c_Pcm.var
 								# Pcm(sCm)>=0
    def EQ15 (Gr,_isCm) :
        return (
          fPcm(_isCm)>=0
        )
    Gr.conEQ15 = py.Constraint(sCm.FlNodS,rule=EQ15 )
 								# Pcm(360)=1
    def EQ16 (Gr) :
        return (
          fPcm(360)==1
        )
    Gr.conEQ16 = py.Constraint(rule=EQ16 )
 								# Pcm'>=0
    def EQ17 (Gr,_isCm) :
        return (
          Pcm.by_x(_isCm)>=0
        )
    Gr.conEQ17 = py.Constraint(sCm.FlNodSm,rule=EQ17 )

    Br.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    Br.gr =  Br.var
    Gr.Br =  Br.var

    Cm.var = py.Var ( Cm.A[0].NodS,domain=Reals, bounds=(sCm.min,None) )
    Cm.gr =  Cm.var
    Gr.Cm =  Cm.var
 								# Ci<sCm.max
    def EQ18 (Gr,_it) :
        return (
          fCi(_it)<=sCm.max
        )
    Gr.conEQ18 = py.Constraint(t.FlNodS,rule=EQ18 )

    P.var = py.Var ( P.A[0].NodS,domain=Reals )
    P.gr =  P.var
    Gr.P =  P.var

    Gcm.var = py.Var ( Gcm.A[0].NodS,domain=Reals, bounds=(0.2,0.4) )
    Gcm.gr =  Gcm.var
    Gr.Gcm =  Gcm.var
 								# Gcm.var[0] = Gcm.var[Gcm.A[0].Ub]
    def EQ19 (Gr) :
        return (
          Gcm.var[0] == Gcm.var[Gcm.A[0].Ub]
        )
    Gr.conEQ19 = py.Constraint(rule=EQ19 )
 								# Gci=Gh2o/1.6
    def EQ20 (Gr,_it) :
        return (
          fGci(_it)==fGh2o(_it)/1.6
        )
    Gr.conEQ20 = py.Constraint(t.FlNodS,rule=EQ20 )
 								# A=Gci*(360-Ci)
    def EQ21 (Gr,_it) :
        return (
          fA(_it)==fGci(_it)*(360-fCi(_it))
        )
    Gr.conEQ21 = py.Constraint(t.FlNodS,rule=EQ21 )
 								# P=P0*Pq(Q)*Pt(T)*Pcm(Cm)
    def EQ22 (Gr,_it) :
        return (
          fP(_it)==fP0()*fPq(fQ(_it))*fPt(fT(_it))*fPcm(fCm(_it))
        )
    Gr.conEQ22 = py.Constraint(t.FlNodS,rule=EQ22 )
 								# A=P-Br
    def EQ23 (Gr,_it) :
        return (
          fA(_it)==fP(_it)-fBr()
        )
    Gr.conEQ23 = py.Constraint(t.FlNodS,rule=EQ23 )
 								# P=Gcm(hours)*(Ci-Cm)
    def EQ24 (Gr,_it) :
        return (
          fP(_it)==fGcm(fhours(_it))*(fCi(_it)-fCm(_it))
        )
    Gr.conEQ24 = py.Constraint(t.FlNodS,rule=EQ24 )

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('E'))
    if E.mu is None : E.mu = Gr.mu0
    E.ValidationSets = SvF.ValidationSets
    E.notTrainingSets = SvF.notTrainingSets
    E.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('A'))
    if A.mu is None : A.mu = Gr.mu0
    A.ValidationSets = SvF.ValidationSets
    A.notTrainingSets = SvF.notTrainingSets
    A.TrainingSets = SvF.TrainingSets
 											# E.MSD()+Gq.Complexity([Penal[0]])+Gwd.Complexity([Penal[1]])+A.MSD()+Pq.Complexity([Penal[2]])+Pt.Complexity([Penal[3]])+Pcm.Complexity([Penal[4]])+Gcm.Complexity([Penal[5]])
    def obj_expression(Gr):  
        return (
             E.MSD()+Gq.Complexity([Penal[0]])+Gwd.Complexity([Penal[1]])+A.MSD()+Pq.Complexity([Penal[2]])+Pt.Complexity([Penal[3]])+Pcm.Complexity([Penal[4]])+Gcm.Complexity([Penal[5]])
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    Gq = Task.Funs[2]

    Gwd = Task.Funs[3]

    E = Task.Funs[8]

    A = Task.Funs[13]

    Pq = Task.Funs[17]

    Pt = Task.Funs[18]

    Pcm = Task.Funs[19]

    Gcm = Task.Funs[25]

    OBJ_ = Gr.OBJ ()
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
    tmp = (A.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tA.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tA.MSD() ='+ stmp+'\n')
    tmp = (Pq.Complexity([Penal[2]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tPq.Complexity([Penal[2]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tPq.Complexity([Penal[2]]) ='+ stmp+'\n')
    tmp = (Pt.Complexity([Penal[3]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tPt.Complexity([Penal[3]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tPt.Complexity([Penal[3]]) ='+ stmp+'\n')
    tmp = (Pcm.Complexity([Penal[4]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tPcm.Complexity([Penal[4]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tPcm.Complexity([Penal[4]]) ='+ stmp+'\n')
    tmp = (Gcm.Complexity([Penal[5]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tGcm.Complexity([Penal[5]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tGcm.Complexity([Penal[5]]) ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
DB.AddField('Err')
DB.dat('Err')[:]=DB.dat('A')[:]-A.grd[:]
DB.AddField('Err_E')
DB.dat('Err_E')[:]=DB.dat('E')[:]-E.grd[:]
DB.WriteSvFtbl('Err.dat')
Task.PlotAll ( )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")