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
SvF.CVNumOfIter = 0
 											# CVstep          21
SvF.CVstep = 21
 											# Select x, t  from  ../Spring5.dat As Tb
Table ( '../Spring5.dat','Tb','x,t' )
 											# GRID:
 											#         t ∈ [ -1.,  2.5, 0.025 ]
t=Grid('t',-1.0,2.5,0.025,'i__t','t')
 											#     X = [ -0.1, 2.2, 0.1   ]
X=Grid('X',-0.1,2.2,0.1,'i__X','X')
 											#     V = [ -1,   1.5, 0.1   ]
V=Grid('V',-1.0,1.5,0.1,'i__V','V')
 											# VAR:
 											#         x ( t ) ;             #  t ∈ [ , 2.5,0.025];  x ∈ [ -10.,10 ]; <=7;  >= -6
x = Fun('x',[t],False,-1,1, '') 
def fx(t) : return x.F([t])
 											#     v ( t )
v = Fun('v',[t],False,-1,1, '') 
def fv(t) : return v.F([t])
 											# VAR:    f ( X, V );    PolyPow = 6
f = pFun('f',[X,V],False,6,1, '') 
def ff(X,V) : return f.F([X,V])
 											# DIF1 = Central
DIF1=Central
 											# EQ:
 											#         d2/dt2(x) ==  f(x,v);  #t <> 1
 											#      v == d/dt(x)
 											# OBJ:    f.Complexity ( Penal[0], Penal[1] )/x.V.sigma2 + x.MSD()from __future__ import division
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

    f.var = Var ( range (28), initialize = 0 )
    Gr.f =  f.var
    def ff(X,V) : return f.F([X,V])
    f.var[0].value = 1
 											# d2/dt2(x)==f(x,v);
    def EQ0 (Gr,i__t) :
        return (
          ((fx((i__t+t.step))+fx((i__t-t.step))-2*fx(i__t))/t.step**2)==ff(fx(i__t),fv(i__t))
        )
    Gr.conEQ0 = Constraint(t.mFlNodSm,rule=EQ0 )
 											# v== d/dt(x)
    def EQ1 (Gr,i__t) :
        return (
          fv(i__t)==((fx((i__t+t.step))-fx(i__t))/t.step)
        )
    Gr.conEQ1 = Constraint(t.FlNodSm,rule=EQ1 )

    x.mu = Gr.mu; x.testSet = SvF.testSet; x.teachSet = SvF.teachSet;
 											# f.Complexity([Penal[0],Penal[1]])/x.V.sigma2+x.MSD()
    def obj_expression(Gr):  
        return (
             f.Complexity([Penal[0],Penal[1]])/x.V.sigma2+x.MSD()
        )  
    Gr.OBJ = Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x = Task.Funs[0]

    f = Task.Funs[2]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (f.Complexity([Penal[0],Penal[1]])/x.V.sigma2)
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tf.Complexity([Penal[0],Penal[1]])/x.V.sigma2 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tf.Complexity([Penal[0],Penal[1]])/x.V.sigma2 ='+ stmp+'\n')
    tmp = (x.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.MSD() ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.print_res = print_res

SvF.lenPenalty = 2

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
 											# Draw x

Task.Draw (  'x' )
 											# Pl = Polyline (x, v, None, ‘Trajectory’)
Pl=Polyline(x,v,None,‘Trajectory')
 											# Pl.Y[0]  = Pl.Y[1]
Pl.Y[0]=Pl.Y[1]
 											# Pl.Y[-1] = Pl.Y[-2]
Pl.Y[-1]=Pl.Y[-2]
 											# Draw f Trajectory;LC:red

Task.Draw (  'f Trajectory;LC:red' )
 											# EOF