import os
import math
import random

import pyomo.environ as pyo

"""
Add "Spline" to the SvF model when all unknown functions are discretized by a mesh-grid
x(t) ≈ F(x(t))
"""

def addSpline_XtFy(model: pyo.ConcreteModel, eps: float = 0.01, useEta = True):
    """
    Add SPLINE of the form
    x(t) ≈ F(x(t))
    It is assumed that model has:
    parameters:
     Nx, Ny, xLimits = {xLo, xUp}, yLmits = {yLo, yUp}
     dy=(yUp - yLo)/Ny
    variables Xt[0:Nx], Fy[0:Ny]
    uniform meshgrids meshT[0:Nx], meshY[0:Ny]
    """
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
        return (model.Xt[k])
        # return (model.Xt[k] + model.Xt[k-1])/2.

    model.setOdeK = pyo.RangeSet(1, Nx)
    if useEta:
        # model.setEtaK = pyo.RangeSet(1, Nt - 1)
        model.setEtaJ = pyo.RangeSet(1, Ny - 1)
        model.Eta = pyo.Var(model.setOdeK, model.setEtaJ, within=pyo.PositiveReals)

    def Eta_rule(m, k, j):
        return (m.Eta[k, j]**2 == (cntrX(m, k) - m.meshY[j])**2 + eps**2)
    if useEta:
        model.Eta_constr = pyo.Constraint(model.setOdeK, model.setEtaJ, rule=Eta_rule)

    def Spline_Eta_rule(m, k):
        return (m.Xt[k] ==
                 m.Fy[0] - A(m, 1)*yLo + (1./2.)*(A(m, 1) + A(m, Ny))*cntrX(m, k) +
                (1. / 2.)*sum(D2F(m, j)*(m.Eta[k, j-1] - m.meshY[j-1]) for j in range(2, Ny))
                )
    def Spline_Sqrt_rule(m, k):
        return (m.Xt[k] ==
                 m.Fy[0] - A(m, 1)*yLo + (1./2.)*(A(m, 1) + A(m, Ny))*cntrX(m, k) +
                (1. / 2.)*sum(D2F(m, j)*(pyo.sqrt((cntrX(m, k) - m.meshY[j])**2 + eps**2) - m.meshY[j-1]) for j in range(2, Ny))
                )
    if useEta:
        model.Spline_Eta = pyo.Constraint(model.setOdeK, rule=Spline_Eta_rule)
    else:
        model.Spline_Sqrt = pyo.Constraint(model.setOdeK, rule=Spline_Sqrt_rule)
