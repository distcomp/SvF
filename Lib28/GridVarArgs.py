# -*- coding: cp1251 -*-

from  numpy import *

from  GaKru import *

import sys
from   copy   import *



import COMMON as com
from Tools import *

import openpyxl


def  getName ( obj ) :
        if type (obj) == type ('abc') : return obj
        return obj.name


def myrange(mi_, ma_, st):  # mi <= ret  <= ma   ret[0] = mi  ret[-1] = ma  возможно округление 1е-10
        mi = float(mi_)        #    conflict    float <-> float64   ???????????????????  #########################
        ma = float(ma_)
        ret = []
        num = 0
        elem = mi
        #        while elem <= ma :
        #           ret.append (elem)
        #          num += 1
        #         elem = mi + st * num
        #    if len( ret ) > 0 :
        #       if (ret[-1]-ma) / st < 1e-10 :  ret[-1] = ma
        #      else                         :  ret.append (elem)
        while elem <= ma:
            ret.append(elem)
            num += 1
            elem = mi + st * num
            if abs((elem - ma) / st) < 1e-10:
                ret.append(ma)
                break
        else:
            ret.append(ma)  # приращение неполное !
        #    if len( ret ) > 0 :
        #       if (ret[-1]-ma) / st < 1e-10 :  ret[-1] = ma
        #      else                         :  ret.append (elem)
        return ret


class Vari :                  #  var  ###################################
  def __init__ (self, name) :
      self.name = name
#      self.Dnum = -99
#      self.num  = -99
      self.avr     = 0
      self.sigma   = 1
      self.sigma2  = 1
      self.average = 0
      self.dat     = None           
#      self.NoR = 0    ##################################### ???
      
  def Vprint(self) :
#      print "Var", self.name, self.num, "NoR", self.NoR, "avr", self.avr, "sig", self.sigma
      print ("Var", self.name, "avr", self.avr, "sig", self.sigma)

  def Normalization (self, VarNormalization) :
        if self.dat is None :  return
        NoR = 0
        self.average = 0
        for m in self.dat:
            if  not isnan(m):
                self.average += m
                NoR += 1
        self.average = self.average / NoR
 #       print 'Vari', NoR, self.average
        if NoR ==1 :
            self.sigma2 = 1
        else :
            self.sigma2 = 0
            for m in self.dat:
                if  not isnan(m):
                    self.sigma2 += (m-self.average)**2
            self.sigma2 =  self.sigma2 / (NoR-1) 
        self.sigma = sqrt ( self.sigma2 )
 #       self.Vprint()

        self.avr = self.average
        if VarNormalization == 'Y' :
            for m in self.dat :   #####################
               if not isnan(m):  m -= self.avr  ################
#            for m in range(data.NoR):  #####################
 #              if data.tbl[m, self.num] != data.NDT:  data.tbl[m, self.num] -= self.avr  ################
        else :
            self.avr = 0

class Grid:
    def __init__ (self, nameOrGrid, gmin=NaN, gmax=NaN, step=NaN, ind = None, oname = None) :
        co.LastGrid = self
        self.className = 'Grid'
#        print ('Grid', type(nameOrGrid))
        if type(nameOrGrid) == type('abc'):
            self.name = nameOrGrid
            self.step = step
            self.min  =  gmin
            self.max  =  gmax
            self.ind  =  ind
            self.oname = oname
        else :
            self.name  = nameOrGrid.name
            self.step  = nameOrGrid.step
            self.min   = nameOrGrid.min
            self.max   = nameOrGrid.max
            self.ind   = nameOrGrid.ind
            self.oname = nameOrGrid.oname
