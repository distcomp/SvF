import pyomo.environ as pyo

import pyomo.core.expr.visitor as pexpv
from pyomo.contrib.simplification import simplify

m = pyo.ConcreteModel("testSimpSPWL")
# m = pyo.AbstractModel("testSimpSPWL")

(Nx, Ny)  = (3, 3)
print("Nx: ", Nx)
print("Ny: ", Ny)
m.I = pyo.RangeSet(0, Nx)
m.J = pyo.RangeSet(0, Ny)
m.I1 = pyo.RangeSet(1, Nx)
m.J1 = pyo.RangeSet(1, Ny)
m.X = pyo.Var(m.I, within=pyo.Reals)
m.Y = pyo.Var(m.J, within=pyo.Reals)
m.F = pyo.Var(m.I, m.J, within=pyo.Reals)

m.eps = pyo.Param(initialize=.01)

A = lambda i, j: m.F[i,j] - m.F[i-1,j]

def tFx(j: int, x: pyo.Var):
    """
    Returns expression widetilde{F}_j(x) SPWL
    """
    if j < 0 or j > Ny:
        raise IndexError(f"tF(j,x), j={j} is out of range {0}:{Ny}")
    return (1/2)*(m.F[0,j] + A(1,j)*(x - m.X[0]) + m.F[0,j] + A(Nx,j)*(x - m.X[Nx])) + \
            (1/2)*pyo.quicksum((m.F[i,j] - 2*m.F[i-1,j] + m.F[i-2,j])*pyo.sqrt( (x - m.X[i-1])**2 + m.eps**2) for i in pyo.RangeSet(2, Nx))


tAx = lambda j, x: tFx(j, x) - tFx(j - 1, x)
def tFxy(x: pyo.Var, y: pyo.Var):
    return (1/2) * (tFx(0, x) + tAx(1,x) * (y - m.Y[0]) + tFx(Ny, x) + tAx(Ny,x) * (y - m.Y[Ny])) + \
           (1/2) * pyo.quicksum((tFx(j,x) - 2*tFx(j - 1, x) + tFx(j - 2, x))*pyo.sqrt((y - m.Y[j - 1]) ** 2 + m.eps ** 2) for j in pyo.RangeSet(2, Ny))

# Nargs число аргументов sos2F(arg)
sos2meshN = Nx # Число узлов сетки sos2F
m.sos2meshIdx = pyo.RangeSet(0, sos2meshN)   # Индексы узлов сетки
def sos2mesh_rule(m, i):
    return m.X[i]               # Пример
m.sos2mesh = pyo.Expression(m.sos2meshIdx, rule=sos2mesh_rule) # Значение узлов сетки аргументов

def sos2meshF_rule(m, i):
    return m.F[i, 0]    # Пример
m.sos2meshF = pyo.Expression(m.sos2meshIdx, rule=sos2meshF_rule)  # Выражения для значения функции в узлах сетки,

sos2argsK = Nx - 1 # Сколько раз надо вычислить sos2F
m.sos2argsIdx = pyo.RangeSet(0, sos2argsK)
def sos2args_rule(m, k):
    return (m.X[k] + m.X[k+1])/2
m.sos2args = pyo.Expression(m.sos2argsIdx, rule = sos2args_rule) # Выражения для аргументов, где надо вычисляять pwlF

def sos2_block_rule(b, k):
    b.wsos = pyo.Var(b.model().sos2meshIdx, within=pyo.NonNegativeReals)
    b.wsos_sum_cons = pyo.Constraint(expr=sum(b.wsos[i] for i in b.model().sos2meshIdx) == 1.)
    b.wsos_SOS2_cons = pyo.SOSConstraint(var=b.wsos, sos=2)
    b.wsos_at_arg_cons = pyo.Constraint(
        expr=sum(b.model().sos2mesh[i] * b.wsos[i] for i in b.model().sos2meshIdx) == b.model().sos2args[k])  # x
    b.Fvalue = sum( b.wsos[i]*b.model().sos2meshF[i] for i in b.model().sos2meshIdx)

m.sos2F = pyo.Block(m.sos2argsIdx, rule=sos2_block_rule)
# m.sos2F[k].Fvalue - выражение для pwlF(m.sos2args[k])

if __name__ == "__main__":
    m.x = pyo.Var()
    m.y = pyo.Var()

    print(m.sos2F[1].Fvalue)

    spwl_Fxy = tFxy(m.x, m.y)
    original_Fxy_str = pexpv.expression_to_string(spwl_Fxy, verbose=False)
    print("Original F(x,y):\n", original_Fxy_str, "\n length ", len(original_Fxy_str))
    # print(m.Fxy.__str__())
    simp_spwl_Fxy = simplify.simplify_with_sympy(spwl_Fxy)
    simplified_Fxy_str = pexpv.expression_to_string(simp_spwl_Fxy, verbose=False)
    print("Simplified F(x,y):\n", simplified_Fxy_str, "\n length ", len(simplified_Fxy_str))



