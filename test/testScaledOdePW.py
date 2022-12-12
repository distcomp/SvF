import os
import math
import random

import pyomo.environ as pyo

from piecewise_yvar import Piecewise


"""
Add ODE of the 1st and 2nd order to the SvF model when all unknown functions are discretized by a mesh-grid
dx(t)/dt = F(x(t))
d2x(t)/d2t = F(x(t),x'(t))
"""

class XTScaling:
    def __init__(self, tLo, tUp, Nt: int, xLo, xUp, Nx: int, FxLo, FxUp, errData):
        if FxLo > FxUp:
            raise Exception(("FxLo=%f > FxUp=%f") % (FxLo, FxUp))
        if xLo > xUp:
            raise Exception(("xLo=%f > xUp=%f") % (xLo, xUp))
        if tLo > tUp:
            raise Exception(("tLo=%f > tUp=%f") % (tLo, tUp))
        self.tLo, self.tUp, self.Nt, self.xLo, self.xUp, self.Nx = tLo, tUp, Nt, xLo, xUp, Nx
        self.dt, self.dx = (tUp - tLo)/(Nt), (xUp - xLo)/(Nx)
        self.FxLo, self.FxUp = FxLo, FxUp
        self.errData = errData


    def t2st(self, t):
        return (t - self.tLo)/(self.dt)
    def x2sx(self, x):
        return (x - self.xLo)/(self.dx)
    def st2t(self, st):
        return self.tLo + st*self.dt
    def sx2x(self, sx):
        return self.xLo + sx*self.dx

def init_XtFx(model: pyo.ConcreteModel, xts: XTScaling): # Nt: int, Nx: int,  FxLo: float, FxUp: float):
    # Values of sx(st) for SCALED x, t  !!!
    DX = xts.xUp - xts.xLo
    DFx = xts.FxUp - xts.FxLo
    model.Xt = pyo.Var(pyo.RangeSet(0, xts.Nt), within=pyo.Reals, bounds=(xts.xLo - DX*.1, xts.xUp + DX*.1))
    # Values of Fx(sx) for SCALED argument !!!
    model.Fx = pyo.Var(pyo.RangeSet(0, xts.Nx), within=pyo.Reals, bounds=(xts.FxLo - DFx*.1, xts.FxUp + DFx*.1))
    model.tLo = pyo.Param(initialize=xts.tLo)
    model.tUp = pyo.Param(initialize=xts.tUp)
    model.xLo = pyo.Param(initialize=xts.xLo)
    model.xUp = pyo.Param(initialize=xts.xUp)
    model.FxLo = pyo.Param(initialize=xts.FxLo)
    model.FxUp = pyo.Param(initialize=xts.FxUp)


def MSD_expr(m: pyo.ConcreteModel, xts: XTScaling, txValuesData: list):
    MSD_summands = []
    for tx in txValuesData:
        t, x = tx[0], tx[1]
        # st = (t - tLo) * Nt / (tUp - tLo)
        # sx = (x - xLo) * Nx / (xUp - xLo)
        MSD_summands.append((x - pw_xt_val(m, t, xts)) ** 2)
    return (pyo.quicksum(msd for msd in MSD_summands)/len(txValuesData))

def REG_expr(m: pyo.ConcreteModel, xts: XTScaling, regCoeff: float):
    dx = (xts.xUp - xts.xLo)/xts.Nx
    # return (regCoeff*( (1/dx)**3 )*pyo.quicksum( (m.Fx[j+1] - 2*m.Fx[j] + m.Fx[j-1])**2 for j in range(1, xts.Nx))/(xts.Nx - 1) )
    return (regCoeff * pyo.quicksum((m.Fx[j + 1] - 2 * m.Fx[j] + m.Fx[j - 1]) ** 2 for j in range(1, xts.Nx)) / (xts.Nx - 1))

