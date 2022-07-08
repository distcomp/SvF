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
from testPlotPW import plotSplineModelPW
import subprocess

IPOPT_EXE = '/opt/solvers/bin/ipopt'

"""
Add "Spline" to the SvF model when all unknown functions are discretized by a mesh-grid
y_lk ≈ F(y_lk), where F(y) is a PW-function
"""

def addSpline_SFx(model: pyo.ConcreteModel, eps: float = 0.01, useEta = True):
    """
    Add SPLINE of the form
    S(y) ≈ F(y)
    It is assumed that model has:
    parameters:
     Ns, Nx, ysLimits = {xsLo, xsUp}, yLmits = {xLo, xUp}
     dy=(xUp - xLo)/Nx
    variables ys[0:Ns], Fx[0:Nx]
    uniform meshgrids meshYs[0:Nt], meshX[0:Nx]
    """
    dy = model.dy.value
    Ns = len(model.setSidx) - 1
    Nx = len(model.Fx) - 1
    xLo = model.xLimits[0]

    def A(m, j: int):
        return (model.Fx[j] - model.Fx[j-1])/dy

    def D2F(m, j: int):
        # (A(j)-A(j-1))/dy
        return (model.Fx[j] - 2*model.Fx[j-1] + model.Fx[j-2])/dy

    # def cntrX(m, k: int):
    #     return (model.Xt[k])
        # return (model.Xt[k] + model.Xt[k-1])/2.

    # model.setOdeK = pyo.RangeSet(1, Nt)
    if useEta:
        # model.setEtaK = pyo.RangeSet(1, Nt - 1)
        model.setEtaJ = pyo.RangeSet(1, Nx - 1)
        model.Eta = pyo.Var(model.setSidx, model.setEtaJ, within=pyo.PositiveReals)

    def Eta_rule(m, k, j):
        return (m.Eta[k, j]**2 == (m.meshYs[k] - m.meshX[j])**2 + eps)
    if useEta:
        model.Eta_constr = pyo.Constraint(model.setSidx, model.setEtaJ, rule=Eta_rule)

    def Spline_Eta_rule(m, k):
        return (m.Sx[k] ==
                 m.Fx[0] - A(m, 1)*xLo + (1./2.)*(A(m, 1) + A(m, Nx))*m.meshYs[k] +
                (1. / 2.)*sum(D2F(m, j)*(m.Eta[k, j-1] - m.meshX[j-1]) for j in pyo.RangeSet(2, Nx))
                )
    def Spline_Sqrt_rule(m, k):
        return (m.Sx[k] ==
                 m.Fx[0] - A(m, 1)*xLo + (1./2.)*(A(m, 1) + A(m, Nx))*m.meshYs[k] +
                (1. / 2.)*sum(D2F(m, j)*(pyo.sqrt((m.meshYs[k] - m.meshX[j-1])**2 + eps) - m.meshX[j-1]) for j in pyo.RangeSet(2, Nx))
                )
    if useEta:
        model.Spline_Eta = pyo.Constraint(model.setSidx, rule=Spline_Eta_rule)
    else:
        model.Spline_Sqrt = pyo.Constraint(model.setSidx, rule=Spline_Sqrt_rule)


def addSvfObject(model: pyo.ConcreteModel, dataYsFunction):
    dy = model.dy.value
    Ns = len(model.setSidx) - 1
    Nx = len(model.Fx) - 1

    def SData_init(m, k):
        return dataYsFunction(m.meshYs[k], k)
    model.SData = pyo.Param(model.setSidx, initialize=SData_init)

    def svfObj_rule(m):
        return ((1./Ns)*sum( (m.Sx[k] - m.SData[k])**2 for k in m.setSidx) +
                m.regCoeff*(1/dy**3)*(1./Nx)*sum((m.Fx[j+1] - 2*m.Fx[j] + m.Fx[j-1])**2 for j in pyo.RangeSet(1, Nx - 1)))
    model.svfObj = pyo.Objective(rule=svfObj_rule, sense=pyo.minimize)

