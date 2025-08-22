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
P = smbFun('P',[Q1,T], SymbolInteg=False, SymbolDiffer=False)
def fP(Q1,T) : return P.F([Q1,T])
c = Tensor('c',[190])
def fc(i) : return c.F([i])
def P_smbF00(Args) :
   Q1 = Args[0]
   T = Args[1]
   return  ( fc(0)+fc(1)*T+fc(2)*Q1+fc(3)*T**2+fc(4)*Q1*T+fc(5)*Q1**2+fc(6)*T**3+fc(7)*Q1*T**2+fc(8)*Q1**2*T+fc(9)*Q1**3+fc(10)*T**4+fc(11)*Q1*T**3+fc(12)*Q1**2*T**2+fc(13)*Q1**3*T+fc(14)*Q1**4+fc(15)*T**5+fc(16)*Q1*T**4+fc(17)*Q1**2*T**3+fc(18)*Q1**3*T**2+fc(19)*Q1**4*T+fc(20)*Q1**5+fc(21)*T**6+fc(22)*Q1*T**5+fc(23)*Q1**2*T**4+fc(24)*Q1**3*T**3+fc(25)*Q1**4*T**2+fc(26)*Q1**5*T+fc(27)*Q1**6+fc(28)*T**7+fc(29)*Q1*T**6+fc(30)*Q1**2*T**5+fc(31)*Q1**3*T**4+fc(32)*Q1**4*T**3+fc(33)*Q1**5*T**2+fc(34)*Q1**6*T+fc(35)*Q1**7+fc(36)*T**8+fc(37)*Q1*T**7+fc(38)*Q1**2*T**6+fc(39)*Q1**3*T**5+fc(40)*Q1**4*T**4+fc(41)*Q1**5*T**3+fc(42)*Q1**6*T**2+fc(43)*Q1**7*T+fc(44)*Q1**8+fc(45)*T**9+fc(46)*Q1*T**8+fc(47)*Q1**2*T**7+fc(48)*Q1**3*T**6+fc(49)*Q1**4*T**5+fc(50)*Q1**5*T**4+fc(51)*Q1**6*T**3+fc(52)*Q1**7*T**2+fc(53)*Q1**8*T+fc(54)*Q1**9+fc(55)*T**10+fc(56)*Q1*T**9+fc(57)*Q1**2*T**8+fc(58)*Q1**3*T**7+fc(59)*Q1**4*T**6+fc(60)*Q1**5*T**5+fc(61)*Q1**6*T**4+fc(62)*Q1**7*T**3+fc(63)*Q1**8*T**2+fc(64)*Q1**9*T+fc(65)*Q1**10+fc(66)*T**11+fc(67)*Q1*T**10+fc(68)*Q1**2*T**9+fc(69)*Q1**3*T**8+fc(70)*Q1**4*T**7+fc(71)*Q1**5*T**6+fc(72)*Q1**6*T**5+fc(73)*Q1**7*T**4+fc(74)*Q1**8*T**3+fc(75)*Q1**9*T**2+fc(76)*Q1**10*T+fc(77)*Q1**11+fc(78)*T**12+fc(79)*Q1*T**11+fc(80)*Q1**2*T**10+fc(81)*Q1**3*T**9+fc(82)*Q1**4*T**8+fc(83)*Q1**5*T**7+fc(84)*Q1**6*T**6+fc(85)*Q1**7*T**5+fc(86)*Q1**8*T**4+fc(87)*Q1**9*T**3+fc(88)*Q1**10*T**2+fc(89)*Q1**11*T+fc(90)*Q1**12+fc(91)*T**13+fc(92)*Q1*T**12+fc(93)*Q1**2*T**11+fc(94)*Q1**3*T**10+fc(95)*Q1**4*T**9+fc(96)*Q1**5*T**8+fc(97)*Q1**6*T**7+fc(98)*Q1**7*T**6+fc(99)*Q1**8*T**5+fc(100)*Q1**9*T**4+fc(101)*Q1**10*T**3+fc(102)*Q1**11*T**2+fc(103)*Q1**12*T+fc(104)*Q1**13+fc(105)*T**14+fc(106)*Q1*T**13+fc(107)*Q1**2*T**12+fc(108)*Q1**3*T**11+fc(109)*Q1**4*T**10+fc(110)*Q1**5*T**9+fc(111)*Q1**6*T**8+fc(112)*Q1**7*T**7+fc(113)*Q1**8*T**6+fc(114)*Q1**9*T**5+fc(115)*Q1**10*T**4+fc(116)*Q1**11*T**3+fc(117)*Q1**12*T**2+fc(118)*Q1**13*T+fc(119)*Q1**14+fc(120)*T**15+fc(121)*Q1*T**14+fc(122)*Q1**2*T**13+fc(123)*Q1**3*T**12+fc(124)*Q1**4*T**11+fc(125)*Q1**5*T**10+fc(126)*Q1**6*T**9+fc(127)*Q1**7*T**8+fc(128)*Q1**8*T**7+fc(129)*Q1**9*T**6+fc(130)*Q1**10*T**5+fc(131)*Q1**11*T**4+fc(132)*Q1**12*T**3+fc(133)*Q1**13*T**2+fc(134)*Q1**14*T+fc(135)*Q1**15+fc(136)*T**16+fc(137)*Q1*T**15+fc(138)*Q1**2*T**14+fc(139)*Q1**3*T**13+fc(140)*Q1**4*T**12+fc(141)*Q1**5*T**11+fc(142)*Q1**6*T**10+fc(143)*Q1**7*T**9+fc(144)*Q1**8*T**8+fc(145)*Q1**9*T**7+fc(146)*Q1**10*T**6+fc(147)*Q1**11*T**5+fc(148)*Q1**12*T**4+fc(149)*Q1**13*T**3+fc(150)*Q1**14*T**2+fc(151)*Q1**15*T+fc(152)*Q1**16+fc(153)*T**17+fc(154)*Q1*T**16+fc(155)*Q1**2*T**15+fc(156)*Q1**3*T**14+fc(157)*Q1**4*T**13+fc(158)*Q1**5*T**12+fc(159)*Q1**6*T**11+fc(160)*Q1**7*T**10+fc(161)*Q1**8*T**9+fc(162)*Q1**9*T**8+fc(163)*Q1**10*T**7+fc(164)*Q1**11*T**6+fc(165)*Q1**12*T**5+fc(166)*Q1**13*T**4+fc(167)*Q1**14*T**3+fc(168)*Q1**15*T**2+fc(169)*Q1**16*T+fc(170)*Q1**17+fc(171)*T**18+fc(172)*Q1*T**17+fc(173)*Q1**2*T**16+fc(174)*Q1**3*T**15+fc(175)*Q1**4*T**14+fc(176)*Q1**5*T**13+fc(177)*Q1**6*T**12+fc(178)*Q1**7*T**11+fc(179)*Q1**8*T**10+fc(180)*Q1**9*T**9+fc(181)*Q1**10*T**8+fc(182)*Q1**11*T**7+fc(183)*Q1**12*T**6+fc(184)*Q1**13*T**5+fc(185)*Q1**14*T**4+fc(186)*Q1**15*T**3+fc(187)*Q1**16*T**2+fc(188)*Q1**17*T+fc(189)*Q1**18 ) 
P.smbF = P_smbF00
P.ArgNormalition=True
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