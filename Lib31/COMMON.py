# -*- coding: UTF-8 -*-
from sys  import float_info
#from Object import *   #################################  НИ КАКОГО  ИМПОРТА!


#setPref = 's_'
funPrefix = 'f_'
Prefix   = ''

comment_buf = ''
StartModel_pos = 0   #  кол-во записанных символов в последней строке
platform = 'Lin'

ModelBuf    = None   #  if  ==1 :  >> Null
SModelFile  = None


Compile = False  # True      # 30 при подготовке модели включен, при рассчетах выключен

addStrToRes = ''

EofTask         = False

SvFprefix       = ''    # 29
TabString       = '    '

Use_var = False         # 29

MarkerSize     = 1
MarkerColor    = 'red'
DataColor      = 'b'
DataMarkerSize = 2
Draw_data_str  = 'data'
Ylabel_x       = 0.03
Xlabel_x        = 1

LineWidth      = 1
LineColor      = 'red'
DrawTransp     = False
Legend         = True
DPI             = 100
Xsize           = 5
Ysize           = 4
X_axe           = ''

graphic_file_type = 'png'
#TranspGrid  = 'N'
#SaveDeriv   = False
#SaveGrid    = 'N'

optEstim = float_info.max

SchemeD1  = ['Forward'] # 'Backward'  #'Central'  #
#DIF1 = 'Forward' # 'Backward'  #'Central'  #  # Central  Backward
UseHomeforPower = False #True   # 29
#ReadFrom = ''


printL       = 0
SavePoints   = False

Version  = 63
DataPath = ''  

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
teachSet     = []           #  teachSet содержит кого выбрасываем
CV_NoR       = 0

Task        = None
TaskName    = 'NoName'

curentTabl  = None

useNaN      = False
VarNormalization = False

optFact          = None
token      =  ''
optFile    =  'peipopt.opt'

LocalSolverName  = 'ipopt' #3_11_1'
SolverName       = 'ipopt'
#RunSolver   = 'Local'   #   LocalParallel   ServerParallel
RunMode     = 'L&L'
#RunMode     = 'P+P'
Hack_Stab   = False
py_max_iter = 50000
py_tol = 1e-9  #  -11
#acceptable_tol
py_warm_start_bound_push = 1e-6
py_warm_start_mult_bound_push = 1e-6
py_constr_viol_tol = 1e-4  ##1e-11
#py_tol = 1e-9
#py_warm_start_bound_push = 1e-6
#py_warm_start_mult_bound_push = 1e-6
#py_constr_viol_tol = 1e-4

path_SvF   = ''  #"/home/sokol/C/_SvF/"
tmpFileDir = ''  #'C:\\C\\_SvF\\TMP\\'
startDir   = ''

###########################  AZIMUT  #########################
lon_center_rad = None
lat_center_rad = None
sin_lat_center_rad = None
cos_lat_center_rad = None

LastGrid = None