def getMSD_REG(model: pyo.ConcreteModel):
    Ns = len(model.Sx) - 1
    Nx = len(model.Fx) - 1
    MSD = sum( (pyo.value(model.Sx[k]) - pyo.value(model.SData[k]))**2 for k in pyo.RangeSet(0, Ns))/Ns
    REG = pyo.value(model.regCoeff)*(1/model.dy**3)*(1./Nx)*sum((pyo.value(model.Fx[j+1]) - 2*pyo.value(model.Fx[j]) + pyo.value(model.Fx[j-1]))**2 for j in pyo.RangeSet(1, Nx - 1))
    return (MSD, REG)

def initUniformMesh4YsFy(model: pyo.ConcreteModel):
    """
    It is assumed that model has:
    parameters:
     Nt, Nx, tLimits = {tLo, tUp}, yLmits = {xLo, xUp}
    variables Xt[0:Nt], Fx[0:Nx]
    """
    xsLo = model.ysLimits[0]
    xsUp = model.ysLimits[1]
    xLo = model.xLimits[0]
    xUp = model.xLimits[1]
    Ns = len(model.setSidx) - 1
    Nx = len(model.Fx) - 1

    dys = (xsUp - xsLo)/Ns
    model.dys = pyo.Param(initialize=dys)
    def meshYs_init(m, k):
        return xsLo + k*dys
    model.meshYs = pyo.Param(model.setSidx, initialize=meshYs_init)

    dy = (xUp - xLo) / Nx
    model.dy = pyo.Param(initialize=dy)
    def meshY_init(m, i):
        return xLo + i * dy
    model.meshX = pyo.Param(model.setXidx, initialize=meshY_init)

def initYsFy(model: pyo.ConcreteModel, xsLo: float, xsUp: float, Ns: int, funcDataYs, xLo: float, xUp: float, Nx: int, regCoeff):
    model.regCoeff = pyo.Param(initialize=regCoeff)

    model.setSidx = pyo.RangeSet(0, Ns)
    model.ysLimits = pyo.Param(pyo.RangeSet(0,1), initialize=(xsLo, xsUp), within=pyo.Reals)
    LO_S = min(funcDataYs(xsLo + (xsUp - xsLo)*k/Ns, k) for  k in model.setSidx)
    LO_S = LO_S - abs(LO_S)*.1
    UP_S = max(funcDataYs(xsLo + (xsUp - xsLo)*k/Ns, k) for  k in model.setSidx)
    UP_S = UP_S + abs(UP_S)*.1
    model.sLimits = pyo.Param(pyo.RangeSet(0,1), initialize=(LO_S, UP_S), within=pyo.Reals)

    # Create y-meshgrid
    model.setXidx = pyo.RangeSet(0, Nx)
    model.xLimits = pyo.Param(pyo.RangeSet(0,1), initialize=(xLo, xUp), within=pyo.Reals)

    model.Sx = pyo.Var(model.setSidx, within=pyo.Reals, bounds=(LO_S, UP_S))
    # !!! Set bounds for EACH Fx individually !!!???
    model.Fx = pyo.Var(model.setXidx, within=pyo.Reals, bounds=(LO_S, UP_S))

def getModelName(prefix, args):
    Ns = args.xSampleLoUpN[2]
    Nx = args.xLoUpN[2]
    reg = args.regcoeff
    err = args.errdata
    prefixOffSpaces = prefix.replace(" ",'')
    return ('%s_Ns_%d_Ny_%d_err_%.2f_reg_%.1f')%(prefixOffSpaces, Ns, Nx, err, reg)

def getNLname(model, args):
    return model.getname()
    # Nt = args.tLoUpN[2]
    # Nx = args.xLoUpN[2]
    # reg = args.regcoeff
    # err = args.errdata
    # fName = model.getname().replace(" ",'')
    # return ('%s_Nx_%d_Ny_%d_err_%.2f_reg_%.1f')%(fName, Nt, Nx, err, reg)

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

