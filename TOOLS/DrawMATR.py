# -*- coding: cp1251 -*-
#    
#   python DrowMATR+L.py POL(X,Y).sol POL(X,Y).txt -Kol.txt  - mtr  + points + line
import matplotlib.pyplot as plt
from   numpy import *
from   sys import *


import platform
LibVersion = 'Lib25'
if platform.system() == 'Windows':
    path_SvF = "C:/_SvF/"
else :
    path_SvF = "/home/sokol/C/_SvF/"
path.append( path_SvF + LibVersion )
path.append( path_SvF + "Pyomo_Everest/pe" )
import COMMON as co
co.path_SvF = path_SvF
co.tmpFileDir = co.path_SvF + 'TMP/'


from  Tools import *
from  InData import ReadSolInf 
from  GIS   import *
from  Lego  import *


len_argv = len(argv)


####################################

MULT = 2

FONT_SIZE = 8;    FONT_SIZE *= MULT
FONTstyle = 'italic'
#dpiMy = 300
dpiMy = 100
figsizeX = 4
figsizeY = 2
Proportional = True
#Proportional = False
diagonal = 10
#fig, ax = plt.subplots(figsize=(figsizeX,figsizeY), dpi=dpiMy)
levelFmt = '%.3f'
levelFmt = '%.0f'
#levs     = 10
levs     = [-50, -20, 0, 50,100,200,300,400,500, 600]
#colorMap = 'binary'
#colorMap = 'gray'  
#colorMap = 'PuBu'
colorMap = 'Wistia_r'
#Transp   = True
Transp   = False

#    colors = [ "g+", "b+", "r+", "m+", "y+", "g+", "b+", "r+", "m+", "y+" ]
colrs = [ "b+", 'r+', 'b', 'r+', 'r+', 'brown',"black","gray","black","black",  "r+", "m+", "y+", "g+", "b+", "r+", "m+", "y+" ]
colr = 0



if len(argv) == 1 :
#     argv.append ('MU(X,Y).sol')
     argv.append ('POL(X,Y).sol')
print argv

     #####################################

cols, xp, yp, tb = ReadSolInf ( argv[1], 1 )
if len (xp) == 0:  f_type = 'tbl'
else            :  f_type = 'matr2'
            
if f_type == 'matr2' :    ################################### MATR
    from numpy import ma
    from matplotlib import colors, ticker, cm
    from matplotlib.mlab import bivariate_normal

    for iarg, arg in enumerate(argv) :
        if iarg == 0 : continue  
        if iarg == 1 :           ### first  matr file        
            print "shape", tb.shape
            print 'mmx', xp[0], xp[-1]
            print 'mmy', yp[0], yp[-1]
            if levelFmt == '' :    # сколько цифр оставлять after .
                minV = +1e34
                maxV = -1e34
                for j in range(tb.shape[0]) :
                   for i in range(tb.shape[1]) :
                     if maxV < tb[j,i] :  maxV = tb[j,i]
                     if minV > tb[j,i] :  minV = tb[j,i]
                delen = int ( floor ( log10( (maxV-minV)/10) ) )
                print maxV, minV, delen
                if delen >= 0 : levelFmt = '%f'
                else :
                    levelFmt = '%.'+str(-delen)+'f'
            print   'levelFmt', levelFmt 

            if Proportional:
                d_y =  xp[-1]-xp[0]
                d_x =  yp[-1]-yp[0]
                print 'd_x d_y', d_x, d_y
                d_xy = sqrt (d_x**2+d_y**2)
                figsizeX = diagonal/d_xy * d_x #* 1.2
                figsizeY = diagonal/d_xy * d_y *1.5 
                print "figsizeX,figsizeY", figsizeX,figsizeY

            fig, ax = plt.subplots(figsize=(figsizeX,figsizeY), dpi=dpiMy)

            if Transp :
                y = linspace(xp[0], xp[-1], len(xp) )
                x = linspace(yp[0], yp[-1], len(yp) )
            else :    
                x = linspace(xp[0], xp[-1], len(xp) )
                y = linspace(yp[0], yp[-1], len(yp) )

            X, Y = meshgrid(x, y)
            z = (bivariate_normal(X, Y, 0.1, 0.2, 1.0, 1.0)
                 + 0.1 * bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0))

            print "z.shape", z.shape

            for j in range(tb.shape[0]) :
                for i in range(tb.shape[1]) :
                    if Transp :  z[i,j] = tb[j,i]
                    else      :  z[j,i] = tb[j,i]
            z = ma.masked_where(z <= -9999, z)    #################### NODATA

            # Automatic selection of levels works; setting the
            # log locator tells contourf to use a log scale:
            #    cs =ax.contourf(X, Y, z, levs, cmap=colorMap)#cm.PuBu_r) # string of SOKOLOVSKY
            #==============================================================================