def add_SvFObject(model: pyo.ConcreteModel, xts: XTScaling, txValuesData: list, regCoeff: float):
    """
    Add MSD(X-xData) + reg*REG(Fx) object function
    :param model: the model
    :param txValuesData: list of (tVal, xVal) tuples of experimental data
    :param regCoeff:
    :return:
    """
    if regCoeff < 0:
        raise Exception("regCoeff = %f < 0" % (regCoeff))
    # model.svfObj = pyo.Objective(expr=MSD_expr(model, xts, txValuesData) +
    #                                   REG_expr(model, xts, regCoeff), sense=pyo.minimize)
    model.svfObjVar = pyo.Var(within=pyo.Reals)
    model.svfExpression = pyo.Expression(expr = MSD_expr(model, xts, txValuesData) + REG_expr(model, xts, regCoeff))
    model.svfObjBound = \
        pyo.Constraint(expr =  model.svfExpression <= model.svfObjVar)
    model.svfObj = pyo.Objective(expr = model.svfObjVar, sense=pyo.minimize)

def sA(m: pyo.ConcreteModel, j): return (m.Fx[j] - m.Fx[j-1])
def s_eta_sqrt(sx, j: int, eps):
    # dx = (xts.xUp - xts.xLo)/xts.Nx
    return  (sx - j)**2/pyo.sqrt((sx - j)**2 + eps) # pyo.sqrt((sx - j)**2 + eps)

# 1/2*(FF(y(0))+FF(y(Ny))+A(1)*(y-y(0))+A(Ny)*(y-y(Ny))) + 1/2*(sum( A(j)*eta(j-1,y,e),j,2,Ny) - sum( A(j)*eta(j,y,e),j,1,Ny-1))
# pyo.quicksum(z for z in [x, - Nx, + 1])) +
def pwFx_sqrt(m: pyo.ConcreteModel, x, xts:XTScaling, eps):
    dx = (xts.xUp - xts.xLo)/xts.Nx
    sx = (x - xts.xLo)/dx
    return  0.5 * (  m.Fx[0] + m.Fx[xts.Nx] + sA(m,1)*(sx - 0) + sA(m, xts.Nx)*(sx - xts.Nx) + # | m.Fx[0] + m.Fx[xts.Nx - 1] + sA(m,1)*(sx - 0) + sA(m, xts.Nx)*(sx - xts.Nx + 1) +
              pyo.quicksum( (m.Fx[j] - 2*m.Fx[j-1] + m.Fx[j-2])*s_eta_sqrt(sx, j - 1, eps) for j in range(2, xts.Nx + 1) ))

#sum( (A(m, j) - A(m,j-1))*eta_sqrt(x, j-1, eps) for j in range(2, Nx+1) )
# sum(A(m, j)*eta_sqrt(x, j-1, eps) for j in range(2, Nx+1)) -
# sum(A(m, j)*eta_sqrt(x, j, eps)   for j in range(1, Nx))

def pwFx_eta(m: pyo.ConcreteModel, x, xts:XTScaling, k):
    dx = (xts.xUp - xts.xLo)/xts.Nx
    sx = (x - xts.xLo)/dx
    return  0.5 * (  m.Fx[0] + m.Fx[xts.Nx] + sA(m,1)*(sx - 0) + sA(m, xts.Nx)*(sx - xts.Nx) +
              pyo.quicksum( (m.Fx[j] - 2*m.Fx[j-1] + m.Fx[j-2])*m.Eta[k, j-1] for j in range(2, xts.Nx + 1) ))

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
        return (m.Xt[k+1] - 2*m.Xt[k] + m.Xt[k-1])/(dt**2) == pwFx_sqrt(m, m.Xt[k], xts, eps)

    model.setOde2K = pyo.RangeSet(1, xts.Nt - 1)
    if useEta:
        raise Exception("add_ode2_XtFx: %s" % ("Eta NOT IMPLEMENTED Yet!"))
        model.setEtaJ = pyo.RangeSet(1, Nx - 1)
        model.Eta = pyo.Var(model.setOde2K, model.setEtaJ, within=pyo.PositiveReals)

    def Eta2_rule(m, k, j):
        # print("Eta_rule[%d,%d]"%(k,j))
        return (m.Eta[k, j]**2 == ((m.Xt[k])/2. - j)**2 + eps)
        # return (m.Eta[k, j]**2 == (cntrX(m, k) - m.meshX[j])**2 + eps)
    if useEta:
        raise Exception("add_ode2_XtFx: %s" % ("Eta NOT IMPLEMENTED Yet!"))
        model.Eta2_constr = pyo.Constraint(model.setOde2K, model.setEtaJ, rule=Eta2_rule)

    if useEta:
        raise Exception("add_ode2_XtFx: %s" % ("Eta NOT IMPLEMENTED Yet!"))
        model.Scaled_Ode2_Eta = pyo.Constraint(model.setOde2K, rule=scaled_ode2_XtFx_eta_rule)
    else:
        model.Scaled_Ode2_Sqrt = pyo.Constraint(model.setOde2K, rule=ode2_XtFx_sqrt_rule)

