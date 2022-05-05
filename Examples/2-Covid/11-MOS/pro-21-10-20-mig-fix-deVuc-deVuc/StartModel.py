# -*- coding: UTF-8 -*-
import sys
import platform
LibVersion = 'Lib29'
if platform.system() == 'Windows':
    path_SvF = "C:/_SvF/"
else:
    path_SvF = "/home/sokol/C/SvF/"
sys.path.append(path_SvF + LibVersion)
sys.path.append(path_SvF + "Everest/python-api")
sys.path.append(path_SvF + "pyomo-everest/ssop")
import COMMON as co
co.path_SvF = path_SvF
co.tmpFileDir = co.path_SvF + 'TMP/'
from CVSets import *
from Table  import *
from Task   import *
from MakeModel import *
from GIS import *

co.Task = TaskClass()
Task = co.Task
co.mngF = 'PROG_DR.mng'
co.Preproc = False
co.TaskName = 'COVID-RUS-PROG'
 											# prognose = True
prognose=True
Task.AddDef('prognose',[True])
 											# Norm = False #True
Norm=False
Task.AddDef('Norm',[False])
 											# Popul = 12636312.
Popul=12636312.
Task.AddDef('Popul',[12636312.])
 											# PopulMln = Popul / 1000000.
PopulMln=Popul/1000000.
Task.AddDef('PopulMln',[Popul/1000000.])
 											# PopulContrMln = (145934460-Popul)/1000000.
PopulContrMln=(145934460-Popul)/1000000.
 											# PopulMO_Mln = 7708499/1000000.
PopulMO_Mln=7708499/1000000.
Task.AddDef('PopulMO_Mln',[7708499/1000000.])
 											# #proVacc  = 50000.0 /Popul #*  доля
 											# proVacc  = 20000.0 /Popul #*  доля
proVacc=20000.0/Popul
Task.AddDef('proVacc',[20000.0/Popul])
 											# #proVacc  = 32000.0 /Popul #*  доля
 											# effVacc  = 0.916  #0.976
effVacc=0.916
Task.AddDef('effVacc',[0.916])
 											# timeVacc = 14
timeVacc=14
Task.AddDef('timeVacc',[14])
 											# begDate = 20200319
begDate=20200319
Task.AddDef('begDate',[20200319])
 											# endDate = 20211020
endDate=20211020
Task.AddDef('endDate',[20211020])
 											# #proDate = 20220101
 											# proDate = 20220503
proDate=20220503
Task.AddDef('proDate',[20220503])
 											# useNaN = True
co.useNaN = True
 											# DataAll = Select nCMos As nC, nCRus as nCR, nCMosObl as nCMO, ROWNUM AS t, date, Anti, nTest as nT, Vac, Exch  from ../../Moscow.xlsx \
 											# DataAll = Select nCMos As nC, nCRus as nCR, nCMosObl as nCMO, ROWNUM AS t, date, Anti, nTest as nT, Vac, Exch  from ../../Moscow.xlsx                                             where date >= begDate and date <= proDate
DataAll=Select ( 'Select nCMos As nC,nCRus as nCR,nCMosObl as nCMO,ROWNUM AS t,date,Anti,nTest as nT,Vac,Exch from ../../Moscow.xlsx As DataAll where date>= begDate and date<= proDate' )
 											# DataAll.nCR[:] = ( DataAll.nCR[:] - DataAll.nC[:] ) / PopulContrMln #* 3
DataAll.dat('nCR')[:]=(DataAll.dat('nCR')[:]-DataAll.dat('nC')[:])/PopulContrMln
 											# DataAll.nCMO[:] /= PopulMO_Mln
DataAll.dat('nCMO')[:]/=PopulMO_Mln
 											# DataAll.nC[:] /= PopulMln
DataAll.dat('nC')[:]/=PopulMln
 											# DataAll.nT[:] /= (5*Popul/1000)
DataAll.dat('nT')[:]/=(5*Popul/1000)
 											# DataAll.Anti[:] /= 100
DataAll.dat('Anti')[:]/=100
 											# Interpolate (DataAll.Vac)
Interpolate(DataAll.dat('Vac'))
 											# Extrapolate (DataAll.Vac)
Extrapolate(DataAll.dat('Vac'))
 											# Interpolate (DataAll.Exch)
Interpolate(DataAll.dat('Exch'))
 											# Extrapolate (DataAll.Exch)
Extrapolate(DataAll.dat('Exch'))
 											# DataAll.Vac[:] /= Popul
DataAll.dat('Vac')[:]/=Popul
 											# #Param: Exch(t)
 											# #Draw Exch
 											# #Param:  nCR(t)
 											# #    nC(t)
 											# #Draw nCR nC;DC:r
 											# # INCLUDE:  get_data.mng
 											# def to_npp ( int_date ) :
def to_npp(int_date):
 											#     return int ( (to_date(int_date)-to_date(begDate)).days )
    return int((to_date(int_date)-to_date(begDate)).days)
 											# SET:  Loc1   = [to_npp('2020-04-15'), to_npp('2020-06-01'), 1]
Loc1=Grid('Loc1',to_npp('2020-04-15'),to_npp('2020-06-01'),1.0,'i__Loc1','Loc1')
Task.AddGrid(Loc1)
 											#       Loc2   = [to_npp('2020-10-04'), to_npp('2021-01-18'), 1]
Loc2=Grid('Loc2',to_npp('2020-10-04'),to_npp('2021-01-18'),1.0,'i__Loc2','Loc2')
Task.AddGrid(Loc2)
 											#       uL2    = [to_npp('2021-03-28'), to_npp('2021-04-26'), 1]
uL2=Grid('uL2',to_npp('2021-03-28'),to_npp('2021-04-26'),1.0,'i__uL2','uL2')
Task.AddGrid(uL2)
 											#       Loc3   = [to_npp('2021-05-01'), to_npp('2021-05-10'), 1]
