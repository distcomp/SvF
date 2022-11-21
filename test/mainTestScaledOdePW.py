import os
import math
import random

import pyomo.environ as pyo

from testScaledOdePW import init_XtFx, add_ode1_XtFx, add_ode2_XtFx, \
                            add_ode1_XtFx_sos, add_ode2_XtFx_sos, add_ode1_XtFx_log, \
                            MSD_expr, REG_expr,  add_SvFObject, XTScaling, \
                            replace_ode1_sm_to_sos
# from testSplinePW import addSpline_XtFy

# The following imports are from /asl_io/write module
from write import write_nl_only, write_nl_smap
from write import get_smap_var
from read import read_sol_smap_var #, read_sol_smap
from testPlotPW import plotScaledModelPW
import subprocess
import time

IPOPT_EXE = '/opt/solvers/bin/ipopt'
SCIP_EXE  = '/opt/solvers/bin/scip'
# IPOPT_EXE = 'ipopt'

def getModelName(prefix, args):
    Nt = args.tLoUpND[2]
    Nd = args.tLoUpND[3]
    Nx = args.xLoUpN[2]
    reg = args.regcoeff
    err = args.errdata
    prefixOffSpaces = prefix.replace(" ",'')
    if args.useEta:
        discretMethod = 'ETA'
    else:
        discretMethod = 'SQRT'
    if args.sos2:
        discretMethod = 'SOS2'
    if args.log:
        discretMethod = 'LOG'

    odeType = ''
    if args.order == 1:
         odeType = args.ode1

    if not args.sos2 and not args.log:
        return ('%s_%s_ODE%s_%s_Nt_%d_Nd_%d_Nx_%d_err_%.f_reg_%.4f')%(
            prefixOffSpaces, discretMethod, str(args.order)+odeType, args.solver, Nt, Nd, Nx, err*100, reg)
    else:
        return ('%s_%s_ODE%s_Nt_%d_Nd_%d_Nx_%d_err_%.f_reg_%.4f') % (
            prefixOffSpaces, discretMethod, str(args.order)+odeType, Nt, Nd, Nx, err*100, reg)

def getNLname(model, args):
    return model.getname()

def makeNLfile(model, args):
    # probName = model.getname().replace(" ",'')
    # workdir = params["workdir"]
    workdir = args.workdir
    try:
        os.mkdir(workdir)
    except OSError:
        pass
    # nlFile = write_nl_only(model, workdir + '/' + getNLname(model, args),  symbolic_solver_labels=True)
    nlFile = write_nl_only(model, workdir + '/' + model.getname(), symbolic_solver_labels=True)
    return nlFile

def readSol(model, nl_file):
    model_smap = get_smap_var(model)
    results = read_sol_smap_var(model, nl_file[:-len('.nl')], model_smap)
    model.solutions.load_from(results)
    return

def IpoptScip4SOS2(IpoptModel):
    pass

def printData(model):
    Nt = len(model.Xt) - 1
    Nx = len(model.Fx) - 1
    print("||||||||||| DATA |||||||||||||||")
    print("Nt = ", Nt, " Nx = ", Nx)
    print("meshT[t]: ", [pyo.value(model.meshT[t]) for t in model.setTidx])
    print("meshX[y]: ", [pyo.value(model.meshX[y]) for y in model.setXidx])
    print("||||||||||||||||||||||||||||||||")

def check_args(args):
    Nt = int(args.tLoUpND[2])
    tLo = args.tLoUpND[0]
    tUp = args.tLoUpND[1]
    Nx = int(args.xLoUpN[2])
    xLo = args.xLoUpN[0]
    xUp = args.xLoUpN[1]
    FxLo = args.FxLoUp[0]
    FxUp = args.FxLoUp[1]
    theFunc = "check_args"
    if Nt < 4:
        raise Exception("%s: Nt=%d < 4... too few" % (theFunc, Nt))
    elif Nx < 5:
        raise Exception("%s: Nx=%d < 5... too few" % (theFunc, Nx))
    elif tLo > tUp:
        raise Exception("%s: tLo=%f > tUp=%f" % (theFunc, tLo, tUp))
    elif xLo > xUp:
        raise Exception("%s: xLo=%f > xtUp=%f" % (theFunc, xLo, xUp))
    elif FxLo > FxUp:
        raise Exception("%s: FxLo=%f > FxtUp=%f" % (theFunc, FxLo, FxUp))

    return tLo, tUp, Nt, xLo, xUp, Nx, FxLo, FxUp

