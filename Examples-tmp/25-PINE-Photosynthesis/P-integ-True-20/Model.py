
from __future__ import division
from  numpy import *

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr
    if SvF.CV_NoR > 0:
        Gr.mu = py.Param ( range(SvF.CV_NoR), mutable=True, initialize = 1 )

    P.var = py.Var ( P.A[0].NodS,P.A[1].NodS,domain=Reals, initialize = 1 )
    Gr.P =  P.var
    P.InitByData()
    def fP(Q,T) : return P.F([Q,T])

    P.mu = Gr.mu; P.testSet = SvF.testSet; P.teachSet = SvF.teachSet;
 											# P.Complexity([Penal[0],Penal[1]])+P.MSDnan()
    def obj_expression(Gr):  
        return (
             P.Complexity([Penal[0],Penal[1]])+P.MSDnan()
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
    tmp = (P.MSDnan())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tP.MSDnan() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tP.MSDnan() ='+ stmp+'\n')

    return