Loc3=Grid('Loc3',to_npp('2021-05-01'),to_npp('2021-05-10'),1.0,'i__Loc3','Loc3')
Task.AddGrid(Loc3)
 											#       uL3    = [to_npp('2021-05-11'), to_npp('2021-06-07'), 1]
uL3=Grid('uL3',to_npp('2021-05-11'),to_npp('2021-06-07'),1.0,'i__uL3','uL3')
Task.AddGrid(uL3)
 											#       Loc4   = [to_npp('2021-06-09'), to_npp('2021-06-19'), 1]
Loc4=Grid('Loc4',to_npp('2021-06-09'),to_npp('2021-06-19'),1.0,'i__Loc4','Loc4')
Task.AddGrid(Loc4)
 											#       uL4    = [to_npp('2021-07-14'), to_npp('2021-07-21'), 1]
uL4=Grid('uL4',to_npp('2021-07-14'),to_npp('2021-07-21'),1.0,'i__uL4','uL4')
Task.AddGrid(uL4)
 											#       Loc5   = [to_npp('2021-09-29'), to_npp('2021-10-03'), 1]
Loc5=Grid('Loc5',to_npp('2021-09-29'),to_npp('2021-10-03'),1.0,'i__Loc5','Loc5')
Task.AddGrid(Loc5)
 											# maxFb = .8 #0.6  #9  #6
maxFb=.8
Task.AddDef('maxFb',[.8])
 											# Imax = 16
Imax=16
Task.AddDef('Imax',[16])
 											# tam = 14
tam=14
Task.AddDef('tam',[14])
 											# st = 1
st=1
Task.AddDef('st',[1])
 											# max_Imun = 280
max_Imun=280
Task.AddDef('max_Imun',[280])
 											# GRID:    ta  = [ 0, tam,    st, tai ]
ta=Grid('ta',0.0,tam,st,'tai','ta')
Task.AddGrid(ta)
 											#      ta1 = [ 0, tam-st, st, tai ]
ta1=Grid('ta1',0.0,tam-st,st,'tai','ta1')
Task.AddGrid(ta1)
 											# #Var:     b ( ta ); PolyPow = 10;  >= 0; ∫r(ta,dta*b(ta)) = 1; \
 											# #Var:     b ( ta );   >= 0; ∫r(ta,dta*b(ta)) = 1;  b(0)=0; b(1)<0.005; b(2)<0.007;  b(tam)=0; #b(tam-1)<0.005;
 											# Param:    b ( ta ) = b(ta).sol ; #  >= 0; ∫r(ta,dta*b(ta)) = 1;  b(0)=0; b(1)<0.005; b(2)<0.007;  b(tam)=0; #b(tam-1)<0.005;
b = Fun('b',[ta],True); 
Task.InitializeAddFun ( b, 'b(ta).sol' )
b__f = b
def fb(ta) : return b.F([ta])
 											# Set:    testS = [ 0, 9, -30 ]
testS=Grid('testS',0.0,9.0,0.3,'i__testS','testS')
Task.AddGrid(testS)
 											# Var:    F(testS) > 0;    d/dtestS(F) >= 0  #.3;
F = Fun('F',[testS],False); 
Task.InitializeAddFun ( F )
F__f = F
def fF(testS) : return F.F([testS])
 											# #Var:    F(testS) > 0;  F(0)<=0.01;  d/dtestS(F) >= 0  #.3;
 											# #Var:    F(testS) > 0;  PolyPow = 6;   F(0)<=0.01;  d/dtestS(F) >= 0  #.3;
 											# Data = Select * from DataAll where date <= endDate
Data=Select ( 'Select * from DataAll As Data where date<= endDate' )
 											# nC3 = Data.nC[0]+Data.nC[1]+Data.nC[2]
nC3=Data.dat('nC')[0]+Data.dat('nC')[1]+Data.dat('nC')[2]
 											# tMaxData = int ( Data.t[-1] )
tMaxData=int(Data.dat('t')[-1])
 											# if prognose :  tMax = to_npp ( proDate )
if prognose:tMax=to_npp(proDate)
 											# else        :  tMax = tMaxData
else:tMax=tMaxData
Task.AddDef('else:tMax',[tMaxData])
 											# GRID:    t   =  [         ,    tMax,  st, ti  ]        # Time - number of point (first=0)
t=Grid('t',nan,tMax,st,'ti','t')
Task.AddGrid(t)
 											#      tp  =  [ t.min+st,    tMax,  st, tpi  ]
tp=Grid('tp', t.min+st,tMax,st,'tpi','tp')
Task.AddGrid(tp)
 											#      tPro = [ tMaxData+1,  tMax,  st, ti  ]
tPro=Grid('tPro', tMaxData+1,tMax,st,'ti','tPro')
Task.AddGrid(tPro)
 											#      t365 = [ 0, max_Imun, 1]
t365=Grid('t365',0.0,max_Imun,1.0,'i__t365','t365')
Task.AddGrid(t365)
 											# Param:    Vac (t)
Vac = Fun('Vac',[t],True); 
Task.InitializeAddFun ( Vac )
Vac__f = Vac
def fVac(t) : return Vac.F([t])
 											# Param:    Exch (t)
Exch = Fun('Exch',[t],True); 
Task.InitializeAddFun ( Exch )
Exch__f = Exch
def fExch(t) : return Exch.F([t])
 											# nCRdate = Select * from ../nC-Rus/nCR(t).sol
nCRdate=Select ( 'Select * from ../nC-Rus/nCR(t).sol As nCRdate' )
 											# Param:    nCR ( t )
nCR = Fun('nCR',[t],True); 
Task.InitializeAddFun ( nCR )
nCR__f = nCR
def fnCR(t) : return nCR.F([t])
 											# for t_nCR in range ( int(nCRdate.t[-1]), t.max ) : nCR.grd[t_nCR+1] = nCR.grd[t_nCR]
