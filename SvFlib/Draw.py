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
from matplotlib.ticker import FuncFormatter

# Функция форматирования для замены точки на запятую
def comma_formatter_pos(x, pos):
#    return f'{x:10.3f}'.replace('.', ',')
    return f'{x:.10g}'.replace('.', ',')


def comma_formatter(x):
    return f'{x:.10g}'.replace('.', ',')
#    return f'{x:.2f}'.replace('.', ',')

def Plot (plots) :
    FONT_SIZE = SvF.FONT_SIZE  # 16 #24  # 16 # 7
    FONTstyle = 'italic'
    NUM_FONT_SIZE = 14  #SvF.NUM_FONT_SIZE
    fig, ax = plt.subplots(figsize=(SvF.Xsize, SvF.Ysize), dpi=SvF.DPI)
    plt.yticks(fontsize=SvF.axisNUM_FONT_SIZE, rotation=0)
    plt.xticks(fontsize=SvF.axisNUM_FONT_SIZE, rotation=0)
    if SvF.xaxis_step != 0:     ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=SvF.xaxis_step))
    if SvF.yaxis_step != 0:     ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=SvF.yaxis_step))
    TRANSPOSE = False

    def swapTRANS(x, y) :
        if TRANSPOSE : return y, x
        else         : return x, y
    FileName = None
    file_name = ''

    C = 'red';  LW = 1.5;  LS = '-'
    MS = 6.0;  MEC = 'auto';  MFC = 'auto'; MARK = None; MEW = 1
    LAB = None

    dC = 'red';  dLW = 0;  dLS = '-'
    dMS = 3.0;  dMEC = 'b';  dMFC = 'none'; dMARK = 'o'; dMEW = 1
    dLAB = None

    xLAB = None;  yLAB = None; tLAB = None   # title
    LEVS = 10; CMAP='PuBu'


    D = None
    xx=None
    yy=None