# -o 2 --tLoUpND 0. 3. 30 15 --xLoUpN -1.5 1.5 10 --FxLoUp -7.0 7. -err .05 -reg 0.001 -eps 0.001
# -o 1 --tLoUpND 0.0 3. 20 10  --xLoUpN .0 25.0 30 --FxLoUp .0 26. -eps 0.001 -reg 1. -err 0.0 -s ipopt
# GLOBAL
#-o 2 --tLoUpND 0. 3. 25 10 --xLoUpN -1.5 1.5 20 --FxLoUp -7.0 7. -err .05 -reg 1 -eps 0.001 -s ipopt -s scip

# -sos2 -o 2 --tLoUpND 0. 3. 14 5 --xLoUpN -1.5 1.5 7 --FxLoUp -7.0 7. -reg .1 -err .0 -s scip
# -sos2 -o 1 --tLoUpND 0.0 3. 10 5  --xLoUpN .0 25.0 5 --FxLoUp .0 26. -reg .1 -err 0.0
import argparse
def makeParser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)#@!!ctlbr517
    parser.add_argument('-pr', '--prefix', default="OdePw", type=str, help='Prefix of problem name')
    parser.add_argument('-wd', '--workdir', default='tmp', help='working directory')
    parser.add_argument('-s', '--solver', default='ipopt', choices=['ipopt', 'scip'], help='solver to use')
    parser.add_argument('-ode1', '--ode1', default='exp', choices=['exp', 'square'], help='type of ODE1')
    parser.add_argument('-t', '--tLoUpND', nargs='+', default=[0., 3., 10, 5], type=float, help='t: Lo Up N number of data')
    parser.add_argument('-x', '--xLoUpN', nargs='+', default=[-1.5, 1.5, 5], type=float, help='x: Lo Up N')
    parser.add_argument('-Fx', '--FxLoUp', nargs='+', default=[-100., 100.], type=float, help='Lo Up limits for Fx')
    parser.add_argument('-o', '--order', default=2, choices=[1,2,0], type=int, help='ODE order 1 or 2 (reduced form), 0 - SPLINE')
    parser.add_argument('-eps', '--epsilon', default=0.01, type=float, help='Epsilon to smooth pos()')
    parser.add_argument('-reg', '--regcoeff', default=.005, type=float, help='Regularization coefficient')
    parser.add_argument('-err', '--errdata', default=.1, type=float, help='Error of data')
    parser.add_argument('-eta', '--useEta', action='store_true', help='use Eta in discretization')
    parser.add_argument('-pw2sos', '--pw2sos', action='store_true', help='use PW to get initial solution for SOS2')
    parser.add_argument('-sos2', '--sos2', action='store_true', help='use SOS2 for discretization')
    parser.add_argument('-log', '--log', action='store_true', help='use LOG for discretization')
    return parser

