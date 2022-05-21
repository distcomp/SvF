import pyomo.environ as pyo

"""
Add ODE of the 1st and 2nd order to the SvF model when all unknown functions are discretized by a mesh-grid
dx(t)/dt = F(x(t))
d2x(t)/d2t = F(x(t),x'(t))
"""

def addOde1(model: pyo.ConcreteModel, setT: list, yMin: float, yMax: float, Ny: int, eps: float, useEta = True):
    Nx = len(setT)-1
    model.setTidx = pyo.RangeSet(0,Nx)

    def meshT_init(m, k):
        return setT[k]
    model.meshT = pyo.Param(model.setTidx, initialize=meshT_init)

    # Create y-meshgrid
    model.setYidx = pyo.RangeSet(0,Ny)
    model.dy = pyo.Param(initialize=(yMax - yMin)/Ny)
    dy = (yMax - yMin)/Ny

    def meshY_init(m, i):
        return yMin + i*dy
    model.meshY = pyo.Param(model.setYidx, initialize=meshY_init)

    def printData():
        print("||||||||||| DATA |||||||||||||||")
        print("Nx = ", Nx, " Ny = ", Ny)
        print("meshT: ", [t for t in setT])
        print("meshY: ", [y for y in model.meshY])
        print("||||||||||||||||||||||||||||||||")
    printData()

    model.Fy = pyo.Var(model.setYidx, within=pyo.Reals)
    model.Xt = pyo.Var(model.setTidx, within=pyo.Reals)

    def A(m, j: int):
        return (m.Fy[j] - m.Fy[j-1])/dy

    def D2F(m, j: int):
        # (A(j)-A(j-1))/dy
        return (m.Fy[j] - 2*m.Fy[j-1] + m.Fy[j-2])/dy

    def cntrX(m, k: int):
        return (m.Xt[k] + m.Xt[k-1])/2.

    model.setOdeK = pyo.RangeSet(1, Nx)
    if useEta:
        # model.setEtaK = pyo.RangeSet(1, Nt - 1)
        model.setEtaJ = pyo.RangeSet(1, Ny - 1)
        model.Eta = pyo.Var(model.setOdeK, model.setEtaJ, within=pyo.PositiveReals)

    # def Eta_rule(m, k, j):
    #     return (m.Eta[k, j]**2 == (m.Xt[k] - m.meshY[j])**2 + eps**2)
    def Eta_rule(m, k, j):
        return (m.Eta[k, j]**2 == (cntrX(m, k) - m.meshY[j])**2 + eps**2)
    if useEta:
        model.Eta_constr = pyo.Constraint(model.setOdeK, model.setEtaJ, rule=Eta_rule)

    # def ODE1_Eta_rule(m, k):
    #     return ((m.Xt[k+1] - m.Xt[k])/(m.meshT[k+1] - m.meshT[k]) ==
    #              m.Fy[0] - A(m, 1)*yMin + (1./2.)*(A(m, 1) + A(m, Ny))*m.Xt[k] +
    #             (1. / 2.)*sum(D2F(m, j)*(m.Eta[k, j-1] - m.meshY[j-1]) for j in range(2, Ny))
    #             )
    def ODE1_Eta_rule(m, k):
        return ((m.Xt[k] - m.Xt[k-1])/(m.meshT[k] - m.meshT[k-1]) ==
                 m.Fy[0] - A(m, 1)*yMin + (1./2.)*(A(m, 1) + A(m, Ny))*cntrX(m, k) +
                (1. / 2.)*sum(D2F(m, j)*(m.Eta[k, j-1] - m.meshY[j-1]) for j in range(2, Ny))
                )

    # def ODE1_Sqrt_rule(m, k):
    #     return ((m.Xt[k+1] - m.Xt[k])/(m.meshT[k+1] - m.meshT[k]) ==
    #              m.Fy[0] - A(m, 1)*yMin + (1./2.)*(A(m, 1) + A(m, Ny))*m.Xt[k] +
    #             (1. / 2.)*sum(D2F(m, j)*(pyo.sqrt((m.Xt[k] - m.meshY[j])**2 + eps**2) - m.meshY[j-1]) for j in range(2, Ny))
    #             )
    def ODE1_Sqrt_rule(m, k):
        return ((m.Xt[k] - m.Xt[k-1])/(m.meshT[k] - m.meshT[k-1]) ==
                 m.Fy[0] - A(m, 1)*yMin + (1./2.)*(A(m, 1) + A(m, Ny))*cntrX(m, k) +
                (1. / 2.)*sum(D2F(m, j)*(pyo.sqrt((cntrX(m, k) - m.meshY[j])**2 + eps**2) - m.meshY[j-1]) for j in range(2, Ny))
                )

    if useEta:
        model.ODE1_Eta = pyo.Constraint(model.setOdeK, rule=ODE1_Eta_rule)
    else:
        model.ODE1_Sqrt = pyo.Constraint(model.setOdeK, rule=ODE1_Sqrt_rule)


if __name__ == "__main__":
    theModel = pyo.ConcreteModel("test Ode1_Eta")
    meshT = [i*2 for i in range(3)]
    yLo = 55.
    yUp = 67.
    Ny = 4
    addOde1(theModel, meshT, yLo, yUp, Ny, float(0.1))

    theModel.pprint()
    # print(theModel.meshT[1], theModel.meshT[len(meshT)])

    print("\n||||||||||||||||||||||||||||| Ode1_Sqrt |||||||||||||||||||||||||||||")
    theModel = pyo.ConcreteModel("test Ode1_Sqrt")
    addOde1(theModel, meshT, yLo, yUp, Ny, float(0.1), useEta=False)
    theModel.pprint()