#    print (plots)
    D = None
    for plo in plots :
        for ip, part_plot in enumerate (plo):
 #           print (ip, type(part_plot))
 #           if part_plot is None : continue                     #  ,,
            if   ip==0 :
                if type(part_plot) == type([]) or type(part_plot) == np.ndarray :
                    xx = part_plot
                    D = '2Dxy'
                elif part_plot.Otype == 'Polyline':
                    D = '2Dpoly'
                    xx = part_plot.X
                    yy = part_plot.Y
                    LAB = part_plot.name
                elif part_plot.Otype == 'Fun':
                    if part_plot.dim == 1:
                        D = '2Dfun1'
                        xx = part_plot.A[0].Val
                        xx_dat = part_plot.A[0].dat
                        xLAB = part_plot.A[0].name
                        yy = part_plot.grd
                        yy_dat = part_plot.V.dat
                        yLAB = part_plot.V.name
                    elif part_plot.dim == 2:
                        D = '2Dfun2'
                        xx = part_plot.A[0].Val
                        xx_dat = part_plot.A[0].dat
                        xLAB = part_plot.A[0].name
                        yy = part_plot.A[1].Val
                        yy_dat = part_plot.A[1].dat
                        yLAB = part_plot.A[1].name
                        zz = part_plot.grd
                        tLAB = part_plot.V.name
                        C = 'k'; LW = 0.5           #  для линий уровня
                    LAB = part_plot.V.name
            elif ip==1 and D=='2Dxy' :  yy = part_plot
            else :
                PAR = part_plot.split('=')[0]
                VAL = None
                if len ( part_plot.split('=') ) == 2:  VAL = part_plot.split('=')[1].strip('"').strip("'")

                if   PAR in ['color', 'c' ] :                   C  = VAL                	# Цвет линии или маркера (например, 'red', '#FF0000')
                elif PAR in ['linewidth', 'lw']:                LW = float(VAL)	            # Толщина линии (в пунктах, float)
                elif PAR in ['linestyle', 'ls'] :               LS = VAL                    # Стиль линии (например, '-', '--', '-.', ':')
                elif PAR in ['marker', 'mark' ] :               MARK = VAL                  # Тип маркера точек (например, 'o', 's', '^', '*')
                elif PAR in ['markersize','ms'] :               MS = float(VAL)             # Размер маркера (в пунктах)
                elif PAR in ['markerfacecolor',	'mfc'] :        MFC = VAL                   # Цвет заливки (внутренней части) маркера mfc=none-не заливать
                elif PAR in ['markeredgecolor', 'mec'] :        MEC = VAL                   # Цвет границы маркера
                elif PAR in ['markeredgewidth', 'mew'] :        MEW = float(VAL)            # Толщина границы маркера
                elif PAR in ['label', 'lab' ] :                 LAB = VAL                   # Текст названия линии. Отображается только при вызове plt.legend()
                #                  Для данных
                elif PAR in ['dcolor', 'dc' ] :                   dC  = VAL                	# Цвет линии или маркера (например, 'red', '#FF0000')
                elif PAR in ['dlinewidth', 'dlw']:                dLW = float(VAL)	        # Толщина линии (в пунктах, float)
                elif PAR in ['dlinestyle', 'dls'] :               dLS = VAL                 # Стиль линии (например, '-', '--', '-.', ':')
                elif PAR in ['dmarker', 'dmark' ] :             dMARK = VAL                  # Тип маркера точек (например, 'o', 's', '^', '*')
                elif PAR in ['dmarkersize','dms'] :             dMS = float(VAL)             # Размер маркера (в пунктах)
                elif PAR in ['dmarkerfacecolor', 'dmfc'] :      dMFC = VAL                   # Цвет заливки (внутренней части) маркера mfc=none-не заливать
                elif PAR in ['dmarkeredgecolor', 'dmec'] :      dMEC = VAL                   # Цвет границы маркера
                elif PAR in ['dmarkeredgewidth', 'dmew'] :      dMEW = float(VAL)            # Толщина границы маркера
                elif PAR in ['xlabel', 'xlab' ] :               xLAB = VAL                   # Текст названия Axe x
                elif PAR in ['ylabel', 'ylab' ] :               yLAB = VAL                   # Текст названия Axe y
                elif PAR in ['tlabel', 'tlab' ] :               tLAB = VAL              # Текст названия Title

                elif PAR in ['filename', 'file']:               FileName = VAL          # сохраняем в файл  FileName
                elif PAR in ['transpose', 'trans']:             TRANSPOSE = not TRANSPOSE
                elif PAR in ['cmap' ]          :                CMAP = VAL              # цветовая карта
                elif PAR in ['levels', 'levs' ] :
                    if VAL[0] == '[' :                  LEVS = VAL[1:-1].split(",")       # число уровней или список уровней
                    else :                              LEVS = int(VAL)

                else:  print('PLOT  ????????????? ************************ PAR =', PAR, VAL)

                """""
                markerfacecoloralt	mfcalt	Альтернативный цвет заливки (используется редко)
                antialiased	aa	Сглаживание линий (True / False)
                alpha	нет	Прозрачность (от 0.0 до 1.0)
                zorder	нет	Порядок отрисовки слоев (чем выше число, тем "выше" слой)
                """""

  #      print ("IIIIIIIIII", ip, MS, MFC, MARK, LAB)

        xLAB, yLAB = swapTRANS(xLAB, yLAB)
        if D == '2Dfun1' or D == '2Dfun2' :
            xx_dat, yy_dat = swapTRANS (xx_dat, yy_dat)
            if not ((xx_dat is None) or (yy_dat is None)):  # DRAW  data    #  точки  данные
                ax.plot(xx_dat, yy_dat, color=dC, lw=dLW, linestyle=dLS,
                    marker=dMARK, markersize=dMS, markerfacecolor=dMFC, markeredgecolor=dMEC, markeredgewidth=dMEW,
                    label=dLAB )
        if D == '2Dfun1' or D == '2Dxy' or D == '2Dpoly' :
            xx, yy = swapTRANS(xx, yy)
            ax.plot(xx, yy, color=C, lw=LW, linestyle=LS,
                marker=MARK, markersize=MS, markerfacecolor=MFC, markeredgecolor=MEC, markeredgewidth=MEW,
                label=LAB )

        elif D == '2Dfun2' :
            xx, yy = swapTRANS(xx, yy)
            if TRANSPOSE:   Z=zz
            else        :   Z=zz.T
            X, Y = np.meshgrid(xx, yy)
            cs = ax.contourf(X, Y, Z, LEVS, cmap=CMAP)
            cbar = plt.colorbar(cs)
       #     if SvF.CommaFormatter:
        #        cbar.ax.yaxis.set_major_formatter(FuncFormatter(comma_formatter_pos))
       #     if (not mii is None) and mii != maa:
            cs1 = ax.contour(X, Y, Z, LEVS, colors=C, linewidths=LW) #, levs, )
        #        if SvF.CommaFormatter:
         #           ax.clabel(cs1, inline=1, fontsize=NUM_FONT_SIZE, fmt=comma_formatter)
          #      else:
           #         ax.clabel(cs1, inline=1, fontsize=NUM_FONT_SIZE, fmt=levelFmt)  # сторо !
            ax.clabel(cs1, inline=1, fontsize=NUM_FONT_SIZE)   #, fmt=levelFmt)  # сторо !

        file_name += LAB
