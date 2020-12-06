# -*- coding: UTF-8 -*-

from __future__ import division
from   numpy import *
from   pyomo.environ import *
import matplotlib.pyplot as plt
from   os.path  import *
#import sys

import os.path



from GridVarArgs import *
from Pars        import *
from InData import *
from Polynome import * 

#import copy
from   copy   import *
from   shutil import move
#from   PyomoEverestEnv import *
import Table as Tab

import COMMON as co



def str_val (val) :
    if isnan(val) : return 'nan'
    return "%20.16g" % (val)


#  GRID 2  *************************************************************
def cnstrFun2 (args, V_name, NDT) :   #
    fu = Func()
    fu.dim = 2
    fu.param = True
    fu.NDT = NDT
    fu.V = Vari (V_name)
    fu.A.append(args[0]);  fu.A[0].setUb();   fu.A[0].makeSets()
    fu.A.append(args[1]);  fu.A[1].setUb();   fu.A[1].makeSets()
    ret =  gFun2 (fu)    #Fun ()
    ret.A[0].Aprint()
    ret.A[1].Aprint()
    ret.grd = zeros((ret.A[0].Ub + 1, ret.A[1].Ub + 1), float64)
    return ret




def Read_gFun1 ( ReadFrom ) :      #  outofdate  27
      try:
            fi = open ( ReadFrom, "r")
      except IOError as e:
            print ("*********************не удалось открыть файл  !"+ReadFrom+'!')
            return  None;
      else:
        fnames = fi.readline().split()
        print ("Read_gFun1 from", ReadFrom,  fnames,)
        tb = loadtxt (fi,'double')
        fi.close()
#        print "shape", tb.shape

        V = Vari ( fnames[1] )
#        A1 = Arg ( fnames[0] )
        A1 = Grid ( fnames[0] )
        A1.Ub = tb.shape[0] - 1
        A1.min = tb[ 0][0]
        A1.max = tb[-1][0]
        A1.step = (A1.max-A1.min)/(A1.Ub)
        A1.Aprint()

        A1.Normalization_UbSets(0)

        tb1 = zeros( A1.Ub+1, float64 )
        for x in range(A1.Ub+1) : tb1[x] = tb[x][1]

        fun1     = Func()
        fun1.grd = tb1
        fun1.V   = V
        fun1.A   = [A1]
        fun1.dim = 1
        return gFun1( fun1 ) 




def Read_gFun2 ( ReadFrom ) :      #  outofdate  27
      try:
            fi = open ( ReadFrom, "r")
      except IOError as e:
            print ("не удалось открыть файл  !"+ReadFrom+'!')
            return None;
      else:
        fnames = fi.readline().split()
        print ("Read_gFun2 from", ReadFrom,  fnames,)
        x_gr = fi.readline().split()
        tb = loadtxt (fi,'double')
        fi.close()
#        print "shape", tb.shape

        V = Vari ( fnames[2] )

        A1 = Grid ( fnames[0] )
#        A1 = Arg ( fnames[0] )
        A1.Ub = len (x_gr) - 1
        A1.min = float(x_gr[0])
        A1.max = float(x_gr[-1])
        A1.step = (A1.max-A1.min)/(A1.Ub)
        A1.Aprint()

        A2 = Grid ( fnames[1] )
#        A2 = Arg ( fnames[1] )
        A2.Ub = tb.shape[0] - 1
        A2.min = tb[ 0][0]
        A2.max = tb[-1][0]
        A2.step = (A2.max-A2.min)/(A2.Ub)
        A2.Aprint()

        A1.Normalization_UbSets()
        A2.Normalization_UbSets()

#        tb = tb[:][5:-1]
#        print "shape", tb.shape
        tb = delete (tb, range(0,1), 1 ).transpose()
        fun1 = Func()
        fun1.grd = tb
        fun1.V = V
        fun1.A = [A1, A2]
        fun1.dim = 2
        return gFun2( fun1 ) 
  

#    d = int(input())
 #   print('1 / {} = {}'.format(d, 1 / d), file=g)


def oFunFromSolFile(ReadFrom, Vnum=1):  # для tbl   нулевая  колонка - аргумент. по умолчанию первая функция
    if co.printL: print ('FunFromFile', ReadFrom)
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
        #            if co.printL :
        #           print "Read from", ReadFrom, cols, 'dim=', ret_fun.dim
        tmp_curentTabl = co.curentTabl  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  ###
        co.curentTabl = None
        if ret_fun.dim == 1:
            tb = loadtxt(fi, 'double')
            ret_fun.A = [Grid(cols[0], tb[0][0], tb[-1][0], -(tb.shape[0] - 1))]
            ret_fun.grd = zeros(ret_fun.A[0].Ub + 1, float64)
            for x in ret_fun.A[0].NodS:
                ret_fun.A[0].Val[x] = tb[x][0]
                ret_fun.grd[x] = tb[x][Vnum]
        #                ret_fun.grd = ravel( delete (tb, range(0,1), 1 ) )
        #                for x in ret_fun.A[0].NodS :
        #                       ret_fun.A[0].Val[x] = tb[x][0]
        #                        ret_fun.grd[x]      = tb[x][1]
        #                return  ret_fun

        elif ret_fun.dim == 2:
            x_gr = fi.readline().split()
            tb = loadtxt(fi, 'double')
            if len(tb.shape) == 1:
                print ("SSSSSSSSSSSSSSSSSSSSSSSSS", tb.shape[0])
                tb = reshape(tb, (1, tb.shape[0]))
                print ("SSSSSSSSS", tb.shape[0], tb.shape[1])
                print (tb)
            ret_fun.A = [Grid(cols[0], float(x_gr[0]), float(x_gr[-1]), -(len(x_gr) - 1)),
                         Grid(cols[1], tb[0][0], tb[-1][0], -(tb.shape[0] - 1))]
            ###                ret_fun.A = [ Grid ( fnames[0], float(x_gr[0]), float(x_gr[-1]), -(len (x_gr)-1) ),
            ###                           Grid ( fnames[1], tb[ 0][0],      tb[-1][0],       -(tb.shape[0]-1) ) ]
            #                ret_fun.A = [ Arg ( fnames[0], -(len (x_gr)-1), float(x_gr[0]), float(x_gr[-1]) ),
            #                             Arg ( fnames[1], -(tb.shape[0]-1), tb[ 0][0], tb[-1][0] ) ]
            for x in ret_fun.A[0].NodS:  ret_fun.A[0].Val[x] = float(x_gr[x])
            for x in ret_fun.A[1].NodS:  ret_fun.A[1].Val[x] = tb[x][0]
            ret_fun.grd = delete(tb, range(0, 1), 1).transpose()
        co.curentTabl = tmp_curentTabl
        return ret_fun

    #      except IOError as e:
    print ("**********************не удалось открыть файл  !" + ReadFrom + '!')
    return None;


def FunFromSolFile(ReadFrom):
    if co.printL: print ('FunFromSolFile', ReadFrom)
    root, ext = splitext(ReadFrom.upper())
    if '.ASC' == ext:
        cols, xp, yp, grd = ReadGridInf(ReadFrom)
    else:
        cols, xp, yp, grd = ReadSolInf(ReadFrom)

#    print 'BBB', grd.shape
    ret_fun = Fun()
    if len(xp) == 0: ret_fun.dim = 1
    else:            ret_fun.dim = 2
    ret_fun.param = True
    ret_fun.V = Vari(cols[-1])

    tmp_curentTabl = co.curentTabl  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  ###
    co.curentTabl = None
    if ret_fun.dim == 1:
            ret_fun.A = [Grid(cols[0], yp[0], yp[-1], -(len(yp) - 1))]
            ret_fun.grd = grd
    elif ret_fun.dim == 2:
            ret_fun.A = [Grid(cols[0], xp[0], xp[-1], -(len(xp) - 1)),
                         Grid(cols[1], yp[0], yp[-1], -(len(yp) - 1))]
            ret_fun.grd = grd.transpose()  # delete(tb, range(0, 1), 1).transpose()
    co.curentTabl = tmp_curentTabl
    return ret_fun



def FunFromFileNew ( ReadFrom, Vnum = 1 ) :        #  для tbl   нулевая  колонка - аргумент. по умолчанию первая функция
        if co.printL : print ('FunFromFile', ReadFrom)
        root, ext = splitext(ReadFrom.upper())
        if '.ASC' == ext or \
           '.SOL' == ext :
            return FunFromSolFile(ReadFrom)
#            cols, x1, x2, tb = ReadGridInf(ReadFrom)
        else:
            cols, x1, x2, tb = ReadSolInf ( ReadFrom )    # только для dim==1
        ret_fun = Fun()
        if len ( x2 ) == 0 :  ret_fun.dim = 1
        else               :  ret_fun.dim = 2
        ret_fun.param = True
        ret_fun.V     = Vari ( cols[Vnum] )

        tmp_curentTabl = co.curentTabl  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  ###
        co.curentTabl = None
        if ret_fun.dim == 1:
            ret_fun.A = [Grid(cols[0], tb[0][0], tb[-1][0], -(tb.shape[0] - 1))]
            ret_fun.grd = zeros(ret_fun.A[0].Ub + 1, float64)
            for x in ret_fun.A[0].NodS:
###                ret_fun.A[0].Val[x] = tb[x][0]
                ret_fun.grd[x] = tb[x][Vnum]
        elif ret_fun.dim == 2:
            ret_fun.A = [Grid(cols[0], float(x1[0]), float(x1[-1]), -(len(x1) - 1)),
                         Grid(cols[1], x2[0], x2[-1], -(len(x2) - 1))]
            ret_fun.grd = tb
#            print (tb.shape)
        co.curentTabl = tmp_curentTabl
        return ret_fun


class Fun (  ) :
    def __init__ (self, Vname='',  As=[], param=False, maxP=-1 ) :
#    def __init__(self, V=0 ):

        self.V = Vari(Vname)  #V #0 #[ ]             #  var
        self.A = copy(As) #[ ]             #  Arg

        self.dim = len (self.A)  #-1
        self.NoR   = 0
        self.sR    = []           # множ записей табл
        self.NDT   = -99999
# 27        self.Task  = co.Task
        self.type  = "g"
        self.maxP  = maxP # -1            # степень полинома
        self.grd   = None
        self.mu       = None
        self.testSet  = []
        self.teachSet = []
        self.domain = None
        self.neNDT = None
        self.Nxx   = 0
        self.Nyy   = 0
        self.Nxy   = 0
        self.gap   = None
## 27        self.G     = 0
        self.MSDv  = None
  #      self.nCrVa = None
        self.CVresult = []    #  [[spart, npart],[spart, npart],.. ]    27
        self.sCrVa = 0        #  sqrt (..)                              27

#        self.ReadFrom = ''
        self.param    = param #False
        self.domain_ = Reals
                                                                        # возможно меняет  param и type.
    def CopyFromFun ( self, DataFrom, new_param=None, new_type=None, copy_dat = True ):
        if new_type is None : self.type  = DataFrom.type                # для полином -> грид : вычисляет значения
        else                : self.type  = new_type
        if new_param is None : self.param  = DataFrom.type
        else                 : self.param  = new_param

        self.V     = deepcopy(DataFrom.V)         # InDada
        if not copy_dat : self.V.dat = None
        self.mu       = DataFrom.mu     ######## 2020 09 06
        self.A     = deepcopy(DataFrom.A)
        self.dim   = DataFrom.dim
        self.NDT   = DataFrom.NDT
 #27       self.Task  = DataFrom.Task
        self.NoR   = DataFrom.NoR
        self.sR    = DataFrom.sR
        self.maxP  = DataFrom.maxP
        self.domain = DataFrom.domain
        self.neNDT = deepcopy(DataFrom.neNDT)      #    deepcopy ?????
        self.Nxx   = DataFrom.Nxx
        self.Nyy   = DataFrom.Nyy
        self.Nxy   = DataFrom.Nxy
        self.gap   = deepcopy(DataFrom.gap)