#            print ('oo', self.oname)
        if com.printL : print ('Grid init by', self.name, self.min, self.max, self.step, self.ind)

        if self.ind   is None : self.ind = 'i__' + self.name
        if self.oname is None : self.oname = self.name
        if isfloat(self.ind) : print (self.name, '****index must be a name:', self.ind);  exit(-1)


        self.Ub     =-1         # сетка от [0 до Ub]
        self.NodS   = [] #0
        self.mNodSm = 0
        self.mNodS  = 0
        self.NodSm  = 0
        self.Val    = []
        self.FlNodS   = 0
        self.mFlNodSm = 0
        self.mFlNodS  = 0
        self.FlNodSm  = 0
        self.ma_mi    = 0

        self.dat = None             #  use in functions

        if isfloat(self.min) and isfloat(self.max) and isfloat(self.step) :  #self.GridInit ()  # 20.12.19

#            if not ( isnan(self.min) or isnan(self.max) or isnan(self.step) ) :  self.GridInit ()  # 20.12.19
 #           if ( isnan(self.min) or isnan(self.max) or isnan(self.step) ) :
                self.GridInit ()  # 20.12.19
        elif not com.Preproc :  self.GridInit ()
        return

    def GridInit(self):

            if isnan(self.min) and (not com.curentTabl is None) :
                    data = com.curentTabl.getField_tb(self.oname)
                    self.min = float(data.min(0))  ###   &&&&&&&&&&&&??????????????????? float64
                    if com.printL: print ('self.min', self.min)
            if isnan(self.max) and (not com.curentTabl is None) :
                    data = com.curentTabl.getField_tb(self.oname)
                    self.max = float(data.max(0))  ###   &&&&&&&&&&&&??????????????????? float64
                    if com.printL: print ('self.max', self.max)

            if isnan(self.min) or isnan(self.max) :  return

            if isnan(self.step): self.step = -50
            if self.step < 0: self.step = - (self.max - self.min) / self.step;
            self.ma_mi = self.max - self.min
            self.Normalization_UbSets()
            self.makeVal()


    def indNormVal ( self, norm_val ):
        ret = int ( floor ( norm_val/self.step + 0.499999999 ) )
        ##  check ?????
        return ret

    def indByVal ( self, val ):
        ret = int ( floor ( (val-self.min)/self.step + 0.499999999 ) )
        ##  check ?????
        return ret

    def makeVal (self) :
        if co.printL == 1: print ('makeVal', self.Ub, self.step)
        if self.Ub == -1 : return
        self.Val = []
        for i in self.NodS : self.Val.append ( self.min + i * self.step )

    def makeSets  (self) :
        if self.Ub == -1 : return
        self.NodS   = range(0, self.Ub + 1)
        self.mNodSm = range(1, self.Ub)
        self.mNodS  = range(1, self.Ub + 1)
        self.NodSm  = range(0, self.Ub)
        self.FlNodS   = myrange(self.min,           self.max,           self.step)
        self.mFlNodSm = myrange(self.min+self.step, self.max-self.step, self.step)
        self.FlNodSm  = myrange(self.min,           self.max-self.step, self.step)
        self.mFlNodS  = myrange(self.min+self.step, self.max,           self.step)

    def setUb (self) :
#        if self.max==FLOMAX or self.min==-FLOMAX or self.step==FLOMAX : return
 #       if isnan( self.max ) or isnan( self.min ) or isnan( self.step ) : return
  #      if self.step < 0 : self.step = - (self.max-self.min) / self.step;       ####  Не убирать - для функций без измерений
        floatUb = (self.max - self.min) / self.step
        self.Ub = int(ceil(floatUb))