#    if Transp:
 #       ax.set_xlabel(V.axe_name, size=FONT_SIZE)
  #      ax.set_ylabel(A.axe_name, size=FONT_SIZE, rotation=yRotation)
   # else:

    ax.set_ylabel(yLAB, size=FONT_SIZE, rotation=0)  # , yRotation)
    ax.set_xlabel(xLAB, size=FONT_SIZE)
    ax.xaxis.set_label_coords( SvF.Xlabel_x, SvF.Xlabel_y ) #-0.01 ) # SvF.Xlabel_x ) #-0.01)
    ax.yaxis.set_label_coords( SvF.Ylabel_x, SvF.Ylabel_y ) #1.02)  # в длиннах оси

    plt.title(tLAB, fontsize=FONT_SIZE + 1, style=FONTstyle, y=1.01, x=SvF.title_x)  # , pad = 3)

    ax.legend(fancybox=True, prop={'size': FONT_SIZE}, framealpha=0)  # framealpha -

    plt.tight_layout()
    if SvF.DrawMode.find('File') >= 0 :
        if FileName is None:  FileName = file_name
#        if DrawErr:  plt.savefig(File_name+'Err.' + SvF.graphic_file_type, dpi=SvF.DPI)  # (os.path.join('%s'%dir,'inner_int_gamma_%g%s.%s'%(fun.gamma, suffix, fmt)), dpi = dpi)
 #       else:        plt.savefig(File_name + '.'+ SvF.graphic_file_type, dpi=SvF.DPI)
        plt.savefig(FileName + '.' + SvF.graphic_file_type, dpi=SvF.DPI)
    if SvF.DrawMode.find('Screen') >= 0 :
            if SvF.ShowAll :  plt.show(block=False)
            else           :  plt.show()
            """""
            x = Ax.Val #linspace(Ax.min, Ax.max, Ax.Ub + 1)
            y = Ay.Val #linspace(Ay.min, Ay.max, Ay.Ub + 1)
            z = np.zeros((Ay.Ub + 1, Ax.Ub + 1), np.float64)

            X, Y = np.meshgrid(x, y)

            if Flow:
                DX, DY = makeDXDY(fun, False)
                mDX = MultVal(DX, -1)
                mDY = MultVal(DY, -1)
                tDX = transpose(mDX.grd)
                tDY = transpose(mDY.grd)
                cs = ax.streamplot(X, Y, tDX, tDY, color='bLack', linewidth=.5, arrowsize=.5)  # 1.6
            else:

                if SvF.printL: print ("z shape", z.shape, Ax.Ub + 1, Ay.Ub + 1)

                for j in Ax.NodS:
                    for i in Ay.NodS:
                        if Transp:      z[i, j] = fun.grdNaNreal (i, j)
                        else:           z[i, j] = fun.grdNaNreal (j, i)
                from matplotlib import ticker, cm

                z = np.ma.masked_where(z <= -9999, z)  #################### NODATA == nan  !!!
                if mii == maa and type(levs) == type(1): levs = [mii - 1, mii, mii + 1]     #28
                cs = ax.contourf(X, Y, z, levs, locator=SvF.locator, cmap=colorMap)  # cm.PuBu_r  cm.autumn   cm.gray
            """""

def DrawComb( param ):
    if SvF.DrawMode == '' :  return
    print ('           Draw', param)
    Transp = SvF.DrawTransp
    FONT_SIZE = SvF.FONT_SIZE  #16 #24  # 16 # 7
    NUM_FONT_SIZE = 14
