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
SvF.mngF = '3Body3D.mng'
currentTab = Table ( '3Body3D.dat','currentTab','t,xNoisy1 as x1,yNoisy1 as y1,zNoisy1 as z1,xNoisy2 as x2,yNoisy2 as y2,zNoisy2 as z2,xNoisy3 as x3,yNoisy3 as y3,zNoisy3 as z3' )
t = Set('t',SvF.currentTab.dat('t')[:].min(),SvF.currentTab.dat('t')[:].max(),0.01,'','t')
r = Set('r',0.5,5.0,0.1,'','r')
x1 = Fun('x1',[t])
def fx1(t) : return x1.F([t])
y1 = Fun('y1',[t])
def fy1(t) : return y1.F([t])
z1 = Fun('z1',[t])
def fz1(t) : return z1.F([t])
x2 = Fun('x2',[t])
def fx2(t) : return x2.F([t])
y2 = Fun('y2',[t])
def fy2(t) : return y2.F([t])
z2 = Fun('z2',[t])
def fz2(t) : return z2.F([t])
x3 = Fun('x3',[t])
def fx3(t) : return x3.F([t])
y3 = Fun('y3',[t])
def fy3(t) : return y3.F([t])
z3 = Fun('z3',[t])
def fz3(t) : return z3.F([t])
G_const=1
m1 = Tensor('m1',[])
def fm1() : return m1.F([])
m2 = Tensor('m2',[])
def fm2() : return m2.F([])
m3 = Tensor('m3',[])
def fm3() : return m3.F([])
fr = smbFun('fr',[r])
def ffr(r) : return fr.F([r])
c_fr = Tensor('c_fr',[9])
def fc_fr(i) : return c_fr.F([i])
def fr_smbF00(Args) :
   r = Args[0]
   SvF.F_Arg_Type = "N"
   ret =  ( fc_fr(0)+fc_fr(1)*r+fc_fr(2)*r**2+fc_fr(3)*r**3+fc_fr(4)*r**4+fc_fr(5)*r**5+fc_fr(6)*r**6+fc_fr(7)*r**7+fc_fr(8)*r**8 ) 
   SvF.F_Arg_Type = ""
   return ret
fr.smbF = fr_smbF00
r12 = smbFun('r12',[t], ArgNorm=False)
def fr12(t) : return r12.F([t])
def r12_smbF00(Args) :
   t = Args[0]
   ret = py.sqrt((fx2(t)-fx1(t))**2+(fy2(t)-fy1(t))**2+(fz2(t)-fz1(t))**2)
   return ret
r12.smbF = r12_smbF00
r13 = smbFun('r13',[t], ArgNorm=False)
def fr13(t) : return r13.F([t])
def r13_smbF00(Args) :
   t = Args[0]
   ret = py.sqrt((fx3(t)-fx1(t))**2+(fy3(t)-fy1(t))**2+(fz3(t)-fz1(t))**2)
   return ret
r13.smbF = r13_smbF00
r23 = smbFun('r23',[t], ArgNorm=False)
def fr23(t) : return r23.F([t])
def r23_smbF00(Args) :
   t = Args[0]
   ret = py.sqrt((fx3(t)-fx2(t))**2+(fy3(t)-fy2(t))**2+(fz3(t)-fz2(t))**2)
   return ret
