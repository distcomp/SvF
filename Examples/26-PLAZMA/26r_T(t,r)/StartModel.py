# -*- coding: UTF-8 -*-
import sys
sys.path.append("/home/sokol/D/SvF/SvFlib")
sys.path.append( "/home/sokol/D/SvF/pyomo-everest/python-api")
sys.path.append( "/home/sokol/D/SvF/pyomo-everest/ssop")
import COMMON as SvF
SvF.tmpFileDir = "/home/sokol/D/SvF/TMP/"
from CVSets import *
from Table  import *
from Task   import *
from MakeModel import *
from GIS import *

SvF.Task = TaskClass()
Task = SvF.Task
SvF.mngF = 'MNG_T.mng'
SvF.Compile = False

SvF.maxJobs=1
SvF.SchemeD1 = "Backward"
Dat = Table ( '../combined_Te_data_sn_26r.txt','Dat','s,t_tot AS t,rho AS r,T,ROWNUM' )
t_old=0
r_old=0
for r in Dat.sR:
  if Dat.dat('t')[r]!=t_old:
    print(r,Dat.dat('s')[r-1],Dat.dat('s')[r],Dat.dat('t')[r]-t_old,r-r_old)
    if((Dat.dat('t')[r]-t_old>0.0032)or(Dat.dat('t')[r]-t_old<0.0029)):
      print('****************')
    t_old=Dat.dat('t')[r]
    r_old=r
Ntime=int(Dat.NoR/9.)
print(Ntime)
r = Set('r',SvF.currentTab.dat('r')[:].min(),SvF.currentTab.dat('r')[:].max(),-25,'','r')
t = Set('t',0,SvF.currentTab.dat('t')[:].max(),0.000999999,'','t')
T = Fun('T',[t,r])
T.AddGap( )
def fT(t,r) : return T.F([t,r])
s_old=Dat.dat('s')[0]
for _ir in Dat.sR:
  if(s_old==Dat.dat('s')[_ir]):continue
  ni=0
  for ti in t.NodS:
    if(t.Val[ti]>=Dat.dat('t')[_ir-1])and(t.Val[ti]<=Dat.dat('t')[_ir]):
      T.gap[ti,:]=0
      ni+=1
  if(ni!=3):print(_ir,ni)
  if ni<3:
    print("step between s too small")
    exit(-1)
  s_old=Dat.dat('s')[_ir]
CVmakeSets (  CV_NumSets=5, GroupBy='t' )
SvF.CVNumOfIter=-1; SvF.RunMode="S&S"; 
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    T.var = py.Var ( T.A[0].NodS,T.A[1].NodS,domain=Reals, bounds=(0,None) )
    T.gr =  T.var
    Gr.T =  T.var

    if len (SvF.CV_NoRs) > 0 :
        Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('T'))
    if T.mu is None : T.mu = Gr.mu0
    T.ValidationSets = SvF.ValidationSets
    T.notTrainingSets = SvF.notTrainingSets
    T.TrainingSets = SvF.TrainingSets
 											# T.Compl([Penal[0],Penal[1]])+T.MSD()
    def obj_expression(Gr):  
        return (
             T.Compl([Penal[0],Penal[1]])+T.MSD()
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    T = Task.Funs[0]

    OBJ_ = SvF.optOBJ
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (T.Compl([Penal[0],Penal[1]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tT.Compl([Penal[0],Penal[1]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tT.Compl([Penal[0],Penal[1]]) ='+ stmp+'\n')
    tmp = (T.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tT.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tT.MSD() ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
for ti in t.mNodSm:
  if T.gap[ti-1,1]==0 and T.gap[ti,1]==0 and T.gap[ti+1,1]==0:
    T.grd[ti,:]=None
SvF.CommaFormatter=True
SvF.Xsize=30
SvF.Ysize=13
SvF.LEVEL_FONT_SIZE=0
Plot( [ [ T, 'dms=1.2', 'xlab_x=1.02', 'xlab_y=0.03', 'ylab_x=0', 'ylab_y=1.04', "ylab='ρ'", 'tlab_x=1.08', "tlab='T, keV'"] ] )
SvF.X_lim=[0,1]
Plot( [ [ T, 'dms=1.2', 'lw=1', 'xlab_x=1.02', 'xlab_y=0.03', 'ylab_x=0', 'ylab_y=1.04', "ylab='ρ'", 'tlab_x=1.08', "tlab='T, keV'", 'file="T_0_1"'] ] )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")
if SvF.addStrToRes != '':
    with open(SvF.resF, 'a') as f:  # RES filewrite
        f.write('addStrToRes: ' + SvF.addStrToRes)