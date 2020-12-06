# -*- coding: cp1251 -*-
#    DRAW_XY   F(X,Y).sol   10  - РєРѕР»-РІРѕ СѓСЂРѕРІРЅРµР№

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


from Tools import *


len_argv = len(argv)
if len_argv >1 :  In = argv[1]      # first File with data 


####################################

MULT = 2

FONT_SIZE = 8;    FONT_SIZE *= MULT

FONTstyle = 'italic'
#fig, ax = plt.subplots(figsize=(3,2.5), dpi=300)
fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))

levelFmt = '%.2f'
levs     = 10
colorMap = 'binary'
#colorMap = 'gray'  
#colorMap = 'PuBu'
#Transp   = True
Transp   = False

if len_argv == 1 :
#    In = "POL(X,Y).sol";   len_argv = 2;   InG = "POL(X,Y).txt"      # dop points on 3D
#    In = "Cu(YearPb).txt"; len_argv = 2
#     In = "BE2(dir,vel).sol";   len_argv = 2;
     In = "Bor(dir360).sol";   len_argv = 2;
#####################################




f_type = 'tbl'
if In.count('#') == 0 :
    with open(In, "r") as fi:
        first_line = fi.readline().split()
        print "Read from", In,  first_line
        if first_line[-1][0:1] == '#' :
            if first_line[-1].count('matr2') == 1 : f_type = 'matr2'
            
if f_type == 'matr2' :
    from numpy import ma
    from matplotlib import colors, ticker, cm
    from matplotlib.mlab import bivariate_normal

    # Number of contours  
#    if len(argv) > 2 : levs = int(argv[2])
    # fmt  
 #   if len(argv) > 3 : levelFmt = str(argv[3])
    # Color maps  
    # see http://matplotlib.org/examples/color/colormaps_reference.html
  #  if len(argv) > 4 : colorMap = str(argv[4])

    print len(argv), In, levs

    with open(In, "r") as fi:
        first_line = fi.readline().split()
        print "ReadSol from", In,  first_line
        xp = fi.readline().split()
        print xp
        print "len(xp)", len(xp)
        tb = loadtxt (fi,'double')

    for fi in range(len(xp)) :
        xp[fi] = radians(-(float(xp[fi])-90))   ###########  Rose



    if levelFmt == '' :    # сколько цифр оставлять after .
        minV = +1e34
        maxV = -1e34
        for j in range(tb.shape[0]) :
            for i in range(tb.shape[1]-1) :
                if maxV < tb[j,i+1] :  maxV = tb[j,i+1]
                if minV > tb[j,i+1] :  minV = tb[j,i+1]
        delen = int ( floor ( log10( (maxV-minV)/10) ) )
        print maxV, minV, delen
        if delen >= 0 : levelFmt = '%f'
        else :
            levelFmt = '%.'+str(-delen)+'f'
    print   levelFmt 

    print "shape", tb.shape
    print 'mmx', float(xp[0]), float(xp[-1])
    print 'mmy', tb[0,0],      tb[-1,0]

    if Transp :
        y = linspace(float(xp[0]), float(xp[-1]), len(xp)    )
        x = linspace(     tb[0,0],      tb[-1,0], tb.shape[0])
    else :    
        x = linspace(float(xp[0]), float(xp[-1]), len(xp)    )
        y = linspace(     tb[0,0],      tb[-1,0], tb.shape[0])

    X, Y = meshgrid(x, y)

    # A low hump with a spike coming out of the top right.
    # Needs to have z/colour axis on a log scale so we see both hump and spike.
    # linear scale only shows the spike.
    z = (bivariate_normal(X, Y, 0.1, 0.2, 1.0, 1.0)
         + 0.1 * bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0))

    print "shape", z.shape

    for j in range(tb.shape[0]) :
        for i in range(tb.shape[1]-1) :
            if Transp :  z[i,j] = tb[j,i+1]
            else      :  z[j,i] = tb[j,i+1]

    # The following is not strictly essential, but it will eliminate
    # a warning.  Comment it out to see the warning.
    z = ma.masked_where(z <= -9999, z)    #################### NODATA

    # Automatic selection of levels works; setting the
    # log locator tells contourf to use a log scale:

    cs =ax.contourf(X, Y, z, levs, cmap=colorMap)#cm.PuBu_r) # string of SOKOLOVSKY
    #==============================================================================

    #cs = plt.contourf(X, Y, z, levs, cmap=cm.autumn) #from red to yellow
    #cs = plt.contourf(X, Y, z, levs, cmap=cm.gray) #gray

    cs1 = ax.contour(X, Y, z, levs, colors='k',  linewidths=0.5)
    ax.clabel(cs1, inline=1, fontsize=FONT_SIZE, fmt = levelFmt)

