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
#from ModelFiles import *  #to_logOut
#import MakeModel as MM
#from MakeModel import ParseSelect30

# import COMMON as co


from Lego_Tools  import *

from Lego_Tensor import *


class BaseFun (Tensor) :
    def __init__ (self, Vname='',  As=[], param=False, Degree=-1,  Finitialize = 1, DataReadFrom = '',Data=[],
                  Type='g', Domain = None, ReadFrom = '' ) :
        Tensor.__init__ (self, Vname )
        from Table import getCurrentFieldData
#        Object.__init__(self, Vname, 'Fun')
        self.V = Vari(Vname)  #V #0 #[ ]             #  var
 #       self.A = copy(As) #[ ]             #  Arg
        self.A = deepcopy(As) #[ ]             #  Arg     КОПИРУЕМ АРГУМЕНТЫ

        #    self.smbF = ''
        self.dim = len (self.A)  #-1
        self.param    = param #False
        self.DataReadFrom = DataReadFrom
        self.NoR   = 0
        self.domain = None
        self.domain_SPWL = None
        self.type  = Type
        self.PolyPow  = Degree # -1            # степень полинома
        if self.PolyPow != -1:  self.type  = 'p'

        self.Int_smbFxx_2 = None

 #       self.domain_ = py.Reals
        if SvF.Compile :  return

        if isnotNone ( Domain ) : self.domain = Domain.domain

        if   self.type == 'g':             pass
        elif   self.type == 'p':           pass
        elif   self.type == 'smbFun':      pass
        elif self.type == 'SPWL':          self.type = 'gSPWL'
#        elif self.type == 'G7':            self.type = 'gSPWL'
#        elif self.type == 'G_ind':         self.type = 'gSPWLi'
        elif self.type == 'SPWLi':         self.type = 'gSPWLi'
        elif self.type == 'G':             self.type = 'gG'  # Там что-то не так
#        elif self.type == 'Cycle':         self.type = 'gCycle'
        elif self.type == 'gCycle':        pass
        else :
            print ('Неизвестный тип функции   ', self.type)
            exit (-1)
#        print ( "Fun:"+self.V.name, "Type:"+self.type)
        self.Oprint()


        self.sR    = []           # множ записей табл
        self.NDT   = -99999
        self.sizeP = 0
        if self.PolyPow > 0 :
            self.type = "p"
            self.sizeP = PolySize ( self.dim, self.PolyPow )

        #self.grd   = None
#        self.var   = None           # 29
        self.mu    = None
        self.CVerr = None           # 04.23
#        self.tesValidationSets  = []
#        self.notTrainingSets = []
        self.ValidationSets  = SvF.ValidationSets
        self.notTrainingSets = SvF.notTrainingSets
        self.TrainingSets = SvF.TrainingSets

        self.Nxx   = 0
        self.Nyy   = 0
        self.Nxy   = 0
        self.gap   = None
## 27        self.G     = 0
        self.MSDv  = None
  #      self.nCrVa = None
        self.MSDmode = ''
        self.measurement_accur = 0
        self.CVresult = []    #  [[spart, npart],[spart, npart],.. ]    27
        self.sCrVa = 0        #  np.sqrt (..)                              27
 #       self.DataReadFrom = DataReadFrom
#        self.param    = param #False
        self.Finitialize = Finitialize
        self.ArgNormalition = False

#        self.sizeP = PolySize ( self.dim, self.PolyPow )
        if SvF.Compile :  return    #####################################

        for a in self.A:
            d = getCurrentFieldData(a.name)     #      Если имя есть в таблице ...
            if not (d is None) : a.dat = d
        for id, d in enumerate(Data):           #      Если имя есть в Data=[]   ...
            if d == '':  continue
            if id==0:   self.V = Vari(Vname, d)
            else:
                self.A[id-1].fld_name = d
                from Table import getCurrentFieldData
                self.A[id-1].dat = getCurrentFieldData(d)

        self.CleanData()   #  dat
        self.Allocate_grd()
#        self.CleanData()   #  dat
        self.Normalization(SvF.VarNormalization)
        self.calcNDTparam()
        if ReadFrom != '':  self.ReadSol(ReadFrom)

    def Allocate_grd(self) :
        if self.type != 'p':  # не полином
            Sizes = [a.Ub + 1 for a in self.A]
            self.Allocate_tensor(Sizes)
        else:
            self.Allocate_tensor([self.sizeP])

    """
    def Initialize ( self, InitFloat = None ) :
        if SvF.printL > 0: printS('Initialize: |'); self.Oprint()
        if InitFloat is None : InitFloat = '0'
       
        tmpcurentTabl = SvF.curentTabl
        if self.DataReadFrom != '':
     #       Tab.Select ( self.DataReadFrom )
            leftName, Fields, FileName, AsName, where = Tab.ParseSelect30(self.DataReadFrom)
            Tab.Table( FileName, AsName, Fields )
        
        for ia, a in enumerate(self.A):  # дописываем гриды
            if SvF.printL:  print ('A:', a)
            if type(a) != type('abc'):
                self.A[ia] = deepcopy(a)   #   !!!!!!!!!!!! #
                continue
            g = findSetByName(SvF.Task.Sets, a)
            if g == None:
                print ('\n***********************  NO Set FOR ARG NAME ', a, '*********************')
                g = Set (a)
                print ("***********************Set:",)
                g.myprint()
                print ('    HAS BEEN ADDED *****************************')
            # exit (-1)
            self.A[ia] = Set (g) #Arg (g)
        
        
        if self.dim > 0 :
            self.CleanData()
#            SvF.curentTabl = tmpcurentTabl
            self.Normalization(SvF.VarNormalization)
            self.calcNDTparam()
        
        #        if self.param:                     # function-Param
        if self.type != 'p':          #  не полином           # function-Param              # 29
#                print('RRRRRRRRRRRRRRRRRR  SSS', self.sizeP, self.type)
                if self.dim == 0:
                    self.grd = 0
                elif self.dim == 1:
#                    print('UUUUUUUUUUUUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS', self.A[0].Ub, self.type)
                    self.grd = np.zeros((self.A[0].Ub + 1), np.float64)
                    if not np.isnan (InitFloat) :  self.grd[:] = InitFloat
                elif self.dim == 2:
#                    print('DDDDDDDUUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS', self.A[0].Ub + 1, self.A[1].Ub + 1, self.type)
                    self.grd = np.zeros((self.A[0].Ub + 1, self.A[1].Ub + 1), np.float64)
                    if not np.isnan (InitFloat) :  self.grd[:][:] = InitFloat
#                    print('G',self.grd)

                elif self.dim == 3:
#                    print('DDDDDDDUUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS', self.A[0].Ub + 1, self.A[1].Ub + 1, self.type)
                    self.grd = np.zeros((self.A[0].Ub + 1, self.A[1].Ub + 1, self.A[2].Ub + 1), np.float64)
                    if not np.isnan (InitFloat) :  self.grd[:][:][:] = InitFloat
                if self.param: self.InitByData()                #29
        else :
#            print('PPPPPPPPPPPPPPPPPPPSSS', self.sizeP, self.type)
            self.grd = np.zeros(self.sizeP, np.float64)
       
        return self
    """

    def CleanData(self):
        from ModelFiles import to_logOut
        if self.dim == 0: return

        dSize = 0
        if isnotNone(self.V.dat): dSize = len(self.V.dat)
        for a in self.A :
            if isnotNone(a.dat): dSize = len(a.dat)
        print (dSize)
        if dSize == 0:
#            print ('Nothing to Clean')
            return

        self.NoR = 0
        for i in range (dSize):
            if isnotNone(self.V.dat):
                if np.isnan(self.V.dat[i]) or self.V.dat[i] == self.NDT:
                    if SvF.useNaN == False:
                        print('Rec', i, 'deleted')
                        to_logOut('W:   Record  ' + str(i) + '  was deleted from data set of function   ' + self.V.name)
                        continue
                self.V.dat[self.NoR] = self.V.dat[i]
            OK = 1
            for a in self.A:
                if a.dat is None: continue
                if np.isnan(a.dat[i]): OK = 0; break
                if a.dat[i] == self.NDT: OK = 0; break
                if a.dat[i] < a.min   or   a.dat[i] > a.max:   OK = 0; break
#                if a.dat[i] < 0   or   a.dat[i] > a.ma_mi :   OK = 0; break
                a.dat[self.NoR] = a.dat[i]
            if  OK:  self.NoR += 1
            else :
                to_logOut('W:   Record  ' + str(i) + '  was deleted from data set of function   ' + self.V.name)
                print('Rec', i, 'deleted')

        if isnotNone(self.V.dat):  # resize
                self.V.dat = np.delete(self.V.dat, range(self.NoR, self.V.dat.shape[0]))
        for a in self.A:
            if isnotNone( a.dat ):
                a.dat = np.delete(a.dat, range(self.NoR, a.dat.shape[0]))

        self.sR = range(self.NoR)
        print('After Cleaning' ,self.name, '->self.NoR =', self.NoR)


    """""
            if tabl is None:  return False
            haveAll = True
            haveAny = False

            V_tb = tabl.getFieldData(self.V.name)
            #        if print ('V', V_tb[:])
            if V_tb is None:
                #            print ("GetData ****************************** No Field in ", tabl.name,  "For Var", self.V.name, "****")
                haveAll = False
            else:
                self.V.dat = np.zeros(tabl.NoR, np.float64)
                haveAny = True

            A_tb = []
            for a in self.A:
                A_tb.append(tabl.getFieldData(a.oname))
                if A_tb[-1] is None:
                    #               print ("GetData ****************************** No Field in ", tabl.name,  "For Arg", a.name, "*****")
                    haveAll = False
                else:
                    a.dat = np.zeros(tabl.NoR, np.float64)
                    haveAny = True
            if haveAny == False: return False

            self.NoR = 0
            numNaN = 0
            for i in tabl.sR:
                if not V_tb is None:
                    if np.isnan(V_tb[i]) or V_tb[i] == self.NDT:
                        if SvF.useNaN == False: continue
                        numNaN += 1
                    self.V.dat[self.NoR] = V_tb[i]  # 0
                OK = 1
                for narg, a_tb in enumerate(A_tb):
                    if A_tb[narg] is None: continue
                    if np.isnan(a_tb[i]): OK = 0; break
                    if a_tb[i] == self.NDT: OK = 0; break
                    if a_tb[i] < self.A[narg].min or a_tb[i] > self.A[narg].max: OK = 0; break
                    self.A[narg].dat[self.NoR] = a_tb[i]  # 1 ...
                if not OK: continue
                self.NoR += 1
            #            print self.NoR,

            if not V_tb is None:  # resize
                self.V.dat = np.delete(self.V.dat, range(self.NoR, self.V.dat.shape[0]))
            for narg, arg in enumerate(self.A):
                if not A_tb[narg] is None:
                    arg.dat = np.delete(arg.dat, range(self.NoR, arg.dat.shape[0]))

            self.sR = range(self.NoR)
            #        if not self.V.dat is None :
            #           for i in range (len(self.V.dat) ) : print (i, self.V.dat[i])
            print(self.name, '->self.NoR =', self.NoR)
            if SvF.printL: print("GetData numNaN", numNaN, "NoR", self.NoR)  # , "mins", tbl.min(0), "maxs", tbl.max(0)
            return haveAll
    """

    def StrArds (self) :
            ret = ''
            for d, a in enumerate (self.A):
                ret += a.name + ','
