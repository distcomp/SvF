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


MU_LABAL = 2147483647

buf = ""

#Mng = ''

def SvFstart19 ( Task ) :
 #   global Mng


    full_start = time.time()
#    print 'full_start',  full_start

#    if co.Preproc :  return
    print ('\n\n\nStart SvFsrat')

#    if Task.createGr is None:
 #       Task.createGr  = Model.createGr
  #      Task.Delta     = None #Mo.Delta
   #     Task.DeltaVal  = None #Mo.DeltaVal
    #    Task.defMSD    = None #Mo.defMSD
     #   Task.defMSDVal = None #Mo.defMSDVal
      #  Task.print_res = Model.print_res


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
            print ("******* Can''t open RES file: ", co.resF, "\n Create new ? (Y/N)")
            ans = input()
            if ans != 'Y' and ans != 'y':  exit (-1)
            print ( "Use Penalty = 0.1" )
    Penal = Penal[ : co.lenPenalty]
    co.Penalty = Penal

#    maxSigEst = 0           # оценка сигмы скольз. среднем

    co.optFact = Factory(co.optFile, co.py_max_iter, co.py_tol)
    print('co.optFactST', co.optFact)

    for ifu, fu in enumerate(Task.Funs) :           # v21
        if (fu.V.dat is None) or fu.param:  continue
#        if len (fu.testSet) == 0 :
        if len(co.testSet) == 0:
                co.testSet, co.teachSet = MakeSets_byParts ( fu.NoR, co.CVstep )  #CV_Sets (fu )
                print ('for FUNC', fu.V.name)
  #          fu.testSet, fu.teachSet = MakeSets_byParts ( fu.NoR, co.CVstep )  #CV_Sets (fu )
#            fu.mu = Gr.mu


    print ('')
    for f in Task.Funs :  f.Oprint()
    print ('')

    if type(co.OptStep) == type('abc') :
        steps = []
        for ip, p in enumerate (Penal) :
            steps.append(Penal[ip]*float(co.OptStep))
        co.OptStep = steps


#    def get_sigCV(Penal, itera):                   #   test
 #       return (Penal[0] - 1) ** 2
  #  SurMin(30, [0.0001], 1e-5, [0.5], get_sigCV)
   # exit(0)

    if co.CVNumOfIter == 0:
        get_sigCV ( Penal, -1 )
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
        for s in co.teachSet[ 0] : Gr.mu[s]=0
        for s in co.teachSet[-1] : Gr.mu[s]=0
        NoRnoB = sum ( Gr.mu[s]() for s in Gr.F[0].sR )
        print ('***** MSD_NoBorder', sqrt(Gr.F[0].NoR* Task.defMSDVal ( Gr, 0 ) /NoRnoB)*Gr.F[0].V.sigma)
#        print '***** MSD_NoBorder', sqrt(Gr.F[0].NoR*Gr.F[0].MSD()()/NoRnoB)*Gr.F[0].V.sigma
        for s in Gr.F[0].sR : Gr.mu[s]=1



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
    for ifu, fu in enumerate(co.Task.Funs):
        if fu.mu is None: continue
        if fu.NoR > co.CV_NoR : continue               # 25/04
        spart = 0
        npart = 0
        if fu.CVval is None: fu.CVval = zeros(fu.NoR, float64)   # 2021/11  from MakeModel

        for s in fu.testSet[k]:
            if s >= fu.NoR        : continue                    #  25/04
            if isnan(fu.V.dat[s]) : continue

            fu.CVval[s] = fu.Ftbl(s)
            if co.Task.DeltaVal is None:  spart += (fu.V.dat[s]-fu.CVval[s])**2   #fu.delta(s) ** 2               # 29
            else:                         spart += Task.DeltaVal(Gr, ifu, fu.V.dat, s) ** 2
            npart += 1
