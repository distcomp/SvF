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
SvF.mngF = 'MSD(Dreg11x11)+Curv(T):M=0.odt'
SvF.RunMode = 'P&P'
 											# CVNumOfIter = 0
SvF.CVNumOfIter = 0
 											# SchemeD1    = 'Backward'  #'Forward'  # Central
SvF.SchemeD1 = "Backward"
 											# Data = Select x, t, Terr as T, ROWNUM as npp from ../Exp3.dat
Data = Table ( '../Exp3.dat','Data','x,t,Terr as T,ROWNUM as npp' )
 											# SvF_MakeSets_byParam ( Data.npp, 8, 0 )
SvF_MakeSets_byParam(Data.dat('npp'),8,0)
 											# Set:    x  ∈ [0, 2, -40]
x=Grid('x',0.0,2.0,-40.0,'i__x','x')
 											#     t  ∈ [0, 5, -40]
t=Grid('t',0.0,5.0,-40.0,'i__t','t')
 											#     sT ∈ [20, 100, 5]
sT=Grid('sT',20.0,100.0,5.0,'i__sT','sT')
 											# Var:    T(x,t) >=0
T = Fun('T',[x,t],False,-1,1, '') 
def fT(x,t) : return T.F([x,t])
 											#     φ(x)   >=0
φ = Fun('φ',[x],False,-1,1, '') 
def fφ(x) : return φ.F([x])
 											#     l(t)   >=0
l = Fun('l',[t],False,-1,1, '') 
def fl(t) : return l.F([t])
 											#     r(t)   >=0
r = Fun('r',[t],False,-1,1, '') 
def fr(t) : return r.F([t])
 											#     K(sT)  >=0; <= 10; PolyPow = 7
K = pFun('K',[sT],False,7,1, '') 
def fK(sT) : return K.F([sT])
 											# EQ:             \frac{\partial}{\partial t}(T)= K(T)\cdot\frac{\partial ^2}{\partial x^2}(T) + \frac{\partial }{\partial T}(K(T)) \cdot( \frac{\partial }{\partial x}(T) ) ** 2
 											#     T(0,t) = l(t)
 											#     T(2,t) = r(t)
 											#     T(x,0) = φ(x)
 											# #EQ:    d/dt(T(x,t)) = K(T)*d2/dx2(T(x,t)) + d/dT(K(T))*(d/dx(T(x,t)))**2
 											# Obj:  T.ComplSig2( Penal[0],Penal[1] ) + T.MSD()from __future__ import division
from  numpy import *

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr
    if SvF.CV_NoR > 0:
        Gr.mu = py.Param ( range(SvF.CV_NoR), mutable=True, initialize = 1 )

    T.var = py.Var ( T.A[0].NodS,T.A[1].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    Gr.T =  T.var
    T.InitByData()
    def fT(x,t) : return T.F([x,t])

    φ.var = py.Var ( φ.A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    Gr.φ =  φ.var
    φ.InitByData()
    def fφ(x) : return φ.F([x])

    l.var = py.Var ( l.A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    Gr.l =  l.var
    l.InitByData()
    def fl(t) : return l.F([t])

    r.var = py.Var ( r.A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    Gr.r =  r.var
    r.InitByData()
    def fr(t) : return r.F([t])

    K.var = py.Var ( range (8), initialize = 0 )
    Gr.K =  K.var
    def fK(sT) : return K.F([sT])
    K.var[0].value = 1
 											# K(sT)>=0
    def EQ0 (Gr,i__sT) :
        return (
          fK(i__sT)>=0
        )
    Gr.conEQ0 = py.Constraint(sT.FlNodS,rule=EQ0 )
 											# K(sT)<=10
    def EQ1 (Gr,i__sT) :
        return (
          fK(i__sT)<=10
        )
    Gr.conEQ1 = py.Constraint(sT.FlNodS,rule=EQ1 )
 											# \frac{d}{d t}(T)=K(T)*\frac{d^2}{d x^2}(T)+\frac{d}{d T}(K(T))*(\frac{d}{d x}(T))**2
    def EQ2 (Gr,i__x,i__t) :
        return (
          ((fT(i__x,i__t)-fT(i__x,(i__t-t.step)))/t.step)==fK(fT(i__x,i__t))*((fT((i__x+x.step),i__t)+fT((i__x-x.step),i__t)-2*fT(i__x,i__t))/x.step**2)+(K.dF_dX(fT(i__x,i__t)))*(((fT(i__x,i__t)-fT((i__x-x.step),i__t))/x.step))**2
        )
    Gr.conEQ2 = py.Constraint(x.mFlNodSm,t.mFlNodS,rule=EQ2 )
 											# T(0,t)=l(t)
    def EQ3 (Gr,i__t) :
        return (
          fT(0,i__t)==fl(i__t)
        )
    Gr.conEQ3 = py.Constraint(t.FlNodS,rule=EQ3 )
 											# T(2,t)=r(t)
    def EQ4 (Gr,i__t) :
        return (
          fT(2,i__t)==fr(i__t)
        )
    Gr.conEQ4 = py.Constraint(t.FlNodS,rule=EQ4 )
 											# T(x,0)=φ(x)
    def EQ5 (Gr,i__x) :
        return (
          fT(i__x,0)==fφ(i__x)
        )
    Gr.conEQ5 = py.Constraint(x.FlNodS,rule=EQ5 )

    T.mu = Gr.mu; T.testSet = SvF.testSet; T.teachSet = SvF.teachSet;
 											# T.ComplSig2([Penal[0],Penal[1]])+T.MSD()
    def obj_expression(Gr):  
        return (
             T.ComplSig2([Penal[0],Penal[1]])+T.MSD()
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    T = Task.Funs[0]

    l = Task.Funs[2]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (T.ComplSig2([Penal[0],Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tT.ComplSig2([Penal[0],Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tT.ComplSig2([Penal[0],Penal[1]]) ='+ stmp+'\n')
    tmp = (T.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tT.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tT.MSD() ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.print_res = print_res

SvF.lenPenalty = 2

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
 											# Draw

Task.Draw (  '' )
 											# EOF      #-----------------------------------------------------