#        self.ReadFrom = DataFrom.ReadFrom
        self.domain_  = DataFrom.domain_
        self.testSet  = DataFrom.testSet
        self.teachSet = DataFrom.teachSet
#        self.G     = DataFrom.G
        self.grd = None
        if self.type == 'p' :           return self     # grd  handling
        if DataFrom.grd is None  : return self
        if not self.param        : return self               # grd  handling
        if DataFrom.param :  self.grd = deepcopy(DataFrom.grd);  return self

        if self.dim   == 1:  self.grd = zeros(self.A[0].Ub + 1, float64)
        elif self.dim == 2:  self.grd = zeros((self.A[0].Ub + 1, self.A[1].Ub + 1), float64)

#        print (self.type)
        if DataFrom.type == 'g' or DataFrom.type == 'G':
                if   self.dim == 0:  self.grd = DataFrom.grd()
                elif self.dim == 1:
                    for i in self.A[0].NodS:  self.grd[i] = DataFrom.grd[i]()
                elif self.dim == 2:
                    for i in self.A[0].NodS:
                        for j in self.A[1].NodS:  self.grd[i, j] = DataFrom.grd[i, j]()
        else :                                                                           #  ПОЛИНОМ
                Ax = self.A[0]
                if self.dim == 1:
                    for x in Ax.NodS:
                        if self.fneNDT(x) == 1:      self.grd[x] = DataFrom.F([Ax.Val[x]])()
#                        if self.neNDT[x] == 1:      self.grd[x] = DataFrom.F([Ax.min + Ax.step * x])()
                        else                 :      self.grd[x] = DataFrom.NDT
                else:  # dim 2
                    Ay = self.A[1]
                    for x in Ax.NodS:
                        for y in Ay.NodS:
                            if self.fneNDT(x,y) == 1:  self.grd[x, y] = DataFrom.F([ Ax.Val[x], Ay.Val[y] ])()
#    27                            self.grd[x, y] = DataFrom.F([Ax.min + Ax.step * x, Ay.min + Ay.step * y])()
                            else                    :  self.grd[x, y] = DataFrom.NDT
        return self


    def Clone ( self ):
                return Fun().CopyFromFun(self)

    def GridParamClone (self, copy_dat = False ):
                return Fun().CopyFromFun ( self, True, 'g', copy_dat )



#    def Ini_par ( self, FuncR, param,  typ = 'g' ) :   #  27


    def Initialize ( self, Finitialize = None ) :
        if co.printL > 0: printS('Initialize: |'); self.printM()
#        haveAll = False
        if Finitialize is None : Finitialize = '0'
        InitFloat = getfloatNaN (Finitialize)
        if isnan(InitFloat) :                     #  Param:  H(X,Y) = DEM_Kostica.asc
            func = FunFromFileNew (Finitialize)
          #  func = FunFromSolFile(Finitialize)
            func.V.name = self.V.name           # сохраняем имена из задания
            self.V = func.V
            for ia, a in enumerate(self.A) :
                if type(a) == type('abc'):   func.A[ia].name = a
                else                     :   func.A[ia].name = a.name
                self.A[ia] = func.A[ia]
            self.grd = func.grd
            self.Normalization(co.VarNormalization)
            return self
        tmpcurentTabl = co.curentTabl
        if co.ReadFrom != '':  Tab.Select ( co.ReadFrom )
#        elif co.curentTabl is None and self.param :
 #           fname = self.nameFun() + ".sol"
  #          if os.path.isfile(fname):
   #             Tab.Select('* from ' + fname)
    #            print ('Read data for PARAM from :', fname)
     #       else:
      #          print ('******** Param : ' + self.nameFun() + '   will be initiated by 0 **************')

        for ia, a in enumerate(self.A):  # дописываем гриды
            if co.printL:  print ('A:', a)
            if type(a) != type('abc'):
                self.A[ia] = deepcopy(a)   #   !!!!!!!!!!!! #
                continue
            g = findGridByName(co.Task.Grids, a)
            if g == None:
                print ('\n***********************  NO GRID FOR ARG NAME ', a, '*********************')
                g = Grid (a)
                print ("***********************GRID:",)
                g.myprint();
                print ('    HAS BEEN ADDED *****************************')
            # exit (-1)
            self.A[ia] = Grid (g) #Arg (g)

        if co.curentTabl != None :
           haveAll = self.GetData (co.curentTabl)     # считываем
           if haveAll==False and self.param :
               print ('Not all field for PARAM')
#               exit (-1)
        co.ReadFrom = ''
        co.curentTabl = tmpcurentTabl

        self.Normalization(co.VarNormalization)

        self.Make_neNDT()
        if self.param:                     # function-Param
                if self.dim == 0:
                    self.grd = 0
                elif self.dim == 1:
                    self.grd = zeros((self.A[0].Ub + 1), float64)
                    if not isnan (InitFloat) :  self.grd[:] = InitFloat
                elif self.dim == 2:
                    self.grd = zeros((self.A[0].Ub + 1, self.A[1].Ub + 1), float64)
                    if not isnan (InitFloat) :  self.grd[:][:] = InitFloat
                self.InitByData()
        return self

    def Normalization ( self, VarNormalization ) :
#      self.dim   = len(self.A)
#       print tbl.min(0)[self.num] 
 #     print len(self.A)
        self.V.name
        for arg in self.A :   arg.Normalization_UbSets ( )
        self.V.Normalization (VarNormalization)
##      self.V.Normalization (self, VarNormalization) 




    def InitBy ( self, val, vis0, vis1) :
              A0 = self.A[0]
              A1 = self.A[1]
              if vis0  < 0 : vis0  = - vis0 * A0.step
              if vis1  < 0 : vis1  = - vis1 * A1.step

              for m in self.sR :
                for x   in range( max(0, A0.indNormVal(A0.dat[m]-vis0)), min(A0.Ub, A0.indNormVal(A0.dat[m]+vis0))+1 ) :
                  for y in range( max(0, A1.indNormVal(A1.dat[m]-vis1)), min(A1.Ub, A1.indNormVal(A1.dat[m]+vis1))+1 ) :
                     self.grd[x,y] = 1
          
            
    def calcNDTparam(self) :
        A0 = self.A[0]
        neNDT = self.neNDT
        if self.dim == 1:
          if neNDT is None :
            self.Nxx = A0.Ub-1
          else :
            self.Nxx = sum ( neNDT[x-1]*neNDT[x]*neNDT[x+1] for x in range( 1,A0.Ub ) )
        else :          
          A1 = self.A[1]
          if neNDT is None :
              self.Nxx = (A0.Ub-1)*(A1.Ub+1)
              self.Nyy = (A0.Ub+1)*(A1.Ub-1)
              self.Nxy = (A0.Ub-1)*(A1.Ub-1)
          else :
            self.Nxx = sum ( neNDT[x-1,y] * neNDT[x,y] * neNDT[x+1,y]  
                    for y in A1.NodS    for x in A0.mNodSm )
            self.Nyy = sum ( neNDT[x,y-1] * neNDT[x,y] * neNDT[x,y+1]  
                    for y in A1.mNodSm  for x in A0.NodS )
            self.Nxy = sum ( neNDT[x+1,y+1] * neNDT[x+1,y-1] * neNDT[x-1,y+1] * neNDT[x-1,y-1]
                    for y in A1.mNodSm  for x in A0.mNodSm )
            

    def fneNDT (self, x, y=0) :
        if self.neNDT is None : return 1
        if self.dim == 1      : return self.neNDT[x]
        if self.dim == 2      : return self.neNDT[x,y]

    def f_gap (self, x, y=0) :
        if self.gap is None : return 1
        if self.dim == 1      : return self.gap[x]
        if self.dim == 2      : return self.gap[x,y]

    def AddGap ( self ) :
        if self.dim == 1 :   self.gap = ones (  self.A[0].Ub+1,                 float64 )
        if self.dim == 2 :   self.gap = ones ( (self.A[0].Ub+1, self.A[1].Ub+1),float64 )


    def Make_neNDT(self) :
        if self.dim == 0 :  return

        if not self.domain is None :
#            self.domain.Make_neNDT()
            self.neNDT = self.domain.isDat
        self.calcNDTparam()
        return

    def neNDTbyVal (self, xVal, yVal=None) :
        ix = self.A[0].ValToInd(xVal)
        if self.dim == 1:
            return self.neNDT[ix]
        else :
            iy = self.A[1].ValToInd(yVal)
            return self.neNDT[ix,iy]

    def GetData ( self, tabl ) :
        if co.printL >0 : printS ('GetData: |'); self.printM()
        if tabl is None :  return False
        haveAll = True
        haveAny = False

        V_tb = tabl.getField_tb (self.V.name)
        if V_tb is None :
            print ("GetData ****************************** No Field in ", tabl.name,  "For Var", self.V.name, "****")
            haveAll = False
        else :
            self.V.dat = zeros( tabl.NoR, float64 )
            haveAny = True

        A_tb = []    
        for a in self.A :
            A_tb.append( tabl.getField_tb (a.oname) )
            if A_tb[-1] is None :
                print ("GetData ****************************** No Field in ", tabl.name,  "For Arg", a.name, "*****")
                haveAll = False
            else :
                a.dat = zeros( tabl.NoR, float64 )
                haveAny = True
        if haveAny == False : return False

        self.NoR = 0
        numNaN = 0
        for i in tabl.sR :
            if not V_tb is None :
                if isnan ( V_tb[i] ) or V_tb[i] == self.NDT :
                    if com.useNaN == False: continue
                    numNaN += 1 
                self.V.dat[self.NoR] = V_tb[i]                   # 0
            OK = 1
            for narg, a_tb in enumerate(A_tb) :
                if A_tb[narg] is None : continue
                if isnan (a_tb[i])     : OK = 0; break
                if a_tb[i] == self.NDT : OK = 0; break
                if a_tb[i] <  self.A[narg].min or a_tb[i] >  self.A[narg].max  : OK = 0; break
                self.A[narg].dat[self.NoR] = a_tb[i]   # 1 ...
            if not OK : continue
            self.NoR += 1
#            print self.NoR, 

        if not V_tb is None :                         #  resize
              self.V.dat = delete ( self.V.dat, range(self.NoR,self.V.dat.shape[0]) )
        for narg, arg in enumerate(self.A) :
            if not A_tb[narg] is None :
                  arg.dat = delete (arg.dat, range(self.NoR,arg.dat.shape[0]) )
        
        self.sR = range (self.NoR)
        if co.printL : print ("GetData numNaN", numNaN,"NoR", self.NoR)  #, "mins", tbl.min(0), "maxs", tbl.max(0)
        return haveAll

    #    def Ini ( self, FuncR, typ = 'g', prLev=1 ) :
 #       self.Ini_par ( FuncR, FuncR.param,  typ, prLev )
        
#        self.CopyFrom(FuncR)
 #       self.type  = typ
  #      if self.dim == 0 :
   #         print "Func"+typ, self.nameFun()
    #    elif self.dim == 1 :
     #       if prLev: print "Func"+typ, self.nameFun(), self.A[0].Ub+1, "Nxx",self.Nxx
      #      if self.param :
       #           self.grd = zeros( ( self.A[0].Ub+1 ), float64 )
        #          self.InitByData()