#                print (ret)
            if len(self.A)>0: ret = ret[0:-1]
            return ret

    def ArgNamesList (self) :
            ret = []
            for a in self.A:  ret.append(a.name)
            return ret


    def NameArds (self) :
            ret = self.V.name
            for d, a in enumerate (self.A):
                if d == 0:  ret += '('
                ret += a
                if d == self.dim-1 :
                    ret += ')'
                    break
                ret += ','
            return ret


    def Oprint (self) :
            if self.param :  param = 'p'
            else          :  param = 'v'
            st = param + self.Otype + ' ' +  self.V.name + '('
   #         printS (self.Otype + ' '+ self.V.name + '(' ,'|')
            for d, a in enumerate (self.A): #range(self.dim) :
                if type (a) == type ('abc') : st += ' ' + a  #print (a)
                else                        :
                    st +=  a.name +': ' + str(a.min) + '-' + str(a.max) + " st:" +str(a.step) + ' Up:' +str(a.Ub) # a.Oprint()
                if d < self.dim-1          : st += ','
                else                        : st += ' ) '
            st += self.type
            if self.type == 'p': st += str(self.PolyPow)
            st += " sig:" + str(self.V.sigma) + ' avr:' + str(self.V.average) + ' NoR:' + str (self.NoR)
            print (st)
            return

    def Rename (self, Vname, *A) :
            self.name = Vname
            self.V.name = Vname
            for ia,a in enumerate ( A ) : self.A[ia].name = a
            return self

    def Clear_dat ( self, Val) :      #  Убирает строки  dat[] = Val
        NoR = 0
        print ('self.NoR', self.NoR)
        for i in self.sR :
            if self.V.dat[i] == Val : continue
            self.V.dat[NoR]    = self.V.dat[i]
            self.A[0].dat[NoR] = self.A[0].dat[i]
            self.A[1].dat[NoR] = self.A[1].dat[i]
            NoR += 1
        self.NoR = NoR
        print(self.NoR)
        self.V.dat    = np.resize(self.V.dat, NoR)
        self.A[0].dat = np.resize(self.A[0].dat, NoR)
        self.A[1].dat = np.resize(self.A[1].dat, NoR)
        self.sR = range(self.NoR)


    def Uppend_dat ( self, V, A0, A1=None) :      #
        self.NoR += 1
        self.V.dat    = np.resize(self.V.dat, self.NoR)
        self.V.dat[self.NoR-1] = V
        self.A[0].dat    = np.resize(self.A[0].dat, self.NoR)
        self.A[0].dat[self.NoR-1] = A0 - self.A[0].min
        if not A1 is None :
            self.A[1].dat    = np.resize(self.A[1].dat, self.NoR)
            self.A[1].dat[self.NoR-1] = A1 - self.A[1].min
        self.sR = range(self.NoR)

    """""
    def grd_to_var (self) :
        if self.var is None:  return
        if self.param : return
        if self.type == 'p' :
            for i in range ( self.sizeP ) :  self.var[i].value = self.grd[i]
        elif self.type == 'smbFun' :
            pass
  #          for i in range ( self.NoCoeff ) :  self.var[i].value = self.grd[i]
        else :
            if   self.dim == 0:
                self.var.value = self.grd
#                print('*************************************var', self.var.value, self.grd)
            elif self.dim == 1:
                for i in self.A[0].NodS:
#                    self.var[i].value = self.grd[i]
                    self.var[i].set_value(self.grd[i], skip_validation=True)
            elif self.dim == 2:
                for i in self.A[0].NodS:
#                    for j in self.A[1].NodS:  self.var[i,j].value = self.grd[i,j]
                    for j in self.A[1].NodS:  self.var[i,j].set_value(self.grd[i,j], skip_validation=True)

            elif self.dim == 3:
                for i in self.A[0].NodS:
                    for j in self.A[1].NodS:
                        for k in self.A[2].NodS:
#                            self.var[i,j,k].value = self.grd[i,j,k]
                            self.var[i,j,k].set_value(self.grd[i,j,k], skip_validation=True)

    
    def var_to_grd (self) :
        if self.var is None:  return
        if self.param : return
#        print ('var_to_grd',self.type,self.dim)
        if self.type == 'p' :
            for i in range ( self.sizeP ) :  self.grd[i] = self.var[i].value
        elif self.type == 'smbFun' :
            pass
    #         for i in range ( self.NoCoeff ) :  self.grd[i] = self.var[i].value
        else :
            if   self.dim == 0:   self.grd = self.var.value
            elif self.dim == 1:
                for i in self.A[0].NodS:  self.grd[i] = self.var[i].value
            elif self.dim == 2:
                for i in self.A[0].NodS:
                    for j in self.A[1].NodS:  self.grd[i,j] = self.var[i,j].value
            elif self.dim == 3:
                for i in self.A[0].NodS:
                    for j in self.A[1].NodS:
                        for k in self.A[2].NodS:
                            self.grd[i,j,k] = self.var[i,j,k].value
    """""
                                                                         # возможно меняет  param и type.
    def CopyFromFun ( self, DataFrom, new_param=None, new_type=None, copy_dat = True ):
        if new_type is None : self.type  = DataFrom.type                # для полином -> грид : вычисляет значения
        else                : self.type  = new_type
        if new_param is None : self.param  = DataFrom.type
        else                 : self.param  = new_param

        if DataFrom.V.name == '' :
            self.V.name  = DataFrom.V.name
        self.Otype = DataFrom.Otype
        self.V     = deepcopy(DataFrom.V)         # InDada
        if not copy_dat : self.V.dat = None
        self.mu       = DataFrom.mu     ######## 2020 09 06
        self.A     = deepcopy(DataFrom.A)
        self.dim   = DataFrom.dim
        self.NDT   = DataFrom.NDT
 #27       self.Task  = DataFrom.Task
        self.NoR   = DataFrom.NoR
        self.sR    = DataFrom.sR
        self.PolyPow  = DataFrom.PolyPow
   #     self.domain = DataFrom.domain
        self.domain = deepcopy(DataFrom.domain)      #    deepcopy ?????
        self.Nxx   = DataFrom.Nxx
        self.Nyy   = DataFrom.Nyy
        self.Nxy   = DataFrom.Nxy
        self.gap   = deepcopy(DataFrom.gap)
        self.DataReadFrom = DataFrom.DataReadFrom
 #       self.domain_  = DataFrom.domain_
        self.ValidationSets  = DataFrom.ValidationSets
        self.notTrainingSets = DataFrom.notTrainingSets
        self.TrainingSets = DataFrom.TrainingSets
#        self.G     = DataFrom.G
        self.grd = None
        self.var = None                 # 29
        if self.type == DataFrom.type :
            self.grd = deepcopy(DataFrom.grd)       # 29
            return self                                   # 29
        if self.type == 'p' :      return self     # grd  handling
#       'p' -> 'g'
        if self.dim   == 1:  self.grd = np.zeros(self.A[0].Ub + 1, np.float64)
        elif self.dim == 2:  self.grd = np.zeros((self.A[0].Ub + 1, self.A[1].Ub + 1), np.float64)
        elif self.dim == 3:  self.grd = np.zeros((self.A[0].Ub + 1, self.A[1].Ub + 1, self.A[2].Ub + 1), np.float64)

        if 1 :           
                Ax = self.A[0]
                if self.dim == 1:
                    for x in Ax.NodS:
                        if self.fneNDT(x) == 1:     self.grd[x] = DataFrom.F([Ax.Val[x]])  # ()
                        else                 :      self.grd[x] = DataFrom.NDT
                else:  # dim 2
                    Ay = self.A[1]
                    for x in Ax.NodS:
                        for y in Ay.NodS:
                            if self.fneNDT(x,y) == 1:  self.grd[x, y] = DataFrom.F([ Ax.Val[x], Ay.Val[y] ]) # ()
                            else                    :  self.grd[x, y] = DataFrom.NDT
        return self


    def Clone ( self, name='' ):
                return Fun(name).CopyFromFun(self)

    def gClone (self, copy_dat = False ):
        if  self.type[0] == 'g' :   # 2407
            ret = deepcopy (self)
            ret.type = 'g'
            if not copy_dat: self.V.dat = None
            return ret
        else :
            return Fun().CopyFromFun(self, True, 'g', copy_dat)     # <= 28

    def Cut (self, slice, name=None, draw_name=None):
        if slice[0]==':' : axenum = 0
        else :             axenum = 1
        val = float (slice[1-axenum])
        if name is None: name = self.V.name + self.A[axenum].name + str(val)
        ret = Fun ( name )
        ret.dim = 1
        if not draw_name is None : ret.V.draw_name = draw_name
        ret.A.append (deepcopy(self.A[axenum]))
        ret.grd = np.zeros((ret.A[0].Ub + 1), np.float64)
        for i,x in enumerate (ret.A[0].Val):
            if axenum == 0:  ret.grd[i] = self.F([x,val])
            else:            ret.grd[i] = self.F([val,x])
        if not (self.V.dat is None or self.A[0].dat is None or self.A[1].dat is None):
            ret.V.dat = []; ret.A[0].dat = []
            for i in self.sR :   #enumerate (self.A[a[1-axenum]].dat):
                if abs(val - self.A[1-axenum].dat[i]) < 1e-7:
                    ret.V.dat.append (self.V.dat[i])
                    ret.A[0].dat.append(self.A[axenum].dat[i])
        return ret


    def Resize (self, As=[]) :    # new sizes
        if self.type != 'p':  # не полином           # function-Param              # 29
            if self.dim == 0:
                pass
            elif self.dim == 1:
                self.grd.resize( As[0].Ub+1)
            elif self.dim == 2:
                new_grd = np.zeros((As[0].Ub + 1, As[1].Ub + 1), np.float64)
                A0 = min (self.A[0].Ub + 1, As[0].Ub + 1)
                A1 = min (self.A[1].Ub + 1, As[1].Ub + 1)
                new_grd[:A0,:A1] = self.grd[:A0,:A1]
                self.grd = new_grd
