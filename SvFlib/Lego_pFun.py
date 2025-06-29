# -*- coding: UTF-8 -*-

from Lego import *
import sympy as sy
from itertools import combinations_with_replacement

class pFun (BaseFun) :
    def __init__ (self, Vname='',  As=[], param=False, Degree=-1,  Finitialize = 0, DataReadFrom = '',Data=[], Type='g', Domain = None ):
        BaseFun.__init__(self, Vname, As, param, Degree, Finitialize, DataReadFrom, Data, Type, Domain)

        if SvF.Compile : return    #  ???

        self.grd   = np.zeros ( self.sizeP )
        self.PolyR = range ( self.sizeP )
        self.pow   = CrePolyPow ( self.dim, self.PolyPow )
        str_vars = self.StrArds()
        if self.dim == 1: str_vars += ','
        print ('str_vars', str_vars, self.dim)

        variables = sy.symbols(str_vars)
        terms = []
        for degree in range(self.PolyPow + 1):
                for term in combinations_with_replacement(variables, degree):
                    #           print (list(term))
                    product = 1
                    for var in term:
                        product *= var
                    terms.append(str(product))
        for n in range(len(terms)):
                terms[n] = 'gr' + str(n) + '*' + terms[n]
            #        print (terms)
        smbF = ' + '.join(terms)
   #     print         (self.ArgNamesList())
    #    1/0
        self.FunStr = smbF
        print('smbF', smbF)
        self.PolinoF = Polyno(self.FunStr, "gr", self.ArgNamesList() )
  #      1/0
        smbFx = str(sy.diff(self.FunStr, variables[0])) + ' ' # for  last gr7 ->gr[7]
        print('smbFx', smbFx)
        self.PolinoFx = Polyno( smbFx, "gr", self.ArgNamesList() )

        smbFxx = str(sy.diff(smbFx, variables[0])) + ' '  # for  last gr7 ->gr[7]
        print('smbFxx', smbFxx)
        self.PolinoFxx = Polyno( smbFxx, "gr", self.ArgNamesList() )

        self.PolinoFy = None
        self.PolinoFxy = None
        self.PolinoFyy = None
        if self.dim == 2 :
            smbFy = str(sy.diff(self.FunStr, variables[1])) + ' '  # for  last gr7 ->gr[7]
            print('smbFy', smbFy)
            self.PolinoFy = Polyno( smbFy, "gr", self.ArgNamesList() )

            smbFxy = str(sy.diff(smbFx, variables[1])) + ' '  # for  last gr7 ->gr[7]
            print('smbFxy', smbFxy)
            self.PolinoFxy = Polyno( smbFxy, "gr", self.ArgNamesList() )

            smbFyy = str(sy.diff(smbFy, variables[1])) + ' '  # for  last gr7 ->gr[7]
            print('smbFyy', smbFyy)
            self.PolinoFyy = Polyno( smbFyy, "gr", self.ArgNamesList() )

    #        1/0

    def calcNDTparam(self) :
        if self.dim == 0: return
        A0 = self.A[0]
        domain = self.domain
        if self.dim == 1:
          if domain is None :
            self.Nxx = A0.Ub+1
          else :
            self.Nxx = sum ( domain[x] for x in A0.mNodSm )
        elif self.dim == 2:
          A1 = self.A[1]
          if domain is None :
              self.Nxx = (A0.Ub+1)*(A1.Ub+1)
              self.Nyy = (A0.Ub+1)*(A1.Ub+1)
              self.Nxy = (A0.Ub+1)*(A1.Ub+1)
          else :
            self.Nxx = sum (  domain[x,y]  for y in A1.NodS   for x in A0.NodS )
            self.Nyy = self.Nxx
            self.Nxy = self.Nxx

    def dF_dX (self, *xy ) :                                #   real args
        x = ( xy[0] - self.A[0].min) / self.A[0].ma_mi
        if len (xy) == 1:
            return  self.derivX([x]) / self.A[0].ma_mi
        else :
            y = (xy[1] - self.A[1].min) / self.A[1].ma_mi           #  test it !
            return  self.derivX([x,y]) / self.A[0].ma_mi

    def derivX (self, xy ) :
  #      if SvF.Use_var:    return self.smbFx(self.var, xy)
   #     else:              return self.smbFx(self.grd, xy)
        if SvF.Use_var:    return self.PolinoFx.Calc(self.var, xy)
        else:              return self.PolinoFx.Calc(self.grd, xy)

    def derivY   (self, xy ) :
 #       if SvF.Use_var:    return self.smbFy(self.var, xy)
  #      else:              return self.smbFy(self.grd, xy)
        if SvF.Use_var:    return self.PolinoFy.Calc(self.var, xy)
        else:              return self.PolinoFy.Calc(self.grd, xy)

    def derivXX (self, xy ) :
#        print(xy, self.PolinoFxx.Calc(self.grd, xy))

        if SvF.Use_var :     return self.PolinoFxx.Calc(self.var, xy)
        else :               return self.PolinoFxx.Calc(self.grd, xy)
  #    if SvF.Use_var :     return self.smbFxx(self.var, xy)
   #   else :               return self.smbFxx(self.grd, xy)

    def derivYY (self, xy ) :
