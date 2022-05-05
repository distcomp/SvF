# -*- SvF.ing: UTF-8 -*-

import sys
import platform
import os
prog_name = sys.argv[0]
path_SvF_Lib            = prog_name[: prog_name.rfind('/')]
path_SvF                = path_SvF_Lib.split('Lib')[0]
path_pyomo_everest_ssop  = path_SvF + "pyomo-everest/ssop"
path_Everest_python_api = path_SvF + "Everest/python-api"

sys.path.append( path_SvF_Lib )
sys.path.append( path_SvF )
sys.path.append( path_pyomo_everest_ssop )
sys.path.append( path_Everest_python_api )

#print (path_SvF)
#print (path_SvF_Lib)

import COMMON as SvF
SvF.path_SvF   = path_SvF
SvF.tmpFileDir = path_SvF + 'TMP/'
SvF.token      = path_Everest_python_api +'/.token'
SvF.startDir  =  os.getcwd()

print ( SvF.startDir )
sys.path.append( SvF.startDir )

from ReadMng import *

while (1) :
    SvF.Compile = True
    Task = ReadMng ( )
    print ('#######################################################################')
    SvF.Compile = False
    print ('\n\nCWD', os.getcwd(),  'RUN   StartModel.py *****************' )
    sys.path.append( os.getcwd() )
    exec(open("StartModel.py").read())
    with open(SvF.resF, 'a') as f:  # RES filewrite
        f.write('addStrToRes: ' + SvF.addStrToRes)
    if SvF.EofTask:
        print('\n\n\n *********  END OF TASK! **************')
        SvF.SModelFile = None
        SvF.ModelFile = None
        SvF.resF = ''
        SvF.OptStep = '0.01'
        SvF.optEstim = float_info.max
        SvF.curentTabl = None
        SvF.useNaN = False
    else :  break

print ('END OF FILE!')
exit(0)

