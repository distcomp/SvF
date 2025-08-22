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
SvF.mngF = 'x(t)_InternalinternalOrganization.odt'
SvF.CVNumOfIter = 0
SvF.CVstep = 21
Table ( '../Spring5.dat','curentTabl','x,t' )
tmin=-1.0
tmax=2.5
step=0.025
T=Grid('T',tmin,tmax,step,'i__T','T')
x = Fun('x',[Grid('t',tmin,tmax,step,'i__T','t')],False,-1,1, '') 
def fx(t) : return x.F([t])
co.testSet,co.teachSet=MakeSets_byParts(x.NoR,co.CVstep)
from  numpy import *

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    x.var = py.Var ( x.A[0].NodS,domain=Reals, initialize = 1 )
    Gr.x =  x.var
    x.InitByData()
    def fx(t) : return x.F([t])

    SvF.testSet, SvF.teachSet = MakeSets_byParts(SvF.curentTabl.NoR, SvF.CVstep)

    Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
 											# sum(Gr.mu0[i]*(x.V.dat[i]-fx(x.A[0].dat[i]+tmin))**2 for i in range ( 0, 20+1 ) )/x.V.sigma2/sum(Gr.mu0[i] for i in range ( 0, 20+1 ) )+Penal[0]*sum ( (int(i__T!=tmin+step)+int(i__T!=tmax-step))/2*T.step*(((fx((i__T+T.step))+fx((i__T-T.step))-2*fx(i__T))/T.step**2))**2 for i__T in myrange (tmin+step,tmax-step,T.step) )/14.5
    def obj_expression(Gr):  
        return (
             sum(Gr.mu0[i]*(x.V.dat[i]-fx(x.A[0].dat[i]+tmin))**2 for i in range ( 0, 20+1 ) )/x.V.sigma2/sum(Gr.mu0[i] for i in range ( 0, 20+1 ) )+Penal[0]*sum ( (int(i__T!=tmin+step)+int(i__T!=tmax-step))/2*T.step*(((fx((i__T+T.step))+fx((i__T-T.step))-2*fx(i__T))/T.step**2))**2 for i__T in myrange (tmin+step,tmax-step,T.step) )/14.5
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x = Task.Funs[0]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (sum(Gr.mu0[i]()*(x.V.dat[i]-fx(x.A[0].dat[i]+tmin))**2 for i in range ( 0, 20+1 ) )/x.V.sigma2/sum(Gr.mu0[i]() for i in range ( 0, 20+1 ) ))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tsum(Gr.mu0[i]()*(x.V.dat[i]-fx(x.A[0].dat[i]+tmin))**2 for i in range ( 0, 20+1 ) )/x.V.sigma2/sum(Gr.mu0[i]() for i in range ( 0, 20+1 ) ) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tsum(Gr.mu0[i]()*(x.V.dat[i]-fx(x.A[0].dat[i]+tmin))**2 for i in range ( 0, 20+1 ) )/x.V.sigma2/sum(Gr.mu0[i]() for i in range ( 0, 20+1 ) ) ='+ stmp+'\n')
    tmp = (Penal[0]*sum ( (int(i__T!=tmin+step)+int(i__T!=tmax-step))/2*T.step*(((fx((i__T+T.step))+fx((i__T-T.step))-2*fx(i__T))/T.step**2))**2 for i__T in myrange (tmin+step,tmax-step,T.step) )/14.5)
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tPenal[0]*sum ( (int(i__T!=tmin+step)+int(i__T!=tmax-step))/2*T.step*(((fx((i__T+T.step))+fx((i__T-T.step))-2*fx(i__T))/T.step**2))**2 for i__T in myrange (tmin+step,tmax-step,T.step) )/14.5 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tPenal[0]*sum ( (int(i__T!=tmin+step)+int(i__T!=tmax-step))/2*T.step*(((fx((i__T+T.step))+fx((i__T-T.step))-2*fx(i__T))/T.step**2))**2 for i__T in myrange (tmin+step,tmax-step,T.step) )/14.5 ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

SvF.lenPenalty = 1

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
Task.Draw ( 'x' )