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

def Factory (optFile , py_max_iter, py_tol ):
    opt = None
    if optFile is None or co.RunMode[0] == 'L' or co.RunMode[2] == 'L' :
        opt = SolverFactory(co.LocalSolverName)  #'server' :  co.LocalSolverName
        opt.options.update( co.solverOptVal )
    if (not optFile is None) and \
        (co.RunMode[0] != 'L' or co.RunMode[2] != 'L'):
        makeSolverOptionsFile(co.tmpFileDir + '/' + optFile, "ipopt", co.solverOptVal)
    return opt


#    opt.options["print_level"] = 4 #4 #6
 #   opt.options['warm_start_init_point']      = 'yes'
  #  opt.options['warm_start_bound_push']      = co.py_warm_start_bound_push
   # opt.options['warm_start_mult_bound_push'] = co.py_warm_start_mult_bound_push
    #opt.options['constr_viol_tol']            = co.py_constr_viol_tol
#    opt.options['mu_init']                    = 1e-6
 #   opt.options['max_iter']             = py_max_iter
  #  opt.options["tol"]                  = py_tol
#  #  opt.options['acceptable_tol']       = 1e-10
    #opt.options['print_user_options']      = 'yes'
#    print (opt.options)

#    if platform.system() != 'Windows':    opt.options["linear_solver"] = 'ma57'
 #           opt.options["linear_solver"] = 'ma86'

def makeNlFile ( Gr, stab_file ) :
#        if co.Hack_Stab:
 #           make_hackStab( stab_file, Gr )
  #          return co.stab_symbol_map
   #     else:
            _, smap_id = Gr.write( stab_file, format=ProblemFormat.nl )#,  io_options={'symbolic_solver_labels': True})  # создаем стаб
            symbol_map = Gr.solutions.symbol_map[smap_id]
            return symbol_map

def setMuToTeach (Gr, teachSet = [] ) :                 #  teachSet 1 - выбрасываем, 0 - берем
        if co.CV_NoR > 0:
            Gr.mu[:] = 1
            for s in teachSet: Gr.mu[s] = 0

def makeNlFileTeach ( Gr, stab_file, teachSet_k ) :
            setMuToTeach(Gr, teachSet_k )
            return makeNlFile(Gr, co.tmpFileDir + "/" + stab_file + ".nl")

#def makeNlFileTeach_it ( stab_file_teachSet_k ) :
 #   return  makeNlFileTeach(stab_file_teachSet_k[0], stab_file_teachSet_k[1], stab_file_teachSet_k[2])

#from multiprocessing import Pool

def makeNlFileS ( Gr, teachSet ) : #, symbol_map, nls ) :
        __peProblems = [co.TaskName + "0000"+str(k)    for k in range(len(teachSet))]     # __pe - prefix for Pyomo&Everest stuff

        co.stab_NoTeach = len(teachSet)       #  передаем в Lego, чтобы не стабать 1 teach
        print('AAA SvF.Use_var', co.Use_var, co.stab_NoTeach)

        if len(teachSet) >= 2 and co.Hack_Stab:
#        if co.Hack_Stab:
            sym_maps = prep_hackStab(Gr, __peProblems, teachSet)
        else :
            sym_maps = [makeNlFileTeach ( Gr, __peProblems[k], teachSet[k] )  for k in range(len(teachSet))]

 #       print (Gr.mu[:]())
    #    print (.00061146841002*)
  #      1/0
#        return  sym_maps, __peProblems

#        name_teach = [[Gr, __peProblems[k], teachSet[k]] for k in range(len(teachSet))]                                             # __pe - prefix for Pyomo&Everest stuff
 #       sym_maps = [makeNlFileTeach_it ( name_teach[k] ) for k in range(len(teachSet))]
  #      return  sym_maps, __peProblems

#        sym_maps = []
 #       with Pool(5) as p:
  #        sym_maps.append(p.map(makeNlFileTeach_it, name_teach))
   #     print ('***************')
    #    return  sym_maps, __peProblems

