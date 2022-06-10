import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pyomo.environ as pyo

def plotModelPW(model: pyo.ConcreteModel):
    t = np.array([pyo.value(model.meshT[i])  for i in model.setTidx], dtype=float)
    # pyo.value(theModel.Xt[t]) for t in theModel.setTidx
    Xt = np.array([pyo.value(model.Xt[t]) for t in model.setTidx], dtype=float)

    y = np.array([pyo.value(model.meshY[j])  for j in model.setYidx])
    Fy = np.array([pyo.value(model.Fy[j]) for j in model.setYidx], dtype=float)

    fig, ax = plt.subplots()
    ax.plot(y, Fy)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')
    ax.grid()
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(t, Xt)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')
    ax.grid()

    plt.show()

