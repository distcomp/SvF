#
# expected solution X=5, Y=6
#
from pyomo.core import *

from write import get_smap_var
from write import write_nl_only

xdata = [1., 3., 6., 10.]
ydata  = [6.,2.,8.,7.]

model = ConcreteModel()

model.X = Var(bounds=(1,10))
model.Y = Var(bounds=(0,100))

model.con = Piecewise(model.Y,model.X,
                      pw_pts=xdata,
                      pw_constr_type='EQ',
                      f_rule=ydata,
                      pw_repn='SOS2')

# see what we get for Y when X=5
def con2_rule(model):
    return model.X==5

model.con2 = Constraint(rule=con2_rule)

model.obj = Objective(expr=model.Y, sense=maximize)

model.pprint()

write_nl_only(model, "testPWSOS.nl", symbolic_solver_labels=True)
