# -*- coding: UTF-8 -*-
from __future__ import division
#from  numpy import *
import numpy as np
import time 
#from  time import *
import os

import COMMON as co
from ssop_session import *
import ssop_config
#from Ssop import *

# import Lego_symFun


#from Lego    import *
from CVSets  import *
from GaKru   import *
from SurMin  import SurMin
from Pars    import *
from Tools   import *
#from Task    import Grd_to_Var
from Task    import Var_to_Grd, FillNaNAll, setUse_var

#from StartModel import Model
#import Model as Model


from SolverTools import *

#from pyomo.environ import *
from pyomo.opt import SolverFactory


#from PyomoEverestEnv import *
#==========================


#MU_LABAL = 2147483647

buf = ""

#Mng = ''

def SvFstart19 ( Task ) :
    full_start = time.time()
    print ('\n\n\nStart SvFstart')
    setUse_var(False)  # 25.10

    if co.resF is None :   #  не считываем, но сохраняем
        co.resF = co.mngF[:co.mngF.rfind('.')] + '.res'  # RES file read
##        co.lenPenalty = len (co.OptNames)
    else :
        if co.resF == '' :  co.resF = co.mngF[:co.mngF.rfind('.')]+'.res'   #  RES file read

        Penal = co.Penalty
##        if co.printL : print ('co.lenPenalty', co.lenPenalty)

        print('From File: ', co.resF) #, len (co.Penalty), co.Penalty)

        try:
                with (open(co.resF,'r') as f):
                    s = f.readline().strip().replace(',', ' ').replace('   ', ' ').replace('  ', ' ').replace(' ', ',')  #.split(', ')
                    Penal = readListFloat19 (s)
                    print ('read PENALTY:', Penal)
        except IOError as e:
                print ("******* Can''t open RES file: ", co.resF)
        #        if len (Penal) == 0 :  exit(-1)
        co.Penalty = Penal
    # print (co.Penalty); exit(22)
    co.Penalty = [0.1 if x is None else x for x in co.Penalty]
#    print (Penal, co.Penalty)
 #   1/0

#    maxSigEst = 0           # оценка сигмы скольз. среднем

    co.optFact = Factory(co.optFile)
#    print('co.optFactST', co.optFact)

#    print ('')
 #   for f in Task.Funs :  f.Oprint()
  #  print ('')

    if type(co.OptStep) is str :
        co.OptStep = [float(co.OptStep) * p for p in co.Penalty[:]]

    if co.CVNumOfIter < 0: pass
    elif co.CVNumOfIter == 0:
            get_sigCV(co.Penalty, -1)
    else :
      #  print ('co.OptStep',co.OptStep, 'co.Penalty', co.Penalty)
        points, step = SurMin ( co.CVNumOfIter, co.OptStep, co.ExitStep, co.Penalty, get_sigCV )   ######## START ###########
        with open(co.resF,'a') as f:      #  RES filewrite
            f.write( 'Step: '+ str(step) + '\nPoints:' )
            for p in points :  f.write( 'Num '+str(p.Num) + ' Val ' + str(p.Val) + ' Arg ' + str(p.Arg) + '\n')
#            print >> f, 'Step:', step, '\nPoints:'
 #           for p in points :  print >> f, 'Num', p.Num, 'Val', p.Val, 'Arg', p.Arg

    Task.ReadSols('')
    Gr = Task.Gr

    if co.CVNumOfIter > 0 :
      if  co.CVNoBorder  :   #  на границах не учитываем
        for s in co.notTrainingSets[ 0] : Gr.mu0[s]=0
        for s in co.notTrainingSets[-1] : Gr.mu0[s]=0
        NoRnoB = sum ( Gr.mu0[s]() for s in Gr.F[0].sR )
        print ('***** MSD_NoBorder', np.sqrt(Gr.F[0].NoR* Task.defMSDVal ( Gr, 0 ) /NoRnoB)*Gr.F[0].V.sigma)
#        print '***** MSD_NoBorder', np.sqrt(Gr.F[0].NoR*Gr.F[0].MSD()()/NoRnoB)*Gr.F[0].V.sigma
        for s in Gr.F[0].sR : Gr.mu0[s]=1

    for f in Task.Funs :
      if not f.param :
#        f.SaveTbl('')
        if co.SavePoints : f.SavePoints()
#        if co.SaveDeriv and f.type != 'p' :  f.SaveDeriv ( "" )
#        if co.SaveGrid=='Y' and f.dim == 2 and f.type != 'p':     f.SaveGrid ( co.TranspGrid, '' )
    print ("EofCulc")
    print ('TIME: ', time.time() - full_start)
    return


##################################################################


#optEstim = sys.float_info.max


def testEstim (Gr, k) :  # k - ValidationSets
    Var_to_Grd()
    for ifu, fu in enumerate(co.Task.Funs):
