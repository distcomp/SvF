
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
 											# nCMO(t)>=0;
    nCMO = Funs[0];  nCMO__f = nCMO
    nCMO__i = Var ( Funs[0].A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    nCMO.var = nCMO__i ; Gr.nCMO =  nCMO__i
    nCMO.InitByData()
    def fnCMO(t) : return nCMO__f.F([t])

    nCMO.mu = Gr.mu; nCMO.testSet = co.testSet; nCMO.teachSet = co.teachSet;
 											# nCMO.MSDnan()+nCMO.ComplSig2([Penal[0]])
    def obj_expression(Gr):  
        return (
             nCMO.MSDnan()+nCMO.ComplSig2([Penal[0]])
        )  
    Gr.OBJ = Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    nCMO = Task.Funs[0]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (nCMO.MSDnan())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tnCMO.MSDnan() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tnCMO.MSDnan() ='+ stmp+'\n')
    tmp = (nCMO.ComplSig2([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tnCMO.ComplSig2([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tnCMO.ComplSig2([Penal[0]]) ='+ stmp+'\n')

    return
