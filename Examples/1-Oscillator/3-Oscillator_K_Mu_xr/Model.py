
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
    x.grd = x__i ; Gr.x =  x__i
    x.InitByData()
    def fx(t) : return x__f.F([t])
 											# v(t)
    v = Funs[1];  v__f = v
    v__i = Var ( Funs[1].A[0].NodS,domain=Reals, initialize = 1 )
    v.grd = v__i ; Gr.v =  v__i
    v.InitByData()
    def fv(t) : return v__f.F([t])
 											# K
    K = Funs[2];  K__f = K
    K__i = Var ( domain=Reals, initialize = 1 )
    K.grd = K__i ; Gr.K =  K__i
    K.InitByData()
    fK = K__i
 											# Deltax
    Deltax = Funs[3];  Deltax__f = Deltax
    Deltax__i = Var ( domain=Reals, initialize = 1 )
    Deltax.grd = Deltax__i ; Gr.Deltax =  Deltax__i
    Deltax.InitByData()
    fDeltax = Deltax__i
 											# muu
    muu = Funs[4];  muu__f = muu
    muu__i = Var ( domain=Reals, initialize = 1 )
    muu.grd = muu__i ; Gr.muu =  muu__i
    muu.InitByData()
    fmuu = muu__i

    x.mu = Gr.mu; x.testSet = co.testSet; x.teachSet = co.teachSet
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
    tmp = (x.Complexity([Penal[0]])/x.V.sigma2)()
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.Complexity([Penal[0]])/x.V.sigma2 =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.Complexity([Penal[0]])/x.V.sigma2 ='+ stmp+'\n')
    tmp = (x.MSD())()
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tx.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tx.MSD() ='+ stmp+'\n')

    return