#            elif self.dim == 3:
 #               self.grd = np.zeros((self.A[0].Ub + 1, self.A[1].Ub + 1, self.A[2].Ub + 1), np.float64)
        self.A = copy(As)

    def Normalization ( self, VarNormalization ) :
#        for arg in self.A :
 #           print('Fun NOR Nor', arg.name, arg.dat)
  #          arg.Normalization ( )
        self.V.Normalization (VarNormalization)




    def InitBy ( self, val, vis0, vis1) :
              A0 = self.A[0]
              A1 = self.A[1]
              if vis0  < 0 : vis0  = - vis0 * A0.step
              if vis1  < 0 : vis1  = - vis1 * A1.step

              for m in self.sR :
                for x   in range( max(0, A0.NormValToInd(A0.dat[m]-vis0)), min(A0.Ub, A0.NormValToInd(A0.dat[m]+vis0))+1 ) :
                  for y in range( max(0, A1.NormValToInd(A1.dat[m]-vis1)), min(A1.Ub, A1.NormValToInd(A1.dat[m]+vis1))+1 ) :
                     self.grd[x,y] = val  #1              29
          
            
    def calcNDTparam(self) :
        if self.dim == 0: return
        A0 = self.A[0]
        domain = self.domain
        if self.dim == 1:
          if domain is None :
            self.Nxx = A0.Ub-1
          else :
            self.Nxx = sum ( domain[x-1]*domain[x]*domain[x+1] for x in range( 1,A0.Ub ) )
        elif self.dim == 2:
          A1 = self.A[1]
          if domain is None :
              self.Nxx = (A0.Ub-1)*(A1.Ub+1)
              self.Nyy = (A0.Ub+1)*(A1.Ub-1)
              self.Nxy = (A0.Ub-1)*(A1.Ub-1)
          else :
            self.Nxx = sum ( domain[x-1,y] * domain[x,y] * domain[x+1,y]
                    for y in A1.NodS    for x in A0.mNodSm )
            self.Nyy = sum ( domain[x,y-1] * domain[x,y] * domain[x,y+1]
                    for y in A1.mNodSm  for x in A0.NodS )
            self.Nxy = sum ( domain[x+1,y+1] * domain[x+1,y-1] * domain[x-1,y+1] * domain[x-1,y-1]
                    for y in A1.mNodSm  for x in A0.mNodSm )


    def fneNDT (self, x, y=0) :
        if self.domain is None : return 1
#        print ('@@@@@@@@@@@@@@@@@@@self.neNDT[x,y]', self.neNDT[x,y])
        if self.dim == 1      : return self.domain[x]
        if self.dim == 2      : return self.domain[x,y]

    def f_gap (self, x, y=0) :
        if self.gap is None : return 1
        if self.dim == 1      : return self.gap[x]
        if self.dim == 2      : return self.gap[x,y]

    def AddGap ( self ) :
        if self.dim == 1 :   self.gap = ones (  self.A[0].Ub+1,                 np.float64 )
        if self.dim == 2 :   self.gap = ones ( (self.A[0].Ub+1, self.A[1].Ub+1),np.float64 )


    def neNDTbyVal (self, xVal, yVal=None) :
        ix = self.A[0].ValToInd(xVal)
        if self.dim == 1:
            return self.domain[ix]
        else :
            iy = self.A[1].ValToInd(yVal)
            return self.domain[ix,iy]



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

    def Extrapolate (self, grd_start_from, incr = 0) :
        for i in range (iround(grd_start_from), self.A[0].Ub+1):
            self.grd[i] = self.grd[i-1] + incr

    def Mult(self, val):
        if self.type == 'p':
#            for p in self.PolyR:       self.grd[p].value *= val
            for p in self.PolyR:       self.grd[p] *= val
        else :
#        elif self.param :
            if self.dim == 1:
                for x in self.A[0].NodS:   self.grd[x] *= val
            else:
                for x in self.A[0].NodS:
                    for y in self.A[1].NodS: self.grd[x, y] *= val
#        else :
 #         if self.dim == 1:
  #          for x in self.A[0].NodS:   self.var[x].value *= val     # 29 ##########   grd
#          else:
 #           for x in self.A[0].NodS:
  #              for y in self.A[1].NodS: self.var[x, y].value *= val

    def Divide (self, by ):
 #           if self.type == 'p':
  #              for p in self.PolyR:       self.grd[p].value *= val
 ####           if by.param :
              if self.dim == 1:
                for x in self.A[0].NodS:   self.grd[x] /= by.grd[x]
              else:
                for x in self.A[0].NodS:
#                    for y in self.A[1].NodS: self.grd[x, y].value /= by.grd[x,y]  # value -ошибка ?
                    for y in self.A[1].NodS: self.grd[x, y] /= by.grd[x,y]
 #           else :
  #            if self.dim == 1:
   #             for x in self.A[0].NodS:   self.grd[x] /= by.grd[x]()              # value -ошибка ?
#              else:
 #               for x in self.A[0].NodS:
  #                  for y in self.A[1].NodS: self.grd[x, y].value /= by.grd[x,y]()

    def Minus(self, by):
            if self.dim == 1:
                for x in self.A[0].NodS:
                    self.grd[x] -= by.grd[x]
            else:
                for x in self.A[0].NodS:
                    for y in self.A[1].NodS: self.grd[x, y] -= by.grd[x, y]

    def Plus(self, by):
            if self.dim == 1:
                for x in self.A[0].NodS:
                    self.grd[x] += by.grd[x]
            else:
                for x in self.A[0].NodS:
                    for y in self.A[1].NodS: self.grd[x, y] += by.grd[x, y]

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
#            if self.param :
                self.grd = float ( val )
 #           else          : self.grd.value = float ( val )
        elif self.dim == 1 :
 #           if self.param :
                self.grd[farg[0]] = float ( val )
  #          else          : self.grd[farg[0]].value = float ( val )
        elif self.dim == 2 :
#            if self.param :
                self.grd[farg[0],farg[1]] = float ( val )
 #           else          : self.grd[farg[0],farg[1]].value = float ( val )
        elif self.dim == 3 :
 #           if self.param :
                self.grd[farg[0],farg[1],farg[2]] = float ( val )
  #          else          : self.grd[farg[0],farg[1],farg[2]].value = float ( val )


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
        if self.domain is None : return
        if self.dim == 0 : return

        if self.dim == 1 :
            for x in self.A[0].NodS :  
                if not self.domain[x] :
                  self.var[x].value = self.NDT
                  self.var[x].fixed = True
        else :      
            for x in self.A[0].NodS :  
              for y in self.A[1].NodS :
           #     if  np.isnan(self.var[x,y].value) or self.var[x,y].value== self.NDT:  ################
            #        self.var[x,y].value=0     ########################################
                if not self.domain[x,y] :
                  self.var[x,y].value = self.NDT
                  self.var[x,y].fixed = True

    def FillNaN (self) :
        if self.type == 'p' : return
        if self.type == 'smbFun' : return

#        if self.domain is None : return
        if self.dim == 0 : return

        if self.dim == 1 :
            for x in self.A[0].NodS :
                if  np.isnan(self.grd[x]) or self.grd[x]== self.NDT:  ################
                    self.grd[x].value=1     ########################################
        else :
            for x in self.A[0].NodS :
              for y in self.A[1].NodS :
                if  np.isnan(self.grd[x,y]) or self.grd[x,y]== self.NDT:  ################
                    self.grd[x,y]=1     ########################################

    """""
    def Feal(self):
        if self.type == 'p': return
        if self.domain is None: return
        if self.dim == 0: return

        if self.dim == 1:
            for x in self.A[0].NodS:
                if not self.domain[x]:
                    self.var[x].value = self.NDT
                    self.var[x].fixed = True
        else:
            for x in self.A[0].NodS:
                for y in self.A[1].NodS:
                    #     if  np.isnan(self.var[x,y].value) or self.var[x,y].value== self.NDT:  ################
                    #        self.var[x,y].value=0     ########################################
                    if not self.domain[x, y]:
                        self.var[x, y].value = self.NDT
                        self.var[x, y].fixed = True
    """
    def delta( self, n ) :
        return	 self.Ftbl ( n ) - self.V.dat[n]   #  13.03.2023
 #       return	 self.V.dat[n] - self.Ftbl ( n )

    def delta_rel ( self, n ) :
        return	 (self.delta(n)/ max(self.V.dat[n],self.measurement_accur))

    def MSD ( self ) :
        return self.MSDnan()
#        if not SvF.Hack_Stab :
 #           return self.MSDnan()
  #      else :
   #         return  1. /self.V.sigma2  /self.NoR * sum (  self.mu[n] * self.delta(n)**2  for n in self.sR )

    def MSDcheck(self) :
            self.MSDmode = 'MSD'
            return  1./self.V.sigma2 /self.V.NoR \
                    * sum ( (self.tbl[n,self.V.num]!=self.NDT) * self.mu[n] * self.delta(n)**2 for n in self.sR )

    def MSDrel (self, measurement_accur = 0) :        # valid_f  - for verification - validation
            if self.mu is None : return self.MSDrel_no_mu()     # 24.01
            self.MSDmode = 'MSDrel'
            self.measurement_accur = measurement_accur
            ret = 0
            num = 0
            if SvF.Use_var:                                      #  mu[n]  <->  mu[n]()
                for n in self.sR :
                    if not np.isnan(self.V.dat[n])  :
