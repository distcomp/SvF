# -*- coding: UTF-8 -*-
from __future__ import division
from  numpy import *
import time 
#from  time import *
import os

import COMMON as co
from ssop_session import *
import ssop_config
#from Ssop import *



#from Lego    import *
from CVSets  import *
from GaKru   import *
from SurMin  import SurMin
from Pars    import *
from Tools   import *
from Task    import Grd_to_Var
from Task    import Var_to_Grd

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
#    print 'full_start',  full_start
    print ('\n\n\nStart SvFstart')

    if co.resF == '' :
        co.resF = co.mngF[:co.mngF.rfind('.')]+'.res'   #  RES file read

    Penal = co.Penalty
    if co.printL : print ('co.lenPenalty', co.lenPenalty)

    if len (co.mngPenalty) > 0 :  Penal = co.mngPenalty
    elif co.lenPenalty > 0 :
        print('From File: ', co.resF)
        try:
            with open(co.resF,'r') as f:
                s = f.readline().strip()
                Penal = s[1:-1].strip().replace(',', ' ').replace('   ', ' ').replace('  ', ' ').split(' ')
                Penal = [float(item) for item in Penal]
#                print Penal
   #             Penal = readListFloat19 ( f.readline().strip() )
                print ('read PENALTY:', Penal)
                if len (Penal) < co.lenPenalty :
                    print ("len(Penal) shoud be", co.lenPenalty)
                    exit(-1)
        except IOError as e:
            print ("******* Can''t open RES file: ", co.resF)
            exit(-1)
 #           print ("******* Can''t open RES file: ", co.resF, "\n Create new ? (Y/N)")
  #          ans = input()
   #         if ans != 'Y' and ans != 'y':  exit (-1)
    #        print ( "Use Penalty = 0.1" )
    Penal = Penal[ : co.lenPenalty]
    co.Penalty = Penal

#    maxSigEst = 0           # оценка сигмы скольз. среднем

    co.optFact = Factory(co.optFile, co.py_max_iter, co.py_tol)
    print('co.optFactST', co.optFact)

#    for ifu, fu in enumerate(Task.Funs) :           # v21
 #       if (fu.V.dat is None) or fu.param:  continue
  #      if len(co.testSet) == 0:
   #             co.testSet, co.teachSet = MakeSets_byParts ( fu.NoR, co.CVstep )  #CV_Sets (fu )
    #            print ('for FUNC', fu.V.name)


    print ('')
    for f in Task.Funs :  f.Oprint()
    print ('')

    if type(co.OptStep) == type('abc') :
        co.OptStep = [float(co.OptStep) * p for p in Penal[:]]

#    def get_sigCV(Penal, itera):                   #   test
 #       return (Penal[0] - 1) ** 2
  #  SurMin(30, [0.0001], 1e-5, [0.5], get_sigCV)
   # exit(0)

#    if co.CVNumOfIter == -1: pass
    if co.CVNumOfIter < 0: pass
    elif co.CVNumOfIter == 0:
            get_sigCV(Penal, -1)
    else :
        points, step = SurMin ( co.CVNumOfIter, co.OptStep, co.ExitStep, Penal, get_sigCV )

        with open(co.resF,'a') as f:      #  RES filewrite
            f.write( 'Step: '+ str(step) + '\nPoints:' )
            for p in points :  f.write( 'Num '+str(p.Num) + ' Val ' + str(p.Val) + ' Arg ' + str(p.Arg) + '\n')
#            print >> f, 'Step:', step, '\nPoints:'
 #           for p in points :  print >> f, 'Num', p.Num, 'Val', p.Val, 'Arg', p.Arg

    Task.ReadSols('')
    Gr = Task.Gr

    if co.CVNumOfIter > 0 :
      if  co.CVNoBorder  :   #  на границах не учитываем
        for s in co.teachSet[ 0] : Gr.mu0[s]=0
        for s in co.teachSet[-1] : Gr.mu0[s]=0
        NoRnoB = sum ( Gr.mu0[s]() for s in Gr.F[0].sR )
        print ('***** MSD_NoBorder', sqrt(Gr.F[0].NoR* Task.defMSDVal ( Gr, 0 ) /NoRnoB)*Gr.F[0].V.sigma)
