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
    def __init__(self, tLo, tUp, Nt: int, xLo, xUp, Nx: int, FxLo, FxUp):
        if FxLo > FxUp:
            raise Exception(("FxLo=%f > FxUp=%f") % (FxLo, FxUp))
        if xLo > xUp:
            raise Exception(("xLo=%f > xUp=%f") % (xLo, xUp))
        if tLo > tUp:
            raise Exception(("tLo=%f > tUp=%f") % (tLo, tUp))
        self.tLo, self.tUp, self.Nt, self.xLo, self.xUp, self.Nx = tLo, tUp, Nt, xLo, xUp, Nx
        self.FxLo, self.FxUp = FxLo, FxUp

    def t2st(self, t):
        return (t - self.tLo)*self.Nt/(self.tUp - self.tLo)
    def x2sx(self, x):
        return (x - self.xLo)*self.Nx/(self.xUp - self.xLo)
    def st2t(self, st):
        return self.tLo + st*(self.tUp - self.tLo)/self.Nt
    def sx2x(self, sx):
        return self.xLo + sx*(self.xUp - self.xLo)/self.Nx

def init_XtFx(model: pyo.ConcreteModel, xts: XTScaling): # Nt: int, Nx: int,  FxLo: float, FxUp: float):
    # Values of sx(st) for SCALED x, t  !!!
    model.Xt = pyo.Var(pyo.RangeSet(0, xts.Nt), within=pyo.Reals, bounds=(xts.xLo, xts.xUp))
    # Values of Fx(sx) for SCALED argument !!!
    model.Fx = pyo.Var(pyo.RangeSet(0, xts.Nx), within=pyo.Reals, bounds=(xts.FxLo, xts.FxUp))

def MSD_expr(m: pyo.ConcreteModel, xts: XTScaling, txValuesData: list):
    MSD_summands = []
    for tx in txValuesData:
        t, x = tx[0], tx[1]
        # st = (t - tLo) * Nt / (tUp - tLo)
        # sx = (x - xLo) * Nx / (xUp - xLo)
        MSD_summands.append((x - pw_xt_val(m, t, xts)) ** 2)
    return (pyo.quicksum(msd for msd in MSD_summands))

def REG_expr(m: pyo.ConcreteModel, xts: XTScaling, regCoeff: float):
    dx = (xts.xUp - xts.xLo)/xts.Nx
    return (regCoeff*( (1/dx)**3 )*pyo.quicksum( (m.Fx[j+1] - 2*m.Fx[j] + m.Fx[j-1])**2 for j in range(1, xts.Nx)) )

def add_SvFObject(model: pyo.ConcreteModel, xts: XTScaling, txValuesData: list, regCoeff: float):
    """
    Add MSD(X-xData) + reg*REG(Fx) object function
    :param model: the model
    :param txValuesData: list of (tVal, xVal) tuples of experimental data
    :param regCoeff:
    :return:
    """
    if regCoeff < 0:
        raise Exception(("regCoeff = %f < 0")%(regCoeff))
    model.svfObj = pyo.Objective(expr=MSD_expr(model, xts, txValuesData) +
                                      REG_expr(model, xts, regCoeff), sense=pyo.minimize)

def sA(m: pyo.ConcreteModel, j): return (m.Fx[j] - m.Fx[j-1])
def s_eta_sqrt(sx, j: int, eps):
    # dx = (xts.xUp - xts.xLo)/xts.Nx
    return  pyo.sqrt((sx - j)**2 + eps)

# 1/2*(FF(y(0))+FF(y(Ny))+A(1)*(y-y(0))+A(Ny)*(y-y(Ny))) + 1/2*(sum( A(j)*eta(j-1,y,e),j,2,Ny) - sum( A(j)*eta(j,y,e),j,1,Ny-1))
# pyo.quicksum(z for z in [x, - Nx, + 1])) +
def pwFx_sqrt(m: pyo.ConcreteModel, x, xts:XTScaling, eps):
    dx = (xts.xUp - xts.xLo)/xts.Nx
    sx = (x - xts.xLo)/dx
    return  ((m.Fx[0] + m.Fx[xts.Nx]) + (sA(m,1)*(sx - 0) + sA(m, xts.Nx)*(sx - xts.Nx)) +
              pyo.quicksum( (m.Fx[j] - 2*m.Fx[j-1] + m.Fx[j-2])*s_eta_sqrt(sx, j - 1, eps) for j in range(2, xts.Nx + 1) ))/2

