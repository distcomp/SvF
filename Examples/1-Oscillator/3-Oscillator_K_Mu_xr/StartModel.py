# -*- coding: UTF-8 -*-
import sys
import platform
LibVersion = 'Lib29'
if platform.system() == 'Windows':
    path_SvF = "C:/_SvF/"
else:
    path_SvF = "/mnt/hgst2/ext4/git_work/SvF/"
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
SvF.mngF = 'MNG.mng'
SvF.CVNumOfIter = 1
 											# CVstep          21
SvF.CVstep = 21
 											# Select x, t  from  ../Spring5.dat
Table ( '../Spring5.dat','curentTabl','x,t' )
 											# GRID:
 											#         t  ∈ [ -1.,  2.5, 0.025 ]
t=Grid('t',-1.0,2.5,0.025,'i__t','t')
 											# Var:    x ( t )
x = Fun('x',[t],False,-1,1, '') 
def fx(t) : return x.F([t])
 											#     v ( t )
v = Fun('v',[t],False,-1,1, '') 
def fv(t) : return v.F([t])
 											#     K
K = Fun('K',[],False,-1,1, '') 
fK = K.grd
 											#     μ  #   will be substituted on 'muu'
muu = Fun('muu',[],False,-1,1, '') 
fmuu = muu.grd
 											#     xr
xr = Fun('xr',[],False,-1,1, '') 
fxr = xr.grd
 											# SchemeD1 = Central
SvF.SchemeD1 = "Central"
 											# EQ:
 											#         d2/dt2(x) == - K * ( x - xr ) - μ * v
 											#      v == d/dt(x)
 											# OBJ:    x.Complexity ( Penal[0] ) / x.V.sigma2 + x.MSD()from __future__ import division
from  numpy import *

from Lego import *
from pyomo.environ import *

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = ConcreteModel()
    Task.Gr = Gr
    if SvF.CV_NoR > 0:
        Gr.mu = Param ( range(SvF.CV_NoR), mutable=True, initialize = 1 )

    x.var = Var ( x.A[0].NodS,domain=Reals, initialize = 1 )
    Gr.x =  x.var
    x.InitByData()
    def fx(t) : return x.F([t])

    v.var = Var ( v.A[0].NodS,domain=Reals, initialize = 1 )
    Gr.v =  v.var
    v.InitByData()
    def fv(t) : return v.F([t])

    K.var = Var ( domain=Reals, initialize = 1 )
    Gr.K =  K.var
    K.InitByData()
    fK = K.var

    muu.var = Var ( domain=Reals, initialize = 1 )
    Gr.muu =  muu.var
    muu.InitByData()
    fmuu = muu.var

    xr.var = Var ( domain=Reals, initialize = 1 )
    Gr.xr =  xr.var
    xr.InitByData()
    fxr = xr.var
 											# d2/dt2(x)==-K*( x-xr)- muu*v
    def EQ0 (Gr,i__t) :
        return (
          ((fx((i__t+t.step))+fx((i__t-t.step))-2*fx(i__t))/t.step**2)==-fK*(fx(i__t)-fxr)-fmuu*fv(i__t)
        )
    Gr.conEQ0 = Constraint(t.mFlNodSm,rule=EQ0 )
 											# v== d/dt(x)
    def EQ1 (Gr,i__t) :
        return (
          fv(i__t)==((fx((i__t+t.step))-fx((i__t-t.step)))/t.step *0.5)
        )
    Gr.conEQ1 = Constraint(t.mFlNodSm,rule=EQ1 )

    x.mu = Gr.mu; x.testSet = SvF.testSet; x.teachSet = SvF.teachSet;
 											# x.Complexity([Penal[0]])/x.V.sigma2+x.MSD()
    def obj_expression(Gr):  
        return (
             x.Complexity([Penal[0]])/x.V.sigma2+x.MSD()
        )  
    Gr.OBJ = Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x = Task.Funs[0]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (x.Complexity([Penal[0]])/x.V.sigma2)
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.Complexity([Penal[0]])/x.V.sigma2 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.Complexity([Penal[0]])/x.V.sigma2 ='+ stmp+'\n')
    tmp = (x.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.MSD() ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.print_res = print_res

SvF.lenPenalty = 1

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
 											# Draw

Task.Draw (  '' )
 											# EOF