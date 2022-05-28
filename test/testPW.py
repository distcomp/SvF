import os

import pyomo.environ as pyo
# The following imports are from /asl_io/write module
from write import write_nl_only
from write import get_smap_var
from read import read_sol_smap_var

"""
Add ODE of the 1st and 2nd order to the SvF model when all unknown functions are discretized by a mesh-grid
dx(t)/dt = F(x(t))
d2x(t)/d2t = F(x(t),x'(t))
"""

# def XXXaddOde1(model: pyo.ConcreteModel, setT: list, yMin: float, yMax: float, Ny: int, eps: float, useEta = True):
#     Nx = len(setT)-1
#     model.setTidx = pyo.RangeSet(0,Nx)
#
#     def meshT_init(m, k):
#         return setT[k]
#     model.meshT = pyo.Param(model.setTidx, initialize=meshT_init)
#
#     # Create y-meshgrid
#     model.setYidx = pyo.RangeSet(0,Ny)
#     model.dy = pyo.Param(initialize=(yMax - yMin)/Ny)
#     dy = (yMax - yMin)/Ny
#
#     def meshY_init(m, i):
#         return yMin + i*dy
#     model.meshY = pyo.Param(model.setYidx, initialize=meshY_init)
#
#     def printData():
#         print("||||||||||| DATA |||||||||||||||")
#         print("Nx = ", Nx, " Ny = ", Ny)
#         print("meshT: ", [t for t in setT])
#         print("meshY: ", [y for y in model.meshY])
#         print("||||||||||||||||||||||||||||||||")
#     printData()
#
#     model.Fy = pyo.Var(model.setYidx, within=pyo.Reals)
#     model.Xt = pyo.Var(model.setTidx, within=pyo.Reals)
#
#     def A(m, j: int):
#         return (m.Fy[j] - m.Fy[j-1])/dy
#
#     def D2F(m, j: int):
#         # (A(j)-A(j-1))/dy
#         return (m.Fy[j] - 2*m.Fy[j-1] + m.Fy[j-2])/dy
#
#     def cntrX(m, k: int):
#         return (m.Xt[k] + m.Xt[k-1])/2.
#
#     model.setOdeK = pyo.RangeSet(1, Nx)
#     if useEta:
#         # model.setEtaK = pyo.RangeSet(1, Nt - 1)
#         model.setEtaJ = pyo.RangeSet(1, Ny - 1)
#         model.Eta = pyo.Var(model.setOdeK, model.setEtaJ, within=pyo.PositiveReals)
#
#     # def Eta_rule(m, k, j):
#     #     return (m.Eta[k, j]**2 == (m.Xt[k] - m.meshY[j])**2 + eps**2)
#     def Eta_rule(m, k, j):
#         return (m.Eta[k, j]**2 == (cntrX(m, k) - m.meshY[j])**2 + eps**2)
#     if useEta:
#         model.Eta_constr = pyo.Constraint(model.setOdeK, model.setEtaJ, rule=Eta_rule)
#
#     # def ODE1_Eta_rule(m, k):
#     #     return ((m.Xt[k+1] - m.Xt[k])/(m.meshT[k+1] - m.meshT[k]) ==
#     #              m.Fy[0] - A(m, 1)*yMin + (1./2.)*(A(m, 1) + A(m, Ny))*m.Xt[k] +
#     #             (1. / 2.)*sum(D2F(m, j)*(m.Eta[k, j-1] - m.meshY[j-1]) for j in range(2, Ny))
#     #             )
#     def ODE1_Eta_rule(m, k):
#         return ((m.Xt[k] - m.Xt[k-1])/(m.meshT[k] - m.meshT[k-1]) ==
#                  m.Fy[0] - A(m, 1)*yMin + (1./2.)*(A(m, 1) + A(m, Ny))*cntrX(m, k) +
#                 (1. / 2.)*sum(D2F(m, j)*(m.Eta[k, j-1] - m.meshY[j-1]) for j in range(2, Ny))
#                 )
#
#     # def ODE1_Sqrt_rule(m, k):
#     #     return ((m.Xt[k+1] - m.Xt[k])/(m.meshT[k+1] - m.meshT[k]) ==
#     #              m.Fy[0] - A(m, 1)*yMin + (1./2.)*(A(m, 1) + A(m, Ny))*m.Xt[k] +
#     #             (1. / 2.)*sum(D2F(m, j)*(pyo.sqrt((m.Xt[k] - m.meshY[j])**2 + eps**2) - m.meshY[j-1]) for j in range(2, Ny))
#     #             )
#     def ODE1_Sqrt_rule(m, k):
#         return ((m.Xt[k] - m.Xt[k-1])/(m.meshT[k] - m.meshT[k-1]) ==
#                  m.Fy[0] - A(m, 1)*yMin + (1./2.)*(A(m, 1) + A(m, Ny))*cntrX(m, k) +
#                 (1. / 2.)*sum(D2F(m, j)*(pyo.sqrt((cntrX(m, k) - m.meshY[j])**2 + eps**2) - m.meshY[j-1]) for j in range(2, Ny))
#                 )
#
#     if useEta:
#         model.ODE1_Eta = pyo.Constraint(model.setOdeK, rule=ODE1_Eta_rule)
#     else:
#         model.ODE1_Sqrt = pyo.Constraint(model.setOdeK, rule=ODE1_Sqrt_rule)