#    axisNUM_FONT_SIZE = 12 #20
    yRotation = 0
    FONTstyle = 'italic'
    fig, ax = plt.subplots(figsize=(SvF.Xsize, SvF.Ysize), dpi=SvF.DPI)
    #fig.tight_layout()
    plt.subplots_adjust(left=SvF.subplots_left, right=SvF.subplots_right,
                        top=SvF.subplots_top, bottom=SvF.subplots_bottom)
    if SvF.CommaFormatter:
        ax.xaxis.set_major_formatter(FuncFormatter(comma_formatter_pos))
        ax.yaxis.set_major_formatter(FuncFormatter(comma_formatter_pos))

    plt.yticks(fontsize=SvF.axisNUM_FONT_SIZE, rotation=0)
    plt.xticks(fontsize=SvF.axisNUM_FONT_SIZE, rotation=0)
    if SvF.xaxis_step != 0:
        ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=SvF.xaxis_step))
    if SvF.yaxis_step != 0:
        ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=SvF.yaxis_step))

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
    MarkerEdgeWidth = 0   # - размер канта (краёв)
    Marker = 'o'
    DataMarker = 'o'
    DataMarkerSize = SvF.DataMarkerSize
    DataLineWidth = 0
    LineWidth = SvF.LineWidth
    LineColor = SvF.LineColor
#    print ("LLL", LineColor )
    LineStyle = '-'
    DataColor = SvF.DataColor
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
 #       print ('part', part)
        for ipar, par in enumerate(part.split(';')) :                  #  Параметры отделяются ;
#        draw_par = part.split(',')
#            print ('par', par, ipar)
            if ipar == 0 :                          # FUN OR PPolyline NAME  or File
                ob = getObjectNotSet(par)   #  Для  drawSvF
#                print ("OOOOOOOOOOOOOOOO")
#                ob.Oprint()
                name = None
                if ob is None:
         #           print ( 'PP', par )
                    if par.find('.sol') >=0 :
                        fun = FunFromSolFile(par)             # FROM Sol FILE
#                        print ("F", fun.grd)
                    elif len (par.split ('.')) > 1:  #  Draw DB.HY   Draw DB.CO2i,DB.Date[:],CO2in Draw E.grd,DB.Date,Emod
                        tabs =  par.split (',')
     #                   print (tabs)
                        p_name = ''
                        x = []; y=[]
                        for nta, ta in enumerate (tabs):
 #                           print ('part of prs', ta)
                            p_tabs = ta.split('.')
                            if len(p_tabs) ==1:
                                p_name = ta
          #                      print ('p_name',ta)
                            else:
                                ob = getObjectNotSet(p_tabs[0])
              #                  print ('ob.Otype',ob.Otype)
                                if ob.Otype == 'Table':
                                    p_name = p_tabs[1]
                                    if nta ==0: y = ob.dat(p_tabs[1])
                                    else:       x = ob.dat(p_tabs[1])
                                elif ob.Otype == 'Fun':                     #  Fun np.array
                                    p_name = ob.V.name
                                    if nta ==0:  y = ob.grd
                                    else:        x = ob.grd
#                                    print('par22222', par, p_tabs,y,x)
                                else:                                   #  из файла  old
#                                    print('par222', par, p_tabs)
                                    #                      fun = FunFromSolFile(par)
                                    tb = Select('* from ' + par)
 #                                   polyline = Polyline(tb.dat('X'), tb.dat('Y'), None, par)
                        if len(y) > 0:
                            if len(x) == 0:  x = [i for i in range(len(y))]
#                            print (len(SvF.Task.Objects))
                            polyline = Polyline(x, y, None, p_name)
                            SvF.Task.Objects = SvF.Task.Objects[1:]     #  чтоб не засорять
 #                           print(len(SvF.Task.Objects))
#                         print ('polXY',polyline.Y, polyline.X, p_name, len(SvF.Task.Objects))
 #                           ob = polyline
                elif ob.Otype == 'Fun': # 'Fun'
                        fun = ob
                else :                  # ob.o_type == 'Polyline':
