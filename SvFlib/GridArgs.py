#from  numpy import *
import numpy as np
#from  GaKru import *
import sys
from copy   import *
from Object import *
#from Table  import *
#import COMMON as com
from Tools import *
import openpyxl
#from Table  import *
#from Table import getCurrentFieldData


def  getName ( obj ) :
        if type (obj) == type ('abc') : return obj
        return obj.name

                               #  Для интегрирования
def myrange(mi_, ma_, st):  # mi <= ret  <= ma   ret[0] = mi  ret[-1] = ma  возможно округление 1е-10. Последний шаг - остаток.
        if mi_ > ma_:  return []    # 08/07/2021
        mi = float(mi_)        #    conflict    float <-> np.float64   ???????????????????  #########################
        ma = float(ma_)
        ret = []
        num = 0
        elem = mi
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
        return ret

class Set (Object):
    def __init__ (self, nameOrGrid, gmin=np.nan, gmax=np.nan, step=-50, ind = '', Data = '') :
        if type(nameOrGrid) is str:  # == type('abc'):
            self.name = nameOrGrid
            self.step = step
            self.min = gmin
            self.max = gmax
            self.ind = ind
            self.fld_name = Data  # None
        else:
            # name = nameOrGrid.name
            self.name = nameOrGrid.name
            self.step = nameOrGrid.step
            self.min = nameOrGrid.min
            self.max = nameOrGrid.max
            self.ind = nameOrGrid.ind
            self.fld_name = nameOrGrid.fld_name
        self.oname = self.name
        self.axe_name = ''

        print(self.name, gmin, gmax, step, ind, self.fld_name, type(self.fld_name) )

        self.dat = None
        if type(self.fld_name) is str:
            if self.fld_name == '': self.fld_name = self.name
        else:
            self.dat = deepcopy (Data)
            self.fld_name = self.name

        if self.ind == '': self.ind = '_i' + self.name

        print('SET init by', self.name, self.min, self.max, self.step, self.ind, self.fld_name, self.dat)

        if isfloat(self.ind): print(self.name, '****index must be a name:', self.ind);  exit(-1)  #  ???

        self.className = 'Set'
        Object.__init__(self, self.name, self.className)
        if SvF.Compile : return      ##############################################################


        self.Ub     =-1         # сетка от [0 до Ub]
        self.NodS   = [] #0
        self.mNodSm = 0
        self.mNodS  = 0
        self.NodSm  = 0
        self.mmNodS  = 0
        self.Val    = []
        self.FlNodS   = 0
        self.mFlNodSm = 0
        self.mFlNodS  = 0
        self.FlNodSm  = 0
        self.ma_mi    = 0

        self.Init()

    def Init(self):
        from Table import getCurrentFieldData
        if self.ind is None: self.ind = '_i' + self.name
        if self.step < 0: self.step = (self.max - self.min) / float(-self.step);
        self.ma_mi = self.max - self.min
        self.set_Ub_max()
        self.makeSets()
        if self.dat is None:
            self.dat = getCurrentFieldData(self.fld_name)

    def set_Ub_max(self):       #  вычисляем Ub и возможно увеличиваем max
        #           if self.step == 0: self.step = 1
        floatUb = (self.max - self.min) / float(self.step)
        self.Ub = int(np.ceil(floatUb))
        if self.Ub > 0:
            if abs(floatUb - (self.Ub - 1)) / self.Ub < 1e-10:  self.Ub -= 1  ###################  Округление Уточнить -13 #######
        old_max = self.max
        self.max = self.min + self.Ub * self.step
        if self.max > old_max :  print (self.name+'.max был увеличен c', old_max, ' до ', self.max)

    def makeSets  (self) :
 #       if self.Ub == -1 : return
        self.NodS   = range(0, self.Ub + 1)
        self.mNodSm = range(1, self.Ub)
        self.mNodS  = range(1, self.Ub + 1)
        self.NodSm  = range(0, self.Ub)
        self.mmNodS  = range(2, self.Ub + 1)
        self.Val = []
        for i in self.NodS : self.Val.append ( self.min*((float(self.Ub)-i)/float(self.Ub)) +self.max*(i/float(self.Ub)) )
        self.FlNodS   = self.Val                 # myrange(self.min,   self.max,    self.step)
        self.mFlNodSm = self.FlNodS[1:-1]         # myrange(self.min+self.step, self.max-self.step, self.step)
        self.FlNodSm  = self.FlNodS[0:-1]        #myrange(self.min,           self.max-self.step, self.step)
        self.mFlNodS  = self.FlNodS[1:]         #myrange(self.min+self.step, self.max,           self.step)
     #   print (self.NodS)
 #       print('_____________________________________________', self.FlNodS)


    def ValToInd(self, val):         # узел снизу
        ret = int ( (val-self.min ) / self.step + 0.5 )
        if ret < 0 :
            print ("\n\n\n\n Out of range", ret)
            return 0
        if ret > self.Ub :
            print ("\n\n\n\n Out of range", ret)
            return self.Ub
        return ret

    def IndToVal(self, ind):
        return self.min + ind * self.step

    def IndByVal ( self, val ):  # ближайший
        if np.isnan( val ) :       # 29
            return val
        else :
            return iround( (val-self.min)/self.step )

    def FlIndByVal ( self, val ):  # ближайший
        if np.isnan( val ) :       # 29
            return val
        else :
            return ifloor( (val-self.min)/self.step )

    def CeIndByVal ( self, val ):  # ближайший
        if np.isnan( val ) :       # 29
            return val
        else :
            return iceil( (val-self.min)/self.step )


    def NormValToInd(self, norm_val):
            #        ret = int ( floor ( norm_val/self.step + 0.499999999 ) )
            ret = int(round(norm_val / self.step))
            ##  check ?????
            return ret

    def CutOutMinMax ( self, val ) :
        if val < self.min :
            print ('Cut min', self.name, val, self.min)
            val = self.min
        if val > self.max :
            print ('Cut max', self.name, val, self.max)
            val = self.max
        return val

    def Oprint(self) :
    #    print(self.Otype, self.name, "mm", self.min, self.max, "st", self.step, 'Up', self.Ub)
        print( self.name, "mm", self.min, self.max, "st", self.step, 'Up', self.Ub)


