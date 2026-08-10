# -*- SvF.ing: UTF-8 -*-
import sys
import platform
import os
# import numpy as np
import COMMON as SvF

#prog_name = sys.argv[0]
#SvF.path_SvF_Lib            = prog_name[: prog_name.rfind('/')]                     #   /home/sokol/D/SvF/SvFlib
#SvF.path_SvF                = SvF.path_SvF_Lib[: SvF.path_SvF_Lib.rfind('/')+1]     #   /home/sokol/D/SvF/  - в верхнем каталоге

#SvF.tmpFileDir      = SvF.path_SvF + 'TMP/'
#SvF.token           = SvF.path_SvF + "pyomo-everest/python-api" +'/.token'

if platform.system() == 'Windows':   SvF.platform = 'Win'       # 2022.05

#startDir        = os.getcwd()
#sys.path.append( SvF.startDir )
#sys.path.append(os.getcwd())

from ReadMng import ReadMng

while (1) :
    SvF.Compile = True
    EoF = ReadMng ( )
#    SvF.Compile = False
    print ( '#########  Start StartModel.py in ' + os.getcwd() + ' #########\n' )
    #sys.path.append( os.getcwd() )
 #   exec(open("StartModel.py").read())                  ######  Model call
    import subprocess
 #   import sys

    result = subprocess.run(
        [sys.executable, os.getcwd()+"/StartModel.py"],
        check=True
    )

    if EoF == 'EOF' :  break
    else:
#    if SvF.EofTask:
        print('\n\n\n *********  END OF TASK! **************')
     #   brak
 #       SvF.SModelFile = None
  #      SvF.ModelBuf = None
   #     SvF.resF = ''
    #    SvF.OptStep = '0.01'
     #   SvF.optEstim = sys.float_info.max
      #  SvF.currentTab = None
       # SvF.useNaN = True    #      26.02.01  False#
#        ValidationSets = []
 #       notTrainingSets = []  # notTrainingSets содержит кого выбрасываем
  #      TrainingSets = []  # TrainingSets содержит точки обучени
   #     SvF.CV_NoRs = []
    #    SvF.numCV = -1


print ('END OF FILE!')
exit(0)