#            cs = plt.contourf(X, Y, z, levs, cmap=cm.PuBu) #from red to yellow
#            cs = plt.contourf(X, Y, z, levs, cmap=cm.autumn_r) #from red to yellow
            cs = plt.contourf(X, Y, z, levs, cmap=colorMap ) ###cmap=cm.Reds_r) 
#            cs = plt.contourf(X, Y, z, levs, cmap=cm.gray) #gray
            cbar = plt.colorbar(cs)

            cs1 = ax.contour(X, Y, z, levs, colors='k',  linewidths=0.5)
            ax.clabel(cs1, inline=1, fontsize=FONT_SIZE, fmt = levelFmt)

            #    plt.xlabel(first_line[1], ha='left', va = 'top', fontsize=FONT_SIZE+1)
            if Transp:
                plt.xlabel(cols[1], fontsize=FONT_SIZE+1,style=FONTstyle)
                plt.ylabel(cols[0], fontsize=FONT_SIZE+1,style=FONTstyle)
            else :        
                plt.ylabel(cols[1], fontsize=FONT_SIZE+1,style=FONTstyle)
                plt.xlabel(cols[0], fontsize=FONT_SIZE+1,style=FONTstyle)
            ax.xaxis.set_label_coords(1.02, -0.025)
            ax.yaxis.set_label_coords(-0.025, 1.05)
            plt.title(cols[2]+'('+cols[0]+','+cols[1]+')',fontsize=FONT_SIZE+1,style=FONTstyle)
            #=================== END Of FIRST File =========================================

            #cs = plt.contourf(X, Y, z, locator=ticker.LogLocator(), cmap=cm.PuBu_r)

            # Alternatively, you can manually set the levels
            # and the norm:
            #lev_exp = np.arange(np.floor(np.log10(z.min())-1),
            #                    np.ceil(np.log10(z.max())+1))
            #levs = np.power(10, lev_exp)
            #cs = P.contourf(X, Y, z, levs, norm=colors.LogNorm())

            # The 'extend' kwarg does not work yet with a log scale.

        else :
            if arg[0] == '-':
                lw = 0.5
                ms = 0
                arg = arg[1:]
            else :
                lw = 0
                ms = 2.5
            ftype, vers, colsX, x1, tbG = ReadSvF ( arg, 1 )
            print 'GRAF shape', tbG.shape
            if Transp :
                plt.plot ( tbG[:,1],tbG[:,0],colrs[colr], label="green+", markersize=ms*MULT, marker='o',  linestyle='-', linewidth=lw*MULT )
            else      :
                plt.plot ( tbG[:,0],tbG[:,1],colrs[colr], label="green+", markersize=ms*MULT, marker='o',  linestyle='-', linewidth=lw*MULT )
            colr += 1
#            print '|'+colrs[colr]+'|'
#    print 'OOO', ax.get_xlim()

    plt.savefig(argv[1] + '.png')  #(os.path.join('%s'%dir,'inner_int_gamma_%g%s.%s'%(self.gamma, suffix, fmt)), dpi = dpi)
    plt.show()
    exit
#    return

#############  ColorLev   ###########################

    if len (InColLev) > 0:
         Cs = Read_gFun2 (InColLev) 
         tCs = transpose(Cs.grd)
#    cs =ax.contourf(X, Y, z, levs, cmap=colorMap)#cm.PuBu_r) # string of SOKOLOVSKY
         cs =ax.contourf(X, Y, tCs, levs, cmap=colorMap)#cm.PuBu_r) # string of SOKOLOVSKY
         cbar = plt.colorbar(cs)
         ticklabs = cbar.ax.get_yticklabels()
         cbar.ax.set_yticklabels(ticklabs, fontsize=FONT_SIZE)

############  STREAM   ###########################

    if len (InH) :
          H = Read_gFun2 ( InH );  H.param = True
          DX, DY = makeDXDY(H)
          mDX = MultVal (DX,-1)
          mDY = MultVal (DY,-1)
          tDX = transpose(mDX.grd)
          tDY = transpose(mDY.grd)
          strm = plt.streamplot(X, Y, tDX, tDY, color='k', linewidth=0.3, arrowsize=0.6 )
