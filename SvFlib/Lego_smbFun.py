# -*- coding: UTF-8 -*-

from Lego import *
import sympy as sy
from itertools import combinations_with_replacement

class smbFun (BaseFun) :
    def __init__ (self, Vname='',  As=[], param=False, Degree=-1,  Finitialize = 0, DataReadFrom = '',Data=[], Type='smbFun',
                          Domain = None, SymbolInteg=False, SymbolDiffer =False, Deriv1=False, ArgNorm =True) :
        BaseFun.__init__(self, Vname, As, param, Degree, Finitialize, DataReadFrom, Data, Type, Domain)

        if SvF.Compile : return    #  ???
#        self.FunStr = smbFun
        self.smbF   = None
#        self.smbFx  = None
 #       self.smbFy  = None
        self.smbFxx = None
        self.smbFyy = None
        self.smbFxy = None
        self.Int_smbFxx_2 = None
        self.Int_smbFyy_2 = None    #  not ready yet
        self.Int_smbFxy_2 = None    #  not ready yet
        self.SymbolInteg  = SymbolInteg
        self.SymbolDiffer = SymbolDiffer
        self.Deriv1 = Deriv1
        self.ArgNorm = ArgNorm
#        self.Deriv1_= [None for _ in range(self.dim)]
 #       self.Hessian = [[None for _ in range(self.dim)] for _ in range(self.dim)]
  #      self.IntegDer2 = [[None for _ in range(self.dim)] for _ in range(self.dim)]


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
              self.Nyy = self.Nxx
              self.Nxy = self.Nxx
          else :
            self.Nxx = sum (  domain[x,y]  for y in A1.NodS   for x in A0.NodS )
            self.Nyy = self.Nxx
            self.Nxy = self.Nxx


    def Real_to_Norm_or_Real ( self, ArS_real ) :    # реальные в [0,1]    нормализация аргументов
        if self.ArgNorm  :  return  [(ArS_real[i]-a.min)/a.ma_mi for i, a in enumerate(self.A)]
        else                    :  return ArS_real

