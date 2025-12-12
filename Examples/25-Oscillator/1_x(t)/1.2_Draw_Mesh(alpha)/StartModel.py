# -*- coding: UTF-8 -*-
import sys
path_SvF = "/home/sokol/D/SvF/"
sys.path.append("/home/sokol/D/SvF/SvFlib")
sys.path.append(path_SvF + "pyomo-everest/python-api")
sys.path.append(path_SvF + "pyomo-everest/ssop")
import COMMON as SvF
SvF.path_SvF = path_SvF
SvF.tmpFileDir = SvF.path_SvF + 'TMP/'
from CVSets import *
from Table  import *
from Task   import *
from MakeModel import *
from GIS import *

SvF.Task = TaskClass()
Task = SvF.Task
SvF.mngF = 'MNG-Draw_alpha.mng'
SvF.CVNumOfIter = 0
D = Table ( 'CV(alpha).dat','D','*' )
for d in D.sR:
  print(D.dat('alpha')[d],sqrt(D.dat('CV')[d]**2-D.dat('delta')[d]**2),(D.dat('CV')[d]**2-D.dat('delta')[d]**2))
alpha = Set('alpha',SvF.currentTab.dat('alpha')[:].min(),SvF.currentTab.dat('alpha')[:].max(),-50,'','alpha')
CV = Fun('CV',[alpha])
def fCV(alpha) : return CV.F([alpha])
SD = Fun('SD',[alpha])
def fSD(alpha) : return SD.F([alpha])
delta = Fun('delta',[alpha])
def fdelta(alpha) : return delta.F([alpha])
import  numpy as np

from Lego import *
import pyomo.environ as py

def createGr ( Task, Penal ) :
    Funs = Task.Funs
    Gr = py.ConcreteModel()
    Task.Gr = Gr

    CV.var = py.Var ( CV.A[0].NodS,domain=Reals )
    CV.gr =  CV.var
    Gr.CV =  CV.var

    SD.var = py.Var ( SD.A[0].NodS,domain=Reals )
    SD.gr =  SD.var
    Gr.SD =  SD.var

    delta.var = py.Var ( delta.A[0].NodS,domain=Reals )
    delta.gr =  delta.var
    Gr.delta =  delta.var

    make_CV_Sets(0, SvF.CVstep)

    if len (SvF.CV_NoRs) > 0 :

       Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )
    SvF.fun_with_mu.append(getFun('CV'))
    if CV.mu is None : CV.mu = Gr.mu0
    CV.ValidationSets = SvF.ValidationSets
    CV.notTrainingSets = SvF.notTrainingSets
    CV.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('SD'))
    if SD.mu is None : SD.mu = Gr.mu0
    SD.ValidationSets = SvF.ValidationSets
    SD.notTrainingSets = SvF.notTrainingSets
    SD.TrainingSets = SvF.TrainingSets
    SvF.fun_with_mu.append(getFun('delta'))
    if delta.mu is None : delta.mu = Gr.mu0
    delta.ValidationSets = SvF.ValidationSets
    delta.notTrainingSets = SvF.notTrainingSets
    delta.TrainingSets = SvF.TrainingSets
 											# CV.MSD()+CV.Complexity([Penal[0]])+SD.MSD()+SD.Complexity([Penal[0]])+delta.MSD()+delta.Complexity([Penal[0]])
    def obj_expression(Gr):  
        return (
             CV.MSD()+CV.Complexity([Penal[0]])+SD.MSD()+SD.Complexity([Penal[0]])+delta.MSD()+delta.Complexity([Penal[0]])
        )  
    Gr.OBJ = py.Objective(rule=obj_expression)  

    return Gr

def print_res(Task, Penal, f__f):

    Gr = Task.Gr

    CV = Task.Funs[0]

    SD = Task.Funs[1]

    delta = Task.Funs[2]

    OBJ_ = Gr.OBJ ()
    print (  '    OBJ =', OBJ_ )
    f__f.write ( '\n    OBJ ='+ str(OBJ_)+'\n')
    tmp = (CV.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tCV.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tCV.MSD() ='+ stmp+'\n')
    tmp = (CV.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tCV.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tCV.Complexity([Penal[0]]) ='+ stmp+'\n')
    tmp = (SD.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tSD.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tSD.MSD() ='+ stmp+'\n')
    tmp = (SD.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tSD.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tSD.Complexity([Penal[0]]) ='+ stmp+'\n')
    tmp = (delta.MSD())
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tdelta.MSD() =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tdelta.MSD() ='+ stmp+'\n')
    tmp = (delta.Complexity([Penal[0]]))
    stmp = str(tmp)
    print (      '    ',int(tmp/OBJ_*1000)/10,'\tdelta.Complexity([Penal[0]]) =', stmp )
    f__f.write ( '    '+str(int(tmp/OBJ_*1000)/10)+'\tdelta.Complexity([Penal[0]]) ='+ stmp+'\n')

    return


SvF.Task.createGr  = createGr

SvF.Task.Delta = None

SvF.Task.DeltaVal = None

SvF.Task.defMSD = None

SvF.Task.defMSDVal = None

SvF.Task.print_res = print_res

from SvFstart62 import SvFstart19

SvFstart19 ( Task )
CV.V.dat=None
SD.V.dat=None
delta.V.dat=None
delta.V.draw_name = '%'
delta.A[0].oname = 'α'
delta.V.oname = 'SDz'
Task.Draw ( 'CV;MS:0 SD;LC:blue delta;LC:green' )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")