#arrowstyle : str

    

    #  ADDITIONAL POINTS   ###########################

    if len(argv) > 2 :
        InG = argv[2]
        ftype, vers, colsX, x1, tbG = ReadSvF ( InG, 1 )
        print 'POINTS shape', tbG.shape
        if Transp :
            plt.plot ( tbG[:,1], tbG[:,0], 'b+', label="green+", markersize=5*MULT, marker='o' )
        else      :
            plt.plot ( tbG[:,0], tbG[:,1], 'b+', label="green+", markersize=5*MULT, marker='o' )

    #  ADDITIONAL Line   ###########################

    if len(InPol) > 0 :
        ftype, vers, colsX, x1, tbG = ReadSvF ( InPol, 1 )
#        for e in tbG : e = e *0.001  
        tbG = tbG * 0.001
        print 'Line shape', tbG.shape
        if Transp :
            plt.plot ( tbG[:,1], tbG[:,0], 'r+', label="m+", markersize=0.3*MULT, marker='o', linewidth=1, linestyle='-' )
        else      :
            plt.plot ( tbG[:,0], tbG[:,1], 'r+', label="m+", markersize=0.25*MULT, marker='o', linewidth=1, linestyle='-' )
    
#    cbar = plt.colorbar(cs)

   
else :  # f_type = 'tbl'

    import math
    fig, ax = plt.subplots(figsize=(figsizeX,figsizeY), dpi=dpiMy)



    for f in range ( 0,len_argv-1 ) :                   # цикл по файлам
        if f > 0 : In  = argv[f+1]
        print "from " + In
        partIn = In.split('#')
        print len(partIn)
        if len(partIn)==2 :    #   если есть #
            In = partIn[0]     #   считываем 
            fi = open ( In )
            cols = fi.readline().split()
            xp = fi.readline().split()
            print "len(xp)", len(xp)
            tb = loadtxt (fi,'double')
            fi.close()
            print "tb.shape ", tb.shape

            print partIn[1]
        
            partComma = partIn[1].split(',')
            for part in partComma :
              from_to  = part.split(':')
              if len (from_to) < 2 : Fr = int(part); To = Fr
              else :
                Fr = 0;  To = tb.shape[0]-1            
                if len(from_to[0]) > 0 : Fr = int(from_to[0])
                if len(from_to[1]) > 0 : To = int(from_to[1])
              tbl = zeros( (len(xp),2), float64)

              print Fr, To
              for r in range (Fr,To+1):
                print 'r', r
                for c in range (len(xp)):  tbl[c,0] = float(xp[c])
                tbl[:,1] = tb[r,1:]
                for g in range (1,tbl.shape[1]) :
                    ax.plot ( tbl[:,0], tbl[:,1], colors[color],
                              label=cols[2]+' '+cols[1]+'='+str(tb[r,0]), markersize=4 )
                    color = color + 1
                    if color >= len (colors) : color = 0
                ax.set_ylabel(cols[2])
                ax.set_xlabel(cols[0])
                ax.legend()

        else :               #  просто файл
            fi = open ( In )
            cols = fi.readline().split()
            tbl = loadtxt (fi,'double')
            fi.close()
            print "tbl.shape ", tbl.shape


            for g in range (1,tbl.shape[1]) :

                if color == 1 : color = 2; continue

                if Transp :
                    tbl_x = tbl[:,g]
                    tbl_y = tbl[:,0]
                else      :
                    tbl_y = tbl[:,g]
                    tbl_x = tbl[:,0]
                if color ==0 :
                    ax.plot ( tbl_x, tbl_y, colors[color], label=cols[g],  linestyle='-', linewidth=0.5, \
                              markersize=0.5, marker='o', markerfacecolor='#FFFFFF' )
                elif color == 1 :
                    ax.plot ( tbl_x, tbl_y, colors[color], label=cols[g], linestyle=':', linewidth=0, markersize=0, marker='o' )
                elif color == 2 :
                    ax.plot ( tbl_x, tbl_y, colors[color], label=cols[g], linestyle='-', linewidth=0, markersize=0.25, marker='o' )
                else :    
                    ax.plot ( tbl_x, tbl_y, colors[color], label=cols[g], markersize=2, marker='o', linewidth=0 )
                color = color + 1
                if color >= len (colors) : color = 0
#            ax.set_ylabel(cols[1], size=16)
            ax.set_ylabel(cols[1], size=FONT_SIZE)
            ax.set_xlabel(cols[0], size=FONT_SIZE)
            ax.xaxis.set_label_coords(1.05, -0.025)
            ax.yaxis.set_label_coords(-0.025, 1.)

            ax.legend(loc=1, prop={'size': FONT_SIZE})
for tick in ax.xaxis.get_major_ticks():
                tick.label.set_fontsize(FONT_SIZE) 
for tick in ax.yaxis.get_major_ticks():
                tick.label.set_fontsize(FONT_SIZE) 
#                tick.label.set_rotation('vertical')
            