def add_ode1_XtFx(model: pyo.ConcreteModel, xts: XTScaling, eps: float = 0.001, useEta = True):
    """
    Add ODE of the form
    dx(t)/dt = F(x(t)) for variables
    It is assumed that
    x \in [xLo, xUp] - is scaled mesh for x;
    t \in [tLo, tUp] -                for t;
    """
    dt = (xts.tUp - xts.tLo)/xts.Nt
    def ode1_XtFx_sqrt_rule(m, k):
        return (m.Xt[k] - m.Xt[k-1])/dt == pwFx_sqrt(m, (m.Xt[k] + m.Xt[k-1])/2, xts, eps) #m.Xt[k-1]

    model.setOde1K = pyo.RangeSet(1, xts.Nt)
    if useEta:
        raise Exception("add_ode1_XtFx: %s" % ("Eta NOT IMPLEMENTED Yet!"))
        # model.setEtaJ = pyo.RangeSet(1, Nx - 1)
        # model.Eta = pyo.Var(model.setOde2K, model.setEtaJ, within=pyo.PositiveReals)

    def Eta2_rule(m, k, j):
        # print("Eta_rule[%d,%d]"%(k,j))
        return (m.Eta[k, j]**2 == ((m.Xt[k])/2. - j)**2 + eps)
        # return (m.Eta[k, j]**2 == (cntrX(m, k) - m.meshX[j])**2 + eps)
    if useEta:
        raise Exception("add_ode1_XtFx: %s" % ("Eta NOT IMPLEMENTED Yet!"))
        # model.Eta2_constr = pyo.Constraint(model.setOde2K, model.setEtaJ, rule=Eta2_rule)

    if useEta:
        raise Exception("add_ode1_XtFx: %s" % ("Eta NOT IMPLEMENTED Yet!"))
        # model.Scaled_Ode2_Eta = pyo.Constraint(model.setOde2K, rule=scaled_ode2_XtFx_eta_rule)
    else:
        model.Scaled_Ode1_Sqrt = pyo.Constraint(model.setOde1K, rule=ode1_XtFx_sqrt_rule)
        # model.Scaled_Ode1_Sqrt.deactivate()

def add_ode1_XtFx_sos(model: pyo.ConcreteModel, xts: XTScaling):
    """
    Add ODE of the form
    dx(t)/dt = F(x(t)) for variables
    It is assumed that
    x \in [xLo, xUp] - is scaled mesh for x;
    t \in [tLo, tUp] -                for t;
    x = sum w_j*x_j
    F(x) = sum w_j*Fx_j,
    sum w_j = 1, w_j >= 0,
    {w} \in SOS
    """
    dt = (xts.tUp - xts.tLo)/xts.Nt
    dx = (xts.xUp - xts.xLo)/xts.Nx
    scaled_x = lambda x: (x - xts.xLo)/dx
    # pyo.RangeSet(0, xts.Nx)
    if model.find_component("setOde1K") == None:
        model.setOde1K = pyo.RangeSet(1, xts.Nt)

    def expr_dxdt_k_rule(m, k):
        return (m.Xt[k] - m.Xt[k-1])/dt
    model.expr_dxdt_k = pyo.Expression(model.setOde1K, rule=expr_dxdt_k_rule)

    def expr_x_k_for_F_rule(m, k):
        return scaled_x((m.Xt[k] + m.Xt[k-1])/2)
    model.expr_x_k_for_F = pyo.Expression(model.setOde1K, rule = expr_x_k_for_F_rule)

    def ode1_sos_block_rule(b, k):
        b.wsos = pyo.Var(pyo.RangeSet(0, xts.Nx), within=pyo.NonNegativeReals)
        b.wsos_sum_cons = pyo.Constraint(expr = sum(b.wsos[xj] for xj in pyo.RangeSet(0, xts.Nx)) == 1.)
        b.wsos_SOS_cons = pyo.SOSConstraint(var = b.wsos, sos=2)
        b.wsos_at_x_cons = pyo.Constraint(expr = sum(xj * b.wsos[xj] for xj in pyo.RangeSet(0, xts.Nx)) == b.model().expr_x_k_for_F[k]) # x
        b.pw_Fx_cons = pyo.Constraint(
            expr = sum(b.model().Fx[xj] * b.wsos[xj] for xj in pyo.RangeSet(0, xts.Nx)) == b.model().expr_dxdt_k[k])

    model.ode1_sos_bs = pyo.Block(model.setOde1K, rule = ode1_sos_block_rule)

