import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pyomo.environ as pyo

from testScaledOdePW import XTScaling

def plotScaledModelPW(model: pyo.ConcreteModel, XTscaler: XTScaling, txDataValues, savefigFileName):
    # t = np.array([pyo.value(model.meshT[i])  for i in model.setTidx], dtype=float)
    tIndex = range(0, XTscaler.Nt + 1)
    t = np.array([XTscaler.st2t(k) for k in tIndex], dtype=float)
    # Xt = np.array([pyo.value(model.Xt[t]) for t in model.setTidx], dtype=float)
    Xt = np.array([pyo.value(model.Xt[k]) for k in tIndex], dtype=float)
    # XtData = np.array([pyo.value(model.XtData[t]) for t in model.setTidx], dtype=float)
    t_data = np.array([tx[0] for tx in txDataValues])
    x_data = np.array([tx[1] for tx in txDataValues])
    # y = np.array([pyo.value(model.meshX[j])  for j in model.setXidx])
    xIndex = range(0, XTscaler.Nx + 1)
    x = np.array([XTscaler.sx2x(j) for j in xIndex], dtype=float)
    Fx = np.array([pyo.value(model.Fx[j]) for j in xIndex], dtype=float)

    fig, ax = plt.subplots()
    ax.plot(x, Fx, label='F(x)')
    ax.set(xlabel='x', ylabel='F(x)', title=model.getname() + ', F(x)')
    ax.grid()
    plt.legend()
    plt.savefig(savefigFileName + '_Fx' + '.png')
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(t, Xt, label='Xt')
    ax.plot(t_data, x_data, 'ro', label=("%s, err=%.1f %%" % ('XtData', 100*XTscaler.errData)))
    ax.set(xlabel='t', ylabel='x(t)', title=model.getname() + ', x(t)')
    ax.grid()
    plt.legend()
    plt.savefig(savefigFileName + '_Xt' + '.png')
    plt.show()

def plotSplineModelPW(model: pyo.ConcreteModel, savefigFileName):
    ys = np.array([pyo.value(model.meshYs[k])  for k in model.setSidx], dtype=float)
    # pyo.value(theModel.Xt[t]) for t in theModel.setTidx
    Sx = np.array([pyo.value(model.Sx[k]) for k in model.setSidx], dtype=float)
    SData = np.array([pyo.value(model.SData[k]) for k in model.setSidx], dtype=float)

    y = np.array([pyo.value(model.meshX[j])  for j in model.setXidx])
    Fx = np.array([pyo.value(model.Fx[j]) for j in model.setXidx], dtype=float)

    # fig, ax = plt.subplots()
    # ax.plot(y, Fx)
    # ax.set(xlabel='y', ylabel='F(y)',
    #        title=model.getname() + ', F(y)')
    # ax.grid()
    # plt.show()

    fig, ax = plt.subplots()
    ax.plot(y, Fx, label='Fx')
    ax.plot(ys, Sx, label='Sx')
    ax.plot(ys, SData, 'ro', label='SData')
    ax.set(xlabel='y', ylabel='S(y)',
           title=model.getname() + ', x(t)')
    plt.legend()
    plt.savefig(savefigFileName + '.png')
    plt.show()

def plotModelPW(model: pyo.ConcreteModel, savefigFileName):
    t = np.array([pyo.value(model.meshT[i])  for i in model.setTidx], dtype=float)
    # pyo.value(theModel.Xt[t]) for t in theModel.setTidx
    Xt = np.array([pyo.value(model.Xt[t]) for t in model.setTidx], dtype=float)
    XtData = np.array([pyo.value(model.XtData[t]) for t in model.setTidx], dtype=float)

    y = np.array([pyo.value(model.meshX[j])  for j in model.setXidx])
    Fx = np.array([pyo.value(model.Fx[j]) for j in model.setXidx], dtype=float)

    fig, ax = plt.subplots()
    ax.plot(y, Fx, label='F(y)')
    ax.set(xlabel='y', ylabel='F(y)', title=model.getname() + ', F(y)')
    ax.grid()
    plt.legend()
    plt.savefig(savefigFileName + '_Fy' + '.png')
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(t, Xt, label='Xt')
    ax.plot(t, XtData, 'ro', label='XtData')
    ax.set(xlabel='t', ylabel='x(t)', title=model.getname() + ', x(t)')
    ax.grid()
    plt.legend()
    plt.savefig(savefigFileName + '_Xt' + '.png')
    plt.show()

