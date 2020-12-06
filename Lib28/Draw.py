# -*- coding: UTF-8 -*-

from __future__ import division
import matplotlib.pyplot as plt

from GridVarArgs import *
from Pars        import *
from Lego import *


import COMMON as co
from Objects import *
from Table   import *
from GIS     import *

def DrawComb( param ):
    Transp = co.DrawTransp
    FONT_SIZE = 24  # 16 # 7
    NUM_FONT_SIZE = 14
    axisNUM_FONT_SIZE = 20
    yRotation = 0
    FONTstyle = 'italic'
    DPI = 100
    Xsize = 8
    Ysize = 7
    fig, ax = plt.subplots(figsize=(Xsize, Ysize), dpi=DPI)
    #     ax.xaxis.set_label_coords(1.03, +0.06)
    ax.xaxis.set_label_coords(1.04,  0.060)
    ax.yaxis.set_label_coords(0.03, 1.02)  # в длиннах оси
    #     plt.yticks(fontsize=axisNUM_FONT_SIZE, rotation=90)
    plt.yticks(fontsize=axisNUM_FONT_SIZE, rotation=0)
    plt.xticks(fontsize=axisNUM_FONT_SIZE, rotation=0)

    # colorMap = 'binary'
    # colorMap = 'gray'
    colorMap = 'PuBu'
#    colorMap = 'prism'
#    colorMap = 'autumn'
#    colorMap = 'jet'
    DrawErr = False
    MarkerSize = co.MarkerSize
    MarkerColor = co.MarkerColor
    DataMarkerSize = co.DataMarkerSize
#    print ('DataMarkerSize', DataMarkerSize)
    LineWidth = co.LineWidth
    LineColor = co.LineColor
    LineStyle = '-'
    name = ''
    file_name = ''

    parts = param.split(' ')
    x_min = 0
    x_max = 1
    D2 = False
    levs = 10
    for part in parts :
        polyline = None
        fun = None
        to_draw = ''
        print ('part', part)
        for ipar, par in enumerate(part.split(';')) :                  #  Параметры отделяются ;
#        draw_par = part.split(',')
#          print ('par', par, ipar)
            if ipar == 0 :                          # FUN OR PPolyline NAME  or File
                ob = getObject(par)   #  Для  drawSvF
                if ob is None:
#                    print ( 'PP', par )
                    if par.find('.sol') >=0 :  fun = FunFromSolFile(par)             # FROM Sol FILE
                    else:
#                        print ('par', par)
  #                      fun = FunFromSolFile(par)
                        tb = Select ( '* from ' + par )
                        polyline = Polyline(tb.dat('X'), tb.dat('Y'), None, par)
                elif ob.o_type == 'Fun': # 'Fun'
                        fun = ob.object
                else :                  # ob.o_type == 'Polyline':
                    polyline = ob.object

                if fun is None:
                    to_draw = 'Polyline'
                else:
                    if fun.type != 'g':   fun = fun.GridParamClone(True)
                    to_draw = 'Fun' + str(fun.dim)


            elif par.split(':')[0] == 'L' :  levs = par.split(':')[1].split(',')     # УРОВНИ  отделяются ,
            elif par.split(':')[0] == 'LC':  LineColor = par.split(':')[1]          # Line Col
            elif par.split(':')[0] == 'LSt': LineStyle = par.split(':')[1]          # Line Style
            elif par.split(':')[0] == 'LW':  LineWidth = float ( par.split(':')[1] )  # LineWidth
            elif par.split(':')[0] == 'MC':  MarkerColor = par.split(':')[1]   #  MarkerSize
            elif par.split(':')[0] == 'MS':  MarkerSize = float(par.split(':')[1])   #  MarkerSize
            elif par.upper() == 'TRANSP'  :  Transp = True
            elif par == 'DrawErr'          :  DrawErr = True
            else: print ('Draw  ????????????? ************************ par =', par)
        if not fun is None :
            if name == '': name = fun.V.name
            if to_draw == 'Fun2' :
                mii, maa = fun.grd_min_max()
#                levelFmt = ''  # '%.2f'                              # number of digits
                levelFmt = '%.4g'                              # number of digits
                if levelFmt == '' and fun.dim == 2:
                    if (not mii is None) and (not maa is None):
                      if maa != mii:
                        dig = log10((maa - mii) / 10)
                        if dig >= 1:
                            levelFmt = '%.0f'
                        elif dig >= 0:
                            levelFmt = '%.1f'
                        else:
                            dig = int(ceil(-dig))
                            levelFmt = '%.' + str(dig) + 'f'
            V = fun.V

        if to_draw == 'Fun0':  # Const
            tb_x = [x_min, x_max]
#            tb_y = [mii, mii]
            tb_y = [fun.grd, fun.grd]
            name = fun.V.name
            file_name += name
            ax.plot(tb_x, tb_y, "gray", label=name, linestyle=LineStyle, linewidth=LineWidth, # '-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'
                markersize=MarkerSize, marker='o', markerfacecolor='#FFFFFF')