# def printData(model):
#     Nt = len(model.Xt) - 1
#     Nx = len(model.Fx) - 1
#     print("||||||||||| DATA |||||||||||||||")
#     print("Nt = ", Nt, " Nx = ", Nx)
#     print("meshT[t]: ", [pyo.value(model.meshT[t]) for t in model.setTidx])
#     print("meshX[y]: ", [pyo.value(model.meshX[y]) for y in model.setXidx])
#     print("||||||||||||||||||||||||||||||||")

import argparse
def makeParser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)#@!!ctlbr517
    parser.add_argument('-pr', '--prefix', default="Spline Pw eta", type=str, help='Prefix of problem name')
    parser.add_argument('-wd', '--workdir', default='tmp', help='working directory')
    parser.add_argument('-s', '--solver', default='ipopt', choices=['ipopt', 'scip'], help='solver to use')
    parser.add_argument('-xsMesh', '--xSampleLoUpN', nargs='+', default=[1., 3., 3], type=float, help='mesh of y Sample: Lo Up N')
    parser.add_argument('-err', '--errdata', default=.1, type=float, help='Error of data')
    parser.add_argument('-xMesh', '--xLoUpN', nargs='+', default=[0., 4., 4], type=float, help='y: Lo Up N')
    parser.add_argument('-eps', '--epsilon', default=0.01, type=float, help='Epsilon to smooth pos()')
    parser.add_argument('-reg', '--regcoeff', default=.005, type=float, help='Regularization coefficient')
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
    Ns = int(args.xSampleLoUpN[2])
    xsLo = args.xSampleLoUpN[0]
    xsUp = args.xSampleLoUpN[1]
    Nx = int(args.xLoUpN[2])
    xLo = args.xLoUpN[0]
    xUp = args.xLoUpN[1]

    if xsLo > xsUp:
        raise Exception(("xsLo=%f > xsUp=%f")%(xsLo, xsUp))
    if xLo > xUp:
        raise Exception(("xLo=%f > xUp=%f")%(xLo, xUp))

    if xsLo < xLo:
        raise Exception(("Spline seg. NOT IN PW seg.: xsLo=%f < xLo=%f")%(xsLo, xLo))
    if xsUp > xUp:
        raise Exception(("Spline seg. NOT IN PW seg.: xsUp=%f > xUp=%f")%(xsUp, xUp))

    # Experimental data with error
    randomError = [random.uniform(-args.errdata/2., args.errdata/2.) for k in range(0,Ns+1)]
    def dataXsAsOscill(sx: float, k: int):
        return math.sin(3*sx)*(1. + randomError[k])
    # ============================

    theModel = pyo.ConcreteModel(getModelName(args.prefix, args))
    # theModel.name = getNLname(theModel, args)
    print("Model name: ", theModel.getname())

    initYsFy(theModel, xsLo, xsUp, Ns, dataXsAsOscill, xLo, xUp, Nx, args.regcoeff)
    initUniformMesh4YsFy(theModel)
    print("CHECK: %f <= ys <= %f"%(xsLo, xsUp))
    print("CHECK: %f <= y <= %f"%(xLo, xUp))
    print("CHECK: %f <= S <= %f"%(theModel.sLimits[0], theModel.sLimits[1]))
    print("CHECK: %f <= Fx <= %f"%(theModel.Fx[0].bounds[0], theModel.Fx[0].bounds[1]))

    # theModel.pprint()
    # quit()
    addSpline_SFx(theModel, eps=args.epsilon, useEta=args.useEta)

    addSvfObject(theModel, dataXsAsOscill)
    # printData(theModel)
    theModel.pprint()
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
    print('S(x): ', [pyo.value(theModel.Sx[k]) for k in theModel.setSidx])
    print('ys: ', [pyo.value(theModel.meshYs[k])  for k in theModel.setSidx])
    print('y: ', [pyo.value(theModel.meshX[j])  for j in theModel.setXidx])
    # quit()
    plotSplineModelPW(theModel, nl_file[:-len('.nl')])
