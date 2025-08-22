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
co.mngF = 'MNG-dif-1G.mng'
co.Preproc = False
co.CVNumOfIter = 1
 											# CVstep       = 21              # кол-во подмножеств для процедуры кросс-валидации
co.CVstep = 21
 											# Select     time AS t, position AS x  from  ../Spring5.xlsx # считывание данных из таблицы ../Spring5.xlsx                             # столбец time переименовывается в t, position - в x
Tab.Select ( 'Select time AS t,position AS x from ../Spring5.xlsx' )
 											# SET:    t = [   ,    , 0.025]          # область определения функции x(t)
t=Grid('t',nan,nan,0.025,'i__t','t')
Task.AddGrid(t)
 											#     X = [  0, 2.2, 0.1  ]          # область значений (с запасом) функции x(t)
X=Grid('X',0.0,2.2,0.1,'i__X','X')
Task.AddGrid(X)
 											# VAR:    x ( t )               # искомая функция
x = Fun('x',[t],False); 
Task.InitializeAddFun ( x )
x__f = x
def fx(t) : return x.F([t])
 											# #    f ( X );  PolyPow = 5         # искомая правая часть - полином 5-ой степени
 											#     f ( X );  VarType = G         # искомая правая часть - сглаженная ломаная
f = Fun('f',[X],False); 
f.type = 'G'; 
Task.InitializeAddFun ( f )
f__f = f
def ff(X) : return f.F([X])
 											# EQ:    d/dt(x) = f(x)            # дифференциальное ур-ие
 											# OBJ:       x.MSD() + f.Complexity ( Penal[0] )  # целевая функция – смешанный критерий выбора x(t)from __future__ import division
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
 											# x(t)
    x = Funs[0];  x__f = x
    x__i = Var ( Funs[0].A[0].NodS,domain=Reals, initialize = 1 )
    x.var = x__i ; Gr.x =  x__i
    x.InitByData()
    def fx(t) : return x__f.F([t])
 											# f(X); VarType=G
    f = Funs[1];  f__f = f
    f__i = Var ( Funs[1].A[0].NodS,domain=Reals, initialize = 1 )
    f.var = f__i ; Gr.f =  f__i
    f.InitByData()
    def ff(X) : return f__f.F([X])
 											# d/dt(x)=f(x)
    def EQ0 (Gr,i__t) :
        return (
          ((fx((i__t+t.step))-fx(i__t))/t.step)==ff(fx(i__t))
        )
    Gr.conEQ0 = Constraint(t.FlNodSm,rule=EQ0 )

    x.mu = Gr.mu; x.testSet = co.testSet; x.teachSet = co.teachSet;
 											# x.MSD()+f.Complexity([Penal[0]])
    def obj_expression(Gr):  
        return (
             x.MSD()+f.Complexity([Penal[0]])
        )  
    Gr.OBJ = Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x = Task.Funs[0]

    f = Task.Funs[1]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (x.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.MSD() ='+ stmp+'\n')
    tmp = (f.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tf.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tf.Complexity([Penal[0]]) ='+ stmp+'\n')

    return


com.Task.createGr  = createGr

com.Task.print_res = print_res

co.lenPenalty = 1

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
 											# Draw                    # отображение всех функции: x(t) и f(x)

Task.Draw (  '' )
 											# EOF