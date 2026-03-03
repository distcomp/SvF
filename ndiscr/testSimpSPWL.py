import os
import math
import random

import pyomo.environ as pyo

m = pyo.ConcreteModel("testSimpSPWL")
(Nx, Ny)  = (3, 3)
print("Nx: ", Nx)
print("Ny: ", Ny)
m.I = pyo.RangeSet(0, Nx)
m.J = pyo.RangeSet(0, Ny)
m.X = pyo.Var(m.I, within=pyo.Reals)
m.Y = pyo.Var(m.J, within=pyo.Reals)
m.F = pyo.Var(m.I, m.J, within=pyo.Reals)
m.x = pyo.Var()

m.eps = pyo.Param(initialize=.01)

m.A = pyo.Expression(m.I, m.J)
for i in m.I:
    if i == 0: continue
    for j in m.J:
        m.A[i,j] = m.F[i,j] - m.F[i-1,j]

m.Fx = pyo.Expression(m.J)
for j in m.J:
    m.Fx[j] = (1/2)*(m.F[0,j] + m.A[1,j]*(m.x - m.X[0]) + m.F[0,j] + m.A[Nx,j]*(m.x - m.X[Nx])) + \
              (1/2)*pyo.quicksum(m.A[i,j] - m.A[i-1,j]*pyo.sqrt( (m.x - m.X[i-1])**2 + m.eps**2) for i in pyo.RangeSet(2, Nx))