#                    polyline = ob.object
                    polyline = ob   #&&&&  ???????????

                if not ob is None:  ob.Oprint()

                if fun is None:
                    to_draw = 'Polyline'
                else:
 #                   if fun.type != 'g' and fun.type != 'G':   fun = fun.gClone(True)
                    if fun.type == 'p':   fun = fun.gClone(True)
                    if fun.type == 'smbFun':   fun = fun.gClone(True)
                    to_draw = 'Fun' + str(fun.dim)

            elif par.split(':')[0] == 'L' :  levs = par.split(':')[1].split(',')     # УРОВНИ  отделяются ,
            elif par.split(':')[0] == 'LC':  LineColor = par.split(':')[1]          # Line Col
            elif par.split(':')[0] == 'DC':  DataColor = par.split(':')[1]          # Line Col
            elif par.split(':')[0] == 'DM':  DataMarker = par.split(':')[1]         # DataMarker  = 'o'
            elif par.split(':')[0] == 'DMS': DataMarkerSize = float(par.split(':')[1])   #  DataMarkerSize
            elif par.split(':')[0] == 'DLW': DataLineWidth = float(par.split(':')[1])
            elif par.split(':')[0] == 'LSt': LineStyle = par.split(':')[1]          # Line Style  dotted dashed
            elif par.split(':')[0] == 'LW':  LineWidth = float ( par.split(':')[1] )  # LineWidth
            elif par.split(':')[0] == 'M':   Marker = par.split(':')[1]  # Marker  = 'o'
            elif par.split(':')[0] == 'MC':  MarkerColor = par.split(':')[1]   #  MarkerCol
            elif par.split(':')[0] == 'MS':  MarkerSize = float(par.split(':')[1])   #  MarkerSize
            elif par.split(':')[0] == 'MEC': MarkerEdgeColor = par.split(':')[1]     #  MarkerEdgeColor
            elif par.split(':')[0] == 'MEW': MarkerEdgeWidth = float(par.split(':')[1]) # MarkerEdgeWidth - размер краёв
            elif par.split(':')[0] == 'Name': name = par.split(':')[1].strip('"').strip("'"); # print ("NAME", name, par, len(name))
            elif par.upper() == 'TRANSP'  :  Transp = True
            elif par == 'DrawErr'         :  DrawErr = True
            elif par == 'Flow'            :  Flow = True
#            elif par.split(':')[0] == 'Xstep':
 #               Xstep = float(par.split(':')[1])
  #              ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator (base=Xstep))
            else: print ('Draw  ????????????? ************************ par =', par)
        if not fun is None :
            if  name == None: name = fun.V.name
            if to_draw == 'Fun2' :
                mii, maa = fun.grd_min_max()
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
                            dig = int(np.ceil(-dig))
                            levelFmt = '%.' + str(dig) + 'f'
            V = fun.V
#        ax.set_yscale('log')

        if to_draw == 'Fun0':  # Const
            tb_x = [x_min, x_max]
#            tb_y = [mii, mii]
            tb_y = [fun.grd[0], fun.grd[0]]
            name = fun.V.name
            file_name += name
            ax.plot(tb_x, tb_y, "gray", label=name, linestyle=LineStyle, linewidth=LineWidth, # '-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'
                markersize=MarkerSize, marker='o', markerfacecolor='#FFFFFF')
#            print tb_x, tb_y, "red", V.name
        elif to_draw == 'Fun1':  # LINE
            name = fun.V.name                   # 25/04
            file_name += name
#            print (file_name)
            A = fun.A[0]
            tb_x = A.Val #np.zeros(A.Ub + 1, np.float64)
            tb_y = np.zeros(A.Ub + 1, np.float64)
            for i in A.NodS:   tb_y[i] = fun.grdNaNreal(i)
 #           print (tb_y)
  #          1/0
            x_min = tb_x[0];  x_max = tb_x[-1]

            if not DrawErr:
                if not ((A.dat is None) or (V.dat is None)):                # DRAW  data    #  точки  данные
                    label_name = V.data_name            #  17.07
                    if not SvF.Legend: label_name = ''
       #             if str(type(A.dat)) == '<class \'list\'>' :
        #                Adat = [x + A.min for x in A.dat]
         #           else :
          #              Adat = A.dat + A.min

                    if Transp:
                        plt.plot(V.dat, A.dat, color=DataColor, label=label_name,
                            markersize=DataMarkerSize, marker=DataMarker, markerfacecolor=DataColor, linewidth=DataLineWidth)
                    else:
                        plt.plot(A.dat, V.dat, color = DataColor, label=label_name,
                            markersize=DataMarkerSize, marker=DataMarker, markerfacecolor=DataColor,  linewidth=DataLineWidth)  # markerfacecolor='#FFFFFF' '#000000'
                                                                            # Draw Model  линии модели
                if LineWidth==0 and MarkerSize==0 : label_name = ''
                else :
                    if V.leg_name == '' : V.leg_name = V.oname
      #              label_name = V.oname