def xtp1_wj_for_ode1(dt: float, dx: float, xLO: float, Xt: float, Xj: float, Xjp1: float, Fxj: float, Fxjp1: float):
    """
    :param dt: (xts.tUp - xts.tLo)/xts.Nt
    :param dx: (xts.xUp - xts.xLo)/xts.Nx
    :param xLO: xts.xLo
    :param Xt: x[t] = xt(t)
    :param Xj: x[j] = x(j)
    :param Xjp1: x[j+1] = x(j+1)
    :param Fxj: F(x[j]) = Fx(j)
    :param Fxjp1: F(x[j+1]) = Fx(j+1)
    :return:
    Det = 2*dx*x(j+1)-dt*Fx(j+1)-2*dx*x(j)+dt*Fx(j)
    x[t+1] = - ((2*dt*Fx(j+1)-2*dt*Fx(j))*xLO+(-2*dx*x(j+1)-dt*Fx(j+1)+2*dx*x(j)+dt*Fx(j))*xt(t)-2*dt*dx*Fx(j)*x(j+1)+2*dt*dx*x(j)*Fx(j+1) ) / Det
    w[j]   =   (2*xLO-2*xt(t)+2*dx*x(j+1)-dt*Fx(j+1)) / Det
    w[j+1] = 1 - w[j]

    Det = 2*dx*Xjp1-dt*Fxjp1-2*dx*Xj+dt*Fxj
    x[t+1] = - ((2*dt*Fxjp1-2*dt*Fxj)*xLO+(-2*dx*Xjp1-dt*Fxjp1+2*dx*Xj+dt*Fxj)*Xt-2*dt*dx*Fxj*Xjp1+2*dt*dx*Xj*Fxjp1 ) / Det
    w[j]   =   (2*xLO-2*Xt+2*dx*Xjp1-dt*Fxjp1) / Det
    """
    Det = 2*dx*Xjp1 - dt*Fxjp1 - 2*dx*Xj + dt*Fxj
    xtp1 = - ((2*dt*Fxjp1 - 2*dt*Fxj)*xLO + (-2*dx*Xjp1 - dt*Fxjp1 + 2*dx*Xj + dt*Fxj)*Xt - 2*dt*dx*Fxj*Xjp1 + 2*dt*dx*Xj*Fxjp1 ) / Det
    wj = (2*xLO-2*Xt+2*dx*Xjp1-dt*Fxjp1) /Det
    # wjp1 = 1 - wj
    return xtp1, wj

