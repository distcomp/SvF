
from __future__ import division
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
 											# nT(t)>=0;nT(tMaxData-1)=nT(tMaxData)
    nT = Funs[0];  nT__f = nT
    nT__i = Var ( Funs[0].A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    nT.var = nT__i ; Gr.nT =  nT__i
    nT.InitByData()
    def fnT(t) : return nT__f.F([t])
 											# nT(tMaxData-1)=nT(tMaxData)
    def EQ0 (Gr) :
        return (
          fnT(tMaxData-1)==fnT(tMaxData)
        )
    Gr.conEQ0 = Constraint(rule=EQ0 )

    nT.mu = Gr.mu; nT.testSet = co.testSet; nT.teachSet = co.teachSet;
 											# nT.MSDnan()+nT.ComplSig2([Penal[0]])
    def obj_expression(Gr):  
        return (
             nT.MSDnan()+nT.ComplSig2([Penal[0]])
        )  
    Gr.OBJ = Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    nT = Task.Funs[0]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (nT.MSDnan())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tnT.MSDnan() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tnT.MSDnan() ='+ stmp+'\n')
    tmp = (nT.ComplSig2([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tnT.ComplSig2([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tnT.ComplSig2([Penal[0]]) ='+ stmp+'\n')

    return
