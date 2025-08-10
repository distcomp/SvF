# -*- coding: UTF-8 -*-
from sys  import float_info
#from Object import *   #################################  НИ КАКОГО  ИМПОРТА!

#Sets = []
#Funs = []    #  Проблеммы с Funs
#Tbls = []
#Objects = []

feasibleSol = None          #  function feasibleSol(Peal) - перед оптимизацией
OptMode = 'SvF'
ObjectiveFun = None

UsePrime = False

max_workers = 3

jobId_s = []
maxJobs = 0

DrawMode = 'Screen&File'
DrawFileName = ''
Resources = [ "pool-scip-ipopt" ]
#Resources = [ "vvvolDellDocker" ]

Substitude = True
Default_step = -50
Epsilon = 0.001
ObjToReadSols = False
_Num = 0       #   номер увеличивается на 1
#setPref = 's_'
funPrefix = 'f'             #  в ReadMng добавить обработку
#funPrefix = 'f_'
Prefix   = ''
Comment = False              #  в ReadMng

UseGreek = False

comment_buf = ''
StartModel_pos = 0   #  кол-во записанных символов в последней строке
platform = 'Lin'

ModelBuf    = None   #  if  ==1 :  >> Null
SModelFile  = None
LogOutFile  = None

Compile = True      # 30 при подготовке модели включен, при рассчетах выключен

addStrToRes = ''

EofTask         = False

SvFprefix       = ''    # 29
TabString       = '    '

Use_var = False         # 29

#   Drow  #############################
CommaFormatter = False
MarkerSize     = 1
MarkerColor    = 'red'
DataColor      = 'b'
DataMarkerSize = 2
Draw_data_str  = 'data'

LineWidth      = 1
LineColor      = 'red'
DrawTransp     = False
Legend         = True
DPI             = 100
Xsize           = 5
Ysize           = 4
X_axe           = ''
X_axe_month     = 2
X_lim           = []
Y_lim           = []
locator         = None
FONT_SIZE       = 16
axisNUM_FONT_SIZE = 12
title_x        = 0.7
Ylabel_x       = 0.03
Xlabel_x        = 1
Ylabel_y       = 1.02
Xlabel_y        = -0.01
xaxis_step      = 0
yaxis_step      = 0
subplots_left   =0.15
subplots_right  =0.9
subplots_top    =0.9
subplots_bottom =0.1
graphic_file_type = 'png'

#TranspSet  = 'N'
#SaveDeriv   = False
#SaveSet    = 'N'

optEstim = float_info.max

SchemeD1  = ['Forward'] # 'Backward'  #'Central'  #
#SchemeD1  = ['Backward']  #'Central'
# #DIF1 = 'Forward' # 'Backward'  #'Central'  #  # Central  Backward
UseHomeforPower = False #True   # 29
#ReadFrom = ''


printL       = 0
SavePoints   = False

#Version  = 63
Version  = 31
DataPath = ''


ExitStep     =   1e-7
OptStep      = '0.01'

mngF = ''

resF = ''    #      #resF = None - not read Penalty

#lenPenalty   = 0   25 02 10
Penalty      = []
OptNames = []
#fromPenalty = None

#  mngPenalty   = []        ???

#CVproc       = ''
CVNumOfIter  =   20
CV_Iter  =   0

curentTabl  = None

numCV      = -1
CV_NoRs     = []     # 23.11    = 0
ValidationSets      = []
notTrainingSets     = []           #  notTrainingSets содержит кого выбрасываем
TrainingSets        = []           #  TrainingSets содержит точки обучени
fun_with_mu = []
CVparam      = ''
#CVmargin     = 0
CVpartSize   = 0
CVside = 0
CVstep       = 7  
CV_NoSets    = 0
CVNoBorder    = False
NotCulcBorder = False

Task        = None
TaskName    = 'NoName'

useNaN      = False
VarNormalization = False

optFact          = None
token      =  ''
optFile    =  'peipopt.opt'

#LocalSolverName  = 'ipopt' #3_11_1'
LocalSolverName  = '/opt/scipopt911/bin/ipopt' # '/opt/solvers/bin/ipopt'

#SolverName       = 'ipopt'
SolverName       = '/opt/scipopt911/bin/ipopt' # '/opt/solvers/bin/ipopt'  # 3.14.09
#RunSolver   = 'Local'   #   LocalParallel   ServerParallel

solverOptVal =  {  "linear_solver"              : 'ma57'\
                 , 'max_iter'                   : 50000 \
                 , "print_level"                : 0     \
                 , 'warm_start_init_point'      : 'yes' \
                 , 'warm_start_bound_push'      : 1e-6 \
                 , 'warm_start_mult_bound_push' : 1e-6 \
                 , 'constr_viol_tol'            : 1e-4 \
                 , 'mu_init'                    : 1e-6 \
                 , "tol"                        : 1e-9 \
                 , 'print_user_options'         : 'yes'
                }
#    opt.options['acceptable_tol']       = 1e-10

RunMode     = 'L&L'         #  S&P&O

Hack_Stab    = False    #        Hack_Stab
stab_file = 'tmp_stab_file.nl'
#stabMU_LABAL = 19541117
stab_val_sub   = []
stab_val_by_cv   = []

#py_max_iter = 50000    #
#py_tol = 1e-9  #  -11
#acceptable_tol
#py_warm_start_bound_push = 1e-6   #
#py_warm_start_mult_bound_push = 1e-6
#py_constr_viol_tol = 1e-4  ##1e-11

path_SvF   = ''     #   "/home/sokol/C/_SvF/"
path_SvF_Lib = ''   #   /home/sokol/D/SvF/SvFlib/
tmpFileDir = ''     #   'C:\\C\\_SvF\\TMP\\'
startDir   = ''

###########################  AZIMUT  #########################
lon_center_rad = None
lat_center_rad = None
sin_lat_center_rad = None
cos_lat_center_rad = None

LastSet = None