#                        ret += self.mu[n] * (self.delta(n)/ max(self.V.dat[n],measurement_accur))**2
                        ret += self.mu[n] * self.delta_rel(n)**2
                        num += self.mu[n]
            else :
                print (self.name)
                for n in self.sR:
                    if not np.isnan(self.V.dat[n]):
#                        ret += self.mu[n]() * (self.delta(n)/ max(self.V.dat[n],measurement_accur))**2
                        ret += self.mu[n]() * self.delta_rel(n)**2
                        num += self.mu[n]()
            ret = ret  / num
            return ret

    def MSDrel_no_mu (self, measurement_accur = 0) :
        self.MSDmode = 'MSDrel'
        self.measurement_accur = measurement_accur
        ret = 0
        num = 0
        for n in self.sR:
                if not np.isnan(self.V.dat[n]):
                    #                        ret += self.mu[n] * (self.delta(n)/ max(self.V.dat[n],measurement_accur))**2
                    ret += self.delta_rel(n) ** 2
                    num += 1
        ret = ret / num
        return ret

    def MSDnan (self, valid_f = None) :        # valid_f  - for verification - validation
            if self.mu is None : return self.MSDnan_no_mu()     # 24.01
            self.MSDmode = 'MSD'
            ret = 0
            num = 0
#            print ('SvF.Use_var', SvF.Use_var)
            if not SvF.Use_var:                                      #  mu[n]  <->  mu[n]()
                for n in self.sR:
                    if not np.isnan(self.V.dat[n]):
#                        print (self.name)
 #                       print( self.mu[n]())
                        ret += self.mu[n]() * self.delta(n) ** 2
                        num += self.mu[n]()
                return ret / self.V.sigma2 / num
            else:
                for n in self.sR:
                    if not np.isnan(self.V.dat[n]):
#                        print ('______________________________', self.delta(n))
 #                       print (self.name)
  #                      print( self.mu[n])
                        ret += self.mu[n] * self.delta(n)**2
                        num += self.mu[n]
                ret = ret / self.V.sigma2 / num
            if SvF.Hack_Stab:
                num = sum ( int(not np.isnan(self.V.dat[n])) for n in self.sR ) # подсчет num
                for n in self.sR:
                    if not np.isnan(self.V.dat[n]):
                        co.stab_val_sub.append( 1 /self.V.sigma2 /num)

                if len(co.stab_val_by_cv) == 0:  co.stab_val_by_cv = [ [] for _ in range(len(co.notTrainingSets))]
#                print ('len(co.stab_val_by_cv)',len(co.stab_val_by_cv))
                for cv_n, cv_set in enumerate (co.notTrainingSets) :
                    mu = [1] * len(self.sR)
                    for s in cv_set: mu[s] = 0
                    num = sum(int((not np.isnan(self.V.dat[nmu])) and emu==1) for nmu, emu in enumerate (mu))  # подсчет num

                    for nmu, emu in enumerate (mu):
                        if (not np.isnan(self.V.dat[nmu])):
                            if emu==1 : co.stab_val_by_cv[cv_n].append( 1 /self.V.sigma2 /num)
                            else:       co.stab_val_by_cv[cv_n].append( 0 )
#                for cv_n in range (len(co.notTrainingSets)): print('LLLLLLLLLLLLLLLLLLLLLLLLL', cv_n, len(co.stab_val_by_cv[cv_n]))

            return ret

#                ret = ret  / self.V.sigma2 / self.NoR #num
#                ret = ret  / self.V.sigma2 / num
 #           else :
#                print ('1/ self.V.sigma2 / num()', num)
 #               print ('1/ self.V.sigma2 / num()', 1/ self.V.sigma2 / num)

  #              pass
  #              ret = ret # / self.V.sigma2 / self.NoR
  #          print( '********************' ,0.0006114684100262* self.V.sigma2 * num   )
   #         return ret
#        if not SvF.Hack_Stab :
 #           return self.MSDnan()
  #      else :
   #         return  1. /self.V.sigma2  /self.NoR * sum (  self.mu[n] * self.delta(n)**2  for n in self.sR )


    def MSDverif(self, verif_f):  # verif_f  - for verification - validation
            self.MSDmode = 'MSD'
            ret = 0
            num = 0
     #       n=0
#            print verif_f.A[0].dat[n],verif_f.A[0].min,verif_f.V.dat[n]
 #           print self.grd[0]()
            for n in verif_f.sR :
                if not np.isnan(verif_f.V.dat[n])  :
                      ret += (self.F([verif_f.A[0].dat[n]+verif_f.A[0].min])-verif_f.V.dat[n])**2
                      num += 1
            ret /= num
            return ret

    def MSD_no_mu ( self ) :            #   MSDno_mu -> MSD_no_mu    24/03/31
        return self.MSDnan_no_mu()
 #       return  1./self.V.sigma2 /self.NoR * sum ( self.delta(n)**2  for n in self.sR )

    def MSDnan_no_mu (self, valid_f = None) :
            self.MSDmode = 'MSD'
            ret = 0
            num = 0
            if self.V.dat is None :  return 0
            for n in self.sR :
                if not np.isnan(self.V.dat[n])  :
                    ret += self.delta(n)**2
                    num += 1
            return ret  / self.V.sigma2 / num


    def Compl ( self, bets ) :
            return self.ComplDer2 ( bets )

    def ComplMean2 ( self, bets ) :
            return self.ComplDer2 ( bets ) / self.Mean()**2

    def ComplSig2 ( self, bets ) :
            return self.ComplDer2 ( bets ) / self.V.sigma2

    def Complexity ( self, bets ) :
            return self.ComplDer2 ( bets )


    def ComplDer2 ( self, bets ) :
#            print ('ComplDer2', self.type)
            if self.dim == 1 :
              return    bets[0]**4 * self.INTxx ( )
            elif self.dim == 3:
                return (  bets[0] ** 4 * self.INTxx()
                        + bets[1] ** 4 * self.INTyy()
                        + bets[2] ** 4 * self.INTzz()
                        + bets[0] ** 2 * bets[1] ** 2 * self.INTxy()
                        + bets[0] ** 2 * bets[2] ** 2 * self.INTxz()
                        + bets[1] ** 2 * bets[2] ** 2 * self.INTyz()
                       )
            else:
              return (  bets[0]**4 * self.INTxx ( )
                      + bets[1]**4 * self.INTyy ( )
                      + bets[0]**2 * bets[1]**2 * self.INTxy ( )
                     )   

    def ComplDer1 ( self, bets ) :
            if self.dim == 1 :
                return  bets[0]**4  * self.INTx()
            else:
                return ( bets[0]**4  * self.INTx()
                       + bets[1]**4  * self.INTy()
                       )
#              return    bets[0]**4 /self.Nxx  /(1./self.A[0].Ub)**2 * self.INTx ( )
 #           else:
  #            return (  bets[0]**4 / self.Nxx  / (1./self.A[0].Ub)**2 * self.INTx ( )
   #                   + bets[1]**4 / self.Nyy  / (1./self.A[1].Ub)**2 * self.INTy ( )
    #                 )

    def Mean ( self ) :                                         #  А как же кол-во дырок   NDT
            if self.param or not SvF.Use_var:    gr = self.grd
            else:                                gr = self.var  # 29
            if self.dim == 1 :
                    return   1./(self.A[0].Ub+1)* sum ( gr[x] * self.fneNDT(x)  for x in self.A[0].NodS )
            else:
                    return ( 1./(self.A[0].Ub+1)/(self.A[1].Ub+1)
                             * sum ( gr[x,y] * self.fneNDT(x,y)  for x in self.A[0].NodS for y in self.A[1].NodS )
                           )  



    def Norma_L2mL2 ( self ) : 
            if self.param or not SvF.Use_var:    gr = self.grd
            else:                                gr = self.var  # 29
            if   self.dim == 1 :
                    return   1./(self.A[0].Ub+1)    \
                             * sum ( gr[x]**2      for x in self.A[0].NodS )
            elif self.dim == 2:
                    return ( 1./(self.A[0].Ub+1)/(self.A[1].Ub+1)
                             * sum ( gr[x,y]**2    for x in self.A[0].NodS
                                                         for y in self.A[1].NodS )
                           )  
            elif self.dim == 3:
                    return ( 1./(self.A[0].Ub+1)/(self.A[1].Ub+1)/(self.A[2].Ub+1)
                             * sum ( gr[x,y,z]**2  for x in self.A[0].NodS
                                                         for y in self.A[1].NodS
                                                         for z in self.A[2].NodS )
                           )  

    def Norma_L2mL2Border ( self ) :
            Bor = self.makeBorder ()
            ret = 0
            NoB = 0
            if self.param or not SvF.Use_var:   gr = self.grd
            else:                               gr = self.var  # 20/02/2023
            for b in Bor :
                  NoB += 1
      #            ret += self.grd[b[0],b[1]]**2
                  ret += gr[b[0], b[1]] ** 2
            return ret/NoB

    def Norma_L2mL2Border3DXY ( self ) :    # для 3 переменных по первым двум
            if self.dim != 3 : return None
            ret = 0
            NoB = 0
            if self.param or not SvF.Use_var:   gr = self.grd
            else:                               gr = self.var  # 20/02/2023
            for i in self.A[0].NodS:
                for j in self.A[1].NodS:
                    for k in self.A[2].NodS:
                        if i == 0 or i == self.A[0].Ub or j == 0 or j == self.A[1].Ub:
                            NoB += 1
                            ret += gr[i,j,k] ** 2
            return ret/NoB

                  
    def SavePoints ( self ) :
        for a in self.A :
            if a.dat is None :  return;
#            if a.num < 0 : print "num < 0  arg=",  a.name;  return;

        Prefix = SvF.Prefix
        if self.dim == 0 : return;
  #      fName = Prefix + self.V.name + "(" +self.A[0].name+ ").txt"
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
            fi.write (  str( self.V.avr + self.Ftbl(n) ) )
            if not self.V.dat is None : 
                fi.write ( '\t'+ str( self.V.avr + self.V.dat[n] ) + '\t' + str ( self.Ftbl(n)-self.V.dat[n] ) )
#            fi.write (  str( self.V.avr + self.Ftbl(n)() ) )
 #           if not self.V.dat is None :
  #              fi.write ( '\t'+ str( self.V.avr + self.V.dat[n] ) + '\t' + str ( self.Ftbl(n)()-self.V.dat[n] ) )

