#
# expected solution X=5, Y=6
#
# from pyomo.core import *
import time
import pyomo.environ as pyo

from write import get_smap_var
from write import write_nl_only

xMesh = [float(j) for j in range(5)] # 200 ~9 sec
xVals = [0.5*(2*k + 1) for k in range(4)] # 150 x-values to calc. Fx, .5, 1.5, 2.5

tic = time.perf_counter()
model = pyo.ConcreteModel()

model.xMesh = pyo.Set(initialize=xMesh, domain=pyo.Reals)
model.xValsSet = pyo.Set(initialize=xVals, domain=pyo.Reals)

# model.xValsSet[0]

# def xVals_init(m, x):
#     return pyo.value(x)
# model.xVals    = pyo.Param(model.xValsSet, initialize=xVals_init)

model.Fx = pyo.Var(model.xMesh, bounds=(-10., 10))
model.pwFxVal = pyo.Var(model.xValsSet)

def ExprPwFxVal_rule(m, x):
    return m.pwFxVal[x]
model.ExprPwFxVal = pyo.Expression(model.xValsSet, rule=ExprPwFxVal_rule)

def xVal_sos_block_rule(b, x):
    b.wsos = pyo.Var(b.model().xMesh, within=pyo.NonNegativeReals)
    b.wsos_sum_cons = pyo.Constraint(expr = sum(b.wsos[xj] for xj in b.model().xMesh) == 1.)
    b.wsos_SOS_cons = pyo.SOSConstraint(var=b.wsos, sos=2 )
    b.wsos_at_x_cons = pyo.Constraint(expr = sum(xj*b.wsos[xj] for xj in b.model().xMesh) == x)
    b.pw_Fx_cons = pyo.Constraint(expr = sum(b.model().Fx[xj]*b.wsos[xj] for xj in b.model().xMesh) == b.model().pwFxVal[x] ) # b.model().ExprPwFxVal[x]
model.pwFxSosBlocks = pyo.Block(model.xValsSet, rule = xVal_sos_block_rule)

if len(xMesh) < 20:
    model.pprint()
write_nl_only(model, "testPWSOS-blocks",  symbolic_solver_labels=True)
toc = time.perf_counter()
print("Blocks, len(xMesh)=%d, len(xVals)=%d took %f sec" % (len(xMesh), len(xVals), toc - tic))
quit()

tic = time.perf_counter()
model = pyo.ConcreteModel()
model.xMesh = pyo.Set(initialize=xMesh, domain=pyo.Reals)
model.xValsSet = pyo.Set(initialize=xVals, domain=pyo.Reals)
model.Fx = pyo.Var(model.xMesh, bounds=(-10., 10))
model.pwFxVal = pyo.Var(model.xValsSet)

def SOS_indices_init(m, x):
    return [(x, xj) for xj in m.xMesh]
model.SOS_indices = pyo.Set(model.xValsSet, dimen=2, ordered=True, initialize=SOS_indices_init)

def SOS_var_indices_init(m):
    return [(x,xj) for x in m.xValsSet for xj in m.xMesh]
model.sos_var_indices = pyo.Set(ordered=True, dimen=2, initialize=SOS_var_indices_init)
model.wsos = pyo.Var(model.sos_var_indices, within=pyo.NonNegativeReals) # SOS2 variable

model.SOS_set_cons = pyo.SOSConstraint(model.xValsSet, var=model.wsos, index=model.SOS_indices, sos=2)

def wsos_sum_cons_rule(m, x):
    return sum(m.wsos[x, xj] for xj in m.xMesh) == 1
model.wsos_sum_cons = pyo.Constraint(model.xValsSet, rule=wsos_sum_cons_rule)

def pw_Fx_cons_rule(m, x):
    return (m.pwFxVal[x] == sum(m.Fx[xj]*m.wsos[x, xj] for xj in m.xMesh))
model.pw_Fx_cons = pyo.Constraint(model.xValsSet, rule=pw_Fx_cons_rule)

def wx_at_xval_cons_rule(m, x):
    return pyo.value(x) == sum(xj * m.wsos[x, xj] for xj in m.xMesh) # pyo.value - is more inpressive but unnecessary !!!
    # return model.xVals[x] == sum(xj*m.wsos[x, xj] for xj in m.xMesh)
model.wx_at_xval_cons = pyo.Constraint(model.xValsSet, rule=wx_at_xval_cons_rule)

if len(xMesh) < 20:
    model.pprint()

write_nl_only(model, "testPWSOS-indices",  symbolic_solver_labels=True)
toc = time.perf_counter()
print("SOS_indices, len(xMesh)=%d, len(xVals)=%d took %f sec" % (len(xMesh), len(xVals), toc - tic))

quit()


xdata = [1., 3., 6., 9]
ydata  = [6.,2.,8.,7.]

model.X = pyo.Var(bounds=(1,10))
model.Y = pyo.Var(bounds=(0,100))

model.ySet = pyo.RangeSet(1, 4)
model.yVar = pyo.Var(model.ySet, bounds=(0,10))

def yMesh_rule(m, x):
    if 0.99 < x < 1.1:
        return m.yVar[1]
    elif 2.99 < x < 3.1:
        return m.yVar[2]
    elif 5.99 < x < 6.1:
        return m.yVar[3]
    elif 8.99 < x < 9.1:
        return m.yVar[4]
    else:
        return 0

#
model.con = pyo.Piecewise(model.Y,model.X,
                      pw_pts=xdata,
                      pw_constr_type='EQ',
                      f_rule=yMesh_rule,
                      pw_repn='SOS2')
#
# # see what we get for Y when X=5
# def con2_rule(model):
#     return model.X==5
#
# model.con2 = pyo.Constraint(rule=con2_rule)
#
# model.obj = pyo.Objective(expr=model.Y, sense=pyo.maximize)
#
# model.pprint()
#
# write_nl_only(model, "testPWSOS.nl", symbolic_solver_labels=True)
