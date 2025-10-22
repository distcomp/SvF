# -*- coding: UTF-8 -*-

from __future__ import division
#from   numpy import *
#from   pyomo.environ import *
import pyomo.environ as py
#import matplotlib.pyplot as plt
from   os.path  import *

from sympy import false

#import sys

from Object import *
import os.path

from Vari      import *     # 30

from GridArgs import *
from Pars        import *
from InData import *
from Polynome import * 

from   copy   import *
from   shutil import move
import Table as Tab



def str_val (val) :
    if np.isnan(val) : return 'nan'
    return "%20.16g" % (val)



def cnstrFun2 (args, V_name, NDT) :   #
    from Lego import Fun
    fu = Func()     #   Устарело! Надо заменить!
    fu.dim = 2
 #   print ('*******************',fu.name)
  #  1/0
    fu.param = True
    fu.NDT = NDT
    fu.V = Vari (V_name)
    fu.A.append(args[0]);  fu.A[0].setUb();   fu.A[0].makeSets()
    fu.A.append(args[1]);  fu.A[1].setUb();   fu.A[1].makeSets()
    ret =  gFun2 (fu)    #Fun ()  #   Устарело!
    ret.A[0].Aprint()
    ret.A[1].Aprint()
    ret.grd = np.zeros((ret.A[0].Ub + 1, ret.A[1].Ub + 1), np.float64)
    return ret




#def Read_gFun1 ( ReadFrom ) :      #  outofdate  27
#def Read_gFun2 ( ReadFrom ) :      #  outofdate  27

def oFunFromSolFile(ReadFrom, Vnum=1):  # для tbl   нулевая  колонка - аргумент. по умолчанию первая функция
    if SvF.printL: print ('FunFromFile', ReadFrom)
    with open(ReadFrom, "r") as fi:
        ret_fun = Fun()
        ret_fun.param = True
        #            fnames = fi.readline().split()
        head = fi.readline()
        Ver, Typ, cols = Get_Ver_Typ_cols(head)

        if Typ == 'tbl':
            ret_fun.dim = 1
            ret_fun.V = Vari(cols[Vnum])   # для tbl   нулевая  колонка - аргумент. Vnum - функция
        else:
            ret_fun.dim = 2
            ret_fun.V = Vari(cols[-1])
        #          dim   = len (fnames) - 2
        #            ret_fun.dim   = dim
 #       ret_fun.V = Vari(cols[Vnum])
        #            if SvF.printL :
        #           print "Read from", ReadFrom, cols, 'dim=', ret_fun.dim
        tmp_currentTab = SvF.currentTab  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  ###
        SvF.currentTab = None
        if ret_fun.dim == 1:
            tb = np.loadtxt(fi, 'double')
            ret_fun.A = [Set(cols[0], tb[0][0], tb[-1][0], -(tb.shape[0] - 1))]
            ret_fun.grd = np.zeros(ret_fun.A[0].Ub + 1, np.float64)
            for x in ret_fun.A[0].NodS:
                ret_fun.A[0].Val[x] = tb[x][0]
                ret_fun.grd[x] = tb[x][Vnum]
        #                ret_fun.grd = ravel( np.delete (tb, range(0,1), 1 ) )
        #                for x in ret_fun.A[0].NodS :
        #                       ret_fun.A[0].Val[x] = tb[x][0]
        #                        ret_fun.grd[x]      = tb[x][1]
        #                return  ret_fun

        elif ret_fun.dim == 2:
            x_gr = fi.readline().split()
            tb = np.loadtxt(fi, 'double')
            if len(tb.shape) == 1:
#                print ("SSSSSSSSSSSSSSSSSSSSSSSSS", tb.shape[0])
                tb = reshape(tb, (1, tb.shape[0]))