# def addOde1(model: pyo.ConcreteModel, meshT, varXt, Nx: int, meshY, varFy, yMin: float, yMax: float, Ny: int, eps: float, useEta = True):
#     dy = (yMax - yMin) / Ny
#     def A(m, j: int):
#         return (varFy[j] - varFy[j-1])/dy
#
#     def D2F(m, j: int):
#         # (A(j)-A(j-1))/dy
#         return (varFy[j] - 2*varFy[j-1] + varFy[j-2])/dy
#
#     def cntrX(m, k: int):
#         return (varXt[k] + varXt[k-1])/2.
#
#     model.setOdeK = pyo.RangeSet(1, Nx)
#     if useEta:
#         # model.setEtaK = pyo.RangeSet(1, Nt - 1)
#         model.setEtaJ = pyo.RangeSet(1, Ny - 1)
#         model.Eta = pyo.Var(model.setOdeK, model.setEtaJ, within=pyo.PositiveReals)
#
#     def Eta_rule(m, k, j):
#         return (m.Eta[k, j]**2 == (cntrX(m, k) - m.meshY[j])**2 + eps**2)
#     if useEta:
#         model.Eta_constr = pyo.Constraint(model.setOdeK, model.setEtaJ, rule=Eta_rule)
#
#     def ODE1_Eta_rule(m, k):
#         return ((varXt[k] - varXt[k-1])/(meshT[k] - meshT[k-1]) ==
#                  varFy[0] - A(m, 1)*yMin + (1./2.)*(A(m, 1) + A(m, Ny))*cntrX(m, k) +
#                 (1. / 2.)*sum(D2F(m, j)*(m.Eta[k, j-1] - meshY[j-1]) for j in range(2, Ny))
#                 )
#
#     def ODE1_Sqrt_rule(m, k):
#         return ((varXt[k] - varXt[k-1])/(meshT[k] - meshT[k-1]) ==
#                  varFy[0] - A(m, 1)*yMin + (1./2.)*(A(m, 1) + A(m, Ny))*cntrX(m, k) +
#                 (1. / 2.)*sum(D2F(m, j)*(pyo.sqrt((cntrX(m, k) - meshY[j])**2 + eps**2) - meshY[j-1]) for j in range(2, Ny))
#                 )
#
#     if useEta:
#         model.ODE1_Eta = pyo.Constraint(model.setOdeK, rule=ODE1_Eta_rule)
#     else:
#         model.ODE1_Sqrt = pyo.Constraint(model.setOdeK, rule=ODE1_Sqrt_rule)

def addDiff1_XtFy(model: pyo.ConcreteModel, eps: float = 0.01, useEta = True):
    """
    It is assumed that model has:
    parameters:
     Nx, Ny, xLimits = {xLo, xUp}, yLmits = {yLo, yUp}
     dx = (xUp - xLo)/Nx, dy=(yUp - yLo)/Ny
    variables Xt[0:Nx], Fy[0:Ny]
    uniform meshgrids meshT[0:Nx], meshY[0:Ny]
    """
    dx = model.dx.value
    dy = model.dy.value
    Nx = len(model.Xt) - 1
    Ny = len(model.Fy) - 1
    yLo = model.yLimits[0]

    def A(m, j: int):
        return (model.Fy[j] - model.Fy[j-1])/dy

    def D2F(m, j: int):
        # (A(j)-A(j-1))/dy
        return (model.Fy[j] - 2*model.Fy[j-1] + model.Fy[j-2])/dy

    def cntrX(m, k: int):
        return (model.Xt[k] + model.Xt[k-1])/2.

    model.setOdeK = pyo.RangeSet(1, Nx)
    if useEta:
        # model.setEtaK = pyo.RangeSet(1, Nt - 1)
        model.setEtaJ = pyo.RangeSet(1, Ny - 1)
        model.Eta = pyo.Var(model.setOdeK, model.setEtaJ, within=pyo.PositiveReals)

    def Eta_rule(m, k, j):
        return (m.Eta[k, j]**2 == (cntrX(m, k) - m.meshY[j])**2 + eps**2)
    if useEta:
        model.Eta_constr = pyo.Constraint(model.setOdeK, model.setEtaJ, rule=Eta_rule)

    def ODE1_Eta_rule(m, k):
        return ((m.Xt[k] - m.Xt[k-1])/(dx) ==
                 m.Fy[0] - A(m, 1)*yLo + (1./2.)*(A(m, 1) + A(m, Ny))*cntrX(m, k) +
                (1. / 2.)*sum(D2F(m, j)*(m.Eta[k, j-1] - m.meshY[j-1]) for j in range(2, Ny))
                )
    def ODE1_Sqrt_rule(m, k):
        return ((m.Xt[k] - m.Xt[k-1])/(dx) ==
                 m.Fy[0] - A(m, 1)*yLo + (1./2.)*(A(m, 1) + A(m, Ny))*cntrX(m, k) +
                (1. / 2.)*sum(D2F(m, j)*(pyo.sqrt((cntrX(m, k) - m.meshY[j])**2 + eps**2) - m.meshY[j-1]) for j in range(2, Ny))
                )
    if useEta:
        model.ODE1_Eta = pyo.Constraint(model.setOdeK, rule=ODE1_Eta_rule)
    else:
        model.ODE1_Sqrt = pyo.Constraint(model.setOdeK, rule=ODE1_Sqrt_rule)

