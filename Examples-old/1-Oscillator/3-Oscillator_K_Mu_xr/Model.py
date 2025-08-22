
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

    x.var = py.Var ( x.A[0].NodS,domain=Reals, initialize = 1 )
    Gr.x =  x.var
    x.InitByData()
    def fx(t) : return x.F([t])

    v.var = py.Var ( v.A[0].NodS,domain=Reals, initialize = 1 )
    Gr.v =  v.var
    v.InitByData()
    def fv(t) : return v.F([t])

    K.var = py.Var ( domain=Reals, initialize = 1 )
    Gr.K =  K.var
    K.InitByData()
    fK = K.var

    muu.var = py.Var ( domain=Reals, initialize = 1 )
    Gr.muu =  muu.var
    muu.InitByData()
    fmuu = muu.var

    xr.var = py.Var ( domain=Reals, initialize = 1 )
    Gr.xr =  xr.var
    xr.InitByData()
    fxr = xr.var
 											# \frac{d^2}{dt^2}(x)==-K*( x-xr)-muu*v
    def EQ0 (Gr,i__t) :
        return (
          ((fx((i__t+t.step))+fx((i__t-t.step))-2*fx(i__t))/t.step**2)==-fK*(fx(i__t)-fxr)-fmuu*fv(i__t)
        )
    Gr.conEQ0 = py.Constraint(t.mFlNodSm,rule=EQ0 )
 											# v== \frac{d}{dt}(x)
    def EQ1 (Gr,i__t) :
        return (
          fv(i__t)==((fx((i__t+t.step))-fx((i__t-t.step)))/t.step *0.5)
        )
    Gr.conEQ1 = py.Constraint(t.mFlNodSm,rule=EQ1 )

    x.mu = Gr.mu; x.testSet = SvF.testSet; x.teachSet = SvF.teachSet;
 											# x.Complexity([Penal[0]])/x.V.sigma2+x.MSD()
    def obj_expression(Gr):  
        return (
             x.Complexity([Penal[0]])/x.V.sigma2+x.MSD()
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

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