###            for c in range(len(self.Col)) : fi.write ( "\t"+ str( self.tbl[n,self.Col[c].num] ) )
        if SvF.printL : print ("End of SavePoints to", fName)



    def grdNaN (self, i,j=None) :
        if self.dim == 1 :
            if self.fneNDT(i) == 0 : return nan
#            if self.param :
            v = self.grd[i]
 #           else          :  v = self.grd[i]()
        else :
            if self.fneNDT(i,j) == 0 : return nan
#            if self.param :
            v = self.grd[i,j]
 #           else          :  v = self.grd[i,j]()
        return  v

    def grdNDT (self, i,j=None) :
        v = self.grdNaN (i,j)
        if np.isnan(v): return self.NDT
        return  v

    def grdNaNreal (self, i=None,j=None,k=None) :
        if self.dim == 0 :
            return self.grd
        elif self.dim == 1 :
            if self.fneNDT(i) == 0 : return nan
            v = self.grd[i]
        elif self.dim == 2 :
            if self.fneNDT(i,j) == 0 : return nan
            v = self.grd[i, j]
        else:
 #           if self.fneNDT(i, j, k) == 0: return nan
            v = self.grd[i, j, k]

        return  v + self.V.avr

    def grdNDTreal (self, i,j=None) :
        v = self.grdNaNreal ( i,j )
        if np.isnan(v): return self.NDT
        return  v



    def prep_val ( self, val, domain ) :
                      if self.param :     ret = val
                      else          :     ret = val()
                      if   domain == 0 :   return  str(self.NDT)
#                      elif not neNDT  :   return  str(self.NDT)
                      else:               return "%20.16g" % ((self.V.avr + ret))   #  значения
          

    def SaveSolNew ( self, fName ) :         #New   бросил, не отладил...
#      print 'type_dim', self.type,  self.dim

      Prefix = SvF.Prefix
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
                fi.write( self.prep_val ( self.grd[i], self.domain[i] )+'/n' )
          elif self.dim == 2:
              for j in self.A[1].NodS:                       #  точки по y
                  for i in self.A[0].NodS :
#                      print >> fi,  self.prep_val ( self.grd[i,j], self.neNDT[i,j] ),
                      fi.write( self.prep_val(self.grd[i, j], self.domain[i, j]) )
                  fi.write ( '\n' )
    
          elif self.dim == 3:
              for k in self.A[2].NodS:                       #  точки по z
                for j in self.A[1].NodS:                       #  точки по y
                  for i in self.A[0].NodS :
 #                     print >> fi,  self.prep_val ( self.grd[i,j,k], 1 ),  #self.neNDT[i,j] )
                      fi.write( self.prep_val(self.grd[i, j, k], 1) )  # self.neNDT[i,j] )
                  fi.write ( '\n' )
          if SvF.printL > 0 : print ("End of SaveSolNew to", fName)

      else :                                                                  # poly
        print >> f, "%d" % self.dim + " %d" % self.PolyPow + " %d" % self.sizeP

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

        fung = self.gClone(True)
        fung.SaveSol(fName)
        if SvF.printL > 0 : print ("END of pFun.SaveSol to ", fName)
      fi.close()
      return


    def SaveSol ( self, fName='' ) :                ## OLD
#      self.var_to_grd()
      Prefix = SvF.Prefix
      
      if SvF.printL > 0 : print ('Before SaveSol to ', fName, self.type)
      if fName == '' :
          if  self.type[0] == 'g'  or self.type == 'smbFun':   # 2505    # 2407
                                fName = Prefix +self.nameFun() + ".sol"
          else                : fName = Prefix +self.nameFun() + ".p.sol"
      if SvF.printL > 0 : print ('SaveSol to ', fName, self.type)
      try:
            fi = open ( fName, "w")
      except IOError as e:
            print ("Can''t open file: ", fName)
            return

      if self.type[0] == 'g'  or self.type == 'smbFun':   # 2505
          for a in self.A : fi.write ( a.name + '\t' )
          fi.write ( self.V.name )
          if   self.dim==0 :
              fi.write ( '\t#SvFver_62_tbl\n' )
              v = self.grdNaNreal()
              fi.write( str_val ( v ) )
          elif self.dim==1 :
            fi.write ( '\t#SvFver_62_tbl\n' )
            A = self.A[0]
            V = self.V
            for i in A.NodS :
                v = self.grdNaNreal(i)
#                fi.write( str(A.min + A.step*i) + "\t" + str_val(v)+'\n' )
                fi.write( str(A.Val[i]) + "\t" + str_val(v)+'\n' )

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
                    fi.write( "\t" + str_val(v) )

          elif self.dim==3 :
              fi.write ( '\t#SvFver_62_mtr3\n' )
              for a in self.A :
                  for j in a.NodS :  fi.write ( "\t" + str(a.min + a.step*j) )     #  точки по x,y,z
                  fi.write ( '\n' )
              for k in self.A[2].NodS:                       #  точки по z
                for j in self.A[1].NodS:                       #  точки по y
                  for i in self.A[0].NodS :
#                      print >> fi,  self.prep_val ( self.grd[i,j,k], 1 ) + '\t',  #self.neNDT[i,j] )
                      v = self.grdNaNreal(i,j,k)
                      fi.write( str_val(v) + '\t' )
#                      fi.write( self.prep_val ( self.grd[i,j,k], 1 ) + '\t' )
                  fi.write ( '\n' )
#      elif self.type == 'smbFun':          pass
      else :                                                    # POLY
        fi.write ( "%d" % self.dim + " %d" % self.PolyPow + " %d" % self.sizeP + '\n' )

        for d in range(self.dim):
            fi.write ( '('+self.A[d].name +'-'+str(self.A[d].min)+')/'+str(self.A[d].ma_mi) +'\t' )
        fi.write ( self.V.name + Prefix )   #Prefix + '\t#SvFver_62_poly\n'

        for i in self.PolyR :
            fi.write ( "\n" + str_val( self.grd[i] ) + "\t" + str(self.pow[i][0]) )   # 29
            if self.dim == 2 :
                fi.write ( "\t" + str(self.pow[i][1]) )
        fung = self.gClone(True)
        gfName = fName.replace ('.p.', '.')
        fung.SaveSol(gfName)
      fi.close()
      if SvF.printL > 0 : print ("END of SaveSol to ", fName, self.type)

      return


    def ReadSol ( self, fName='', printL=0 ) :
      if self.type == 'smbFun':  ##########################
          return
#      print 'self.Task.Mng.Prefix'+self.Task.Mng.Prefix+'|',fName
      Prefix = SvF.Prefix
      if fName == '' :
          if self.type[0] == 'g':      # 2407
              fName = Prefix +self.nameFun() + ".sol"
          else                : fName = Prefix +self.nameFun() + ".p.sol"
      try:
            fi = open ( fName, "r")
      except IOError as e:
            print ("Can''t open file: ", fName)
            return False
      head = fi.readline().split()
      print ("ReadSol from", fName,  head )
######################################################
      if head[0][0:4] == '#SvF' :    #New   бросил, не отладил...
         ver = head[0].split('_')
 #        print ('ver', ver)

         if ver[1] == '64' :
            dim = int (ver[3])
            if ver[2] == 'g' :
                  StepInStep = []
                  for d in range (dim) :
                        StepInStep.append(float(len(fi.readline().split())-1)/self.A[d].Ub)
#                        Af = []
#                        for a in A : Af.append ( float(a) ) 
 #                       Arg.append ( Af )
 #                       print (self.A[d].Ub)
  #                print ('StepInStep', StepInStep)
                  tb = np.loadtxt ( fi,'double' )
                  if SvF.printL : print ("shape", tb.shape)
                                
                  if self.dim==0 :
#                        self.grd.value = float(fi.readline()) 
                        self.grd.value = tb
   #                     print ('TTT', self.grd())
                        
                  elif self.dim==1 :
#                       tb = np.loadtxt (fi,'double')
 #                      if printL : print "shape", tb.shape
                       for j in self.A[0].NodS :
                           self.grd[j].value = (tb[int(j*StepInStep[0]), 0]-self.V.avr)  #  значения в новых узлах 
                  elif dim==2 :
  #                     tb = np.loadtxt (fi,'double')
   #                    if printL : print "shape", tb.shape

                       #for j in self.A[1].NodS :
                        # for i in self.A[0].NodS :
                         #  self.grd[i,j].value = (tb[int(j*StepInStep[1]),int(i*StepInStep[0])] -self.V.avr)  #  значения в новых узлах
                         
#                        fi.readline().split()
 #                       tb = np.loadtxt (fi,'double')
                        if SvF.printL : print ("shape", tb.shape)

                        for j in self.A[1].NodS :
                            for i in self.A[0].NodS :
                                self.grd[i,j].value = (tb[int(j*(tb.shape[0]-1)/self.A[1].Ub)       
                                                         ,int(i*(tb.shape[1]-1)/self.A[0].Ub)   
                                                         ] -self.V.avr)  #  значения в новых узлах
                        fi.close()
                        if SvF.printL > 0 : print ("End of Fun.ReadSol from"), fName


#                       print self.grd[0,0].value, self.grd[self.A[0].Ub,self.A[1].Ub].value
            fi.close()
            if SvF.printL > 0 : print ("End of Fun.ReadSol from", fName)
            print ("End of Fun.ReadSol from", fName)
            return
##############################################################################
      if self.type[0] == 'g' :         # 2407
  #      print ('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%', self.V.name, fName)
   #     print (self.grd)
        gr = self.grd
        if self.dim==0 :
            self.grd = float(fi.readline())                  #   !  gr  !
#            print ('*************************************gr', gr, self.grd)
###            fi.close()
        elif self.dim==1 :
###           fi.close()
           fun = FunFromSolFile ( fName, False )
           for j in self.A[0].NodS :
                if self.fneNDT(j) == 0:
#                    self.grd[j].value = nan
                    gr[j] = nan
                else :
                    gr[j] = fun.F1_extra_const ( self.A[0].min + j * self.A[0].step ) -self.V.avr   #  значения в новых узлах
                    if np.isnan(gr[j]): gr[j] = 1
        elif self.dim==2 :