#                else                              : label_name = V.draw_name
                if not SvF.Legend: label_name = ''

                if Transp:
#                    ax.plot(tb_y, tb_x, LineColor, label=label_name, linestyle=LineStyle, linewidth=LineWidth,
                    ax.plot(tb_y, tb_x, LineColor, label=V.leg_name, linestyle=LineStyle, linewidth=LineWidth,
                            markersize=MarkerSize, marker='o', markerfacecolor='#FFFFFF')
                else :
#                    ax.plot(tb_x, tb_y, LineColor, label=label_name, linestyle=LineStyle, linewidth=LineWidth,   # function
                    ax.plot(tb_x, tb_y, LineColor, label=V.leg_name, linestyle=LineStyle, linewidth=LineWidth,   # function
                            markersize=MarkerSize, marker='o', #markerfacecolor='#FFFFFF',
                            markerfacecolor = MarkerColor, markeredgecolor=MarkerEdgeColor,
                            markeredgewidth=MarkerEdgeWidth)
            if DrawErr:
                tb_err = deepcopy(V.dat)
                for n in fun.sR:  tb_err[n] = fun.delta(n)
                plt.plot( A.dat, tb_err, LineColor, label=name + 'Err', linewidth=1, #DataColor, #LineWidth,
                     markersize=MarkerSize, marker=Marker, markerfacecolor='#000000')  # markerfacecolor='#FFFFFF'
            if V.axe_name == '': V.axe_name = V.draw_name
            if A.axe_name == '': A.axe_name = A.oname
            if Transp:
                ax.set_xlabel(V.axe_name, size=FONT_SIZE)
                ax.set_ylabel(A.axe_name, size=FONT_SIZE, rotation=yRotation)
            else :
                ax.set_ylabel(V.axe_name, size=FONT_SIZE, rotation=yRotation)
                ax.set_xlabel(A.axe_name, size=FONT_SIZE)

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
                    elif int( (month-1)/ SvF.X_axe_month ) * SvF.X_axe_month == month-1:
                        ticks_lab.append(str(month))
                    else:
                        ticks_lab.append('')
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
            z = np.zeros((Ay.Ub + 1, Ax.Ub + 1), np.float64)

            X, Y = np.meshgrid(x, y)

            if Flow:
                DX, DY = makeDXDY(fun, False)
                mDX = MultVal(DX, -1)
                mDY = MultVal(DY, -1)
                tDX = transpose(mDX.grd)
                tDY = transpose(mDY.grd)
                cs = ax.streamplot(X, Y, tDX, tDY, color='bLack', linewidth=.5, arrowsize=.5)  # 1.6
            else:

                if SvF.printL: print ("z shape", z.shape, Ax.Ub + 1, Ay.Ub + 1)

                for j in Ax.NodS:
                    for i in Ay.NodS:
                        if Transp:      z[i, j] = fun.grdNaNreal (i, j)
                        else:           z[i, j] = fun.grdNaNreal (j, i)
                from matplotlib import ticker, cm

                z = np.ma.masked_where(z <= -9999, z)  #################### NODATA == nan  !!!
                if mii == maa and type(levs) == type(1): levs = [mii - 1, mii, mii + 1]     #28