#    def Node_to_Norm_or_Real (self, xy):
 #       if self.ArgNorm :  return  [xy[i]*a.step/a.ma_mi for i, a in enumerate(self.A)]
  #      else                   :  return  [a.Val[xy[i]] for i, a in enumerate(self.A)]

    def Node_to_Norm_or_Real (self, nodeArgs):
        #realArgs = self.Node_to_Real (nodeArgs)      
        #return self.Real_to_Norm_or_Real (realArgs)
        if self.ArgNorm :  return  [nodeArgs[i]*a.step / a.ma_mi   for i, a in enumerate(self.A)]
        else            :  return  [nodeArgs[i]*a.step + a.min     for i, a in enumerate(self.A)]
        

    """"
    def dF_dX (self, *xy ) :                                #   real args
        x = ( xy[0] - self.A[0].min) / self.A[0].ma_mi
        if len (xy) == 1:
            return  self.derivX([x]) / self.A[0].ma_mi
        else :
            y = (xy[1] - self.A[1].min) / self.A[1].ma_mi           #  test it !
            return  self.derivX([x,y]) / self.A[0].ma_mi

    def derivX (self, xy ) :
  #      if SvF.Use_var:    return self.txtFx(self.var, xy)
   #     else:              return self.txtFx(self.grd, xy)
        if SvF.Use_var:    return self.PolinoFx.Calc(self.var, xy)
        else:              return self.PolinoFx.Calc(self.grd, xy)

    def derivY   (self, xy ) :
 #       if SvF.Use_var:    return self.txtFy(self.var, xy)
  #      else:              return self.txtFy(self.grd, xy)
        if SvF.Use_var:    return self.PolinoFy.Calc(self.var, xy)
        else:              return self.PolinoFy.Calc(self.grd, xy)
    """
    def by_xx (self,x,y=None) :
        if self.SymbolDiffer :

            if y is None :
                print ("YTS")
                Args = [x,y]
                if self.ArgNorm:
                    Args = [(Args[i] - a.min) / a.ma_mi for i, a in enumerate(self.A)]
                    return self.Hessian[0][0](Args) / (self.A[0].ma_mi) ** 2
                else:
                    return self.Hessian[0][0](Args)

                ret = self.Hessian[0][0](self.Real_to_Norm_or_Real([x,y]))
                if self.ArgNorm :   ret /=  (self.A[0].ma_mi)**2
                return ret
          #      return self.Hessian[0][0](self.Node_to_Norm_or_Real([x,y]))  # [x, y]))

            #    return (self.F([x + self.A[0].step]) - 2 * self.F([x]) + self.F([x - self.A[0].step])) / (self.A[0].step ** 2)
            else:
                print('*******************************************************by_xx', x)
                return (self.F([x+self.A[0].step,y]) - 2*self.F([x,y]) + self.F([x-self.A[0].step,y]))/(self.A[0].step**2)
        else : return super().by_xx(x,y)

    def by_x (self,x) :
      #  print ("LLL", len(self.Deriv1_) )
        if self.Deriv1 :
            return self.Deriv1_([0][x])
        else: return super().by_x(x)

    def derivXX (self, xy ) :
   #     print (xy, self.smbFxx( xy ))
        return self.smbFxx( xy )
        #if SvF.Use_var :     return self.txtFxx(self.var, xy)
        #else :               return self.txtFxx(self.grd, xy)

    def derivYY (self, xy ) :
        return self.smbFyy(xy)
 #     if SvF.Use_var:      return self.smbFyy(self.var, xy)
  #    else :               return self.smbFyy(self.grd, xy)

    def derivXY (self, xy ) :
        return self.smbFxy(xy)
   #   if SvF.Use_var:      return self.smbFxy(self.var, xy)
    #  else :               return self.smbFxy(self.grd, xy)


    """"
    def INTx(self):
        if self.dim == 1:
            return sum(self.fneNDT(x) * self.f_gap(x) *
   #                    (self.derivX([x * self.A[0].step / self.A[0].ma_mi])) ** 2
                       (self.derivX(self.Node_to_Norm_or_Real([x]))) ** 2
                       for x in self.A[0].NodS) / self.Nxx   Nx?
        else:
            return sum(self.fneNDT(x, y) * self.gap[x, y] *
  #                     (self.derivX([x * self.A[0].step / self.A[0].ma_mi, y * self.A[1].step / self.A[1].ma_mi])) ** 2
                       (self.derivX(self.Node_to_Norm_or_Real([x, y]))) ** 2
                       for y in self.A[1].NodS for x in self.A[0].NodS) / self.Nxx
    def INTy(self):
            return sum(self.fneNDT(x,y) * self.gap[x, y] *
#                       (self.derivY([x * self.A[0].step / self.A[0].ma_mi, y * self.A[1].step / self.A[1].ma_mi])) ** 2
                       (self.derivY(self.Node_to_Norm_or_Real([x, y]))) ** 2
                       for y in self.A[1].NodS for x in self.A[0].NodS) / self.Nyy
    """

    def by_xy_node (self, by0, by1, arg_node ): #  Вторая РАЗНОСТЬ по by0, by1 d узле
        if self.ArgNorm:
            step = [a.step / a.ma_mi for a in self.A]

    def DERIV2(self, d0, d1, argxy):   # x, y):
            if self.SymbolDiffer:
                return self.Hessian[d0][d1](self.Node_to_Norm_or_Real(argxy)) #[x, y]))
            else:
                arg = np.array(self.Node_to_Norm_or_Real(argxy))  #[x, y]))    #  np.array    for + -
                if self.ArgNorm:   step = [a.step/a.ma_mi for a in self.A]
                else:              step = [a.step for a in self.A]

                if d0==0 and d1==0 :
                    if self.dim != 1:  step[1] = 0
                    return  ( self.smbF(arg-step) -2*self.smbF(arg) +self.smbF(arg+step) )/step[0]**2
                elif d0==1 and d1==1 :
                    step[0] = 0
                    return  ( self.smbF(arg-step) -2*self.smbF(arg) +self.smbF(arg+step) )/step[1]**2
                else:      #if d0==0 and d1==1 :
                    step1 = [step[0],-step[1]]
                    return  ( self.smbF(arg+step)+self.smbF(arg-step)-self.smbF(arg+step1)-self.smbF(arg-step1) ) \
                        / step[0] / step[1] * .25

    def INT2D ( self, d0, d1 ) :
            if  self.SymbolInteg:
                if self.ArgNorm:
                    arg_min = [0. for i in range(self.dim)]
                    arg_max = [1. for i in range(self.dim)]
                    return self.IntegDer2[d0][d1](arg_max) - self.IntegDer2[d0][d1](arg_min)
                else :
                    arg_min = [self.A[i].min for i in range(self.dim)]
                    arg_max = [self.A[i].max for i in range(self.dim)]
                    ret = (self.IntegDer2[d0][d1](arg_max) - self.IntegDer2[d0][d1](arg_min) ) \
                           * self.A[d0].ma_mi ** 2 * self.A[d1].ma_mi ** 2       #  произв **2  сжатие
                    for i in range(self.dim):  ret = ret / self.A[i].ma_mi        #  на объем
                    return ret
            else:                               #if self.SymbolDiffer True   and False
                ret = 0;  num = 0
                if self.dim == 1 :
                    for x in self.A[0].NodS:
                        if self.fneNDT(x) * self.f_gap(x) !=0:
                            num += 1
                            ret += self.DERIV2 ( d0,d1,[x] ) ** 2
                elif self.dim == 2:
                    for x in self.A[0].NodS :
                      for y in self.A[1].NodS :
                        if self.fneNDT(x,y) * self.f_gap(x,y) != 0:
                            num += 1
                            ret += self.DERIV2 ( d0,d1,[x, y] ) ** 2

                ret = ret / num
                if self.ArgNorm == False:
                    ret *= self.A[d0].ma_mi **2  * self.A[d1].ma_mi **2        #  сводим к [0,1]
                return ret
      #      else :

    def ComplDer2(self, bets):
        ret = 0
        for d0 in range(self.dim) :
            for d1 in range(d0, self.dim) :
                if d0 == d1 :
                    ret += bets[d0] ** 2 * bets[d1] ** 2 * self.INT2D(d0,d1)
                else :
                    ret += bets[d0] ** 2 * bets[d1] ** 2 * self.INT2D(d0,d1) * 2
        return ret


    def Ftbl ( self, n ) :
        Args = [a.dat[n] for a in self.A]
