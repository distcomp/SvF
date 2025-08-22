
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
 											# x(t)
    x = Funs[0];  x__f = x
    x__i = Var ( Funs[0].A[0].NodS,domain=Reals, initialize = 1 )
    x.var = x__i ; Gr.x =  x__i
    x.InitByData()
    def fx(t) : return x__f.F([t])
 											# v(t)
    v = Funs[1];  v__f = v
    v__i = Var ( Funs[1].A[0].NodS,domain=Reals, initialize = 1 )
    v.var = v__i ; Gr.v =  v__i
    v.InitByData()
    def fv(t) : return v__f.F([t])
 											# K
    K = Funs[2];  K__f = K
    K__i = Var ( domain=Reals, initialize = 1 )
    K.var = K__i ; Gr.K =  K__i
    K.InitByData()
    fK = K__i
 											# Deltax
    Deltax = Funs[3];  Deltax__f = Deltax
    Deltax__i = Var ( domain=Reals, initialize = 1 )
    Deltax.var = Deltax__i ; Gr.Deltax =  Deltax__i
    Deltax.InitByData()
    fDeltax = Deltax__i
 											# muu
    muu = Funs[4];  muu__f = muu
    muu__i = Var ( domain=Reals, initialize = 1 )
    muu.var = muu__i ; Gr.muu =  muu__i
    muu.InitByData()
    fmuu = muu__i
 											# \frac{d^2}{dt^2}(x)==-K*( x-Delta x)-muu*v
    def EQ0 (Gr,i__t) :
        return (
          ((fx((i__t+t.step))+fx((i__t-t.step))-2*fx(i__t))/t.step**2)==-fK*(fx(i__t)-fDeltax)-fmuu*fv(i__t)
        )
    Gr.conEQ0 = Constraint(t.mFlNodSm,rule=EQ0 )
 											# v== \frac{d}{dt}(x)
    def EQ1 (Gr,i__t) :
        return (
          fv(i__t)==((fx((i__t+t.step))-fx((i__t-t.step)))/t.step *0.5)
        )
    Gr.conEQ1 = Constraint(t.mFlNodSm,rule=EQ1 )

    x.mu = Gr.mu; x.testSet = co.testSet; x.teachSet = co.teachSet;
 											# x.Complexity([Penal[0]])/x.V.sigma2+x.MSD()
    def obj_expression(Gr):  
        return (
             x.Complexity([Penal[0]])/x.V.sigma2+x.MSD()
        )  
    Gr.OBJ = Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    x = Task.Funs[0]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (x.Complexity([Penal[0]])/x.V.sigma2)
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.Complexity([Penal[0]])/x.V.sigma2 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.Complexity([Penal[0]])/x.V.sigma2 ='+ stmp+'\n')
    tmp = (x.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.MSD() ='+ stmp+'\n')

    return
