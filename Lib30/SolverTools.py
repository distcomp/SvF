# -*- coding: UTF-8 -*-
from __future__ import division
import subprocess



import COMMON as co

from Task    import Grd_to_Var

import platform

#from pyomo.environ import *
#import pyomo.environ as py
from pyomo.opt import SolverFactory
from pyomo.opt import ProblemFormat
from pyomo.opt import TerminationCondition
from pyomo.opt import (ReaderFactory,ResultsFormat)

from ssop_session import *



def Factory (optFile , py_max_iter, py_tol ): # , warm_start_bound_push      =1e-6,
    opt = SolverFactory(co.LocalSolverName)
    opt.options["print_level"] = 4 #4 #6
    opt.options['warm_start_init_point']      = 'yes'
    opt.options['warm_start_bound_push']      = co.py_warm_start_bound_push
    opt.options['warm_start_mult_bound_push'] = co.py_warm_start_mult_bound_push
    opt.options['constr_viol_tol']            = co.py_constr_viol_tol
    opt.options['mu_init']                    = 1e-6
    opt.options['max_iter']             = py_max_iter
    opt.options["tol"]                  = py_tol
#    opt.options['acceptable_tol']       = 1e-10
    opt.options['print_user_options']      = 'yes'

    if platform.system() != 'Windows':
            opt.options["linear_solver"] = 'ma57'
 #           opt.options["linear_solver"] = 'ma86'
    if  optFile != None :
        if co.RunMode[0] != 'L' or co.RunMode[2] != 'L' :
 #           writeIpoptOptionsFile(opt.options, co.tmpFileDir+'/'+optFile)
            makeSolverOptionsFile(co.tmpFileDir+'/'+optFile, "ipopt", opt.options)
    return opt

def writeIpoptOptionsFile(optsDict, fNameOpts):
    fOpts = open(fNameOpts, 'w')
    for key in optsDict.keys():
        if key != 'solver': fOpts.write('%s %s\n' % (key, str(optsDict[key])))
    fOpts.close()



def makeNlFile ( Gr, stab_file ) :
            _, smap_id = Gr.write( stab_file, format=ProblemFormat.nl )#,  io_options={'symbolic_solver_labels': True})  # создаем стаб
            symbol_map = Gr.solutions.symbol_map[smap_id]
#            print ("makeNlFile", stab_file)
            return symbol_map

def setMuToTeach (Gr, teachSet = [] ) :                     #  teachSet содержит кого выбрасываем
#            for m in range(com.CV_NoR) : Gr.mu[m] = 1
        if co.CV_NoR > 0:
            Gr.mu[:] = 1
            for s in teachSet  : Gr.mu[s] = 0



def makeNlFileTeach ( Gr, stab_file, teachSet_k ) :
            setMuToTeach(Gr, teachSet_k )
            return makeNlFile(Gr, co.tmpFileDir + "/" + stab_file + ".nl")


def makeNlFileS ( Gr, teachSet ) : #, symbol_map, nls ) :
        sym_maps = []
        __peProblems = []                                             # __pe - prefix for Pyomo&Everest stuff
        for k in range(len(teachSet)) :  #co.CV_NoSets):                                  # make   STABs
 #           if co.NotCulcBorder :  #  границ не считаем
  #              if k == 0 or k == len(co.testSet) - 1:   continue
            pName = co.TaskName + "0000"+str(k)

            symbol_map = makeNlFileTeach ( Gr, pName, teachSet[k] )

            __peProblems.append(pName)
            sym_maps.append(symbol_map)

#            for s in teachSet[k]:  Gr.mu[s] = 1
    #        for fu in co.Task.Funs:
     #               if (fu.V.dat is None) or fu.param:  continue
      #              for s in co.teachSet[k]: fu.mu[s] = 1
#                    for s in fu.teachSet[k]: fu.mu[s] = 1
        print ('for  '+co.TaskName, len(__peProblems), '   files')
        return  sym_maps, __peProblems

def solveNlFileS ( sym_maps, __peProblems, tmpFileDir, RunMo ) :
        if RunMo == 'S':                                        # RUN dist    #===== solve in parallel ===========
            theSession = SsopSession(name=co.TaskName,
                                     token= co.token,
                                     resources=[
                                                ssop_config.SSOP_RESOURCES["pool-scip-ipopt"]
                                                #ssop_config.SSOP_RESOURCES["hse"],
                                        #        ssop_config.SSOP_RESOURCES["vvvolhome2"],
                                                #ssop_config.SSOP_RESOURCES["vvvoldell"],
                                         #       ssop_config.SSOP_RESOURCES["ui4.kiae.vvvol"],
                                                #ssop_config.SSOP_RESOURCES["govorun.vvvol"],
                                                #ssop_config.SSOP_RESOURCES["vvvolhome"]
                                               ],
                                     workdir=tmpFileDir, debug=False)
#            optFile = 'peipopt.opt'
 #           makeIpoptOptionsFile(co.tmpFileDir,  optFile)
            #print (__peProblems )
            solved, unsolved, jobId = theSession.runJob(__peProblems, co.optFile)  # by default solver = "ipopt"
#            print("solved:   ", solved)
            print("unsolved: ", unsolved)
            print("Job %s is finished" % (jobId))

#            theSession.deleteWorkFiles([".nl", ".sol", ".zip", ".plan"])

        # Delete jobs created to save disk space at Everest server , MAY BE
   #     if args.cleanjobs:
