import os
import math
import random

import pyomo.environ as pyo

from testOdePW import addOde_1_XtFy, addOde_2_XtFy
# from testSplinePW import addSpline_XtFy

# The following imports are from /asl_io/write module
from write import write_nl_only, write_nl_smap
from write import get_smap_var
from read import read_sol_smap_var, read_sol_smap
from testPlotPW import plotModelPW
import subprocess

IPOPT_EXE = '/opt/solvers/bin/ipopt'

def addSvfObject(model: pyo.ConcreteModel, XtDataFunction):
    dx = model.dx.value
    dy = model.dy.value
    Nx = len(model.Xt) - 1
    Ny = len(model.Fy) - 1

    def XtData_init(m, k):
        return XtDataFunction(m.meshT[k], k)
    model.XtData = pyo.Param(model.setTidx, initialize=XtData_init)

    def svfObj_rule(m):
        return ((1./Nx)*sum( (m.Xt[k] - m.XtData[k])**2 for k in pyo.RangeSet(0, Nx)) +
                m.regCoeff*(1/dy**3)*(1./Ny)*sum((m.Fy[j+1] - 2*m.Fy[j] + m.Fy[j-1])**2 for j in pyo.RangeSet(1, Ny - 1)))
    model.svfObj = pyo.Objective(rule=svfObj_rule, sense=pyo.minimize)

def getMSD_REG(model: pyo.ConcreteModel):
    Nx = len(model.Xt) - 1
    Ny = len(model.Fy) - 1
    MSD = sum( (pyo.value(model.Xt[k]) - pyo.value(model.XtData[k]))**2 for k in pyo.RangeSet(0, Nx))/Nx
    REG = pyo.value(model.regCoeff)*(1/model.dy**3)*(1./Ny)*sum((pyo.value(model.Fy[j+1]) - 2*pyo.value(model.Fy[j]) + pyo.value(model.Fy[j-1]))**2 for j in pyo.RangeSet(1, Ny - 1))
    return (MSD, REG)

def initUniformMesh4XtFy(model: pyo.ConcreteModel):
    """
    It is assumed that model has:
    parameters:
     Nx, Ny, tLimits = {tLo, tUp}, yLmits = {yLo, yUp}
    variables Xt[0:Nt], Fy[0:Ny]
    """
    tLo = model.tLimits[0]
    tUp = model.tLimits[1]
    yLo = model.yLimits[0]
    yUp = model.yLimits[1]
    Nt = len(model.Xt) - 1
    Ny = len(model.Fy) - 1

    dt = (tUp - tLo)/Nt
    model.dx = pyo.Param(initialize=dt)
    def meshT_init(m, k):
        return tLo + k*dt
    model.meshT = pyo.Param(model.setTidx, initialize=meshT_init)

    dy = (yUp - yLo) / Ny
    model.dy = pyo.Param(initialize=dy)
    def meshY_init(m, i):
        return yLo + i * dy
    model.meshY = pyo.Param(model.setYidx, initialize=meshY_init)

def initXtFy(model: pyo.ConcreteModel, tLo: float, tUp: float, Nt: int, funcDataXt, yLo: float, yUp: float, Ny: int,
             FyLo: float, FyUp: float, regCoeff):
    # Nx = len(setT) - 1
    if tLo > tUp:
        raise Exception(("tLo=%f > tUp=%f")%(tLo, tUp))
    if yLo > yUp:
        raise Exception(("yLo=%f > yUp=%f")%(yLo, yUp))
    if FyLo > FyUp:
        raise Exception(("FyLo=%f > FyUp=%f")%(yLo, yUp))

    model.regCoeff = pyo.Param(initialize=regCoeff)

    model.setTidx = pyo.RangeSet(0, Nt)
    model.tLimits = pyo.Param(pyo.RangeSet(0,1), initialize=(tLo, tUp), within=pyo.Reals)
    LO_Xt = min(funcDataXt(tLo + (tUp - tLo)*k/Nt, k) for  k in model.setTidx)
    LO_Xt = LO_Xt - abs(LO_Xt)*.1
    UP_Xt = max(funcDataXt(tLo + (tUp - tLo)*k/Nt, k) for  k in model.setTidx)
    UP_Xt = UP_Xt + abs(UP_Xt)*.1
    model.xLimits = pyo.Param(pyo.RangeSet(0,1), initialize=(LO_Xt, UP_Xt), within=pyo.Reals)

    # Create y-meshgrid
    model.setYidx = pyo.RangeSet(0, Ny)
    model.yLimits = pyo.Param(pyo.RangeSet(0,1), initialize=(yLo, yUp), within=pyo.Reals)
    model.FyLimits = pyo.Param(pyo.RangeSet(0,1), initialize=(FyLo, FyUp), within=pyo.Reals)

    model.Xt = pyo.Var(model.setTidx, within=pyo.Reals, bounds=(LO_Xt, UP_Xt))
    model.Fy = pyo.Var(model.setYidx, within=pyo.Reals, bounds=(FyLo, FyUp))