for t_nCR in range(int(nCRdate.dat('t')[-1]),t.max): nCR.grd[t_nCR+1]=nCR.grd[t_nCR]
 											# nTdate = Select * from ../nT/nT(t).sol
nTdate=Select ( 'Select * from ../nT/nT(t).sol As nTdate' )
 											# Param:    nT ( t )
nT = Fun('nT',[t],True); 
Task.InitializeAddFun ( nT )
nT__f = nT
def fnT(t) : return nT.F([t])
 											# for t_nT in range ( int(nTdate.t[-1]), t.max ) : nT.grd[t_nT+1] = nT.grd[t_nT]
for t_nT in range(int(nTdate.dat('t')[-1]),t.max): nT.grd[t_nT+1]=nT.grd[t_nT]
 											# if prognose :
if prognose:
 											#     for iv in tPro.Val :
    for iv in tPro.Val:
 											#         tt = int (iv)
        tt=int(iv)
 											#         nCR.grd[tt] = nCR.grd[tt-1]
        nCR.grd[tt]=nCR.grd[tt-1]
 											#         nT.grd[tt]  = nT.grd[tt-1]
        nT.grd[tt]=nT.grd[tt-1]
 											#         Vac.grd[tt] = Vac.grd[tt-1] + proVacc
        Vac.grd[tt]=Vac.grd[tt-1]+proVacc
 											#         Exch.grd[tt] = Exch.grd[tt-1]
        Exch.grd[tt]=Exch.grd[tt-1]
 											# for tt in range ( int(tMax), timeVacc-1, -1 ) :  Vac.grd[tt] = Vac.grd[tt-timeVacc]    # сдвиг на 2 недели
for tt in range(int(tMax),timeVacc-1,-1): Vac.grd[tt]=Vac.grd[tt-timeVacc]
 											# #Draw nCR
 											# #Draw Vac
 											# #Draw Exch
 											# Param: dVac (t)
dVac = Fun('dVac',[t],True); 
Task.InitializeAddFun ( dVac )
dVac__f = dVac
def fdVac(t) : return dVac.F([t])
 											# for i in range( 1, int(tMax)+1 ) :
for i in range(1,int(tMax)+1):
 											#     if i>0 : dVac.grd[i] =  Vac.grd[i] - Vac.grd[i-1]
    if i>0:dVac.grd[i]=Vac.grd[i]-Vac.grd[i-1]
 											# #Draw dVac
 											# curentTabl = Data
co.curentTabl = Data
 											# Var:    Mig ( t )
Mig = Fun('Mig',[t],False); 
Task.InitializeAddFun ( Mig )
Mig__f = Mig
def fMig(t) : return Mig.F([t])
 											#     MigCoef > 0.05; < 0.2                 #  миграция  5%
MigCoef = Fun('MigCoef',[],False); 
Task.InitializeAddFun ( MigCoef )
MigCoef__f = MigCoef
fMigCoef = MigCoef.grd
 											#     ActR > 3; < 4
ActR = Fun('ActR',[],False); 
Task.InitializeAddFun ( ActR )
ActR__f = ActR
fActR = ActR.grd
 											# Var:    nC ( t )  >= 0
nC = Fun('nC',[t],False); 
Task.InitializeAddFun ( nC )
nC__f = nC
def fnC(t) : return nC.F([t])
 											#     n (t, ta)>= 0;
n = Fun('n',[t,ta],False); 
Task.InitializeAddFun ( n )
n__f = n
def fn(t,ta) : return n.F([t,ta])
 											#     N  ( t )  >= 0;   N = ∫r(ta,dta*n(t,ta));   N < 1000000*0.30;  #N(0) < nC3/3*100;
N = Fun('N',[t],False); 
Task.InitializeAddFun ( N )
N__f = N
def fN(t) : return N.F([t])
 											#     n0 >= 0;
n0 = Fun('n0',[],False); 
Task.InitializeAddFun ( n0 )
n0__f = n0
fn0 = n0.grd
 											#     np >0.75; <=0.8
np = Fun('np',[],False); 
Task.InitializeAddFun ( np )
np__f = np
fnp = np.grd
 											# Var:    R0  ( t ) >= 0; <= Imax;   R0(tMax) = R0(tMax-1); \
 											# Var:    R0  ( t ) >= 0; <= Imax;   R0(tMax) = R0(tMax-1);               d/dLoc2(R0(Loc2)) <0;  d/duL2(R0(uL2)) >0; \
 											# Var:    R0  ( t ) >= 0; <= Imax;   R0(tMax) = R0(tMax-1);               d/dLoc2(R0(Loc2)) <0;  d/duL2(R0(uL2)) >0;               d/dLoc3(R0(Loc3)) <0;  d/duL3(R0(uL3)) >0; \
 											# Var:    R0  ( t ) >= 0; <= Imax;   R0(tMax) = R0(tMax-1);               d/dLoc2(R0(Loc2)) <0;  d/duL2(R0(uL2)) >0;               d/dLoc3(R0(Loc3)) <0;  d/duL3(R0(uL3)) >0;               d/dLoc4(R0(Loc4)) <0;  d/duL4(R0(uL4)) >0; # \ ##.005;  ###########################
R0 = Fun('R0',[t],False); 
Task.InitializeAddFun ( R0 )
R0__f = R0
def fR0(t) : return R0.F([t])
 											# #              d/dLoc5(R0(Loc5)) <0;
 											#     IS ( t ) >= 0;   # IS * b <= maxFb;
IS = Fun('IS',[t],False); 
Task.InitializeAddFun ( IS )
IS__f = IS
def fIS(t) : return IS.F([t])
 											#     B  ( t ) >= 0;
B = Fun('B',[t],False); 
Task.InitializeAddFun ( B )
B__f = B
def fB(t) : return B.F([t])
 											#     Anti(t) > 0; < 1
Anti = Fun('Anti',[t],False); 
Task.InitializeAddFun ( Anti )
Anti__f = Anti
def fAnti(t) : return Anti.F([t])
 											#     VacImm (t) >=0
