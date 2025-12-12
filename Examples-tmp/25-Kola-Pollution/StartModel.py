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
SvF.mngF = 'Ni_Pollution_Kola_lakes_eng.docx'
NiCu='Ni'
SvF.DataPath='_DATA100-158/'
SvF.CVNumOfIter = -1
InitSols=0
ShoreErr=False
SvF.RunMode = 'L&P'
SvF.max_workers=10
SvF.maxJobs=3
latNik=69.413;lonNik=30.234
latZap=69.425;lonZap=30.822
StartYear=1946
EndYear=2030
StartZap=1956
ProgYear=2050
t = Set('t',StartYear,EndYear,1,'','t')
rmax=130
rStep=1
Fi = Set('Fi',-180,180,10,'','Fi')
r = Set('r',0,rmax,rStep,'','r')
r1 = Set('r1',2*rStep,rmax,rStep,'','r1')
r2 = Set('r2',50,rmax-1,rStep,'','r2')
Prognose = Set('Prognose',StartYear,ProgYear,1,'','Prognose')
AzimutInit(latZap,lonZap)
xyNik=LatLonToAzimut(latNik,lonNik)
def fiNik(X,Y):return degrees(np.arctan2(Y-xyNik[1],X-xyNik[0]))
def rNik(X,Y):return sqrt((Y-xyNik[1])**2+(X-xyNik[0])**2)
xyZap=LatLonToAzimut(latZap,lonZap)
def fiZap(X,Y):return degrees(np.arctan2(Y-xyZap[1],X-xyZap[0]))
def rZap(X,Y):return sqrt((Y-xyZap[1])**2+(X-xyZap[0])**2)
Table ( 'NikRosePol37(Fi).sol','curentTabl','Fi,RosePol AS Pfi' )
Pfi = CycleFun('Pfi',[Fi])
def fPfi(Fi) : return Pfi.F([Fi])
EmNik = Fun('EmNik',[t])
def fEmNik(t) : return EmNik.F([t])
PrNik = Fun('PrNik',[r])
def fPrNik(r) : return PrNik.F([r])
DepNik = Fun('DepNik',[r])
def fDepNik(r) : return DepNik.F([r])
EmZap = Fun('EmZap',[t])
def fEmZap(t) : return EmZap.F([t])
PrZap = Fun('PrZap',[r])
def fPrZap(r) : return PrZap.F([r])
DepZap = Fun('DepZap',[r])
def fDepZap(r) : return DepZap.F([r])
EMS2a = Table ( '2Source2030.xlsx','EMS2a','Year as t,NiNi as EmNikZap' )
EmNikZap = Fun('EmNikZap',[t])
def fEmNikZap(t) : return EmNikZap.F([t])
t1946_1955 = Set('t1946_1955',StartYear,StartZap-1,1,'','t1946_1955')
tMono = Set('tMono',1955,1976,1,'','tMono')
tMonoNik = Set('tMonoNik',1946,1976,1,'','tMonoNik')
t1955_2014 = Set('t1955_2014',1955,2014,1,'','t1955_2014')
t2010_2014 = Set('t2010_2014',2010,2014,1,'','t2010_2014')
t2016_2019 = Set('t2016_2019',2016,2019,1,'','t2016_2019')
t2022_2030 = Set('t2022_2030',2022,EndYear,1,'','t2022_2030')
t1946_2009 = Set('t1946_2009',StartYear,2009,1,'','t1946_2009')
SolubleNik = Fun('SolubleNik',[r])
def fSolubleNik(r) : return SolubleNik.F([r])
SolubleZap = Fun('SolubleZap',[r])
def fSolubleZap(r) : return SolubleZap.F([r])
def Depos_sol(x,y,_it):
  dep=0
  if _it<=EndYear:
    if rNik(x,y)<=rmax:dep+=fPfi(fiNik(x,y))*fPrNik(rNik(x,y))*fEmNik(_it)*fSolubleNik(rNik(x,y))
    if rZap(x,y)<=rmax:dep+=fPfi(fiZap(x,y))*fPrZap(rZap(x,y))*fEmZap(_it)*fSolubleZap(rZap(x,y))
  return dep*1000
def Depos_insol(x,y,_it):
  if _it>EndYear:return 0
  dep=0
  if rNik(x,y)<=rmax:dep+=fPfi(fiNik(x,y))*fPrNik(rNik(x,y))*fEmNik(_it)*(1-fSolubleNik(rNik(x,y)))
  if rZap(x,y)<=rmax:dep+=fPfi(fiZap(x,y))*fPrZap(rZap(x,y))*fEmZap(_it)*(1-fSolubleZap(rZap(x,y)))
  return dep*1000
CONS = Table ( 'POINT.xlsx','CONS','nP,X,Y,Catch,S as SQw,Catch as SQs,lake1,peat1' )
CONS.dat('SQw')[:]+=(CONS.dat('Catch')[:]-CONS.dat('SQw')[:])*(CONS.dat('lake1')[:]+CONS.dat('peat1')[:])/100
CONS.dat('SQs')[:]-=CONS.dat('SQw')[:]
nP = Set('nP',SvF.curentTabl.dat('nP')[:].min(),SvF.curentTabl.dat('nP')[:].max(),1,'','nP')
X = Fun('X',[nP], param=True)
def fX(nP) : return X.F([nP])
Y = Fun('Y',[nP], param=True)
def fY(nP) : return Y.F([nP])
Catch = Fun('Catch',[nP], param=True)
def fCatch(nP) : return Catch.F([nP])
SQw = Fun('SQw',[nP], param=True)
def fSQw(nP) : return SQw.F([nP])
SQs = Fun('SQs',[nP], param=True)
def fSQs(nP) : return SQs.F([nP])
precip=0.4
fonWater=1.0
fonSoilDW=10
fonSedi=20
depISout=0.2
intoIS=0.2
Snow = Tensor('Snow',[])
def fSnow() : return Snow.F([])
notSnow = Tensor('notSnow',[])
def fnotSnow() : return notSnow.F([])
depIS = Fun('depIS',[nP,t])
def fdepIS(nP,t) : return depIS.F([nP,t])
depS = Fun('depS',[nP,t])
def fdepS(nP,t) : return depS.F([nP,t])
hSoil = Tensor('hSoil',[])
def fhSoil() : return hSoil.F([])
S = Fun('S',[nP,t])
def fS(nP,t) : return S.F([nP,t])
leaching = Tensor('leaching',[])
def fleaching() : return leaching.F([])
B = Fun('B',[nP,t])
def fB(nP,t) : return B.F([nP,t])
botSedLeach = Tensor('botSedLeach',[])
def fbotSedLeach() : return botSedLeach.F([])
W = Fun('W',[nP,t])
def fW(nP,t) : return W.F([nP,t])
H = Tensor('H',[])
def fH() : return H.F([])
SvF.useNaN = True
TDep = Table ( 'EXP_DEPOS.xlsx','TDep','nP AS nPD,Year as tD,ROWNUM as nD,depNi as deposD,X as Xd,Y as Yd' )
nD = Set('nD',SvF.curentTabl.dat('nD')[:].min(),SvF.curentTabl.dat('nD')[:].max(),1,'','nD')
nPD = Fun('nPD',[nD], param=True)
def fnPD(nD) : return nPD.F([nD])
tD = Fun('tD',[nD], param=True)
def ftD(nD) : return tD.F([nD])
deposD = Fun('deposD',[nD])
def fdeposD(nD) : return deposD.F([nD])
TSoil = Table ( 'EXP_SOIL.xlsx','TSoil','nP AS nPS,Year as tS,ROWNUM as nS,soilNi as soilD,X as Xs,Y as Ys' )
for i in TSoil.sR:TSoil.dat('soilD')[i]=max(TSoil.dat('soilD')[i],fonSoilDW)
nS = Set('nS',SvF.curentTabl.dat('nS')[:].min(),SvF.curentTabl.dat('nS')[:].max(),1,'','nS')
nPS = Fun('nPS',[nS], param=True)
def fnPS(nS) : return nPS.F([nS])
tS = Fun('tS',[nS], param=True)
def ftS(nS) : return tS.F([nS])
soilD = Fun('soilD',[nS])
def fsoilD(nS) : return soilD.F([nS])
TWater = Table ( 'EXP_LAKE.xlsx','TWater','X as Xw,Y as Yw,Year AS tW,Avg-TNi AS waterD,ROWNUM as nW,nP AS nPW,nP,CONn' )
CVmakeSets ( CV_NumSets=7,CV_Unit='nPW' )
nW = Set('nW',SvF.curentTabl.dat('nW')[:].min(),SvF.curentTabl.dat('nW')[:].max(),1,'','nW')
nPW = Fun('nPW',[nW], param=True)
def fnPW(nW) : return nPW.F([nW])
tW = Fun('tW',[nW], param=True)
def ftW(nW) : return tW.F([nW])
waterD = Fun('waterD',[nW])
def fwaterD(nW) : return waterD.F([nW])
TBott = Table ( 'EXP_SEDIMNT.xlsx','TBott','nP AS nPB,Year as tB,ROWNUM as nB,Vsedim,delT,Ni_0_1 as botSedD,X as Xb,Y as Yb' )
nB = Set('nB',SvF.curentTabl.dat('nB')[:].min(),SvF.curentTabl.dat('nB')[:].max(),1,'','nB')
nPB = Fun('nPB',[nB], param=True)
def fnPB(nB) : return nPB.F([nB])
tB = Fun('tB',[nB], param=True)
def ftB(nB) : return tB.F([nB])
Vsedim = Fun('Vsedim',[nB], param=True)
def fVsedim(nB) : return Vsedim.F([nB])
delT = Fun('delT',[nB], param=True)
def fdelT(nB) : return delT.F([nB])
botSedD = Fun('botSedD',[nB])
def fbotSedD(nB) : return botSedD.F([nB])
sedimMult = Tensor('sedimMult',[])
def fsedimMult() : return sedimMult.F([])
def TimeStep(Xi,Yi,ti,Catchi,Si,s,w,b):
  SQsi=Catchi-Si
  depSo=Depos_sol(Xi,Yi,ti)
  depISo=Depos_insol(Xi,Yi,ti)
  Bo=b+depISo*(1+SQsi/Si*fSnow())*(1-depISout)-fbotSedLeach()*b+fonSedi*0.1
  So=s*(1-fleaching())+(depISo+depSo*intoIS)*fnotSnow()
  Wo=w+(depSo*(Si+SQsi*(fSnow()+fnotSnow()*(1-intoIS)))+fleaching()*s*SQsi+fbotSedLeach()*b*Si-Catchi*precip*(w-fonWater))/(Si*fH()+Catchi*precip)
  return depSo,depISo,Bo,So,Wo
