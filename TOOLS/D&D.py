# -*- coding: cp1251 -*-
#    DRAW_XY   F(X,Y).sol   10  - РєРѕР»-РІРѕ СѓСЂРѕРІРЅРµР№

from   sys import *
import matplotlib.pyplot as plt
from   numpy import *


len_argv = len(argv)

# first File with data 
if len_argv >1 :  In = argv[1]
#else             :  In = "I(t).sol"; len_argv = 2
else             :  In = "F(X,Y).sol"; len_argv = 2

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
    if len(argv) > 2 : levs = int(argv[2])
    else            : levs = 10
    # fmt  
    if len(argv) > 3 : levelFmt = str(argv[3])
    else            : levelFmt = '' #'%.1f'
    # Color maps  
    # see http://matplotlib.org/examples/color/colormaps_reference.html
    if len(argv) > 4 : colorMap = str(argv[4])
    else            : colorMap = 'PuBu'

    print len(argv), In, levs

    with open(In, "r") as fi:
        first_line = fi.readline().split()
        print "ReadSol from", In,  first_line
        xp = fi.readline().split()
        print xp
        print "len(xp)", len(xp)
        tb = loadtxt (fi,'double')


    if levelFmt == '' :    # сколько цифр оставлять after .
        minV = +1e34
        maxV = -1e34
        for j in range(tb.shape[0]) :
            for i in range(tb.shape[1]-1) :
                if maxV < tb[j,i+1] :  maxV = tb[j,i+1]
                if minV > tb[j,i+1] :  minV = tb[j,i+1]
        delen = int ( floor ( log10( (maxV-minV)/10) ) )
#        delen = int ( floor ( log10( (maxV-minV)/10) ) ) - 1
        print maxV, minV, delen
        if delen >= 0 : levelFmt = '%f'
        else :
            levelFmt = '%.'+str(-delen)+'f'
    print   levelFmt 

    print "shape", tb.shape
    print 'mmx', float(xp[0]), float(xp[-1])
    print 'mmy', tb[0,0],      tb[-1,0]

    y = linspace(float(xp[0]), float(xp[-1]), len(xp)    )
    x = linspace(     tb[0,0],      tb[-1,0], tb.shape[0])

    X, Y = meshgrid(x, y)

    # A low hump with a spike coming out of the top right.
    # Needs to have z/colour axis on a log scale so we see both hump and spike.
    # linear scale only shows the spike.
    z = (bivariate_normal(X, Y, 0.1, 0.2, 1.0, 1.0)
         + 0.1 * bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0))

    print "shape", z.shape

    for j in range(tb.shape[0]) :
        for i in range(tb.shape[1]-1) :
            z[i,j] = tb[j,i+1]

    # The following is not strictly essential, but it will eliminate
    # a warning.  Comment it out to see the warning.
    z = ma.masked_where(z <= -9999, z)    #################### NODATA

    # Automatic selection of levels works; setting the
    # log locator tells contourf to use a log scale:

    cs = plt.contourf(X, Y, z, levs, cmap=colorMap)#cm.PuBu_r) # string of SOKOLOVSKY
    #==============================================================================

    #cs = plt.contourf(X, Y, z, levs, cmap=cm.autumn) #from red to yellow
    #cs = plt.contourf(X, Y, z, levs, cmap=cm.gray) #gray

    cs1 = plt.contour(X, Y, z, levs, colors='k')
    plt.clabel(cs1, inline=1, fontsize=10, fmt = levelFmt)

    plt.xlabel(first_line[1],fontsize=15)
    plt.ylabel(first_line[0],fontsize=15)
    plt.title(first_line[2],fontsize=20)
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

   
else :  # f_type = 'tbl'

    import math
    from matplotlib import mlab

    fig, ax = plt.subplots()
    colors = [ "g+", "b+", "r+", "m+", "y+", "g+", "b+", "r+", "m+", "y+" ]
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
                ax.plot ( tbl[:,0], tbl[:,g], colors[color], label=cols[g], markersize=4 )
                color = color + 1
                if color >= len (colors) : color = 0
            ax.set_ylabel(cols[1])
            ax.set_xlabel(cols[0])
            ax.legend()

plt.savefig(In + '.png')  #(os.path.join('%s'%dir,'inner_int_gamma_%g%s.%s'%(self.gamma, suffix, fmt)), dpi = dpi)


plt.show()