VacImm = Fun('VacImm',[t],False); 
Task.InitializeAddFun ( VacImm )
VacImm__f = VacImm
def fVacImm(t) : return VacImm.F([t])
 											# #Var:    Imun (t365) >0.0;  d/dt365(Imun) <=0; Imun(0)= 1; Imun(max_Imun)= 0.
 											# Param:  Imun (t365) = Imun(t365).sol
Imun = Fun('Imun',[t365],True); 
Task.InitializeAddFun ( Imun, 'Imun(t365).sol' )
Imun__f = Imun
def fImun(t365) : return Imun.F([t365])
 											# Var:    Vacc (t365) >0.0;  d/dt365(Vacc) <=0; Vacc(0)= effVacc; Vacc(max_Imun)= 0.
Vacc = Fun('Vacc',[t365],False); 
Task.InitializeAddFun ( Vacc )
Vacc__f = Vacc
def fVacc(t365) : return Vacc.F([t365])
 											# #Param:  Vacc (t365) = Vacc(t365).sol
 											# EQ:      if ti+st <= t.max:   (n(t+st,ta1+st)-n(t,ta1))/st = -( IS(t)*b(ta1) )*n(t,ta1)
 											# #     B (t) = R0(t) * (1-Anti(t)) * (1-VacImm(t)*effVacc) * ∫r(ta,dta*b(ta)*n(t,ta)) * (1. + Mig(t)/nC(t))
 											#      B (t) = R0(t) * (1-Anti(t)) * (1-VacImm(t)) * ∫r(ta,dta*b(ta)*n(t,ta)) * (1. + Mig(t)/nC(t))
 											#      n(tp,0) = B(tp-st) # + Mig(tp)
 											#      n(0,ta) = n0 * (np**ta)
 											#      IS(t) = F(nT(t))
 											#          nC(t)  = IS(t) * ∫r(ta1,dta1*b(ta1)*n(t,ta1) )
 											#     nC(0)+nC(1)+nC(2) >= nC3/3
 											#     nC(0)+nC(1)+nC(2) <= nC3*3
 											# #    Anti = ∫r(max(1,t-max_Imun),t,dtp*B(tp-1)*Imun(t-tp)) / 1000000  #  доля  за полгода  - 250
 											# #    Anti = ∫r(max(0,t-max_Imun),t,dtp*B(tp)*Imun(t-tp)) / 1000000  #  доля  за полгода  - 280  max_Imun
 											#     Anti = ∫(max(0,t-max_Imun),t,dtp*B(tp)*Imun(t-tp)) / 1000000  #  доля  за полгода  - 280  max_Imun
 											#     VacImm = ∫(max(0,t-max_Imun),t,dtp*dVac(tp)*Vacc(t-tp))   #  доля  за полгода  - 280  max_Imun
 											# #        n(t,tam) >= 2*nC(t)
 											#     Mig = (ActR * nCR - nC) * MigCoef * Exch
 											# # INCLUDE:  common.mng
 											# Task.ReadSols()
Task.ReadSols()
 											# #Draw Vac VacImm;LC:b
 											# #Draw B Mig
 											# #Draw N nCR
 											# Draw Vacc

Task.Draw (  'Vacc' )
 											# realProg = True
realProg=True
Task.AddDef('realProg',[True])
 											# realProg = False
realProg=False
Task.AddDef('realProg',[False])
 											# Dat = Select nC As nCr, nT, nCR, t AS tr, date from DataAll as Dat  where date > endDate  #where date <= proTime
Dat=Select ( 'Select nC As nCr,nT,nCR,t AS tr,date from DataAll as Dat where date>endDate' )
 											# Var: nCr(tr)
nCr = Fun('nCr',['tr'],False); 
Task.InitializeAddFun ( nCr )
nCr__f = nCr
def fnCr(tr) : return nCr.F([tr])
 											# nCr.V.name = 'verification set'
nCr.V.name='verification set'
Task.AddDef('nCr.V.name',['verification set'])
 											# #nCRdate = Select * from ../nC-MO/nMO(t).sol
 											# Param:    nCMO ( t ) = ../nC-MO/nCMO(t).sol
nCMO = Fun('nCMO',[t],True); 
Task.InitializeAddFun ( nCMO, '../nC-MO/nCMO(t).sol' )
nCMO__f = nCMO
def fnCMO(t) : return nCMO.F([t])
 											# #Draw nCR
 											# Draw nC nCR nCMO;LC:g

Task.Draw (  'nC nCR nCMO;LC:g' )
 											# #GRID:    tPro = [ 500,  tMax,  st, ti  ]
 											# for iv in tPro.Val :