#                print ("SSSSSSSSS", tb.shape[0], tb.shape[1])
                print (tb)
            ret_fun.A = [Set(cols[0], float(x_gr[0]), float(x_gr[-1]), -(len(x_gr) - 1)),
                         Set(cols[1], tb[0][0], tb[-1][0], -(tb.shape[0] - 1))]
            ###                ret_fun.A = [ Grid ( fnames[0], float(x_gr[0]), float(x_gr[-1]), -(len (x_gr)-1) ),
            ###                           Grid ( fnames[1], tb[ 0][0],      tb[-1][0],       -(tb.shape[0]-1) ) ]
            #                ret_fun.A = [ Arg ( fnames[0], -(len (x_gr)-1), float(x_gr[0]), float(x_gr[-1]) ),
            #                             Arg ( fnames[1], -(tb.shape[0]-1), tb[ 0][0], tb[-1][0] ) ]
            for x in ret_fun.A[0].NodS:  ret_fun.A[0].Val[x] = float(x_gr[x])
            for x in ret_fun.A[1].NodS:  ret_fun.A[1].Val[x] = tb[x][0]
            ret_fun.grd = np.delete(tb, range(0, 1), 1).transpose()
        SvF.currentTab = tmp_currentTab
        return ret_fun

    #      except IOError as e:
    print ("**********************не удалось открыть файл  !" + ReadFrom + '!')
    return None;


def FunFromSolFile(ReadFrom, AddObj = False):
    if SvF.printL: print ('FunFromSolFile', ReadFrom)
    root, ext = splitext(ReadFrom.upper())
    if '.ASC' == ext:
        cols, xp, yp, grd = ReadSetInf(ReadFrom)
    else:
        cols, xp, yp, grd = ReadSolInf(ReadFrom)

#    print 'BBB', grd.shape
    from Lego import Fun
    if AddObj :
        ret_fun = Fun(cols[-1])
    else :
        ret_fun = Fun('')
        ret_fun.V = Vari(cols[-1])
    if len(xp) == 0 and len(yp) == 0: ret_fun.dim = 0
    elif len(xp) == 0:                ret_fun.dim = 1
    else:                             ret_fun.dim = 2
    ret_fun.param = True
    ret_fun.V = Vari(cols[-1])

    tmp_currentTab = SvF.currentTab  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  ###
    SvF.currentTab = None
    if ret_fun.dim == 0:
        ret_fun.A = []
        ret_fun.grd = grd    #  бросил надоело ...
    elif ret_fun.dim == 1:
            ret_fun.A = [Set(cols[0], yp[0], yp[-1], -(len(yp) - 1))]
            ret_fun.grd = grd
    elif ret_fun.dim == 2:
            ret_fun.A = [Set(cols[0], xp[0], xp[-1], -(len(xp) - 1)),
                         Set(cols[1], yp[0], yp[-1], -(len(yp) - 1))]
            ret_fun.grd = grd.transpose()  # np.delete(tb, range(0, 1), 1).transpose()
    SvF.currentTab = tmp_currentTab
    ret_fun.set_gr_grd_or_var()
    return ret_fun



def FunFromFileNew ( ReadFrom, Vnum = 1, AddObj = False ) :    #  для tbl  нулевая колонка - аргумент. по умолчанию первая функция
        if SvF.printL : print ('FunFromFile', ReadFrom)
        root, ext = splitext(ReadFrom.upper())
        if '.ASC' == ext or \
           '.SOL' == ext :
            return FunFromSolFile(ReadFrom, AddObj)
#            cols, x1, x2, tb = ReadGridInf(ReadFrom)
        else:
            cols, x1, x2, tb = ReadSolInf ( ReadFrom )    # только для dim==1
        if AddObj:
            ret_fun = Fun(cols[Vnum])
        else:
            ret_fun = Fun('')
            ret_fun.V = Vari(cols[Vnum])
#        ret_fun = Fun()
        if len ( x2 ) == 0 :  ret_fun.dim = 1
        else               :  ret_fun.dim = 2
        ret_fun.param = True
#        ret_fun.V     = Vari ( cols[Vnum] )

        tmp_currentTab = SvF.currentTab  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  ###
        SvF.currentTab = None
        if ret_fun.dim == 1:
            ret_fun.A = [Set(cols[0], tb[0][0], tb[-1][0], -(tb.shape[0] - 1))]
            ret_fun.grd = np.zeros(ret_fun.A[0].Ub + 1, np.float64)
            for x in ret_fun.A[0].NodS:
###                ret_fun.A[0].Val[x] = tb[x][0]
                ret_fun.grd[x] = tb[x][Vnum]
        elif ret_fun.dim == 2:
            ret_fun.A = [Set(cols[0], float(x1[0]), float(x1[-1]), -(len(x1) - 1)),
                         Set(cols[1], x2[0], x2[-1], -(len(x2) - 1))]
            ret_fun.grd = tb
#            print (tb.shape)
        SvF.currentTab = tmp_currentTab
        return ret_fun

##### ********************************************************** #######