#sum( (A(m, j) - A(m,j-1))*eta_sqrt(x, j-1, eps) for j in range(2, Nx+1) )
# sum(A(m, j)*eta_sqrt(x, j-1, eps) for j in range(2, Nx+1)) -
# sum(A(m, j)*eta_sqrt(x, j, eps)   for j in range(1, Nx))

def pwFx_eta(m: pyo.ConcreteModel, x, Nx, tk):
    """
    :param m: the model to add constraints
    :param x: expression for Fx arguments
    :param Nx: number of mesh INTERVALS = NUMBER OF POINTS -1
    :param tk: the index of LEFT SIDE ofs ODE equation
    :return: expression for RIGHT SIDE
    """
    return ( ((m.Fx[0] + m.Fx[Nx-1]) + (sA(m,1)*(x - 0) + sA(m,Nx)*(x - Nx + 1)) +
              sum(sA(m, j)*m.Eta[tk, j-1] for j in range(2, Nx+1)) -
              sum(sA(m, j)*m.Eta[tk, j]   for j in range(1, Nx)) )/2
            )


def pw_xt_val(m: pyo.ConcreteModel, t: float, xts: XTScaling):
    """
    Get value of piecewise X(t) for arbitrary (!) t \in [tLo, tUp]
    :param m: our model with Xt[k]
    :param t:  t
    :param xts: mesh data
    :return: pyo Expression !
    """
    if t < xts.tLo or t > xts.tUp:
        raise Exception("pw_xt_val: t (%f) IS NOT IN [%f, %f]" %(t, xts.tLo, xts.tUp))
    dt = (xts.tUp - xts.tLo)/xts.Nt
    k = int((t - xts.tLo)/dt)
    w = (t - xts.tLo)/dt - k
    return (m.Xt[k]*(1 - w) + m.Xt[min(k+1, xts.Nt)]*w)

# def pw_Fx_val(m: pyo.ConcreteModel, scaled_x: float, Nx):
#     """
#     Get value of piecewise Fx(x) for arbitrary scaled (!) x \in [0, Nx]
#     :param m: our model with Fx[j]
#     :param scaled_x: scaled x
#     :param Nx: number of segments over x
#     :return: pyo Expression !
#     """
#     if scaled_x < 0 or scaled_x > Nx:
#         raise Exception("pw_x_val: scaled_x (%f) IS NOT IN [0, %d]" %(scaled_x, Nx))
#     j = int(scaled_x)
#     return (m.Fx[j]*(j + 1 - scaled_x) + m.Xt[min(j+1, Nx)]*(scaled_x - j))

def add_ode1_XtFx(model: pyo.ConcreteModel, xts: XTScaling, eps: float = 0.01, useEta = True):
    """
    Add ODE of the form
    dx(t)/dt = Fpw(x(t))
    It is assumed that
    x \in [xLo, xUp] - is scaled mesh for x;
    t \in [tLo, tUp] -                for t;
    """
    # s1*(x[t] - x[t-1]) = F((x[t] + x[t-1])/2)
    # s1 = ((xUp - xLo)/Nx)*(Nt/(tUp - tLo))
    # s1_factor = ((xUp - xLo)/Nx)*(Nt/(tUp - tLo))

    dt = (xts.tUp - xts.tLo)/xts.Nt

    # def ode1_XtFx_eta_rule(m, k):
    #     # x = (m.Xt[k] + m.Xt[k-1])/2
    #     # pwFx_eta_val = (0.5*(m.Fx[0] + m.Fx[Nx]) + A(m,1)*(x - 0) + A(m,Nx)*(x - Nx) +
    #     #     0.5*sum(A(m, j)*m.Eta[k,j-1] for j in range(2, Nx+1)) -
    #     #     0.5*sum(A(m, j)*m.Eta[k,j]  for j in range(1, Nx))
    #     #     )
    #     return (s1_factor * (m.Xt[k] - m.Xt[k-1]) == pwFx_eta(m, (m.Xt[k] + m.Xt[k-1])/2, Nx, k) )

    def ode1_XtFx_sqrt_rule(m, k):
        return ((m.Xt[k] - m.Xt[k-1])/dt == pwFx_sqrt(m,(m.Xt[k] + m.Xt[k-1])/2, xts, eps ))

    model.setOde1K = pyo.RangeSet(1, xts.Nt)
    if useEta:
        raise Exception("add_ode1_XtFx: %s" % ("Eta NOT IMPLEMENTED Yet!"))
        # model.setEtaJ = pyo.RangeSet(1, Nx - 1)
        # model.Eta = pyo.Var(model.setOde1K, model.setEtaJ, within=pyo.PositiveReals)

    # def Eta1_rule(m, k, j):
    #     # print("Eta_rule[%d,%d]"%(k,j))
    #     return (m.Eta[k, j]**2 == ((m.Xt[k] + m.Xt[k-1])/2. - j)**2 + eps)
    #     # return (m.Eta[k, j]**2 == (cntrX(m, k) - m.meshX[j])**2 + eps)
    if useEta:
        raise Exception("add_ode1_XtFx: %s" % ("Eta NOT IMPLEMENTED Yet!"))
        # model.Eta1_constr = pyo.Constraint(model.setOde1K, model.setEtaJ, rule=Eta1_rule)

    if useEta:
        raise Exception("add_ode1_XtFx: %s" % ("Eta NOT IMPLEMENTED Yet!"))
        # model.Scaled_Ode1_Eta = pyo.Constraint(model.setOde1K, rule=scaled_ode1_XtFx_eta_rule)
    else:
        model.Ode1_Sqrt = pyo.Constraint(model.setOde1K, rule=ode1_XtFx_sqrt_rule)