def replace_ode1_sm_to_sos(modelSolved: pyo.ConcreteModel, xts: XTScaling):
    # pyo.ConcreteModel.name
    modelSolved.Scaled_Ode1_Sqrt.deactivate()
    modelSolved.del_component("Scaled_Ode1_Sqrt")
    add_ode1_XtFx_sos(modelSolved, xts)
    # Calculate model.Xt[k] and b.wsos !!!
    dt = (xts.tUp - xts.tLo)/xts.Nt
    dx = (xts.xUp - xts.xLo)/xts.Nx
    for k in modelSolved.setOde1K:
        for j in pyo.RangeSet(0, xts.Nx - 1):
            Xt = pyo.value(modelSolved.Xt[k-1])
            Xj = float(j)
            Xjp1 = float(j + 1)
            Fxj = pyo.value(modelSolved.Fx[j])
            Fxjp1 = pyo.value(modelSolved.Fx[j+1])
            xtp1, wj = xtp1_wj_for_ode1(dt, dx, xts.xLo, Xt, Xj, Xjp1, Fxj, Fxjp1)
            if wj >=0 and wj <=1:
                modelSolved.Xt[k].set_value(xtp1)
                modelSolved.ode1_sos_bs[k].wsos[j].set_value(wj)
                modelSolved.ode1_sos_bs[k].wsos[j+1].set_value(1 - wj)
    modelSolved.svfObjVar.set_value(pyo.value(modelSolved.svfExpression))
    modelSolved.name = "init" + modelSolved.getname()

# def init_ode1_sm_to_sos(initModel: pyo.ConcreteModel, modelSolved: pyo.ConcreteModel, xts: XTScaling):
#     # Calculate model.Xt[k] and b.wsos !!!
#     dt = (xts.tUp - xts.tLo)/xts.Nt
#     dx = (xts.xUp - xts.xLo)/xts.Nx
#
#     for j in pyo.RangeSet(0, xts.Nx):
#         initModel.Fx[j].set_value(pyo.value(modelSolved.Fx[j]))
#
#     initModel.Xt[0].set_value(pyo.value(modelSolved.Xt[0]))
#
#     for k in modelSolved.setOde1K:
#         for j in pyo.RangeSet(0, xts.Nx - 1):
#             Xt = pyo.value(modelSolved.Xt[k-1])
#             Xj = float(j)
#             Xjp1 = float(j + 1)
#             Fxj = pyo.value(modelSolved.Fx[j])
#             Fxjp1 = pyo.value(modelSolved.Fx[j+1])
#             xtp1, wj = xtp1_wj_for_ode1(dt, dx, xts.xLo, Xt, Xj, Xjp1, Fxj, Fxjp1)
#             if wj >=0 and wj <=1:
#                 initModel.Xt[k].value = xtp1
#                 initModel.ode1_sos_bs[k].wsos[j].value = wj
#                 initModel.ode1_sos_bs[k].wsos[j+1].value = 1 - wj

def add_ode1_XtFx_log(model: pyo.ConcreteModel, xts: XTScaling):
    """
    Add ODE of the form
    dx(t)/dt = F(x(t)) for variables
    It is assumed that
    x \in [xLo, xUp] - is scaled mesh for x;
    t \in [tLo, tUp] -                for t;
    x = sum w_j*x_j
    F(x) = sum w_j*Fx_j,
    sum w_j = 1, w_j >= 0,
    {w} \in SOS IN LOG Representation !
    """
    dt = (xts.tUp - xts.tLo)/xts.Nt
    dx = (xts.xUp - xts.xLo)/xts.Nx
    scaled_x = lambda x: (x - xts.xLo)/dx
    # pyo.RangeSet(0, xts.Nx)
    model.setOde1K = pyo.RangeSet(1, xts.Nt)

    def expr_dxdt_k_rule(m, k):
        return (m.Xt[k] - m.Xt[k-1])/dt
    model.expr_dxdt_k = pyo.Expression(model.setOde1K, rule=expr_dxdt_k_rule)

    def expr_x_k_for_F_rule(m, k):
        return scaled_x((m.Xt[k] + m.Xt[k-1])/2)
    model.expr_x_k_for_F = pyo.Expression(model.setOde1K, rule = expr_x_k_for_F_rule)

    def pwf_rule(m, k, j):
        return m.Fx[j]
    model.pwCons = Piecewise(model.setOde1K, model.expr_dxdt_k, model.expr_x_k_for_F,
                             pw_pts=[j for j in pyo.RangeSet(0, xts.Nx)],
                             pw_constr_type='EQ',
                             f_rule=pwf_rule,
                             pw_repn='LOG')

