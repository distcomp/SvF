# -*- coding: UTF-8 -*-
from __future__ import division
import subprocess

import COMMON as SvF

from Task    import Grd_to_Var

import platform

#from pyomo.environ import *
#import pyomo.environ as py
from pyomo.opt import SolverFactory
from pyomo.opt import ProblemFormat
from pyomo.opt import TerminationCondition
from pyomo.opt import (ReaderFactory,ResultsFormat)
import pyomo   #      05.10.24

from ssop_session import *

def Factory (optFile , py_max_iter, py_tol ):
    opt = None
    if optFile is None or SvF.RunMode[0] == 'L' or SvF.RunMode[2] == 'L' :
        opt = SolverFactory(SvF.LocalSolverName)  #'server' :  SvF.LocalSolverName
        opt.options.update( SvF.solverOptVal )
    if (not optFile is None) and \
        (SvF.RunMode[0] != 'L' or SvF.RunMode[2] != 'L'):
        makeSolverOptionsFile(SvF.tmpFileDir + '/' + optFile, "ipopt", SvF.solverOptVal)
    return opt


#    opt.options["print_level"] = 4 #4 #6
 #   opt.options['warm_start_init_point']      = 'yes'
  #  opt.options['warm_start_bound_push']      = SvF.py_warm_start_bound_push
   # opt.options['warm_start_mult_bound_push'] = SvF.py_warm_start_mult_bound_push
    #opt.options['constr_viol_tol']            = SvF.py_constr_viol_tol
#    opt.options['mu_init']                    = 1e-6
 #   opt.options['max_iter']             = py_max_iter
  #  opt.options["tol"]                  = py_tol
#  #  opt.options['acceptable_tol']       = 1e-10
    #opt.options['print_user_options']      = 'yes'
#    print (opt.options)

#    if platform.system() != 'Windows':    opt.options["linear_solver"] = 'ma57'
 #           opt.options["linear_solver"] = 'ma86'

def makeNlFile ( Gr, stab_file ) :
            _, smap_id = Gr.write( stab_file, format=ProblemFormat.nl )#,  io_options={'symbolic_solver_labels': True})  # создаем стаб
            symbol_map = Gr.solutions.symbol_map[smap_id]
            return symbol_map

#def setMuToTeach (Gr, notTrainingSets = [] ) :                 #  notTrainingSets 1 - выбрасываем, 0 - берем
 #       if SvF.CV_NoRs[0] > 0:
  #          Gr.mu0[:] = 1
   #         for s in notTrainingSets: Gr.mu0[s] = 0

def setMuToTeach_k (k) :                 #  notTrainingSets 1 - выбрасываем, 0 - берем
    for f in SvF.fun_with_mu:
#        print (len(SvF.fun_with_mu), f.name, len (f.mu), k)
        f.mu[:] = 1
        if type(k) == type(1):
           for s in f.notTrainingSets[k]:   f.mu[s].value = 0


#def makeNlFileTeach(Gr, stab_file, notTrainingSets_k):
 #   setMuToTeach(Gr, notTrainingSets_k)
  #  return makeNlFile(Gr, SvF.tmpFileDir + "/" + stab_file + ".nl")


def makeNlFileTeach_k(Gr, stab_file, k):
    setMuToTeach_k(k)
    return makeNlFile(Gr, SvF.tmpFileDir + "/" + stab_file + ".nl")


def makeNlFileS ( Gr, SetNum ) : #, symbol_map, nls ) :
    if SetNum == '' :
        __peProblems = [SvF.TaskName + "0000" + '0']
        sym_maps = [makeNlFileTeach_k(Gr, __peProblems[0], '')]
    else :
        __peProblems = [SvF.TaskName + "0000"+str(k)    for k in range(SvF.CV_NoSets)]     # __pe - prefix for Pyomo&Everest stuff

 #       SvF.stab_NoTeach = len(notTrainingSets)       #  передаем в Lego, чтобы не стабать 1 teach
  #      print('AAA SvF.Use_var', SvF.Use_var, SvF.stab_NoTeach)

        if SvF.CV_NoSets >= 2 and SvF.Hack_Stab:
            sym_maps = prep_hackStab(Gr, __peProblems)
        else :
            sym_maps = [makeNlFileTeach_k ( Gr, __peProblems[k], k )  for k in range(SvF.CV_NoSets)]
