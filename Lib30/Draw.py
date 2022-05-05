# -*- coding: UTF-8 -*-

from __future__ import division
import matplotlib.pyplot as plt

from GridArgs import *
from Pars        import *
from Lego import *

from   Object import *

#from Task    import *
from Table   import *
from GIS     import *

import matplotlib.ticker

def DrawComb( param ):
    Transp = SvF.DrawTransp
    FONT_SIZE = 16 #24  # 16 # 7
    NUM_FONT_SIZE = 14
    axisNUM_FONT_SIZE = 15 #20
    yRotation = 0
    FONTstyle = 'italic'
#    Xsize = 8
 #   Ysize = 7
    Xsize = SvF.Xsize
    Ysize = SvF.Ysize
#    Xsize = 5
 #   Ysize = 4
    fig, ax = plt.subplots(figsize=(Xsize, Ysize), dpi=SvF.DPI)
    #     ax.xaxis.set_label_coords(1.03, +0.06)
#    ax.xaxis.set_label_coords(1.04,  0.060)
    ax.xaxis.set_label_coords(SvF.Xlabel_x, -0.01 ) # SvF.Xlabel_x ) #-0.01)
    ax.yaxis.set_label_coords(SvF.Ylabel_x, 1.02)  # в длиннах оси
#    ax.yaxis.set_label_coords(0.03, 1.02)  # в длиннах оси
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
    Flow = False
    MarkerSize = SvF.MarkerSize
    MarkerColor = SvF.MarkerColor
    MarkerEdgeColor = 'r'
    MarkerEdgeWidth = 0
    Marker = 'o'
    DataMarker = 'o'
    DataMarkerSize = SvF.DataMarkerSize
    DataLineWidth = 0
    LineWidth = SvF.LineWidth
    LineColor = SvF.LineColor
#    print ("LLL", LineColor )
    LineStyle = '-'
    DataColor = SvF.DataColor
    name = ''
    file_name = ''

    parts = param.split(' ')
    x_min = 0
    x_max = 1
    D2 = False
    levs = 10

    NoTicks = 0

    for part in parts :
        if part == '': continue
        polyline = None
        fun = None
        to_draw = ''
        print ('part', part)
        for ipar, par in enumerate(part.split(';')) :                  #  Параметры отделяются ;
#        draw_par = part.split(',')
            print ('par', par, ipar)
            if ipar == 0 :                          # FUN OR PPolyline NAME  or File
                ob = getObjectNotGrid(par)   #  Для  drawSvF
#                print ("OOOOOOOOOOOOOOOO")
                ob.Oprint()
                if ob is None:
#                    print ( 'PP', par )
                    if par.find('.sol') >=0 :
                        fun = FunFromSolFile(par)             # FROM Sol FILE
#                        print ("F", fun.grd)
                    else:
                        print ('par222', par)
  #                      fun = FunFromSolFile(par)
                        tb = Select ( '* from ' + par )
                        polyline = Polyline(tb.dat('X'), tb.dat('Y'), None, par)
                elif ob.Otype == 'Fun': # 'Fun'
                        fun = ob
                elif ob.Otype == 'Table':  # 'Tab'
                    print('NNNNNNNN')
                    1/0
                else :                  # ob.o_type == 'Polyline':
#                    polyline = ob.object
                    polyline = ob

                if fun is None:
                    to_draw = 'Polyline'
                else:
 #                   if fun.type != 'g' and fun.type != 'G':   fun = fun.gClone(True)
                    if fun.type == 'p':   fun = fun.gClone(True)
                    to_draw = 'Fun' + str(fun.dim)

            elif par.split(':')[0] == 'L' :  levs = par.split(':')[1].split(',')     # УРОВНИ  отделяются ,
            elif par.split(':')[0] == 'LC':  LineColor = par.split(':')[1]          # Line Col
            elif par.split(':')[0] == 'DC':  DataColor = par.split(':')[1]          # Line Col
            elif par.split(':')[0] == 'DM':  DataMarker = par.split(':')[1]         # DataMarker  = 'o'
            elif par.split(':')[0] == 'DMS': DataMarkerSize = float(par.split(':')[1])   #  DataMarkerSize
            elif par.split(':')[0] == 'DLW': DataLineWidth = float(par.split(':')[1])
            elif par.split(':')[0] == 'LSt': LineStyle = par.split(':')[1]          # Line Style
            elif par.split(':')[0] == 'LW':  LineWidth = float ( par.split(':')[1] )  # LineWidth
            elif par.split(':')[0] == 'M':   Marker = par.split(':')[1]  # Marker  = 'o'
            elif par.split(':')[0] == 'MC':  MarkerColor = par.split(':')[1]   #  MarkerCol
            elif par.split(':')[0] == 'MS':  MarkerSize = float(par.split(':')[1])   #  MarkerSize
            elif par.split(':')[0] == 'MEC': MarkerEdgeColor = par.split(':')[1]     #  MarkerEdgeColor
            elif par.split(':')[0] == 'MEW': MarkerEdgeWidth = float(par.split(':')[1]) # MarkerEdgeWidth
            elif par.upper() == 'TRANSP'  :  Transp = True
            elif par == 'DrawErr'         :  DrawErr = True
            elif par == 'Flow'            :  Flow = True