#            theSession.deleteAllJobs()

        # CLOSE THE SESSION !!! MUST BE
            theSession.session.close()

        else :
          for pName in __peProblems:                  # RUN Nl local
            print ("solve", pName+".nl")
#            subprocess.check_call('ipopt3_11_1 -s ' + pName+".nl"+" \"option_file_name=peipopt.opt\"", shell=True)
            subprocess.check_call(co.SolverName+' ' +tmpFileDir+'/'+ pName+".nl -AMPL"+
                                  " \"option_file_name=" +tmpFileDir+ "peipopt.opt\"", shell=True)
        #def gatherNlFileS ( __peProblems, sym_maps ) :
        resultss = []
        for k, pName in enumerate(__peProblems):                         #
#            print (k, "gather", tmpFileDir + "/" +pName+".sol")
            with ReaderFactory(ResultsFormat.sol) as reader:
                results = reader( tmpFileDir + "/" +pName+".sol" )
            results._smap = sym_maps[k]
            if results.solver.termination_condition != TerminationCondition.optimal:
                print ("results.solver.Message: ", results.solver.Message)
                print ("TermCond:", results.solver.termination_condition, '\n')
                if ( results.solver.Message.find ('Search Direction becomes Too Small') >=0
                  or results.solver.Message.find ('Maximum Number of Iterations Exceeded') >=0 ):
                    results.solver.termination_condition = TerminationCondition.optimal
                    results.solver.status = pyomo.opt.SolverStatus.warning
                else :
                    raise RuntimeError("Solver did not terminate with status = optimal")
            resultss.append(results)
        if RunMo == 'S':  theSession.deleteWorkFiles([".nl", ".sol", ".zip", ".plan"])
        return resultss


def  solveProblemsNl( Gr, teachSet, RunMo = 'L' ):   #  'L' - Local, 'N'- Nl local, 'S' - Server
        if RunMo == 'L' :
            resultss = []                                   #!!  ТОЛЬКО ДЛЯ ОДНОГО resultss
            for k in range(len(teachSet)):  # co.CV_NoSets):                                  # make   STABs
                if k > 0: co.Task.ReadSols('.tmp')
 #               Grd_to_Var()
                setMuToTeach(Gr, teachSet[k])
       #         results = co.optFact.solve(Gr, tee=False, keepfiles=True)  # tee=True)   keepfiles=True)  #!!  ТОЛЬКО ДЛЯ ОДНОГО resultss
                results = co.optFact.solve(Gr, tee=False)  # tee=True)   keepfiles=True)  #!!  ТОЛЬКО ДЛЯ ОДНОГО resultss
                get_termination_condition(results)
                resultss.append(results)                    #!!  ТОЛЬКО ДЛЯ ОДНОГО resultss
        else :
            sym_maps, __peProblems = makeNlFileS ( Gr, teachSet )
            resultss = solveNlFileS ( sym_maps, __peProblems, co.tmpFileDir, RunMo )
#            resultss = gatherNlFileS ( __peProblems, sym_maps )
        return resultss

def splitStab ( stab_file ) :
    with open( stab_file ) as f :                        # считываем и разбираем структуру
        nls = f.read().split('n'+str( MU_LABAL ))
    print ('SplitStab', len(nls))
    return  nls


def make_hackStab ( stab_file, Gr ) :
        for s in range(len(Gr.mu)):  Gr.mu[s] = MU_LABAL * 100000 + s
        symbol_map = makeNlFile ( Gr, stab_file + ".nl" )
        nls = splitStab ( stab_file + ".nl" )
        for s in range(len(Gr.mu)):  Gr.mu[s] = 1
        return symbol_map, nls



def hackStab ( stab_file, Gr, nls ) :              #  Мастерим стаб заменяя метку на 0 или NoR / sum!=0
    with open ( stab_file, "w" ) as f :
        NoR = len (Gr.mu)
        new_sum = sum( Gr.mu[s]() for s in range(NoR) )
        new_mu =  NoR / new_sum
#        new_mu =  1/new_sum
        for i, part in enumerate ( nls ):
            if i==0 :  f.write ( part )  # до первого mu
            else    :
                mu_num = int(part[:5])
                if Gr.mu[mu_num] :
                    f.write ( 'n' +str(new_mu) + part[6:] )
                else :
                    f.write ( 'n0'             + part[6:] )
#                print i, mu_num
        return

def hack_Solve ( stab_file, Gr, symbol_map, nls ) :
        hackStab ( stab_file+'.nl' , Gr, nls )
        subprocess.check_call(co.SolverName+' ' + stab_file + ".nl -AMPL"+
                                  " \"option_file_name=" +tmpFileDir+ "peipopt.opt\"", shell=True)
        with ReaderFactory(ResultsFormat.sol) as reader:
            results = reader( stab_file + ".sol" )
        results._smap = symbol_map
        return results


def get_termination_condition(results):
    if results.solver.termination_condition != TerminationCondition.optimal:
        print("results.solver.Message: ", results.solver.Message)
        print("TermCond:", results.solver.termination_condition, '\n')
        if (results.solver.Message.find('Search Direction becomes Too Small') >= 0
                or results.solver.Message.find('Maximum Number of Iterations Exceeded') >= 0):
#            results.solver.termination_condition = TerminationCondition.optimal
            results.solver.status = pyomo.opt.SolverStatus.warning
        else:
            raise RuntimeError("Solver did not terminate with status = optimal")
