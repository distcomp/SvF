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
SvF.mngF = '24-12-Pine.odt'
Wmin=68.0
Wmax=75.0
Sneedles=32/2
Emult=Sneedles*6.48e-2
SvF.useNaN = True
DB = Table ( 'Phot-7shoX5_P.xlsx','DB','ROWNUM AS n,t,I AS Q,WPD AS VPD,WPD AS V,Ta AS T,H,EX5 AS E,PhX2 AS P,Dat,Date,Dt,NN,PRel,ERel' )
DB.dat('E')[:]*=1.12
SvF_MakeSets_byParam ( SvF.curentTabl.dat('Dat'), 11 )
n=Grid('n',0.0,SvF.curentTabl.dat('n')[:].max(),1.0,'i__n','n')
sWD=Grid('sWD',0.0,(Wmax-Wmin)/Wmax*100,-40.0,'i__sWD','sWD')
sQ=Grid('sQ',0.0,SvF.curentTabl.dat('Q')[:].max(),-50.0,'q','Q')
sT=Grid('sT',SvF.curentTabl.dat('T')[:].min(),SvF.curentTabl.dat('T')[:].max(),-50.0,'te','T')
st=Grid('st',0.0,24.0,0.5,'t','t')
sG=Grid('sG',0.0,0.4,-40.0,'i__sG','sG')
sCO2M=Grid('sCO2M',270.0,370.0,-40.0,'i__sCO2M','sCO2M')
Gq = Fun('Gq',[sQ],False,-1,1, '') 
def fGq(sQ) : return Gq.F([sQ])
Gwd = pFun('Gwd',[sWD],False,5,1, '') 
def fGwd(sWD) : return Gwd.F([sWD])
WFwd = Fun('WFwd',[],False,-1,1, '') 
WFwd.grd = 1
def fWFwd() : return WFwd.F([])
E = Fun('E',[n],False,-1,1, '') 
def fE(n) : return E.F([n])
W = Fun('W',[n],False,-1,1, '') 
def fW(n) : return W.F([n])
WD = Fun('WD',[n],False,-1,1, '') 
def fWD(n) : return WD.F([n])
WF = Fun('WF',[n],False,-1,1, '') 
def fWF(n) : return WF.F([n])
G = Fun('G',[n],False,-1,1, '') 
def fG(n) : return G.F([n])
VPD = Fun('VPD',[n],True,-1,1, '') 
def fVPD(n) : return VPD.F([n])
Q = Fun('Q',[n],True,-1,1, '') 
def fQ(n) : return Q.F([n])
T = Fun('T',[n],True,-1,1, '') 
def fT(n) : return T.F([n])
Dt = Fun('Dt',[n],True,-1,1, '') 
def fDt(n) : return Dt.F([n])
t = Fun('t',[n],True,-1,1, '') 
def ft(n) : return t.F([n])
P = Fun('P',[n],False,-1,1, '') 
def fP(n) : return P.F([n])
CO2I = Fun('CO2I',[n],False,-1,1, '') 
def fCO2I(n) : return CO2I.F([n])
CO2M = Fun('CO2M',[n],False,-1,1, '') 
def fCO2M(n) : return CO2M.F([n])
Pq = Fun('Pq',[sQ],False,-1,1, '') 
def fPq(sQ) : return Pq.F([sQ])
Pt = Fun('Pt',[sT],False,-1,1, '') 
def fPt(sT) : return Pt.F([sT])
Pm = pFun('Pm',[sCO2M],False,7,1, '') 
def fPm(sCO2M) : return Pm.F([sCO2M])
Pbr = Fun('Pbr',[],False,-1,1, '') 
Pbr.grd = 1
def fPbr() : return Pbr.F([])
GMt = Fun('GMt',[st],False,-1,1, '') 
def fGMt(st) : return GMt.F([st])
SvF.CVNumOfIter = 1
co.resF="MNG.res"
SvF.RunMode = "L&P"
SvF.max_workers=12
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr
    Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )

    Gq.var = py.Var ( Gq.A[0].NodS,domain=Reals, initialize = 1 )
    Gr.Gq =  Gq.var
    Gq.InitByData()
    Gq.mu = Gr.mu0;
 								# Gq'>=0
    def EQ0 (Gr,q) :
        return (
          ((fGq((q+sQ.step))-fGq(q))/sQ.step)>=0
        )
    Gr.conEQ0 = py.Constraint(sQ.FlNodSm,rule=EQ0 )

    Gwd.var = py.Var ( range (6), initialize = 0 )
    Gr.Gwd =  Gwd.var
    Gwd.mu = Gr.mu0;
    Gwd.var[0].value = 1
 								# Gwd(sWD)<=1
    def EQ1 (Gr,i__sWD) :
        return (
          fGwd(i__sWD)<=1
        )
    Gr.conEQ1 = py.Constraint(sWD.FlNodS,rule=EQ1 )
 								# Gwd'<=0
    def EQ2 (Gr,i__sWD) :
        return (
          (Gwd.dF_dX(i__sWD))<=0
        )
    Gr.conEQ2 = py.Constraint(sWD.FlNodS,rule=EQ2 )
 								# Gwd(0.0)=1
    def EQ3 (Gr) :
        return (
          fGwd(0.0)==1
        )
    Gr.conEQ3 = py.Constraint(rule=EQ3 )

    WFwd.var = py.Var ( domain=Reals, bounds=(0,None), initialize = 1 )
    Gr.WFwd =  WFwd.var
    WFwd.InitByData()
    WFwd.mu = Gr.mu0;

    E.var = py.Var ( E.A[0].NodS,domain=Reals, initialize = 1 )
    Gr.E =  E.var
    E.InitByData()
    E.mu = Gr.mu0;

    W.var = py.Var ( W.A[0].NodS,domain=Reals, bounds=(Wmin,Wmax), initialize = 1 )
    Gr.W =  W.var
    W.InitByData()
    W.mu = Gr.mu0;

    WD.var = py.Var ( WD.A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    Gr.WD =  WD.var
    WD.InitByData()
    WD.mu = Gr.mu0;

    WF.var = py.Var ( WF.A[0].NodS,domain=Reals, initialize = 1 )
    Gr.WF =  WF.var
    WF.InitByData()
    WF.mu = Gr.mu0;

    G.var = py.Var ( G.A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    Gr.G =  G.var
    G.InitByData()
    G.mu = Gr.mu0;
 								# W' = (WF - E * Emult) * Dt
    def EQ4 (Gr,i__n) :
        return (
          ((fW((i__n+n.step))-fW(i__n))/n.step) == (fWF(i__n) - fE(i__n) * Emult) * fDt(i__n)
        )
    Gr.conEQ4 = py.Constraint(n.FlNodSm,rule=EQ4 )
 								# W(0)=Wmax-1.0
    def EQ5 (Gr) :
        return (
          fW(0)==Wmax-1.0
        )
    Gr.conEQ5 = py.Constraint(rule=EQ5 )
 								# WD=(Wmax-W)/Wmax*100
    def EQ6 (Gr,i__n) :
        return (
          fWD(i__n)==(Wmax-fW(i__n))/Wmax*100
        )
    Gr.conEQ6 = py.Constraint(n.FlNodS,rule=EQ6 )
 								# WF=WFwd*WD
    def EQ7 (Gr,i__n) :
        return (
          fWF(i__n)==fWFwd()*fWD(i__n)
        )
    Gr.conEQ7 = py.Constraint(n.FlNodS,rule=EQ7 )
 								# E=G*VPD*0.010017
    def EQ8 (Gr,i__n) :
        return (
          fE(i__n)==fG(i__n)*fVPD(i__n)*0.010017
        )
    Gr.conEQ8 = py.Constraint(n.FlNodS,rule=EQ8 )
 								# G=Gq(Q)*Gwd(WD)
    def EQ9 (Gr,i__n) :
        return (
          fG(i__n)==fGq(fQ(i__n))*fGwd(fWD(i__n))
        )
    Gr.conEQ9 = py.Constraint(n.FlNodS,rule=EQ9 )

    P.var = py.Var ( P.A[0].NodS,domain=Reals, initialize = 1 )
    Gr.P =  P.var
    P.InitByData()
    P.mu = Gr.mu0;

    CO2I.var = py.Var ( CO2I.A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    Gr.CO2I =  CO2I.var
    CO2I.InitByData()
    CO2I.mu = Gr.mu0;

    CO2M.var = py.Var ( CO2M.A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    Gr.CO2M =  CO2M.var
    CO2M.InitByData()
    CO2M.mu = Gr.mu0;

    Pq.var = py.Var ( Pq.A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    Gr.Pq =  Pq.var
    Pq.InitByData()
    Pq.mu = Gr.mu0;
 								# Pq(0)=0
    def EQ10 (Gr) :
        return (
          fPq(0)==0
        )
    Gr.conEQ10 = py.Constraint(rule=EQ10 )
 								# Pq'>=0
    def EQ11 (Gr,q) :
        return (
          ((fPq((q+sQ.step))-fPq(q))/sQ.step)>=0
        )
    Gr.conEQ11 = py.Constraint(sQ.FlNodSm,rule=EQ11 )

    Pt.var = py.Var ( Pt.A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    Gr.Pt =  Pt.var
    Pt.InitByData()
    Pt.mu = Gr.mu0;
 								# Pt(20)=1
    def EQ12 (Gr) :
        return (
          fPt(20)==1
        )
    Gr.conEQ12 = py.Constraint(rule=EQ12 )
 								# Pt'>=0
    def EQ13 (Gr,te) :
        return (
          ((fPt((te+sT.step))-fPt(te))/sT.step)>=0
        )
    Gr.conEQ13 = py.Constraint(sT.FlNodSm,rule=EQ13 )

    Pm.var = py.Var ( range (8), initialize = 0 )
    Gr.Pm =  Pm.var
    Pm.mu = Gr.mu0;
    Pm.var[0].value = 1
 								# Pm(sCO2M)>=0
    def EQ14 (Gr,i__sCO2M) :
        return (
          fPm(i__sCO2M)>=0
        )
    Gr.conEQ14 = py.Constraint(sCO2M.FlNodS,rule=EQ14 )
 								# Pm(360)=1
    def EQ15 (Gr) :
        return (
          fPm(360)==1
        )
    Gr.conEQ15 = py.Constraint(rule=EQ15 )
 								# Pm'>=0
    def EQ16 (Gr,i__sCO2M) :
        return (
          (Pm.dF_dX(i__sCO2M))>=0
        )
    Gr.conEQ16 = py.Constraint(sCO2M.FlNodS,rule=EQ16 )

    Pbr.var = py.Var ( domain=Reals, bounds=(0,None), initialize = 1 )
    Gr.Pbr =  Pbr.var
    Pbr.InitByData()
    Pbr.mu = Gr.mu0;

    GMt.var = py.Var ( GMt.A[0].NodS,domain=Reals, bounds=(0.1,0.2), initialize = 1 )
    Gr.GMt =  GMt.var
    GMt.InitByData()
    GMt.mu = Gr.mu0;
 								# GMt(0)=GMt(24)
    def EQ17 (Gr) :
        return (
          fGMt(0)==fGMt(24)
        )
    Gr.conEQ17 = py.Constraint(rule=EQ17 )
 								# P=Pq(Q)*Pt(T)*Pm(CO2M)-Pbr
    def EQ18 (Gr,i__n) :
        return (
          fP(i__n)==fPq(fQ(i__n))*fPt(fT(i__n))*fPm(fCO2M(i__n))-fPbr()
        )
    Gr.conEQ18 = py.Constraint(n.FlNodS,rule=EQ18 )
 								# P=(360-CO2I)*(G*2.2596)
    def EQ19 (Gr,i__n) :
        return (
          fP(i__n)==(360-fCO2I(i__n))*(fG(i__n)*2.2596)
        )
    Gr.conEQ19 = py.Constraint(n.FlNodS,rule=EQ19 )
 								# P=(CO2I-CO2M)*(GMt(t)*2.2596)
    def EQ20 (Gr,i__n) :
        return (
          fP(i__n)==(fCO2I(i__n)-fCO2M(i__n))*(fGMt(ft(i__n))*2.2596)
        )
    Gr.conEQ20 = py.Constraint(n.FlNodS,rule=EQ20 )
    SvF.fun_with_mu.append(getFun('E'))
    SvF.fun_with_mu.append(getFun('P'))
 											# Gq.Complexity([Penal[0]])/4+Gwd.Complexity([Penal[1]])+E.MSDnan()+Pq.Complexity([Penal[2]])+Pt.Complexity([Penal[3]])+Pm.Complexity([Penal[4]])+GMt.ComplCyc0E([Penal[5]])+P.MSD()
    def obj_expression(Gr):  
        return (
             Gq.Complexity([Penal[0]])/4+Gwd.Complexity([Penal[1]])+E.MSDnan()+Pq.Complexity([Penal[2]])+Pt.Complexity([Penal[3]])+Pm.Complexity([Penal[4]])+GMt.ComplCyc0E([Penal[5]])+P.MSD()
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    Gq = Task.Funs[0]

    Gwd = Task.Funs[1]

    E = Task.Funs[3]

    t = Task.Funs[12]

    P = Task.Funs[13]

    Pq = Task.Funs[16]

    Pt = Task.Funs[17]

    Pm = Task.Funs[18]

    GMt = Task.Funs[20]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (Gq.Complexity([Penal[0]])/4)
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tGq.Complexity([Penal[0]])/4 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tGq.Complexity([Penal[0]])/4 ='+ stmp+'\n')
    tmp = (Gwd.Complexity([Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tGwd.Complexity([Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tGwd.Complexity([Penal[1]]) ='+ stmp+'\n')
    tmp = (E.MSDnan())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tE.MSDnan() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tE.MSDnan() ='+ stmp+'\n')
    tmp = (Pq.Complexity([Penal[2]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tPq.Complexity([Penal[2]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tPq.Complexity([Penal[2]]) ='+ stmp+'\n')
    tmp = (Pt.Complexity([Penal[3]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tPt.Complexity([Penal[3]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tPt.Complexity([Penal[3]]) ='+ stmp+'\n')
    tmp = (Pm.Complexity([Penal[4]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tPm.Complexity([Penal[4]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tPm.Complexity([Penal[4]]) ='+ stmp+'\n')
    tmp = (GMt.ComplCyc0E([Penal[5]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tGMt.ComplCyc0E([Penal[5]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tGMt.ComplCyc0E([Penal[5]]) ='+ stmp+'\n')
    tmp = (P.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tP.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tP.MSD() ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

SvF.lenPenalty = 6

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
Task.Draw ('')