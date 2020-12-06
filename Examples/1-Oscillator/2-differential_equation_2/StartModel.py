# -*- coding: UTF-8 -*-
import sys
import platform
LibVersion = 'Lib28'
if platform.system() == 'Windows':
    path_SvF = "C:/_SvF/"
else:
    path_SvF = "/home/sokol/C/SvF/"
sys.path.append(path_SvF + LibVersion)
sys.path.append(path_SvF + "Pyomo_Everest/pe")
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
co.mngF = 'MNG-dif-2.mng'
co.Preproc = False
co.CVNumOfIter = 21
 											# CVstep       = 21  			# кол-во подмножеств для процедуры кросс-валидации
co.CVstep   = 21
 											# 
 											# Select 	t, x  from  ../Spring5.dat      # считывание данных
Tab.Select ( 't,x from ../Spring5.dat' )
 											# 
 											# SET:	t = [     ,    , 0.025] 	# область определения функции x(t)
t=Grid('t',nan,nan,0.025,'i__t','t')
Task.AddGrid(t)
 											# 	X = [ -0.1, 2.2, 0.1  ] 	# область значений (с запасом) функции x(t)
X=Grid('X',-0.1,2.2,0.1,'i__X','X')
Task.AddGrid(X)
 											#  	V = [ -1,   1.5, 0.1  ]		# область значений (с запасом) функции v(t)
V=Grid('V',-1.0,1.5,0.1,'i__V','V')
Task.AddGrid(V)
 											# 
 											# VAR:    x ( t )   			# искомая функция
x = Fun('x',[t],False); 
Task.InitializeAddFun ( x )
x__f = x
def fx(t) : return x.F([t])
 											# 	v ( t )			 	# искомая функция
v = Fun('v',[t],False); 
Task.InitializeAddFun ( v )
v__f = v
def fv(t) : return v.F([t])
 											# 	f ( X, V ); PolyPow = 6		# искомая правая часть - полином 5-ой степени от x и t
f = pFun(Fun('f',[X,V],False,6))
Task.InitializeAddFun ( f )
f__f = f
def ff(X,V) : return f.F([X,V])
 											# EQ:	d2/dt2(x) ==  f(x,v)		# дифференциальное ур-ие 2-ого порядка
 											#         v == d/dt(x)			# дифференциальное ур-ие 1-ого порядка
 											# 
 											# OBJ:   f.Complexity(Penal[0], Penal[1])/x.V.sigma2 + x.MSD()  # критерий выбора x(t),v(t) и f(x,t)from __future__ import division
from  numpy import *

from Lego import *
from pyomo.environ import *

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = ConcreteModel()
    Task.Gr = Gr
    if com.CV_NoR > 0:
        Gr.mu = Param ( range(com.CV_NoR), mutable=True, initialize = 1 )

    t = Task.Grids[0]

    X = Task.Grids[1]

    V = Task.Grids[2]
 											# x(t)
    x = Funs[0];  x__f = x
    x__i = Var ( Funs[0].A[0].NodS,domain=Reals, initialize = 1 )
    x.grd = x__i ; Gr.x =  x__i
    x.InitByData()
    def fx(t) : return x__f.F([t])
 											# v(t)
    v = Funs[1];  v__f = v
    v__i = Var ( Funs[1].A[0].NodS,domain=Reals, initialize = 1 )
    v.grd = v__i ; Gr.v =  v__i
    v.InitByData()
    def fv(t) : return v__f.F([t])
 											# f(X,V); PolyPow=6
    f = Funs[2];  f__f = f
    f__i = Var ( range (PolySize(2,6) ), initialize = 0 )
    f.grd = f__i ; Gr.f =  f__i
    def ff(X,V) : return f.F([X,V])
    f__i[0].value = 1
 											# d2/dt2(x)==f(x,v)
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

    x.mu = Gr.mu; x.testSet = co.testSet; x.teachSet = co.teachSet
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
    tmp = (f.Complexity([Penal[0],Penal[1]])/x.V.sigma2)()
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tf.Complexity([Penal[0],Penal[1]])/x.V.sigma2 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tf.Complexity([Penal[0],Penal[1]])/x.V.sigma2 ='+ stmp+'\n')
    tmp = (x.MSD())()
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.MSD() ='+ stmp+'\n')

    return


com.Task.createGr  = createGr

com.Task.print_res = print_res

co.lenPenalty = 2

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
 											# 
 											# Draw   x				# отображение функции x(t)

Task.Draw (  'x' )
 											# 
 											# Pl = Polyline (x, v, None, ‘Trajectory’)
Pl=Polyline(x,v,None,'Trajectory')
 											# Pl.Y[0]  = Pl.Y[1]
Pl.Y[0]=Pl.Y[1]
 											# Pl.Y[-1] = Pl.Y[-2]
Pl.Y[-1]=Pl.Y[-2]
 											# 
 											# Draw f Trajectory;LC:red

Task.Draw (  'f Trajectory;LC:red' )
 											# 
 											# 
 											# EOF