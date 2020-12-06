# -*- coding: UTF-8 -*-
from sys  import float_info

MarkerSize     = 1
MarkerColor    = 'red'
DataMarkerSize = 2
DataLineWidth  = 0
LineWidth      = 1
LineColor      = 'red'
DrawTransp     = False


#TranspGrid  = 'N'
#SaveDeriv   = False
#SaveGrid    = 'N'


optEstim = float_info.max

DIF1 = 'Forward'  # Central  Backward
UseHomeforPower = False #True
ReadFrom = ''

#Preproc = False
Preproc = True

printL       = 0
SavePoints   = False

Version  = 63
DataPath = ''  
funPrefix = 'f'
Prefix   = ''

mngF = ''
resF = ''

ExitStep     =   1e-7
OptStep      = '0.01'

lenPenalty   = 0
Penalty      = [.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1,.1]
mngPenalty   = []

#CVproc       = ''
CVNumOfIter  =   20
CVparam      = ''
#CVmargin     = 0
CVpartSize   = 0
CVside = 0
CVstep       = 7  
CV_NoSets    = 0
CVNoBorder    = False
NotCulcBorder = False

testSet      = []
teachSet     = []
CV_NoR       = 0



#from Task import *

Task        = None
TaskName    = 'NoName'

#MakeModel   = True
ModelFile   = None   #  if  ==1 :  >> Null
SModelFile  = None

curentTabl  = None
#numNaN      = False
useNaN      = False
VarNormalization = False

optFact          = None
token      =  ''
optFile    =  'peipopt.opt'

LocalSolverName  = 'ipopt' #3_11_1'
SolverName       = 'ipopt'
#RunSolver   = 'Local'   #   LocalParallel   ServerParallel
RunMode     = 'L+L'
Hack_Stab   = False
py_max_iter = 50000
py_tol = 1e-9
py_warm_start_bound_push = 1e-6
py_warm_start_mult_bound_push = 1e-6
py_constr_viol_tol = 1e-4

path_SvF   = ''  #"/home/sokol/C/_SvF/"
tmpFileDir = ''  #'C:\\C\\_SvF\\TMP\\'

###########################  AZIMUT  #########################
lon_center_rad = None
lat_center_rad = None
sin_lat_center_rad = None
cos_lat_center_rad = None

LastGrid = None