#        print ("BBBMMMMMMMMMMMMMMMMMMMMMMMMMMMMM", ifu, fu.name)
        if fu.type == 'tensor' : continue
        if fu.mu is None: continue                     #  2024.01
        if fu.V.dat is None or fu.param: continue       #  23.11
 #       print ("MMMMMMMMMMMMMMMMMMMMMMMMMMMMM", fu.name)
#        if fu.NoR > co.CV_NoRs[0] : continue               # 25/04
        spart = 0
        npart = 0
        if fu.CVerr is None: fu.CVerr = np.zeros(fu.NoR, np.float64)   # 04.2023

        for s in fu.ValidationSets[k]:
            if s >= fu.NoR        : continue                    #  25/04
            if np.isnan(fu.V.dat[s]) : continue

            if not co.Task.DeltaVal is None: err = Task.DeltaVal(Gr, ifu, fu.V.dat, s) #** 2
            elif  fu.MSDmode == 'MSDrel':    err = fu.delta_rel(s) #** 2          # 21.02.2023
            else:                            err = fu.delta(s) #** 2
   #         if s==0 :
    #            print ('err=', err)
     #           1/0
            spart += err ** 2
            npart += 1
            fu.CVerr[s] = err                                   # 04.2023
#            print ('CVerr', s, fu.CVerr[s])
 #       print (fu.CVerr)
        if npart == 0:  print (spart, npart, 'NoVal', 'NoVal',)
        else:
            if fu.MSDmode == 'MSDrel':
                print ('  ', k, fu.name, spart, npart, np.sqrt(spart / npart), np.sqrt(spart / npart) * 100.,)
            else :
                print ('  ', k, fu.name, spart, npart, np.sqrt(spart / npart), np.sqrt(spart / npart) / fu.V.sigma * 100.,)
    # OLTCHEV
    #                NDT = Gr.F[d].NDT
    #                sumTbl  = sum((Gr.F[d].tbl[s, Gr.F[d].V.num] != NDT) * Gr.F[d].tbl[s,Gr.F[d].V.num] for s in ValidationSets[k])
    #               sumFTbl = sum((Gr.F[d].tbl[s, Gr.F[d].V.num] != NDT) * Gr.F[d].Ftbl ( s )() for s in ValidationSets[k])
    #              sumDelta = sum((Gr.F[d].tbl[s, Gr.F[d].V.num] != NDT) * Gr.F[d].delta ( s )() for s in ValidationSets[k])
    #             print sumTbl,sumFTbl, sumDelta/ npart,

####    if co.CVNoBorder:  # на границах не учитываем
####        if k == 0 or k == len(fu.ValidationSets) - 1:   continue
        fu.CVresult.append([spart, npart])


def getEstimCV(Gr) :
        printS ("\nParts |")      #    printS ("\n???????Parts |")
        Estim = 0
        NumOfFuns = 0
        for ifu, fu in enumerate (co.Task.Funs ):
            if fu.type == 'tensor': continue
            if fu.mu is None : continue             #  20.01
            if (fu.V.dat is None) or fu.param:  continue
            sCrVa = 0;  nCrVa = 0
            for CVr in fu.CVresult :
                sCrVa += CVr[0]
                nCrVa += CVr[1]
            if nCrVa > 0 :
                sCrVa = np.sqrt(sCrVa / nCrVa)
            if fu.MSDmode == 'MSDrel':  print (sCrVa, sCrVa * 100.,)
            else:                       print (sCrVa, sCrVa / fu.V.sigma * 100.,)
            fu.sCrVa = sCrVa
            if fu.MSDmode == 'MSDrel':  Estim += sCrVa                  # 21.02.2023
            else :                      Estim += sCrVa / fu.V.sigma
            NumOfFuns += 1
        Estim = Estim / NumOfFuns * 100
        return Estim


def printMSD () :
    printS ("sol SD%: |")
    for ifu, fu in enumerate(co.Task.Funs) :
            if  fu.type == 'tensor' : continue
            if fu.V.dat is None or fu.param: continue       #  23.11
#            if fu.mu is None:  continue                    #  23.11
            if not co.Task.DeltaVal is None: fu.MSDv = co.Task.defMSDVal ( Gr, ifu )
            else:
                if fu.MSDmode == 'MSDrel':  fu.MSDv = fu.MSDrel(fu.measurement_accur)          # 21.02.2023
                else :                      fu.MSDv = fu.MSDnan()
#            if co.Task.defMSDVal is None : fu.MSDv = fu.MSDnan()  ### ()
 #           else                         : fu.MSDv = co.Task.defMSDVal ( Gr, ifu )
            printS (fu.V.name, np.sqrt(fu.MSDv)*100.,' |')
    print ('')