r23.smbF = r23_smbF00
CVmakeSets (  CV_NumSets=5 )
SvF.CVNumOfIter=0; SvF.RunMode="L&S"; 
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    x1.var = py.Var ( x1.A[0].NodS,domain=Reals )
    x1.gr =  x1.var
    Gr.x1 =  x1.var

    y1.var = py.Var ( y1.A[0].NodS,domain=Reals )
    y1.gr =  y1.var
    Gr.y1 =  y1.var

    z1.var = py.Var ( z1.A[0].NodS,domain=Reals )
    z1.gr =  z1.var
    Gr.z1 =  z1.var

    x2.var = py.Var ( x2.A[0].NodS,domain=Reals )
    x2.gr =  x2.var
    Gr.x2 =  x2.var

    y2.var = py.Var ( y2.A[0].NodS,domain=Reals )
    y2.gr =  y2.var
    Gr.y2 =  y2.var

    z2.var = py.Var ( z2.A[0].NodS,domain=Reals )
    z2.gr =  z2.var
    Gr.z2 =  z2.var

    x3.var = py.Var ( x3.A[0].NodS,domain=Reals )
    x3.gr =  x3.var
    Gr.x3 =  x3.var

    y3.var = py.Var ( y3.A[0].NodS,domain=Reals )
    y3.gr =  y3.var
    Gr.y3 =  y3.var

    z3.var = py.Var ( z3.A[0].NodS,domain=Reals )
    z3.gr =  z3.var
    Gr.z3 =  z3.var

    m1.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    m1.gr =  m1.var
    Gr.m1 =  m1.var

    m2.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    m2.gr =  m2.var
    Gr.m2 =  m2.var

    m3.var = py.Var ( range (1), domain=Reals, bounds=(0,None) )
    m3.gr =  m3.var
    Gr.m3 =  m3.var

    c_fr.var = py.Var ( range (c_fr.Sizes[0]),domain=Reals )
    c_fr.gr =  c_fr.var
    Gr.c_fr =  c_fr.var
 								# fr(r)>=0
    def EQ0 (Gr,_ir) :
        return (
          ffr(_ir)>=0
        )
    Gr.conEQ0 = py.Constraint(r.FlNodS,rule=EQ0 )
 								# fr(1.)=1.
    def EQ1 (Gr) :
        return (
          ffr(1.)==1.
        )
    Gr.conEQ1 = py.Constraint(rule=EQ1 )
 								# fr'<0
    def EQ2 (Gr,_ir) :
        return (
          fr.by_x(_ir)<=0
        )
    Gr.conEQ2 = py.Constraint(r.FlNodSm,rule=EQ2 )
 								# x1''=G_const*m2*fr(r12(t))*(x2-x1)/r12(t)+G_const*m3*fr(r13(t))*(x3-x1)/r13(t)
    def EQ3 (Gr,_it) :
        return (
          x1.by_xx(_it)==G_const*fm2()*ffr(fr12(_it))*(fx2(_it)-fx1(_it))/fr12(_it)+G_const*fm3()*ffr(fr13(_it))*(fx3(_it)-fx1(_it))/fr13(_it)
        )
    Gr.conEQ3 = py.Constraint(t.mFlNodSm,rule=EQ3 )
 								# y1''=G_const*m2*fr(r12(t))*(y2-y1)/r12(t)+G_const*m3*fr(r13(t))*(y3-y1)/r13(t)
    def EQ4 (Gr,_it) :
        return (
          y1.by_xx(_it)==G_const*fm2()*ffr(fr12(_it))*(fy2(_it)-fy1(_it))/fr12(_it)+G_const*fm3()*ffr(fr13(_it))*(fy3(_it)-fy1(_it))/fr13(_it)
        )
    Gr.conEQ4 = py.Constraint(t.mFlNodSm,rule=EQ4 )
 								# z1''=G_const*m2*fr(r12(t))*(z2-z1)/r12(t)+G_const*m3*fr(r13(t))*(z3-z1)/r13(t)
    def EQ5 (Gr,_it) :
        return (
          z1.by_xx(_it)==G_const*fm2()*ffr(fr12(_it))*(fz2(_it)-fz1(_it))/fr12(_it)+G_const*fm3()*ffr(fr13(_it))*(fz3(_it)-fz1(_it))/fr13(_it)
        )
    Gr.conEQ5 = py.Constraint(t.mFlNodSm,rule=EQ5 )
 								# x2''=G_const*m1*fr(r12(t))*(x1-x2)/r12(t)+G_const*m3*fr(r23(t))*(x3-x2)/r23(t)
    def EQ6 (Gr,_it) :
        return (
          x2.by_xx(_it)==G_const*fm1()*ffr(fr12(_it))*(fx1(_it)-fx2(_it))/fr12(_it)+G_const*fm3()*ffr(fr23(_it))*(fx3(_it)-fx2(_it))/fr23(_it)
        )
    Gr.conEQ6 = py.Constraint(t.mFlNodSm,rule=EQ6 )
 								# y2''=G_const*m1*fr(r12(t))*(y1-y2)/r12(t)+G_const*m3*fr(r23(t))*(y3-y2)/r23(t)
    def EQ7 (Gr,_it) :
        return (
          y2.by_xx(_it)==G_const*fm1()*ffr(fr12(_it))*(fy1(_it)-fy2(_it))/fr12(_it)+G_const*fm3()*ffr(fr23(_it))*(fy3(_it)-fy2(_it))/fr23(_it)
        )
    Gr.conEQ7 = py.Constraint(t.mFlNodSm,rule=EQ7 )
 								# z2''=G_const*m1*fr(r12(t))*(z1-z2)/r12(t)+G_const*m3*fr(r23(t))*(z3-z2)/r23(t)
    def EQ8 (Gr,_it) :
        return (
          z2.by_xx(_it)==G_const*fm1()*ffr(fr12(_it))*(fz1(_it)-fz2(_it))/fr12(_it)+G_const*fm3()*ffr(fr23(_it))*(fz3(_it)-fz2(_it))/fr23(_it)
        )
    Gr.conEQ8 = py.Constraint(t.mFlNodSm,rule=EQ8 )
 								# x3''=G_const*m1*fr(r13(t))*(x1-x3)/r13(t)+G_const*m2*fr(r23(t))*(x2-x3)/r23(t)
    def EQ9 (Gr,_it) :
        return (
          x3.by_xx(_it)==G_const*fm1()*ffr(fr13(_it))*(fx1(_it)-fx3(_it))/fr13(_it)+G_const*fm2()*ffr(fr23(_it))*(fx2(_it)-fx3(_it))/fr23(_it)
        )
    Gr.conEQ9 = py.Constraint(t.mFlNodSm,rule=EQ9 )
 								# y3''=G_const*m1*fr(r13(t))*(y1-y3)/r13(t)+G_const*m2*fr(r23(t))*(y2-y3)/r23(t)
    def EQ10 (Gr,_it) :
        return (
          y3.by_xx(_it)==G_const*fm1()*ffr(fr13(_it))*(fy1(_it)-fy3(_it))/fr13(_it)+G_const*fm2()*ffr(fr23(_it))*(fy2(_it)-fy3(_it))/fr23(_it)
        )
    Gr.conEQ10 = py.Constraint(t.mFlNodSm,rule=EQ10 )
 								# z3''=G_const*m1*fr(r13(t))*(z1-z3)/r13(t)+G_const*m2*fr(r23(t))*(z2-z3)/r23(t)
    def EQ11 (Gr,_it) :
        return (
          z3.by_xx(_it)==G_const*fm1()*ffr(fr13(_it))*(fz1(_it)-fz3(_it))/fr13(_it)+G_const*fm2()*ffr(fr23(_it))*(fz2(_it)-fz3(_it))/fr23(_it)
        )
    Gr.conEQ11 = py.Constraint(t.mFlNodSm,rule=EQ11 )

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('x1'))
    if x1.mu is None : x1.mu = Gr.mu0
    x1.ValidationSets = SvF.ValidationSets
    x1.notTrainingSets = SvF.notTrainingSets
    x1.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('y1'))
    if y1.mu is None : y1.mu = Gr.mu0
    y1.ValidationSets = SvF.ValidationSets
    y1.notTrainingSets = SvF.notTrainingSets
    y1.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('z1'))
    if z1.mu is None : z1.mu = Gr.mu0
    z1.ValidationSets = SvF.ValidationSets
    z1.notTrainingSets = SvF.notTrainingSets
    z1.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('x2'))
    if x2.mu is None : x2.mu = Gr.mu0
    x2.ValidationSets = SvF.ValidationSets
    x2.notTrainingSets = SvF.notTrainingSets
    x2.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('y2'))
    if y2.mu is None : y2.mu = Gr.mu0
    y2.ValidationSets = SvF.ValidationSets
    y2.notTrainingSets = SvF.notTrainingSets
    y2.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('z2'))
    if z2.mu is None : z2.mu = Gr.mu0
    z2.ValidationSets = SvF.ValidationSets
    z2.notTrainingSets = SvF.notTrainingSets
    z2.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('x3'))
    if x3.mu is None : x3.mu = Gr.mu0
    x3.ValidationSets = SvF.ValidationSets
    x3.notTrainingSets = SvF.notTrainingSets
    x3.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('y3'))
    if y3.mu is None : y3.mu = Gr.mu0
    y3.ValidationSets = SvF.ValidationSets
    y3.notTrainingSets = SvF.notTrainingSets
    y3.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('z3'))
    if z3.mu is None : z3.mu = Gr.mu0
    z3.ValidationSets = SvF.ValidationSets
    z3.notTrainingSets = SvF.notTrainingSets
    z3.TrainingSets = SvF.TrainingSets
 											# x1.MSD()+y1.MSD()+z1.MSD()+x2.MSD()+y2.MSD()+z2.MSD()+x3.MSD()+y3.MSD()+z3.MSD()+x1.Complexity([Penal[0]])+y1.Complexity([Penal[1]])+z1.Complexity([Penal[2]])+x2.Complexity([Penal[3]])+y2.Complexity([Penal[4]])+z2.Complexity([Penal[5]])+x3.Complexity([Penal[6]])+y3.Complexity([Penal[7]])+z3.Complexity([Penal[8]])+fr.Complexity([Penal[9]])
    def obj_expression(Gr):  
        return (
             x1.MSD()+y1.MSD()+z1.MSD()+x2.MSD()+y2.MSD()+z2.MSD()+x3.MSD()+y3.MSD()+z3.MSD()+x1.Complexity([Penal[0]])+y1.Complexity([Penal[1]])+z1.Complexity([Penal[2]])+x2.Complexity([Penal[3]])+y2.Complexity([Penal[4]])+z2.Complexity([Penal[5]])+x3.Complexity([Penal[6]])+y3.Complexity([Penal[7]])+z3.Complexity([Penal[8]])+fr.Complexity([Penal[9]])
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x1 = Task.Funs[0]

    y1 = Task.Funs[1]

    z1 = Task.Funs[2]

    x2 = Task.Funs[3]

    y2 = Task.Funs[4]

    z2 = Task.Funs[5]

    x3 = Task.Funs[6]

    y3 = Task.Funs[7]

    z3 = Task.Funs[8]

    fr = Task.Funs[12]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (x1.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx1.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx1.MSD() ='+ stmp+'\n')
    tmp = (y1.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty1.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty1.MSD() ='+ stmp+'\n')
    tmp = (z1.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tz1.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tz1.MSD() ='+ stmp+'\n')
    tmp = (x2.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx2.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx2.MSD() ='+ stmp+'\n')
    tmp = (y2.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty2.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty2.MSD() ='+ stmp+'\n')
    tmp = (z2.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tz2.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tz2.MSD() ='+ stmp+'\n')
    tmp = (x3.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx3.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx3.MSD() ='+ stmp+'\n')
    tmp = (y3.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty3.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty3.MSD() ='+ stmp+'\n')
    tmp = (z3.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tz3.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tz3.MSD() ='+ stmp+'\n')
    tmp = (x1.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx1.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx1.Complexity([Penal[0]]) ='+ stmp+'\n')
    tmp = (y1.Complexity([Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty1.Complexity([Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty1.Complexity([Penal[1]]) ='+ stmp+'\n')
    tmp = (z1.Complexity([Penal[2]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tz1.Complexity([Penal[2]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tz1.Complexity([Penal[2]]) ='+ stmp+'\n')
    tmp = (x2.Complexity([Penal[3]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx2.Complexity([Penal[3]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx2.Complexity([Penal[3]]) ='+ stmp+'\n')
    tmp = (y2.Complexity([Penal[4]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty2.Complexity([Penal[4]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty2.Complexity([Penal[4]]) ='+ stmp+'\n')
    tmp = (z2.Complexity([Penal[5]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tz2.Complexity([Penal[5]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tz2.Complexity([Penal[5]]) ='+ stmp+'\n')
    tmp = (x3.Complexity([Penal[6]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx3.Complexity([Penal[6]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx3.Complexity([Penal[6]]) ='+ stmp+'\n')
    tmp = (y3.Complexity([Penal[7]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\ty3.Complexity([Penal[7]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\ty3.Complexity([Penal[7]]) ='+ stmp+'\n')
    tmp = (z3.Complexity([Penal[8]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tz3.Complexity([Penal[8]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tz3.Complexity([Penal[8]]) ='+ stmp+'\n')
    tmp = (fr.Complexity([Penal[9]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tfr.Complexity([Penal[9]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tfr.Complexity([Penal[9]]) ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
Plot( [ [ x1], [y1], [z1] ] )
Plot( [ [ x2], [y2], [z2] ] )
Plot( [ [ x3], [y3], [z3] ] )
rev_fr = Fun('rev_fr',[r], param=True)
def frev_fr(r) : return rev_fr.F([r])
for nr in r.NodS:rev_fr.grd[nr]=1/(r.Val[nr])**2
Plot( [ [ rev_fr, 'label=1/r/r'], [fr, 'c=g', 'file=1_r_r'] ] )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")