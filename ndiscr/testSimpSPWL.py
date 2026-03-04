import os
import math
import random

import pyomo.environ as pyo

import pyomo.core.expr.visitor as pexpv
from pyomo.contrib.simplification import Simplifier

m = pyo.ConcreteModel("testSimpSPWL")
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
m.x = pyo.Var()
m.y = pyo.Var()

m.eps = pyo.Param(initialize=.01)

m.A = pyo.Expression(m.I1, m.J)
for i in m.I1:
    for j in m.J:
        m.A[i,j] = m.F[i,j] - m.F[i-1,j]

m.Fx = pyo.Expression(m.J)
for j in m.J:
    m.Fx[j] = (1/2)*(m.F[0,j] + m.A[1,j]*(m.x - m.X[0]) + m.F[0,j] + m.A[Nx,j]*(m.x - m.X[Nx])) + \
              (1/2)*pyo.quicksum(m.A[i,j] - m.A[i-1,j]*pyo.sqrt( (m.x - m.X[i-1])**2 + m.eps**2) for i in pyo.RangeSet(2, Nx))
print(pexpv.expression_to_string(m.Fx[1], verbose=False) )

m.Ax = pyo.Expression(m.J1)
for j in m.J1:
    m.Ax[j] = m.Fx[j] - m.Fx[j-1]
m.Fxy = pyo.Expression()
m.Fxy = (1/2)*(m.Fx[0] + m.Ax[1]*(m.y - m.Y[0]) + m.Fx[Ny] + m.Ax[Ny]*(m.y - m.Y[Ny])) + \
        (1/2)*pyo.quicksum(m.Ax[j] - m.Ax[j-1]*pyo.sqrt( (m.y - m.Y[j-1])**2 + m.eps**2) for i in pyo.RangeSet(2, Ny))
print(pexpv.expression_to_string(m.Fxy, verbose=False) )