#        print '***** MSD_NoBorder', sqrt(Gr.F[0].NoR*Gr.F[0].MSD()()/NoRnoB)*Gr.F[0].V.sigma
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


def testEstim (Gr, k) :  # k - testSet
    Var_to_Grd()
    for ifu, fu in enumerate(co.Task.Funs):
#        print ("BBBMMMMMMMMMMMMMMMMMMMMMMMMMMMMM", ifu, fu.name)
        if fu.mu is None: continue                     #  2024.01
        if fu.V.dat is None or fu.param: continue       #  23.11
 #       print ("MMMMMMMMMMMMMMMMMMMMMMMMMMMMM", fu.name)
#        if fu.NoR > co.CV_NoRs[0] : continue               # 25/04
        spart = 0
        npart = 0
        if fu.CVerr is None: fu.CVerr = zeros(fu.NoR, float64)   # 04.2023

        for s in fu.testSet[k]:
            if s >= fu.NoR        : continue                    #  25/04
            if isnan(fu.V.dat[s]) : continue

            if not co.Task.DeltaVal is None: err = Task.DeltaVal(Gr, ifu, fu.V.dat, s) #** 2
            elif  fu.MSDmode == 'MSDrel':    err = fu.delta_rel(s) #** 2          # 21.02.2023
            else:                            err = fu.delta(s) #** 2
            spart += err ** 2
            npart += 1
            fu.CVerr[s] = err                                   # 04.2023
#            print ('CVerr', s, fu.CVerr[s])
 #       print (fu.CVerr)
        if npart == 0:  print (spart, npart, 'NoVal', 'NoVal',)
        else:
            if fu.MSDmode == 'MSDrel':
                print ('  ', k, fu.name, spart, npart, sqrt(spart / npart), sqrt(spart / npart) * 100.,)
            else :
                print ('  ', k, fu.name, spart, npart, sqrt(spart / npart), sqrt(spart / npart) / fu.V.sigma * 100.,)
    # OLTCHEV
    #                NDT = Gr.F[d].NDT
    #                sumTbl  = sum((Gr.F[d].tbl[s, Gr.F[d].V.num] != NDT) * Gr.F[d].tbl[s,Gr.F[d].V.num] for s in testSet[k])
    #               sumFTbl = sum((Gr.F[d].tbl[s, Gr.F[d].V.num] != NDT) * Gr.F[d].Ftbl ( s )() for s in testSet[k])
    #              sumDelta = sum((Gr.F[d].tbl[s, Gr.F[d].V.num] != NDT) * Gr.F[d].delta ( s )() for s in testSet[k])
    #             print sumTbl,sumFTbl, sumDelta/ npart,

####    if co.CVNoBorder:  # на границах не учитываем
####        if k == 0 or k == len(fu.testSet) - 1:   continue
        fu.CVresult.append([spart, npart])


def getEstimCV(Gr) :
        printS ("\Parts |")
        Estim = 0
        NumOfFuns = 0
        for ifu, fu in enumerate (co.Task.Funs ):
            if fu.mu is None : continue             #  20.01
            if (fu.V.dat is None) or fu.param:  continue
            sCrVa = 0;  nCrVa = 0
            for CVr in fu.CVresult :
                sCrVa += CVr[0]
                nCrVa += CVr[1]
            if nCrVa > 0 :
                sCrVa = sqrt(sCrVa / nCrVa)
            if fu.MSDmode == 'MSDrel':  print (sCrVa, sCrVa * 100.,)
            else:                       print (sCrVa, sCrVa / fu.V.sigma * 100.,)
            fu.sCrVa = sCrVa
            if fu.MSDmode == 'MSDrel':  Estim += sCrVa                  # 21.02.2023
            else :                      Estim += sCrVa / fu.V.sigma
            NumOfFuns += 1
        Estim = Estim / NumOfFuns * 100
        return Estim


