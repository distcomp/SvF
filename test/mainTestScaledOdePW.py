import os
import math
import random

import pyomo.environ as pyo

from testScaledOdePW import init_scaled_XtFx, add_scaled_ode1_XtFx, add_scaled_ode2_XtFx, add_scaled_SvFObject
# from testSplinePW import addSpline_XtFy

# The following imports are from /asl_io/write module
from write import write_nl_only, write_nl_smap
from write import get_smap_var
from read import read_sol_smap_var #, read_sol_smap
from testPlotPW import plotModelPW
import subprocess

IPOPT_EXE = '/opt/solvers/bin/ipopt'
# IPOPT_EXE = 'ipopt'

# def addSvfObject(model: pyo.ConcreteModel, XtDataFunction):
#     dt = model.dt.value
#     dy = model.dy.value
#     Nt = len(model.Xt) - 1
#     Nx = len(model.Fx) - 1
#
#     def XtData_init(m, k):
#         return XtDataFunction(m.meshT[k], k)
#     model.XtData = pyo.Param(model.setTidx, initialize=XtData_init)
#
#     def svfObj_rule(m):
#         return ((1./Nt)*sum( (m.Xt[k] - m.XtData[k])**2 for k in pyo.RangeSet(0, Nt)) +
#                 m.regCoeff*(1/dy**3)*(1./Nx)*sum((m.Fx[j+1] - 2*m.Fx[j] + m.Fx[j-1])**2 for j in pyo.RangeSet(1, Nx - 1)))
#     model.svfObj = pyo.Objective(rule=svfObj_rule, sense=pyo.minimize)

# def getMSD_REG(model: pyo.ConcreteModel):
#     Nt = len(model.Xt) - 1
#     Nx = len(model.Fx) - 1
#     MSD = sum( (pyo.value(model.Xt[k]) - pyo.value(model.XtData[k]))**2 for k in pyo.RangeSet(0, Nt))/Nt
#     REG = pyo.value(model.regCoeff)*(1/model.dy**3)*(1./Nx)*sum((pyo.value(model.Fx[j+1]) - 2*pyo.value(model.Fx[j]) + pyo.value(model.Fx[j-1]))**2 for j in pyo.RangeSet(1, Nx - 1))
#     return (MSD, REG)

# def initUniformMesh4XtFy(model: pyo.ConcreteModel):
#     """
#     It is assumed that model has:
#     parameters:
#      Nt, Nx, tLimits = {tLo, tUp}, yLmits = {xLo, xUp}
#     variables Xt[0:Nt], Fx[0:Nx]
#     """
#     tLo = model.tLimits[0]
#     tUp = model.tLimits[1]
#     xLo = model.xLimits[0]
#     xUp = model.xLimits[1]
#     Nt = len(model.Xt) - 1
#     Nx = len(model.Fx) - 1
#
#     dt = (tUp - tLo)/Nt
#     model.dt = pyo.Param(initialize=dt)
#     def meshT_init(m, k):
#         return tLo + k*dt
#     model.meshT = pyo.Param(model.setTidx, initialize=meshT_init)
#
#     dy = (xUp - xLo) / Nx
#     model.dy = pyo.Param(initialize=dy)
#     def meshY_init(m, i):
#         return xLo + i * dy
#     model.meshX = pyo.Param(model.setXidx, initialize=meshY_init)
#
# def initXtFy(model: pyo.ConcreteModel, tLo: float, tUp: float, Nt: int, funcDataXt, xLo: float, xUp: float, Nx: int,
#              FxLo: float, FxUp: float, regCoeff):
#     # Nt = len(setT) - 1
#     if tLo > tUp:
#         raise Exception(("tLo=%f > tUp=%f")%(tLo, tUp))
#     if xLo > xUp:
#         raise Exception(("xLo=%f > xUp=%f")%(xLo, xUp))
#     if FxLo > FxUp:
#         raise Exception(("FxLo=%f > FxUp=%f")%(xLo, xUp))
#
#     model.regCoeff = pyo.Param(initialize=regCoeff)
#
#     model.setTidx = pyo.RangeSet(0, Nt)
#     model.tLimits = pyo.Param(pyo.RangeSet(0,1), initialize=(tLo, tUp), within=pyo.Reals)
#     LO_Xt = min(funcDataXt(tLo + (tUp - tLo)*k/Nt, k) for  k in model.setTidx)
#     LO_Xt = LO_Xt - abs(LO_Xt)*.1
#     UP_Xt = max(funcDataXt(tLo + (tUp - tLo)*k/Nt, k) for  k in model.setTidx)
#     UP_Xt = UP_Xt + abs(UP_Xt)*.1
#     # model.xLimits = pyo.Param(pyo.RangeSet(0,1), initialize=(LO_Xt, UP_Xt), within=pyo.Reals)
#
#     # Create x-meshgrid
#     model.setXidx = pyo.RangeSet(0, Nx)
#     model.xLimits = pyo.Param(pyo.RangeSet(0,1), initialize=(min(xLo, LO_Xt), max(xUp, UP_Xt)), within=pyo.Reals)
#     model.FxLimits = pyo.Param(pyo.RangeSet(0,1), initialize=(FxLo, FxUp), within=pyo.Reals)
#
#     model.Xt = pyo.Var(model.setTidx, within=pyo.Reals, bounds=(LO_Xt, UP_Xt))
#     model.Fx = pyo.Var(model.setXidx, within=pyo.Reals, bounds=(FxLo, FxUp))