def xtp1_wj_wjp1_for_ode2(dt: float, dx: float, xLO: float, Xtm1: float, Xt: float, Xj: float, Xjp1: float, Fxj: float, Fxjp1: float):
    """
    :param dt: (xts.tUp - xts.tLo)/xts.Nt
    :param dx: (xts.xUp - xts.xLo)/xts.Nx
    :param xLO: xts.xLo
    :param Xtm1: x[t-1] = xt(t-1)
    :param Xt: x[t] = xt(t)
    :param Xj: x[j] = x(j)
    :param Xjp1: x[j+1] = x(j+1)
    :param Fxj: F(x[j]) = Fx(j)
    :param Fxjp1: F(x[j+1]) = Fx(j+1)
    :return:
    Det = dx*x(j+1)-dx*x(j)
    x[t+1] = -((dt^2*Fx(j+1)-dt^2*Fx(j))*xLO+(-2*dx*x(j+1)-dt^2*Fx(j+1)+2*dx*x(j)+dt^2*Fx(j))*xt(t)+(dx*x(j+1)-dx*x(j))*xt(t-1)-dt^2*dx*Fx(j)*x(j+1)+dt^2*dx*x(j)*Fx(j+1))
             / Det
    w[j]   =   (xLO-xt(t)+dx*x(j+1)) / Det
    w[j+1] = 1 - w[j]

    Det = dx*Xjp1-dx*Xj
    x[t+1] = -((dt**2*Fxjp1-dt**2*Fxj)*xLO+(-2*dx*Xjp1-dt**2*Fxjp1+2*dx*Xj+dt**2*Fxj)*Xt+(dx*Xjp1-dx*Xj)*Xtm1-dt**2*dx*Fxj*Xjp1+dt**2*dx*Xj*Fxjp1)
             / Det
    w[j]   = (xLO-Xt+dx*Xjp1) / Det
    """
    Det = dx*(Xjp1 - Xj)
    xtp1 = -((dt**2*Fxjp1-dt**2*Fxj)*xLO+(-2*dx*Xjp1-dt**2*Fxjp1+2*dx*Xj+dt**2*Fxj)*Xt+(dx*Xjp1-dx*Xj)*Xtm1-dt**2*dx*Fxj*Xjp1+dt**2*dx*Xj*Fxjp1) / Det
    wj = (xLO-Xt+dx*Xjp1) / Det
    # wjp1 = 1 - wj
    return xtp1, wj

def add_ode2_XtFx_sos(model: pyo.ConcreteModel, xts: XTScaling):
    """
    Add ODE of the form
    d2x(t)/dt2 = F(x(t)) for variables
    It is assumed that
    x \in [xLo, xUp] - is scaled mesh for x;
    t \in [tLo, tUp] -                for t;
    x = sum w_j*x_j
    F(x) = sum w_j*Fx_j,
    sum w_j = 1, w_j >= 0,
    {w} \in SOS
    """
    dt = (xts.tUp - xts.tLo)/xts.Nt
    dx = (xts.xUp - xts.xLo)/xts.Nx
    scaled_x = lambda x: (x - xts.xLo)/dx
    # pyo.RangeSet(0, xts.Nx)
    model.setOde2K = pyo.RangeSet(1, xts.Nt - 1)

    def expr_d2xdt2_k_rule(m, k):
        return (m.Xt[k+1] - 2*m.Xt[k] + m.Xt[k-1])/(dt**2)
    model.expr_d2xdt2_k = pyo.Expression(model.setOde2K, rule=expr_d2xdt2_k_rule)

    def expr_x_k_for_F_rule(m, k):
        return scaled_x(m.Xt[k])
    model.expr_x_k_for_F = pyo.Expression(model.setOde2K, rule = expr_x_k_for_F_rule)

    def ode2_sos_block_rule(b, k):
        jSet = pyo.RangeSet(0, xts.Nx)
        b.wsos = pyo.Var(pyo.RangeSet(0, xts.Nx), within=pyo.NonNegativeReals)
        b.wsos_sum_cons = pyo.Constraint(expr = sum(b.wsos[xj] for xj in jSet) == 1.)
        b.wsos_SOS_cons = pyo.SOSConstraint(var = b.wsos, sos=2) #, weights=[1 for j in jSet]
        b.wsos_at_x_cons = pyo.Constraint(expr = sum(xj * b.wsos[xj] for xj in jSet) == b.model().expr_x_k_for_F[k]) # x
        b.pw_Fx_cons = pyo.Constraint(
            expr = sum(b.model().Fx[xj] * b.wsos[xj] for xj in jSet) == b.model().expr_d2xdt2_k[k])

    model.ode2_sos_bs = pyo.Block(model.setOde2K, rule = ode2_sos_block_rule)