#        print (Args, self.Real_to_Norm_or_Real(Args))
        return self.smbF(self.Real_to_Norm_or_Real(Args))
     #   if not SvF.Use_var:  return self.txtF(self.grd, self.Real_to_Norm_or_Real( Args))
      ##  else:                return self.txtF(self.var, self.Real_to_Norm_or_Real( Args))



    def F ( self, ArS_real ) :  #   real args
#        print ('ArS_real', self.name,  ArS_real, self.Real_to_Norm_or_Real( ArS_real),
 #              self.smbF( self.Real_to_Norm_or_Real( ArS_real) ) + self.V.avr)
        return self.smbF( self.Real_to_Norm_or_Real( ArS_real) ) + self.V.avr    # gr = self.grd
    #    if self.param or not SvF.Use_var:  return self.txtF(self.grd, self.Real_to_Norm_or_Real( ArS_real)) + self.V.avr    # gr = self.grd
     #   else :                             return self.txtF(self.var, self.Real_to_Norm_or_Real( ArS_real)) + self.V.avr    #gr = self.var

    def Fijk ( self, ijk ) :  # i j k  args
        ArS_real = [ a.Val[ijk[ia]] for ia, a in enumerate (self.A) ]
        return self.smbF( self.Real_to_Norm_or_Real( ArS_real) ) + self.V.avr    # gr = self.grd
    #    if self.param or not SvF.Use_var:  return self.txtF(self.grd, self.Real_to_Norm_or_Real( ArS_real)) + self.V.avr    # gr = self.grd
     #   else :                             return self.txtF(self.var, self.Real_to_Norm_or_Real( ArS_real)) + self.V.avr    #gr = self.var

    def var_to_grd (self) :
            if self.dim == 1:
                for i in range(self.Sizes[0]):
                    self.grd[i] = self.Fijk ([i])
            elif self.dim == 2:
                for i in range(self.Sizes[0]):
                    for j in range(self.Sizes[1]):
                        self.grd[i,j] = self.Fijk ([i,j])

    def grd_to_var (self) :
        return