#        else :          # self.dim == 2 :
 #           if prLev: print "Func"+typ, self.nameFun(), self.A[0].Ub+1, self.A[1].Ub+1, "Nxx",self.Nxx,self.Nyy,self.Nxy
  #          if self.param :
   #               self.grd = zeros( ( self.A[0].Ub+1, self.A[1].Ub+1 ), float64 ) 
    #              self.InitByData()

    def nameFun(self):
            name = self.V.name
            if len(self.A) > 0:  name += '('
            #           print 'nnn', name, self.dim
            for ar in self.A:
                if type(ar) == type('abc'):  name += ar + ','
                else:                        name += ar.name + ','
            if len(self.A) > 0:  name = name[0:-1]  # -1 убрать запятую
            if len(self.A) > 0:  name = name + ')'
            #            print 'nameFun', name, len(self.A), '|'
            return name

    def onameFun(self):
            name = self.V.name
            if len(self.A) > 0:  name += '('
            #           print 'nnn', name, self.dim
            for ar in self.A:
                if type(ar) == type('abc'):  name += ar + ','
                else                      :  name += ar.oname + ','
            if len(self.A) > 0:  name = name[0:-1]  # -1 убрать запятую
            if len(self.A) > 0:  name = name + ')'
            #            print 'nameFun', name, len(self.A), '|'
            return name

    def myprint (self) :  self.printM()


    def printM (self) :
            printS (self.V.name + '(' ,'|')
            for d, a in enumerate (self.A): #range(self.dim) :
                if type (a) == type ('abc') : print (a)
                else                        : a.printM()
                if d == self.dim-1 :  break
                printS (',','|')

            if self.param :  param = 'p'
            else          :  param = 'v' 
            if self.type == 'p' : printS (')',self.type+str(self.maxP)+param,'|')
            else                : printS (')',self.type               +param,'|')
            print (self.V.sigma, self.V.average, self.NoR)

    def Mult(self, val):
        if self.type == 'p':
            for p in self.PolyR:       self.grd[p].value *= val
        elif self.param :
            if self.dim == 1:
                for x in self.A[0].NodS:   self.grd[x] *= val
                #            print "FixAll d1",
            else:
                for x in self.A[0].NodS:
                    for y in self.A[1].NodS: self.grd[x, y] *= val
        else :
          if self.dim == 1:
            for x in self.A[0].NodS:   self.grd[x].value *= val
            #            print "FixAll d1",
          else:
            for x in self.A[0].NodS:
                for y in self.A[1].NodS: self.grd[x, y].value *= val

    def Divide (self, by ):
 #           if self.type == 'p':
  #              for p in self.PolyR:       self.grd[p].value *= val
            if by.param :
              if self.dim == 1:
                for x in self.A[0].NodS:   self.grd[x] /= by.grd[x]
                #            print "FixAll d1",
              else:
                for x in self.A[0].NodS:
                    for y in self.A[1].NodS: self.grd[x, y].value /= by.grd[x,y]
            else :
              if self.dim == 1:
                for x in self.A[0].NodS:   self.grd[x] /= by.grd[x]()
                #            print "FixAll d1",
              else:
                for x in self.A[0].NodS:
                    for y in self.A[1].NodS: self.grd[x, y].value /= by.grd[x,y]()

    def Minus(self, by):
        #           if self.type == 'p':
        #              for p in self.PolyR:       self.grd[p].value *= val
        if by.param:
            if self.dim == 1:
                for x in self.A[0].NodS:
#                    print ('????????', x, self.grd[x], by.grd[x] )
                    self.grd[x] -= by.grd[x]
 #                   print (self.grd[x])
            else:
                for x in self.A[0].NodS:
                    for y in self.A[1].NodS: self.grd[x, y].value -= by.grd[x, y]
        else:
            if self.dim == 1:
                for x in self.A[0].NodS:   self.grd[x] -= by.grd[x]()
                #            print "FixAll d1",
            else:
                for x in self.A[0].NodS:
                    for y in self.A[1].NodS: self.grd[x, y].value -= by.grd[x, y]()

    def SetPointValue ( self, args, val ) :
        if self.type == 'p' :
            print ('************************ set val POLY *************')
            return
        farg = []
        for ia, a in enumerate(self.A) :
            ind = int( (float(args[ia])-a.min)/a.step + 0.5 )
            ind = max (ind, 0   )
            ind = min (ind, a.Ub)
            farg.append (ind)
        if self.dim == 0 :
            if self.param : self.grd = float ( val )
            else          : self.grd.value = float ( val )
        elif self.dim == 1 :
            if self.param : self.grd[farg[0]] = float ( val )
            else          : self.grd[farg[0]].value = float ( val )
        elif self.dim == 2 :
            if self.param : self.grd[farg[0],farg[1]] = float ( val )
            else          : self.grd[farg[0],farg[1]].value = float ( val )
        elif self.dim == 3 :
            if self.param : self.grd[farg[0],farg[1],farg[2]] = float ( val )
            else          : self.grd[farg[0],farg[1],farg[2]].value = float ( val )


    def FixAll (self) :
        if self.type == 'p' :
            for p in self.PolyR :  self.grd[p].fixed = True 
            print ("FixAll Poly",)
        elif self.dim == 1 :
            for x in self.A[0].NodS :  self.grd[x].fixed = True 
            print ("FixAll d1",)
        else :      
            for x in self.A[0].NodS :  
              for y in self.A[1].NodS :  self.grd[x,y].fixed = True
            print ("FixAll d2",)


    def Fix (self) :
        if self.type == 'p' : return
        if self.neNDT is None : return
        if self.dim == 0 :
            pass
# ?????                  self.grd.value = self.NDT
# ?????                  self.grd.fixed = True 
        elif self.dim == 1 :
            for x in self.A[0].NodS :  
                if not self.neNDT[x] :
                  self.grd[x].value = self.NDT
                  self.grd[x].fixed = True 
        else :      
            for x in self.A[0].NodS :  
              for y in self.A[1].NodS :  
                if not self.neNDT[x,y] :
                  self.grd[x,y].value = self.NDT
                  self.grd[x,y].fixed = True

    def sumXX ( self ) :   pass

    def delta( self, n ) :
#        print  self.tbl[n,self.V.num] - self.Ftbl ( n ) 
#        return	 self.tbl[n,self.V.num] - self.Ftbl ( n ) 
        return	 self.V.dat[n] - self.Ftbl ( n ) 

    def MSD ( self ) :
        if not co.Hack_Stab :
#            return  1. /self.V.sigma**2  /self.NoR * sum (  self.G.mu[n] * self.delta(n)**2  for n in self.sR )
#            print 'MSD', self.V.name, len (self.mu)
            return  1. /self.V.sigma2 /sum ( self.mu[n] for n in self.sR )  \
                                    * sum (  self.mu[n] * self.delta(n)**2 for n in self.sR )
        else :
            return  1. /self.V.sigma2  /self.NoR * sum (  self.mu[n] * self.delta(n)**2  for n in self.sR )

    def MSDcheck(self) :
            return  1./self.V.sigma2 /self.V.NoR * sum ( (self.tbl[n,self.V.num]!=self.NDT)
                                           * self.mu[n] * self.delta(n)**2
                                     for n in self.sR )

    def MSDnan (self, valid_f = None) :        # valid_f  - for verification - validation
            ret = 0
            num = 0
            for n in self.sR :
                if not isnan(self.V.dat[n])  :
                      ret += self.mu[n] * self.delta(n)**2
                      num += self.mu[n]
            ret = 1. / self.V.sigma2 / num * ret
            return ret


    def MSDverif(self, verif_f):  # verif_f  - for verification - validation
            ret = 0
            num = 0
     #       n=0
#            print verif_f.A[0].dat[n],verif_f.A[0].min,verif_f.V.dat[n]
 #           print self.grd[0]()
            for n in verif_f.sR :
                if not isnan(verif_f.V.dat[n])  :
                      ret += (self.F([verif_f.A[0].dat[n]+verif_f.A[0].min])-verif_f.V.dat[n])**2
                      num += 1
            ret /= num
            return ret

    def MSDno_mu ( self ) : 
        return  1./self.V.sigma2 /self.NoR * sum ( self.delta(n)**2  for n in self.sR )

    def Compl ( self, bets ) :                      #28 for the sake of brevity
            return self.ComplDer2 ( bets )

    def Complexity ( self, bets ) :
            return self.ComplDer2 ( bets )

    def ComplCycle ( self, bets ) :                      #28 for the sake of brevity
            return    bets[0]**4 * self.sumXXcycle ( )

    def ComplCyc0E ( self, bets ) :                 #28    первая точка должна быть равна последней
            return    bets[0]**4 * self.sumXXcyc0E ( )


    def ComplDer2 ( self, bets ) :
            if self.dim == 1 :
              return    bets[0]**4 * self.sumXX ( )
            else:
              return (  bets[0]**4 * self.sumXX ( ) 
                      + bets[1]**4 * self.sumYY ( ) 
                      + bets[0]**2 * bets[1]**2 * self.sumXY ( )
                     )   
##!!              return    bets[0]**4 /self.Nxx  /(1./self.A[0].Ub)**4 * self.sumXX ( )
#            else:
#              return (  bets[0]**4 / self.Nxx  / (1./self.A[0].Ub)**4 * self.sumXX ( )
 #                     + bets[1]**4 / self.Nyy  / (1./self.A[1].Ub)**4 * self.sumYY ( ) 
  #                    + bets[0]**2 * bets[1]**2 * 2. / self.Nxy * 0.25 / (1./self.A[0].Ub)**2
   #                                     / (1./self.A[1].Ub)**2 * self.sumXY ( )
    #                 )   

    def ComplDer1 ( self, bets ) :
            if self.dim == 1 :
                return  bets[0]**4  * self.sumX()
            else:
                return ( bets[0]**4  * self.sumX()
                       + bets[1]**4  * self.sumY()
                       )
#              return    bets[0]**4 /self.Nxx  /(1./self.A[0].Ub)**2 * self.sumX ( )
 #           else:
  #            return (  bets[0]**4 / self.Nxx  / (1./self.A[0].Ub)**2 * self.sumX ( )
   #                   + bets[1]**4 / self.Nyy  / (1./self.A[1].Ub)**2 * self.sumY ( )
    #                 )

    def Mean ( self ) : 
            if self.dim == 1 :
                    return   1./(self.A[0].Ub+1)* sum ( self.grd[x]  for x in self.A[0].NodS )
            else:
                    return ( 1./(self.A[0].Ub+1)/(self.A[1].Ub+1)
                             * sum ( self.grd[x,y]  for x in self.A[0].NodS for y in self.A[1].NodS )
                           )  

    def Norma_L2mL2 ( self ) : 
            if   self.dim == 1 :
                    return   1./(self.A[0].Ub+1)    \
                             * sum ( self.grd[x]**2      for x in self.A[0].NodS )
            elif self.dim == 2:
                    return ( 1./(self.A[0].Ub+1)/(self.A[1].Ub+1)   \
                             * sum ( self.grd[x,y]**2    for x in self.A[0].NodS
                                                         for y in self.A[1].NodS )
                           )  
            elif self.dim == 3:
                    return ( 1./(self.A[0].Ub+1)/(self.A[1].Ub+1)/(self.A[2].Ub+1)  \
                             * sum ( self.grd[x,y,z]**2  for x in self.A[0].NodS
                                                         for y in self.A[1].NodS
                                                         for z in self.A[2].NodS )
                           )  

    def Norma_L2mL2Border ( self ) :
            Bor = self.makeBorder ()
            ret = 0
            NoB = 0
            for b in Bor :
                  NoB += 1
                  ret += self.grd[b[0],b[1]]**2
            return ret/NoB
                  
    def SavePoints ( self ) :
        for a in self.A :
            if a.dat is None :  return;
