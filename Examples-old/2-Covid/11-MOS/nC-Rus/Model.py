
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
 											# nCR(t)>=0;
    nCR = Funs[0];  nCR__f = nCR
    nCR__i = Var ( Funs[0].A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    nCR.var = nCR__i ; Gr.nCR =  nCR__i
    nCR.InitByData()
    def fnCR(t) : return nCR__f.F([t])

    nCR.mu = Gr.mu; nCR.testSet = co.testSet; nCR.teachSet = co.teachSet;
 											# nCR.MSDnan()+nCR.ComplSig2([Penal[0]])
    def obj_expression(Gr):  
        return (
             nCR.MSDnan()+nCR.ComplSig2([Penal[0]])
        )  
    Gr.OBJ = Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    nCR = Task.Funs[0]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (nCR.MSDnan())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tnCR.MSDnan() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tnCR.MSDnan() ='+ stmp+'\n')
    tmp = (nCR.ComplSig2([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tnCR.ComplSig2([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tnCR.ComplSig2([Penal[0]]) ='+ stmp+'\n')

    return
