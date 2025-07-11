# -*- SvF.ing: UTF-8 -*-
import sys
import platform
import os
import numpy as np
import COMMON as SvF

prog_name = sys.argv[0]
SvF.path_SvF_Lib            = prog_name[: prog_name.rfind('/')]             #   /home/sokol/D/SvF/SvFlib
SvF.path_SvF                = SvF.path_SvF_Lib[: SvF.path_SvF_Lib.rfind('/')+1]     #   /home/sokol/D/SvF/

SvF.tmpFileDir      = SvF.path_SvF + 'TMP/'
SvF.token           = SvF.path_SvF + "pyomo-everest/python-api" +'/.token'
SvF.startDir        = os.getcwd()
if platform.system() == 'Windows':   SvF.platform = 'Win'       # 2022.05

print ( SvF.startDir )
sys.path.append( SvF.startDir )

if SvF.startDir.find('/home/vladimirv/mc2/agent') == 0 :       #  опции для       svf-remote   **************
    SvF.DrawMode         = 'File'
    SvF.LocalSolverName  = '/opt/scipopt911/bin/ipopt'
    SvF.SolverName       = '/opt/scipopt911/bin/ipopt'  # 3.14.09

from ReadMng import ReadMng

while (1) :
    SvF.Compile = True
    Task = ReadMng ( )
    print ('#######################################################################')
    SvF.Compile = False
    print ('\n\nCWD', os.getcwd(),  'RUN   StartModel.py *****************' )
    sys.path.append( os.getcwd() )
    exec(open("StartModel.py").read())                  ######  Model call
#    print ('SvF.resF'+SvF.resF+'!')
    with open(SvF.resF, 'a') as f:  # RES filewrite
        f.write('addStrToRes: ' + SvF.addStrToRes)
    if SvF.EofTask:
        print('\n\n\n *********  END OF TASK! **************')
        SvF.SModelFile = None
        SvF.ModelBuf = None
        SvF.resF = ''
        SvF.OptStep = '0.01'
        SvF.optEstim = np.float_info.max
        SvF.curentTabl = None
        SvF.useNaN = False
    else :  break

print ('END OF FILE!')
exit(0)