#            print tb_x, tb_y, "red", V.name
        elif to_draw == 'Fun1':  # LINE
            name = fun.V.name                   # 25/04
            file_name += name
            A = fun.A[0]
            tb_x = A.Val #zeros(A.Ub + 1, float64)
            tb_y = zeros(A.Ub + 1, float64)
            for i in A.NodS:
              tb_y[i] = fun.grdNaNreal(i)
            if not ((A.dat is None) or (V.dat is None)):  # DRAW  data
              if not DrawErr:
                #             print 'LL', fun.V.name, len (fun.A[0].dat), len (fun.V.dat)
                  plt.plot(A.dat + A.min, V.dat, 'b+', label=name + "data",  # "m+",
                         markersize=DataMarkerSize, marker='o', markerfacecolor='#000000')  # markerfacecolor='#FFFFFF'
            x_min = tb_x[0];  x_max = tb_x[-1]

            if not DrawErr:  # Draw Model
 #               print (name, tb_y[0])
                ax.plot(tb_x, tb_y, LineColor, label=name, linestyle=LineStyle, linewidth=LineWidth,
                      markersize=MarkerSize, marker='o', markerfacecolor='#FFFFFF')
        #       for tick in ax.xaxis.get_major_ticks():    tick.label.set_fontsize(NUM_FONT_SIZE)
        #     for tick in ax.yaxis.get_major_ticks():    tick.label.set_fontsize(NUM_FONT_SIZE)
            if DrawErr:
              tb_err = deepcopy(V.dat)
              for n in fun.sR:
                  tb_err[n] = fun.delta(n)()
              plt.plot( A.dat + A.min, tb_err, 'b+', label="Data",
                     markersize=MarkerSize, marker='o', markerfacecolor='#000000')  # markerfacecolor='#FFFFFF'

            ax.set_ylabel(name, size=FONT_SIZE, rotation=yRotation)
            ax.set_xlabel(A.oname, size=FONT_SIZE)

        elif to_draw == 'Fun2':  # ISO  ######################################
            D2 = True
            file_name += name

            if Transp:
                Ay = fun.A[0]
                Ax = fun.A[1]
            else :
                Ax = fun.A[0]
                Ay = fun.A[1]

            x = Ax.Val #linspace(Ax.min, Ax.max, Ax.Ub + 1)
            y = Ay.Val #linspace(Ay.min, Ay.max, Ay.Ub + 1)
            z = zeros((Ay.Ub + 1, Ax.Ub + 1), float64)

            X, Y = meshgrid(x, y)

            if co.printL: print ("z shape", z.shape, Ax.Ub + 1, Ay.Ub + 1)

            for j in Ax.NodS:
              for i in Ay.NodS:
                if Transp:      z[i, j] = fun.grdNaNreal (i, j)
                else:           z[i, j] = fun.grdNaNreal (j, i)

            z = ma.masked_where(z <= -9999, z)  #################### NODATA == NaN  !!!
 #           if mii == maa and len(levs) == 1: levs = [mii - 1, mii, mii + 1]
            if mii == maa and type(levs) == type(1): levs = [mii - 1, mii, mii + 1]     #28
            cs = ax.contourf(X, Y, z, levs, cmap=colorMap)  # cm.PuBu_r  cm.autumn   cm.gray

            if (not mii is None) and mii != maa:
                cs1 = ax.contour(X, Y, z, levs, colors='k', linewidths=0.5)
                ax.clabel(cs1, inline=1, fontsize=NUM_FONT_SIZE, fmt=levelFmt)

            plt.xlabel(Ax.oname, fontsize=FONT_SIZE + 1, style=FONTstyle)
            plt.ylabel(Ay.oname, fontsize=FONT_SIZE + 1, style=FONTstyle, rotation=yRotation)
            plt.title(fun.onameFun(), fontsize=FONT_SIZE + 1, style=FONTstyle, y=1.01)  # , pad = 3)
            cbar = plt.colorbar(cs)
            ticklabs = cbar.ax.get_yticklabels()
            cbar.ax.set_yticklabels(ticklabs, fontsize=NUM_FONT_SIZE)
        # Data
            if not (Ax.dat is None or Ay.dat is None):
                plt.plot(Ax.dat + Ax.min, Ay.dat + Ay.min, LineColor, # label="y+",
                         markersize=DataMarkerSize, marker='o', markerfacecolor= MarkerColor,
                         linestyle='-', linewidth=co.DataLineWidth)
        else :  #  to_draw == 'Polyline'
            if name == '' : name = polyline.name
            if Transp:
                plt.plot(polyline.Y, polyline.X, LineColor, label=name, markersize=MarkerSize,
                                        marker='o', linewidth=LineWidth, linestyle='-')
            else:
                plt.plot(polyline.X, polyline.Y, LineColor, label=name, markersize=MarkerSize, markerfacecolor= MarkerColor,
                                        marker='o', linewidth=LineWidth, linestyle='-')
            file_name += name

    if D2 == False :
        ax.legend(fancybox=True, prop={'size': FONT_SIZE}, framealpha=0)  # framealpha -
        #  ax.legend(loc=1, prop={'size': FONT_SIZE})

    if DrawErr:  plt.savefig(file_name+'Err' + '.png')  # (os.path.join('%s'%dir,'inner_int_gamma_%g%s.%s'%(fun.gamma, suffix, fmt)), dpi = dpi)
    else:        plt.savefig(file_name + '.png')
    plt.show()
