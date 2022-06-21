import os
import math
import random

import pyomo.environ as pyo

"""
Add ODE of the 1st and 2nd order to the SvF model when all unknown functions are discretized by a mesh-grid
dx(t)/dt = F(x(t))
d2x(t)/d2t = F(x(t),x'(t))
"""



def pwfunction1(model: pyo.ConcreteModel, y, eps):
    return None

def addOde_1_XtFy(model: pyo.ConcreteModel, eps: float = 0.01, useEta = True):
    """
    Add ODE of the form
    dx(t)/dt = F(x(t))
    It is assumed that model has:
    parameters:
     Nt, Nx, tLimits = {tLo, tUp}, yLmits = {xLo, xUp}
     dx = (tUp - tLo)/Nt, dy=(xUp - xLo)/Nx
    variables Xt[0:Nt], Fx[0:Nx]
    uniform meshgrids meshT[0:Nt], meshX[0:Nx]
    """
    dt = model.dt.value
    dy = model.dy.value
    Nt = len(model.Xt) - 1
    Nx = len(model.Fx) - 1
    xLo = model.xLimits[0]

    def A(m, j: int):
        return (model.Fx[j] - model.Fx[j-1])/dy

    def D2F(m, j: int):
        # (A(j)-A(j-1))/dy
        return (m.Fx[j] - 2*m.Fx[j-1] + m.Fx[j-2])/dy

    def cntrX(m, k: int):
        return (m.Xt[k] + m.Xt[k-1])/2.

    model.setOdeK = pyo.RangeSet(1, Nt)
    if useEta:
        model.setEtaJ = pyo.RangeSet(1, Nx - 1)
        model.Eta = pyo.Var(model.setOdeK, model.setEtaJ, within=pyo.PositiveReals)

    def Eta_rule(m, k, j):
        # print("Eta_rule[%d,%d]"%(k,j))
        return (m.Eta[k, j]**2 == ((m.Xt[k] + m.Xt[k-1])/2. - m.meshX[j])**2 + eps)
        # return (m.Eta[k, j]**2 == (cntrX(m, k) - m.meshX[j])**2 + eps)
    if useEta:
        model.Eta_constr = pyo.Constraint(model.setOdeK, model.setEtaJ, rule=Eta_rule)

    def ODE1_Eta_rule(m, k):
        return ((m.Xt[k] - m.Xt[k - 1])/(dt) ==
                 m.Fx[0] - A(m, 1)*xLo + (1./2.)*(A(m, 1) + A(m, Nx))*cntrX(m, k) +
                (1. / 2.)*sum(D2F(m, j)*(m.Eta[k, j - 1] - m.meshX[j - 1]) for j in pyo.RangeSet(2, Nx))
                )
    def ODE1_Sqrt_rule(m, k):
        return ((m.Xt[k] - m.Xt[k-1])/(dt) ==
                 m.Fx[0] - A(m, 1)*xLo + (1./2.)*(A(m, 1) + A(m, Nx))*cntrX(m, k) +
                (1. / 2.)*sum(D2F(m, j)*(pyo.sqrt((cntrX(m, k) - m.meshX[j-1])**2 + eps) - m.meshX[j-1]) for j in pyo.RangeSet(2, Nx))
                )
    if useEta:
        model.ODE1_Eta = pyo.Constraint(model.setOdeK, rule=ODE1_Eta_rule)
    else:
        model.ODE1_Sqrt = pyo.Constraint(model.setOdeK, rule=ODE1_Sqrt_rule)

def addOde_2_XtFy(model: pyo.ConcreteModel, eps: float = 0.01, useEta = True):
    """
    Add ODE of the form
    d2x(t)/dt^2 = F(x(t))
    It is assumed that model has:
    parameters:
     Nt, Nx, tLimits = {tLo, tUp}, yLmits = {xLo, xUp}
     dt = (tUp - tLo)/Nt, dy=(xUp - xLo)/Nx
    variables Xt[0:Nt], Fx[0:Nx]
    uniform meshgrids meshT[0:Nt], meshX[0:Nx]
    """
    dt = model.dt.value
    dy = model.dy.value
    Nt = len(model.Xt) - 1
    Nx = len(model.Fx) - 1
    xLo = model.xLimits[0]

    def A(m, j: int):
        return (model.Fx[j] - model.Fx[j-1])/dy

    def D2F(m, j: int):
        # (A(j)-A(j-1))/dy
        return (model.Fx[j] - 2*model.Fx[j-1] + model.Fx[j-2])/dy

    def cntrX2(m, k: int):
        return (m.Xt[k])

    model.setOde2K = pyo.RangeSet(1, Nt-1)
    if useEta:
        model.setEtaJ = pyo.RangeSet(1, Nx - 1)
        model.Eta = pyo.Var(model.setOde2K, model.setEtaJ, within=pyo.PositiveReals)

    def Eta_rule(m, k, j):
        return (m.Eta[k, j]**2 == (cntrX2(m, k) - m.meshX[j])**2 + eps)
    if useEta:
        model.Eta_constr = pyo.Constraint(model.setOde2K, model.setEtaJ, rule=Eta_rule)

    def ODE2_Eta_rule(m, k):
        return ((m.Xt[k+1] - 2*m.Xt[k] - m.Xt[k-1])/(dt*dt) ==
                 m.Fx[0] - A(m, 1)*xLo + (1./2.)*(A(m, 1) + A(m, Nx))*cntrX2(m, k) +
                (1. / 2.)*sum(D2F(m, j)*(m.Eta[k, j - 1] - m.meshX[j-1]) for j in pyo.RangeSet(2, Nx))
                )
    def ODE2_Sqrt_rule(m, k):
        return ((m.Xt[k+1] - 2*m.Xt[k] - m.Xt[k-1])/(dt*dt) ==
                 m.Fx[0] - A(m, 1)*xLo + (1./2.)*(A(m, 1) + A(m, Nx))*cntrX2(m, k) +
                (1. / 2.)*sum(D2F(m, j)*(pyo.sqrt((cntrX2(m, k) - m.meshX[j-1])**2 + eps) - m.meshX[j-1]) for j in pyo.RangeSet(2, Nx))
                )
    if useEta:
        model.ODE2_Eta = pyo.Constraint(model.setOde2K, rule=ODE2_Eta_rule)
    else:
        model.ODE2_Sqrt = pyo.Constraint(model.setOde2K, rule=ODE2_Sqrt_rule)