#            sym_maps = [makeNlFileTeach ( Gr, __peProblems[k], notTrainingSets[k] )  for k in range(len(notTrainingSets))]

    print ('for  '+SvF.TaskName, len(__peProblems), '   files')
    return  sym_maps, __peProblems

import concurrent.futures  ###################

def solveNlFileS ( sym_maps, __peProblems, tmpFileDir, RunMo ) :
        def run_subTask(pName):
            if SvF.SolverName.find('ipopt') >= 0:    pName_nl = pName + ".nl"
            elif SvF.SolverName.find('scip') >= 0:   pName_nl = pName
            else:
                print("Solver Name ?")
                exit(-17)

            print('Start', pName )
            subprocess.check_call(SvF.SolverName + ' ' + tmpFileDir + pName_nl + " -AMPL" +
                              " \"option_file_name=" + tmpFileDir + "peipopt.opt\"", shell=True)
            return pName

        if RunMo == 'S':                                        # RUN dist    #===== solve in parallel ===========
            SvF_resources = []                                                  #####   ABC   28/01/2023
            for r in SvF.Resources:
                SvF_resources.append(ssop_config.SSOP_RESOURCES[r])
            theSession = SsopSession(name      = SvF.TaskName + str(SvF.CV_Iter),
                                     token     = SvF.token,
                                     resources = SvF_resources,

##                                     resources=[
  ##                                              ssop_config.SSOP_RESOURCES["pool-scip-ipopt"]
                                                #ssop_config.SSOP_RESOURCES["hse"],
                                        #        ssop_config.SSOP_RESOURCES["vvvolhome2"],
                                                #ssop_config.SSOP_RESOURCES["vvvoldell"],
                                         #       ssop_config.SSOP_RESOURCES["ui4.kiae.vvvol"],
                                                #ssop_config.SSOP_RESOURCES["govorun.vvvol"],
                                                #ssop_config.SSOP_RESOURCES["vvvolhome"]
    ##                                           ],
                                     workdir=tmpFileDir, debug=False)
            print (__peProblems )
            print ( SvF.optFile )
            if SvF.maxJobs > 0 :
                while ( len (SvF.jobId_s) > SvF.maxJobs ) :
                    theSession.session.deleteJob( SvF.jobId_s[0] )
                    print ('Job  ', SvF.jobId_s[0], '  was killed' )
                    SvF.jobId_s.pop(0)
            solved, unsolved, jobId = theSession.runJob(__peProblems, SvF.optFile)  # by default solver = "ipopt"
#            print("solved:   ", solved)
            print("unsolved: ", unsolved)
            print("Job %s is finished" % (jobId))
            SvF.jobId_s.append(jobId)
#            theSession.deleteWorkFiles([".nl", ".sol", ".zip", ".plan"])

        # Delete jobs created to save disk space at Everest server , MAY BE
   #     if args.cleanjobs:
#            theSession.deleteAllJobs()

        # CLOSE THE SESSION !!! MUST BE
            theSession.session.close()
        elif RunMo == 'P':  ###################################
            with concurrent.futures.ThreadPoolExecutor(max_workers=SvF.max_workers) as executor:
            # Start the load operations and mark each future with its pName
              PNameTask = {executor.submit(run_subTask, pName): pName for pName in __peProblems}
              for future in concurrent.futures.as_completed(PNameTask):
                pNam = PNameTask[future]
                try:
                    future.result()
                except Exception as exc:
                    print('Generated an exception: %s' ,exc, 'solving', pNam)
                else:
                    print(pNam, ' is Solved' )
        else :                  #  RunMo == 'O':  ###################################  One by one
          for pName in __peProblems:   run_subTask(pName)             # RUN Nl local

        resultss = []
        for k, pName in enumerate(__peProblems):                         #
            with ReaderFactory(ResultsFormat.sol) as reader:
                results = reader( tmpFileDir + "/" +pName+".sol" )
            results._smap = sym_maps[k]
            print (pName, results.solver.termination_condition)
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