#            if a.num < 0 : print "num < 0  arg=",  a.name;  return;

        Prefix = co.Prefix
        if self.dim == 0 : return;
        fName = Prefix + self.V.name + "(" +self.A[0].name+ ").txt"
        if self.dim == 1 : fName = Prefix + self.V.name + "(" +self.A[0].name+ ").txt"
        else :  fName = Prefix + self.V.name + "(" +self.A[0].name+ "," +self.A[1].name+ ").txt"
        fi = open ( fName, "w")
        for a in self.A :  fi.write ( a.name + "\t" )      # Names args
        fi.write ( self.V.name + Prefix ) # решение
        if not self.V.dat is None : fi.write ( "\t" + self.V.name + 'data\tErr\t#SvFver_62_tbl\n' )  # точки
         
        for n in self.sR :                                           # Data
            fi.write ( "\n" )             
#            for a in self.A : fi.write ( str( a.min + a.step * self.tbl[n,a.num] ) + '\t' )
##            for a in self.A : fi.write ( str( a.min + self.tbl[n,a.num] ) + '\t' )
            for a in self.A : fi.write ( str( a.min + a.dat[n] ) + '\t' )
            fi.write (  str( self.V.avr + self.Ftbl(n)() ) )
            if not self.V.dat is None : 
                fi.write ( '\t'+ str( self.V.avr + self.V.dat[n] ) + '\t' + str ( self.Ftbl(n)()-self.V.dat[n] ) )

###            for c in range(len(self.Col)) : fi.write ( "\t"+ str( self.tbl[n,self.Col[c].num] ) )
        if co.printL : print ("End of SavePoints to", fName)



    def grdNaN (self, i,j=None) :
        if self.dim == 1 :
            if self.fneNDT(i) == 0 : return NaN
            if self.param :  v = self.grd[i]
            else          :  v = self.grd[i]()
        else :
            if self.fneNDT(i,j) == 0 : return NaN
            if self.param :  v = self.grd[i,j]
            else          :  v = self.grd[i,j]()
        return  v

    def grdNDT (self, i,j=None) :
        v = grdNaN (self, i,j)
        if isnan(v): return self.NDT
        return  v

    def grdNaNreal (self, i,j=None) :
        if self.dim == 1 :
            if self.fneNDT(i) == 0 : return NaN
            if self.param :  v = self.grd[i]
            else          :  v = self.grd[i]()
        else :
            if self.fneNDT(i,j) == 0 : return NaN
            if self.param :  v = self.grd[i,j]
            else          :  v = self.grd[i,j]()
        return  v + self.V.avr

    def grdNDTreal (self, i,j=None) :
        v = self.grdNaNreal ( i,j )
        if isnan(v): return self.NDT
        return  v



    def prep_val ( self, val, neNDT ) :
                      if self.param :     ret = val
                      else          :     ret = val()
                      if   neNDT == 0 :   return  str(self.NDT)
#                      elif not neNDT  :   return  str(self.NDT)
                      else:               return "%20.16g" % ((self.V.avr + ret))   #  значения
          

    def SaveSolNew ( self, fName ) :         #New   бросил, не отладил...
#      print 'type_dim', self.type,  self.dim

      Prefix = co.Prefix
      if fName == '' :
          if self.type == 'g' : fName = Prefix +self.nameFun() + ".sol"
          else                : fName = Prefix +self.nameFun() + ".p.sol"
      fi = open ( fName, "w")
      fi.write ( '#SvF_64_' + self.type + '_' + str(self.dim) + '\t' )
      
      if self.type == 'g' :
          for a in self.A : fi.write ( a.name + '\t' )
          fi.write ( self.V.name + '\n' )
          for a in self.A :
              for j in a.NodS :  fi.write ( "\t" + str(a.min + a.step*j) )     #  точки по x,y,z
              fi.write ( '\n' )
          if self.dim == 0:
#              print >> fi,  self.prep_val ( self.grd, 1 )
              fi.write( self.prep_val ( self.grd, 1 ) + '\n' )
          elif self.dim == 1:
              for i in self.A[0].NodS :
#                print >> fi,  self.prep_val ( self.grd[i], self.neNDT[i] )
                fi.write( self.prep_val ( self.grd[i], self.neNDT[i] )+'/n' )
          elif self.dim == 2:
              for j in self.A[1].NodS:                       #  точки по y
                  for i in self.A[0].NodS :
#                      print >> fi,  self.prep_val ( self.grd[i,j], self.neNDT[i,j] ),
                      fi.write( self.prep_val(self.grd[i, j], self.neNDT[i, j]) )
                  fi.write ( '\n' )
    
          elif self.dim == 3:
              for k in self.A[2].NodS:                       #  точки по z
                for j in self.A[1].NodS:                       #  точки по y
                  for i in self.A[0].NodS :
 #                     print >> fi,  self.prep_val ( self.grd[i,j,k], 1 ),  #self.neNDT[i,j] )
                      fi.write( self.prep_val(self.grd[i, j, k], 1) )  # self.neNDT[i,j] )
                  fi.write ( '\n' )
          if co.printL > 0 : print ("End of gFun2.SaveSol to", fName)

      else :                                                                  # poly
        print >> f, "%d" % self.dim + " %d" % self.maxP + " %d" % self.sizeP 

        for d in range(self.dim):
            f.write ( '('+self.A[d].name +'-'+str(self.A[d].min)+')/'+str(self.A[d].ma_mi) +'\t' )
#            print >> f, self.A[d].name + '-', "%g" % (self.A[d].min) + "\t",
        f.write ( self.V.name + Prefix )   #Prefix + '\t#SvFver_62_poly\n'
        for i in self.PolyR :
#            f.write ( "\n" + str(self.grd[i]()) + "\t" + str(self.pow[i][0]) )
            print >> f,"\n", "%20.16g" % (self.grd[i]()) + "\t", str(self.pow[i][0]), 
            if self.dim == 2 :
                f.write ( "\t" + str(self.pow[i][1]) )
        f.close()

        fung = self.GridParamClone(True)
        fung.SaveSol(fName)
        if co.printL > 0 : print ("END of pFun.SaveSol to ", fpName)
      fi.close()
      return


    def SaveSol ( self, fName='' ) :                ## OLD
      Ksigma = 0
      Prefix = co.Prefix
      
      if co.printL > 0 : print ('Before SaveSol to ', fName, self.type)
      if fName == '' :
          if self.type == 'g' : fName = Prefix +self.nameFun() + ".sol"
          else                : fName = Prefix +self.nameFun() + ".p.sol"
      if co.printL > 0 : print ('SaveSol to ', fName, self.type)
      try:
            fi = open ( fName, "w")
      except IOError as e:
            print ("Can''t open file: ", fName)
            return;

      if self.type == 'g' or self.type == 'G' :
          for a in self.A : fi.write ( a.name + '\t' )
          fi.write ( self.V.name )

          if   self.dim==0 :
              fi.write ( '\t#SvFver_62_tbl\n' )
              fi.write( str_val ( self.grd() ) )
              if self.param :     Ksigma += self.grd
              else          :     Ksigma += self.grd()

          elif self.dim==1 :
            fi.write ( '\t#SvFver_62_tbl\n' )
            A = self.A[0]
            V = self.V
            for i in A.NodS :
                v = self.grdNaNreal(i)
#                fi.write( str(A.min + A.step*i) + "\t" + str_val(v)+'\n' )
                fi.write( str(A.Val[i]) + "\t" + str_val(v)+'\n' )
                Ksigma += v     # nan  ?

          elif self.dim==2 :
            fi.write ( '\t#SvFver_62_mtr2\n' )
            Ax = self.A[0]
            Ay = self.A[1]
            V = self.V
            for i in Ax.NodS :  fi.write ( "\t" + str(Ax.min + Ax.step*i) )     #  точки по х
            for j in Ay.NodS :
                fi.write ( "\n" + str(Ay.min + Ay.step*j) )     #  точки по y
                for i in Ax.NodS :
                    v = self.grdNaNreal(i,j)
#                    print >> fi, "\t" + str_val(v),
                    fi.write( "\t" + str_val(v) )
                    Ksigma += v  # nan  ?
#                    print >> fi, "\t" + self.prep_val ( self.grd[i,j], self.fneNDT(i,j) ),
 #                   if self.param :     Ksigma += self.grd[i,j]
  #                  else          :     Ksigma += self.grd[i,j]()

          elif self.dim==3 :
              fi.write ( '\t#SvFver_62_mtr3\n' )
              for a in self.A :
                  for j in a.NodS :  fi.write ( "\t" + str(a.min + a.step*j) )     #  точки по x,y,z
                  fi.write ( '\n' )
              for k in self.A[2].NodS:                       #  точки по z
                for j in self.A[1].NodS:                       #  точки по y
                  for i in self.A[0].NodS :
#                      print >> fi,  self.prep_val ( self.grd[i,j,k], 1 ) + '\t',  #self.neNDT[i,j] )
                      fi.write( self.prep_val ( self.grd[i,j,k], 1 ) + '\t' )
                      if self.param :     Ksigma += self.grd[i,j,k]
                      else          :     Ksigma += self.grd[i,j,k]()
                  fi.write ( '\n' )


      else :                                                    # POLY
#        print >> fi, "%d" % self.dim + " %d" % self.maxP + " %d" % self.sizeP
        fi.write ( "%d" % self.dim + " %d" % self.maxP + " %d" % self.sizeP + '\n' )

        for d in range(self.dim):
            fi.write ( '('+self.A[d].name +'-'+str(self.A[d].min)+')/'+str(self.A[d].ma_mi) +'\t' )
#            print >> f, self.A[d].name + '-', "%g" % (self.A[d].min) + "\t",
        fi.write ( self.V.name + Prefix )   #Prefix + '\t#SvFver_62_poly\n'
        for i in self.PolyR :
#            f.write ( "\n" + str(self.grd[i]()) + "\t" + str(self.pow[i][0]) )
#            print >> fi,"\n", "%20.16g" % (self.grd[i]()) + "\t", str(self.pow[i][0]),
            fi.write ( "\n" + str_val( self.grd[i]() ) + "\t" + str(self.pow[i][0]) )
            if self.dim == 2 :
                fi.write ( "\t" + str(self.pow[i][1]) )
        fung = self.GridParamClone(True)
        gfName = fName.replace ('.p.', '.')
        fung.SaveSol(gfName)
      fi.close()
      if co.printL > 0 : print ("END of SaveSol to ", fName,'Ksigma', Ksigma, self.type)

      return


    def ReadSol ( self, fName='', printL=0 ) :
      Ksigma = 0
#      print 'self.Task.Mng.Prefix'+self.Task.Mng.Prefix+'|',fName
      Prefix = co.Prefix
#      Prefix = ''
      if fName == '' :
          if self.type == 'g' or self.type == 'G':
              fName = Prefix +self.nameFun() + ".sol"
          else                : fName = Prefix +self.nameFun() + ".p.sol"
      try:
            fi = open ( fName, "r")
      except IOError as e:
            print ("Can''t open file: ", fName)
            return;
      head = fi.readline().split()