#                cs = ax.contourf(X, Y, z, levs, locator=ticker.LogLocator(base=2.0), cmap=colorMap)  # cm.PuBu_r  cm.autumn   cm.gray
                cs = ax.contourf(X, Y, z, levs, locator=SvF.locator, cmap=colorMap)  # cm.PuBu_r  cm.autumn   cm.gray
                if SvF.CommaFormatter:
                    ax.clabel(cs, inline=True, fontsize=8, fmt=comma_formatter)

                if (not mii is None) and mii != maa:
                    cs1 = ax.contour(X, Y, z, levs, colors='k', linewidths=0.5)
                    if SvF.CommaFormatter:
                        ax.clabel(cs1, inline=1, fontsize=NUM_FONT_SIZE, fmt=comma_formatter)
                    else :
                        ax.clabel(cs1, inline=1, fontsize=NUM_FONT_SIZE, fmt=levelFmt)   #  сторо !

                if Ax.axe_name == '': Ax.axe_name = Ax.oname
                if Ay.axe_name == '': Ay.axe_name = Ay.oname

                plt.xlabel(Ax.axe_name, fontsize=FONT_SIZE + 1, style=FONTstyle)
                plt.ylabel(Ay.axe_name, fontsize=FONT_SIZE + 1, style=FONTstyle, rotation=yRotation)

                if SvF.Legend :
 #                   leg_name = fun.V.draw_name
  #                  if leg_name == '' : leg_name = fun.onameFun()
   #                 plt.title(leg_name, fontsize=FONT_SIZE + 1, style=FONTstyle, y=1.01, x=SvF.title_x )# , pad = 3)
                    if fun.V.title_name == '' : fun.V.title_name = fun.onameFun()
                    plt.title(fun.V.title_name, fontsize=FONT_SIZE + 1, style=FONTstyle, y=1.01, x=SvF.title_x )# , pad = 3)
                    cbar = plt.colorbar(cs)
                    if SvF.CommaFormatter:
                        cbar.ax.yaxis.set_major_formatter(FuncFormatter(comma_formatter_pos))
          # Data
                if not (Ax.dat is None or Ay.dat is None):
                    plt.plot(Ax.dat, Ay.dat, LineColor, # label="y+",
                         markersize=DataMarkerSize, marker='o', markerfacecolor= MarkerColor,
                         markeredgecolor= MarkerColor, linestyle=LineStyle, linewidth=DataLineWidth)
        else :  #  to_draw == 'Polyline'
                if name == None : name = polyline.name
                print ('Pname',name, MarkerSize)
                if Transp:
                    plt.plot(polyline.Y, polyline.X, LineColor, label=name, markersize=MarkerSize,
                                        marker='o', linewidth=LineWidth, linestyle=LineStyle )
                else:
                    plt.plot(polyline.X, polyline.Y, LineColor, label=name, markersize=MarkerSize,
                         markerfacecolor= MarkerColor, markeredgecolor=MarkerEdgeColor, markeredgewidth = MarkerEdgeWidth,
                         marker=Marker, linewidth=LineWidth, linestyle=LineStyle ) #, fillstyle='none' )
                file_name += name

    if len(SvF.X_lim) != 0: plt.xlim(SvF.X_lim )
    if len(SvF.Y_lim) != 0: plt.ylim(SvF.Y_lim )

    if D2 == False and SvF.Legend:
        ax.legend(fancybox=True, prop={'size': FONT_SIZE}, framealpha=0)  # framealpha -
        #  ax.legend(loc=1, prop={'size': FONT_SIZE})
#    print (file_name + '.'+ SvF.graphic_file_type)

    ax.xaxis.set_label_coords( SvF.Xlabel_x, SvF.Xlabel_y ) #-0.01 ) # SvF.Xlabel_x ) #-0.01)
    ax.yaxis.set_label_coords( SvF.Ylabel_x, SvF.Ylabel_y ) #1.02)  # в длиннах оси

    plt.tight_layout()
    if SvF.DrawMode.find('File') >= 0 :
        if SvF.DrawFileName != '':  file_name = SvF.DrawFileName
        if DrawErr:  plt.savefig(file_name+'Err.' + SvF.graphic_file_type, dpi=SvF.DPI)  # (os.path.join('%s'%dir,'inner_int_gamma_%g%s.%s'%(fun.gamma, suffix, fmt)), dpi = dpi)
        else:        plt.savefig(file_name + '.'+ SvF.graphic_file_type, dpi=SvF.DPI)
    if SvF.DrawMode.find('Screen') >= 0 :
            if SvF.ShowAll :  plt.show(block=False)
            else           :  plt.show()