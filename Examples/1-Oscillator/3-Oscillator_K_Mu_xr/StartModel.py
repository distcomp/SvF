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
co.mngF = 'Oscillator_K_Mu_xr_ChDir.odt'
co.Preproc = False
co.CVNumOfIter = 50
 											# CVstep      = 21  			# кол-во подмножеств для процедуры кросс-валидации      			
co.CVstep   = 21
 											# DIF1 	= Central        		# использование центральной схемы аппроксимации производной	       		
co.DIF1 = 'Central'
 											# Select x, t  from  ../Spring5.dat   # считывание данных    
Tab.Select ( 'x,t from ../Spring5.dat' )
 											# GRID:      t  ∈ [ -1., 2.5, 0.025 ] # область определения функции x(t) и v(t)      
t=Grid('t',-1.0,2.5,0.025,'i__t','t')
Task.AddGrid(t)
 											# Var:    	x ( t ) 			# искомая функция   				
x = Fun('x',[t],False); 
Task.InitializeAddFun ( x )
x__f = x
def fx(t) : return x.F([t])
 											# 	v ( t )			# искомая функция				
v = Fun('v',[t],False); 
Task.InitializeAddFun ( v )
v__f = v
def fv(t) : return v.F([t])
 											# 	K   			# неизвестный параметр – жесткость пружины 	  			
K = Fun('K',[],False); 
Task.InitializeAddFun ( K )
K__f = K
fK = K.grd
 											# 	Δx  			# неизвестный параметр - смещение точки крепления (Deltax)	 			
Deltax = Fun('Deltax',[],False); 
Task.InitializeAddFun ( Deltax )
Deltax__f = Deltax
fDeltax = Deltax.grd
 											# 	μ     			# неизвестный параметр - вязкость среды (в формуле Стокса), 	    			
muu = Fun('muu',[],False); 
Task.InitializeAddFun ( muu )
muu__f = muu
fmuu = muu.grd
 											# 					#    (в программе заменяется на muu)   					     
 											# # EQ:   d2/dt2(x) == - K * (x - Δx) - μ*v  # обычная запись ур-ия – без редактора формул      
 											# EQ:          # Формулы набираются в редакторе формул         \frac{d^2}{dt^2}(x) == - K * ( x - \Delta x ) -\mu * v 
 											#           			     # дифференциальное ур-ие 1-ого порядка         v == \frac {d}{dt}(x)
 											# OBJ:    x.Complexity ( Penal[0])/x.V.sigma2 + x.MSD()   # критерий выбора     from __future__ import division
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
 											# K
    K = Funs[2];  K__f = K
    K__i = Var ( domain=Reals, initialize = 1 )
    K.grd = K__i ; Gr.K =  K__i
    K.InitByData()
    fK = K__i
 											# Deltax
    Deltax = Funs[3];  Deltax__f = Deltax
    Deltax__i = Var ( domain=Reals, initialize = 1 )
    Deltax.grd = Deltax__i ; Gr.Deltax =  Deltax__i
    Deltax.InitByData()
    fDeltax = Deltax__i
 											# muu
    muu = Funs[4];  muu__f = muu
    muu__i = Var ( domain=Reals, initialize = 1 )
    muu.grd = muu__i ; Gr.muu =  muu__i
    muu.InitByData()
    fmuu = muu__i

    x.mu = Gr.mu; x.testSet = co.testSet; x.teachSet = co.teachSet
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
    tmp = (x.Complexity([Penal[0]])/x.V.sigma2)()
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.Complexity([Penal[0]])/x.V.sigma2 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.Complexity([Penal[0]])/x.V.sigma2 ='+ stmp+'\n')
    tmp = (x.MSD())()
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.MSD() ='+ stmp+'\n')

    return


com.Task.createGr  = createGr

com.Task.print_res = print_res

co.lenPenalty = 1

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
 											# Draw								# отображение функций								

Task.Draw (  '' )
 											# EOF								# конец обработки задания								