def replace_ode2_sm_to_sos(modelSolved: pyo.ConcreteModel, xts: XTScaling):
    # pyo.ConcreteModel.name
    modelSolved.Scaled_Ode2_Sqrt.deactivate()
    modelSolved.del_component("Scaled_Ode2_Sqrt")
    add_ode2_XtFx_sos(modelSolved, xts)
    # Calculate model.Xt[k] and b.wsos !!!
    dt = (xts.tUp - xts.tLo)/xts.Nt
    dx = (xts.xUp - xts.xLo)/xts.Nx
    for k in modelSolved.setOde2K:
        for j in pyo.RangeSet(0, xts.Nx - 1):
            Xtm1 = pyo.value(modelSolved.Xt[k-1])
            Xt = pyo.value(modelSolved.Xt[k])
            Xj = float(j)
            Xjp1 = float(j + 1)
            Fxj = pyo.value(modelSolved.Fx[j])
            Fxjp1 = pyo.value(modelSolved.Fx[j+1])
            xtp1, wj = xtp1_wj_wjp1_for_ode2(dt, dx, xts.xLo, Xtm1, Xt, Xj, Xjp1, Fxj, Fxjp1)
            if wj >=0 and wj <=1:
                modelSolved.Xt[k+1].set_value(xtp1)
                modelSolved.ode2_sos_bs[k].wsos[j].set_value(wj)
                modelSolved.ode2_sos_bs[k].wsos[j+1].set_value(1 - wj)
    modelSolved.svfObjVar.set_value(pyo.value(modelSolved.svfExpression))
    modelSolved.name = "init" + modelSolved.getname()


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx
# def add_ode1_XtFxX(model: pyo.ConcreteModel, xts: XTScaling, eps: float = 0.01, useEta = True):
#     """
#     Add ODE of the form
#     dx(t)/dt = Fpw(x(t))
#     It is assumed that
#     x \in [xLo, xUp] - is scaled mesh for x;
#     t \in [tLo, tUp] -                for t;
#     """
#     dt = (xts.tUp - xts.tLo)/xts.Nt
#
#     def ode1_XtFx_sqrt_rule(m, k):
#         return ((m.Xt[k] - m.Xt[k-1])/dt == pwFx_sqrt(m,(m.Xt[k] + m.Xt[k-1])/2, xts, eps ))
#
#     model.setOde1K = pyo.RangeSet(1, xts.Nt)
#     if useEta:
#         # raise Exception("add_ode1_XtFx: %s" % ("Eta NOT IMPLEMENTED Yet!"))
#         model.setEtaJ = pyo.RangeSet(1, xts.Nx - 1)
#         model.Eta = pyo.Var(model.setOde1K, model.setEtaJ, within=pyo.PositiveReals)
#
#     # def Eta1_rule(m, k, j):
#     #     # print("Eta_rule[%d,%d]"%(k,j))
#     #     return (m.Eta[k, j]**2 == ((m.Xt[k] + m.Xt[k-1])/2. - j)**2 + eps)
#     #     # return (m.Eta[k, j]**2 == (cntrX(m, k) - m.meshX[j])**2 + eps)
#     if useEta:
#         raise Exception("add_ode1_XtFx: %s" % ("Eta NOT IMPLEMENTED Yet!"))
#         # model.Eta1_constr = pyo.Constraint(model.setOde1K, model.setEtaJ, rule=Eta1_rule)
#
#     if useEta:
#         raise Exception("add_ode1_XtFx: %s" % ("Eta NOT IMPLEMENTED Yet!"))
#         # model.Scaled_Ode1_Eta = pyo.Constraint(model.setOde1K, rule=scaled_ode1_XtFx_eta_rule)
#     else:
#         model.Ode1_Sqrt = pyo.Constraint(model.setOde1K, rule=ode1_XtFx_sqrt_rule)
