import pyomo.environ as pyo

"""
Add ODE of the 1st and 2nd order to the SvF model when all unknown functions are discretized by a mesh-grid
dx(t)/dt = F(x(t))
d2x(t)/d2t = F(x(t),x'(t))
"""

def addOde1(model: pyo.ConcreteModel, setT: list, yMin: float, yMax: float, Ny: int, eps: float):
    Nt = len(setT)
    print(Nt)
    model.setTidx = pyo.RangeSet(1,len(setT))

    def meshT_init(m, k):
        return setT[k-1]
    model.meshT = pyo.Param(model.setTidx, initialize=meshT_init)

    # Create y-meshgrid
    model.setYidx = pyo.RangeSet(0,Ny)
    model.dy = pyo.Param(initialize=(yMax - yMin)/Ny)
    dy = (yMax - yMin)/Ny
    def meshY_init(m, i):
        return yMin + i*dy
    model.meshY = pyo.Param(model.setYidx, initialize=meshY_init)

    model.Fy = pyo.Var(model.setYidx, within=pyo.Reals)
    model.Xt = pyo.Var(model.setTidx, within=pyo.Reals)

    def A(j: int):
        return (model.Fy[j] - model.Fy[j-1])/dy

    def D2F(j: int):
        # (A(j)-A(j-1))/dy
        return (model.Fy[j] - 2*model.Fy[j-1] + model.Fy[j-2])/dy

    model.setEtaI = pyo.RangeSet(1, Nt - 1)
    model.setEtaJ = pyo.RangeSet(1, Ny - 1)
    model.Eta = pyo.Var(model.setEtaI, model.setEtaJ, within=pyo.PositiveReals)

    def Eta_rule(m, i, j):
        return (m.Eta[i, j]**2 == (m.Xt[i] - m.meshY[j])**2 + eps**2)
    model.Eta_constr = pyo.Constraint(model.setEtaI, model.setEtaJ, rule=Eta_rule)

    def ODE1_Eta_rule(m, k):
        return ((m.Xt[k+1] - m.Xt[k])/(m.meshT[k+1] - m.meshT[k]) ==
                 m.Fy[0] - A(1)*yMin + (1./2.)*(A(1) + A(Ny))*m.Xt[k] +
                (1. / 2.)*sum(D2F(j)*(m.Eta[k,j-1] - m.meshY[j-1]) for j in range(2, Ny))
                )
    model.ODE1_Eta = pyo.Constraint(model.setEtaI, rule=ODE1_Eta_rule)


if __name__ == "__main__":
    theModel = pyo.ConcreteModel("test Ode1")
    meshT = [i*0.1 for i in range(3)]
    yLo = 55.
    yUp = 57.
    Ny = 6
    addOde1(theModel, meshT, yLo, yUp, Ny, 0.03)

    theModel.pprint()
    # print(theModel.meshT[1], theModel.meshT[len(meshT)])