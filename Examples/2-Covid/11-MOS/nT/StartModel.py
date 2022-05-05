# -*- coding: UTF-8 -*-
import sys
import platform
LibVersion = 'Lib29'
if platform.system() == 'Windows':
    path_SvF = "C:/_SvF/"
else:
    path_SvF = "/home/sokol/C/SvF/"
sys.path.append(path_SvF + LibVersion)
sys.path.append(path_SvF + "Everest/python-api")
sys.path.append(path_SvF + "pyomo-everest/ssop")
import COMMON as co
co.path_SvF = path_SvF
co.tmpFileDir = co.path_SvF + 'TMP/'
from CVSets import *
from Table  import *
from Task   import *
from MakeModel import *
from GIS import *

co.Task = TaskClass()
Task = co.Task
co.mngF = 'MNG-3Task.odt'
co.Preproc = False
co.TaskName = 'COVID-RUS-NT'
 											# CVNumOfIter     7
co.CVNumOfIter = 7
 											# Runmode = 'L&L'
co.RunMode = 'L&L'
 											# co.resF = 'MNG-nT.res'
co.resF='MNG-nT.res'
Task.AddDef('co.resF',['MNG-nT.res'])
 											# Popul = 12636312.
Popul=12636312.
Task.AddDef('Popul',[12636312.])
 											# PopulMln = Popul / 1000000.
PopulMln=Popul/1000000.
Task.AddDef('PopulMln',[Popul/1000000.])
 											# PopulContrMln = (145934460-Popul)/1000000.
PopulContrMln=(145934460-Popul)/1000000.
 											# proVucc  = 12000.0 /Popul #*  доля
proVucc=12000.0/Popul
Task.AddDef('proVucc',[12000.0/Popul])
 											# #proVucc  = 20000.0 /Popul #*  доля
 											# effVucc  = 0.916  #0.976
effVucc=0.916
Task.AddDef('effVucc',[0.916])
 											# timeVucc = 14
timeVucc=14
Task.AddDef('timeVucc',[14])
 											# begDate = 20200319
begDate=20200319
Task.AddDef('begDate',[20200319])
 											# endDate = 20211201
endDate=20211201
Task.AddDef('endDate',[20211201])
 											# #proDate = 20220101
 											# proDate = 20220503
proDate=20220503
Task.AddDef('proDate',[20220503])
 											# useNaN = True
co.useNaN = True
 											# DataAll = Select nCMos As nC, nCRus as nCR, ROWNUM AS t, date, Anti, nTest as nT, Exch  from ../../Moscow.xlsx \
 											# DataAll = Select nCMos As nC, nCRus as nCR, ROWNUM AS t, date, Anti, nTest as nT, Exch  from ../../Moscow.xlsx                                             where date >= begDate and date <= proDate
DataAll=Select ( 'Select nCMos As nC,nCRus as nCR,ROWNUM AS t,date,Anti,nTest as nT,Exch from ../../Moscow.xlsx As DataAll where date>= begDate and date<= proDate' )
 											# DataAll.nCR[:] = ( DataAll.nCR[:] - DataAll.nC[:] ) / PopulContrMln #* 3
DataAll.dat('nCR')[:]=(DataAll.dat('nCR')[:]-DataAll.dat('nC')[:])/PopulContrMln
 											# DataAll.nC[:] /= PopulMln
DataAll.dat('nC')[:]/=PopulMln
 											# DataAll.nT[:] /= (5*Popul/1000)
DataAll.dat('nT')[:]/=(5*Popul/1000)
 											# DataAll.Anti[:] /= 100
DataAll.dat('Anti')[:]/=100
 											# Interpolate (DataAll.Exch)
Interpolate(DataAll.dat('Exch'))
 											# Extrapolate (DataAll.Exch)
Extrapolate(DataAll.dat('Exch'))
 											# # INCLUDE:  get_data.mng
 											# Data = Select nT, t, date from DataAll where date <= endDate
Data=Select ( 'Select nT,t,date from DataAll As Data where date<= endDate' )
 											# tMaxData = int ( Data.t[-1] )
tMaxData=int(Data.dat('t')[-1])
 											# Set:    t ∈ [         ,   ,  1, ti  ]        # Time - number of point (first=0)
t=Grid('t',nan,nan,1.0,'ti','t')
Task.AddGrid(t)
 											# Var:    nT  ( t ) >= 0;   nT(tMaxData-1)=nT(tMaxData)
nT = Fun('nT',[t],False); 
Task.InitializeAddFun ( nT )
nT__f = nT
def fnT(t) : return nT.F([t])
 											# MakeSets_byParam t 9 2
SvF_MakeSets_byParam ( co.curentTabl.dat('t'), 9,2 )
 											# Obj:    nT.MSDnan() + nT.ComplSig2(Penal[0])from __future__ import division
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
 											# nT(t)>=0;nT(tMaxData-1)=nT(tMaxData)
    nT = Funs[0];  nT__f = nT
    nT__i = Var ( Funs[0].A[0].NodS,domain=Reals, bounds=(0,None), initialize = 1 )
    nT.var = nT__i ; Gr.nT =  nT__i
    nT.InitByData()
    def fnT(t) : return nT__f.F([t])
 											# nT(tMaxData-1)=nT(tMaxData)
    def EQ0 (Gr) :
        return (
          fnT(tMaxData-1)==fnT(tMaxData)
        )
    Gr.conEQ0 = Constraint(rule=EQ0 )

    nT.mu = Gr.mu; nT.testSet = co.testSet; nT.teachSet = co.teachSet;
 											# nT.MSDnan()+nT.ComplSig2([Penal[0]])
    def obj_expression(Gr):  
        return (
             nT.MSDnan()+nT.ComplSig2([Penal[0]])
        )  
    Gr.OBJ = Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    nT = Task.Funs[0]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (nT.MSDnan())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tnT.MSDnan() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tnT.MSDnan() ='+ stmp+'\n')
    tmp = (nT.ComplSig2([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tnT.ComplSig2([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tnT.ComplSig2([Penal[0]]) ='+ stmp+'\n')

    return


com.Task.createGr  = createGr

com.Task.print_res = print_res

co.lenPenalty = 1

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
 											# Draw

Task.Draw (  '' )
 											# #EOTask   ######################################################
 											# # INCLUDE:  ../nT/MNG-nT.odt
 											# EOTask   #-----------------------------------------------------