#      if printL : print "ReadSol from", fName,  head,
######################################################
      if head[0][0:4] == '#SvF' :    #New   бросил, не отладил...
         ver = head[0].split('_')
         print ('ver', ver)

         if ver[1] == '64' :
            dim = int (ver[3])
            if ver[2] == 'g' :
                  StepInStep = []
                  for d in range (dim) :
                        StepInStep.append(float(len(fi.readline().split())-1)/self.A[d].Ub)
#                        Af = []
#                        for a in A : Af.append ( float(a) ) 
 #                       Arg.append ( Af )
                        print (self.A[d].Ub)
                  print ('StepInStep', StepInStep)
                  tb = loadtxt ( fi,'double' )
                  if co.printL : print ("shape", tb.shape)
                                
                  if self.dim==0 :
#                        self.grd.value = float(fi.readline()) 
                        self.grd.value = tb
                        print ('TTT', self.grd())
                        
                  elif self.dim==1 :
#                       tb = loadtxt (fi,'double')
 #                      if printL : print "shape", tb.shape
                       for j in self.A[0].NodS :
                           self.grd[j].value = (tb[int(j*StepInStep[0]), 0]-self.V.avr)  #  значения в новых узлах 
                  elif dim==2 :
  #                     tb = loadtxt (fi,'double')
   #                    if printL : print "shape", tb.shape

                       #for j in self.A[1].NodS :
                        # for i in self.A[0].NodS :
                         #  self.grd[i,j].value = (tb[int(j*StepInStep[1]),int(i*StepInStep[0])] -self.V.avr)  #  значения в новых узлах
                         
#                        fi.readline().split()
 #                       tb = loadtxt (fi,'double')
                        if co.printL : print ("shape", tb.shape)

                        for j in self.A[1].NodS :
                            for i in self.A[0].NodS :
                                self.grd[i,j].value = (tb[int(j*(tb.shape[0]-1)/self.A[1].Ub)       
                                                         ,int(i*(tb.shape[1]-1)/self.A[0].Ub)   
                                                         ] -self.V.avr)  #  значения в новых узлах
                        fi.close()
                        if co.printL > 0 : print ("End of gFun2.ReadSol from"), fName


#                       print self.grd[0,0].value, self.grd[self.A[0].Ub,self.A[1].Ub].value
            fi.close()
            if co.printL > 0 : print ("End of gFun2.ReadSol from", fName)
            return      
##############################################################################

      if self.type == 'g' and self.dim==0 :
            self.grd.value = float(fi.readline()) 
            Ksigma = self.grd()

      elif (self.type == 'g' or self.type == 'G') and self.dim==1 :
           fi.close()   
           fun = FunFromSolFile ( fName )
#           fun.myprint()

           for j in self.A[0].NodS :
                if self.fneNDT(j) == 0:
                    self.grd[j].value = NaN
                else :
                    self.grd[j].value = fun.F1_extra_const ( self.A[0].min + j * self.A[0].step ) -self.V.avr   #  значения в новых узлах
                    if isnan(self.grd[j].value): self.grd[j].value = 1
                    Ksigma += self.grd[j]()

           return     
      elif self.type == 'g' and self.dim==2 :
           fi.close()   
           fun = FunFromSolFile ( fName )
              
           for j in self.A[1].NodS :
               for i in self.A[0].NodS :
                   if self.fneNDT(i,j) == 0:
                       self.grd[i,j].value = NaN
                   else :
                       self.grd[i,j].value = fun.F2_extra_const ( self.A[0].min + i * self.A[0].step,
                                          self.A[1].min + j * self.A[1].step) -self.V.avr  #  значения в новых узлах
                       if isnan(self.grd[i,j].value) :  self.grd[i,j].value = 1
                       Ksigma += self.grd[i,j]()

#      elif self.type == 'g' and self.dim==2 :
 #       for m in self.sR :
  #          if self.V.dat[m] == self.NDT or isnan (self.V.dat[m]):  continue
   #         self.grd [ int (floor(0.499999999 + self.A[0].dat[m]/self.A[0].step)),
    #                   int (floor(0.499999999 + self.A[1].dat[m]/self.A[1].step))
     #                ] = self.V.dat[m]
      #  for y in self.A[1].NodS :
       #     for x in self.A[0].NodS :
        #        if self.fneNDT(x,y)==0 :
         #           self.grd[x,y].value = NaN

      elif self.type == 'g' and self.dim==3 :
                  StepInStep = []
                  A = []
                  for d in range (self.dim) :
                      A.append ( fi.readline().split() )
                      StepInStep.append(float(len(A[d])-1)/self.A[d].Ub)
#                      print self.A[d].Ub, len(A[d])
#                        Af = []
#                        for a in A : Af.append ( float(a) ) 
 #                       Arg.append ( Af )
 #                 print 'StepInStep', StepInStep
                  tb = loadtxt (fi,'double')
                  if co.printL : print ("shape", tb.shape)
                  for k in self.A[2].NodS :
                    for j in self.A[1].NodS :
                      for i in self.A[0].NodS :
#                        print k, j, i,   int(k*StepInStep[2]) * len(A[1]) + int(j*StepInStep[1])
                        self.grd[i,j,k].value = (tb[ int(k*StepInStep[2]) * len(A[1]) + int(j*StepInStep[1]) 
                                                    ,int(i*StepInStep[0])   
                                                   ] -self.V.avr)  #  значения в новых узлах
                        Ksigma += self.grd[i,j,k]()

      else :                                                    # POLY
#            print 'ZZZZZZZZZZ',self.grd[0],  self.grd[0]()
 #           1/0
            nums = head  #fi.readline().split()
            file_dim = int(nums[0])
#            file_maxP = int(nums[1]) - пока не нужно
            file_sizeP = int(nums[2])
            if co.printL : print ("file_dim=", file_dim," dim=", self.dim)
            if file_dim > self.dim :
                print ("*************************** ReadSol Poly  file_dim > dim", file_dim,">", self.dim)
                return;
            fi.readline()
            tb = loadtxt (fi,'double')
            fi.close()
            if co.printL : print ("ReadSol from", fName, "shape", tb.shape)

            if self.param :
                if tb.ndim == 1:  # одна строка  (только свободный член)
                    self.grd[0] = tb[0]
                else:
                    for i in range(min(file_sizeP, self.sizeP)):    self.grd[i] = tb[i, 0]
            else :
                for i in self.PolyR :  self.grd[i].value = 0   # обнуляем
                if file_dim == self.dim :
                  if tb.ndim == 1 :   #  одна строка  (только свободный член)
                    self.grd[0].value = tb[0]
                  else :
                    for i in range (min(file_sizeP, self.sizeP)) :    self.grd[i].value = tb[i,0]
                else :   # file_dim < self.dim      1 < 2
                    for i_file in range (file_sizeP) :
                        for i_self in self.PolyR :
                            if self.pow[i_self][0] == tb[i_file,1] and self.pow[i_self][1] == 0 :
                                self.grd[i_self] = tb[i_file,0]
      if co.printL > 0 : print ("End of ReadSol from", fName, 'Ksigma', Ksigma)
      fi.close()
           

    def InitByData ( self ) :
      if self.V.dat is None : return
      if self.type == 'g' and self.dim==0 :
        if self.V.dat[0] != self.NDT :
                self.grd = self.V.dat[0]

      elif self.type == 'g' and self.dim==1 :
 #       print 'CCCCCCCCCCCC',self.V.dat.shape
        for m in self.sR :
            if self.V.dat[m] == self.NDT or isnan (self.V.dat[m]): continue
            self.grd[int(floor(0.499999999 + self.A[0].dat[m]/self.A[0].step))] = self.V.dat[m]
        for x in self.A[0].NodS:
            if self.fneNDT(x) == 0:
                self.grd[x].value = NaN

      elif self.type == 'g' and self.dim==2 :
        print (self.V.name)

        for m in self.sR :
            if self.V.dat[m] == self.NDT or isnan (self.V.dat[m]):  continue
            self.grd [ int (floor(0.499999999 + self.A[0].dat[m]/self.A[0].step)),
                       int (floor(0.499999999 + self.A[1].dat[m]/self.A[1].step))
                     ] = self.V.dat[m]
        for y in self.A[1].NodS :
            for x in self.A[0].NodS :
                if self.fneNDT(x,y)==0 :
                    self.grd[x,y].value = NaN



    def SaveDeriv ( self, fName ) :                  #  В корзинку  !!
      if co.printL : print   ('SaveDeriv')
      if self.type == 'g' and self.dim==0 : return
      
      elif self.type == 'g' and self.dim==1 :
        A = self.A[0]
        V = self.V
        if fName == '' :  fName = co.Prefix+V.name + "(" +A.name+ ").der"
        fi = open ( fName, "w")