def initUniformMesh4XtFy(model: pyo.ConcreteModel):
    """
    It is assumed that model has:
    parameters:
     Nx, Ny, xLimits = {xLo, xUp}, yLmits = {yLo, yUp}
    variables Xt[0:Nx], Fy[0:Ny]
    """
    xLo = model.xLimits[0]
    xUp = model.xLimits[1]
    yLo = model.yLimits[0]
    yUp = model.yLimits[1]
    Nx = len(model.Xt) - 1
    Ny = len(model.Fy) - 1

    dx = (xUp - xLo)/Nx
    model.dx = pyo.Param(initialize=dx)
    def meshT_init(m, k):
        return xLo + k*dx
    model.meshT = pyo.Param(model.setTidx, initialize=meshT_init)

    dy = (yUp - yLo) / Ny
    model.dy = pyo.Param(initialize=dy)
    def meshY_init(m, i):
        return yLo + i * dy
    model.meshY = pyo.Param(model.setYidx, initialize=meshY_init)

def initXtFy(model: pyo.ConcreteModel, xLo: float, xUp: float, Nx: int, yLo: float, yUp: float, Ny: int):
    # Nx = len(setT) - 1
    if xLo > xUp:
        raise Exception(("xLo=%f > xUp=%f")%(xLo, xUp))
    if yLo > yUp:
        raise Exception(("yLo=%f > yUp=%f")%(yLo, yUp))

    model.setTidx = pyo.RangeSet(0, Nx)
    model.xLimits = pyo.Param(pyo.RangeSet(0,1), initialize=(xLo, xUp), within=pyo.Reals)

    # Create y-meshgrid
    model.setYidx = pyo.RangeSet(0, Ny)
    model.yLimits = pyo.Param(pyo.RangeSet(0,1), initialize=(yLo, yUp), within=pyo.Reals)

    model.Fy = pyo.Var(model.setYidx, within=pyo.Reals)
    model.Xt = pyo.Var(model.setTidx, within=pyo.Reals)

def makeNlFile(model, **params):
    probName = model.getname().replace(" ",'')
    workdir = params["workdir"]
    try:
        os.mkdir(workdir)
    except OSError:
        pass
    nlName = write_nl_only(model, workdir + '/' + probName,  symbolic_solver_labels=True)
    return nlName

def printData(model):
    Nx = len(model.Xt) - 1
    Ny = len(model.Fy) - 1
    print("||||||||||| DATA |||||||||||||||")
    print("Nx = ", Nx, " Ny = ", Ny)
    print("meshT: ", [t for t in model.meshT])
    print("meshY: ", [y for y in model.meshY])
    print("||||||||||||||||||||||||||||||||")

import argparse
def makeParser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-pr', '--problem', default="test Ode Pw eta", type=str, help='problem name')
    parser.add_argument('-wd', '--workdir', default='./tmp', help='working directory')
    parser.add_argument('-s', '--solver', default='ipopt', choices=['ipopt', 'scip'], help='solver to use')
    parser.add_argument('-xMesh', '--xLoUpN', nargs='+', default=[1., 3., 2], type=float, help='x: Lo Up N')
    parser.add_argument('-yMesh', '--yLoUpN', nargs='+', default=[5., 7., 4], type=float, help='y: Lo Up N')
    parser.add_argument('-eps', '--epsilon', default=0.01, type=float, help='Epsilon to smooth pos()')
    parser.add_argument('-useEta', '--useEta', action='store_true', help='use Eat in discrtization')
    return parser

if __name__ == "__main__":
    # Nx = 2
    # xLo = 1
    # xUp = 3
    #
    # Ny = 4
    # yLo = 55.
    # yUp = 67.
    parser = makeParser()
    args = parser.parse_args()
    # vargs = vars(args)
    print('Arguments of the test')
    print('======================')
    for arg in vars(args):
        print(arg + ":", getattr(args, arg))
    print('======================')
    Nx = args.xLoUpN[2]
    xLo = args.xLoUpN[0]
    xUp = args.xLoUpN[1]
    Ny = args.yLoUpN[2]
    yLo = args.yLoUpN[0]
    yUp = args.yLoUpN[1]

    # quit()

    theModel = pyo.ConcreteModel(args.problem)
    print("Model name: ", theModel.getname())

    initXtFy(theModel, xLo, xUp, Nx, yLo, yUp, Ny)
    initUniformMesh4XtFy(theModel)
    addDiff1_XtFy(theModel, eps=args.epsilon, useEta=args.useEta)
    printData(theModel)
    theModel.pprint()

    makeNlFile(theModel, workdir=args.workdir)

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
