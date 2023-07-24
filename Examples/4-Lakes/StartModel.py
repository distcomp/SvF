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
SvF.mngF = 'MNG.odt'
SvF.CVNumOfIter = 0
SvF.RunMode = 'P&S'
latNik=69.413;lonNik=30.234
latZap=69.425;lonZap=30.822
AzimutInit(latZap,lonZap)
rmax=170
minR=7
rStep=5
StartYear=1946
EndYear=2030
StartZap=1956
Snow=0.6
notSnow=1-Snow
R=Grid('R',0.0,rmax,rStep,'i__R','R')
R1=Grid('R1',rStep,rmax,rStep,'i__R1','R1')
T=Grid('T',StartYear,EndYear,1.0,'i__T','T')
T9=Grid('T9',StartYear,2009.0,1.0,'i__T9','T9')
Tpro=Grid('Tpro',2020.0,EndYear,1.0,'i__Tpro','Tpro')
TZap0=Grid('TZap0',StartYear,StartZap,1.0,'i__TZap0','TZap0')
Fi=Grid('Fi',-180.0,180.0,10.0,'i__Fi','Fi')
t2010_2014=Grid('t2010_2014',2010.0,2014.0,1.0,'i__t2010_2014','t2010_2014')
t2016_2019=Grid('t2016_2019',2016.0,2019.0,1.0,'i__t2016_2019','t2016_2019')
t2022_2030=Grid('t2022_2030',2022.0,2030.0,1.0,'i__t2022_2030','t2022_2030')
EMS2a = Table ( '2Source2030.xlsx','EMS2a','Year as T,NiNi as NikZap' )
NikZap = Fun('NikZap',[T],False,-1,1, '') 
def fNikZap(T) : return NikZap.F([T])
Nik = Fun('Nik',[T],False,-1,1, '') 
def fNik(T) : return Nik.F([T])
Zap = Fun('Zap',[T],False,-1,1, '') 
def fZap(T) : return Zap.F([T])
xyNik=LatLonToAzimut(latNik,lonNik)
def fiNik(X,Y):return degrees(arctan2(Y-xyNik[1],X-xyNik[0]))
def rNik(X,Y):return sqrt((Y-xyNik[1])**2+(X-xyNik[0])**2)
xyZap=LatLonToAzimut(latZap,lonZap)
def fiZap(X,Y):return degrees(arctan2(Y-xyZap[1],X-xyZap[0]))
def rZap(X,Y):return sqrt((Y-xyZap[1])**2+(X-xyZap[0])**2)
Soluble = Fun('Soluble',[R],False,-1,1, '') 
def fSoluble(R) : return Soluble.F([R])
Table ( 'NikRosePol37(Fi).sol','curentTabl','Fi,RosePol AS PfiNik' )
PfiNik = Fun('PfiNik',[Fi],False,-1,1, '') 
def fPfiNik(Fi) : return PfiNik.F([Fi])
P_RNik = Fun('P_RNik',[R],False,-1,1, '') 
def fP_RNik(R) : return P_RNik.F([R])
def DEPOSITNik(X,Y,i__T):return fPfiNik(fiNik(X,Y))*fP_RNik(rNik(X,Y))*fNik(i__T)*1000
def DEPOSITsolNik(X,Y,i__T):return DEPOSITNik(X,Y,i__T)*fSoluble(rNik(X,Y))
def DEPOSITinsolNik(X,Y,i__T):return DEPOSITNik(X,Y,i__T)*(1-fSoluble(rNik(X,Y)))
Table ( 'ZapRosePol37(Fi).sol','curentTabl','Fi,RosePol AS PfiZap' )
PfiZap = Fun('PfiZap',[Fi],False,-1,1, '') 
def fPfiZap(Fi) : return PfiZap.F([Fi])
P_RZap = Fun('P_RZap',[R],False,-1,1, '') 
def fP_RZap(R) : return P_RZap.F([R])
def DEPOSITZap(X,Y,i__T):return fPfiZap(fiZap(X,Y))*fP_RZap(rZap(X,Y))*fZap(i__T)*1000
def DEPOSITsolZap(X,Y,i__T):return DEPOSITZap(X,Y,i__T)*fSoluble(rZap(X,Y))
def DEPOSITinsolZap(X,Y,i__T):return DEPOSITZap(X,Y,i__T)*(1-fSoluble(rZap(X,Y)))
def DEPOSIT(X,Y,i__T):return DEPOSITNik(X,Y,i__T)+DEPOSITZap(X,Y,i__T)
def DEPOSITsol(X,Y,i__T):return DEPOSITsolNik(X,Y,i__T)+DEPOSITsolZap(X,Y,i__T)
def DEPOSITinsol(X,Y,i__T):return DEPOSITinsolNik(X,Y,i__T)+DEPOSITinsolZap(X,Y,i__T)
CONS = Table ( 'CONS.txt','CONS','*' )
b=Grid('b',0.0,CONS.NoR-1,1.0,'i__b','b')
t=Grid('t',StartYear,EndYear,1.0,'i__t','t')
X = Fun('X',[b],True,-1,1, '') 
def fX(b) : return X.F([b])
Y = Fun('Y',[b],True,-1,1, '') 
def fY(b) : return Y.F([b])
Catch = Fun('Catch',[b],True,-1,1, '') 
def fCatch(b) : return Catch.F([b])
S = Fun('S',[b],True,-1,1, '') 
def fS(b) : return S.F([b])
fonNiSoil=20
sNi = Fun('sNi',[b,t],False,-1,1, '') 
def fsNi(b,t) : return sNi.F([b,t])
leaching = Fun('leaching',[],False,-1,1, '') 
leaching.grd = 1
def fleaching() : return leaching.F([])
precip=0.4
wNi = Fun('wNi',[b,t],False,-1,1, '') 
def fwNi(b,t) : return wNi.F([b,t])
H = Fun('H',[],False,-1,1, '') 
H.grd = 1
def fH() : return H.F([])
fonNiSedi=20
bNi = Fun('bNi',[b,t],False,-1,1, '') 
def fbNi(b,t) : return bNi.F([b,t])
TDep = Table ( 'TDep.txt','TDep','*' )
nD=Grid('nD',SvF.curentTabl.dat('nD')[:].min(),SvF.curentTabl.dat('nD')[:].max(),1.0,'i__nD','nD')
bD = Fun('bD',[nD],True,-1,1, '') 
def fbD(nD) : return bD.F([nD])
TD = Fun('TD',[nD],True,-1,1, '') 
def fTD(nD) : return TD.F([nD])
depNi = Fun('depNi',[nD],False,-1,1, '') 
def fdepNi(nD) : return depNi.F([nD])
Soil = Table ( 'Soil.txt','Soil','*' )
hSoil = Fun('hSoil',[],False,-1,1, '') 
hSoil.grd = 1
def fhSoil() : return hSoil.F([])
nS=Grid('nS',SvF.curentTabl.dat('nS')[:].min(),SvF.curentTabl.dat('nS')[:].max(),1.0,'i__nS','nS')
bS = Fun('bS',[nS],True,-1,1, '') 
def fbS(nS) : return bS.F([nS])
tS = Fun('tS',[nS],True,-1,1, '') 
def ftS(nS) : return tS.F([nS])
soilNi = Fun('soilNi',[nS],False,-1,1, '') 
def fsoilNi(nS) : return soilNi.F([nS])
FonSoilNi = Fun('FonSoilNi',[nS],False,-1,1, '') 
def fFonSoilNi(nS) : return FonSoilNi.F([nS])
TBott = Table ( 'TBott.txt','TBott','*' )
nB=Grid('nB',SvF.curentTabl.dat('nB')[:].min(),SvF.curentTabl.dat('nB')[:].max(),1.0,'i__nB','nB')
bB = Fun('bB',[nB],True,-1,1, '') 
def fbB(nB) : return bB.F([nB])
tB = Fun('tB',[nB],True,-1,1, '') 
def ftB(nB) : return tB.F([nB])
Vsedim = Fun('Vsedim',[nB],True,-1,1, '') 
def fVsedim(nB) : return Vsedim.F([nB])
delT = Fun('delT',[nB],True,-1,1, '') 
def fdelT(nB) : return delT.F([nB])
botNi = Fun('botNi',[nB],False,-1,1, '') 
def fbotNi(nB) : return botNi.F([nB])
TSedAcc = Table ( 'TSedAcc.txt','TSedAcc','*' )
nSA=Grid('nSA',SvF.curentTabl.dat('nSA')[:].min(),SvF.curentTabl.dat('nSA')[:].max(),1.0,'i__nSA','nSA')
bSA = Fun('bSA',[nSA],True,-1,1, '') 
def fbSA(nSA) : return bSA.F([nSA])
Tsa = Fun('Tsa',[nSA],True,-1,1, '') 
def fTsa(nSA) : return Tsa.F([nSA])
sedaccNi = Fun('sedaccNi',[nSA],False,-1,1, '') 
def fsedaccNi(nSA) : return sedaccNi.F([nSA])
multNumSA=Grid('multNumSA',SvF.curentTabl.dat('multNumSA')[:].min(),SvF.curentTabl.dat('multNumSA')[:].max(),1.0,'i__multNumSA','multNumSA')
multSA = Fun('multSA',[multNumSA],False,-1,1, '') 
def fmultSA(multNumSA) : return multSA.F([multNumSA])
multNumSA = Fun('multNumSA',[nSA],True,-1,1, '') 
def fmultNumSA(nSA) : return multNumSA.F([nSA])
Water = Table ( 'Water.txt','Water','*' )
nW=Grid('nW',SvF.curentTabl.dat('nW')[:].min(),SvF.curentTabl.dat('nW')[:].max(),1.0,'i__nW','nW')
bW = Fun('bW',[nW],True,-1,1, '') 
def fbW(nW) : return bW.F([nW])
tW = Fun('tW',[nW],True,-1,1, '') 
def ftW(nW) : return tW.F([nW])
waterNi = Fun('waterNi',[nW],False,-1,1, '') 
def fwaterNi(nW) : return waterNi.F([nW])
SvF_MakeSets_byParam ( SvF.curentTabl.dat('bW'), 7 )
Task.ReadSols()
Year=Grid('Year',StartYear,EndYear,1.0,'i__Year','Year')
def where_condition ( Ni, bB, Year ):
    return (bB==9)
