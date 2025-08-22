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
SvF.mngF = 'MNG.mng'
SvF.CVNumOfIter = 1
SvF.useNaN = True
Table ( '../../DATA/Phot-7shoX5.xlsx','curentTabl','ROWNUM AS t,I AS Q1,Ta AS T,WPD AS VPD,PhX2 AS P,PhX2 AS P,Dat,NN,PRel,ERel' )
Q1 = Set('Q1',SvF.curentTabl.dat('Q1')[:].min(),SvF.curentTabl.dat('Q1')[:].max(),-50,'','Q1')
T = Set('T',SvF.curentTabl.dat('T')[:].min(),SvF.curentTabl.dat('T')[:].max(),-50,'','T')
P = Fun('P',[Q1,T])
def fP(Q1,T) : return P.F([Q1,T])
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    P.var = py.Var ( P.A[0].NodS,P.A[1].NodS,domain=Reals )
    Gr.P =  P.var

    make_CV_Sets(0, SvF.CVstep)

    if len (SvF.CV_NoRs) > 0 :

       Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('P'))
    if P.mu is None : P.mu = Gr.mu0
    P.ValidationSets = SvF.ValidationSets
    P.notTrainingSets = SvF.notTrainingSets
    P.TrainingSets = SvF.TrainingSets
 											# P.Complexity([Penal[0],Penal[1]])+P.MSD()
    def obj_expression(Gr):  
        return (
             P.Complexity([Penal[0],Penal[1]])+P.MSD()
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    P = Task.Funs[0]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (P.Complexity([Penal[0],Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tP.Complexity([Penal[0],Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tP.Complexity([Penal[0],Penal[1]]) ='+ stmp+'\n')
    tmp = (P.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tP.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tP.MSD() ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
Task.Draw ('')