if __name__ == "__main__":
    parser = makeParser()
    args = parser.parse_args()
    # vargs = vars(args)
    print('Arguments of the test')
    if args.sos2:
        args.solver = 'scip'
    print('======================')
    for arg in vars(args):
        print(arg + ":", getattr(args, arg))
    print('======================')
    tLo, tUp, Nt, xLo, xUp, Nx, FxLo, FxUp = check_args(args)
    Ndata = int(args.tLoUpND[3])
    regCoeff = args.regcoeff
    print(">>>> tLo=%f, tUp=%f, Nt=%d, xLo=%f, xUp=%f, Nx=%d, FxLo=%f, FxUp=%f" % (tLo, tUp, Nt, xLo, xUp, Nx, FxLo, FxUp) )

    # True/actual Fx depending on args
    def getTrueFx(args):
        if args.order == 2:
            # F(x) = -4*x
            return lambda x: -4*x
        elif args.order == 1:
            if args.ode1 == 'exp':
                # F(x) = x
                return lambda x: x
            elif args.ode1 == 'square':
                # F(x) = x^2
                return lambda x: x**2
            else:
                raise Exception("UNKNOWN ODE1: %s" % (args.ode1))
        else:
            raise Exception("UNKNOWN Generator XtData")

    # Experimental data with error
    randomError = [random.uniform(-args.errdata/2., args.errdata/2.) for k in range(0,Ndata+1)]
    def generatorXtData(t: float, k: int):
        if args.order == 2:
            # F(x) = -4*x
            return (math.sin(2*t) + math.cos(2*t))*(1. + randomError[k])
        elif args.order == 1:
            if args.ode1 == 'exp':
                # F(x) = x
                return math.exp(t)*(1. + randomError[k])
            elif args.ode1 == 'square':
                # F(x) = x^2
                return (1./(1. - t))*(1. + randomError[k])
            else:
                raise Exception("UNKNOWN ODE1: %s" % (args.ode1))
        else:
            raise Exception("UNKNOWN Generator XtData")
    # Fill txValuesData list
    txDataValues = []
    for k in range(Ndata+1):
        tk = tLo + k*(tUp - tLo)/Ndata
        txDataValues.append( (tk, generatorXtData(tk, k)) )
    for tx in txDataValues:
        t, x = tx[0], tx[1]
        tLo, tUp = min(t, tLo), max(t, tUp)
        xLo, xUp = min(x, xLo), max(x, xUp)
    # Bounds on t and x may be CHANGED !
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    xtmesh  = XTScaling(tLo, tUp, Nt, xLo, xUp, Nx, FxLo, FxUp, args.errdata)
    # ===========================================
    print('>>>>>>>>> DATA =========')
    print(">>>> tLo=%f, tUp=%f, Nt=%d, xLo=%f, xUp=%f, Nx=%d, FxLo=%f, FxUp=%f" % (tLo, tUp, Nt, xLo, xUp, Nx, FxLo, FxUp) )
    print("data, t, x")
    for tx in txDataValues:
        print("%f  %f" % (tx[0], tx[1]))
    # print("data, t: ", [tx[0] for tx in txDataValues])
    # print("data, x: ", [tx[1] for tx in txDataValues])
    print('========================')
    # ============================
    if args.pw2sos:
        args.prefix = "OdePw2sos"
    theModel = pyo.ConcreteModel(getModelName(args.prefix, args))
    # theModel.name = getNLname(theModel, args)
    print("Model name: ", theModel.getname())

    init_XtFx(theModel, xtmesh)

    if args.order == 1:
        if args.sos2 and not args.pw2sos:
            add_ode1_XtFx_sos(theModel, xtmesh)
        if args.log and not args.pw2sos:
            add_ode1_XtFx_log(theModel, xtmesh)
        if not args.sos2 and not args.log : # and args.pw2sos
            add_ode1_XtFx(theModel, xtmesh, eps=args.epsilon, useEta=args.useEta)
    elif args.order == 2:
        if args.sos2 and not args.pw2sos:
            add_ode2_XtFx_sos(theModel, xtmesh)
        if args.log:
            raise Exception("LOG is not implemented for ODE2 yet")
        if not args.sos2 and not args.log:
            add_ode2_XtFx(theModel, xtmesh, eps=args.epsilon, useEta=args.useEta)
        # if not args.sos2:
        #     add_ode2_XtFx(theModel, xtmesh, eps=args.epsilon, useEta=args.useEta)
        # else:
        #     add_ode2_XtFx_sos(theModel, xtmesh)
    else:
        raise Exception("UNKNOWN Type of equation OR pw2sos !!!")

    add_SvFObject(theModel, xtmesh, txDataValues, args.regcoeff)
    # printData(theModel)

    if args.log:
        theModel.pprint()
        # quit()

    with open(args.workdir + '/' + theModel.getname() + '.model.txt', 'w') as out_file:
        theModel.pprint(ostream = out_file)
        out_file.close()
    # quit()

    nl_file = makeNLfile(theModel, args)
    print(nl_file)
    # The name to distinguish tests
    the_test_name = nl_file[:-len('.nl')]

    print('Running in the folder:')
    subprocess.check_call("pwd")
    print('||||||||||||||||||||||')
    # quit()
    tic = time.perf_counter()
    if args.pw2sos:
        subprocess.check_call(
            IPOPT_EXE + ' ' + nl_file + " -AMPL \"option_file_name=" + "ipopt.opt\" | tee " + the_test_name + ".log.txt",
            shell=True)
        readSol(theModel, nl_file)
        with open(args.workdir + '/' + theModel.getname() + '.model.txt', 'w') as out_file:
            theModel.pprint(ostream=out_file)
            out_file.close()
        replace_ode1_sm_to_sos(theModel, xtmesh)
        print("SOS2 Model with initial solution = " + theModel.getname())
        with open(args.workdir + '/' + theModel.getname() + '.model.txt', 'w') as out_file:
            theModel.pprint(ostream=out_file)
            out_file.close()
        nl_file = makeNLfile(theModel, args)
        print(nl_file)
        # The name to distinguish tests
        the_test_name = nl_file[:-len('.nl')]
        print("Test name: " + the_test_name)
        subprocess.check_call(SCIP_EXE + ' ' + nl_file[:-len('.nl')] + " -AMPL | tee " + the_test_name + ".log.txt",
                              shell=True)
        quit()
    #

    if args.solver == 'ipopt' and not args.sos2 and not args.log:
        subprocess.check_call(IPOPT_EXE + ' ' + nl_file + " -AMPL \"option_file_name=" + "ipopt.opt\" | tee " + the_test_name + ".log.txt", shell=True)# +
    else:
        subprocess.check_call(SCIP_EXE + ' ' + nl_file[:-len('.nl')] + " -AMPL | tee " + the_test_name + ".log.txt", shell=True)
    toc = time.perf_counter()
    print("!!!!! Solved in: %f sec !!!!!!" % (toc - tic))
    readSol(theModel, nl_file)

    msdSol = pyo.value(MSD_expr(theModel, xtmesh, txDataValues))
    regSol = pyo.value(REG_expr(theModel, xtmesh, regCoeff))
    # (msdSol, regSol) = getMSD_REG(theModel)

    with open(args.workdir + '/' + theModel.getname() + '.model.txt', 'w') as out_file:
        theModel.pprint(ostream = out_file)
        out_file.close()

    print('SvF obj.: ', pyo.value(theModel.svfObj))
    print('MSD = %f, REG = %f' % (msdSol, regSol))
    print('F(x): ', [pyo.value(theModel.Fx[j]) for j in pyo.RangeSet(0,Nx)])
    print('X(t): ', [pyo.value(theModel.Xt[t]) for t in pyo.RangeSet(0,Nt)])
    if args.sos2:
        if args.order == 2:
            for k in theModel.ode2_sos_bs.index_set():
                print('wsos[%f]: ' % (pyo.value(k)), [pyo.value(theModel.ode2_sos_bs[k].wsos[xj]) for xj in pyo.RangeSet(0, Nx)])
        if args.order == 1:
            for k in theModel.ode1_sos_bs.index_set():
                print('wsos[%f]: ' % (pyo.value(k)), [pyo.value(theModel.ode1_sos_bs[k].wsos[xj]) for xj in pyo.RangeSet(0, Nx)])

    # quit()

    # plotModelPW(theModel, nl_file[:-len('.nl')])
    plotScaledModelPW(theModel, xtmesh, txDataValues, getTrueFx(args), nl_file[:-len('.nl')])
    quit()
