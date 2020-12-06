
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

    V = Task.Grids[2]
 											# x(t)
    x = Funs[0];  x__f = x
    x__i = Var ( Funs[0].A[0].NodS,domain=Reals, initialize = 1 )
    x.grd = x__i ; Gr.x =  x__i
    x.InitByData()
    def fx(t) : return x__f.F([t])
 											# v(t)
    v = Funs[1];  v__f = v
    v__i = Var ( Funs[1].A[0].NodS,domain=Reals, initialize = 1 )
    v.grd = v__i ; Gr.v =  v__i
    v.InitByData()
    def fv(t) : return v__f.F([t])
 											# f(X,V); PolyPow=6
    f = Funs[2];  f__f = f
    f__i = Var ( range (PolySize(2,6) ), initialize = 0 )
    f.grd = f__i ; Gr.f =  f__i
    def ff(X,V) : return f.F([X,V])
    f__i[0].value = 1
 											# d2/dt2(x)==f(x,v)
    def EQ0 (Gr,i__t) :
        return (
          ((fx((i__t+t.step))+fx((i__t-t.step))-2*fx(i__t))/t.step**2)==ff(fx(i__t),fv(i__t))
        )
    Gr.conEQ0 = Constraint(t.mFlNodSm,rule=EQ0 )
 											# v== d/dt(x)
    def EQ1 (Gr,i__t) :
        return (
          fv(i__t)==((fx((i__t+t.step))-fx(i__t))/t.step)
        )
    Gr.conEQ1 = Constraint(t.FlNodSm,rule=EQ1 )

    x.mu = Gr.mu; x.testSet = co.testSet; x.teachSet = co.teachSet
 											# f.Complexity([Penal[0],Penal[1]])/x.V.sigma2+x.MSD()
    def obj_expression(Gr):  
        return (
             f.Complexity([Penal[0],Penal[1]])/x.V.sigma2+x.MSD()
        )  
    Gr.OBJ = Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x = Task.Funs[0]

    f = Task.Funs[2]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (f.Complexity([Penal[0],Penal[1]])/x.V.sigma2)()
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tf.Complexity([Penal[0],Penal[1]])/x.V.sigma2 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tf.Complexity([Penal[0],Penal[1]])/x.V.sigma2 ='+ stmp+'\n')
    tmp = (x.MSD())()
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.MSD() ='+ stmp+'\n')

    return
