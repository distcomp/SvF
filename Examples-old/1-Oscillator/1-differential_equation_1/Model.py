
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

    X = Task.Grids[1]
 											# x(t)
    x = Funs[0];  x__f = x
    x__i = Var ( Funs[0].A[0].NodS,domain=Reals, initialize = 1 )
    x.var = x__i ; Gr.x =  x__i
    x.InitByData()
    def fx(t) : return x__f.F([t])
 											# f(X); PolyPow=5
    f = Funs[1];  f__f = f
    f__i = Var ( range (6), initialize = 0 )
    f.var = f__i ; Gr.f =  f__i
    def ff(X) : return f__f.F([X])
    f__i[0].value = 1
 											# d/dt(x)=f(x)
    def EQ0 (Gr,i__t) :
        return (
          ((fx((i__t+t.step))-fx(i__t))/t.step)==ff(fx(i__t))
        )
    Gr.conEQ0 = Constraint(t.FlNodSm,rule=EQ0 )

    x.mu = Gr.mu; x.testSet = co.testSet; x.teachSet = co.teachSet;
 											# x.MSD()+f.Complexity([Penal[0]])
    def obj_expression(Gr):  
        return (
             x.MSD()+f.Complexity([Penal[0]])
        )  
    Gr.OBJ = Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x = Task.Funs[0]

    f = Task.Funs[1]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (x.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.MSD() ='+ stmp+'\n')
    tmp = (f.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tf.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tf.Complexity([Penal[0]]) ='+ stmp+'\n')

    return