#        fi.write ( A.name + '\t' + V.name + "_der")
        fi.write ( A.name + '\t' + V.name + "_der \t#SvFver_62_tbl")
        for i in A.mNodSm :
            fi.write ( "\n" + str(A.min + A.step*i)
                     + "\t" + str( (self.grd[i+1]()-self.grd[i-1]()) / (2*A.step) ) )
        fi.close()
      elif self.type == 'g' and self.dim==2 :
        Ax = self.A[0]
        Ay = self.A[1]
        V = self.V
    # Y
        if fName == '' :  fName = co.Prefix+V.name + "(" +Ax.name+ ',' +Ay.name+ ").d_d"+ Ay.name
        fi = open ( fName, "w")
        fi.write ( Ax.name + '\t' + Ay.name + '\td' + V.name + "_d"+ Ay.name+ '\t#SvFver_62_matr2\n')       #  загол
        for i in Ax.NodS :  fi.write ( "\t" + str(Ax.min + Ax.step*i) )     #  точки по х
        for j in Ay.mNodSm :
            fi.write ( "\n" + str(Ay.min + Ay.step*j) )     #  точки по y
            for i in Ax.NodS :
                fi.write ( "\t" + str(V.avr + (self.grd[i,j+1]()-self.grd[i,j-1]()) /(2*Ay.step) ) )  #  значения
        fi.close()
    # X
        fName = co.Prefix+V.name + "(" +Ax.name+ ',' +Ay.name+ ").d_d"+Ax.name
        fi = open ( fName, "w")
        fi.write ( Ax.name + '\t' + Ay.name + '\td' + V.name + "_d"+Ax.name + '\t#SvFver_62_matr2\n')       #  загол
        for i in Ax.mNodSm :  fi.write ( "\t" + str(Ax.min + Ax.step*i) )     #  точки по х
        for j in Ay.NodS :
            fi.write ( "\n" + str(Ay.min + Ay.step*j) )     #  точки по y
            for i in Ax.mNodSm :
                fi.write ( "\t" + str(V.avr + (self.grd[i+1,j]()-self.grd[i-1,j]()) /(2*Ax.step) ) )  #  значения
      fi.close()
      print ("End of SaveDeriv")


    def grd_min_max ( self ) :
        mi = None
        ma = None
        if   self.dim==0 :
            return self.grd(), self.grd()
        elif self.dim==1 :
            for j in self.A[0].NodS :
                if self.fneNDT(j) :
                    if self.param : val = self.grd[j]
                    else          : val = self.grd[j]()
                    if isnan (val) : continue
                    if mi is None :
                        mi = val
                        ma = val
                    else :    
                        if val < mi : mi = val
                        if val > ma : ma = val
        else :
            for j in self.A[0].NodS :
              for i in self.A[1].NodS :
                if self.fneNDT(j,i) :
                    if self.param : val = self.grd[j,i]
                    else          : val = self.grd[j,i]()
                    if isnan (val) : continue
                    if mi is None :
                        mi = val
                        ma = val
                    else :    
                        if val < mi : mi = val
                        if val > ma : ma = val
        return mi, ma


    def  CopyMtr (self, copy_dat = False, name='') :                   # outofdate ?
        ret = self.GridParamClone(copy_dat)
        if name != '':  ret.V.name = name
        return ret


    def CopyInParam (self) :              #  всегда возвращает Парам
        if self.dim == 0 or self.type == 'p' : return None
        tmp = self.grd
        if self.param :
            return deepcopy(self)
        else :
            tmp = self.grd
            self.grd = None        # not copy pyomo strucher
            ret = deepcopy(self)
            self.grd = tmp

            ret.param = True

            if ret.dim==1 :
                ret.grd = zeros ( ret.A[0].Ub+1,float64 )
                for i in ret.A[0].NodS :
                        ret.grd[i] = self.grd[i]()
            elif ret.dim==2 :
                ret.grd = zeros ( (ret.A[0].Ub+1, ret.A[1].Ub+1),float64 )
                for i in ret.A[0].NodS :
                      for j in ret.A[1].NodS :
                        ret.grd[i,j] = self.grd[i,j]()
            return ret


    def interpol ( self, lev, X,Y=0,Z=0 ) :
        if lev == 3 :
            Zi = int(floor ( Z ))
            if Zi < 0            : Zi = 0 
            if Zi==self.A[2].Ub  : Zi=self.A[2].Ub-1
            dZ = Z-Zi
            if abs(dZ) < 1e-10   :  return  self.interpol ( lev-1, X,Y,Zi )       
            if abs(dZ-1) < 1e-10 :  return  self.interpol ( lev-1, X,Y,Zi+1 )     
            else                 :  return  self.interpol ( lev-1, X,Y,Zi ) * (1-dZ) + self.interpol ( lev-1, X,Y,Zi+1 ) * dZ       
        if lev == 2 :
            Yi = int(floor ( Y ))
            if Yi < 0            : Yi = 0 
            if Yi==self.A[1].Ub  : Yi=self.A[1].Ub-1
            dY = Y-Yi
            if abs(dY) < 1e-10   :  return  self.interpol ( lev-1, X,Yi,Z )
            if abs(dY-1) < 1e-10 :  return  self.interpol ( lev-1, X,Yi+1,Z ) 
            else                 :  return  self.interpol ( lev-1, X,Yi,Z ) * (1-dY) + self.interpol ( lev-1, X,Yi+1,Z ) * dY
        if lev == 1 :

            if self.type == 'G':
                ret = 0
                for i in self.A[0].NodSm:
                    dX = X - i
                    ret += (self.grd[i] * (1 - dX) + self.grd[i + 1] * dX) * tetta(1 - dX) * tetta(dX)
                return ret

            Xi = int(floor ( X ))
            if Xi < 0            : Xi = 0 
            if Xi==self.A[0].Ub  : Xi=self.A[0].Ub-1
            dX = X-Xi
            if abs(dX) < 1e-10   :  
                if self.dim == 1 :  return  self.grd[Xi       ] 
                if self.dim == 2 :  return  self.grd[Xi ,Y    ] 
                if self.dim == 3 :  return  self.grd[Xi ,Y , Z] 
            if abs(dX-1) < 1e-10 :   
                if self.dim == 1 :  return  self.grd[Xi+1       ]
                if self.dim == 2 :  return  self.grd[Xi+1 ,Y    ] 
                if self.dim == 3 :  return  self.grd[Xi+1 ,Y , Z] 
            else                 :
                if self.dim == 1 :  return  self.grd[Xi       ] * (1-dX) + self.grd[Xi+1       ] * dX
                if self.dim == 2 :  return  self.grd[Xi ,Y    ] * (1-dX) + self.grd[Xi+1 ,Y    ] * dX
                if self.dim == 3 :  return  self.grd[Xi ,Y , Z] * (1-dX) + self.grd[Xi+1 ,Y , Z] * dX


    def Ftbl ( self, n ) :
#      if self.type == 'g' : #or self.type == 'G':
      if self.type == 'g' or self.type == 'G':
        if   self.dim==1 :
            return self.interpol ( 1, self.A[0].dat[n]/self.A[0].step )
        elif self.dim==2 :
            return self.interpol ( 2, self.A[0].dat[n]/self.A[0].step,
                                      self.A[1].dat[n]/self.A[1].step )
        elif self.dim==3 :
            return self.interpol ( 3, self.A[0].dat[n]/self.A[0].step,
                                      self.A[1].dat[n]/self.A[1].step,
                                      self.A[2].dat[n]/self.A[2].step )
#      elif self.type == 'G':
 #         ret = 0
  #        X = self.A[0].dat[n]/self.A[0].step
   #       for i in self.A[0].NodSm :
    #          dX = X - i
     #         ret += (self.grd[i] * (1-dX) + self.grd[i+1] * dX) * tetta (1-dX)*tetta(dX)
      #    return ret


    def F1 ( self, Ar_real ) :   return self.F ( [ Ar_real ] )
    
    def F1_extra_const ( self, Ar_real ) :
            Ar_real = max (Ar_real, self.A[0].min )
            Ar_real = min (Ar_real, self.A[0].max )
            return self.F ( [ Ar_real ] )  


    def F2_extra_const ( self, Ar_real0, Ar_real1  ) :
            Ar_real0 = max (Ar_real0, self.A[0].min )
            Ar_real0 = min (Ar_real0, self.A[0].max )
            Ar_real1 = max (Ar_real1, self.A[1].min )
            Ar_real1 = min (Ar_real1, self.A[1].max )
            return self.F ( [ Ar_real0, Ar_real1 ] )  


    def F ( self, ArS_real ) :  # не проверенно
      if ( self.type == 'g' or self.type == 'G' ) and self.dim==1 :
        x = (ArS_real[0]-self.A[0].min)/self.A[0].step
        return self.interpol ( 1, x )
      elif self.type == 'g' and self.dim==2 :
        x = (ArS_real[0]-self.A[0].min)/self.A[0].step
        y = (ArS_real[1]-self.A[1].min)/self.A[1].step
        return self.interpol ( 2, x, y )
      elif self.type == 'g' and self.dim==3 :
          x = (ArS_real[0]-self.A[0].min)/self.A[0].step
          y = (ArS_real[1]-self.A[1].min)/self.A[1].step
          z = (ArS_real[2]-self.A[2].min)/self.A[2].step
#          print x,y,z
          return self.interpol ( 3, x, y, z )


    def sumX ( self ) :                                                                    # self.fneNDT(x) ??
      if self.type == 'g' and self.dim==1 :
        return  sum ( self.fneNDT(x-1) * self.fneNDT(x) * self.fneNDT(x+1) * self.f_gap(x) *
                     ( self.grd[x+1] - self.grd[x-1] )**2  
		    for x in self.A[0].mNodSm )
      elif self.type == 'g' and self.dim==2 :
        return  sum ( self.fneNDT(x-1,y) * self.fneNDT(x,y) * self.fneNDT(x+1,y) * self.f_gap(x,y) *
                     ( self.grd[x+1,y] - self.grd[x-1,y] )**2  
                    for y in self.A[1].NodS    for x in self.A[0].mNodSm )

    def grdCycle (self, x) :
        if x==-1             : return self.grd[self.A[0].Ub]
        if x==self.A[0].Ub+1 : return self.grd[0]
        return self.grd[x]

    def NDTCycle (self, x) :
        if x==-1             : return self.fneNDT(self.A[0].Ub)
        if x==self.A[0].Ub+1 : return self.fneNDT(0)
        return self.fneNDT(x)

    def sumXXcycle(self):
            if self.type == 'g' :
                if self.dim == 1:
                    return sum(self.NDTCycle(x - 1) * self.NDTCycle(x) * self.NDTCycle(x + 1) * self.f_gap(x) *
                               (self.grdCycle(x - 1) - 2 * self.grdCycle(x) + self.grdCycle(x + 1)) ** 2
                               for x in self.A[0].NodS) / (self.Nxx+2) / (1. / self.A[0].Ub) ** 4
            print ("SumXX:  No cycle")
            exit (-1)


    def grdCyc0E (self, x) :
        if x==self.A[0].Ub+1 : return self.grd[1]
        if x==-1             : return self.grd[self.A[0].Ub]  #  не нужно
        return self.grd[x]

    def NDTCyc0E (self, x) :
        if x==self.A[0].Ub+1 : return self.fneNDT(1)
        if x==-1             : return self.fneNDT(self.A[0].Ub)   #  не нужно
        return self.fneNDT(x)

    def sumXXcyc0E(self):
            if self.type == 'g':
                if self.dim == 1:
                    return sum(self.NDTCyc0E(x - 1) * self.NDTCyc0E(x) * self.NDTCyc0E(x + 1) * self.f_gap(x) *
                               (self.grdCyc0E(x - 1) - 2 * self.grdCyc0E(x) + self.grdCyc0E(x + 1)) ** 2
                               for x in self.A[0].mNodS) / (self.Nxx+1) / (1. / self.A[0].Ub) ** 4
            print ("SumXX:  No cycle")
            exit (-1)


    def sumXX ( self ) :
      if self.type == 'g' or self.type == 'G' :
          if   self.dim==1 :
             return  sum ( self.fneNDT(x-1) * self.fneNDT(x) * self.fneNDT(x+1) * self.f_gap(x) *
                        ( self.grd[x-1]-2*self.grd[x]+self.grd[x+1] )**2
		       for x in self.A[0].mNodSm )  /self.Nxx  /(1./self.A[0].Ub)**4
  #           return  sum ( self.fneNDT(x-1) * self.fneNDT(x) * self.fneNDT(x+1) * self.f_gap(x) *  # хитрый штраф
 #                          (0.00001+    ( self.grd[x-1]-2*self.grd[x]+self.grd[x+1] )**2 )**.125
#		       for x in self.A[0].mNodSm )  /self.Nxx  /(1./self.A[0].Ub)**4
          elif self.dim==2 :
             return  sum ( self.fneNDT(x-1,y) * self.fneNDT(x,y) * self.fneNDT(x+1,y) * self.f_gap(x,y) *
                        ( self.grd[x-1,y]-2*self.grd[x,y]+self.grd[x+1,y] )**2  
                       for y in self.A[1].NodS    for x in self.A[0].mNodSm ) / self.Nxx  / (1./self.A[0].Ub)**4
          elif self.dim==3 :
  #           return  sum ( self.fneNDT(x-1,y) * self.fneNDT(x,y) * self.fneNDT(x+1,y) * self.f_gap(x,y) *
             return  1 / ((self.A[2].Ub+1)*(self.A[1].Ub+1)*(self.A[0].Ub-1)) / (1./self.A[0].Ub)**4        \
                       * sum ( 
                        ( self.grd[x-1,y,z]-2*self.grd[x,y,z]+self.grd[x+1,y,z] )**2  
                       for z in self.A[2].NodS   for y in self.A[1].NodS    for x in self.A[0].mNodSm ) 




    def  SetVal ( self, val = 0 ) :
            for i in self.A[0].NodS :
                for j in self.A[1].NodS :
                    if self.param:
                      if self.grd[i,j] != self.NDT  :
                        self.grd[i,j] = val
                    else :
                      if self.grd[i,j].value != self.NDT  :
                        self.grd[i,j].value = val



    def Border (self,x,y) :
        if x == 0 :            return True
        if x == self.A[0].Ub : return True
        if y == 0 :            return True
        if y == self.A[1].Ub : return True
        return False

    def makeBorder (self) :
        Border = []
        for i in self.A[0].NodS :
            for j in self.A[1].NodS :
                if self.Border(i,j) :
                    Border.append([i,j])    
        return Border


    def PutPixel (self, i,j,Val, PixSize=1) :
        nb = self.Neighbors ( i,j, PixSize/2, True)
        for n in nb :
            x = n[0]
            y = n[1]
            if isnan(self.grd[x,y]): continue
            self.grd[x, y] = Val

    def Neighbors (self,x,y,dist=1,plus = False) :  # plus  сама точка
        Neighb = []
        idist = int(ceil(dist))
        for i in range( -idist, idist + 1, 1):
            if x+i < 0: continue
            if x+i > self.A[0].Ub: continue
            for j in range( -idist, idist + 1, 1):
                if y+j < 0: continue
                if y+j > self.A[1].Ub: continue
                if i==0 and j==0  and not plus: continue
                if i**2 + j**2 > dist**2 : continue
                Neighb.append([x+i, y+j])