for iv in tPro.Val:
 											#     t9 = int (iv)
    t9=int(iv)
 											# #    print ('{',t,Anti.grd[t])
 											# #    Vac.grd[t9] = 0 #+= 1000/Popul  ######################
 											#     if realProg :
    if realProg:
 											#         R0.grd[t9] = R0.grd[t9-1] + 0.013             ##########################
        R0.grd[t9]=R0.grd[t9-1]+0.013
 											#         if R0.grd[t9] > 2.5:  R0.grd[t9] = 2.5       ##########################
        if R0.grd[t9]>2.5:R0.grd[t9]=2.5
 											#         nT.grd[t9] = nT.grd[t9-1] - 0.04             ##########################
        nT.grd[t9]=nT.grd[t9-1]-0.04
 											#         if nT.grd[t9] < 4.5:  nT.grd[t9] = 4.5       ##########################
        if nT.grd[t9]<4.5:nT.grd[t9]=4.5
 											#         IS.grd[t9] = fF(nT.grd[t9])
        IS.grd[t9]=fF(nT.grd[t9])
 											# #        IS.grd[t9] = IS.grd[t9-1] - 0.001             ##########################
 											# #        if IS.grd[t9] < 0.1:  IS.grd[t9] = 0.1       ##########################
 											#     for tau in  ta1.NodS :
    for tau in ta1.NodS:
 											#     #    ta = int (tau)
 											# #        print ('ta',tau, b.grd[tau])
 											#         n.grd[t9,tau+1] = n.grd[t9-1,tau] * ( 1 - IS.grd[t9-1]*b.grd[tau] )
        n.grd[t9,tau+1]=n.grd[t9-1,tau]*(1-IS.grd[t9-1]*b.grd[tau])
 											#     n.grd[t9,0]= B.grd[t9-1] #+ Mig.grd[t9]
    n.grd[t9,0]=B.grd[t9-1]
 											#     VacImm.grd[t9] = sum ((dVac.grd[tt+1]*Vacc.grd[t9-tt-1]+dVac.grd[tt]*Vacc.grd[t9-tt])*0.5  for tt in range(t9-max_Imun, t9) )
    VacImm.grd[t9]=sum((dVac.grd[tt+1]*Vacc.grd[t9-tt-1]+dVac.grd[tt]*Vacc.grd[t9-tt])*0.5 for tt in range(t9-max_Imun,t9))
 											#     Anti.grd[t9] = sum ((B.grd[tt+1]*Imun.grd[t9-tt-1]+B.grd[tt]*Imun.grd[t9-tt])*0.5  for tt in range(t9-max_Imun, t9) )  / 1000000
    Anti.grd[t9]=sum((B.grd[tt+1]*Imun.grd[t9-tt-1]+B.grd[tt]*Imun.grd[t9-tt])*0.5 for tt in range(t9-max_Imun,t9))/1000000
 											#     Mig.grd[t9] = (ActR.grd * nCR.grd[t9-1] - nC.grd[t9-1]) * MigCoef.grd * Exch.grd[t9]
    Mig.grd[t9]=(ActR.grd*nCR.grd[t9-1]-nC.grd[t9-1])*MigCoef.grd*Exch.grd[t9]
 											# #    B.grd[t9] = R0.grd[t9] * (1-Anti.grd[t9]) * (1-VacImm.grd[t9]*effVacc)  * sum ( b.grd[tau] * n.grd[t9,tau] for tau in ta.NodS ) \
 											#     B.grd[t9] = R0.grd[t9] * (1-Anti.grd[t9]) * (1-VacImm.grd[t9])  * sum ( b.grd[tau] * n.grd[t9,tau] for tau in ta.NodS ) \
 											#     B.grd[t9] = R0.grd[t9] * (1-Anti.grd[t9]) * (1-VacImm.grd[t9])  * sum ( b.grd[tau] * n.grd[t9,tau] for tau in ta.NodS )       * (1.+Mig.grd[t9]/nC.grd[t9])
    B.grd[t9]=R0.grd[t9]*(1-Anti.grd[t9])*(1-VacImm.grd[t9])*sum(b.grd[tau]*n.grd[t9,tau]for tau in ta.NodS)*(1.+Mig.grd[t9]/nC.grd[t9])
 											# #    Anti.grd[t9] = sum ((B.grd[tt+1]*Imun.grd[t9-tt-1]+B.grd[tt]*Imun.grd[t9-tt])*0.5  for tt in range(t9-max_Imun, t9) )  / 1000000    # iteration
 											# #    B.grd[t9] =  R0.grd[t9] * (1-Anti.grd[t9]) * (1-VacImm.grd[t9]*effVacc)  * sum ( b.grd[tau] * n.grd[t9,tau] for tau in ta.NodS )  # ВЛИЯЕТ СЛАБО
 											#     nC.grd[t9]  = IS.grd[t9] * sum ( b.grd[tau] * n.grd[t9,tau]  for tau in ta1.NodS )
    nC.grd[t9]=IS.grd[t9]*sum(b.grd[tau]*n.grd[t9,tau]for tau in ta1.NodS)
 											#     N.grd[t9] = sum ( n.grd[t9,tau]  for tau in ta1.NodS )
    N.grd[t9]=sum(n.grd[t9,tau]for tau in ta1.NodS)
 											# #Draw Vac VacImm;LC:g
 											# #Draw B
 											# DatM = Select date As month, t AS tm from DataAll     where month%100==1        # month
DatM=Select ( 'Select date As month,t AS tm from DataAll As DatM where month%100==1' )
 											# for i in t.NodS :
for i in t.NodS:
 											#     if i >= DatM.tm[-1]+30 :  DatM.AppendRec (0, DatM.tm[-1]+367./12)  #30)
    if i>= DatM.dat('tm')[-1]+30:DatM.AppendRec(0,DatM.dat('tm')[-1]+367./12)
 											# print ('MMM', DatM.tm)
print('MMM',DatM.dat('tm'))
 											# Var: month(tm)
month = Fun('month',['tm'],False); 
Task.InitializeAddFun ( month )
month__f = month
def fmonth(tm) : return month.F([tm])
 											# month.V.dat[:] = -0.2;  month.V.name = '';  month.A[0].oname = 't'
month.V.dat[:]=-0.2;month.V.name='';month.A[0].oname='t'
 											# DatY = Select date As year, t AS tm from DataAll     where year%10100==1        # year
DatY=Select ( 'Select date As year,t AS tm from DataAll As DatY where year%10100==1' )
 											# for i in DatM.tm[:] :
for i in DatM.dat('tm')[:]:
 											#     print (i, DatY.tm[-1])
    print(i,DatY.dat('tm')[-1])
 											#     if i >= DatY.tm[-1]+364 :  DatY.AppendRec (0, i)
    if i>= DatY.dat('tm')[-1]+364:DatY.AppendRec(0,i)
 											# print ('YYY', DatY.tm)
print('YYY',DatY.dat('tm'))
 											# Var: year(tm)
year = Fun('year',['tm'],False); 
Task.InitializeAddFun ( year )
year__f = year
def fyear(tm) : return year.F([tm])
 											# year.V.dat[:] = -0.2;  year.V.name = '';  year.A[0].oname = 't';