def getModelName(prefix, args):
    Nt = args.tLoUpND[2]
    Nx = args.xLoUpN[2]
    reg = args.regcoeff
    err = args.errdata
    prefixOffSpaces = prefix.replace(" ",'')
    if args.useEta:
        prefixOffSpaces = prefixOffSpaces + '_ETA'
    else:
        prefixOffSpaces = prefixOffSpaces + '_SQRT'
    return ('%s_ODE%d_Nt_%d_Nx_%d_err_%.3f_reg_%.3f')%(prefixOffSpaces, args.order, Nt, Nx, err, reg)

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
    nlFile = write_nl_only(model, workdir + '/' + getNLname(model, args),  symbolic_solver_labels=True)
    return nlFile

def readSol(model, nl_file):
    model_smap = get_smap_var(model)
    results = read_sol_smap_var(model, nl_file[:-len('.nl')], model_smap)
    model.solutions.load_from(results)
    return

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


import argparse
def makeParser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)#@!!ctlbr517
    parser.add_argument('-pr', '--prefix', default="OdePw", type=str, help='Prefix of problem name')
    parser.add_argument('-wd', '--workdir', default='tmp', help='working directory')
    parser.add_argument('-s', '--solver', default='ipopt', choices=['ipopt', 'scip'], help='solver to use')
    parser.add_argument('-t', '--tLoUpND', nargs='+', default=[1., 3., 4, 5], type=float, help='t: Lo Up N number of data')
    parser.add_argument('-x', '--xLoUpN', nargs='+', default=[5., 7., 5], type=float, help='x: Lo Up N')
    parser.add_argument('-Fx', '--FxLoUp', nargs='+', default=[0., 1.], type=float, help='Lo Up limits for Fx')
    parser.add_argument('-o', '--order', default=1, choices=[1,2,0], type=int, help='ODE order 1 or 2 (reduced form), 0 - SPLINE')
    parser.add_argument('-eps', '--epsilon', default=0.01, type=float, help='Epsilon to smooth pos()')
    parser.add_argument('-reg', '--regcoeff', default=.005, type=float, help='Regularization coefficient')
    parser.add_argument('-err', '--errdata', default=.1, type=float, help='Error of data')
    parser.add_argument('-eta', '--useEta', action='store_true', help='use Eta in discretization')
    return parser