#        if x != 0 :            Neighb.append([x-1,y])
 #       if x != self.A[0].Ub : Neighb.append([x+1,y])
  #      if y != 0 :            Neighb.append([x,y-1])
   #     if y != self.A[1].Ub : Neighb.append([x,y+1])
        return Neighb


    def FloodFillReal (self, xy, BordVal,FillVal) :
        self.FloodFill([self.A[0].getPointNum (xy[0]), self.A[1].getPointNum (xy[1])], BordVal, FillVal)


    def FloodFill (self, xy_in, BordVal,FillVal) :
        quer = [xy_in]   # очередь
        pos = 0
        while len (quer) > pos :
            xy = quer[pos]
            if     self.grd[xy[0], xy[1]] != BordVal \
               and self.grd[xy[0], xy[1]] != FillVal \
               and  not isnan(self.grd[xy[0], xy[1]]) :
                    self.grd[xy[0], xy[1]] = FillVal
                    quer = quer + self.Neighbors (xy[0],xy[1])
            pos += 1
 #           print 'QU', pos, len (quer)


        print ('FF', xy, self.grd[xy[0],xy[1]])
        if     self.grd[xy[0],xy[1]] == BordVal \
            or self.grd[xy[0],xy[1]] == FillVal \
            or isnan(self.grd[xy[0],xy[1]]) :
            return
        star += 1
        if star >= 998: return
        self.grd[xy[0],xy[1]] = FillVal
        print (star, xy[0],xy[1])
        nei = self.Neighbors (xy[0],xy[1])
        for xy1 in nei :
            self.FloodFill (xy1, BordVal,FillVal,star)
        return



    def getVal (self, x, y=NaN) :                        #  если все ОК возвращает значение
        if x < 0:  return NaN
        if x > self.A[0].Ub:  return NaN
        if self.dim == 1 :  return self.grdNaN (x)                  # real ???
#            if self.fneNDT(x) == 0: return NaN
 #           if self.param:  return self.grd[x]
  #          else:           return self.grd[x]()
        else :
            if y < 0:  return NaN
            if y > self.A[1].Ub:  return NaN
            return self.grdNaN(x,y)                     # real ???
 #           if self.fneNDT(x,y) == 0 : return NaN
  #          if self.param :   return self.grd[x,y]
   #         else          :   return self.grd[x,y]()


    def Smoothing (self, dh=NaN, max_ang_grad=NaN, mask=None, mVal=None) :     # усреднение по 9 точкам  для точек mask=mVal
        print ("Smoothing start ")
        num_change = 0
        if not isnan(max_ang_grad) :
            max_ang_rad = max_ang_grad /180.*pi
            print (max_ang_grad, max_ang_rad)
#        XYs = []
        for y in self.A[1].NodS :
            for x in self.A[0].NodS : # XYs.append([x,y])
        #for xy in XYs :
    #            x = xy[0]
     #           y = xy[1]
                if isnan(self.grd[x, y]) : continue
                if not mask.grd[x,y] is None :
                    if mask.grd[x,y] != mVal: continue
                sum = 0
                num = 0
                max_ang = .0
                for i in range (-1,2,1) :
                    for j in range(-1, 2, 1):
 #                       print 'j', j
                        v = self.getVal(x+i,y+j)
                        if isnan(v) : continue
                        if (not isnan(max_ang_grad)) and i!=0 and j!=0 :         # по углу
                            ang = abs((v-self.grd[x,y])/sqrt((i*self.A[0].step)**2+(j*self.A[0].step)**2))
                            if ang >= max_ang :
                                max_ang = ang
                                v_ang = v
                                v_mask = mask.grd[x+i,y+j]
                        if not isnan(dh):
                            num += 1
                            sum += v
                if not isnan(max_ang_grad):
                    if max_ang > max_ang_rad :
                        print ('SrezaemAng: ', max_ang, v_ang, self.grd[x, y], x, y, x + i, y + j,)
                        self.grd[x, y] = 0.7 * self.grd[x, y] + 0.3 * v_ang
                        print (self.grd[x, y], v_mask)
                        num_change += 1

                if not isnan(dh):
                    if num <= 1: continue
                    new = sum/num
                    if abs (new-self.grd[x, y]) < dh: continue
#                    if abs ( (num*new-self.grd[x, y])/(num-1)-self.grd[x, y] ) < dh: continue
                    print ('Srezaem: ', new, self.grd[x, y], x,y)
                    self.grd[x, y] = new
                    num_change += 1
        print  ("num_change",    num_change)

    def d_dx(self,x,y=NaN): #  на границе  левая и правая  иначе центральная
            i1 = max ( x-1, 0)
            i2 = min ( x+1, self.A[0].Ub )
            if self.type == 'g' and self.dim == 1:
                v1 = self.getVal(i1)
                v2 = self.getVal(i2)
            elif self.type == 'g' and self.dim == 2:
                v1 = self.getVal(i1,y)
                v2 = self.getVal(i2,y)
            if isnan (v1) : return NaN
            if isnan (v2) : return NaN

            return (v2 - v1)/(i2 - i1) / self.A[0].step

    def d_dy(self, x, y):  # на границе  левая и правая  иначе центральная
        i1 = max(y - 1, 0)
        i2 = min(y + 1, self.A[1].Ub)
        if self.type == 'g' and self.dim == 2:
            v1 = self.getVal(x, i1)
            v2 = self.getVal(x, i2)
        if isnan(v1): return NaN
        if isnan(v2): return NaN

        return (v2 - v1) / (i2 - i1) / self.A[1].step



    def Make_1_Deriv(self, der='x'):
        if co.printL: print   ('MakeDeriv1')
        ret = self.GridParamClone()
#        ret = self.Clone()
        if self.type == 'g' and self.dim == 1:
            for i in self.A[0].NodS: ret.grd[i] = self.d_dx (i)
        elif self.type == 'g' and self.dim == 2:
            for i in self.A[0].NodS:
                for j in self.A[1].NodS:
                    if der=='x' :   ret.grd[i,j] = self.d_dx(i,j)
                    else        :   ret.grd[i,j] = self.d_dy(i,j)
        return ret

    def TiltAngle (self) :
        if self.type == 'g' and self.dim == 2:
            X = self.Make_1_Deriv ()
            Y = self.Make_1_Deriv ('y')
            for i in self.A[0].NodS:
                for j in self.A[1].NodS:
                    X.grd[i,j] = sqrt (X.grd[i,j]**2+Y.grd[i,j]**2)
            return X
        return None

    def makeMtrParamVnameSetG ( self, Vname, gr_value = 0 ) :
        ret = gFun2(self)
        ret.grd = zeros((ret.A[0].Ub + 1, ret.A[1].Ub + 1), float64)
        if gr_value != 0:
            for i in ret.A[0].NodS:
                for j in ret.A[1].NodS:
                    ret.grd[i, j] = gr_value
        ret.V.name = Vname
        ret.param = True
        ret.V.avr = 0   # 19.12.19
        return ret



    def sumY ( self ) :
        return  sum ( self.fneNDT(x,y-1) * self.fneNDT(x,y) * self.fneNDT(x,y+1) * self.f_gap(x,y) *
                     ( self.grd[x,y+1] - self.grd[x,y-1] )**2 
                    for y in self.A[1].mNodSm  for x in self.A[0].NodS )


    def sumYY ( self ) :
          if   self.dim==2 :
              return  sum ( self.fneNDT(x,y-1) * self.fneNDT(x,y) * self.fneNDT(x,y+1) * self.f_gap(x,y) *
                     ( self.grd[x,y-1]-2*self.grd[x,y]+self.grd[x,y+1] )**2 
                    for y in self.A[1].mNodSm  for x in self.A[0].NodS )   / self.Nyy  / (1./self.A[1].Ub)**4
          elif self.dim==3 :
             return  1 / ((self.A[2].Ub+1)*(self.A[1].Ub-1)*(self.A[0].Ub+1)) / (1./self.A[1].Ub)**4        \
                       * sum ( 
                        ( self.grd[x,y-1,z]-2*self.grd[x,y,z]+self.grd[x,y+1,z] )**2  
                       for z in self.A[2].NodS   for y in self.A[1].mNodSm    for x in self.A[0].NodS ) 

    
    def sumXY ( self ) :
          if   self.dim==2 :
              return  sum ( self.fneNDT(x+1,y+1) * self.fneNDT(x+1,y-1) * self.fneNDT(x-1,y+1) * self.fneNDT(x-1,y-1) * self.f_gap(x,y) *
                     ( self.grd[x+1,y+1]-self.grd[x+1,y-1]-self.grd[x-1,y+1]+self.grd[x-1,y-1] )**2 
                    for y in self.A[1].mNodSm  for x in self.A[0].mNodSm )                \
                                    * 2. / self.Nxy * 0.25 / (1./self.A[0].Ub)**2 / (1./self.A[1].Ub)**2
          elif self.dim==3 :
             return   2. / ((self.A[2].Ub+1)*(self.A[1].Ub-1)*(self.A[0].Ub-1)) * 0.25 / (1./self.A[0].Ub)**2 / (1./self.A[1].Ub)**2   \
                       * sum ( 
                        ( self.grd[x+1,y+1,z]-self.grd[x+1,y-1,z]-self.grd[x-1,y+1,z]+self.grd[x-1,y-1,z] )**2  
                       for z in self.A[2].NodS   for y in self.A[1].mNodSm    for x in self.A[0].mNodSm ) 

    
#    def Freal ( self, ArS_real ) :  
##        return ( self.F( [ (ArS_real[0]-self.A[0].min)/self.A[0].step,  
##                           (ArS_real[1]-self.A[1].min)/self.A[1].step ] )
#        return ( self.F( [ (ArS_real[0]-self.A[0].min),  
#                           (ArS_real[1]-self.A[1].min) ] )
#                 + self.V.avr
#               )

    def SaveSection ( self, fName, sect ) :
        Ax = self.A[0]
        Ay = self.A[1]
        V = self.V
        if fName == '' :  fName = V.name + "(" +Ax.name+ ',' +Ay.name+ ")SvF.Sec" 
        fi = open ( fName, "w")
        fi.write ( Ax.name + '\t' + Ay.name + '\t' + V.name + "_SvF\n")       #  загол
        for s in sect :  fi.write ( "\t" + str(s) )     #  точки по х
        for j in Ay.NodS :
            fi.write ( "\n" + str(Ay.min + Ay.step*j) )     #  точки по y
            for s in sect :
#########                fi.write ( "\t" + str(self.Freal([s, Ay.min + Ay.step*j])() ) )      #  значения
                fi.write ( "\t" + str(self.F([s, Ay.min + Ay.step*j])() ) )      #  значения
        fi.close()
        print("END of SaveSection")