year.V.dat[:]=-0.2;year.V.name='';year.A[0].oname='t';
 											# DatTod = Select tm, ROWNUM as today from DatM     where today <= 2            # today
DatTod=Select ( 'Select tm,ROWNUM as today from DatM As DatTod where today<= 2' )
 											# Var: today(tm)
today = Fun('today',['tm'],False); 
Task.InitializeAddFun ( today )
today__f = today
def ftoday(tm) : return today.F([tm])
 											# today.V.name= ''
today.V.name=''
Task.AddDef('today.V.name',[''])
 											# Param: SB (t)
SB = Fun('SB',[t],True); 
Task.InitializeAddFun ( SB )
SB__f = SB
def fSB(t) : return SB.F([t])
 											# for i in t.NodS :
for i in t.NodS:
 											#     if i == 0 : SB.grd[i] = 0
    if i== 0:SB.grd[i]=0
 											#     else      : SB.grd[i] = SB.grd[i-1] + (B.grd[i-1]+B.grd[i])*0.5/10000  #1000000*100
    else:SB.grd[i]=SB.grd[i-1]+(B.grd[i-1]+B.grd[i])*0.5/10000
 											# #Legend = False
 											# if not Norm :
if not Norm:
 											#     nC.grd[:]       *= (PopulMln/1000)
    nC.grd[:]*=(PopulMln/1000)
 											#     nC.V.dat[:]     *= (PopulMln/1000)
    nC.V.dat[:]*=(PopulMln/1000)
 											#     nCr.V.dat[:]     *= (PopulMln/1000)
    nCr.V.dat[:]*=(PopulMln/1000)
 											#     N.grd[:]       *= (PopulMln/1000)
    N.grd[:]*=(PopulMln/1000)
 											#     B.grd[:]       *= (PopulMln/1000)
    B.grd[:]*=(PopulMln/1000)
 											#     year.V.dat[:]   *= (PopulMln/1000)
    year.V.dat[:]*=(PopulMln/1000)
 											# #    month.V.dat[9]  *= (PopulMln/1000)
 											# #    month.V.dat[21] *= (PopulMln/1000)
 											# Teach = Select t, nC from Data
Teach=Select ( 'Select t,nC from Data As Teach' )
 											# Teach.nC[:] *= PopulMln/1000
Teach.dat('nC')[:]*=PopulMln/1000
 											# Teach.WriteSvFtbl ( 'test.txt' )
Teach.WriteSvFtbl('test.txt')
 											# Test = Select tr, nCr from Dat
Test=Select ( 'Select tr,nCr from Dat As Test' )
 											# Test.nCr[:] *= PopulMln/1000
Test.dat('nCr')[:]*=PopulMln/1000
 											# Test.WriteSvFtbl ( 'test.txt' )
Test.WriteSvFtbl('test.txt')
 											# nC.SaveSol ('nCtbl.txt')
nC.SaveSol('nCtbl.txt')
 											# vave3 = sum ( nC.grd[int(iv)] for iv in range (tMaxData+1,  tMax+1 ) )
vave3=sum(nC.grd[int(iv)]for iv in range(tMaxData+1,tMax+1))
 											# print     ('1 may   ', vave3)
print('1 may ',vave3)
 											# vave3 = sum ( nC.grd[int(iv)] for iv in range (tMaxData+1,  tMax+1-30 ) )
vave3=sum(nC.grd[int(iv)]for iv in range(tMaxData+1,tMax+1-30))
 											# print     ('1 april   ', vave3)
print('1 april ',vave3)
 											# vave3 = sum ( nC.grd[int(iv)] for iv in range (tMaxData+1,  653 ) )
vave3=sum(nC.grd[int(iv)]for iv in range(tMaxData+1,653))
 											# print     ('NY   ', vave3)
print('NY ',vave3)
 											# #Draw B
 											# today.V.dat[0] = -0.4;  today.V.dat[1] = 9.5;  today.A[0].min = Data.NoR-1;  today.A[0].dat[:] = 0;                  # nC
today.V.dat[0]=-0.4;today.V.dat[1]=9.5;today.A[0].min=Data.NoR-1;today.A[0].dat[:]=0;
 											# nC.A[0].oname = 't';
nC.A[0].oname='t';
 											# co.Draw_data_str = ''
co.Draw_data_str=''
Task.AddDef('co.Draw_data_str',[''])
 											# Ylabel_x=0.2
co.Ylabel_x = 0.2
 											# nCdata = nC.Clone();  nCdata.V.name= 'nCdata'; Task.AddFun (nCdata); nCdata.V.name= 'teaching set'
nCdata=nC.Clone();nCdata.V.name='nCdata';Task.AddFun(nCdata);nCdata.V.name='teaching set'
 											# nC.V.dat = None; nC.V.oname= 'nC model'; nC.V.draw_name= 'nC - новые случаи (тыс.чел.)';
nC.V.dat=None;nC.V.oname='nC model';nC.V.draw_name='nC-новые случаи(тыс.чел.)';
 											# Draw month;LW:0;MS:0;DC:black;DMS:5;DM:| year;DMS:12 today;DLW:1;DC:y nCr;DC:green;LW:0;MS:0;DLW:0;DMS:3;DM:. nCdata;MS:0;LW:0;DC:b nC;LW:2

Task.Draw (  'month;LW:0;MS:0;DC:black;DMS:5;DM:| year;DMS:12 today;DLW:1;DC:y nCr;DC:green;LW:0;MS:0;DLW:0;DMS:3;DM:. nCdata;MS:0;LW:0;DC:b nC;LW:2' )
 											# Draw month;LW:0;MS:0;DC:black;DMS:5;DM:| year;DMS:12 today;DLW:1;DC:black nCr;DC:black;LW:0;MS:0;DLW:0;DMS:3;DM:. nCdata;MS:0;LW:0;DC:black;DM:x nC;LW:1;LC:black