def get_sigCV( Penal, itera ):
    co.CV_Iter = itera
    Task = co.Task
#    reload (Model)
    Task.ReadSols('')
#    SvF.Penalty = Penal
    if not (SvF.feasibleSol is None) : SvF.feasibleSol(Penal)

    print ('for Penal: ', Penal ) #, end=' ')

    if SvF.OptMode == 'SurMinOpt' :
  #      co.Use_var = True       # 29
        setUse_var(True)       # 25.10

        Gr = Task.createGr(Task, Penal)   # обновлем на каждой итерации
        Grd_to_Var()
        #co.Use_var = False       # 29
        setUse_var(False)  # 25.10

        resultss = solveProblemsNl(Gr, '', co.RunMode[0])               #  tmp
        Gr.solutions.load_from(resultss[0])
        Var_to_Grd()
        Task.SaveSols('.tmp')

        print ('OBJ',Gr.OBJ())
        Estim = Gr.OBJ()

    elif SvF.OptMode == 'SvF':

        FillNaNAll ()
     #   co.Use_var = True       # 29
        setUse_var(True)  # 25.10

        Gr = Task.createGr(Task, Penal)   # обновлем на каждой итерации
        Grd_to_Var()
#        co.Use_var = False       # 29
        setUse_var(False)  # 25.10

        for fu in Task.Funs :  fu.CVresult = []

        if itera <= 0 : printS (' Load on Start ');   printMSD()

        resultss = solveProblemsNl(Gr, '', co.RunMode[0])               #  tmp
        Gr.solutions.load_from(resultss[0])
        Var_to_Grd()
        Task.SaveSols('.tmp')

        print ('OBJ',Gr.OBJ())
        printMSD()


        if not Task.OBJ_U is None :
            Estim = Task.OBJ_U(Task)()
            print ('**************KK=', Estim)

        elif co.CVNumOfIter != 0 :
            star = time.time()

            if co.RunMode[2] != 'L':
    #            resultss = solveProblemsNl ( Gr, co.notTrainingSets, co.RunMode[2] )
                resultss = solveProblemsNl ( Gr, '*', co.RunMode[2] )              # All tests
                for nres, res in enumerate (resultss) :
                    Gr.solutions.load_from(res)
                    testEstim(Gr, nres)
            else:       ## co.RunMode[2] == 'L' :
                res_num = 0
 #               print(co.CV_NoSets, "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                for k in range(co.CV_NoSets):                                  # LOAD RES,  culculation
                    #               if co.NotCulcBorder :  #  границ не считаем
                    #                  if k == 0 or k == len(ValidationSets) - 1:   1/0;  continue  #########  ???????????????????
                    #             printS (str(k)+' |')
                    #                results = solveProblemsNl(Gr, [co.notTrainingSets[k]], co.RunMode[2])[0]  #!! РАБОТАЕТ ТОЛЬКО ДЛЯ ОДНОГО resultss
                    results = solveProblemsNl(Gr, k, co.RunMode[2])[0]  #!! РАБОТАЕТ ТОЛЬКО ДЛЯ ОДНОГО resultss
                    res_num += 1
                    Gr.solutions.load_from(results)
                    testEstim(Gr, k)

            Estim = getEstimCV(Gr)
            print ('\tEstim% '+str(Estim)+"\tTime  "+ str(time.time() - star))
        else : Estim = -1

    elif SvF.OptMode == 'SurMin':
       Estim = SvF.ObjectiveFun (Penal)

    if Estim < co.optEstim :
            co.optEstim = Estim
            Task.RenameSols( '.tmp', '.sol' )
            with open(co.resF,'w') as f:      #  RES filewrite
#                print >> f, [p for  p in Penal]
                f.write (str(Penal))
                for fu in Task.Funs :           # v21
#                      if fu.mu is None: continue                     #  2023.11
                      if fu.type == 'tensor': continue
                      if fu.V.dat is None or fu.param: continue  # 23.11
                      str_wr = '\n'+fu.nameFun()+' '
                      if co.CVNumOfIter > 0 :
                          if fu.MSDmode == 'MSDrel':   str_wr += " CV% " + str(fu.sCrVa*100)
                          else:                     str_wr += " CV% " + str(fu.sCrVa/fu.V.sigma*100)
                      str_wr += ' SD% ' + str(np.sqrt(fu.MSDv)*100) + " CV " + str(fu.sCrVa) \
                                +' SD ' + str(np.sqrt(fu.MSDv)*fu.V.sigma) + ' sig '+str(fu.V.sigma)

                      f.write( str_wr )
                      print (str_wr)
                f.write( '\n'+'Estim ' + str(Estim))
#                print >> f, 'Estim',Estim
 #               print ('(((((((((((', Gr.OBJ ())
                if Task.print_res != None :
                    Task.print_res(Task, Penal, f)
    return Estim