#        print self.Ub, self.max, self.min, self.step
        if self.Ub > 0 :
            if abs(floatUb - (self.Ub - 1)) / self.Ub < 1e-10:  self.Ub -= 1    ###################  Округление Уточнить -13 #######

    def getPointNum (self, val) :                          # узел снизу
        ret = int ( (val-self.min ) / self.step + 0.5 )
        if ret < 0 :
            print ("\n\n\n\n Out of range", ret)
            return 0
        if ret > self.Ub :
            print ("\n\n\n\n Out of range", ret)
            return self.Ub
        return ret

    def ValToInd (self, val) :
        return self.getPointNum ( val)

    def IndToVal (self, ind) :
        return self.min + ind * self.step
    
    def myprint(self) :
        print ("Grid", self.name, "mm", self.min, self.max, "st", self.step, 'Up', self.Ub)
    def Gprint(self) :
        print ("Grid", self.name, "mm", self.min, self.max, "st", self.step, 'Up', self.Ub)

    def printM(self):
        printS (self.name+"{" + str(self.min), self.max, self.step, str(self.Ub) + '} |')

    def Normalization_UbSets  (self) :

        if not self.dat is None :  self.dat -= self.min     # не приводим к штукам шагов
        self.setUb()
        self.makeSets()


    def Aprint(self) :
      print ("Arg", self.name, "mm", self.min, self.max, "st", self.step, 'Up', self.Ub)

    def CutOutMinMax ( self, val ) :
        if val < self.min :
            print ('Cut min', self.name, val, self.min)
            val = self.min      
        if val > self.max :
            print ('Cut max', self.name, val, self.max)
            val = self.max
        return val
    
class Domain :
    def __init__( self, name, gridX, visX=0, gridY=None, visY=0):
        self.className = 'Domain'
        self.name  = name
        self.A     = [gridX]
        if not gridY is None : self.A.append(gridY)
        self.dim   = len(self.A)
        self.visX  = float(visX)
        self.visY  = float(visY)

        if com.Preproc : self.isDat = None
        else           : self.Make_isDat()

    def Make_isDat(self):
        if self.visX==0 and self.visY==0 : return
        if self.dim == 0:  return

 #       print 'Make_neNDT',len(self.A[0].dat)
        A0 = self.A[0]
        mmm=A0.min
        A0_dat = com.curentTabl.getField_tb(A0.oname)
        if self.visX < 0: self.visX = - self.visX * A0.step;

        if self.dim == 1:
#            self.gap = ones(A0.Ub + 1, int8)                   # 27
                isDat = zeros(A0.Ub + 1, int8)
#                if not self.V.dat is None:    #  for what ?    27
 #                   for m in range(self.NoR):
  #                      if self.V.dat[m] != self.NDT:
   #                         isDat[int(floor(0.499999999 + A0.dat[m] / A0.step))] = 1
                for m in range(self.NoR):
#                    for x in range(max(0, int(ceil((A0_dat[m] - self.visX) / A0.step))),
#                                   min(A0.Ub, int(floor((A0_dat[m] + self.visX) / A0.step))) + 1):
                    for x in range(max(0, A0.indByVal(A0dat - self.visX)),
                                    min(A0.Ub, A0.indByVal(A0dat + self.visX)) + 1):
                            isDat[x] = 1
        else:
                A1 = self.A[1]
                A1_dat = com.curentTabl.getField_tb(A1.oname)
                if self.visY < 0: self.visY = - self.visY * A1.step;

                #           self.gap = ones((A0.Ub + 1, A1.Ub + 1), int8)
                isDat = zeros((A0.Ub + 1, A1.Ub + 1), int8)

                for m,A0dat in enumerate(A0_dat):
                    for x in range(max(0, A0.indByVal(A0dat - self.visX)),
                                   min(A0.Ub, A0.indByVal(A0dat + self.visX)) + 1):
                        for y in range(max(0, A1.indByVal(A1_dat[m] - self.visY)),
                                       min(A1.Ub, A1.indByVal(A1_dat[m] + self.visY)) + 1):
                            isDat[x, y] = 1



        self.isDat = isDat
#        self.calcNDTparam()
        return


def cnstrArg (name, mi, ma, step) :
    ret = Arg (name)
    ret.min = mi
    ret.max = ma
    ret.step = step
    return ret


def intersection_step (A1,A2) :
    ret = A1.name
    ret.min = max(A1.min,A2.min)
    ret.max = min(A1.max,A2.max)
    ret.step = min(A1.step,A2.step)
    ret.Ub = int( (ret.max - ret.min) / ret.step )
    ret.makeSets()
    return ret