def getModelName(prefix, args):
    Nt = args.tLoUpN[2]
    Ny = args.yLoUpN[2]
    reg = args.regcoeff
    err = args.errdata
    prefixOffSpaces = prefix.replace(" ",'')
    return ('%s_Nt_%d_Ny_%d_err_%.2f_reg_%.3f')%(prefixOffSpaces, Nt, Ny, err, reg)

def getNLname(model, args):
    return model.getname()
    # Nx = args.xLoUpN[2]
    # Ny = args.yLoUpN[2]
    # reg = args.regcoeff
    # err = args.errdata
    # fName = model.getname().replace(" ",'')
    # return ('%s_Nx_%d_Ny_%d_err_%.2f_reg_%.1f')%(fName, Nx, Ny, err, reg)

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
    Nx = len(model.Xt) - 1
    Ny = len(model.Fy) - 1
    print("||||||||||| DATA |||||||||||||||")
    print("Nt = ", Nt, " Ny = ", Ny)
    print("meshT[t]: ", [pyo.value(model.meshT[t]) for t in model.setTidx])
    print("meshY[y]: ", [pyo.value(model.meshY[y]) for y in model.setYidx])
    print("||||||||||||||||||||||||||||||||")

import argparse
def makeParser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)#@!!ctlbr517
    parser.add_argument('-pr', '--prefix', default="test Ode Pw eta", type=str, help='Prefix of problem name')
    parser.add_argument('-wd', '--workdir', default='tmp', help='working directory')
    parser.add_argument('-s', '--solver', default='ipopt', choices=['ipopt', 'scip'], help='solver to use')
    parser.add_argument('-tMesh', '--tLoUpN', nargs='+', default=[1., 3., 2], type=float, help='t: Lo Up N')
    parser.add_argument('-yMesh', '--yLoUpN', nargs='+', default=[5., 7., 4], type=float, help='y: Lo Up N')
    parser.add_argument('-FyLoUp', '--FyLoUp', nargs='+', default=[0., 1.], type=float, help='Lo Up limits for Fy')
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
    Nt = int(args.tLoUpN[2])
    tLo = args.tLoUpN[0]
    tUp = args.tLoUpN[1]
    Ny = int(args.yLoUpN[2])
    yLo = args.yLoUpN[0]
    yUp = args.yLoUpN[1]
    FyLo = args.FyLoUp[0]
    FyUp = args.FyLoUp[1]


    # Experimental data with error
    randomError = [random.uniform(-args.errdata/2., args.errdata/2.) for k in range(0,Nt+1)]
    def generatorXtData(t: float, k: int):
        if args.order == 2:
            return math.sin(2*t) + math.cos(2*t) #*(1. + randomError[k])
        elif args.order == 1:
            return (-1./(1.+t))*(1. + randomError[k]) # 2*math.exp(t)
        else:
            raise Exception("UNKNOWN Generator XtData")
    # ============================

    theModel = pyo.ConcreteModel(getModelName(args.prefix, args))
    # theModel.name = getNLname(theModel, args)
    print("Model name: ", theModel.getname())

    initXtFy(theModel, tLo, tUp, Nt, generatorXtData, yLo, yUp, Ny, FyLo, FyUp, args.regcoeff)
    initUniformMesh4XtFy(theModel)
    print("CHECK: %f <= t <= %f"%(tLo, tUp))
    print("CHECK: %f <= Xt <= %f"%(theModel.Xt[0].bounds[0], theModel.Xt[0].bounds[1]))
    print("CHECK: %f <= y <= %f"%(yLo, yUp))
    print("CHECK: %f <= Fy <= %f"%(theModel.Fy[0].bounds[0], theModel.Fy[0].bounds[1]))


    # quit()
    # if args.order == 0:
    #     addSpline_XtFy(theModel, eps=args.epsilon, useEta=args.useEta)
    if args.order == 1:
        addOde_1_XtFy(theModel, eps=args.epsilon, useEta=args.useEta)
    elif args.order == 2:
        addOde_2_XtFy(theModel, eps=args.epsilon, useEta=args.useEta)
    else:
        raise Exception("UNKNOWN Type of equation")

    addSvfObject(theModel, generatorXtData)
    printData(theModel)

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
    print('F(y): ', [pyo.value(theModel.Fy[j]) for j in theModel.setYidx])
    print('X(t): ', [pyo.value(theModel.Xt[t]) for t in theModel.setTidx])
    print('t: ', [pyo.value(theModel.meshT[i])  for i in theModel.setTidx])
    print('y: ', [pyo.value(theModel.meshY[j])  for j in theModel.setYidx])

    plotModelPW(theModel, nl_file[:-len('.nl')])
    quit()
    #
    # print("\n||||||||||||||||||||||||||||| Ode1_Sqrt |||||||||||||||||||||||||||||")
    # theModel = pyo.ConcreteModel("test Ode1_Sqrt")
    # print("Model name: ", theModel.getname())
    #
    # initXtFy(theModel, xLo, xUp, Nx, yLo, yUp, Ny)
    # initUniformMesh4XtFy(theModel)
    # addDiff1_XtFy(theModel, eps=0.01, useEta=False)
    # printData(theModel)
    # theModel.pprint()
    #
    # makeNlFile(theModel, workdir="./tmp")
