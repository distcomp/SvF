# -*- coding: UTF-8 -*-
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
#sys.path.append( path_Pyomo_Everest_pe )        #old
sys.path.append( path_pyomo_everest_ssop )
sys.path.append( path_Everest_python_api )

#print (path_SvF)
#print (path_SvF_Lib)

import COMMON as co
co.path_SvF   = path_SvF
co.tmpFileDir = path_SvF + 'TMP/'
co.token      = path_Everest_python_api +'/.token'

print ( os.getcwd() )
sys.path.append( os.getcwd() )

from ReadMng import *
Task = ReadMng ( )

if co.Preproc :
    print ('CWD', os.getcwd())
    sys.path.append( os.getcwd() )
    exec(open("StartModel.py").read())
print ('END OF ALL!')
exit(0)