###           fi.close()
           fun = FunFromSolFile ( fName, False )
           for j in self.A[1].NodS :
               for i in self.A[0].NodS :
                   if self.fneNDT(i,j) == 0:
                       gr[i,j] = nan
 #                      self.grd[i,j].value = nan
                   else :
                       gr[i,j] = fun.F2_extra_const ( self.A[0].min + i * self.A[0].step,
                                          self.A[1].min + j * self.A[1].step) -self.V.avr  #  значения в новых узлах
                       if np.isnan(gr[i,j]) :  gr[i,j] = 1
#                       if np.isnan(gr[i,j]) :  self.grd[i,j] = 1

#                       self.grd[i,j].value = fun.F2_extra_const ( self.A[0].min + i * self.A[0].step,
 #                                         self.A[1].min + j * self.A[1].step) -self.V.avr  #  значения в новых узлах
  #                     if np.isnan(self.grd[i,j].value) :  self.grd[i,j].value = 1

        elif self.dim==3 :
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
                  tb = np.loadtxt (fi,'double')
                  if SvF.printL : print ("shape", tb.shape)
                  for k in self.A[2].NodS :
                    for j in self.A[1].NodS :
                      for i in self.A[0].NodS :
#                        print k, j, i,   int(k*StepInStep[2]) * len(A[1]) + int(j*StepInStep[1])
#                        self.grd[i,j,k].value = (tb[ int(k*StepInStep[2]) * len(A[1]) + int(j*StepInStep[1])
                        gr[i,j,k] = (tb[ int(k*StepInStep[2]) * len(A[1]) + int(j*StepInStep[1])
                                                    ,int(i*StepInStep[0])
                                                   ] -self.V.avr)  #  значения в новых узлах
      else :                                                    # POLY
            nums = head  #fi.readline().split()          #  1 7 8
            file_dim = int(nums[0])
            file_sizeP = int(nums[2])
            if SvF.printL : print ("file_dim=", file_dim," dim=", self.dim)
            if file_dim > self.dim :
                print ("*************************** ReadSol Poly  file_dim > dim", file_dim,">", self.dim)
                return
            fi.readline()                   # (sCO2M-270.0)/100.0	Pm
            tb = np.loadtxt (fi,'double')      #  коеф  и степени
            if SvF.printL : print ("ReadSol from", fName, "shape", tb.shape)

            if self.param and (file_sizeP!=self.sizeP):
                print ("******************* ReadSol Poly for param file_sizeP!=self.sizeP", file_sizeP, self.sizeP)
                return
            for i in self.PolyR :  self.grd[i] = 0   # обнуляем
            if file_dim == self.dim :
                    for i in range (min(file_sizeP, self.sizeP)) :    self.grd[i] = tb[i,0]
            else :   # file_dim < self.dim      1 < 2
                    for i_file in range (file_sizeP) :
                        for i_self in self.PolyR :
                            if self.pow[i_self][0] == tb[i_file,1] and self.pow[i_self][1] == 0 :
                                self.grd[i_self] = tb[i_file,0]
      self.grd_to_var()
      if SvF.printL > 0 : print ("End of ReadSol from", fName )
      fi.close()
           

    def InitByData ( self ) :
      if self.V.dat is None : return
      if self.type == 'p':    return
      if self.type == 'smbFun':    return
#      print('IB*+++++++++++++', self.name, self.param)

      if self.dim==0 :
        if self.V.dat[0] != self.NDT :
                self.grd = self.V.dat[0]
      elif self.dim==1 :
#        print   (self.name, self.A[0].name, self.A[0].dat, self.sR)
        for m in self.sR :
#            print (m)
            if self.V.dat[m] == self.NDT or np.isnan (self.V.dat[m]): continue
#            self.grd[int(floor(0.499999999 + self.A[0].dat[m]/self.A[0].step))] = self.V.dat[m]
            self.grd[self.A[0].IndByVal(self.A[0].dat[m])] = self.V.dat[m]
 #           print ('HH', m)
        for x in self.A[0].NodS:   ####   ??????????????????
            if self.fneNDT(x) == 0:
                self.grd[x] = nan

      elif self.dim==2 :
        for m in self.sR :
            if self.V.dat[m] == self.NDT or np.isnan (self.V.dat[m]):  continue
#            self.grd [ int (floor(0.499999999 + self.A[0].dat[m]/self.A[0].step)),
 #                      int (floor(0.499999999 + self.A[1].dat[m]/self.A[1].step))
  #                   ] = self.V.dat[m]
            self.grd [ self.A[0].IndByVal(self.A[0].dat[m]),                # не проверенр
                       self.A[1].IndByVal(self.A[1].dat[m])
                     ] = self.V.dat[m]


        for y in self.A[1].NodS :
            for x in self.A[0].NodS :
                if self.fneNDT(x,y)==0 :
                    self.grd[x,y] = nan
      self.grd_to_var()


    def SaveDeriv ( self, fName ) :                  #  В корзинку  !!
      if SvF.printL : print   ('SaveDeriv')
      if self.type == 'g' and self.dim==0 : return
      
      elif self.type == 'g' and self.dim==1 :
        A = self.A[0]
        V = self.V
        if fName == '' :  fName = SvF.Prefix+V.name + "(" +A.name+ ").der"
        fi = open ( fName, "w")
#        fi.write ( A.name + '\t' + V.name + "_der")
        fi.write ( A.name + '\t' + V.name + "_der \t#SvFver_62_tbl")
        for i in A.mNodSm :
            fi.write ( "\n" + str(A.min + A.step*i)
                     + "\t" + str( (self.grd[i+1]-self.grd[i-1]) / (2*A.step) ) )
#                     + "\t" + str( (self.grd[i+1]()-self.grd[i-1]()) / (2*A.step) ) )
        fi.close()
      elif self.type == 'g' and self.dim==2 :
        Ax = self.A[0]
        Ay = self.A[1]
        V = self.V
    # Y
        if fName == '' :  fName = SvF.Prefix+V.name + "(" +Ax.name+ ',' +Ay.name+ ").d_d"+ Ay.name
        fi = open ( fName, "w")
        fi.write ( Ax.name + '\t' + Ay.name + '\td' + V.name + "_d"+ Ay.name+ '\t#SvFver_62_matr2\n')       #  загол
        for i in Ax.NodS :  fi.write ( "\t" + str(Ax.min + Ax.step*i) )     #  точки по х
        for j in Ay.mNodSm :
            fi.write ( "\n" + str(Ay.min + Ay.step*j) )     #  точки по y
            for i in Ax.NodS :
                fi.write ( "\t" + str(V.avr + (self.grd[i,j+1]-self.grd[i,j-1]) /(2*Ay.step) ) )  #  значения
        #        fi.write("\t" + str(V.avr + (self.grd[i, j + 1]() - self.grd[i, j - 1]()) / (2 * Ay.step)))  # значения
        fi.close()
    # X
        fName = SvF.Prefix+V.name + "(" +Ax.name+ ',' +Ay.name+ ").d_d"+Ax.name
        fi = open ( fName, "w")
        fi.write ( Ax.name + '\t' + Ay.name + '\td' + V.name + "_d"+Ax.name + '\t#SvFver_62_matr2\n')       #  загол
        for i in Ax.mNodSm :  fi.write ( "\t" + str(Ax.min + Ax.step*i) )     #  точки по х
        for j in Ay.NodS :
            fi.write ( "\n" + str(Ay.min + Ay.step*j) )     #  точки по y
            for i in Ax.mNodSm :
                fi.write ( "\t" + str(V.avr + (self.grd[i+1,j]-self.grd[i-1,j]) /(2*Ax.step) ) )  #  значения
#                fi.write ( "\t" + str(V.avr + (self.grd[i+1,j]()-self.grd[i-1,j]()) /(2*Ax.step) ) )  #  значения
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
                    val = self.grd[j]
#                    if self.param : val = self.grd[j]
 #                   else          : val = self.grd[j]()
                    if np.isnan (val) : continue
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
                    val = self.grd[j, i]
#                    if self.param : val = self.grd[j,i]
 #                   else          : val = self.grd[j,i]()
                    if np.isnan (val) : continue
                    if mi is None :
                        mi = val
                        ma = val
                    else :    
                        if val < mi : mi = val
                        if val > ma : ma = val
        return mi, ma


    def  CopyMtr (self, copy_dat = False, name='') :                   # outofdate ?
        ret = self.gClone(copy_dat)
        if name != '':  ret.V.name = name
        return ret


    def CopyInParam (self) :              #  всегда возвращает Парам
        if self.dim == 0 or self.type == 'p' : return None
        ret = deepcopy(self)    # 29
        ret.param = True
        ret.var   = None    #  ?????

#        tmp = self.grd
 #       if self.param :
  #          return deepcopy(self)
   #     else :
    #        tmp = self.grd
     #       self.grd = None        # not copy pyomo strucher
      #      ret = deepcopy(self)
       #     self.grd = tmp

#            ret.param = True

 #           if ret.dim==1 :
  #              ret.grd = np.zeros ( ret.A[0].Ub+1,np.float64 )
   #             for i in ret.A[0].NodS :
    #                    ret.grd[i] = self.grd[i]()
     #       elif ret.dim==2 :
      #          ret.grd = np.zeros ( (ret.A[0].Ub+1, ret.A[1].Ub+1),np.float64 )
       #         for i in ret.A[0].NodS :
        #              for j in ret.A[1].NodS :
         #               ret.grd[i,j] = self.grd[i,j]()
        return ret



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



    def ArgsNorm_step ( self, ArS_real ) :    # нормализация аргументов
        return [(ArS_real[a]-self.A[a].min)/self.A[a].step for a in range (self.dim) ]

#        Args = []
 #       for a in range (self.dim) : Args.append ((ArS_real[a]-self.A[a].min)/self.A[a].step)
  #      return Args



    def F_or0 ( self, ArS_real0, ArS_real1 = None  ) :
        if ArS_real0 < self.A[0].min : return 0
        if ArS_real0 > self.A[0].max : return 0
        if ArS_real1 is None:
            return self.F([ArS_real0])
        else:
            if ArS_real1 < self.A[0].min: return  0
            if ArS_real1 > self.A[0].max: return  0
            return self.F ( [ ArS_real0, ArS_real1 ] )