#    plt.xlabel(first_line[1], ha='left', va = 'top', fontsize=FONT_SIZE+1)
    if Transp:
        plt.xlabel(first_line[1], fontsize=FONT_SIZE+1,style=FONTstyle)
        plt.ylabel(first_line[0], fontsize=FONT_SIZE+1,style=FONTstyle)
    else :        
        plt.ylabel(first_line[1], fontsize=FONT_SIZE+1,style=FONTstyle)
        plt.xlabel(first_line[0], fontsize=FONT_SIZE+1,style=FONTstyle)
    ax.xaxis.set_label_coords(1.0, -0.025)
    ax.yaxis.set_label_coords(-0.025, 1.)
    plt.title(first_line[2]+'('+first_line[0]+','+first_line[1]+')',fontsize=FONT_SIZE+1,style=FONTstyle)
    #==============================================================================

    #cs = plt.contourf(X, Y, z, locator=ticker.LogLocator(), cmap=cm.PuBu_r)

    # Alternatively, you can manually set the levels
    # and the norm:
    #lev_exp = np.arange(np.floor(np.log10(z.min())-1),
    #                    np.ceil(np.log10(z.max())+1))
    #levs = np.power(10, lev_exp)
    #cs = P.contourf(X, Y, z, levs, norm=colors.LogNorm())

    # The 'extend' kwarg does not work yet with a log scale.

    cbar = plt.colorbar(cs)

    ticklabs = cbar.ax.get_yticklabels()
    cbar.ax.set_yticklabels(ticklabs, fontsize=FONT_SIZE)    

    #  ADDITIONAL POINTS   ###########################

    if len(argv) > 2 :
        InG = argv[2]
        ftype, vers, colsX, x1, tbG = ReadSvF ( InG, 1 )
        print 'GRAF shape', tbG.shape
        if Transp :
            plt.plot ( tbG[:,1], tbG[:,0], 'b+', label="m+", markersize=0.05, marker='+' )
        else      :
            plt.plot ( tbG[:,0], tbG[:,1], 'b+', label="m+", markersize=0.05, marker='+' )
    
#    cbar = plt.colorbar(cs)

   
else :  # f_type = 'tbl'

    import math
    print  'tbl'

#    colors = [ "r+", "b+", "r+", "m+", "y+", "g+", "b+", "r+", "m+", "y+" ]
    colors = [ "r+","black","gray","black","black", "b+", "r+", "m+", "y+", "g+", "b+", "r+", "m+", "y+" ]
    color = 0

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
                if Transp :
                    tbl_x = tbl[:,g]
                    tbl_y =  radians(-(tbl[:,0]-90))
                else      :
                    tbl_y = tbl[:,g]
                    tbl_x =  radians(-(tbl[:,0]-90))
                if color ==0 :
                    ax.plot ( tbl_x, tbl_y, colors[color], label=cols[g],  linestyle='-', linewidth=0.5*MULT, \
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
#            ax.set_ylabel(cols[1], size=FONT_SIZE)
 #           ax.set_xlabel(cols[0], size=FONT_SIZE)
  #          ax.xaxis.set_label_coords(1.05, -0.025)
   #         ax.yaxis.set_label_coords(-0.025, 1.)

            ax.legend(loc=1, prop={'size': FONT_SIZE})
for tick in ax.xaxis.get_major_ticks():
                tick.label.set_fontsize(FONT_SIZE) 
for tick in ax.yaxis.get_major_ticks():
                tick.label.set_fontsize(FONT_SIZE) 
#                tick.label.set_rotation('vertical')
            

plt.savefig(In + '.png')  #(os.path.join('%s'%dir,'inner_int_gamma_%g%s.%s'%(self.gamma, suffix, fmt)), dpi = dpi)


plt.show()