#    def interPol2a ( self,x,y ) :
 #       Xi = floor ( x );  Yi = floor ( y )
  #      if Xi==self.A[0].Ub : Xi=self.A[0].Ub-1     # убирает данное с (не 0) границы.
   #     if Yi==self.A[1].Ub : Yi=self.A[1].Ub-1     
    #    return (   self.grd[Xi  ,Yi  ] * ( 1- (x-Xi) ) * ( 1- (y-Yi) ) 
     #            + self.grd[Xi+1,Yi  ] * (    (x-Xi) ) * ( 1- (y-Yi) ) 
#	         + self.grd[Xi  ,Yi+1] * ( 1- (x-Xi) ) * (    (y-Yi) ) 
#	         + self.grd[Xi+1,Yi+1] * (    (x-Xi) ) * (    (y-Yi) ) )



    def SaveTbl ( self, fName='' ) :
        Ax = self.A[0]
        Ay = self.A[1]
        V = self.V
        if fName == '' :  fName = "SvF_"+V.name + "(" +Ax.name+ ',' +Ay.name+ ").tbl"
        fi = open ( fName, "w")
        fi.write ( Ax.name + '\t' + Ay.name + '\t' + V.name + "_SvF")       #  загол
        for j in Ay.NodS :
            for i in Ax.NodS :
                fi.write ( "\n" + str(Ay.min + Ay.step*j) )     #  точки по y
                fi.write ( "\t" + str(Ax.min + Ax.step*i) )     #  точки по х
#                print >> fi, "\t" + "%20.16g" % (grdNaNreal(i,j)),  # значения    19.12.19
                fi.write( "\t" + "%20.16g" % (grdNaNreal(i,j)) )  # значения    19.12.19

#                if not self.neNDT[i,j] :
 #                   print >> fi, "\t" + str (self.NDT),
  #              else :
   #                 if self.param :
    #                    print >> fi, "\t" + "%20.16g" % ((V.avr + self.grd[i,j])),   #  значения
     #               else :
      #                  print >> fi, "\t" + "%20.16g" % ((V.avr + self.grd[i,j]())),
        fi.close()
        print ("End of SaveTbl")




    def SaveGrid ( self, fn, TranspGrid = 'N' ) :
        if TranspGrid == 'N':
            Ax = self.A[0]
            Ay = self.A[1]
        else :
            Ay = self.A[0]
            Ax = self.A[1]
        if fn == '' : fn = self.V.name + "(" +Ax.name+ "," +Ay.name+ ")_SvF.asc"   
        f = open ( fn, "w")
        f.write( "NCOLS "   + str(Ax.Ub+1) )
        f.write( "\nNROWS " + str(Ay.Ub+1) )
        XLLCORNER = Ax.min-Ax.step*.5                   # на край ячейки
        YLLCORNER = Ay.min-Ay.step*.5                   # на край ячейки
        f.write( "\nXLLCORNER " + str(XLLCORNER) )
        f.write( "\nYLLCORNER " + str(YLLCORNER) )
        f.write( "\nCELLSIZE " + str(Ax.step) )            # stepX !
        f.write( "\nNODATA_VALUE " + str(self.NDT) )
        for y in range(Ay.Ub+1) :
          f.write( "\n" )
          for x in range(Ax.Ub+1) :
            if TranspGrid == 'N':
                if self.type == 'g' :
                    f.write(" " + str(self.grdNDTreal(x, Ay.Ub-y)))
#                    if self.param :
 #                       f.write ( " " + str( self.grd[x, Ay.Ub-y] + self.V.avr ) + " " )
  #                  else :
   #                     if (not self.neNDT[ x,Ay.Ub-y]) or isnan(self.grd[ x,Ay.Ub-y]) :
    #                        f.write ( " " + str (self.NDT) )
     #                   else :
      #                      f.write ( " " + str( self.grd[x, Ay.Ub-y]() + self.V.avr ) + " " )
       #         else :
        #          f.write ( " " + str( self.F([x, Ay.Ub-y])() + self.V.avr ) + " " )
            else :
              f.write(" " + str(self.grdNDTreal(Ay.Ub-y,x)))
#              if (not self.neNDT[ Ay.Ub-y,x] ) or isnan(self.grd[Ay.Ub-y,x]) :
 #                f.write ( " " + str (self.NDT) )
  #            else :
   #             if self.type == 'g' :
    #                if self.param:
     #                   f.write ( " " + str( self.grd[Ay.Ub-y,x] + self.V.avr ) + " " )
      #              else:
       #                 f.write ( " " + str( self.grd[Ay.Ub-y,x]() + self.V.avr ) + " " )
        #        else :
         #         f.write ( " " + str( self.F([Ay.Ub-y,x])() + self.V.avr ) + " " )
        f.close()
        print ("END of SaveGrid")



        


        
        


#########################################################################
# POLY            ********************************************************
class pFun (Fun) :                                
    def __init__ (self, FuncR ) :
        self.CopyFromFun ( FuncR, FuncR.param,  'p' )   # 27
#        print self.param
#        self.Ini ( FuncR, 'p' )
#        print (self.mu)
        self.sizeP = PolySize ( self.dim, self.maxP )
        self.PolyR = range ( self.sizeP )
        self.pow   = CrePolyPow ( self.dim, self.maxP )

        self.Dx, self.Cx = CreDeriv1Pow ( self.pow, [], 0 )
        if self.dim > 1 :
            self.Dy, self.Cy = CreDeriv1Pow(self.pow, [], 1)

        self.Dxx, self.Cxx = CreDeriv2Pow(self.pow, 0, 0)
        if self.dim > 1 :
            self.Dyy, self.Cyy = CreDeriv2Pow ( self.pow, 1, 1 )
            self.Dxy, self.Cxy = CreDeriv2Pow ( self.pow, 0, 1 )




    def derivXd1 (self, x ) :
        return  sum (  self.Cx[i] * self.grd[i] * x**self.Dx[i][0]     for i in self.PolyR )
    def derivX   (self, x, y ) :
        return  sum (  self.Cx[i] * self.grd[i] * x**self.Dx[i][0]
                                                * y**self.Dx[i][1]     for i in self.PolyR )
    def derivY   (self, x, y ) :
        return  sum (  self.Cy[i] * self.grd[i] * x**self.Dy[i][0]
                                                * y**self.Dy[i][1]     for i in self.PolyR )

    def derivXXd1 (self, x ) :
        return  sum (  self.Cxx[i] * self.grd[i] * x**self.Dxx[i][0]   for i in self.PolyR )
    def derivXX (self, x, y ) :
        return  sum (  self.Cxx[i] * self.grd[i] * x**self.Dxx[i][0]
                                                 * y**self.Dxx[i][1]   for i in self.PolyR )
    def derivYY (self, x, y ) :
        return sum (  self.Cyy[i] * self.grd[i] * x**self.Dyy[i][0]
                                                * y**self.Dyy[i][1]    for i in self.PolyR )
    def derivXY (self, x, y ) :
        return sum (  self.Cxy[i] * self.grd[i] * x**self.Dxy[i][0]
                                                * y**self.Dxy[i][1]    for i in self.PolyR )
    def sumX(self):
        if self.dim == 1:
            return sum(self.fneNDT(x) * self.f_gap(x) *
                       (self.derivXd1(x * self.A[0].step / self.A[0].ma_mi)) ** 2
                       for x in self.A[0].NodS) / self.Nxx
        else:
            return sum(self.fneNDT(x, y) * self.gap[x, y] *
                       (self.derivX(x * self.A[0].step / self.A[0].ma_mi, y * self.A[1].step / self.A[1].ma_mi)) ** 2
                       for y in self.A[1].NodS for x in self.A[0].NodS) / self.Nxx
    def sumY(self):
            return sum(self.fneNDT(x,y) * self.gap[x, y] *
                       (self.derivY(x * self.A[0].step / self.A[0].ma_mi, y * self.A[1].step / self.A[1].ma_mi)) ** 2
                       for y in self.A[1].NodS for x in self.A[0].NodS) / self.Nyy

    def sumXX ( self ) :
        if self.dim == 1 :
            return  sum (  self.fneNDT(x) * self.f_gap(x) *
                          ( self.derivXXd1 ( x*self.A[0].step/self.A[0].ma_mi ) )**2
                        for x in self.A[0].NodS )  /self.Nxx  
##!!                        for x in self.A[0].NodS ) 
        else:
            return  sum (  self.fneNDT(x,y) * self.f_gap(x,y) *
                     ( self.derivXX ( x*self.A[0].step/self.A[0].ma_mi, y*self.A[1].step/self.A[1].ma_mi ) )**2  
#                     ( self.derivXX ( x, y ) )**2  
                    for y in self.A[1].NodS    for x in self.A[0].NodS )  /self.Nxx
    def sumYY ( self ) :
        return  sum (  self.fneNDT(x,y) * self.f_gap(x,y) *
                     ( self.derivYY ( x*self.A[0].step/self.A[0].ma_mi, y*self.A[1].step/self.A[1].ma_mi ) )**2  
#                     ( self.derivYY ( x, y ) )**2  
                    for y in self.A[1].NodS    for x in self.A[0].NodS ) /self.Nyy
    def sumXY ( self ) :
        return  sum (  self.fneNDT(x,y) * self.f_gap(x,y) *
                     ( self.derivXY ( x*self.A[0].step/self.A[0].ma_mi, y*self.A[1].step/self.A[1].ma_mi ) )**2  
#                     ( self.derivXY ( x, y ) )**2  
                    for y in self.A[1].NodS    for x in self.A[0].NodS ) /self.Nxy

    def Ftbl ( self, n ) :
        x = self.A[0].dat[n]/self.A[0].ma_mi
        if self.dim == 1 :
            return sum ( self.grd[i] * x**self.pow[i][0] for i in self.PolyR )
        else :            
#            y = self.tbl[n,self.A[1].num]/self.A[1].step
            y = self.A[1].dat[n]/self.A[1].ma_mi
            return sum ( self.grd[i] * x**self.pow[i][0] * y**self.pow[i][1] for i in self.PolyR )
        
        
    def F ( self, ArS_real ) :  # не проверенно
###        x = ArS_real[0]-self.A[0].min
        x = (ArS_real[0]-self.A[0].min)/self.A[0].ma_mi
        if self.dim == 1 :
            return sum ( self.grd[i] * x**self.pow[i][0]
                        for i in self.PolyR )  + self.V.avr 
        else :
###            y = ArS_real[1]-self.A[1].min
            y = (ArS_real[1]-self.A[1].min)/self.A[1].ma_mi
            return sum ( self.grd[i] * x**self.pow[i][0] * y**self.pow[i][1]
                        for i in self.PolyR )  + self.V.avr


#        Ax = self.A[0]
 #       if self.dim == 1:
  #          for x in Ax.NodS:
   #             if self.neNDT[x] == 1 :
    #                fun.grd[x] = self.F([Ax.min + Ax.step * x])()
     #           else : fun.grd[x] = self.NDT
      #  else:  # dim 2
       #     Ay = self.A[1]
        #    for x in Ax.NodS:
         #       for y in Ay.NodS:
          #          if self.neNDT[x,y] == 1 :
           #             fun.grd[x,y] = self.F([Ax.min + Ax.step* x, Ay.min + Ay.step* y ])()
            #        else : fun.grd[x,y] = self.NDT
#        fun.neNDT = self.neNDT
 #       fun.NDT  = self.NDT
  #      return fun


#    def Draw ( self, Transp = False ) :
 #           fung = self.GridParamClone(True)
  #          fung.Draw( Transp )
   #         return