#        if ArS_real[0] < self.A[0].min : return 0
 #       if ArS_real[0] > self.A[0].max : return 0
  #      if self.dim == 2:
   #         if ArS_real[1] < self.A[0].min: return  0
    #        if ArS_real[1] > self.A[0].max: return  0
     #   return self.F (ArS_real )


    def INTx ( self ) :                                                                    # self.fneNDT(x) ??
      if self.type[0] == 'g' and self.dim==1 :
        return  sum ( self.fneNDT(x-1) * self.fneNDT(x) * self.fneNDT(x+1) * self.f_gap(x) *
                     ( self.grd[x+1] - self.grd[x-1] )**2  
		    for x in self.A[0].mNodSm )
      elif self.type[0] == 'g' and self.dim==2 :
        return  sum ( self.fneNDT(x-1,y) * self.fneNDT(x,y) * self.fneNDT(x+1,y) * self.f_gap(x,y) *
                     ( self.grd[x+1,y] - self.grd[x-1,y] )**2  
                    for y in self.A[1].NodS    for x in self.A[0].mNodSm )

    def derivXX (self, xy ) :
        if self.param or not SvF.Use_var:   gr = self.grd
        else:                               gr = self.var  # 29
        if self.dim == 1:
            return   (gr[xy - 1] - 2 * gr[xy] + gr[xy + 1]) / self.A[0].step**2



    def INTxx ( self ) :
#      print ('gG INTxx', self.type)
       if self.type[0] == 'g' :     # 2407
          if self.param or not SvF.Use_var:     gr = self.grd
          else:                                 gr = self.var  # 29
#          print ("Use", SvF.Use_var)
          if   self.dim==1 :
          #   return  sum ( self.fneNDT(x-1) * self.fneNDT(x) * self.fneNDT(x+1) * self.f_gap(x) *
           #                ( gr[x-1]-2*gr[x]+gr[x+1] )**2   for x in self.A[0].mNodSm
            #             )  /self.Nxx  /(1./self.A[0].Ub)**4
             return  sum ( self.fneNDT(x-1) * self.fneNDT(x) * self.fneNDT(x+1) * self.f_gap(x) *
                          ( self.derivXX ( x ) )**2   for x in self.A[0].mNodSm
                       )  /self.Nxx  *  self.A[0].ma_mi**4  #self.A[0].Ub**4 * self.A[0].step**4

          elif self.dim==2 :
 #            if self.param or not SvF.Use_var:           #   * nan
                 summa = 0
                 for x in self.A[0].mNodSm :
                     for y in self.A[1].NodS :
                         if self.fneNDT(x-1,y) * self.fneNDT(x,y) * self.fneNDT(x+1,y) * self.f_gap(x,y) != 0 :
                             summa +=  self.f_gap(x,y) * ( gr[x-1,y]-2*gr[x,y]+gr[x+1,y] )**2
                 return summa * float(self.A[0].Ub**4) / self.Nxx

          elif self.dim==3 :
  #           return  sum ( self.fneNDT(x-1,y) * self.fneNDT(x,y) * self.fneNDT(x+1,y) * self.f_gap(x,y) *
             return  1 / ((self.A[2].Ub+1)*(self.A[1].Ub+1)*(self.A[0].Ub-1)) / (1./self.A[0].Ub)**4        \
                       * sum ( 
                        ( gr[x-1,y,z]-2*gr[x,y,z]+gr[x+1,y,z] )**2
                       for z in self.A[2].NodS   for y in self.A[1].NodS    for x in self.A[0].mNodSm ) 


    def  SetVal ( self, val = 0 ) :
            for i in self.A[0].NodS :
                for j in self.A[1].NodS :
 #                   if self.param:
                      if self.grd[i,j] != self.NDT  :
                        self.grd[i,j] = val
  #                  else :
   #                   if self.grd[i,j].value != self.NDT  :
    #                    self.grd[i,j].value = val



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
            if np.isnan(self.grd[x,y]): continue
            self.grd[x, y] = Val

    def Neighbors (self,x,y,dist=1,plus = False) :  # plus  сама точка
        Neighb = []
        idist = int(np.ceil(dist))
        for i in range( -idist, idist + 1, 1):
            if x+i < 0: continue
            if x+i > self.A[0].Ub: continue
            for j in range( -idist, idist + 1, 1):
                if y+j < 0: continue
                if y+j > self.A[1].Ub: continue
                if i==0 and j==0  and not plus: continue
                if i**2 + j**2 > dist**2 : continue
                Neighb.append([x+i, y+j])
        return Neighb


    def FloodFillReal (self, xy, BordVal,FillVal) :
        self.FloodFill([self.A[0].ValToInd (xy[0]), self.A[1].ValToInd (xy[1])], BordVal, FillVal)


    def FloodFill (self, xy_in, BordVal,FillVal) :
        quer = [xy_in]   # очередь
        pos = 0
        while len (quer) > pos :
            xy = quer[pos]
            if     self.grd[xy[0], xy[1]] != BordVal \
               and self.grd[xy[0], xy[1]] != FillVal \
               and  not np.isnan(self.grd[xy[0], xy[1]]) :
                    self.grd[xy[0], xy[1]] = FillVal
                    quer = quer + self.Neighbors (xy[0],xy[1])
            pos += 1
 #           print 'QU', pos, len (quer)


        print ('FF', xy, self.grd[xy[0],xy[1]])
        if     self.grd[xy[0],xy[1]] == BordVal \
            or self.grd[xy[0],xy[1]] == FillVal \
            or np.isnan(self.grd[xy[0],xy[1]]) :
            return
        star += 1
        if star >= 998: return
        self.grd[xy[0],xy[1]] = FillVal
        print (star, xy[0],xy[1])
        nei = self.Neighbors (xy[0],xy[1])
        for xy1 in nei :
            self.FloodFill (xy1, BordVal,FillVal,star)
        return



    def getVal (self, x, y=nan) :                        #  если все ОК возвращает значение
        if x < 0:  return nan
        if x > self.A[0].Ub:  return nan
        if self.dim == 1 :  return self.grdNaN (x)                  # real ???
#            if self.fneNDT(x) == 0: return nan
 #           if self.param:  return self.grd[x]
  #          else:           return self.grd[x]()
        else :
            if y < 0:  return nan
            if y > self.A[1].Ub:  return nan
            return self.grdNaN(x,y)                     # real ???
 #           if self.fneNDT(x,y) == 0 : return nan
  #          if self.param :   return self.grd[x,y]
   #         else          :   return self.grd[x,y]()


    def Smoothing (self, dh=nan, max_ang_grad=nan, mask=None, mVal=None) :     # усреднение по 9 точкам  для точек mask=mVal
        print ("Smoothing start ")
        num_change = 0
        if not np.isnan(max_ang_grad) :
            max_ang_rad = max_ang_grad /180.*pi
            print (max_ang_grad, max_ang_rad)
#        XYs = []
        for y in self.A[1].NodS :
            for x in self.A[0].NodS : # XYs.append([x,y])
        #for xy in XYs :
    #            x = xy[0]
     #           y = xy[1]
                if np.isnan(self.grd[x, y]) : continue
                if not mask.grd[x,y] is None :
                    if mask.grd[x,y] != mVal: continue
                sum = 0
                num = 0
                max_ang = .0
                for i in range (-1,2,1) :
                    for j in range(-1, 2, 1):
 #                       print 'j', j
                        v = self.getVal(x+i,y+j)
                        if np.isnan(v) : continue
                        if (not np.isnan(max_ang_grad)) and i!=0 and j!=0 :         # по углу
                            ang = abs((v-self.grd[x,y])/np.sqrt((i*self.A[0].step)**2+(j*self.A[0].step)**2))
                            if ang >= max_ang :
                                max_ang = ang
                                v_ang = v
                                v_mask = mask.grd[x+i,y+j]
                        if not np.isnan(dh):
                            num += 1
                            sum += v
                if not np.isnan(max_ang_grad):
                    if max_ang > max_ang_rad :
                        print ('SrezaemAng: ', max_ang, v_ang, self.grd[x, y], x, y, x + i, y + j,)
                        self.grd[x, y] = 0.7 * self.grd[x, y] + 0.3 * v_ang
                        print (self.grd[x, y], v_mask)
                        num_change += 1

                if not np.isnan(dh):
                    if num <= 1: continue
                    new = sum/num
                    if abs (new-self.grd[x, y]) < dh: continue
#                    if abs ( (num*new-self.grd[x, y])/(num-1)-self.grd[x, y] ) < dh: continue
                    print ('Srezaem: ', new, self.grd[x, y], x,y)
                    self.grd[x, y] = new
                    num_change += 1
        print  ("num_change",    num_change)

    def d_dx(self,x,y=nan): #  на границе  левая и правая  иначе центральная
            i1 = max ( x-1, 0)
            i2 = min ( x+1, self.A[0].Ub )
            if self.type[0] == 'g' and self.dim == 1:
                v1 = self.getVal(i1)
                v2 = self.getVal(i2)
            elif self.type[0] == 'g' and self.dim == 2:
                v1 = self.getVal(i1,y)
                v2 = self.getVal(i2,y)
            if np.isnan (v1) : return nan
            if np.isnan (v2) : return nan

            return (v2 - v1)/(i2 - i1) / self.A[0].step

    def d_dy(self, x, y):  # на границе  левая и правая  иначе центральная
        i1 = max(y - 1, 0)
        i2 = min(y + 1, self.A[1].Ub)
        if self.type[0] == 'g' and self.dim == 2:
            v1 = self.getVal(x, i1)
            v2 = self.getVal(x, i2)
        if np.isnan(v1): return nan
        if np.isnan(v2): return nan

        return (v2 - v1) / (i2 - i1) / self.A[1].step



    def Make_1_Deriv(self, der='x'):
        if SvF.printL: print   ('MakeDeriv1')
        ret = self.gClone()