TBott = Table ( 'TBott.txt','TBott','botNi as Ni,bB,tB as Year',where_condition )
Ni = Fun('Ni',[Year],True,-1,1, '') 
def fNi(Year) : return Ni.F([Year])
for tt in t.NodS:
    Ni.grd[tt]=bNi.grd[9,tt]/(1.7*0.25)*0.55
Task.Draw ( 'Ni;Transp' )
Task.Draw ( 'botNi' )
Task.Draw ( 'Soluble' )
SvF.Xsize=8
SvF.Ylabel_x=0.13
NikZap.V.oname = 'Ni - модель'; NikZap.V.data_name = 'Ni - данные'; NikZap.V.draw_name = 'Выбросы Ni, т/год'; NikZap.A[0].oname = 'Годы';
Task.Draw ( 'NikZap;LW:1.5;MS:0' )
SQUARE=sum(Catch.grd[int(ib)]for ib in b.NodS)
S_Lakes=sum(S.grd[int(ib)]for ib in b.NodS)
print(len(b.NodS),'n sum SQUARE',SQUARE,' sum S_Lakes',S_Lakes)
S_DEPOSITION = Fun('S_DEPOSITION',[T],True,-1,1, '') 
def fS_DEPOSITION(T) : return S_DEPOSITION.F([T])
A_DEPOSITION = Fun('A_DEPOSITION',[T],True,-1,1, '') 
def fA_DEPOSITION(T) : return A_DEPOSITION.F([T])
S_SOIL = Fun('S_SOIL',[T],True,-1,1, '') 
def fS_SOIL(T) : return S_SOIL.F([T])
A_SOIL = Fun('A_SOIL',[T],True,-1,1, '') 
def fA_SOIL(T) : return A_SOIL.F([T])
M_SOIL = Fun('M_SOIL',[T],True,-1,1, '') 
def fM_SOIL(T) : return M_SOIL.F([T])
S_SEDIMENTION = Fun('S_SEDIMENTION',[T],True,-1,1, '') 
def fS_SEDIMENTION(T) : return S_SEDIMENTION.F([T])
A_SEDIMENTION = Fun('A_SEDIMENTION',[T],True,-1,1, '') 
def fA_SEDIMENTION(T) : return A_SEDIMENTION.F([T])
S_WATER = Fun('S_WATER',[T],True,-1,1, '') 
def fS_WATER(T) : return S_WATER.F([T])
A_WATER = Fun('A_WATER',[T],True,-1,1, '') 
def fA_WATER(T) : return A_WATER.F([T])
M_WATER = Fun('M_WATER',[T],True,-1,1, '') 
def fM_WATER(T) : return M_WATER.F([T])
S_OUT = Fun('S_OUT',[T],True,-1,1, '') 
def fS_OUT(T) : return S_OUT.F([T])
A_OUT = Fun('A_OUT',[T],True,-1,1, '') 
def fA_OUT(T) : return A_OUT.F([T])
for it in T.NodS:
    i__t=T.Val[it]
    S_DEPOSITION.grd[it]=sum(DEPOSIT(X.grd[ib],Y.grd[ib],i__t)*Catch.grd[ib]for ib in b.NodS)/SQUARE
    S_SOIL.grd[it]=sum(DEPOSITinsol(X.grd[ib],Y.grd[ib],i__t)*(Catch.grd[ib]-S.grd[ib])*notSnow for ib in b.NodS)/SQUARE
    S_SEDIMENTION.grd[it]=sum(DEPOSITinsol(X.grd[ib],Y.grd[ib],i__t)*(S.grd[ib]+(Catch.grd[ib]-S.grd[ib])*Snow)for ib in b.NodS)/SQUARE
    S_WATER.grd[it]=sum(DEPOSITsol(X.grd[ib],Y.grd[ib],i__t)*(Catch.grd[ib])for ib in b.NodS)/SQUARE
    S_OUT.grd[it]=sum(wNi.grd[ib,it]*precip*(Catch.grd[ib])for ib in b.NodS)/SQUARE
    if it==0:
        A_DEPOSITION.grd[it]=S_DEPOSITION.grd[it]
        A_SEDIMENTION.grd[it]=S_SEDIMENTION.grd[it]
        A_OUT.grd[it]=S_OUT.grd[it]
    else:
        A_DEPOSITION.grd[it]=S_DEPOSITION.grd[it]+A_DEPOSITION.grd[it-1]
        A_SEDIMENTION.grd[it]=S_SEDIMENTION.grd[it]+A_SEDIMENTION.grd[it-1]
        A_OUT.grd[it]=S_OUT.grd[it]+A_OUT.grd[it-1]
    A_SOIL.grd[it]=sum(sNi.grd[ib,it]*(Catch.grd[ib]-S.grd[ib])for ib in b.NodS)/SQUARE
    M_SOIL.grd[it]=sum(sNi.grd[ib,it]*(Catch.grd[ib]-S.grd[ib])for ib in b.NodS)/SQUARE/(800*fhSoil())
    A_WATER.grd[it]=sum(wNi.grd[ib,it]*S.grd[ib]for ib in b.NodS)/S_Lakes*(fH()+precip)
    M_WATER.grd[it]=sum(wNi.grd[ib,it]*S.grd[ib]for ib in b.NodS)/S_Lakes