def  solveProblemsNl( Gr, SetNum, RunMo = 'L' ):   #  'L' - Local, 'N'- Nl local, 'S' - Server
        if RunMo == 'L' :
                resultss = []                                   #!!  ТОЛЬКО ДЛЯ ОДНОГО resultss
                setMuToTeach_k(SetNum)
                results = SvF.optFact.solve(Gr, tee=False)  # tee=True)   keepfiles=True)  #!!  ТОЛЬКО ДЛЯ ОДНОГО resultss
                get_termination_condition(results)
                resultss.append(results)                    #!!  ТОЛЬКО ДЛЯ ОДНОГО resultss
##                resultss.append(deepcopy(results))  # НЕ ПОМОГЛО !!!!      #!!  ТОЛЬКО ДЛЯ ОДНОГО resultss
        else :
            sym_maps, __peProblems = makeNlFileS ( Gr, SetNum )
            resultss = solveNlFileS ( sym_maps, __peProblems, SvF.tmpFileDir, RunMo )
        return resultss

def prep_hackStab (Gr, __peProblems):
#        SvF.stab_val_sub = []    #  нельзя:  массив уже сформирован
        _, smap_id = Gr.write(SvF.stab_file, format=ProblemFormat.nl ) #,  io_options={'symbolic_solver_labels': True})  # создаем стаб
        stab_symbol_map = Gr.solutions.symbol_map[smap_id]
        with open(SvF.stab_file) as f:  # считываем и разбираем структуру по ка для одного SvF.stab_val_sub[0]
          tfile = f.read()
          nls = [tfile]
          old_val = -1
          for val_sub in SvF.stab_val_sub :
#            print (val_sub, old_val)
            if val_sub == old_val : continue
            txt = nls[-1]
            beg = txt.find ('\nn')
            while (beg >= 0):
                end = txt.find ('\n',beg+1)
                try:
                    val = float(txt[beg+2:end])
                    if abs (val-val_sub)/val_sub < 1e-9:  # значение строки близко к SvF.stab_val_sub[0]
                        str_val = txt[beg + 2:end]
                        print('st_val = ', str_val)
                        nls.pop()
                        nls = nls+ txt.split('n' + str_val)
                        old_val = val_sub
                        break
                except ValueError:
                    pass
                beg = txt.find('\nn', beg + 1)
#            print ('st_val = ', str_val)
 #           nls.append( txt.split('n'+str_val) )
        if len (nls) != len (SvF.stab_val_sub)+1 :
            print ('len (nls) != len (SvF.stab_val_sub)+1', len (nls), len (SvF.stab_val_sub)+1 )
            exit (-333)
        print('SplitStab OK', len(nls), len (SvF.stab_val_sub))
        sym_maps = []
        for n_f, stab_val in enumerate (SvF.stab_val_by_cv):
            make_hackStab ( SvF.tmpFileDir + "/" + __peProblems[n_f] + ".nl", stab_val, nls )
#            print ('make_hackStab ( ', SvF.tmpFileDir + "/" + __peProblems[n_f] + ".nl" )
            sym_maps.append (stab_symbol_map)
        SvF.stab_val_sub = []
        SvF.stab_val_by_cv = []

        for s in range(len(Gr.mu0)):  Gr.mu0[s] = 1
        return sym_maps

def make_hackStab ( stab_file, stab_val, nls ) :              #  Мастерим стаб заменяя  stab_val на stab_val_by_cv
    with open ( stab_file, "w" ) as f :
        print ('len(nls)', len(nls), len(stab_val))
        for i, part in enumerate ( nls ):
            if i==0 :  f.write ( part )  # до первого mu
            else    :  f.write('n' + str(stab_val[i - 1]) + part)
    return

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