def printMSD () :
    printS ("sol MSD%: |")
    for ifu, fu in enumerate(co.Task.Funs) :
            if fu.V.dat is None or fu.param: continue       #  23.11
#            if fu.mu is None:  continue                    #  23.11
            if not co.Task.DeltaVal is None: fu.MSDv = co.Task.defMSDVal ( Gr, ifu )
            else:
                if fu.MSDmode == 'MSDrel':  fu.MSDv = fu.MSDrel(fu.measurement_accur)          # 21.02.2023
                else :                      fu.MSDv = fu.MSDnan()
#            if co.Task.defMSDVal is None : fu.MSDv = fu.MSDnan()  ### ()
 #           else                         : fu.MSDv = co.Task.defMSDVal ( Gr, ifu )
            printS (fu.V.name, sqrt(fu.MSDv)*100.,' |')
    print ('')



def get_sigCV( Penal, itera ):
    co.CV_Iter = itera
    Task = co.Task
#    reload (Model)
    co.Use_var = True       # 29
    Gr = Task.createGr(Task, Penal)
    co.Use_var = False       # 29

    for fu in Task.Funs :  fu.CVresult = []

    Task.ReadSols('')
 #   Grd_to_Var()
    if itera <= 0 : printS (' Load on Start ');   printMSD()

#    resultss = solveProblemsNl(Gr, [[]], co.RunMode[0])
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
#            resultss = solveProblemsNl ( Gr, co.teachSet, co.RunMode[2] )
            resultss = solveProblemsNl ( Gr, '*', co.RunMode[2] )              # All tests
            for nres, res in enumerate (resultss) :
                Gr.solutions.load_from(res)
                testEstim(Gr, nres)
        else:       ## co.RunMode[2] == 'L' :
            res_num = 0
            print(co.CV_NoSets, "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            for k in range(co.CV_NoSets):                                  # LOAD RES,  culculation
                #               if co.NotCulcBorder :  #  границ не считаем
                #                  if k == 0 or k == len(testSet) - 1:   1/0;  continue  #########  ???????????????????
                #             printS (str(k)+' |')
                #                results = solveProblemsNl(Gr, [co.teachSet[k]], co.RunMode[2])[0]  #!! РАБОТАЕТ ТОЛЬКО ДЛЯ ОДНОГО resultss
                results = solveProblemsNl(Gr, k, co.RunMode[2])[0]  #!! РАБОТАЕТ ТОЛЬКО ДЛЯ ОДНОГО resultss
                res_num += 1
                Gr.solutions.load_from(results)
                testEstim(Gr, k)

        Estim = getEstimCV(Gr)
        print ('\tEstim% '+str(Estim)+"\tTime  "+ str(time.time() - star))
    else : Estim = -1

#    co.Use_var = False       # 29

    if Estim < co.optEstim :
            co.optEstim = Estim
            Task.RenameSols( '.tmp', '.sol' )
            with open(co.resF,'w') as f:      #  RES filewrite
#                print >> f, [p for  p in Penal]
                f.write (str(Penal))
                for fu in Task.Funs :           # v21
#                      if fu.mu is None: continue                     #  2023.11
                      if fu.V.dat is None or fu.param: continue  # 23.11
                      str_wr = '\n'+fu.nameFun()+' '
                      if co.CVNumOfIter > 0 :
                          if fu.MSDmode == 'MSDrel':   str_wr += " CV% " + str(fu.sCrVa*100) + " CV " + str(fu.sCrVa)
                          else:                     str_wr += " CV% " + str(fu.sCrVa/fu.V.sigma*100) + " CV " + str(fu.sCrVa)
                      str_wr += ' MSD% ' + str(sqrt(fu.MSDv)*100) +' MSD ' + str(sqrt(fu.MSDv)*fu.V.sigma)
                      f.write( str_wr )
                      print (str_wr)
                f.write( '\n'+'Estim ' + str(Estim))
#                print >> f, 'Estim',Estim
                Task.print_res(Task, Penal, f)
    return Estim


