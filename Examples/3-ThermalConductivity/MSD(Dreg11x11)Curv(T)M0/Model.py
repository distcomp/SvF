
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

    T.var = py.Var ( T.A[0].NodS,T.A[1].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    Gr.T =  T.var
    T.InitByData()
    def fT(x,t) : return T.F([x,t])

    φ.var = py.Var ( φ.A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    Gr.φ =  φ.var
    φ.InitByData()
    def fφ(x) : return φ.F([x])

    l.var = py.Var ( l.A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    Gr.l =  l.var
    l.InitByData()
    def fl(t) : return l.F([t])

    r.var = py.Var ( r.A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    Gr.r =  r.var
    r.InitByData()
    def fr(t) : return r.F([t])

    K.var = py.Var ( range (8), initialize = 0 )
    Gr.K =  K.var
    def fK(sT) : return K.F([sT])
    K.var[0].value = 1
 											# K(sT)>=0
    def EQ0 (Gr,i__sT) :
        return (
          fK(i__sT)>=0
        )
    Gr.conEQ0 = py.Constraint(sT.FlNodS,rule=EQ0 )
 											# K(sT)<=10
    def EQ1 (Gr,i__sT) :
        return (
          fK(i__sT)<=10
        )
    Gr.conEQ1 = py.Constraint(sT.FlNodS,rule=EQ1 )
 											# \frac{d}{d t}(T)=K(T)*\frac{d^2}{d x^2}(T)+\frac{d}{d T}(K(T))*(\frac{d}{d x}(T))**2
    def EQ2 (Gr,i__x,i__t) :
        return (
          ((fT(i__x,i__t)-fT(i__x,(i__t-t.step)))/t.step)==fK(fT(i__x,i__t))*((fT((i__x+x.step),i__t)+fT((i__x-x.step),i__t)-2*fT(i__x,i__t))/x.step**2)+(K.dF_dX(fT(i__x,i__t)))*(((fT(i__x,i__t)-fT((i__x-x.step),i__t))/x.step))**2
        )
    Gr.conEQ2 = py.Constraint(x.mFlNodSm,t.mFlNodS,rule=EQ2 )
 											# T(0,t)=l(t)
    def EQ3 (Gr,i__t) :
        return (
          fT(0,i__t)==fl(i__t)
        )
    Gr.conEQ3 = py.Constraint(t.FlNodS,rule=EQ3 )
 											# T(2,t)=r(t)
    def EQ4 (Gr,i__t) :
        return (
          fT(2,i__t)==fr(i__t)
        )
    Gr.conEQ4 = py.Constraint(t.FlNodS,rule=EQ4 )
 											# T(x,0)=φ(x)
    def EQ5 (Gr,i__x) :
        return (
          fT(i__x,0)==fφ(i__x)
        )
    Gr.conEQ5 = py.Constraint(x.FlNodS,rule=EQ5 )

    T.mu = Gr.mu; T.testSet = SvF.testSet; T.teachSet = SvF.teachSet;
 											# T.ComplSig2([Penal[0],Penal[1]])+T.MSD()
    def obj_expression(Gr):  
        return (
             T.ComplSig2([Penal[0],Penal[1]])+T.MSD()
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    T = Task.Funs[0]

    l = Task.Funs[2]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (T.ComplSig2([Penal[0],Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tT.ComplSig2([Penal[0],Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tT.ComplSig2([Penal[0],Penal[1]]) ='+ stmp+'\n')
    tmp = (T.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tT.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tT.MSD() ='+ stmp+'\n')

    return