if __name__ == "__main__":
    parser = makeParser()
    args = parser.parse_args()
    # vargs = vars(args)
    print('Arguments of the test')
    print('======================')
    for arg in vars(args):
        print(arg + ":", getattr(args, arg))
    print('======================')
    tLo, tUp, Nt, xLo, xUp, Nx, FxLo, FxUp = check_args(args)
    Ndata = int(args.tLoUpND[3])
    # Nt = int(args.tLoUpN[2])
    # tLo = args.tLoUpN[0]
    # tUp = args.tLoUpN[1]
    # Nx = int(args.xLoUpN[2])
    # xLo = args.xLoUpN[0]
    # xUp = args.xLoUpN[1]
    # FxLo = args.FxLoUp[0]
    # FxUp = args.FxLoUp[1]


    # Experimental data with error
    randomError = [random.uniform(-args.errdata/2., args.errdata/2.) for k in range(0,Ndata)]
    def generatorXtData(t: float, k: int):
        if args.order == 2:
            return math.sin(2*t) + math.cos(2*t) #*(1. + randomError[k])
        elif args.order == 1:
            return (-1./(1.+t))*(1. + randomError[k]) # 2*math.exp(t)
        else:
            raise Exception("UNKNOWN Generator XtData")
    # Fill txValuesData list
    txDataValues = []
    for k in range(Ndata):
        tk = tLo + k*(tUp - tLo)/Ndata
        txDataValues.append( (tk, generatorXtData(tk, k)) )
    # ============================

    theModel = pyo.ConcreteModel(getModelName(args.prefix, args))
    # theModel.name = getNLname(theModel, args)
    print("Model name: ", theModel.getname())

    init_scaled_XtFx(theModel, Nt, Nx, FxLo, FxUp)
    # initUniformMesh4XtFy(theModel)
    # print("CHECK: %f <= t <= %f"%(tLo, tUp))
    # print("CHECK: %f <= Xt <= %f"%(theModel.Xt[0].bounds[0], theModel.Xt[0].bounds[1]))
    # print("CHECK: %f <= y <= %f"%(xLo, xUp))
    # print("CHECK: %f <= Fx <= %f"%(theModel.Fx[0].bounds[0], theModel.Fx[0].bounds[1]))


    # quit()
    # if args.order == 0:
    #     addSpline_XtFy(theModel, eps=args.epsilon, useEta=args.useEta)
    if args.order == 1:
        add_scaled_ode1_XtFx(theModel, tLo, tUp, Nt, xLo, xUp, Nx, eps=args.epsilon, useEta=args.useEta)
    elif args.order == 2:
        add_scaled_ode2_XtFx(theModel, tLo, tUp, Nt, xLo, xUp, Nx, eps=args.epsilon, useEta=args.useEta)
    else:
        raise Exception("UNKNOWN Type of equation")

    add_scaled_SvFObject(theModel, tLo, tUp, Nt, xLo, xUp, Nx, txDataValues, args.regcoeff)
    # printData(theModel)

    theModel.pprint()

    with open(args.workdir + '/' + theModel.getname() + '.model.txt', 'w') as out_file:
        theModel.pprint(ostream = out_file)
        out_file.close()
    # quit()

    nl_file = makeNLfile(theModel, args)
    print(nl_file)
    subprocess.check_call("pwd")
    # quit()
    if args.solver == 'ipopt':
        subprocess.check_call(IPOPT_EXE + ' ' + nl_file + " -AMPL \"option_file_name=" + "ipopt.opt\"", shell=True)# +
    else:
        subprocess.check_call('scipampl' + ' ' + nl_file + " -AMPL scip4pw.set", shell=True)

    readSol(theModel, nl_file)
    (msdSol, regSol) = getMSD_REG(theModel)

    print('SvF obj.: ', pyo.value(theModel.svfObj))
    print('MSD = %f, REG = %f' % (msdSol, regSol))
    print('F(x): ', [pyo.value(theModel.Fx[j]) for j in theModel.setXidx])
    print('X(t): ', [pyo.value(theModel.Xt[t]) for t in theModel.setTidx])
    print('t: ', [pyo.value(theModel.meshT[i])  for i in theModel.setTidx])
    print('x: ', [pyo.value(theModel.meshX[j])  for j in theModel.setXidx])

    plotModelPW(theModel, nl_file[:-len('.nl')])
    quit()
    #
    # print("\n||||||||||||||||||||||||||||| Ode1_Sqrt |||||||||||||||||||||||||||||")
    # theModel = pyo.ConcreteModel("test Ode1_Sqrt")
    # print("Model name: ", theModel.getname())
    #
    # initXtFy(theModel, tLo, tUp, Nt, xLo, xUp, Nx)
    # initUniformMesh4XtFy(theModel)
    # addDiff1_XtFy(theModel, eps=0.01, useEta=False)
    # printData(theModel)
    # theModel.pprint()
    #
    # makeNlFile(theModel, workdir="./tmp")
