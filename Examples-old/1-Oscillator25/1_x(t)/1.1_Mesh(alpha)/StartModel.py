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
SvF.mngF = 'MNG-0.1166-Opt.mng'
DAT = Table ( 'Spring5.dat','DAT','*' )
t = Set('t',SvF.curentTabl.dat('t')[:].min(),SvF.curentTabl.dat('t')[:].max(),0.025,'','t')
x = Fun('x',[t])
def fx(t) : return x.F([t])
CVmakeSets ( CV_NumSets=21 )
SvF.CVNumOfIter = 1
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    x.var = py.Var ( x.A[0].NodS,domain=Reals )
    Gr.x =  x.var

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('x'))
    if x.mu is None : x.mu = Gr.mu0
    x.ValidationSets = SvF.ValidationSets
    x.notTrainingSets = SvF.notTrainingSets
    x.TrainingSets = SvF.TrainingSets
 											# x.MSD()+x.Complexity([Penal[0]])
    def obj_expression(Gr):  
        return (
             x.MSD()+x.Complexity([Penal[0]])
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x = Task.Funs[0]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (x.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.MSD() ='+ stmp+'\n')
    tmp = (x.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.Complexity([Penal[0]]) ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
x.SaveSol ('xOpt(t).sol')
t21 = Set('t21',SvF.curentTabl.dat('t')[:].min(),SvF.curentTabl.dat('t')[:].max(),0.175,'','t')
x_f = Fun('x_f',[t21], param=True)
def fx_f(t21) : return x_f.F([t21])
x_f.grd=x_f.V.dat
sqrt_x_f__x=sqrt ( sum((fx_f(va)-fx(va))**2 for va in x_f.A[0].Val)/DAT.NoR)/x.V.sigma*100
print('\nsqrt_x_f__x',sqrt_x_f__x,'NoR',DAT.NoR)
SvF.addStrToRes='sqrt_x_f-x= '+str(sqrt_x_f__x)
xOver = Fun('xOver',[t], param=True, ReadFrom="xOver(t).sol")
def fxOver(t) : return xOver.F([t])
xUnder = Fun('xUnder',[t], param=True, ReadFrom="xUnder(t).sol")
def fxUnder(t) : return xUnder.F([t])
Reg=Polyline([-1,-1,2.5,2.5,-1],[-0.1,2.2,2.2,-0.1,-0.1],None,'Region')
x.V.oname="Ballanced"
xOver.V.oname="Overtrained"
xUnder.V.oname="Undertrained "
x_f.V.leg_name  = "z(t)"
x_f.V.dat=None
Task.Draw ( 'Region;LC:green;LSt:dashed x_f;MS:0;DMS:0;LSt:solid;LC:green xOver;LC:b;MS:0;LW:1;LSt:dotted xUnder;LC:gray x;LC:r;LSt:solid;DMS:3;DLW:0;DC:b' )