#            elif par.split(':')[0] == 'MEW': MarkerEdgeWidth = float(par.split(':')[1])  # MarkerEdgeWidth
            elif par.split(':')[0] == 'Xstep':
                Xstep = float(par.split(':')[1])
                ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator (base=Xstep))
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
 #           Xstep = 0.4
  #          ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=Xstep))  # 0.5))
            name = fun.V.name                   # 25/04
            file_name += name
            print (file_name)
            A = fun.A[0]
            tb_x = A.Val #zeros(A.Ub + 1, float64)
            tb_y = zeros(A.Ub + 1, float64)
            for i in A.NodS:
              tb_y[i] = fun.grdNaNreal(i)
            x_min = tb_x[0];  x_max = tb_x[-1]

            if not DrawErr:
                if not ((A.dat is None) or (V.dat is None)):                # DRAW  data    #  точки  данные
 #                   print (A.dat); print (V.dat)
#                    if name != '' : label_name = V.draw_name + SvF.Draw_data_str  #'data'
                    if name != '' : label_name = V.oname + SvF.Draw_data_str  #'data'
                    else          : label_name = ''
                    if not SvF.Legend: label_name = ''
                    if str(type(A.dat)) == '<class \'list\'>' :
                        Adat = [x + A.min for x in A.dat]
                    else :
                        Adat = A.dat + A.min
#                    print ('LL', label_name)
#                    plt.plot(A.dat + A.min, V.dat, color = DataColor, label=label_name,
                    plt.plot(Adat, V.dat, color = DataColor, label=label_name,
                                    markersize=DataMarkerSize, marker=DataMarker, markerfacecolor=DataColor,
                                    linewidth=DataLineWidth)  # markerfacecolor='#FFFFFF' '#000000'
                                                                            # Draw Model  линии модели
#                ax.plot(tb_x, tb_y, LineColor, label='', linestyle=LineStyle, linewidth=LineWidth,
 #                               markersize=MarkerSize, marker='o', markerfacecolor='#FFFFFF')
                if LineWidth==0 and MarkerSize==0 : label_name = ''
                else                              : label_name = V.oname
#                else                              : label_name = V.draw_name
                if not SvF.Legend: label_name = ''
                ax.plot(tb_x, tb_y, LineColor, label=label_name, linestyle=LineStyle, linewidth=LineWidth,
                        markersize=MarkerSize, marker='o', markerfacecolor='#FFFFFF')
            if DrawErr:
              tb_err = deepcopy(V.dat)
              for n in fun.sR:
                  tb_err[n] = fun.delta(n)
              plt.plot( A.dat + A.min, tb_err, LineColor, label=name + 'Err', linewidth=1, #DataColor, #LineWidth,
                     markersize=MarkerSize, marker=Marker, markerfacecolor='#000000')  # markerfacecolor='#FFFFFF'
            ax.set_ylabel(V.draw_name, size=FONT_SIZE, rotation=yRotation)
            ax.set_xlabel(A.oname, size=FONT_SIZE)

            import datetime
            if SvF.X_axe == 'Date' :
              begin = datetime.date(2020, 3, 19)
              ticks = []
              ticks_lab = []
              for i in A.NodS:
                day = (begin + datetime.timedelta(int(tb_x[i]))).day
                if day == 1:
                    month = (begin + datetime.timedelta(int(tb_x[i]))).month
                    ticks.append(tb_x[i])
                    if month == 1:
                        ticks_lab.append(str((begin + datetime.timedelta(int(tb_x[i]))).year))
                    elif int(month / 2) * 2 == month:
                        ticks_lab.append('')
                    else:
                        ticks_lab.append(str(month))
              if len(ticks) > NoTicks:
                NoTicks = len(ticks)
                ax.set_xticks(ticks)
                ax.set_xticklabels(ticks_lab)
                for tick in ax.xaxis.get_major_ticks():
                    if len(tick.label.get_text()) > 2:  tick.label.set_fontsize(FONT_SIZE)  # ГОД
                    else:                               tick.label.set_fontsize(FONT_SIZE - 3)

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

            if Flow:
                DX, DY = makeDXDY(fun, False)
                mDX = MultVal(DX, -1)
                mDY = MultVal(DY, -1)
                tDX = transpose(mDX.grd)
                tDY = transpose(mDY.grd)
                #         tDX = ma.masked_where(tCs <= -9999, tDX)    #################### NODATA
                #        tDY = ma.masked_where(tCs <= -9999, tDY)    #################### NODATA
                #          strm = plt.streamplot(X, Y, tDX, tDY, color='bLack', linewidth=1, arrowsize=2.5 ) #1.6
                cs = ax.streamplot(X, Y, tDX, tDY, color='bLack', linewidth=.5, arrowsize=.5)  # 1.6
