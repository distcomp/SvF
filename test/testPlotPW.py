import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pyomo.environ as pyo

def plotSplineModelPW(model: pyo.ConcreteModel, savefigFileName):
    ys = np.array([pyo.value(model.meshYs[k])  for k in model.setSidx], dtype=float)
    # pyo.value(theModel.Xt[t]) for t in theModel.setTidx
    Sy = np.array([pyo.value(model.Sy[k]) for k in model.setSidx], dtype=float)
    SData = np.array([pyo.value(model.SData[k]) for k in model.setSidx], dtype=float)

    y = np.array([pyo.value(model.meshY[j])  for j in model.setYidx])
    Fy = np.array([pyo.value(model.Fy[j]) for j in model.setYidx], dtype=float)

    # fig, ax = plt.subplots()
    # ax.plot(y, Fy)
    # ax.set(xlabel='y', ylabel='F(y)',
    #        title=model.getname() + ', F(y)')
    # ax.grid()
    # plt.show()

    fig, ax = plt.subplots()
    ax.plot(y, Fy, label='Fy')
    ax.plot(ys, Sy, label='Sy')
    ax.plot(ys, SData, 'ro', label='SData')
    ax.set(xlabel='y', ylabel='S(y)',
           title=model.getname() + ', x(t)')
    plt.legend()
    plt.savefig(savefigFileName + '.png')
    plt.show()

def plotModelPW(model: pyo.ConcreteModel):
    t = np.array([pyo.value(model.meshT[i])  for i in model.setTidx], dtype=float)
    # pyo.value(theModel.Xt[t]) for t in theModel.setTidx
    Xt = np.array([pyo.value(model.Xt[t]) for t in model.setTidx], dtype=float)
    XtData = np.array([pyo.value(model.XtData[t]) for t in model.setTidx], dtype=float)

    y = np.array([pyo.value(model.meshY[j])  for j in model.setYidx])
    Fy = np.array([pyo.value(model.Fy[j]) for j in model.setYidx], dtype=float)

    fig, ax = plt.subplots()
    ax.plot(y, Fy)
    ax.set(xlabel='y', ylabel='F(y)',
           title=model.getname() + ', F(y)')
    ax.grid()
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(t, Xt, label='Xt')
    ax.plot(t, XtData, 'ro', label='XtData')
    ax.set(xlabel='t', ylabel='x(t)',
           title=model.getname() + ', x(t)')
    plt.show()