#        sym_maps = [0 for k in range(len(teachSet))]
 #       with concurrent.futures.ThreadPoolExecutor(max_workers=co.max_workers) as executor:
            # Start the load operations and mark each future with its pName
  #          NL_Task = { executor.submit ( makeNlFileTeach, Gr, __peProblems[k], teachSet[k] ): k
   #                         for k in range(len(teachSet)) }
    #        for future in concurrent.futures.as_completed(NL_Task):
     #           print (future)
      #          print (NL_Task[future])
       #         k = NL_Task[future]
        #        try:
         #           s_map = future.result()
          #      except Exception as exc:
           #         print('Generated an exception: %s' )#,exc, 'solving', pNam)
            #    else:
             #       sym_maps[k] = s_map
              #      print('Solved')#, pNam )
        print ('for  '+co.TaskName, len(__peProblems), '   files')
        return  sym_maps, __peProblems

import concurrent.futures  ###################

def solveNlFileS ( sym_maps, __peProblems, tmpFileDir, RunMo ) :
        def run_subTask(pName):
            if co.SolverName.find('ipopt') >= 0:    pName_nl = pName + ".nl"
            elif co.SolverName.find('scip') >= 0:   pName_nl = pName
            else:
                print("Solver Name ?")
                exit(-17)

            print('Start', pName )
            subprocess.check_call(co.SolverName + ' ' + tmpFileDir + pName_nl + " -AMPL" +
                              " \"option_file_name=" + tmpFileDir + "peipopt.opt\"", shell=True)
            return pName

        if RunMo == 'S':                                        # RUN dist    #===== solve in parallel ===========
            SvF_resources = []                                                  #####   ABC   28/01/2023
            for r in co.Resources:
                SvF_resources.append(ssop_config.SSOP_RESOURCES[r])
            theSession = SsopSession(name      = co.TaskName + str(co.CV_Iter),
                                     token     = co.token,
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
            print ( co.optFile )
            if co.maxJobs > 0 :
                while ( len (co.jobId_s) > co.maxJobs ) :
                    theSession.session.deleteJob( co.jobId_s[0] )
                    print ('Job  ', co.jobId_s[0], '  was killed' )
                    co.jobId_s.pop(0)
            solved, unsolved, jobId = theSession.runJob(__peProblems, co.optFile)  # by default solver = "ipopt"
#            print("solved:   ", solved)
            print("unsolved: ", unsolved)
            print("Job %s is finished" % (jobId))
            co.jobId_s.append(jobId)
#            theSession.deleteWorkFiles([".nl", ".sol", ".zip", ".plan"])

        # Delete jobs created to save disk space at Everest server , MAY BE
   #     if args.cleanjobs:
#            theSession.deleteAllJobs()

        # CLOSE THE SESSION !!! MUST BE
            theSession.session.close()
        elif RunMo == 'P':  ###################################
            with concurrent.futures.ThreadPoolExecutor(max_workers=co.max_workers) as executor:
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

from   copy   import *

def  solveProblemsNl( Gr, teachSet, RunMo = 'L' ):   #  'L' - Local, 'N'- Nl local, 'S' - Server
        if RunMo == 'L' :
            resultss = []                                   #!!  ТОЛЬКО ДЛЯ ОДНОГО resultss
            for k in range(len(teachSet)):  # co.CV_NoSets):                                  # make   STABs
                if k > 0: co.Task.ReadSols('.tmp')
                setMuToTeach(Gr, teachSet[k])
                results = co.optFact.solve(Gr, tee=False)  # tee=True)   keepfiles=True)  #!!  ТОЛЬКО ДЛЯ ОДНОГО resultss
                get_termination_condition(results)
                resultss.append(results)                    #!!  ТОЛЬКО ДЛЯ ОДНОГО resultss
##                resultss.append(deepcopy(results))  # НЕ ПОМОГЛО !!!!      #!!  ТОЛЬКО ДЛЯ ОДНОГО resultss
        else :
            sym_maps, __peProblems = makeNlFileS ( Gr, teachSet )
            resultss = solveNlFileS ( sym_maps, __peProblems, co.tmpFileDir, RunMo )
        return resultss

#MU_LABAL = 19541117

#def splitStab ( stab_file ) :
 #   with open( stab_file ) as f :                        # считываем и разбираем структуру
  #      nls = f.read().split('n'+str( co.stabMU_LABAL ))
   # print ('SplitStab', len(nls))
    #return  nls

def prep_hackStab (Gr, __peProblems, teachSet):
#        print('SSSS SvF.Use_var', co.Use_var, co.stab_NoTeach)
    ######        co.stab_symbol_map = makeNlFile ( Gr, stab_file + ".nl" )
        _, smap_id = Gr.write(co.stab_file, format=ProblemFormat.nl ) #,  io_options={'symbolic_solver_labels': True})  # создаем стаб
 #       _, smap_id = Gr.write(stab_file + ".nl", format=ProblemFormat.nl)  # ,  io_options={'symbolic_solver_labels': True})  # создаем стаб
        stab_symbol_map = Gr.solutions.symbol_map[smap_id]
        with open(co.stab_file) as f:  # считываем и разбираем структуру по ка для одного co.stab_val_sub[0]
            txt = f.read()
            st_val = ''
            ind = txt.find ('\nn')
            while (ind >= 0):
                end = txt.find ('\n',ind+1)
#                print(txt[ind + 2:end])
                try:
                    val = float(txt[ind+2:end])
#                    print (txt[ind+2:end],val)
                    if abs (val-co.stab_val_sub[0])/co.stab_val_sub[0] < 1e-9:  # значение строки близко к co.stab_val_sub[0]
                        st_val = txt[ind + 2:end]
                        break
                except ValueError:
                    pass
                ind = txt.find('\nn', ind + 1)
            print ('st_val = ', st_val)
            nls = txt.split('n'+st_val)
        print('SplitStab', len(nls), co.stab_val_sub[0], st_val)
        sym_maps = []
        for n_f, stab_val in enumerate (co.stab_val_by_cv):
            make_hackStab ( co.tmpFileDir + "/" + __peProblems[n_f] + ".nl", stab_val, nls )
#            print ('make_hackStab ( ', co.tmpFileDir + "/" + __peProblems[n_f] + ".nl" )
            sym_maps.append (stab_symbol_map)

        co.stab_val_sub = []
        co.stab_val_by_cv = []

        for s in range(len(Gr.mu)):  Gr.mu[s] = 1
        return sym_maps

def make_hackStab ( stab_file, stab_val, nls ) :              #  Мастерим стаб заменяя  stab_val на stab_val_by_cv
    with open ( stab_file, "w" ) as f :
        print ('len(nls)', len(nls), len(stab_val))
        for i, part in enumerate ( nls ):
            if i==0 :  f.write ( part )  # до первого mu
            else    :  f.write('n' + str(stab_val[i - 1]) + part)
    return

def make_hackStab_old ( stab_file, Gr ) :              #  Мастерим стаб заменяя метку на 0 или NoR / sum!=0
    with open ( stab_file, "w" ) as f :
        print ('len(co.stab_nls)', len(co.stab_nls))
        for i, part in enumerate ( co.stab_nls ):
            if i==0 :  f.write ( part )  # до первого mu
            else    :
                mu_num = int(part[:5])
                print ('MMMMMMMM', i,mu_num,Gr.mu[mu_num]() ) #, part[6:])
                if Gr.mu[mu_num]() == 1 :
                    f.write ( 'n' +str(co.stab_value[i-1]) + part[5:] )
                else :
                    f.write ( 'n0'             + part[5:] )
#                print i, mu_num
        return


#def hack_Solve ( stab_file, Gr, symbol_map, nls ) :
 #       make_hackStab ( stab_file+'.nl' , Gr, nls )
  #      subprocess.check_call(co.SolverName+' ' + stab_file + ".nl -AMPL"+
   #                               " \"option_file_name=" +tmpFileDir+ "peipopt.opt\"", shell=True)
    #    with ReaderFactory(ResultsFormat.sol) as reader:
     #       results = reader( stab_file + ".sol" )
      #  results._smap = symbol_map
       # return results


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
