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
SvF.OptStep = [-0.0000406246898655751,-0.010]
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
Tt = Fun('Tt',[t])
Tt.AddGap( )
def fTt(t) : return Tt.F([t])
Tr = Fun('Tr',[r])
def fTr(r) : return Tr.F([r])
T = smbFun('T',[t,r])
T.AddGap( )
def fT(t,r) : return T.F([t,r])
def T_smbF00(Args) :
   t = Args[0]
   r = Args[1]
   SvF.F_Arg_Type = "N"
   ret = fTt(t)+fTr(r)
   SvF.F_Arg_Type = ""
   return ret
T.smbF = T_smbF00
s_old=Dat.dat('s')[0]
for _ir in Dat.sR:
  if(s_old==Dat.dat('s')[_ir]):continue
  ni=0
  for ti in t.NodS:
    if(t.Val[ti]>=Dat.dat('t')[_ir-1])and(t.Val[ti]<=Dat.dat('t')[_ir]):
      Tt.gap[ti]=0
      T.gap[ti,:]=0
      ni+=1
  if ni!=3:print(_ir,ni)
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

    Tt.var = py.Var ( Tt.A[0].NodS,domain=Reals, bounds=(0,None) )
    Tt.gr =  Tt.var
    Gr.Tt =  Tt.var

    Tr.var = py.Var ( Tr.A[0].NodS,domain=Reals, bounds=(0,None) )
    Tr.gr =  Tr.var
    Gr.Tr =  Tr.var
 								# d/dr(Tr(r))<=0
    def EQ0 (Gr,_ir) :
        return (
          Tr.by_x(_ir)<=0
        )
    Gr.conEQ0 = py.Constraint(r.FlNodSm,rule=EQ0 )

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

    T = Task.Funs[2]

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
  if Tt.gap[ti-1]==0 and Tt.gap[ti]==0 and Tt.gap[ti+1]==0:
    Tt.grd[ti]=nan
    T.grd[ti,:]=nan
SvF.CommaFormatter=True
Plot( [ [ Tr, "xlab='ρ'", "ylab='Aρ'", "lab='Aρ'"] ] )
SvF.Xsize=30
SvF.Ysize=13
SvF.LEVEL_FONT_SIZE=0
Plot( [ [ T, 'dms=1.2', 'xlab_x=1.02', 'xlab_y=0.03', 'ylab_x=0', 'ylab_y=1.04', "ylab='ρ'", 'tlab_x=1.08', "tlab='T, keV'"] ] )
Plot( [ [ Tt, "ylab='At'", "lab='At'", 'xlab_y=0.07', 'xlab_x=0.96'] ] )
SvF.X_lim=[0,1]
Plot( [ [ T, 'dms=1.2', 'lw=1', 'xlab_x=1.02', 'xlab_y=0.03', 'ylab_x=0', 'ylab_y=1.04', "ylab='ρ'", 'tlab_x=1.08', "tlab='T, keV'", 'file="T_0_1"'] ] )
Plot( [ [ Tt, "ylab='At'", "lab='At'", 'xlab_y=0.07', 'xlab_x=0.96', 'file="Tt_0_1"'] ] )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")
if SvF.addStrToRes != '':
    with open(SvF.resF, 'a') as f:  # RES filewrite
        f.write('addStrToRes: ' + SvF.addStrToRes)