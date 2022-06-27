import os
import math
import random

import pyomo.environ as pyo

"""
Add ODE of the 1st and 2nd order to the SvF model when all unknown functions are discretized by a mesh-grid
dx(t)/dt = F(x(t))
d2x(t)/d2t = F(x(t),x'(t))
"""

class XTScaling:
    def __init__(self, tLo, tUp, Nt, xLo, xUp, Nx):
        self.tLo, self.tUp, self.Nt, self.xLo, self.xUp, self.Nx = tLo, tUp, Nt, xLo, xUp, Nx
    def t2st(self, t):
        return (t - self.tLo)*self.Nt/(self.tUp - self.tLo)
    def x2sx(self, x):
        return (x - self.xLo)*self.Nx/(self.xUp - self.xLo)
    def st2t(self, st):
        return self.tLo + st*(self.tUp - self.tLo)/self.Nt
    def sx2x(self, sx):
        return self.xLo + sx*(self.xUp - self.xLo)/self.Nx

def init_scaled_XtFx(model: pyo.ConcreteModel, Nt: int, Nx: int,  FxLo: float, FxUp: float):
    if FxLo > FxUp:
        raise Exception(("FxLo=%f > FxUp=%f")%(FxLo, FxUp))
    # Values of sx(st) for SCALED x, t  !!!
    model.Xt = pyo.Var(pyo.RangeSet(0,Nt), within=pyo.Reals, bounds=(0, Nx))
    # Values of Fx(sx) for SCALED argument !!!
    model.Fx = pyo.Var(pyo.RangeSet(0,Nx), within=pyo.Reals, bounds=(FxLo, FxUp))

def scaled_MSD_expr(m: pyo.ConcreteModel, tLo, tUp, Nt, xLo, xUp, Nx, txValuesData: list):
    MSD_summands = []
    for tx in txValuesData:
        t, x = tx[0], tx[1]
        st = (t - tLo) * Nt / (tUp - tLo)
        sx = (x - xLo) * Nx / (xUp - xLo)
        MSD_summands.append((sx - pw_xt_val(m, st, Nt)) ** 2)
    return (pyo.quicksum(msd for msd in MSD_summands))

def scaled_REG_expr(m: pyo.ConcreteModel, xLo, xUp, Nx, regCoeff: float):
    return (regCoeff*( (Nx/(xUp - xLo))**3 )*pyo.quicksum( (m.Fx[j+1] - 2*m.Fx[j] + m.Fx[j-1])**2 for j in range(1, Nx)) )

def add_scaled_SvFObject(model: pyo.ConcreteModel, tLo, tUp, Nt, xLo, xUp, Nx, txValuesData: list, regCoeff: float):
    """
    Add MSD(X-xData) + reg*REG(Fx) object function
    :param model: the model
    :param txValuesData: list of (tVal, xVal) tuples of experimental data
    :param regCoeff:
    :return:
    """
    if regCoeff < 0:
        raise Exception(("regCoeff = %f < 0")%(regCoeff))
    model.svfObj = pyo.Objective(expr=scaled_MSD_expr(model, tLo, tUp, Nt, xLo, xUp, Nx, txValuesData) +
                                      scaled_REG_expr(model, xLo, xUp, Nx, regCoeff), sense=pyo.minimize)

def A(m: pyo.ConcreteModel, j): return (m.Fx[j] - m.Fx[j-1])
def eta_sqrt(x, j: int, eps): return pyo.sqrt((x - j)**2 + eps)

# 1/2*(FF(y(0))+FF(y(Ny))+A(1)*(y-y(0))+A(Ny)*(y-y(Ny))) + 1/2*(sum( A(j)*eta(j-1,y,e),j,2,Ny) - sum( A(j)*eta(j,y,e),j,1,Ny-1))
def pwFx_sqrt(m: pyo.ConcreteModel, x, Nx, eps):
    return (0.5*(m.Fx[0] + m.Fx[Nx]) + A(m,1)*(x - 0) + A(m,Nx)*(x - Nx) +
            0.5*sum(A(m, j)*eta_sqrt(x, j-1, eps) for j in range(2, Nx+1)) -
            0.5*sum(A(m, j)*eta_sqrt(x, j, eps)   for j in range(1, Nx))
            )

def pwFx_eta(m: pyo.ConcreteModel, x, Nx):
    return (0.5*(m.Fx[0] + m.Fx[Nx]) + A(m,1)*(x - 0) + A(m,Nx)*(x - Nx) +
            0.5*sum(A(m, j)*m.Eta[j-1] for j in range(2, Nx+1)) -
            0.5*sum(A(m, j)*m.Eta[j]  for j in range(1, Nx))
            )

