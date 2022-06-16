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

def addSpline_SFy(model: pyo.ConcreteModel, eps: float = 0.01, useEta = True):
    """
    Add SPLINE of the form
    S(y) ≈ F(y)
    It is assumed that model has:
    parameters:
     Ns, Ny, ysLimits = {ysLo, ysUp}, yLmits = {yLo, yUp}
     dy=(yUp - yLo)/Ny
    variables ys[0:Ns], Fy[0:Ny]
    uniform meshgrids meshYs[0:Nx], meshY[0:Ny]
    """
    dy = model.dy.value
    Ns = len(model.setSidx) - 1
    Ny = len(model.Fy) - 1
    yLo = model.yLimits[0]

    def A(m, j: int):
        return (model.Fy[j] - model.Fy[j-1])/dy

    def D2F(m, j: int):
        # (A(j)-A(j-1))/dy
        return (model.Fy[j] - 2*model.Fy[j-1] + model.Fy[j-2])/dy

    # def cntrX(m, k: int):
    #     return (model.Xt[k])
        # return (model.Xt[k] + model.Xt[k-1])/2.

    # model.setOdeK = pyo.RangeSet(1, Nx)
    if useEta:
        # model.setEtaK = pyo.RangeSet(1, Nt - 1)
        model.setEtaJ = pyo.RangeSet(1, Ny - 1)
        model.Eta = pyo.Var(model.setSidx, model.setEtaJ, within=pyo.PositiveReals)

    def Eta_rule(m, k, j):
        return (m.Eta[k, j]**2 == (m.meshYs[k] - m.meshY[j])**2 + eps**2)
    if useEta:
        model.Eta_constr = pyo.Constraint(model.setSidx, model.setEtaJ, rule=Eta_rule)

    def Spline_Eta_rule(m, k):
        return (m.Sy[k] ==
                 m.Fy[0] - A(m, 1)*yLo + (1./2.)*(A(m, 1) + A(m, Ny))*m.meshYs[k] +
                (1. / 2.)*sum(D2F(m, j)*(m.Eta[k, j-1] - m.meshY[j-1]) for j in range(2, Ny))
                )
    def Spline_Sqrt_rule(m, k):
        return (m.Sy[k] ==
                 m.Fy[0] - A(m, 1)*yLo + (1./2.)*(A(m, 1) + A(m, Ny))*m.meshYs[k] +
                (1. / 2.)*sum(D2F(m, j)*(pyo.sqrt((m.meshYs[k] - m.meshY[j])**2 + eps**2) - m.meshY[j-1]) for j in range(2, Ny))
                )
    if useEta:
        model.Spline_Eta = pyo.Constraint(model.setSidx, rule=Spline_Eta_rule)
    else:
        model.Spline_Sqrt = pyo.Constraint(model.setSidx, rule=Spline_Sqrt_rule)


def addSvfObject(model: pyo.ConcreteModel, dataYsFunction):
    dy = model.dy.value
    Ns = len(model.setSidx) - 1
    Ny = len(model.Fy) - 1

    def SData_init(m, k):
        return dataYsFunction(m.meshYs[k], k)
    model.SData = pyo.Param(model.setSidx, initialize=SData_init)

    def svfObj_rule(m):
        return ((1./Ns)*sum( (m.Sy[k] - m.SData[k])**2 for k in m.setSidx) +
                m.regCoeff*(1/dy**3)*(1./Ny)*sum((m.Fy[j+1] - 2*m.Fy[j] + m.Fy[j-1])**2 for j in pyo.RangeSet(1, Ny - 1)))
    model.svfObj = pyo.Objective(rule=svfObj_rule, sense=pyo.minimize)

def getMSD_REG(model: pyo.ConcreteModel):
    Ns = len(model.Sy) - 1
    Ny = len(model.Fy) - 1
    MSD = sum( (pyo.value(model.Sy[k]) - pyo.value(model.SData[k]))**2 for k in pyo.RangeSet(0, Ns))/Ns
    REG = pyo.value(model.regCoeff)*(1/model.dy**3)*(1./Ny)*sum((pyo.value(model.Fy[j+1]) - 2*pyo.value(model.Fy[j]) + pyo.value(model.Fy[j-1]))**2 for j in pyo.RangeSet(1, Ny - 1))
    return (MSD, REG)

def initUniformMesh4YsFy(model: pyo.ConcreteModel):
    """
    It is assumed that model has:
    parameters:
     Nx, Ny, tLimits = {tLo, tUp}, yLmits = {yLo, yUp}
    variables Xt[0:Nt], Fy[0:Ny]
    """
    ysLo = model.ysLimits[0]
    ysUp = model.ysLimits[1]
    yLo = model.yLimits[0]
    yUp = model.yLimits[1]
    Ns = len(model.setSidx) - 1
    Ny = len(model.Fy) - 1

    dys = (ysUp - ysLo)/Ns
    model.dys = pyo.Param(initialize=dys)
    def meshYs_init(m, k):
        return ysLo + k*dys
    model.meshYs = pyo.Param(model.setSidx, initialize=meshYs_init)

    dy = (yUp - yLo) / Ny
    model.dy = pyo.Param(initialize=dy)
    def meshY_init(m, i):
        return yLo + i * dy
    model.meshY = pyo.Param(model.setYidx, initialize=meshY_init)