A_SOIL.grd[:]-=A_SOIL.grd[0]
SvF.Ylabel_x=0.35
S_WATER.V.oname='вода';S_DEPOSITION.V.oname='всего';S_SOIL.V.oname='почва';S_SEDIMENTION.V.oname='донные отложения'
S_SOIL.V.draw_name = 'Распределение выпадения Ni, мг/м2/год'; S_SOIL.A[0].oname = 'Годы';
Task.Draw ( 'S_DEPOSITION;MS:0;LW:1.5 S_SEDIMENTION;LC:black;LSt:dotted S_WATER;LC:b;LSt:dashdot S_SOIL;LC:brown;LSt:dashed' )
SvF.Ylabel_x=0.2
A_WATER.V.oname='вода';A_DEPOSITION.V.oname='всего';A_SOIL.V.oname='почва';A_SEDIMENTION.V.oname='донные отложения';A_OUT.V.oname='потери со стоком'
A_WATER.V.draw_name = 'Баланс накопления Ni, мг/м2'; A_WATER.A[0].oname = 'Годы';
Task.Draw ( 'A_DEPOSITION;MS:0;LW:1.5 A_SEDIMENTION;LC:black;LSt:dotted A_OUT;LC:green;LSt:solid;MS:3;LW:1 A_SOIL;LC:brown;LSt:dashed;MS:0;LW:1.5 A_WATER;LC:b;LSt:dashdot' )
SvF.Ylabel_x=0.25
M_WATER.V.draw_name = 'Концентрация Ni, мг/м2 в воде'; M_WATER.A[0].oname = 'Годы'; M_WATER.V.oname ='вода';
Task.Draw ( 'M_WATER;LC:b;LSt:dashdot;LW:1.5;MS:0' )
SvF.Ylabel_x=0.35
M_SOIL.V.draw_name = 'Концентрация Ni, мг/кг(сух.веса) в почве'; M_SOIL.A[0].oname = 'Годы'; M_SOIL.V.oname ='почва';
Task.Draw ( 'M_SOIL;LC:brown;LSt:dashed;LW:1.5;MS:0' )
Task.Draw ( 'P_RZap P_RNik' )
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
TP68 = Table ( 'P68.txt','TP68','*' )
xx,yy=LatLonToAzimut(TP68.dat('Y')[:],TP68.dat('X')[:])
P68=Polyline(xx,yy,None,'P68')
TP69 = Table ( 'P69.txt','TP69','*' )
xx,yy=LatLonToAzimut(TP69.dat('Y')[:],TP69.dat('X')[:])
P69=Polyline(xx,yy,None,'P69')
TP70 = Table ( 'P70.txt','TP70','*' )
xx,yy=LatLonToAzimut(TP70.dat('Y')[:],TP70.dat('X')[:])
P70=Polyline(xx,yy,None,'P70')
TMERID = Table ( 'MERID.txt','TMERID','*' )
xx,yy=LatLonToAzimut(TMERID.dat('Y')[:],TMERID.dat('X')[:])
MERID=Polyline(xx,yy,None,'MERID')
Lakes=Polyline(Water.dat('X')[:],Water.dat('Y')[:],None,'Lakes')
Depos=Polyline(TDep.dat('X')[:],TDep.dat('Y')[:],None,'Depos')
TBott = Table ( 'TBott.txt','TBott','*' )
Bott=Polyline(TBott.dat('X')[:],TBott.dat('Y')[:],None,'Bott')
SedAcc=Polyline(TSedAcc.dat('X')[:],TSedAcc.dat('Y')[:],None,'SedAcc')
PSoil=Polyline(Soil.dat('X')[:],Soil.dat('Y')[:],None,'PSoil')
SvF.Legend=False
SvF.X_lim=[-110,110]
SvF.Y_lim=[-110,80]
Task.Draw ( 'P68;LC:gray;LW:1;MS:0;LSt:dotted P69;MS:0 P70;MS:0 MERID Shore;LC:blue;LW:1;MS:0;LSt:solid Brus;LC:red;MS:0 Bnor_fin;LC:red;MS:0 Town;MS:6;LW:0;MC:red;MEW:2;MEC:black Lakes;MC:w;LW:0;MS:7;MEW:1;MEC:blue Depos;MC:w;LC:w;MS:6;M:s;MEW:1;MEC:black Bott;M:^;MS:6;MEC:r SedAcc PSoil;MC:g;M:X;MS:9;MEW:1;MEC:w' )
X=Grid('X',-100.0,100.0,2.0,'i__X','X')
Y=Grid('Y',-100.0,100.0,2.0,'i__Y','Y')
SvF.curentTabl=None
pPOL = Fun('pPOL',[X,Y],True,-1,1, '') 
def fpPOL(X,Y) : return pPOL.F([X,Y])
SoilXY = Fun('SoilXY',[X,Y],True,-1,1, '') 
def fSoilXY(X,Y) : return SoilXY.F([X,Y])
WaterXY = Fun('WaterXY',[X,Y],True,-1,1, '') 
def fWaterXY(X,Y) : return WaterXY.F([X,Y])
SoilXY.grd[:,:]=fonNiSoil
WaterXY.grd[:,:]=1
SvF.DataMarkerSize = 2
SvF.Ylabel_x=0.05
SvF.Xlabel_x=0.96
SvF.Ylabel_y=0.90
SvF.Xlabel_y=0.07
SvF.X_lim=[-100,100]
SvF.Y_lim=[-100,100]
SvF.xaxis_step=50
SvF.yaxis_step=50
SvF.Xsize=5.
SvF.Ysize=4.1
SvF.Legend=True
from matplotlib import ticker
SvF.locator=ticker.LogLocator(base=2.0)
for i__t in range(1946,2031,1):
  for x in X.NodS:
    for y in Y.NodS:
        xv=X.Val[x]
        yv=Y.Val[y]
        dNik=rNik(xv,yv)
        dZap=rZap(xv,yv)
        Dep=0
        DepInsol=0
        DepSol=0
        if dNik<rmax:
            Dep+=DEPOSITNik(xv,yv,i__t)
            DepInsol+=DEPOSITinsolNik(xv,yv,i__t)
            DepSol+=DEPOSITsolNik(xv,yv,i__t)
        if dZap<rmax:
            Dep+=DEPOSITZap(xv,yv,i__t)
            DepInsol+=DEPOSITinsolZap(xv,yv,i__t)
            DepSol+=DEPOSITsolZap(xv,yv,i__t)
        pPOL.grd[x,y]=Dep
        SoilXY.grd[x,y]+=(DepInsol*notSnow-leaching.grd*SoilXY.grd[x,y]*800*fhSoil())/(800*fhSoil())
        WaterXY.grd[x,y]+=(DepSol+fleaching()*SoilXY.grd[x,y]*15-precip*WaterXY.grd[x,y])/(fH()+precip)
  if i__t in[1980,2005,2018,2030]:
      pPOL.V.draw_name=''
      SoilXY.V.draw_name=' '
      WaterXY.V.draw_name='Ni в воде, мг/м2 '+str(i__t)
      print(i__t)
      Task.Draw ( 'pPOL;L:1,2,4,8,16,32,64,128,9999;MS:0 P68;LC:gray;LW:1;MS:0;LSt:dotted P69;MS:0 P70;MS:0 MERID Shore;LC:blue;LW:1;MS:0;LSt:solid Brus;LC:red;MS:0 Bnor_fin;LC:red;MS:0 Town;MS:6;LW:0;MC:red;MEW:2;MEC:black' )
      Task.Draw ( 'SoilXY;L:25,50,100,200,1000,9999;MS:0 P68;LC:gray;LW:1;MS:0;LSt:dotted P69;MS:0 P70;MS:0 MERID Shore;LC:blue;LW:1;MS:0;LSt:solid Brus;LC:red;MS:0 Bnor_fin;LC:red;MS:0 Town;MS:6;LW:0;MC:red;MEW:2;MEC:black' )
      Task.Draw ( 'WaterXY;L:1,3,10,30,100,300,1000,3000;MS:0 P68;LC:gray;LW:1;MS:0;LSt:dotted P69;MS:0 P70;MS:0 MERID Shore;LC:blue;LW:1;MS:0;LSt:solid Brus;LC:red;MS:0 Bnor_fin;LC:red;MS:0 Town;MS:6;LW:0;MC:red;MEW:2;MEC:black Lakes;MC:w;LW:0;MS:6;MEW:1;MEC:blue' )