def RunModel(start,end):
 if start==StartYear:
  S.grd[:,0]=fonSoilDW*fhSoil()*800
  W.grd[:,0]=fonWater
  B.grd[:,0]=0
 for bi in nP.NodS:
  bv=nP.Val[bi]
  for tv in range(start,end+1,1):
    ti=tv-StartYear
    depS.grd[bi,ti],depIS.grd[bi,ti],Bo,So,Wo=TimeStep(fX(bv),fY(bv),tv,fCatch(bv),fSQw(bv),fS(bv,tv),fW(bv,tv),fB(bv,tv))
    if tv<end:
      S.grd[bi,ti+1]=So
      W.grd[bi,ti+1]=Wo
      B.grd[bi,ti+1]=Bo
if(InitSols):
 Task.ReadSols()
 RunModel(StartYear,EndYear)
 for n in nD.NodS:
  nv=nD.Val[n]
  deposD.grd[n]=fdepIS(fnPD(nv),ftD(nv))+fdepS(fnPD(nv),ftD(nv))
 for n in nS.NodS:
  nv=nS.Val[n]
  soilD.grd[n]=fS(fnPS(nv),ftS(nv))/(800*fhSoil())
 for n in nB.NodS:
  nv=nB.Val[n]
  botSedD.grd[n]=(fB(fnPB(nv),ftB(nv))-fB(fnPB(nv),ftB(nv)-fdelT(nv)))/fdelT(nv)/(fVsedim(nv)*fsedimMult()*0.25)
 Task.SaveSols()
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    Pfi.var = py.Var ( Pfi.A[0].NodS,domain=Reals, bounds=(0.4,None) )
    Gr.Pfi =  Pfi.var
 								# Pfi.var[0] = Pfi.var[Pfi.A[0].Ub]
    def EQ0 (Gr) :
        return (
          Pfi.var[0] == Pfi.var[Pfi.A[0].Ub]
        )
    Gr.conEQ0 = py.Constraint(rule=EQ0 )
 								# \int(-180,180,Pfi(Fi)*d(Fi))==360
    def EQ1 (Gr) :
        return (
          sum ( (int(_iFi!=-180)+int(_iFi!=180))/2*Fi.step*fPfi(_iFi) for _iFi in myrange (-180,180,Fi.step) )==360
        )
    Gr.conEQ1 = py.Constraint(rule=EQ1 )

    EmNik.var = py.Var ( EmNik.A[0].NodS,domain=Reals, bounds=(0,None) )
    Gr.EmNik =  EmNik.var

    PrNik.var = py.Var ( PrNik.A[0].NodS,domain=Reals, bounds=(0,None) )
    Gr.PrNik =  PrNik.var
 								# PrNik(0)=PrNik(rStep)
    def EQ2 (Gr) :
        return (
          fPrNik(0)==fPrNik(rStep)
        )
    Gr.conEQ2 = py.Constraint(rule=EQ2 )
 								# PrNik(rmax)=0
    def EQ3 (Gr) :
        return (
          fPrNik(rmax)==0
        )
    Gr.conEQ3 = py.Constraint(rule=EQ3 )
 								# d/dr(PrNik(r))<=0
    def EQ4 (Gr,_ir) :
        return (
          ((fPrNik((_ir+r.step))-fPrNik(_ir))/r.step)<=0
        )
    Gr.conEQ4 = py.Constraint(r.FlNodSm,rule=EQ4 )

    DepNik.var = py.Var ( DepNik.A[0].NodS,domain=Reals, bounds=(0,None) )
    Gr.DepNik =  DepNik.var
 								# DepNik(rmax)=1
    def EQ5 (Gr) :
        return (
          fDepNik(rmax)==1
        )
    Gr.conEQ5 = py.Constraint(rule=EQ5 )
 								# d/dr1(PrNik(r1)*r1)<=-0.003*PrNik(r1)*r1
    def EQ6 (Gr,_ir1) :
        return (
          ((fPrNik((_ir1+r1.step))*(_ir1+r1.step)-fPrNik(_ir1)*_ir1)/r1.step)<=-0.003*fPrNik(_ir1)*_ir1
        )
    Gr.conEQ6 = py.Constraint(r1.FlNodSm,rule=EQ6 )
 								# d/dr2(PrNik(r2)*r2)>=-0.2*PrNik(r2)*r2
    def EQ7 (Gr,_ir2) :
        return (
          ((fPrNik((_ir2+r2.step))*(_ir2+r2.step)-fPrNik(_ir2)*_ir2)/r2.step)>=-0.2*fPrNik(_ir2)*_ir2
        )
    Gr.conEQ7 = py.Constraint(r2.FlNodSm,rule=EQ7 )
 								# DepNik(r)=\int(0,r,PrNik(r1)*r1*d(r1))*2*pi
    def EQ8 (Gr,_ir) :
        return (
          fDepNik(_ir)==sum ( (int(_ir1!=0)+int(_ir1!=_ir))/2*r1.step*fPrNik(_ir1)*_ir1 for _ir1 in myrange (0,_ir,r1.step) )*2*pi
        )
    Gr.conEQ8 = py.Constraint(r.FlNodS,rule=EQ8 )

    EmZap.var = py.Var ( EmZap.A[0].NodS,domain=Reals, bounds=(0,None) )
    Gr.EmZap =  EmZap.var

    PrZap.var = py.Var ( PrZap.A[0].NodS,domain=Reals, bounds=(0,None) )
    Gr.PrZap =  PrZap.var
 								# PrZap(0)=PrZap(rStep)
    def EQ9 (Gr) :
        return (
          fPrZap(0)==fPrZap(rStep)
        )
    Gr.conEQ9 = py.Constraint(rule=EQ9 )
 								# PrZap(rmax)=0
    def EQ10 (Gr) :
        return (
          fPrZap(rmax)==0
        )
    Gr.conEQ10 = py.Constraint(rule=EQ10 )
 								# d/dr(PrZap(r))<=0
    def EQ11 (Gr,_ir) :
        return (
          ((fPrZap((_ir+r.step))-fPrZap(_ir))/r.step)<=0
        )
    Gr.conEQ11 = py.Constraint(r.FlNodSm,rule=EQ11 )

    DepZap.var = py.Var ( DepZap.A[0].NodS,domain=Reals, bounds=(0,None) )
    Gr.DepZap =  DepZap.var
 								# DepZap(rmax)=1
    def EQ12 (Gr) :
        return (
          fDepZap(rmax)==1
        )
    Gr.conEQ12 = py.Constraint(rule=EQ12 )
 								# d/dr1(PrZap(r1)*r1)<=-0.003*PrZap(r1)*r1
    def EQ13 (Gr,_ir1) :
        return (
          ((fPrZap((_ir1+r1.step))*(_ir1+r1.step)-fPrZap(_ir1)*_ir1)/r1.step)<=-0.003*fPrZap(_ir1)*_ir1
        )
    Gr.conEQ13 = py.Constraint(r1.FlNodSm,rule=EQ13 )
 								# d/dr2(PrZap(r2)*r2)>=-0.2*PrZap(r2)*r2
    def EQ14 (Gr,_ir2) :
        return (
          ((fPrZap((_ir2+r2.step))*(_ir2+r2.step)-fPrZap(_ir2)*_ir2)/r2.step)>=-0.2*fPrZap(_ir2)*_ir2
        )
    Gr.conEQ14 = py.Constraint(r2.FlNodSm,rule=EQ14 )
 								# DepZap(r)=\int(0,r,PrZap(r1)*r1*d(r1))*2*pi
    def EQ15 (Gr,_ir) :
        return (
          fDepZap(_ir)==sum ( (int(_ir1!=0)+int(_ir1!=_ir))/2*r1.step*fPrZap(_ir1)*_ir1 for _ir1 in myrange (0,_ir,r1.step) )*2*pi
        )
    Gr.conEQ15 = py.Constraint(r.FlNodS,rule=EQ15 )

    EmNikZap.var = py.Var ( EmNikZap.A[0].NodS,domain=Reals, bounds=(0,700) )
    Gr.EmNikZap =  EmNikZap.var
 								# EmNikZap(t)=EmNik(t)+EmZap(t)
    def EQ16 (Gr,_it) :
        return (
          fEmNikZap(_it)==fEmNik(_it)+fEmZap(_it)
        )
    Gr.conEQ16 = py.Constraint(t.FlNodS,rule=EQ16 )
 								# EmZap(t1946_1955)=0
    def EQ17 (Gr,_it1946_1955) :
        return (
          fEmZap(_it1946_1955)==0
        )
    Gr.conEQ17 = py.Constraint(t1946_1955.FlNodS,rule=EQ17 )
 								# d/dtMono(EmZap(tMono))>1
    def EQ18 (Gr,_itMono) :
        return (
          ((fEmZap((_itMono+tMono.step))-fEmZap(_itMono))/tMono.step)>=1
        )
    Gr.conEQ18 = py.Constraint(tMono.FlNodSm,rule=EQ18 )
 								# EmNik(StartYear)<=10
    def EQ19 (Gr) :
        return (
          fEmNik(StartYear)<=10
        )
    Gr.conEQ19 = py.Constraint(rule=EQ19 )
 								# d/dtMonoNik(EmNik(tMonoNik))>1
    def EQ20 (Gr,_itMonoNik) :
        return (
          ((fEmNik((_itMonoNik+tMonoNik.step))-fEmNik(_itMonoNik))/tMonoNik.step)>=1
        )
    Gr.conEQ20 = py.Constraint(tMonoNik.FlNodSm,rule=EQ20 )
 								# EmNikZap(t2022_2030)<=20.
    def EQ21 (Gr,_it2022_2030) :
        return (
          fEmNikZap(_it2022_2030)<=20.
        )
    Gr.conEQ21 = py.Constraint(t2022_2030.FlNodS,rule=EQ21 )
 								# EmZap(t1955_2014)<=EmNik(t1955_2014)*1.2
    def EQ22 (Gr,_it1955_2014) :
        return (
          fEmZap(_it1955_2014)<=fEmNik(_it1955_2014)*1.2
        )
    Gr.conEQ22 = py.Constraint(t1955_2014.FlNodS,rule=EQ22 )
 								# d/dt2022_2030(EmNikZap(t2022_2030))<0
    def EQ23 (Gr,_it2022_2030) :
        return (
          ((fEmNikZap((_it2022_2030+t2022_2030.step))-fEmNikZap(_it2022_2030))/t2022_2030.step)<=0
        )
    Gr.conEQ23 = py.Constraint(t2022_2030.FlNodSm,rule=EQ23 )

    SolubleNik.var = py.Var ( SolubleNik.A[0].NodS,domain=Reals, bounds=(0.05,.5) )
    Gr.SolubleNik =  SolubleNik.var
 								# d/dr(SolubleNik)>0
    def EQ24 (Gr,_ir) :
        return (
          ((fSolubleNik((_ir+r.step))-fSolubleNik(_ir))/r.step)>=0
        )
    Gr.conEQ24 = py.Constraint(r.FlNodSm,rule=EQ24 )

    SolubleZap.var = py.Var ( SolubleZap.A[0].NodS,domain=Reals, bounds=(0.05,.5) )
    Gr.SolubleZap =  SolubleZap.var
 								# d/dr(SolubleZap)>0
    def EQ25 (Gr,_ir) :
        return (
          ((fSolubleZap((_ir+r.step))-fSolubleZap(_ir))/r.step)>=0
        )
    Gr.conEQ25 = py.Constraint(r.FlNodSm,rule=EQ25 )

    Snow.var = py.Var ( domain=Reals, bounds=(0.1,0.5) )
    Gr.Snow =  Snow.var

    notSnow.var = py.Var ( domain=Reals )
    Gr.notSnow =  notSnow.var
 								# notSnow=1-Snow
    def EQ26 (Gr) :
        return (
          fnotSnow()==1-fSnow()
        )
    Gr.conEQ26 = py.Constraint(rule=EQ26 )

    depIS.var = py.Var ( depIS.A[0].NodS,depIS.A[1].NodS,domain=Reals )
    Gr.depIS =  depIS.var
 								# depIS=Depos_insol(X(nP),Y(nP),t)
    def EQ27 (Gr,_it,_inP) :
        return (
          fdepIS(_inP,_it)==Depos_insol(fX(_inP),fY(_inP),_it)
        )
    Gr.conEQ27 = py.Constraint(t.FlNodS,nP.FlNodS,rule=EQ27 )

    depS.var = py.Var ( depS.A[0].NodS,depS.A[1].NodS,domain=Reals )
    Gr.depS =  depS.var
 								# depS=Depos_sol(X,Y,t)
    def EQ28 (Gr,_it,_inP) :
        return (
          fdepS(_inP,_it)==Depos_sol(fX(_inP),fY(_inP),_it)
        )
    Gr.conEQ28 = py.Constraint(t.FlNodS,nP.FlNodS,rule=EQ28 )

    hSoil.var = py.Var ( domain=Reals, bounds=(0.005,None) )
    Gr.hSoil =  hSoil.var

    S.var = py.Var ( S.A[0].NodS,S.A[1].NodS,domain=Reals, bounds=(7.5,None) )
    Gr.S =  S.var

    leaching.var = py.Var ( domain=Reals, bounds=(0.0015,None) )
    Gr.leaching =  leaching.var
 								# S(nP,StartYear)=fonSoilDW*hSoil*800
    def EQ29 (Gr,_inP) :
        return (
          fS(_inP,StartYear)==fonSoilDW*fhSoil()*800
        )
    Gr.conEQ29 = py.Constraint(nP.FlNodS,rule=EQ29 )
 								# d/dt(S)=(depIS(nP,t)+depS(nP,t)*intoIS)*notSnow-leaching*S
    def EQ30 (Gr,_it,_inP) :
        return (
          ((fS(_inP,(_it+t.step))-fS(_inP,_it))/t.step)==(fdepIS(_inP,_it)+fdepS(_inP,_it)*intoIS)*fnotSnow()-fleaching()*fS(_inP,_it)
        )
    Gr.conEQ30 = py.Constraint(t.FlNodSm,nP.FlNodS,rule=EQ30 )

    B.var = py.Var ( B.A[0].NodS,B.A[1].NodS,domain=Reals, bounds=(0,None) )
    Gr.B =  B.var

    botSedLeach.var = py.Var ( domain=Reals, bounds=(0.00,None) )
    Gr.botSedLeach =  botSedLeach.var
 								# botSedLeach=leaching
    def EQ31 (Gr) :
        return (
          fbotSedLeach()==fleaching()
        )
    Gr.conEQ31 = py.Constraint(rule=EQ31 )
 								# B(nP,StartYear)=0
    def EQ32 (Gr,_inP) :
        return (
          fB(_inP,StartYear)==0
        )
    Gr.conEQ32 = py.Constraint(nP.FlNodS,rule=EQ32 )
 								# d/dt(B)=depIS(nP,t)*(1+SQs(nP)/SQw(nP)*Snow)*(1-depISout)-botSedLeach*B+fonSedi*0.1
    def EQ33 (Gr,_it,_inP) :
        return (
          ((fB(_inP,(_it+t.step))-fB(_inP,_it))/t.step)==fdepIS(_inP,_it)*(1+fSQs(_inP)/fSQw(_inP)*fSnow())*(1-depISout)-fbotSedLeach()*fB(_inP,_it)+fonSedi*0.1
        )
    Gr.conEQ33 = py.Constraint(t.FlNodSm,nP.FlNodS,rule=EQ33 )

    W.var = py.Var ( W.A[0].NodS,W.A[1].NodS,domain=Reals, bounds=(0,None) )
    Gr.W =  W.var

    H.var = py.Var ( domain=Reals, bounds=(0,2) )
    Gr.H =  H.var
 								# W(nP,StartYear)=fonWater
    def EQ34 (Gr,_inP) :
        return (
          fW(_inP,StartYear)==fonWater
        )
    Gr.conEQ34 = py.Constraint(nP.FlNodS,rule=EQ34 )
 								# d/dt(W)=(depS(nP,t)*(SQw(nP)+SQs(nP)*(Snow+notSnow*(1-intoIS)))+leaching*S*SQs(nP)+botSedLeach*B*SQw(nP)-Catch(nP)*precip*(W-fonWater))/(SQw(nP)*H+Catch(nP)*precip)
    def EQ35 (Gr,_it,_inP) :
        return (
          ((fW(_inP,(_it+t.step))-fW(_inP,_it))/t.step)==(fdepS(_inP,_it)*(fSQw(_inP)+fSQs(_inP)*(fSnow()+fnotSnow()*(1-intoIS)))+fleaching()*fS(_inP,_it)*fSQs(_inP)+fbotSedLeach()*fB(_inP,_it)*fSQw(_inP)-fCatch(_inP)*precip*(fW(_inP,_it)-fonWater))/(fSQw(_inP)*fH()+fCatch(_inP)*precip)
        )
    Gr.conEQ35 = py.Constraint(t.FlNodSm,nP.FlNodS,rule=EQ35 )

    deposD.var = py.Var ( deposD.A[0].NodS,domain=Reals, bounds=(0,None) )
    Gr.deposD =  deposD.var
 								# deposD(nD)=depIS(nPD(nD),tD(nD))+depS(nPD(nD),tD(nD))
    def EQ36 (Gr,_inD) :
        return (
          fdeposD(_inD)==fdepIS(fnPD(_inD),ftD(_inD))+fdepS(fnPD(_inD),ftD(_inD))
        )
    Gr.conEQ36 = py.Constraint(nD.FlNodS,rule=EQ36 )

    soilD.var = py.Var ( soilD.A[0].NodS,domain=Reals, bounds=(0,None) )
    Gr.soilD =  soilD.var
 								# soilD*800*hSoil=S(nPS,tS)
    def EQ37 (Gr,_inS) :
        return (
          fsoilD(_inS)*800*fhSoil()==fS(fnPS(_inS),ftS(_inS))
        )
    Gr.conEQ37 = py.Constraint(nS.FlNodS,rule=EQ37 )

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )

    waterD.var = py.Var ( waterD.A[0].NodS,domain=Reals, bounds=(0,None) )
    Gr.waterD =  waterD.var
    waterD.mu = Gr.mu0;
 								# waterD=W(nPW,tW)
    def EQ38 (Gr,_inW) :
        return (
          fwaterD(_inW)==fW(fnPW(_inW),ftW(_inW))
        )
    Gr.conEQ38 = py.Constraint(nW.FlNodS,rule=EQ38 )

    botSedD.var = py.Var ( botSedD.A[0].NodS,domain=Reals, bounds=(0,None) )
    Gr.botSedD =  botSedD.var
    botSedD.mu = Gr.mu0;

    sedimMult.var = py.Var ( domain=Reals, bounds=(0,None) )
    Gr.sedimMult =  sedimMult.var
    sedimMult.mu = Gr.mu0;
 								# botSedD(nB)*Vsedim(nB)*sedimMult*0.25=(B(nPB,tB(nB))-B(nPB,tB(nB)-delT(nB)))/delT(nB)
    def EQ39 (Gr,_inB) :
        return (
          fbotSedD(_inB)*fVsedim(_inB)*fsedimMult()*0.25==(fB(fnPB(_inB),ftB(_inB))-fB(fnPB(_inB),ftB(_inB)-fdelT(_inB)))/fdelT(_inB)
        )
    Gr.conEQ39 = py.Constraint(nB.FlNodS,rule=EQ39 )
    SvF.fun_with_mu.append(getFun('waterD'))
    if waterD.mu is None : waterD.mu = Gr.mu0
    waterD.ValidationSets = SvF.ValidationSets
    waterD.notTrainingSets = SvF.notTrainingSets
    waterD.TrainingSets = SvF.TrainingSets
    deposD.mu = None
    EmNikZap.mu = None
    soilD.mu = None
    Pfi.mu = None
    botSedD.mu = None
 											# waterD.MSDrel(2.0)+0.0002*deposD.MSD_no_mu()+Penal[4]*EmNikZap.MSD_no_mu()+Penal[5]*soilD.MSDrel_no_mu(30.0)+Penal[7]*Pfi.MSD_no_mu()+Penal[6]*botSedD.MSDrel_no_mu(40)+Pfi.ComplCyc0E([Penal[0]])+DepNik.Compl([Penal[1]])+EmNik.ComplMean2([Penal[2]])+DepZap.Compl([Penal[1]])+EmZap.ComplMean2([Penal[2]])+SolubleNik.ComplMean2([Penal[3]])+SolubleZap.ComplMean2([Penal[3]])
    def obj_expression(Gr):  
        return (
             waterD.MSDrel(2.0)+0.0002*deposD.MSD_no_mu()+Penal[4]*EmNikZap.MSD_no_mu()+Penal[5]*soilD.MSDrel_no_mu(30.0)+Penal[7]*Pfi.MSD_no_mu()+Penal[6]*botSedD.MSDrel_no_mu(40)+Pfi.ComplCyc0E([Penal[0]])+DepNik.Compl([Penal[1]])+EmNik.ComplMean2([Penal[2]])+DepZap.Compl([Penal[1]])+EmZap.ComplMean2([Penal[2]])+SolubleNik.ComplMean2([Penal[3]])+SolubleZap.ComplMean2([Penal[3]])
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    Pfi = Task.Funs[0]

    EmNik = Task.Funs[1]

    DepNik = Task.Funs[3]

    EmZap = Task.Funs[4]

    DepZap = Task.Funs[6]

    EmNikZap = Task.Funs[7]

    SolubleNik = Task.Funs[8]

    SolubleZap = Task.Funs[9]

    deposD = Task.Funs[28]

    soilD = Task.Funs[31]

    waterD = Task.Funs[34]

    botSedD = Task.Funs[39]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (waterD.MSDrel(2.0))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\twaterD.MSDrel(2.0) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\twaterD.MSDrel(2.0) ='+ stmp+'\n')
    tmp = (0.0002*deposD.MSD_no_mu())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\t0.0002*deposD.MSD_no_mu() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\t0.0002*deposD.MSD_no_mu() ='+ stmp+'\n')
    tmp = (Penal[4]*EmNikZap.MSD_no_mu())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tPenal[4]*EmNikZap.MSD_no_mu() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tPenal[4]*EmNikZap.MSD_no_mu() ='+ stmp+'\n')
    tmp = (Penal[5]*soilD.MSDrel_no_mu(30.0))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tPenal[5]*soilD.MSDrel_no_mu(30.0) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tPenal[5]*soilD.MSDrel_no_mu(30.0) ='+ stmp+'\n')
    tmp = (Penal[7]*Pfi.MSD_no_mu())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tPenal[7]*Pfi.MSD_no_mu() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tPenal[7]*Pfi.MSD_no_mu() ='+ stmp+'\n')
    tmp = (Penal[6]*botSedD.MSDrel_no_mu(40))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tPenal[6]*botSedD.MSDrel_no_mu(40) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tPenal[6]*botSedD.MSDrel_no_mu(40) ='+ stmp+'\n')
    tmp = (Pfi.ComplCyc0E([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tPfi.ComplCyc0E([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tPfi.ComplCyc0E([Penal[0]]) ='+ stmp+'\n')
    tmp = (DepNik.Compl([Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tDepNik.Compl([Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tDepNik.Compl([Penal[1]]) ='+ stmp+'\n')
    tmp = (EmNik.ComplMean2([Penal[2]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tEmNik.ComplMean2([Penal[2]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tEmNik.ComplMean2([Penal[2]]) ='+ stmp+'\n')
    tmp = (DepZap.Compl([Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tDepZap.Compl([Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tDepZap.Compl([Penal[1]]) ='+ stmp+'\n')
    tmp = (EmZap.ComplMean2([Penal[2]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tEmZap.ComplMean2([Penal[2]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tEmZap.ComplMean2([Penal[2]]) ='+ stmp+'\n')
    tmp = (SolubleNik.ComplMean2([Penal[3]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tSolubleNik.ComplMean2([Penal[3]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tSolubleNik.ComplMean2([Penal[3]]) ='+ stmp+'\n')
    tmp = (SolubleZap.ComplMean2([Penal[3]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tSolubleZap.ComplMean2([Penal[3]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tSolubleZap.ComplMean2([Penal[3]]) ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
Lang='Eng'
print(fH(),fhSoil(),fSnow(),fsedimMult(),fleaching(),fbotSedLeach())
S.Resize ( [nP,Prognose] )
W.Resize ( [nP,Prognose] )
B.Resize ( [nP,Prognose] )
depIS.Resize ( [nP,Prognose] )
depS.Resize ( [nP,Prognose] )
RunModel(EndYear,ProgYear)
if(ShoreErr):
 TWater.AddField('Err')
 TWater.AddField('Err_rel')
 TWater.AddField('CVerr')
 for n in TWater.sR:
  TWater.dat('Err')[n]=waterD.delta(n)
  TWater.dat('Err_rel')[n]=waterD.delta_rel(n)
  if not waterD.CVerr is None:TWater.dat('CVerr')[n]=waterD.CVerr[n]
 TWater.WriteSvFtbl('a.txt')
 if not waterD.CVerr is None:
  CVerr=Polyline(TWater.dat('nP')[:],TWater.dat('CVerr')[:],None,'CVerr')
  CVerr=Polyline(TWater.dat('nW')[:],TWater.dat('CVerr')[:],None,'CVerr')
 Errs_rel=Polyline(TWater.dat('nP')[:],TWater.dat('Err_rel')[:],None,'Errs_rel')
 Task.Draw ( 'Errs_rel' )
 Errs=Polyline(TWater.dat('nP')[:],TWater.dat('Err')[:],None,'Errs')
 Task.Draw ( 'Errs' )
 Errs_rel=Polyline(TWater.dat('CONn')[:],TWater.dat('Err_rel')[:],None,'Errs_rel')
 Task.Draw ( 'Errs_rel' )
 Errs=Polyline(TWater.dat('CONn')[:],TWater.dat('Err')[:],None,'Errs')
 Task.Draw ( 'Errs' )
Task.Draw ( 'Pfi' )
if(0):
    Task.Draw ( 'Pfi' )
    Task.Draw ( 'EmNikZap EmNik;LC:c EmZap;LC:b' )
    Task.Draw ( 'DepNik DepZap;LC:b' )
    Task.Draw ( 'PrNik PrZap;LC:b' )
    Task.Draw ( 'soilD' )
    Task.Draw ( 'botSedD' )
    Task.Draw ( 'waterD' )
    Task.Draw ( 'deposD' )
SvF.Xsize=9;SvF.Ysize=3.6
def DrLake(inP):
 x=[]
 d=[]
 y=[]
 for n in nW.NodS:
  if nPW.grd[n]==inP:
   d.append(waterD.V.dat[n])
   y.append(tW.grd[n])
   x1=W.grd[int(inP)-1,:]
   y1=Prognose.Val
 name='P'+str(int(inP))
 Polyline(y1,x1,'None',name)
 Polyline(y,d,'None',name+'D')
if(0):
 nold=-1
 for n in nW.NodS:
  if nold!=nPW.grd[n]:
    nold=nPW.grd[n]
    DrLake(nold)
 name58='P47'
 name52='P52'
 name60='P60'
 name64='P64'
 print('************************************ ')
 Task.Draw(name58+' '+name58+'D;MS:3;LW:0 '+name52+';LW:1;MS:0;LC:b '+name52+'D;MS:3;LW:0;MC:b '+name60+';LW:1;MS:0;LC:g '+name60+'D;MS:3;LW:0;MC:g '+name64+';LW:1;MS:0;LC:black '+name64+'D;MS:3;LW:0;MC:black')
 print('TND************************************ ')
SvF.Xsize=5
def where_condition ( Year, botSedD, CONn, nP ):
    return (CONn==161)
TBott1 = Table ( 'EXP_SEDIMNT.xlsx','TBott1','Year,Ni_0_1 as botSedD,CONn,nP',where_condition )
Year = Set('Year',SvF.curentTabl.dat('Year')[:].min(),SvF.curentTabl.dat('Year')[:].max(),-50,'','Year')
botSedD = Fun('botSedD',[Year], param=True)
def fbotSedD(Year) : return botSedD.F([Year])
if(1):
 for tt in botSedD.A[0].NodS:
  botSedD.grd[tt]=(fB(TBott1.dat('nP')[0],botSedD.A[0].Val[tt])-fB(TBott1.dat('nP')[0],botSedD.A[0].Val[tt]-1))*15
SvF.Xsize=9;SvF.Ysize=3.6;SvF.Ylabel_x=0.13;SvF.Xlabel_x=0.95
EmNikZap.V.oname =NiCu+' - Nik+Zap';
EmNik.V.oname =NiCu+' - Nik'; EmZap.V.oname =NiCu+' - Zap';
if Lang == 'Rus' :
    EmZap.V.draw_name= 'Выбросы '+NiCu+', т/год'; EmZap.A[0].oname= 'Годы'; EmNikZap.V.data_name =NiCu+' - данные';
else :
    EmZap.V.draw_name= 'Emission '+NiCu+', tons/year'; EmZap.A[0].oname= 'Years'; EmNikZap.V.data_name =NiCu+' - data';
Task.Draw ( 'EmNikZap;LW:1.5;MS:0;DC:r EmNik;LC:g;LW:0.5 EmZap;LC:b' )
SvF.Xsize=5;SvF.Ylabel_x=0.27;SvF.Xlabel_x=0.99
if Lang=='Rus':
  PrZap.V.draw_name='Выпадения '+NiCu+', mg/m2/year'
else:
  PrZap.V.draw_name='Depositions '+NiCu+', mg/m2/year'
Task.Draw ( 'PrNik;LC:g PrZap;LC:b' )
SvF.Ylabel_x=0.21;SvF.Xlabel_x=0.99
DepNik.grd[:]*=100
DepZap.grd[:]*=100
if Lang=='Rus':
  DepZap.V.draw_name='% Выпадения '+NiCu+', %'
else:
  DepZap.V.draw_name='% Depositions '+NiCu+', %'
Task.Draw ( 'DepNik;LC:g DepZap;LC:b' )
DepNik.grd[:]/=100
DepZap.grd[:]/=100
SvF.Ylabel_x=0.27
SolubleNik.grd[:]*=100
SolubleZap.grd[:]*=100
if Lang=='Rus':
  SolubleZap.V.draw_name='% растворимого '+NiCu+', %'
else:
  SolubleZap.V.draw_name='% soluble '+NiCu+', %'
Task.Draw ( 'SolubleNik;LC:g SolubleZap;LC:b' )
SolubleNik.grd[:]/=100
SolubleZap.grd[:]/=100
S_DEPOSITION = Fun('S_DEPOSITION',[Prognose], param=True)
def fS_DEPOSITION(Prognose) : return S_DEPOSITION.F([Prognose])
A_DEPOSITION = Fun('A_DEPOSITION',[Prognose], param=True)
def fA_DEPOSITION(Prognose) : return A_DEPOSITION.F([Prognose])
S_SOIL = Fun('S_SOIL',[Prognose], param=True)
def fS_SOIL(Prognose) : return S_SOIL.F([Prognose])
A_SOIL = Fun('A_SOIL',[Prognose], param=True)
def fA_SOIL(Prognose) : return A_SOIL.F([Prognose])
M_SOIL = Fun('M_SOIL',[Prognose], param=True)
def fM_SOIL(Prognose) : return M_SOIL.F([Prognose])
S_SEDIMENTION = Fun('S_SEDIMENTION',[Prognose], param=True)
def fS_SEDIMENTION(Prognose) : return S_SEDIMENTION.F([Prognose])
A_SEDIMENTION = Fun('A_SEDIMENTION',[Prognose], param=True)
def fA_SEDIMENTION(Prognose) : return A_SEDIMENTION.F([Prognose])
M_SEDIMENTION = Fun('M_SEDIMENTION',[Prognose], param=True)
def fM_SEDIMENTION(Prognose) : return M_SEDIMENTION.F([Prognose])
S_WATER = Fun('S_WATER',[Prognose], param=True)
def fS_WATER(Prognose) : return S_WATER.F([Prognose])
A_WATER = Fun('A_WATER',[Prognose], param=True)
def fA_WATER(Prognose) : return A_WATER.F([Prognose])
M_WATER = Fun('M_WATER',[Prognose], param=True)
def fM_WATER(Prognose) : return M_WATER.F([Prognose])
M_WATERdep = Fun('M_WATERdep',[Prognose], param=True)
def fM_WATERdep(Prognose) : return M_WATERdep.F([Prognose])
M_WATERlea = Fun('M_WATERlea',[Prognose], param=True)
def fM_WATERlea(Prognose) : return M_WATERlea.F([Prognose])
S_OUT = Fun('S_OUT',[Prognose], param=True)
def fS_OUT(Prognose) : return S_OUT.F([Prognose])
A_OUT = Fun('A_OUT',[Prognose], param=True)
def fA_OUT(Prognose) : return A_OUT.F([Prognose])
Mode='NUM'
if(1):
 for ti in Prognose.NodS:
   S_Catch=0
   S_Lakes=0
   NoLakes=0
   S_DEPOSITION.grd[ti]=0
   S_OUT.grd[ti]=0
   S_SOIL.grd[ti]=0
   S_SEDIMENTION.grd[ti]=0
   S_WATER.grd[ti]=0
   A_SOIL.grd[ti]=0
   A_SEDIMENTION.grd[ti]=0
   M_SEDIMENTION.grd[ti]=0
   A_WATER.grd[ti]=0
   M_SOIL.grd[ti]=fonSoilDW*fhSoil()*800
   M_WATER.grd[ti]=fonWater
   M_WATERdep.grd[ti]=0
   M_WATERlea.grd[ti]=fonWater
   for bi in nP.NodS:
    if bi in nPW.grd:
     S_Catch+=Catch.grd[bi]
     S_Lakes+=SQw.grd[bi]
     NoLakes+=1
     Si=SQw.grd[bi]
     SQsi=SQs.grd[bi]
     Catchi=Catch.grd[bi]
     S_DEPOSITION.grd[ti]+=depS.grd[bi,ti]+depIS.grd[bi,ti]
     S_OUT.grd[ti]+=W.grd[bi,ti]*precip+depIS.grd[bi,ti]*(SQw.grd[bi]+SQs.grd[bi]*fSnow())/Catch.grd[bi]*depISout
     S_SOIL.grd[ti]+=(depIS.grd[bi,ti]+depS.grd[bi,ti]*intoIS)*fnotSnow()*SQs.grd[bi]/Catch.grd[bi]
     A_SOIL.grd[ti]+=S.grd[bi,ti]*SQs.grd[bi]/Catch.grd[bi]
     M_SOIL.grd[ti]+=S.grd[bi,ti]/(800*fhSoil())
     S_WATER.grd[ti]+=depS.grd[bi,ti]*(Si+SQsi*(fSnow()+fnotSnow()*(1-intoIS)))/Catchi
     A_WATER.grd[ti]+=W.grd[bi,ti]*fH()*Si/Catch.grd[bi]
     M_WATER.grd[ti]+=W.grd[bi,ti]
     M_WATERdep.grd[ti]+=W.grd[bi,ti]*depS.grd[bi,ti]*(Si+SQsi*(fSnow()+fnotSnow()*(1-intoIS)))/(depS.grd[bi,ti]*(Si+SQsi*(fSnow()+fnotSnow()*(1-intoIS)))+fleaching()*S.grd[bi,ti]*SQsi+fbotSedLeach()*B.grd[bi,ti]*Si)
     M_WATERlea.grd[ti]=M_WATER.grd[ti]-M_WATERdep.grd[ti]
     S_SEDIMENTION.grd[ti]+=depIS.grd[bi,ti]*(Si+SQs.grd[bi]*fSnow())/Catch.grd[bi]
     A_SEDIMENTION.grd[ti]+=B.grd[bi,ti]*Si/Catch.grd[bi]
     M_SEDIMENTION.grd[ti]+=B.grd[bi,ti]
   S_DEPOSITION.grd[ti]/=NoLakes
   S_OUT.grd[ti]/=NoLakes
   S_SOIL.grd[ti]/=NoLakes
   A_SOIL.grd[ti]/=NoLakes
   M_SOIL.grd[ti]/=NoLakes
   S_SEDIMENTION.grd[ti]/=NoLakes
   A_SEDIMENTION.grd[ti]/=NoLakes
   M_SEDIMENTION.grd[ti]/=NoLakes
   S_WATER.grd[ti]/=NoLakes
   A_WATER.grd[ti]/=NoLakes
   M_WATER.grd[ti]/=NoLakes
   M_WATERdep.grd[ti]/=NoLakes
   M_WATERlea.grd[ti]/=NoLakes
print('*********S_Catch=',S_Catch,'S_Lakes=',S_Lakes,'NoLakes',NoLakes,'Mean_Catch=',S_Catch/NoLakes,'Mean_Lake=',S_Lakes/NoLakes)
if Mode=='SQUARE':
  S_DEPOSITION.grd[:]/=S_Catch
  S_SOIL.grd[:]/=S_Catch
  S_WATER.grd[:]/=S_Catch
  S_OUT.grd[:]/=S_Catch
  S_SEDIMENTION.grd[:]/=S_Catch
  M_WATER.grd[:]/=S_Lakes
  A_WATER.grd[:]/=S_Lakes
  M_SOIL.grd[:]/=(S_Catch-S_Lakes)
  A_SOIL.grd[:]/=(S_Catch-S_Lakes)
A_DEPOSITION.grd[0]=S_DEPOSITION.grd[0]
A_OUT.grd[0]=S_OUT.grd[0]
for ti in Prognose.mNodS:
  A_DEPOSITION.grd[ti]=A_DEPOSITION.grd[ti-1]+S_DEPOSITION.grd[ti]
  A_OUT.grd[ti]=A_OUT.grd[ti-1]+S_OUT.grd[ti]
A_SOIL.grd[:]-=A_SOIL.grd[0]
SvF.Xsize=9;SvF.Ysize=3.6;SvF.Ylabel_x=0.35;SvF.Xlabel_x=0.95
if Lang=='Rus':
 S_WATER.V.oname='вода';S_DEPOSITION.V.oname='всего';S_SOIL.V.oname='почва';S_SEDIMENTION.V.oname='донные отложения'
 S_WATER.V.draw_name='Распределение выпадения '+NiCu+', мг/м2/год';S_SOIL.A[0].oname='Годы'
else:
 S_WATER.V.oname='water';S_DEPOSITION.V.oname='total';S_SOIL.V.oname='soil';S_SEDIMENTION.V.oname='botton sediments'
 S_WATER.V.draw_name='Distribution of '+NiCu+' depositions, mg/m2/year';S_WATER.A[0].oname='Years'
Task.Draw ( 'S_DEPOSITION;MS:0;LW:1.5 S_SEDIMENTION;LC:black;LSt:dotted S_SOIL;LC:brown;LSt:dashed S_WATER;LC:b;LSt:dashdot' )
SvF.Ylabel_x=0.2
if Lang=='Rus':
 A_WATER.V.oname='вода';A_DEPOSITION.V.oname='всего';A_SOIL.V.oname='почва';A_SEDIMENTION.V.oname='донные отложения'
 A_OUT.V.oname='потери со стоком';A_WATER.V.draw_name='Баланс накопления '+NiCu+', мг/м2';A_WATER.A[0].oname='Годы'
else:
 A_WATER.V.oname='water';A_DEPOSITION.V.oname='total';A_SOIL.V.oname='soil';A_SEDIMENTION.V.oname='botton sediments'
 A_OUT.V.oname='loss with runoff';A_WATER.V.draw_name='Balance of '+NiCu+' accumulation, mg/m2';A_WATER.A[0].oname='Years'
Task.Draw ( 'A_DEPOSITION;MS:0;LW:1.5 A_SEDIMENTION;LC:black;LSt:dotted A_SOIL;LC:brown;LSt:dashed;MS:0;LW:1.5 A_OUT;LC:green;LSt:solid;MS:3;LW:1 A_WATER;LC:b;LSt:dashdot' )
SvF.Ylabel_x=0.25
if Lang=='Rus':
 M_WATER.V.draw_name='Концентрация '+NiCu+' в воде, мг/м3';M_WATER.A[0].oname='Годы'
 M_WATER.V.oname='вода';M_WATERdep.V.oname='выпадения';M_WATERlea.V.oname='выщелочивание'
else:
 M_WATER.V.draw_name=NiCu+' Concentration in water, mg/m3';M_WATER.A[0].oname='Years'
 M_WATER.V.oname='water';M_WATERdep.V.oname='depositions';M_WATERlea.V.oname='leaching'
Task.Draw ( 'M_WATERdep M_WATERlea;LC:g M_WATER;LC:b;LSt:dashdot;LW:1.5;MS:0' )
SvF.Ylabel_x=0.35
if Lang=='Rus':
 M_SOIL.V.draw_name='Концентрация '+NiCu+', мг/кг(сух.веса) в почве';M_SOIL.A[0].oname='Годы';M_SOIL.V.oname='почва'
else:
 M_SOIL.V.draw_name=NiCu+' Concentration in soil, mg/kg dw';M_SOIL.A[0].oname='Years';M_SOIL.V.oname='soil'
Task.Draw ( 'M_SOIL;LC:brown;LSt:dashed;LW:1.5;MS:0' )
SvF.Ylabel_x=0.25
if Lang=='Rus':
 M_SEDIMENTION.V.draw_name='Запас '+NiCu+' в донных отложениях, мг/м2';M_SEDIMENTION.A[0].oname='Годы'
 M_SEDIMENTION.V.oname='донные отложения'
else:
 M_SEDIMENTION.V.draw_name='Amount of '+NiCu+' in botton sediments, mg/m2';M_SEDIMENTION.A[0].oname='Years'
 M_SEDIMENTION.V.oname='botton sediments'
Task.Draw ( 'M_SEDIMENTION;LC:brown;LSt:dashed;LW:1.5;MS:0' )
SvF.DataPath='Draw/'
TShore = Table ( 'SHORE.txt','TShore','*' )
xx,yy=LatLonToAzimut(TShore.dat('Y')[:],TShore.dat('X')[:])
Shore=Polyline(xx,yy,None,'Shore')
TTown = Table ( 'TOWN.txt','TTown','*' )
xx,yy=LatLonToAzimut(TTown.dat('Y')[:],TTown.dat('X')[:])
Town=Polyline(xx,yy,None,'Town')
TBrus = Table ( 'BORDER_R.txt','TBrus','*' )
xx,yy=LatLonToAzimut(TBrus.dat('Y')[:],TBrus.dat('X')[:])
Brus=Polyline(xx,yy,None,'Brus')
TBnor_fin = Table ( 'BORDER_F_N.txt','TBnor_fin','*' )
xx,yy=LatLonToAzimut(TBnor_fin.dat('Y')[:],TBnor_fin.dat('X')[:])
Bnor_fin=Polyline(xx,yy,None,'Bnor_fin')
SvF.curentTabl=None
PARALx=[];PARALy=[]
for y in range(66,70+1):
  if y%2==0:
    for x in range(28,38):
      PARALy.append(y)
      PARALx.append(x)
  else:
    for x in range(37,27,-1):
      PARALy.append(y)
      PARALx.append(x)
xx,yy=LatLonToAzimut(PARALy,PARALx)
PARAL=Polyline(xx,yy,None,'PARAL')
MERIDx=[];MERIDy=[]
for x in range(28,38):
  if x%2==0:
    for y in range(66,72):
      MERIDy.append(y)
      MERIDx.append(x)
  else:
    for y in range(71,65,-1):
      MERIDy.append(y)
      MERIDx.append(x)
xx,yy=LatLonToAzimut(MERIDy,MERIDx)
MERID=Polyline(xx,yy,None,'MERID')
Lakes=Polyline(TWater.dat('Xw')[:],TWater.dat('Yw')[:],None,'Lakes')
Deposs=Polyline(TDep.dat('Xd')[:],TDep.dat('Yd')[:],None,'Deposs')
PSoil=Polyline(TSoil.dat('Xs')[:],TSoil.dat('Ys')[:],None,'PSoil')
PbotSed=Polyline(TBott.dat('Xb')[:],TBott.dat('Yb')[:],None,'PbotSed')
SvF.Xsize=5.3
SvF.Legend=False
SvF.X_lim=[-110,110]
SvF.Y_lim=[-110,80]
Task.Draw ( 'PARAL;LC:gray;LW:1;MS:0 MERID Shore;LC:blue;LW:1;MS:0;LSt:solid Brus;LC:red;MS:0 Bnor_fin Lakes;MC:w;LW:0;MS:7;MEW:1;MEC:blue Deposs;MC:w;LC:w;MS:6;M:s;MEW:1;MEC:black PbotSed;M:^;MS:6;MEC:r PSoil;MC:g;M:X;MS:9;MEW:1;MEC:w Town;M:o;MS:6;LW:0;MC:red;MEW:2;MEC:black' )
X = Set('X',-100,100,4,'','X')
Y = Set('Y',-100,100,4,'','Y')
SvF.curentTabl=None
pPOL = Fun('pPOL',[X,Y], param=True)
def fpPOL(X,Y) : return pPOL.F([X,Y])
SoilXY = Fun('SoilXY',[X,Y], param=True)
def fSoilXY(X,Y) : return SoilXY.F([X,Y])
WaterXY = Fun('WaterXY',[X,Y], param=True)
def fWaterXY(X,Y) : return WaterXY.F([X,Y])
BotSedXY = Fun('BotSedXY',[X,Y], param=True)
def fBotSedXY(X,Y) : return BotSedXY.F([X,Y])
SoilXYp1 = Fun('SoilXYp1',[X,Y], param=True)
def fSoilXYp1(X,Y) : return SoilXYp1.F([X,Y])
WaterXYp1 = Fun('WaterXYp1',[X,Y], param=True)
def fWaterXYp1(X,Y) : return WaterXYp1.F([X,Y])
BotSedXYp1 = Fun('BotSedXYp1',[X,Y], param=True)
def fBotSedXYp1(X,Y) : return BotSedXYp1.F([X,Y])
SvF.DataMarkerSize = 2
SvF.Ylabel_x=0.05
SvF.Xlabel_x=0.96
SvF.Ylabel_y=0.90
SvF.Xlabel_y=0.07
SvF.X_lim=[-100,100]
SvF.Y_lim=[-100,100]
SvF.xaxis_step=50
SvF.yaxis_step=50
SvF.Xsize=5.3
SvF.Ysize=4.1
SvF.Legend=True
from matplotlib import ticker
SvF.locator=ticker.LogLocator(base=2.0)
SoilXYp1.grd[:,:]=fonSoilDW*fhSoil()*800
WaterXYp1.grd[:,:]=fonWater
BotSedXYp1.grd[:,:]=0
mapCOM=' PARAL;LC:gray;LW:1;MS:0 MERID Shore;LC:blue;LSt:solid Brus;LC:red;MS:0 Bnor_fin Town;M:o;MS:6;LW:0;MC:red;MEW:2;MEC:black'
pPOLleg='pPOL;L:2,8,16,32,64,128,9999;MS:0 '
pWATERleg='WaterXY;L:1.5,2,3,10,30,100,300;MS:0 '
pSOILleg='SoilXY;L:5,10,25,50,100,200,1000;MS:0 '
pBOTSEDleg='BotSedXY;L:0.3,1,3,10,30,100,1000;MS:0 '
for tv in range(1946,2051,1):
 SoilXY.grd[:,:]=SoilXYp1.grd[:,:]
 WaterXY.grd[:,:]=WaterXYp1.grd[:,:]
 BotSedXY.grd[:,:]=BotSedXYp1.grd[:,:]/1000
 for x in X.NodS:
  for y in Y.NodS:
    xv=X.Val[x]
    yv=Y.Val[y]
    depSo,depISo,BotSedXYp1.grd[x,y],SoilXYp1.grd[x,y],WaterXYp1.grd[x,y]=TimeStep(xv,yv,tv,30,1,SoilXY.grd[x,y],WaterXY.grd[x,y],BotSedXYp1.grd[x,y])
    pPOL.grd[x,y]=depSo+depISo
 SoilXY.grd[:,:]/=(800*fhSoil())
 if tv in[1980,1995,2018,2050]:
  if Lang=='Rus':
   pPOL.V.draw_name='Выпадениe '+NiCu+', мг/м2/год '+str(tv)
   WaterXY.V.draw_name=NiCu+' в воде, мг/м3 '+str(tv)
   SoilXY.V.draw_name=NiCu+' в почве, мг/кг(сух.веса) '+str(tv)
   BotSedXY.V.draw_name=NiCu+' в ДО, г/м2 '+str(tv)
  else:
   pPOL.V.draw_name=NiCu+' Deposition, mg/m2/year '+str(tv)
   WaterXY.V.draw_name=NiCu+' in water, mg/m3 '+str(tv)
   SoilXY.V.draw_name=NiCu+' in soil, mg/kg(dw) '+str(tv)
   BotSedXY.V.draw_name=NiCu+' in sediments, g/m2 '+str(tv)
  print(tv)
  Task.Draw(pPOLleg+'Deposs;MC:w;LC:w;MS:6;M:s;MEW:1;MEC:black;LW:0'+mapCOM)
  Task.Draw(pWATERleg+'Lakes;MC:w;LW:0;MS:7;MEW:1;MEC:blue;LW:0'+mapCOM)
  Task.Draw ( pSOILleg + 'PSoil;MC:g;M:X;MS:9;MEW:1;MEC:w;LW:0' + mapCOM )

  Task.Draw ( pBOTSEDleg + 'PbotSed;M:^;MS:6;MEC:r;LW:0' + mapCOM )
  continue
  Task.Draw ( 'SoilXY;L:10,25,50,100,200,1000;MS:0 PARAL;LC:gray;LW:1;MS:0 MERID Shore;LC:blue;LW:1;MS:0;LSt:solid Brus;LC:red;MS:0 Bnor_fin PSoil;MC:g;M:X;MS:9;MEW:1;MEC:w;LW:0 Town;M:o;MS:6;LW:0;MC:red;MEW:2;MEC:black' )
  Task.Draw ( 'SoilXY;L:11,25,50,100,200,1000;MS:0 PARAL;LC:gray;LW:1;MS:0 MERID Shore;LC:blue;LW:1;MS:0;LSt:solid Brus;LC:red;MS:0 Bnor_fin PSoil;MC:g;M:X;MS:9;MEW:1;MEC:w;LW:0 Town;M:o;MS:6;LW:0;MC:red;MEW:2;MEC:black' )
  Task.Draw ( 'WaterXY;L:1.2,3,10,30,100,300,1000,3000;MS:0 PARAL;LC:gray;LW:1;MS:0 MERID Shore;LC:blue;LW:1;MS:0;LSt:solid Brus;LC:red;MS:0 Bnor_fin Lakes;MC:w;LW:0;MS:7;MEW:1;MEC:blue Town;M:o;MS:6;LW:0;MC:red;MEW:2;MEC:black' )
  Task.Draw ( 'WaterXY;L:1.5,3,10,30,100,300,1000,3000;MS:0 PARAL;LC:gray;LW:1;MS:0 MERID Shore;LC:blue;LW:1;MS:0;LSt:solid Brus;LC:red;MS:0 Bnor_fin Lakes;MC:w;LW:0;MS:7;MEW:1;MEC:blue Town;M:o;MS:6;LW:0;MC:red;MEW:2;MEC:black' )
  Task.Draw ( 'BotSedXY;L:300,1000,3000,10000,30000,100000,1000000;MS:0 PARAL;LC:gray;LW:1;MS:0 MERID Shore;LC:blue;LW:1;MS:0;LSt:solid Brus;LC:red;MS:0 Bnor_fin PbotSed;M:^;MS:6;MEC:r;LW:0 Town;M:o;MS:6;LW:0;MC:red;MEW:2;MEC:black' )
  Task.Draw ( 'BotSedXY;L:200,1000,3000,10000,30000,100000,1000000;MS:0 PARAL;LC:gray;LW:1;MS:0 MERID Shore;LC:blue;LW:1;MS:0;LSt:solid Brus;LC:red;MS:0 Bnor_fin PbotSed;M:^;MS:6;MEC:r;LW:0 Town;M:o;MS:6;LW:0;MC:red;MEW:2;MEC:black' )
  Task.Draw ( 'BotSedXY;L:150,1000,3000,10000,30000,100000,1000000;MS:0 PARAL;LC:gray;LW:1;MS:0 MERID Shore;LC:blue;LW:1;MS:0;LSt:solid Brus;LC:red;MS:0 Bnor_fin PbotSed;M:^;MS:6;MEC:r;LW:0 Town;M:o;MS:6;LW:0;MC:red;MEW:2;MEC:black' )
  Task.Draw ( 'BotSedXY;L:100,1000,3000,10000,30000,100000,1000000;MS:0 PARAL;LC:gray;LW:1;MS:0 MERID Shore;LC:blue;LW:1;MS:0;LSt:solid Brus;LC:red;MS:0 Bnor_fin PbotSed;M:^;MS:6;MEC:r;LW:0 Town;M:o;MS:6;LW:0;MC:red;MEW:2;MEC:black' )
  Task.Draw ( 'BotSedXY;L:80,1000,3000,10000,30000,100000,1000000;MS:0 PARAL;LC:gray;LW:1;MS:0 MERID Shore;LC:blue;LW:1;MS:0;LSt:solid Brus;LC:red;MS:0 Bnor_fin PbotSed;M:^;MS:6;MEC:r;LW:0 Town;M:o;MS:6;LW:0;MC:red;MEW:2;MEC:black' )
  Task.Draw ( 'BotSedXY;L:70,1000,3000,10000,30000,100000,1000000;MS:0 PARAL;LC:gray;LW:1;MS:0 MERID Shore;LC:blue;LW:1;MS:0;LSt:solid Brus;LC:red;MS:0 Bnor_fin PbotSed;M:^;MS:6;MEC:r;LW:0 Town;M:o;MS:6;LW:0;MC:red;MEW:2;MEC:black' )
  Task.Draw ( 'BotSedXY;L:50,1000,3000,10000,30000,100000,1000000;MS:0 PARAL;LC:gray;LW:1;MS:0 MERID Shore;LC:blue;LW:1;MS:0;LSt:solid Brus;LC:red;MS:0 Bnor_fin PbotSed;M:^;MS:6;MEC:r;LW:0 Town;M:o;MS:6;LW:0;MC:red;MEW:2;MEC:black' )