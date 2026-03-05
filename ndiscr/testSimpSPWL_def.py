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
# m.eps = pyo.Expression(initialize=.01)
# m.eps = pyo.Expression(expr = .01)


# m.A = pyo.Expression(m.I1, m.J)
# for i in m.I1:
#     for j in m.J:
#         m.A[i,j] = m.F[i,j] - m.F[i-1,j]
A = lambda i, j: m.F[i,j] - m.F[i-1,j]

# m.Fx = pyo.Expression(m.J)
# for j in m.J:
#     m.Fx[j] = (1/2)*(m.F[0,j] + m.A[1,j]*(m.x - m.X[0]) + m.F[0,j] + m.A[Nx,j]*(m.x - m.X[Nx])) + \
#               (1/2)*pyo.quicksum(m.A[i,j] - m.A[i-1,j]*pyo.sqrt( (m.x - m.X[i-1])**2 + m.eps**2) for i in pyo.RangeSet(2, Nx))
# # print(pexpv.expression_to_string(m.Fx[1], verbose=False) )

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
    # xxx = (1/2)*(m.Fx[0] + m.Ax[1]*(m.y - m.Y[0]) + m.Fx[Ny] + m.Ax[Ny]*(m.y - m.Y[Ny])) + \
    #     (1/2)*pyo.quicksum(m.Ax[j] - m.Ax[j-1]*pyo.sqrt( (m.y - m.Y[j-1])**2 + m.eps**2) for i in pyo.RangeSet(2, Ny))
    return (1/2) * (tFx(0, x) + tAx(1,x) * (y - m.Y[0]) + tFx(Ny, x) + tAx(Ny,x) * (y - m.Y[Ny])) + \
           (1/ 2) * pyo.quicksum((tFx(j,x) - 2*tFx(j - 1, x) + tFx(j - 2, x)) * pyo.sqrt((y - m.Y[j - 1]) ** 2 + m.eps ** 2) for j in pyo.RangeSet(2, Ny))

m.x = pyo.Var()
m.y = pyo.Var()

spwl_Fxy = tFxy(m.x, m.y)
original_Fxy_str = pexpv.expression_to_string(spwl_Fxy, verbose=False)
print("Original F(x,y):\n", original_Fxy_str, "\n length ", len(original_Fxy_str))
# print(m.Fxy.__str__())
simp_spwl_Fxy = simplify.simplify_with_sympy(spwl_Fxy)
simplified_Fxy_str = pexpv.expression_to_string(simp_spwl_Fxy, verbose=False)
print("Simplified F(x,y):\n", simplified_Fxy_str, "\n length ", len(simplified_Fxy_str))



