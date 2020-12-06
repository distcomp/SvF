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
co.mngF = 'MNG-full.mng'
co.Preproc = False
co.CVNumOfIter = 21
 											# CVstep       = 21  			# кол-во подмножеств для процедуры кросс-валидации
co.CVstep   = 21
 											# 
 											# Select 	x, t  from  ../Spring5.dat 	# считывание столбцов  x, t из файла  ../Spring5.dat
Tab.Select ( 'x,t from ../Spring5.dat' )
 											# 
 											# t_min = -1.0				# левая  граница интервала
t_min=-1.0
Task.AddDef('t_min',[-1.0])
 											# t_max =  2.5				# правая граница интервала
t_max=2.5
Task.AddDef('t_max',[2.5])
 											# 
 											# SET:	T   = [t_min,  t_max,  0.025]	# множество Т от t_min до t_max с шагом 0.025
T=Grid('T',t_min,t_max,0.025,'i__T','T')
Task.AddGrid(T)
 											# 
 											# VAR:    x ( t ); t ∈ T  # t \in T   	# неизвестная функция, заданная на множестве Т
x = Fun('x',[Grid('t',t_min,t_max,0.025,'i__T','t')],False); 
Task.InitializeAddFun ( x )
x__f = x
def fx(t) : return x.F([t])
 											# 
 											# OBJ:   	x.MSD() + x.Complexity(Penal[0]) # целевая функцияfrom __future__ import division
from  numpy import *

from Lego import *
from pyomo.environ import *

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = ConcreteModel()
    Task.Gr = Gr
    if com.CV_NoR > 0:
        Gr.mu = Param ( range(com.CV_NoR), mutable=True, initialize = 1 )

    T = Task.Grids[0]
 											# x(t); t\inn  T
    x = Funs[0];  x__f = x
    x__i = Var ( Funs[0].A[0].NodS,domain=Reals, initialize = 1 )
    x.grd = x__i ; Gr.x =  x__i
    x.InitByData()
    def fx(t) : return x__f.F([t])

    x.mu = Gr.mu; x.testSet = co.testSet; x.teachSet = co.teachSet
 											# x.MSD()+x.Complexity([Penal[0]])
    def obj_expression(Gr):  
        return (
             x.MSD()+x.Complexity([Penal[0]])
        )  
    Gr.OBJ = Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x = Task.Funs[0]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (x.MSD())()
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.MSD() ='+ stmp+'\n')
    tmp = (x.Complexity([Penal[0]]))()
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.Complexity([Penal[0]]) ='+ stmp+'\n')

    return


com.Task.createGr  = createGr

com.Task.print_res = print_res

co.lenPenalty = 1

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
 											# 
 											# Draw	x				# отображение нацденной функции x(t)

Task.Draw (  'x' )
 											# 
 											# EOF					# конец файла, все что дальше опускается