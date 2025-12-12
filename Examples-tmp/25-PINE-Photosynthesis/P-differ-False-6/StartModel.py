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
Table ( '../Phot-7shoX5.xlsx','curentTabl','ROWNUM AS t,I AS Q1,Ta AS T,WPD AS VPD,PhX2 AS P,PhX2 AS P,Dat,NN,PRel,ERel' )
Q1 = Set('Q1',SvF.curentTabl.dat('Q1')[:].min(),SvF.curentTabl.dat('Q1')[:].max(),-50,'','Q1')
T = Set('T',SvF.curentTabl.dat('T')[:].min(),SvF.curentTabl.dat('T')[:].max(),-50,'','T')
P = smbFun('P',[Q1,T], SymbolInteg=False)
def fP(Q1,T) : return P.F([Q1,T])
c = Tensor('c',[36])
def fc(i) : return c.F([i])
def P_smbF00(Args) :
   Q1 = Args[0]
   T = Args[1]
   return  ( fc(0)+fc(1)*T+fc(2)*Q1+fc(3)*T**2+fc(4)*Q1*T+fc(5)*Q1**2+fc(6)*T**3+fc(7)*Q1*T**2+fc(8)*Q1**2*T+fc(9)*Q1**3+fc(10)*T**4+fc(11)*Q1*T**3+fc(12)*Q1**2*T**2+fc(13)*Q1**3*T+fc(14)*Q1**4+fc(15)*T**5+fc(16)*Q1*T**4+fc(17)*Q1**2*T**3+fc(18)*Q1**3*T**2+fc(19)*Q1**4*T+fc(20)*Q1**5+fc(21)*T**6+fc(22)*Q1*T**5+fc(23)*Q1**2*T**4+fc(24)*Q1**3*T**3+fc(25)*Q1**4*T**2+fc(26)*Q1**5*T+fc(27)*Q1**6+fc(28)*T**7+fc(29)*Q1*T**6+fc(30)*Q1**2*T**5+fc(31)*Q1**3*T**4+fc(32)*Q1**4*T**3+fc(33)*Q1**5*T**2+fc(34)*Q1**6*T+fc(35)*Q1**7 ) 
P.smbF = P_smbF00
def P_Hessian00(Args) :
   Q1 = Args[0]
   T = Args[1]
   return 2*(21*Q1**5*fc(35) + 15*Q1**4*T*fc(34) + 15*Q1**4*fc(27) + 10*Q1**3*T**2*fc(33) + 10*Q1**3*T*fc(26) + 10*Q1**3*fc(20) + 6*Q1**2*T**3*fc(32) + 6*Q1**2*T**2*fc(25) + 6*Q1**2*T*fc(19) + 6*Q1**2*fc(14) + 3*Q1*T**4*fc(31) + 3*Q1*T**3*fc(24) + 3*Q1*T**2*fc(18) + 3*Q1*T*fc(13) + 3*Q1*fc(9) + T**5*fc(30) + T**4*fc(23) + T**3*fc(17) + T**2*fc(12) + T*fc(8) + fc(5)) 
P.Hessian[0][0] = P_Hessian00
def P_Hessian01(Args) :
   Q1 = Args[0]
   T = Args[1]
   return 6*Q1**5*fc(34) + 10*Q1**4*T*fc(33) + 5*Q1**4*fc(26) + 12*Q1**3*T**2*fc(32) + 8*Q1**3*T*fc(25) + 4*Q1**3*fc(19) + 12*Q1**2*T**3*fc(31) + 9*Q1**2*T**2*fc(24) + 6*Q1**2*T*fc(18) + 3*Q1**2*fc(13) + 10*Q1*T**4*fc(30) + 8*Q1*T**3*fc(23) + 6*Q1*T**2*fc(17) + 4*Q1*T*fc(12) + 2*Q1*fc(8) + 6*T**5*fc(29) + 5*T**4*fc(22) + 4*T**3*fc(16) + 3*T**2*fc(11) + 2*T*fc(7) + fc(4) 
P.Hessian[0][1] = P_Hessian01
def P_Hessian11(Args) :
   Q1 = Args[0]
   T = Args[1]
   return 2*(Q1**5*fc(33) + 3*Q1**4*T*fc(32) + Q1**4*fc(25) + 6*Q1**3*T**2*fc(31) + 3*Q1**3*T*fc(24) + Q1**3*fc(18) + 10*Q1**2*T**3*fc(30) + 6*Q1**2*T**2*fc(23) + 3*Q1**2*T*fc(17) + Q1**2*fc(12) + 15*Q1*T**4*fc(29) + 10*Q1*T**3*fc(22) + 6*Q1*T**2*fc(16) + 3*Q1*T*fc(11) + Q1*fc(7) + 21*T**5*fc(28) + 15*T**4*fc(21) + 10*T**3*fc(15) + 6*T**2*fc(10) + 3*T*fc(6) + fc(3)) 
P.Hessian[1][1] = P_Hessian11
P.ArgNormalition=False
SvF.RunMode = 'S&S'
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    c.var = py.Var ( range (c.Sizes[0]),domain=Reals )
    Gr.c =  c.var

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