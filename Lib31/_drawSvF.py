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

import COMMON as SvF
SvF.path_SvF   = path_SvF
SvF.tmpFileDir = path_SvF + 'TMP/'
SvF.token      = path_Everest_python_api +'/.token'
import Task as ta
SvF.Task = ta.TaskClass ()

print ( os.getcwd() )

sys.path.append( os.getcwd() )

import Draw as dra
#SvF.Compile = False

str = ''
for na, a in enumerate (sys.argv) :
    if na==0 : continue
    if na==1 : str = a
    else     : str += ' ' + a
dra.DrawComb(str) #sys.argv[1])
#dra.DrawComb('Pdf(r,t).sol')
exit(0)


