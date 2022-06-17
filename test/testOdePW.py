import os
import math
import random

import pyomo.environ as pyo

"""
Add ODE of the 1st and 2nd order to the SvF model when all unknown functions are discretized by a mesh-grid
dx(t)/dt = F(x(t))
d2x(t)/d2t = F(x(t),x'(t))
"""

def addOde_1_XtFy(model: pyo.ConcreteModel, eps: float = 0.01, useEta = True):
    """
    Add ODE of the form
    dx(t)/dt = F(x(t))
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
        return (m.Fy[j] - 2*m.Fy[j-1] + m.Fy[j-2])/dy

    def cntrX(m, k: int):
        return (m.Xt[k] + m.Xt[k-1])/2.

    model.setOdeK = pyo.RangeSet(1, Nx)
    if useEta:
        model.setEtaJ = pyo.RangeSet(1, Ny - 1)
        model.Eta = pyo.Var(model.setOdeK, model.setEtaJ, within=pyo.PositiveReals)

    def Eta_rule(m, k, j):
        # print("Eta_rule[%d,%d]"%(k,j))
        return (m.Eta[k, j]**2 == ((m.Xt[k] + m.Xt[k-1])/2. - m.meshY[j])**2 + eps**2)
        # return (m.Eta[k, j]**2 == (cntrX(m, k) - m.meshY[j])**2 + eps**2)
    if useEta:
        model.Eta_constr = pyo.Constraint(model.setOdeK, model.setEtaJ, rule=Eta_rule)

    def ODE1_Eta_rule(m, k):
        return ((m.Xt[k] - m.Xt[k - 1])/(dx) ==
                 m.Fy[0] - A(m, 1)*yLo + (1./2.)*(A(m, 1) + A(m, Ny))*cntrX(m, k) +
                (1. / 2.)*sum(D2F(m, j)*(m.Eta[k, j - 1] - m.meshY[j - 1]) for j in pyo.RangeSet(2, Ny))
                )
    def ODE1_Sqrt_rule(m, k):
        return ((m.Xt[k] - m.Xt[k-1])/(dx) ==
                 m.Fy[0] - A(m, 1)*yLo + (1./2.)*(A(m, 1) + A(m, Ny))*cntrX(m, k) +
                (1. / 2.)*sum(D2F(m, j)*(pyo.sqrt((cntrX(m, k) - m.meshY[j-1])**2 + eps**2) - m.meshY[j-1]) for j in pyo.RangeSet(2, Ny))
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

    def cntrX2(m, k: int):
        return (m.Xt[k])

    model.setOde2K = pyo.RangeSet(1, Nx-1)
    if useEta:
        model.setEtaJ = pyo.RangeSet(1, Ny - 1)
        model.Eta = pyo.Var(model.setOde2K, model.setEtaJ, within=pyo.PositiveReals)

    def Eta_rule(m, k, j):
        return (m.Eta[k, j]**2 == (cntrX2(m, k) - m.meshY[j])**2 + eps**2)
    if useEta:
        model.Eta_constr = pyo.Constraint(model.setOde2K, model.setEtaJ, rule=Eta_rule)

    def ODE2_Eta_rule(m, k):
        return ((m.Xt[k+1] - 2*m.Xt[k] - m.Xt[k-1])/(dx*dx) ==
                 m.Fy[0] - A(m, 1)*yLo + (1./2.)*(A(m, 1) + A(m, Ny))*m.Xt[k] +
                (1. / 2.)*sum(D2F(m, j)*(m.Eta[k, j - 1] - m.meshY[j-1]) for j in pyo.RangeSet(2, Ny))
                )
    def ODE2_Sqrt_rule(m, k):
        return ((m.Xt[k+1] - 2*m.Xt[k] - m.Xt[k-1])/(dx*dx) ==
                 m.Fy[0] - A(m, 1)*yLo + (1./2.)*(A(m, 1) + A(m, Ny))*m.Xt[k] +
                (1. / 2.)*sum(D2F(m, j)*(pyo.sqrt((cntrX2(m, k) - m.meshY[j-1])**2 + eps**2) - m.meshY[j-1]) for j in pyo.RangeSet(2, Ny))
                )
    if useEta:
        model.ODE2_Eta = pyo.Constraint(model.setOde2K, rule=ODE2_Eta_rule)
    else:
        model.ODE2_Sqrt = pyo.Constraint(model.setOde2K, rule=ODE2_Sqrt_rule)
