
from __future__ import division
from  numpy import *

from Lego import *
from pyomo.environ import *

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = ConcreteModel()
    Task.Gr = Gr
    if com.CV_NoR > 0:
        Gr.mu = Param ( range(com.CV_NoR), mutable=True, initialize = 1 )

    Loc1 = Task.Grids[0]

    Loc2 = Task.Grids[1]

    uL2 = Task.Grids[2]

    Loc3 = Task.Grids[3]

    uL3 = Task.Grids[4]

    Loc4 = Task.Grids[5]

    uL4 = Task.Grids[6]

    Loc5 = Task.Grids[7]

    uL5 = Task.Grids[8]

    ta = Task.Grids[9]

    ta1 = Task.Grids[10]
 											# b(ta)= b(ta).sol;
    b = Funs[0];  b__f = b
    b__i = Funs[0].grd
    def fb(ta) : return b__f.F([ta])

    testS = Task.Grids[11]
 											# F(testS)>0;d/dtestS(F)>=0
    F = Funs[1];  F__f = F
    F__i = Var ( Funs[1].A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    F.var = F__i ; Gr.F =  F__i
    F.InitByData()
    def fF(testS) : return F__f.F([testS])
 											# d/dtestS(F)>=0
    def EQ23 (Gr,i__testS) :
        return (
          ((fF((i__testS+testS.step))-fF(i__testS))/testS.step)>=0
        )
    Gr.conEQ23 = Constraint(testS.FlNodSm,rule=EQ23 )

    t = Task.Grids[12]

    tp = Task.Grids[13]

    tPro = Task.Grids[14]

    t365 = Task.Grids[15]
 											# Vac(t)
    Vac = Funs[2];  Vac__f = Vac
    Vac__i = Funs[2].grd
    def fVac(t) : return Vac__f.F([t])
 											# Exch(t)
    Exch = Funs[3];  Exch__f = Exch
    Exch__i = Funs[3].grd
    def fExch(t) : return Exch__f.F([t])
 											# nCR(t)
    nCR = Funs[4];  nCR__f = nCR
    nCR__i = Funs[4].grd
    def fnCR(t) : return nCR__f.F([t])
 											# nT(t)
    nT = Funs[5];  nT__f = nT
    nT__i = Funs[5].grd
    def fnT(t) : return nT__f.F([t])
 											# dayVac(t)
    dayVac = Funs[6];  dayVac__f = dayVac
    dayVac__i = Funs[6].grd
    def fdayVac(t) : return dayVac__f.F([t])
 											# Mig(t)
    Mig = Funs[7];  Mig__f = Mig
    Mig__i = Var ( Funs[7].A[0].NodS,domain=Reals, initialize = 1 )
    Mig.var = Mig__i ; Gr.Mig =  Mig__i
    Mig.InitByData()
    def fMig(t) : return Mig__f.F([t])
 											# MigCoef>0.05;<0.2
    MigCoef = Funs[8];  MigCoef__f = MigCoef
    MigCoef__i = Var ( domain=Reals, bounds=(0.05,0.2), initialize = 1 )
    MigCoef.var = MigCoef__i ; Gr.MigCoef =  MigCoef__i
    MigCoef.InitByData()
    fMigCoef = MigCoef__i
 											# ActR>3;<4
    ActR = Funs[9];  ActR__f = ActR
    ActR__i = Var ( domain=Reals, bounds=(3,4), initialize = 1 )
    ActR.var = ActR__i ; Gr.ActR =  ActR__i
    ActR.InitByData()
    fActR = ActR__i
 											# nC(t)>=0
    nC = Funs[10];  nC__f = nC
    nC__i = Var ( Funs[10].A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    nC.var = nC__i ; Gr.nC =  nC__i
    nC.InitByData()
    def fnC(t) : return nC__f.F([t])
 											# n(t,ta)>=0;
    n = Funs[11];  n__f = n
    n__i = Var ( Funs[11].A[0].NodS,Funs[11].A[1].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    n.var = n__i ; Gr.n =  n__i
    n.InitByData()
    def fn(t,ta) : return n.F([t,ta])
 											# N(t)>=0;N=\intr(ta,dta*n(t,ta));N<1000000*0.30;
    N = Funs[12];  N__f = N
    N__i = Var ( Funs[12].A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    N.var = N__i ; Gr.N =  N__i
    N.InitByData()
    def fN(t) : return N__f.F([t])
 											# N=\intr(ta,dta*n(t,ta))
    def EQ24 (Gr,ti) :
        return (
          fN(ti)==sum ( ta.step*fn(ti,tai) for tai in myrange (0.0,tam-ta.step,ta.step) )
        )
    Gr.conEQ24 = Constraint(t.FlNodS,rule=EQ24 )
 											# N<1000000*0.30
    def EQ25 (Gr,ti) :
        return (
          fN(ti)<=1000000*0.30
        )
    Gr.conEQ25 = Constraint(t.FlNodS,rule=EQ25 )
 											# n0>= 0;
    n0 = Funs[13];  n0__f = n0
    n0__i = Var ( domain=Reals, bounds=(0,None), initialize = 1 )
    n0.var = n0__i ; Gr.n0 =  n0__i
    n0.InitByData()
    fn0 = n0__i
 											# np>0.75;<=0.8
    np = Funs[14];  np__f = np
    np__i = Var ( domain=Reals, bounds=(0.75,0.8), initialize = 1 )
    np.var = np__i ; Gr.np =  np__i
    np.InitByData()
    fnp = np__i
 											# R0(t)>=0;<=Imax;d/dLoc2(R0(Loc2))<0;d/duL2(R0(uL2))>0;d/dLoc3(R0(Loc3))<0;d/duL3(R0(uL3))>0;d/dLoc4(R0(Loc4))<0;d/duL4(R0(uL4))>0;d/dLoc5(R0(Loc5))<0;d/duL5(R0(uL5))>0;
    R0 = Funs[15];  R0__f = R0
    R0__i = Var ( Funs[15].A[0].NodS,domain=Reals, bounds=(0,Imax), initialize = 1 )
    R0.var = R0__i ; Gr.R0 =  R0__i
    R0.InitByData()
    def fR0(t) : return R0__f.F([t])
 											# d/dLoc2(R0(Loc2))<0
    def EQ26 (Gr,i__Loc2) :
        return (
          ((fR0((i__Loc2+Loc2.step))-fR0(i__Loc2))/Loc2.step)<=0
        )
    Gr.conEQ26 = Constraint(Loc2.FlNodSm,rule=EQ26 )
 											# d/duL2(R0(uL2))>0
    def EQ27 (Gr,i__uL2) :
        return (
          ((fR0((i__uL2+uL2.step))-fR0(i__uL2))/uL2.step)>=0
        )
    Gr.conEQ27 = Constraint(uL2.FlNodSm,rule=EQ27 )
 											# d/dLoc3(R0(Loc3))<0
    def EQ28 (Gr,i__Loc3) :
        return (
          ((fR0((i__Loc3+Loc3.step))-fR0(i__Loc3))/Loc3.step)<=0
        )
    Gr.conEQ28 = Constraint(Loc3.FlNodSm,rule=EQ28 )
 											# d/duL3(R0(uL3))>0
    def EQ29 (Gr,i__uL3) :
        return (
          ((fR0((i__uL3+uL3.step))-fR0(i__uL3))/uL3.step)>=0
        )
    Gr.conEQ29 = Constraint(uL3.FlNodSm,rule=EQ29 )
 											# d/dLoc4(R0(Loc4))<0
    def EQ30 (Gr,i__Loc4) :
        return (
          ((fR0((i__Loc4+Loc4.step))-fR0(i__Loc4))/Loc4.step)<=0
        )
    Gr.conEQ30 = Constraint(Loc4.FlNodSm,rule=EQ30 )
 											# d/duL4(R0(uL4))>0
    def EQ31 (Gr,i__uL4) :
        return (
          ((fR0((i__uL4+uL4.step))-fR0(i__uL4))/uL4.step)>=0
        )
    Gr.conEQ31 = Constraint(uL4.FlNodSm,rule=EQ31 )
 											# d/dLoc5(R0(Loc5))<0
    def EQ32 (Gr,i__Loc5) :
        return (
          ((fR0((i__Loc5+Loc5.step))-fR0(i__Loc5))/Loc5.step)<=0
        )
    Gr.conEQ32 = Constraint(Loc5.FlNodSm,rule=EQ32 )
 											# d/duL5(R0(uL5))>0
    def EQ33 (Gr,i__uL5) :
        return (
          ((fR0((i__uL5+uL5.step))-fR0(i__uL5))/uL5.step)>=0
        )
    Gr.conEQ33 = Constraint(uL5.FlNodSm,rule=EQ33 )
 											# IS(t)>=0;
    IS = Funs[16];  IS__f = IS
    IS__i = Var ( Funs[16].A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    IS.var = IS__i ; Gr.IS =  IS__i
    IS.InitByData()
    def fIS(t) : return IS__f.F([t])
 											# B(t)>=0;
    B = Funs[17];  B__f = B
    B__i = Var ( Funs[17].A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    B.var = B__i ; Gr.B =  B__i
    B.InitByData()
    def fB(t) : return B__f.F([t])
 											# Anti(t)>0;<1
    Anti = Funs[18];  Anti__f = Anti
    Anti__i = Var ( Funs[18].A[0].NodS,domain=Reals, bounds=(0,1), initialize = 1 )
    Anti.var = Anti__i ; Gr.Anti =  Anti__i
    Anti.InitByData()
    def fAnti(t) : return Anti__f.F([t])
 											# VacImm(t)>=0
    VacImm = Funs[19];  VacImm__f = VacImm
    VacImm__i = Var ( Funs[19].A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    VacImm.var = VacImm__i ; Gr.VacImm =  VacImm__i
    VacImm.InitByData()
    def fVacImm(t) : return VacImm__f.F([t])
 											# Imun(t365)=Imun(t365).sol
    Imun = Funs[20];  Imun__f = Imun
    Imun__i = Funs[20].grd
    def fImun(t365) : return Imun__f.F([t365])
 											# Vacc(t365)=Vacc(t365).sol
    Vacc = Funs[21];  Vacc__f = Vacc
    Vacc__i = Funs[21].grd
    def fVacc(t365) : return Vacc__f.F([t365])
 											# (n(t+st,ta1+st)-n(t,ta1))/st=-(IS(t)*b(ta1))*n(t,ta1)
    def EQ34 (Gr,tai,ti) :
        if not ( ti+st<= t.max) : return Constraint.Skip
        return (
          (fn(ti+st,tai+st)-fn(ti,tai))/st==-(fIS(ti)*fb(tai))*fn(ti,tai)
        )
    Gr.conEQ34 = Constraint(ta1.FlNodS,t.FlNodS,rule=EQ34 )
 											# B(t)=R0(t)*(1-Anti(t))*(1-VacImm(t))*\intr(ta,dta*b(ta)*n(t,ta))*(1.+Mig(t)/nC(t))
    def EQ35 (Gr,ti) :
        return (
          fB(ti)==fR0(ti)*(1-fAnti(ti))*(1-fVacImm(ti))*sum ( ta.step*fb(tai)*fn(ti,tai) for tai in myrange (0.0,tam-ta.step,ta.step) )*(1.+fMig(ti)/fnC(ti))
        )
    Gr.conEQ35 = Constraint(t.FlNodS,rule=EQ35 )
 											# n(tp,0)=B(tp-st)
    def EQ36 (Gr,tpi) :
        return (
          fn(tpi,0)==fB(tpi-st)
        )
    Gr.conEQ36 = Constraint(