#        ret = self.Clone()
        if self.type[0] == 'g' and self.dim == 1:
            for i in self.A[0].NodS: ret.grd[i] = self.d_dx (i)
        elif self.type[0] == 'g' and self.dim == 2:
            for i in self.A[0].NodS:
                for j in self.A[1].NodS:
                    if der=='x' :   ret.grd[i,j] = self.d_dx(i,j)
                    else        :   ret.grd[i,j] = self.d_dy(i,j)
        return ret

    def TiltAngle (self) :
        if self.type[0] == 'g' and self.dim == 2:
            X = self.Make_1_Deriv ()
            Y = self.Make_1_Deriv ('y')
            for i in self.A[0].NodS:
                for j in self.A[1].NodS:
                    X.grd[i,j] = np.sqrt (X.grd[i,j]**2+Y.grd[i,j]**2)
            return X
        return None

    def makeMtrParamVnameSetG ( self, Vname, gr_value = 0 ) :
        ret = gFun2(self)   #  Устарело
        ret.grd = np.zeros((ret.A[0].Ub + 1, ret.A[1].Ub + 1), np.float64)
        if gr_value != 0:
            for i in ret.A[0].NodS:
                for j in ret.A[1].NodS:
                    ret.grd[i, j] = gr_value
        ret.V.name = Vname
        ret.param = True
        ret.V.avr = 0   # 19.12.19
        return ret

    def INTy ( self ) :
        return  sum ( self.fneNDT(x,y-1) * self.fneNDT(x,y) * self.fneNDT(x,y+1) * self.f_gap(x,y) *
                     ( self.grd[x,y+1] - self.grd[x,y-1] )**2 
                    for y in self.A[1].mNodSm  for x in self.A[0].NodS )


    def INTyy ( self ) :
        if self.param or not SvF.Use_var:   gr = self.grd
        else:                               gr = self.var  # 29

        if   self.dim==2 :
 #           if self.param or not SvF.Use_var:
                summa = 0
                for x in self.A[0].NodS:
                    for y in self.A[1].mNodSm:
                        if self.fneNDT(x,y-1) * self.fneNDT(x,y) * self.fneNDT(x,y+1) * self.f_gap(x,y) != 0:
                            summa += self.f_gap(x,y) * ( gr[x,y-1]-2*gr[x,y]+gr[x,y+1] )**2
                #                        print( summa)
     #           summa *= float(self.A[1].Ub ** 4) / self.Nyy
#               print('SYY', summa)
                return summa * float(self.A[1].Ub ** 4) / self.Nyy
#            return  sum ( self.fneNDT(x,y-1) * self.fneNDT(x,y) * self.fneNDT(x,y+1) * self.f_gap(x,y) *
 #                    ( gr[x,y-1]-2*gr[x,y]+gr[x,y+1] )**2
  #                  for y in self.A[1].mNodSm  for x in self.A[0].NodS )   / self.Nyy  / (1./self.A[1].Ub)**4
        elif self.dim==3 :
             return  1 / ((self.A[2].Ub+1)*(self.A[1].Ub-1)*(self.A[0].Ub+1)) / (1./self.A[1].Ub)**4        \
                       * sum ( 
                        ( gr[x,y-1,z]-2*gr[x,y,z]+gr[x,y+1,z] )**2
                       for z in self.A[2].NodS   for y in self.A[1].mNodSm    for x in self.A[0].NodS ) 


    def INTzz ( self ) :
        if self.param or not SvF.Use_var:   gr = self.grd
        else:                               gr = self.var  # 29
        if self.dim==3 :
             return  1 / ((self.A[2].Ub+1)*(self.A[1].Ub-1)*(self.A[0].Ub+1)) / (1./self.A[2].Ub)**4        \
                       * sum (
                        ( gr[x,y,z-1]-2*gr[x,y,z]+gr[x,y,z+1] )**2
                       for z in self.A[2].mNodSm   for y in self.A[1].NodS    for x in self.A[0].NodS )

    def INTxz ( self ) :
        if self.param or not SvF.Use_var:  gr = self.grd
        else:                              gr = self.var  # 29
        if self.dim==3 :
             return   2. / ((self.A[2].Ub-1)*(self.A[1].Ub+1)*(self.A[0].Ub-1)) * 0.25 / (1./self.A[0].Ub)**2 / (1./self.A[2].Ub)**2   \
                       * sum (
                        ( gr[x+1,y,z+1]-gr[x+1,y,z-1]-gr[x-1,y,z+1]+gr[x-1,y,z-1] )**2
                       for z in self.A[2].mNodSm   for y in self.A[1].NodS    for x in self.A[0].mNodSm )

    def INTyz ( self ) :
        if self.param or not SvF.Use_var:  gr = self.grd
        else:                              gr = self.var  # 29
        if self.dim==3 :
             return   2. / ((self.A[2].Ub-1)*(self.A[1].Ub-1)*(self.A[0].Ub+1)) * 0.25 / (1./self.A[1].Ub)**2 / (1./self.A[2].Ub)**2   \
                       * sum (
                        ( gr[x,y+1,z+1]-gr[x,y+1,z-1]-gr[x,y-1,z+1]+gr[x,y-1,z-1] )**2
                       for z in self.A[2].mNodSm   for y in self.A[1].mNodSm    for x in self.A[0].NodS )



    def INTxy ( self ) :
        if self.param or not SvF.Use_var:  gr = self.grd
        else:                              gr = self.var  # 29

        if   self.dim==2 :
#            if self.param or not SvF.Use_var:
                summa = 0
                for x in self.A[0].mNodSm:
                    for y in self.A[1].mNodSm:
                        if self.fneNDT(x+1,y+1) * self.fneNDT(x+1,y-1) * self.fneNDT(x-1,y+1) * self.fneNDT(x-1,y-1) *self.f_gap(x, y) != 0:
                            summa += self.f_gap(x, y) * ( gr[x+1,y+1]-gr[x+1,y-1]-gr[x-1,y+1]+gr[x-1,y-1] )**2
                #                        print( summa)
 #               summa *= 2 / self.Nxy * 0.25 * self.A[0].Ub**2 * self.A[1].Ub**2
#                print('SYY', summa)
                return summa * 2 / self.Nxy * 0.25 * self.A[0].Ub**2 * self.A[1].Ub**2
  #          return  sum ( self.fneNDT(x+1,y+1) * self.fneNDT(x+1,y-1) * self.fneNDT(x-1,y+1) * self.fneNDT(x-1,y-1) * self.f_gap(x,y) *
   #                  ( gr[x+1,y+1]-gr[x+1,y-1]-gr[x-1,y+1]+gr[x-1,y-1] )**2
    #                for y in self.A[1].mNodSm  for x in self.A[0].mNodSm )                \
     #                               * 2. / self.Nxy * 0.25 / (1./self.A[0].Ub)**2 / (1./self.A[1].Ub)**2
        elif self.dim==3 :
             return   2. / ((self.A[2].Ub+1)*(self.A[1].Ub-1)*(self.A[0].Ub-1)) * 0.25 / (1./self.A[0].Ub)**2 / (1./self.A[1].Ub)**2   \
                       * sum ( 
                        ( gr[x+1,y+1,z]-gr[x+1,y-1,z]-gr[x-1,y+1,z]+gr[x-1,y-1,z] )**2
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
#                fi.write( "\t" + "%20.16g" % (grdNaNreal(i,j)) )  # значения    19.12.19
                fi.write( "\t" + "%20.16g" % (self.grdNaNreal(i,j)) )  # значения    9.05.22
        fi.close()
        print ("End of SaveTbl")




    def SaveSet ( self, fn, TranspSet = 'N' ) :
        if TranspSet == 'N':
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
            if TranspSet == 'N':
                if self.type[0] == 'g' :
                    f.write(" " + str(self.grdNDTreal(x, Ay.Ub-y)))
            else :
              f.write(" " + str(self.grdNDTreal(Ay.Ub-y,x)))
        f.close()
        print ("END of SaveSet")



# ********************************************************************************************** #
class Fun (BaseFun) :
    def __init__ (self, Vname='',  As=[], param=False, Degree=-1,  Finitialize = 1, DataReadFrom = '',Data=[],
                  Type='g', Domain = None, ReadFrom = '' ) :
        BaseFun.__init__ (self, Vname,  As, param, Degree,  Finitialize, DataReadFrom, Data,
                  Type, Domain, ReadFrom)

    def F ( self, ArS_real ) :
          if self.dim == 0:                           #  31
                if SvF.Use_var: return self.var
                else          : return self.grd
          ar =  self.ArgsNorm_step ( ArS_real )
          if ( self.type[0] == 'g' ) and self.dim==1 :       # 2407
            return self.interpol ( 1, ar[0] )
          elif ( self.type[0] == 'g' ) and self.dim==2 :       # 2407
            return self.interpol ( 2, ar[0], ar[1] )
          elif self.type[0] == 'g' and self.dim==3 :
              return self.interpol ( 3, ar[0], ar[1], ar[2] )

    def Ftbl ( self, n ) :
      if self.type[0] == 'g':      # 2407
        if   self.dim==1 :
   #         print ( self.V.name,n)
  #          print (self.A[0].dat)
   #         print (self.A[0].dat[n])
            return self.interpol ( 1, (self.A[0].dat[n]-self.A[0].min)/self.A[0].step )
        elif self.dim==2 :
            return self.interpol ( 2, self.A[0].dat[n]/self.A[0].step,
                                      self.A[1].dat[n]/self.A[1].step )
        elif self.dim==3 :
            return self.interpol ( 3, self.A[0].dat[n]/self.A[0].step,
                                      self.A[1].dat[n]/self.A[1].step,
                                      self.A[2].dat[n]/self.A[2].step )

    def interpol ( self, lev, X,Y=0,Z=0 ) :   # X,Y,Z  в шагах
        if self.param or not SvF.Use_var: gr = self.grd
        else                            : gr = self.var            # 29
 #       print ("Use", SvF.Use_var)
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
            Xi = ifloor (X)      #int(floor ( X ))
            if Xi < 0            : Xi = 0
            if Xi==self.A[0].Ub  : Xi=self.A[0].Ub-1
            dX = X-Xi
            if abs(dX) < 1e-10   :
                if self.dim == 1 :  return  gr[Xi       ]
                if self.dim == 2 :  return  gr[Xi ,Y    ]
                if self.dim == 3 :  return  gr[Xi ,Y , Z]
            if abs(dX-1) < 1e-10 :
                if self.dim == 1 :  return  gr[Xi+1       ]
                if self.dim == 2 :  return  gr[Xi+1 ,Y    ]
                if self.dim == 3 :  return  gr[Xi+1 ,Y , Z]
            else                 :
                if self.dim == 1 :  return  gr[Xi       ] * (1-dX) + gr[Xi+1       ] * dX
                if self.dim == 2 :  return  gr[Xi ,Y    ] * (1-dX) + gr[Xi+1 ,Y    ] * dX
                if self.dim == 3 :  return  gr[Xi ,Y , Z] * (1-dX) + gr[Xi+1 ,Y , Z] * dX