class Domain (Object):
    def __init__( self, name, gridX, gridY=None, visX=0, visY=0 ):
        self.name  = name
        self.A     = [gridX]
#        print (name, gridX.name,gridX.dat, visX, gridY, visY)
        self.className = 'Domain'
        Object.__init__(self, self.name, self.className)

        #1/0
        if SvF.Compile : return

        print ('DOM', name, gridX.name, gridX.dat, visX, gridY, visY)

        if type ( gridY ) is float :
            self.visX = float (gridY)
        else :
            self.A.append(gridY)
            self.visX = float (visX)
            self.visY = float (visY)
            if self.visY < 0: self.visY = - self.visY * self.A[1].step
        if self.visX < 0: self.visX = - self.visX * self.A[0].step;
        self.dim = len (self.A)
        self.domain = None       # 30
        self.Make_domain()
        print ('Domain OK')
        return


    def Make_domain(self):
        if self.visX==0 and self.visY==0 : return
        if self.dim == 0:  return

        A0 = self.A[0]
        print ('Make_neNDT', A0.fld_name,self.visX, A0.dat)

        if self.dim == 1:
            print ('Not ready'); exit(-33)
#            self.gap = ones(A0.Ub + 1, int8)                   # 27
     #           domain = np.zeros(A0.Ub + 1, int8)
      #          for m,A0dat in enumerate(A0.dat) :
       #             for x in range(max(0, A0.IndByVal(A0dat - self.visX)),
        #                            min(A0.Ub, A0.IndByVal(A0dat + self.visX)) + 1):
         #                   domain[x] = 1
        else:
                A1 = self.A[1]
                print('Make_neNDT', A1.fld_name, self.visY, A1.dat)
                domain = np.zeros((A0.Ub + 1, A1.Ub + 1), np.int8)

                for m,A0dat in enumerate(A0.dat):
      #              if m > 5: break
        #            print (A0dat, A1.dat[m])
                    for x in range ( A0.FlIndByVal (A0dat-self.visX), A0.CeIndByVal (A0dat+self.visX)+1 ):
                        for y in range( A1.FlIndByVal (A1.dat[m]-self.visY), A1.CeIndByVal (A1.dat[m]+self.visY)+1 ):
                            if x < 0 or x>A0.Ub or y < 0 or y > A1.Ub :  continue
                            if np.abs (    A0dat - A0.IndToVal(x)  ) > self.visX: continue
                            if np.abs (A1.dat[m] - A1.IndToVal(y)  ) > self.visY: continue
                            domain[x, y] = 1
       #                     print ('OK', x, y)
        self.domain = domain
        print (domain)
      #  1/0


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