#                strm = plt.streamplot(X, Y, tDX, tDY, color='bLack', linewidth=2, arrowsize=3)  # 1.6
            else:

                if SvF.printL: print ("z shape", z.shape, Ax.Ub + 1, Ay.Ub + 1)

                for j in Ax.NodS:
                    for i in Ay.NodS:
                        if Transp:      z[i, j] = fun.grdNaNreal (i, j)
                        else:           z[i, j] = fun.grdNaNreal (j, i)

                z = ma.masked_where(z <= -9999, z)  #################### NODATA == NaN  !!!
 #              if mii == maa and len(levs) == 1: levs = [mii - 1, mii, mii + 1]
                if mii == maa and type(levs) == type(1): levs = [mii - 1, mii, mii + 1]     #28
                cs = ax.contourf(X, Y, z, levs, cmap=colorMap)  # cm.PuBu_r  cm.autumn   cm.gray

                if (not mii is None) and mii != maa:
                    cs1 = ax.contour(X, Y, z, levs, colors='k', linewidths=0.5)
                    ax.clabel(cs1, inline=1, fontsize=NUM_FONT_SIZE, fmt=levelFmt)

                plt.xlabel(Ax.oname, fontsize=FONT_SIZE + 1, style=FONTstyle)
                plt.ylabel(Ay.oname, fontsize=FONT_SIZE + 1, style=FONTstyle, rotation=yRotation)
                if SvF.Legend :
                    plt.title(fun.onameFun(), fontsize=FONT_SIZE + 1, style=FONTstyle, y=1.01)  # , pad = 3)
                    cbar = plt.colorbar(cs)
                    ticklabs = cbar.ax.get_yticklabels()
                    cbar.ax.set_yticklabels(ticklabs, fontsize=NUM_FONT_SIZE)
          # Data
                if not (Ax.dat is None or Ay.dat is None):
                    plt.plot(Ax.dat + Ax.min, Ay.dat + Ay.min, LineColor, # label="y+",
                         markersize=DataMarkerSize, marker='o', markerfacecolor= MarkerColor,
                         markeredgecolor= MarkerColor, linestyle=LineStyle, linewidth=DataLineWidth)
        else :  #  to_draw == 'Polyline'
                if name == '' : name = polyline.name
                print ('Pname',name, MarkerSize)
                if Transp:
                    plt.plot(polyline.Y, polyline.X, LineColor, label=name, markersize=MarkerSize,
                                        marker='o', linewidth=LineWidth, linestyle=LineStyle )
                else:
                    plt.plot(polyline.X, polyline.Y, LineColor, label=name, markersize=MarkerSize,
                         markerfacecolor= MarkerColor, markeredgecolor=MarkerEdgeColor, markeredgewidth = MarkerEdgeWidth,
                         marker=Marker, linewidth=LineWidth, linestyle=LineStyle ) #, fillstyle='none' )
                file_name += name

    if D2 == False and SvF.Legend:
        ax.legend(fancybox=True, prop={'size': FONT_SIZE}, framealpha=0)  # framealpha -
        #  ax.legend(loc=1, prop={'size': FONT_SIZE})
#    print (file_name + '.'+ SvF.graphic_file_type)
    if DrawErr:  plt.savefig(file_name+'Err.' + SvF.graphic_file_type, dpi=SvF.DPI)  # (os.path.join('%s'%dir,'inner_int_gamma_%g%s.%s'%(fun.gamma, suffix, fmt)), dpi = dpi)
    else:        plt.savefig(file_name + '.'+ SvF.graphic_file_type, dpi=SvF.DPI)
    plt.show()