Task.Draw (  'month;LW:0;MS:0;DC:black;DMS:5;DM:| year;DMS:12 today;DLW:1;DC:black nCr;DC:black;LW:0;MS:0;DLW:0;DMS:3;DM:. nCdata;MS:0;LW:0;DC:black;DM:x nC;LW:1;LC:black' )
 											# Ylabel_x=0.03
co.Ylabel_x = 0.03
 											# co.Draw_data_str = '-data'
co.Draw_data_str='-data'
Task.AddDef('co.Draw_data_str',['-data'])
 											# Draw N;DC:green;LW:2;MS:0 nC;DC:b;LW:2 month;LW:0;DC:black;DMS:5;DM:| year;DMS:12

Task.Draw (  'N;DC:green;LW:2;MS:0 nC;DC:b;LW:2 month;LW:0;DC:black;DMS:5;DM:| year;DMS:12' )
 											# # Imun.A[0].oname = 't'
 											# # Draw Imun
 											# Im = Anti.Clone();  Im.V.name= 'Immunized'; Im.V.dat = None; Task.AddFun (Im);
Im=Anti.Clone();Im.V.name='Immunized';Im.V.dat=None;Task.AddFun(Im);
 											# Im.grd[:] = ( 1- (1-Anti.grd[:]) * (1- VacImm.grd[:]*effVacc) )*100
Im.grd[:]=(1-(1-Anti.grd[:])*(1-VacImm.grd[:]*effVacc))*100
 											# Anti.grd[:] *= 100;  Anti.V.dat[:] *= 100;  Vac.grd[:] *= 100
Anti.grd[:]*=100;Anti.V.dat[:]*=100;Vac.grd[:]*=100
 											# VacImm.grd[:] *= 100;
VacImm.grd[:]*=100;
 											# Param: LostImm (t)
LostImm = Fun('LostImm',[t],True); 
Task.InitializeAddFun ( LostImm )
LostImm__f = LostImm
def fLostImm(t) : return LostImm.F([t])
 											# LostImm.grd[:] = SB.grd[:] - Anti.grd[:]
LostImm.grd[:]=SB.grd[:]-Anti.grd[:]
 											# Legend = True
co.Legend = True
 											# today.V.draw_name = '% населения Москвы'
today.V.draw_name='%населения Москвы'
Task.AddDef('today.V.draw_name',['%населения Москвы'])
 											# month.V.dat[:] = -3;  year.V.dat[:] = -3; today.V.dat[0] = 0;  today.V.dat[1] = 100; today.V.oname = 'Antibody (%)';
month.V.dat[:]=-3;year.V.dat[:]=-3;today.V.dat[0]=0;today.V.dat[1]=100;today.V.oname='Antibody(%)';
 											# Draw SB;LC:g  Anti;LC:r;DMS:4  LostImm;LC:b month;LW:0;MS:0;DC:black;DMS:5;DM:| year;DMS:12 today;DLW:1;DC:y

Task.Draw (  'SB;LC:g Anti;LC:r;DMS:4 LostImm;LC:b month;LW:0;MS:0;DC:black;DMS:5;DM:| year;DMS:12 today;DLW:1;DC:y' )
 											# Param: LostImmDay (t)
LostImmDay = Fun('LostImmDay',[t],True); 
Task.InitializeAddFun ( LostImmDay )
LostImmDay__f = LostImmDay
def fLostImmDay(t) : return LostImmDay.F([t])
 											# LostImmDay.grd[1:int(t.max)] = (LostImm.grd[1:int(t.max)] - LostImm.grd[0:int(t.max)-1])*PopulMln*10
LostImmDay.grd[1:int(t.max)]=(LostImm.grd[1:int(t.max)]-LostImm.grd[0:int(t.max)-1])*PopulMln*10
 											# LostImmDay.grd[int(t.max)] = LostImmDay.grd[int(t.max)-1]
LostImmDay.grd[int(t.max)]=LostImmDay.grd[int(t.max)-1]
 											# today.V.dat[1] = 70;
today.V.dat[1]=70;
 											# Draw B;LC:g  LostImmDay;LC:b month;LW:0;MS:0;DC:black;DMS:5;DM:| year;DMS:12 today;DLW:1;DC:y

Task.Draw (  'B;LC:g LostImmDay;LC:b month;LW:0;MS:0;DC:black;DMS:5;DM:| year;DMS:12 today;DLW:1;DC:y' )
 											# month.V.dat[:] = -3;  year.V.dat[:] = -3; today.V.dat[0] = 0;  today.V.dat[1] = 65; today.V.oname = 'Immunization';
month.V.dat[:]=-3;year.V.dat[:]=-3;today.V.dat[0]=0;today.V.dat[1]=65;today.V.oname='Immunization';
 											# VacImm.V.dat = None
VacImm.V.dat=None
Task.AddDef('VacImm.V.dat',[None])
 											# Ylabel_x=0.15
co.Ylabel_x = 0.15
 											# Im.oname = 'Immunized'
Im.oname='Immunized'
Task.AddDef('Im.oname',['Immunized'])
 											# Draw Immunized;LC:g  Anti;LC:r;DMS:4  VacImm;LC:b month;LW:0;MS:0;DC:black;DMS:5;DM:| year;DMS:12 today;DLW:1;DC:y

Task.Draw (  'Immunized;LC:g Anti;LC:r;DMS:4 VacImm;LC:b month;LW:0;MS:0;DC:black;DMS:5;DM:| year;DMS:12 today;DLW:1;DC:y' )
 											# #Legend = False
 											# R0A = R0.Clone();  R0A.V.name= 'R0A'; Task.AddFun (R0A);  R0A.grd[:] = R0A.grd[:]*(1-Anti.grd[:]/100); R0A.V.oname= 'R0A';
