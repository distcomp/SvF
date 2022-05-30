# -*- coding: cp1251 -*-

from  numpy import *
from  GaKru import *
import sys
from   copy   import *
from Object import *
#import COMMON as com
from Tools import *
import openpyxl

def  getName ( obj ) :
        if type (obj) == type ('abc') : return obj
        return obj.name

def myrange(mi_, ma_, st):  # mi <= ret  <= ma   ret[0] = mi  ret[-1] = ma  возможно округление 1е-10
        if mi_ > ma_:  return []    # 08/07/2021
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


class Grid (Object):
    def __init__ (self, nameOrGrid, gmin=NaN, gmax=NaN, step=NaN, ind = None, oname = None) :
#        Object.__init__(self, nameOrGrid, 'Grid')
        co.LastGrid = self
        self.className = 'Grid'
        if type(nameOrGrid) == type('abc'):
            name = nameOrGrid
            self.step = step
            self.min  =  gmin
            self.max  =  gmax
            self.ind  =  ind
            self.oname = oname
        else :
            name  = nameOrGrid.name
            self.step  = nameOrGrid.step
            self.min   = nameOrGrid.min
            self.max   = nameOrGrid.max
            self.ind   = nameOrGrid.ind
            self.oname = nameOrGrid.oname
        Object.__init__(self, name, 'Grid')
        if SvF.printL : print ('Grid init by', self.name, self.min, self.max, self.step, self.ind)

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

        self.dat = None             #  use in functions    !!!!!!!!   -self.min     !!!!!!!!!!
        if SvF.Compile : return

#        if isfloat(self.min) and isfloat(self.max) and isfloat(self.step) :  #self.GridInit ()  # 20.12.19   30
 #               self.GridInit ()  # 20.12.19
#        elif not SvF.Preproc :  self.GridInit ()  30
        self.GridInit()
        return

    def Oprint(self) :
        print(self.Otype, self.name, "mm", self.min, self.max, "st", self.step, 'Up', self.Ub)

    def GridInit(self):

            if self.step < 0: self.step = - (self.max - self.min) / self.step;
            self.ma_mi = self.max - self.min
            self.Normalization_UbSets()
            self.makeVal()


    def indNormVal ( self, norm_val ):
#        ret = int ( floor ( norm_val/self.step + 0.499999999 ) )
        ret = int ( round ( norm_val/self.step ) )
        ##  check ?????
        return ret

    def indByVal ( self, val ):
        if isnan( val ) :       # 29
            return val
        else :
            return int ( round( (val-self.min)/self.step ) )
#            return int(floor((val - self.min) / self.step + 0.499999999))
##  check ?????

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
        if self.step == 0 : self.step = 1
        floatUb = (self.max - self.min) / self.step
#        self.Oprint()
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
    

    def Normalization_UbSets  (self) :

        if not self.dat is None :  self.dat -= self.min     # не приводим к штукам шагов
        self.setUb()
        self.makeSets()


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

        self.isDat = None       # 30
        if SvF.Compile : return
        self.Make_isDat()

# 30       if SvF.Preproc : self.isDat = None
 #       else           : self.Make_isDat()

    def Make_isDat(self):
        if self.visX==0 and self.visY==0 : return
        if self.dim == 0:  return

#        print ('Make_neNDT',self.visX, self.visY);  1/0
        A0 = self.A[0]
        mmm=A0.min
        A0_dat = SvF.curentTabl.getField_tb(A0.oname)
        if self.visX < 0: self.visX = - self.visX * A0.step;

        if self.dim == 1:
#            self.gap = ones(A0.Ub + 1, int8)                   # 27
                isDat = zeros(A0.Ub + 1, int8)
#                if not self.V.dat is None:    #  for what ?    27
 #                   for m in range(self.NoR):
  #                      if self.V.dat[m] != self.NDT:
   #                         isDat[int(floor(0.499999999 + A0.dat[m] / A0.step))] = 1
             ###   for m in range(self.NoR):
                for m,A0dat in enumerate(A0_dat) :
#                    for x in range(max(0, int(ceil((A0_dat[m] - self.visX) / A0.step))),
#                                   min(A0.Ub, int(floor((A0_dat[m] + self.visX) / A0.step))) + 1):
                    for x in range(max(0, A0.indByVal(A0dat - self.visX)),
                                    min(A0.Ub, A0.indByVal(A0dat + self.visX)) + 1):
                            isDat[x] = 1
        else:
                A1 = self.A[1]
                A1_dat = SvF.curentTabl.getField_tb(A1.oname)
                if self.visY < 0: self.visY = - self.visY * A1.step;

                #           self.gap = ones((A0.Ub + 1, A1.Ub + 1), int8)
                isDat = zeros((A0.Ub + 1, A1.Ub + 1), int8)

                for m,A0dat in enumerate(A0_dat):
                    for x in range(max(0, A0.indByVal(A0dat - self.visX)),
                                   min(A0.Ub, A0.indByVal(A0dat + self.visX)) + 1):
                        for y in range(max(0, A1.indByVal(A1_dat[m] - self.visY)),
                                       min(A1.Ub, A1.indByVal(A1_dat[m] + self.visY)) + 1):
                            isDat[x, y] = 1
#                            if not isnan(self.V.dat): isDat[x, y] = 1  # 29



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