#      if SvF.Use_var:      return self.smbFyy(self.var, [x,y])
 #     else :               return self.smbFyy(self.grd, [x, y])
      if SvF.Use_var :     return self.PolinoFyy.Calc(self.var, xy)
      else :               return self.PolinoFyy.Calc(self.grd, xy)

    def derivXY (self, xy ) :
  #    if SvF.Use_var:      return self.smbFxy(self.var, [x, y])
   #   else :               return self.smbFxy(self.grd, [x, y])
      if SvF.Use_var :     return self.PolinoFxy.Calc(self.var, xy)
      else :               return self.PolinoFxy.Calc(self.grd, xy)

    def NormStep_ma_mi (self, xy):
        ret = []
        for na in range (self.dim) : ret.append (xy[na] * self.A[na].step / self.A[na].ma_mi)
        return ret

    def INTx(self):
        if self.dim == 1:
            return sum(self.fneNDT(x) * self.f_gap(x) *
   #                    (self.derivX([x * self.A[0].step / self.A[0].ma_mi])) ** 2
                       (self.derivX(self.NormStep_ma_mi([x]))) ** 2
                       for x in self.A[0].NodS) / self.Nxx
        else:
            return sum(self.fneNDT(x, y) * self.gap[x, y] *
  #                     (self.derivX([x * self.A[0].step / self.A[0].ma_mi, y * self.A[1].step / self.A[1].ma_mi])) ** 2
                       (self.derivX(self.NormStep_ma_mi([x, y]))) ** 2
                       for y in self.A[1].NodS for x in self.A[0].NodS) / self.Nxx
    def INTy(self):
            return sum(self.fneNDT(x,y) * self.gap[x, y] *
#                       (self.derivY([x * self.A[0].step / self.A[0].ma_mi, y * self.A[1].step / self.A[1].ma_mi])) ** 2
                       (self.derivY(self.NormStep_ma_mi([x, y]))) ** 2
                       for y in self.A[1].NodS for x in self.A[0].NodS) / self.Nyy

    def INTxx ( self ) :
        if self.dim == 1 :
            #                   ( self.derivXX ( [x*self.A[0].step/self.A[0].ma_mi] ) )**2
            return  sum (  self.fneNDT(x) * self.f_gap(x) *
                          ( self.derivXX(self.NormStep_ma_mi([x]) ) ) ** 2
                        for x in self.A[0].NodS )  /self.Nxx
##!!                        for x in self.A[0].NodS ) 
        else:
            return  sum (  self.fneNDT(x,y) * self.f_gap(x,y) *
             #        ( self.derivXX ( [x*self.A[0].step/self.A[0].ma_mi, y*self.A[1].step/self.A[1].ma_mi] ) )**2
                           (self.derivXX(self.NormStep_ma_mi([x,y]))) ** 2
                    for y in self.A[1].NodS    for x in self.A[0].NodS )  /self.Nxx
    def INTyy ( self ) :
        return  sum (  self.fneNDT(x,y) * self.f_gap(x,y) *
                       (self.derivYY(self.NormStep_ma_mi([x, y]))) ** 2
 #                      ( self.derivYY ( [x*self.A[0].step/self.A[0].ma_mi, y*self.A[1].step/self.A[1].ma_mi] ) )**2
#                     ( self.derivYY ( x, y ) )**2  
                    for y in self.A[1].NodS    for x in self.A[0].NodS ) /self.Nyy
    def INTxy ( self ) :
        return  sum (  self.fneNDT(x,y) * self.f_gap(x,y) *
                       (self.derivXY(self.NormStep_ma_mi([x, y]))) ** 2
   #                   ( self.derivXY ( [x*self.A[0].step/self.A[0].ma_mi, y*self.A[1].step/self.A[1].ma_mi] ) )**2
#                     ( self.derivXY ( x, y ) )**2  
                    for y in self.A[1].NodS    for x in self.A[0].NodS ) /self.Nxy

    def Ftbl ( self, n ) :
        if  not SvF.Use_var: gr = self.grd
        else               : gr = self.var            # 30
        Args = []
        for a in range (self.dim) : Args.append ( (self.A[a].dat[n]-self.A[a].min) / self.A[a].ma_mi )
        return self.PolinoF.Calc(gr, Args)
#        return self.smbF(gr, Args)

    def ArgsNorm_ma_mi ( self, ArS_real ) :    # нормализация аргументов
        Args = []
        for a in range (self.dim) : Args.append ((ArS_real[a]-self.A[a].min)/self.A[a].ma_mi)
        return Args

    def F ( self, ArS_real ) :  # не проверенно    real args
        x = self.ArgsNorm_ma_mi( ArS_real)
 #       print('ФТ', self.ArgsNorm_ma_mi([0.5]), self.V.avr)
        if self.param or not SvF.Use_var:  return self.PolinoF.Calc(self.grd, x) + self.V.avr    # gr = self.grd
        else :                             return self.PolinoF.Calc(self.var, x) + self.V.avr    #gr = self.var

    def var_to_grd (self) :
        if self.var is None:  return
        if self.param : return
        for i in range ( self.sizeP ) :  self.grd[i] = self.var[i].value

    def grd_to_var (self) :
        if self.var is None:  return
        if self.param : return
        for i in range ( self.sizeP ) :  self.var[i].value = self.grd[i]