def pw_xt_val(m: pyo.ConcreteModel, scaled_t: float, Nt):
    """
    Get value of piecewise X(t) for arbitrary scaled (!) t \in [0, Nt]
    :param m: our model with Xt[k]
    :param scaled_t: scaled t
    :param Nt: number of segments over t
    :return: pyo Expression !
    """
    if scaled_t < 0 or scaled_t > Nt:
        raise Exception("pw_xt_val: scaled_t (%f) IS NOT IN [0, %d]" %(scaled_t, Nt))
    k = int(scaled_t)
    return (m.Xt[k]*(k + 1 - scaled_t) + m.Xt[min(k+1, Nt)]*(scaled_t - k))

def pw_Fx_val(m: pyo.ConcreteModel, scaled_x: float, Nx):
    """
    Get value of piecewise Fx(x) for arbitrary scaled (!) x \in [0, Nx]
    :param m: our model with Fx[j]
    :param scaled_x: scaled x
    :param Nx: number of segments over x
    :return: pyo Expression !
    """
    if scaled_x < 0 or scaled_x > Nx:
        raise Exception("pw_x_val: scaled_x (%f) IS NOT IN [0, %d]" %(scaled_x, Nx))
    j = int(scaled_x)
    return (m.Fx[j]*(j + 1 - scaled_x) + m.Xt[min(j+1, Nx)]*(scaled_x - j))

def add_scaled_ode1_XtFx(model: pyo.ConcreteModel, tLo, tUp, Nt, xLo, xUp, Nx, eps: float = 0.01, useEta = True):
    """
    Add ODE of the form
    dx(t)/dt = F(x(t)) for SCALED variables
    It is assumed that
    x \in [0, Nx] - is scaled mesh for x;
    t \in [0, Nt] -                for t;
    s1*(x[t] - x[t-1]) = F((x[t] + x[t-1])/2)
    s1 = ((xUp - xLo)/Nx)*(Nt/(tUp - tLo))
    """
    s1_factor = ((xUp - xLo)/Nx)*(Nt/(tUp - tLo))

    def scaled_ode1_XtFx_eta_rule(m, k):
        return (s1_factor * (m.Xt[k] - m.Xt[k-1]) == pwFx_eta(m, (m.Xt[k] + m.Xt[k-1])/2), Nx)
    def scaled_ode1_XtFx_sqrt_rule(m, k):
        return (s1_factor * (m.Xt[k] - m.Xt[k-1]) == pwFx_sqrt(m, (m.Xt[k] + m.Xt[k-1])/2, Nx, eps ))

    model.setOde1K = pyo.RangeSet(1, Nt)
    if useEta:
        model.setEtaJ = pyo.RangeSet(1, Nx - 1)
        model.Eta = pyo.Var(model.setOde1K, model.setEtaJ, within=pyo.PositiveReals)

    def Eta1_rule(m, k, j):
        # print("Eta_rule[%d,%d]"%(k,j))
        return (m.Eta[k, j]**2 == ((m.Xt[k] + m.Xt[k-1])/2. - j)**2 + eps)
        # return (m.Eta[k, j]**2 == (cntrX(m, k) - m.meshX[j])**2 + eps)
    if useEta:
        model.Eta1_constr = pyo.Constraint(model.setOde1K, model.setEtaJ, rule=Eta1_rule)

    if useEta:
        model.Scaled_Ode1_Eta = pyo.Constraint(model.setOde1K, rule=scaled_ode1_XtFx_eta_rule)
    else:
        model.Scaled_Ode1_Sqrt = pyo.Constraint(model.setOde1K, rule=scaled_ode1_XtFx_sqrt_rule)