R0A=R0.Clone();R0A.V.name='R0A';Task.AddFun(R0A);R0A.grd[:]=R0A.grd[:]*(1-Anti.grd[:]/100);R0A.V.oname='R0A';
 											# R0V = R0.Clone();  R0V.V.name= 'R0V'; Task.AddFun (R0V);  R0V.grd[:] = R0V.grd[:]*(1-VacImm.grd[:]*effVacc/100); R0V.V.oname= 'R0V';
R0V=R0.Clone();R0V.V.name='R0V';Task.AddFun(R0V);R0V.grd[:]=R0V.grd[:]*(1-VacImm.grd[:]*effVacc/100);R0V.V.oname='R0V';
 											# R0AV = R0.Clone();  R0AV.V.name= 'R0AV'; Task.AddFun (R0AV);  R0AV.grd[:] = R0AV.grd[:]*(1-Im.grd[:]/100); R0AV.V.oname= 'R0AV';
R0AV=R0.Clone();R0AV.V.name='R0AV';Task.AddFun(R0AV);R0AV.grd[:]=R0AV.grd[:]*(1-Im.grd[:]/100);R0AV.V.oname='R0AV';
 											# month.V.dat[:] = .7;  month.grd[:] = 1; month.V.name=''; month.V.oname=''; month.V.draw_name=''; year.V.dat[:] = .7;  year.grd[:] = 1;
month.V.dat[:]=.7;month.grd[:]=1;month.V.name='';month.V.oname='';month.V.draw_name='';year.V.dat[:]=.7;year.grd[:]=1;
 											# today.V.dat[0] = .7;  today.V.dat[1] = 3; today.grd[:] = 1;  today.V.draw_name = 'Индекс Репродукции';
today.V.dat[0]=.7;today.V.dat[1]=3;today.grd[:]=1;today.V.draw_name='Индекс Репродукции';
 											# Draw R0AV;LC:g R0A;LC:r R0V;LC:b R0;LC:black month;LW:1;LC:black;LSt:dotted;MS:0;DC:black;DMS:5;DM:| year;DMS:12;LW:0 today;DLW:1;DC:y

Task.Draw (  'R0AV;LC:g R0A;LC:r R0V;LC:b R0;LC:black month;LW:1;LC:black;LSt:dotted;MS:0;DC:black;DMS:5;DM:| year;DMS:12;LW:0 today;DLW:1;DC:y' )
 											# today.V.dat[0] = -.5;  today.V.dat[1] = 11; month.V.dat[:] = -.2;  year.V.dat[:] = -0.2; today.V.oname = 'Тесты/1000';
today.V.dat[0]=-.5;today.V.dat[1]=11;month.V.dat[:]=-.2;year.V.dat[:]=-0.2;today.V.oname='Тесты/1000';
 											# draw nT month;LW:0;MS:0;DC:black;DMS:5;DM:| year;DMS:12;LW:0 today;DLW:1;DC:y

Task.Draw (  'nT month;LW:0;MS:0;DC:black;DMS:5;DM:| year;DMS:12;LW:0 today;DLW:1;DC:y' )
 											# r = nC.Clone();  r.V.name= 'r'; r.V.dat = None; Task.AddFun (r);
r=nC.Clone();r.V.name='r';r.V.dat=None;Task.AddFun(r);
 											# month.V.name = ''
month.V.name=''
Task.AddDef('month.V.name',[''])
 											# for i in t.NodS :
for i in t.NodS:
 											#     if i <= 4 : r.grd[i] = 30
    if i<= 4:r.grd[i]=30
 											#     else :      r.grd[i] = (nC.grd[i]-nC.grd[i-1])/nC.grd[i-1]*100
    else:r.grd[i]=(nC.grd[i]-nC.grd[i-1])/nC.grd[i-1]*100
 											# #    else :      r.grd[i] = (N.grd[i]-N.grd[i-1])/N.grd[i-1]*100
 											# month.V.dat[:] = -6;   month.grd[:] = 0;  year.V.dat[:] = -6;
month.V.dat[:]=-6;month.grd[:]=0;year.V.dat[:]=-6;
 											# today.V.dat[0] = -6;  today.V.dat[1] = 30;
today.V.dat[0]=-6;today.V.dat[1]=30;
 											# #print ('PPP', year.A[0].dat[1])
 											# Draw r;LC:r  month;LW:1;LC:black;LSt:dotted;MS:0;DC:black;DMS:5;DM:| year;DMS:12;LW:0 today;DLW:1;DC:y

Task.Draw (  'r;LC:r month;LW:1;LC:black;LSt:dotted;MS:0;DC:black;DMS:5;DM:| year;DMS:12;LW:0 today;DLW:1;DC:y' )
 											# month.V.dat[:] = .0;  month.grd[:] = .0;  year.V.dat[:] = .0;  year.grd[:] = 0;
month.V.dat[:]=.0;month.grd[:]=.0;year.V.dat[:]=.0;year.grd[:]=0;
 											# Draw month;LW:0;MS:0;DC:black;DMS:5;DM:| year;DMS:12;LW:0 IS;LC:g;LW:2

Task.Draw (  'month;LW:0;MS:0;DC:black;DMS:5;DM:| year;DMS:12;LW:0 IS;LC:g;LW:2' )
 											# nC_N = nC.Clone();  nC_N.V.name= 'nC_N'; nC_N.V.dat = None; Task.AddFun (nC_N);  nC_N.Divide(N);  nC_N.Mult(100);  nC_N.V.oname = '% Выявленных'
nC_N=nC.Clone();nC_N.V.name='nC_N';nC_N.V.dat=None;Task.AddFun(nC_N);nC_N.Divide(N);nC_N.Mult(100);nC_N.V.oname='%Выявленных'
 											# Draw month;LW:0;MS:0;DC:black;DMS:5;DM:| year;DMS:12;LW:0 nC_N;LC:g;LW:2

Task.Draw (  'month;LW:0;MS:0;DC:black;DMS:5;DM:| year;DMS:12;LW:0 nC_N;LC:g;LW:2' )
 											# Draw

Task.Draw (  '' )
 											# EOF