def add_ode2_XtFx(model: pyo.ConcreteModel, xts: XTScaling, eps: float = 0.01, useEta = True):
    """
    Add ODE of the form
    d2x(t)/d2t = F(x(t)) for SCALED variables
    It is assumed that
    x \in [xLo, xUp] - is scaled mesh for x;
    t \in [tLo, tUp] -                for t;
    xxxxxxxxxxxxxxxxxxxxxxx s2*(x[t+1] - 2*x[t] + x[t-1]) = F( x[t] )
    xxxxxxxxxxxxxxxxxxxxxxx s2 = ((xUp - xLo)/Nx)*(Nt/(tUp - tLo))**2
    """
    # s2_factor = ((xUp - xLo)/Nx)*((Nt/(tUp - tLo))**2)

    # def scaled_ode2_XtFx_eta_rule(m, k):
    #     return (s2_factor * (m.Xt[k+1] - 2*m.Xt[k] - m.Xt[k-1]) == pwFx_eta(m, m.Xt[k], Nx, k) )
    dt = (xts.tUp - xts.tLo)/xts.Nt
    def ode2_XtFx_sqrt_rule(m, k):
        return (m.Xt[k+1] - 2*m.Xt[k] - m.Xt[k-1])/(dt**2) == pwFx_sqrt(m, m.Xt[k], xts, eps)

    model.setOde2K = pyo.RangeSet(1, xts.Nt - 1)
    if useEta:
        raise Exception("add_ode1_XtFx: %s" % ("Eta NOT IMPLEMENTED Yet!"))
        model.setEtaJ = pyo.RangeSet(1, Nx - 1)
        model.Eta = pyo.Var(model.setOde2K, model.setEtaJ, within=pyo.PositiveReals)

    def Eta2_rule(m, k, j):
        # print("Eta_rule[%d,%d]"%(k,j))
        return (m.Eta[k, j]**2 == ((m.Xt[k])/2. - j)**2 + eps)
        # return (m.Eta[k, j]**2 == (cntrX(m, k) - m.meshX[j])**2 + eps)
    if useEta:
        raise Exception("add_ode1_XtFx: %s" % ("Eta NOT IMPLEMENTED Yet!"))
        model.Eta2_constr = pyo.Constraint(model.setOde2K, model.setEtaJ, rule=Eta2_rule)

    if useEta:
        raise Exception("add_ode1_XtFx: %s" % ("Eta NOT IMPLEMENTED Yet!"))
        model.Scaled_Ode2_Eta = pyo.Constraint(model.setOde2K, rule=scaled_ode2_XtFx_eta_rule)
    else:
        model.Scaled_Ode2_Sqrt = pyo.Constraint(model.setOde2K, rule=ode2_XtFx_sqrt_rule)