def add_scaled_ode2_XtFx(model: pyo.ConcreteModel, tLo, tUp, Nt, xLo, xUp, Nx, eps: float = 0.01, useEta = True):
    """
    Add ODE of the form
    d2x(t)/d2t = F(x(t)) for SCALED variables
    It is assumed that
    x \in [0, Nx] - is scaled mesh for x;
    t \in [0, Nt] -                for t;
    s2*(x[t+1] - 2*x[t] + x[t-1]) = F( x[t] )
    s2 = ((xUp - xLo)/Nx)*(Nt/(tUp - tLo))**2
    """
    s2_factor = ((xUp - xLo)/Nx)*((Nt/(tUp - tLo))**2)

    def scaled_ode2_XtFx_eta_rule(m, k):
        return (s2_factor * (m.Xt[k+1] - 2*m.Xt[k] - m.Xt[k-1]) == pwFx_eta(m, m.Xt[k]) )
    def scaled_ode2_XtFx_sqrt_rule(m, k):
        return (s2_factor * (m.Xt[k+1] - 2*m.Xt[k] - m.Xt[k-1]) == pwFx_sqrt(m, m.Xt[k]),eps )

    model.setOde2K = pyo.RangeSet(1, Nt-1)
    if useEta:
        model.setEtaJ = pyo.RangeSet(1, Nx - 1)
        model.Eta = pyo.Var(model.setOde2K, model.setEtaJ, within=pyo.PositiveReals)

    def Eta2_rule(m, k, j):
        # print("Eta_rule[%d,%d]"%(k,j))
        return (m.Eta[k, j]**2 == ((m.Xt[k])/2. - j)**2 + eps)
        # return (m.Eta[k, j]**2 == (cntrX(m, k) - m.meshX[j])**2 + eps)
    if useEta:
        model.Eta2_constr = pyo.Constraint(model.setOde2K, model.setEtaJ, rule=Eta2_rule)

    if useEta:
        model.Scaled_Ode2_Eta = pyo.Constraint(model.setOde2K, rule=scaled_ode2_XtFx_eta_rule)
    else:
        model.Scaled_Ode2_Sqrt = pyo.Constraint(model.setOde2K, rule=scaled_ode2_XtFx_sqrt_rule)

#
# def addOde_2_XtFy(model: pyo.ConcreteModel, eps: float = 0.01, useEta = True):
#     """
#     Add ODE of the form
#     d2x(t)/dt^2 = F(x(t))
#     It is assumed that model has:
#     parameters:
#      Nt, Nx, tLimits = {tLo, tUp}, yLmits = {xLo, xUp}
#      dt = (tUp - tLo)/Nt, dy=(xUp - xLo)/Nx
#     variables Xt[0:Nt], Fx[0:Nx]
#     uniform meshgrids meshT[0:Nt], meshX[0:Nx]
#     """
#     dt = model.dt.value
#     dy = model.dy.value
#     Nt = len(model.Xt) - 1
#     Nx = len(model.Fx) - 1
#     xLo = model.xLimits[0]
#
#     def A(m, j: int):
#         return (model.Fx[j] - model.Fx[j-1])/dy
#
#     def D2F(m, j: int):
#         # (A(j)-A(j-1))/dy
#         return (model.Fx[j] - 2*model.Fx[j-1] + model.Fx[j-2])/dy
#
#     def cntrX2(m, k: int):
#         return (m.Xt[k])
#
#     model.setOde2K = pyo.RangeSet(1, Nt-1)
#     if useEta:
#         model.setEtaJ = pyo.RangeSet(1, Nx - 1)
#         model.Eta = pyo.Var(model.setOde2K, model.setEtaJ, within=pyo.PositiveReals)
#
#     def Eta_rule(m, k, j):
#         return (m.Eta[k, j]**2 == (cntrX2(m, k) - m.meshX[j])**2 + eps)
#     if useEta:
#         model.Eta_constr = pyo.Constraint(model.setOde2K, model.setEtaJ, rule=Eta_rule)
#
#     def ODE2_Eta_rule(m, k):
#         return ((m.Xt[k+1] - 2*m.Xt[k] - m.Xt[k-1])/(dt*dt) ==
#                  m.Fx[0] - A(m, 1)*xLo + (1./2.)*(A(m, 1) + A(m, Nx))*cntrX2(m, k) +
#                 (1. / 2.)*sum(D2F(m, j)*(m.Eta[k, j - 1] - m.meshX[j-1]) for j in pyo.RangeSet(2, Nx))
#                 )
#     def ODE2_Sqrt_rule(m, k):
#         return ((m.Xt[k+1] - 2*m.Xt[k] - m.Xt[k-1])/(dt*dt) ==
#                  m.Fx[0] - A(m, 1)*xLo + (1./2.)*(A(m, 1) + A(m, Nx))*cntrX2(m, k) +
#                 (1. / 2.)*sum(D2F(m, j)*(pyo.sqrt((cntrX2(m, k) - m.meshX[j-1])**2 + eps) - m.meshX[j-1]) for j in pyo.RangeSet(2, Nx))
#                 )
#     if useEta:
#         model.ODE2_Eta = pyo.Constraint(model.setOde2K, rule=ODE2_Eta_rule)
#     else:
#         model.ODE2_Sqrt = pyo.Constraint(model.setOde2K, rule=ODE2_Sqrt_rule)