#            if k <= 1:  print ('=',k,s, spart,npart,  fu.V.dat[s], fu.CVval[s], (fu.V.dat[s]-fu.CVval[s])**2)
        if npart > 0:  print ('  ', spart, npart, sqrt(spart / npart), sqrt(spart / npart) / fu.V.sigma * 100.,)
        else:          print (spart, npart, 'NoVal', 'NoVal',)
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
            if (fu.V.dat is None) or fu.param:  continue
            sCrVa = 0;  nCrVa = 0
            for CVr in fu.CVresult :
                sCrVa += CVr[0]
                nCrVa += CVr[1]
            if nCrVa > 0 :
                sCrVa = sqrt(sCrVa / nCrVa)
            print (sCrVa, sCrVa / fu.V.sigma * 100.,)
            fu.sCrVa = sCrVa
            Estim += sCrVa / fu.V.sigma
            NumOfFuns += 1
        Estim = Estim / NumOfFuns * 100
        return Estim


def printMSD () :
 #   printS ("sol MSD%:")
    printS ("sol MSD%: |")
    for ifu, fu in enumerate(co.Task.Funs) :
#        if (not fu.V.dat is None) and not fu.param:
       #     fu.myprint()
        #    print (fu.mu)
            if fu.mu is None:  continue
            if co.Task.defMSDVal is None : fu.MSDv = fu.MSDnan()  ### ()
            else                         : fu.MSDv = co.Task.defMSDVal ( Gr, ifu )
            printS (fu.V.name, sqrt(fu.MSDv)*100.,' |')
    print ('')



def get_sigCV( Penal, itera ):
    Task = co.Task
#    reload (Model)
    co.Use_var = True       # 29
    Gr = Task.createGr(Task, Penal)
    co.Use_var = False       # 29

    for fu in Task.Funs :  fu.CVresult = []

    Task.ReadSols('')
 #   Grd_to_Var()
    if itera <= 0 : printS (' Load on Start ');   printMSD()

    resultss = solveProblemsNl(Gr, [[]], co.RunMode[0])
    Gr.solutions.load_from(resultss[0])
    Var_to_Grd()
    Task.SaveSols('.tmp')#,0)

    print ('OBJ',Gr.OBJ())
    printMSD()

    if not Task.OBJ_U is None :
        Estim = Task.OBJ_U(Task)()
        print ('**************KK=', Estim)

    elif co.CVNumOfIter != 0 :
        star = time.time()

        if co.RunMode[2] != 'L' :   resultss = solveProblemsNl ( Gr, co.teachSet, co.RunMode[2] )

        res_num = 0
        for k in range(co.CV_NoSets):                                  # LOAD RES,  culculation
            if co.NotCulcBorder :  #  границ не считаем
                if k == 0 or k == len(testSet) - 1:   1/0;  continue
            printS (str(k)+' |')

            if co.RunMode[2] == 'L' :
                results = solveProblemsNl(Gr, [co.teachSet[k]], co.RunMode[2])[0]  # !!  ТОЛЬКО ДЛЯ ОДНОГО resultss
            else :
                results = resultss[res_num]
            res_num += 1

            Gr.solutions.load_from(results)

            Var_to_Grd()
            testEstim(Gr, k)

        Estim = getEstimCV(Gr)
        print ('\tEstim% '+str(Estim)+"\tTime  "+ str(time.time() - star))
#        Mng.MSD   = MSD
 ###       Mng.sCrVa = sCrVa
    else : Estim = -1

#    co.Use_var = False       # 29

    if Estim < co.optEstim :
            co.optEstim = Estim
            Task.RenameSols( '.tmp', '.sol' )
            with open(co.resF,'w') as f:      #  RES filewrite
#                print >> f, [p for  p in Penal]
                f.write (str(Penal))
                for fu in Task.Funs :           # v21
               #     if ( not fu.V.dat is None) and fu.param == False:
                      if fu.mu is None:  continue
                      str_wr = '\n'+fu.nameFun()+' '
                      if co.CVNumOfIter > 0 :
                          str_wr += " CV% " + str(fu.sCrVa/fu.V.sigma*100) + " CV " + str(fu.sCrVa)
                      str_wr += ' MSD% ' + str(sqrt(fu.MSDv)*100) +' MSD ' + str(sqrt(fu.MSDv)*fu.V.sigma)
                      f.write( str_wr )
                      print (str_wr)
                f.write( '\n'+'Estim ' + str(Estim))
#                print >> f, 'Estim',Estim
                Task.print_res(Task, Penal, f)
    return Estim