def initYsFy(model: pyo.ConcreteModel, ysLo: float, ysUp: float, Ns: int, funcDataYs, yLo: float, yUp: float, Ny: int, regCoeff):
    model.regCoeff = pyo.Param(initialize=regCoeff)

    model.setSidx = pyo.RangeSet(0, Ns)
    model.ysLimits = pyo.Param(pyo.RangeSet(0,1), initialize=(ysLo, ysUp), within=pyo.Reals)
    LO_S = min(funcDataYs(ysLo + (ysUp - ysLo)*k/Ns, k) for  k in model.setSidx)
    LO_S = LO_S - abs(LO_S)*.1
    UP_S = max(funcDataYs(ysLo + (ysUp - ysLo)*k/Ns, k) for  k in model.setSidx)
    UP_S = UP_S + abs(UP_S)*.1
    model.sLimits = pyo.Param(pyo.RangeSet(0,1), initialize=(LO_S, UP_S), within=pyo.Reals)

    # Create y-meshgrid
    model.setYidx = pyo.RangeSet(0, Ny)
    model.yLimits = pyo.Param(pyo.RangeSet(0,1), initialize=(yLo, yUp), within=pyo.Reals)

    model.Sy = pyo.Var(model.setSidx, within=pyo.Reals, bounds=(LO_S, UP_S))
    # !!! Set bounds for EACH Fy individually !!!???
    model.Fy = pyo.Var(model.setYidx, within=pyo.Reals, bounds=(LO_S, UP_S))

def getModelName(prefix, args):
    Ns = args.ySampleLoUpN[2]
    Ny = args.yLoUpN[2]
    reg = args.regcoeff
    err = args.errdata
    prefixOffSpaces = prefix.replace(" ",'')
    return ('%s_Nt_%d_Ny_%d_err_%.2f_reg_%.1f')%(prefixOffSpaces, Ns, Ny, err, reg)

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

# def printData(model):
#     Nx = len(model.Xt) - 1
#     Ny = len(model.Fy) - 1
#     print("||||||||||| DATA |||||||||||||||")
#     print("Nt = ", Nt, " Ny = ", Ny)
#     print("meshT[t]: ", [pyo.value(model.meshT[t]) for t in model.setTidx])
#     print("meshY[y]: ", [pyo.value(model.meshY[y]) for y in model.setYidx])
#     print("||||||||||||||||||||||||||||||||")

import argparse
def makeParser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)#@!!ctlbr517
    parser.add_argument('-pr', '--prefix', default="Spline Pw eta", type=str, help='Prefix of problem name')
    parser.add_argument('-wd', '--workdir', default='tmp', help='working directory')
    parser.add_argument('-s', '--solver', default='ipopt', choices=['ipopt', 'scip'], help='solver to use')
    parser.add_argument('-ysMesh', '--ySampleLoUpN', nargs='+', default=[1., 3., 3], type=float, help='mesh of y Sample: Lo Up N')
    parser.add_argument('-err', '--errdata', default=.1, type=float, help='Error of data')
    parser.add_argument('-yMesh', '--yLoUpN', nargs='+', default=[0., 4., 4], type=float, help='y: Lo Up N')
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
    Ns = int(args.ySampleLoUpN[2])
    ysLo = args.ySampleLoUpN[0]
    ysUp = args.ySampleLoUpN[1]
    Ny = int(args.yLoUpN[2])
    yLo = args.yLoUpN[0]
    yUp = args.yLoUpN[1]

    if ysLo > ysUp:
        raise Exception(("ysLo=%f > ysUp=%f")%(ysLo, ysUp))
    if yLo > yUp:
        raise Exception(("yLo=%f > yUp=%f")%(yLo, yUp))

    if ysLo < yLo:
        raise Exception(("Spline seg. NOT IN PW seg.: ysLo=%f < yLo=%f")%(ysLo, yLo))
    if ysUp > yUp:
        raise Exception(("Spline seg. NOT IN PW seg.: ysUp=%f > yUp=%f")%(ysUp, yUp))

    # Experimental data with error
    randomError = [random.uniform(-args.errdata/2., args.errdata/2.) for k in range(0,Ns+1)]
    def dataYsAsOscill(sy: float, k: int):
        return math.sin(3*sy)*(1. + randomError[k])
    # ============================

    theModel = pyo.ConcreteModel(getModelName(args.prefix, args))
    # theModel.name = getNLname(theModel, args)
    print("Model name: ", theModel.getname())

    initYsFy(theModel, ysLo, ysUp, Ns, dataYsAsOscill, yLo, yUp, Ny, args.regcoeff)
    initUniformMesh4YsFy(theModel)
    print("CHECK: %f <= ys <= %f"%(ysLo, ysUp))
    print("CHECK: %f <= y <= %f"%(yLo, yUp))
    print("CHECK: %f <= S <= %f"%(theModel.sLimits[0], theModel.sLimits[1]))
    print("CHECK: %f <= Fy <= %f"%(theModel.Fy[0].bounds[0], theModel.Fy[0].bounds[1]))

    # theModel.pprint()
    # quit()
    addSpline_SFy(theModel, eps=args.epsilon, useEta=args.useEta)

    addSvfObject(theModel, dataYsAsOscill)
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
    print('F(y): ', [pyo.value(theModel.Fy[j]) for j in theModel.setYidx])
    print('S(y): ', [pyo.value(theModel.Sy[k]) for k in theModel.setSidx])
    print('ys: ', [pyo.value(theModel.meshYs[k])  for k in theModel.setSidx])
    print('y: ', [pyo.value(theModel.meshY[j])  for j in theModel.setYidx])
    # quit()
    plotSplineModelPW(theModel, nl_file[:-len('.nl')])
