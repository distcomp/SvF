# -*- coding: UTF-8 -*-


from Lego import *

#########################################################################
# POLY            ********************************************************
class pFun (Fun) :                                
    def __init__ (self, Vname='',  As=[], param=False, PolyPow=-1, Finitialize = 0, DataReadFrom = '' ) :
#    def __init__ (self, FuncR ) :
        Fun.__init__(self, Vname, As, param, PolyPow, Finitialize, DataReadFrom)
#        self.CopyFromFun ( FuncR, FuncR.param,  'p' )   # 27
 #       del SvF.Task.Funs[-1]
  #      Object.__init__(self, self.V.name, 'Fun')
   #     self.sizeP = PolySize ( self.dim, self.PolyPow )
        print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS', self.sizeP)

        if SvF.Compile : return

        self.grd   = zeros ( self.sizeP )
        self.PolyR = range ( self.sizeP )
        self.pow   = CrePolyPow ( self.dim, self.PolyPow )

        self.Dx, self.Cx = CreDeriv1Pow ( self.pow, [], 0 )
        if self.dim > 1 :
            self.Dy, self.Cy = CreDeriv1Pow(self.pow, [], 1)

        self.Dxx, self.Cxx = CreDeriv2Pow(self.pow, 0, 0)
        if self.dim > 1 :
            self.Dyy, self.Cyy = CreDeriv2Pow ( self.pow, 1, 1 )
            self.Dxy, self.Cxy = CreDeriv2Pow ( self.pow, 0, 1 )


    def dF_dX (self, *xy ) :                                #   real args
        x = ( xy[0] - self.A[0].min) / self.A[0].ma_mi
        if len (xy) == 1:
            return  self.derivX(x) / self.A[0].ma_mi
        else :
            y = (xy[1] - self.A[1].min) / self.A[1].ma_mi           #  test it !
            return  self.derivX(x,y) / self.A[0].ma_mi


#    def derivXd1 (self, *xy ) :
    def derivX (self, *xy ) :
#        print (len(xy), self.Cx, self.Dx)
        if SvF.Use_var : gr = self.var
        else          : gr = self.grd
        x = xy[0]
        if len (xy) == 1:
            return  sum (  self.Cx[i] * gr[i] * x**self.Dx[i][0]     for i in self.PolyR )
        else :
            y = xy[1]
            return  sum (  self.Cx[i] * gr[i] * x**self.Dx[i][0]
                                              * y**self.Dx[i][1]     for i in self.PolyR )
#    def derivX   (self, x, y ) :
#        return  sum (  self.Cx[i] * self.var[i] * x**self.Dx[i][0]
#                                                * y**self.Dx[i][1]     for i in self.PolyR )
    def derivY   (self, x, y ) :
        return  sum (  self.Cy[i] * self.var[i] * x**self.Dy[i][0]
                                                * y**self.Dy[i][1]     for i in self.PolyR )

    def derivXXd1 (self, x ) :
        if SvF.Use_var :
            ret = sum (  self.Cxx[i] * self.var[i] * x**self.Dxx[i][0]   for i in self.PolyR )
 #           print ('var', ret)
#            return  sum (  self.Cxx[i] * self.var[i] * x**self.Dxx[i][0]   for i in self.PolyR )
        else :
            ret =  sum (  self.Cxx[i] * self.grd[i] * x**self.Dxx[i][0]   for i in self.PolyR )
#            print ('grd', ret)
#            return  sum (  self.Cxx[i] * self.grd[i] * x**self.Dxx[i][0]   for i in self.PolyR )
        return ret

    def derivXX (self, x, y ) :
#      print ('derivXX', SvF.Use_var, sum ( self.Cxx[i] * self.grd[i] * x**self.Dxx[i][0] * y**self.Dxx[i][1] for i in self.PolyR ))
      if SvF.Use_var :
        return  sum ( self.Cxx[i] * self.var[i] * x**self.Dxx[i][0] * y**self.Dxx[i][1] for i in self.PolyR )
      else :
        return  sum ( self.Cxx[i] * self.grd[i] * x**self.Dxx[i][0] * y**self.Dxx[i][1] for i in self.PolyR )

    def derivYY (self, x, y ) :
      if SvF.Use_var:
        return sum (  self.Cyy[i] * self.var[i] * x**self.Dyy[i][0] * y**self.Dyy[i][1] for i in self.PolyR )
      else :
        return sum (  self.Cyy[i] * self.grd[i] * x**self.Dyy[i][0] * y**self.Dyy[i][1] for i in self.PolyR )

    def derivXY (self, x, y ) :
      if SvF.Use_var:
        return sum (  self.Cxy[i] * self.var[i] * x**self.Dxy[i][0] * y**self.Dxy[i][1]    for i in self.PolyR )
      else :
        return sum (  self.Cxy[i] * self.grd[i] * x**self.Dxy[i][0] * y**self.Dxy[i][1]    for i in self.PolyR )


    def sumX(self):
        if self.dim == 1:
            return sum(self.fneNDT(x) * self.f_gap(x) *
                       (self.derivX(x * self.A[0].step / self.A[0].ma_mi)) ** 2
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
        if  not SvF.Use_var: gr = self.grd
        else               : gr = self.var            # 30
        x = self.A[0].dat[n]/self.A[0].ma_mi
        if self.dim == 1 :
            return sum ( gr[i] * x**self.pow[i][0] for i in self.PolyR )
        else :            
#            y = self.tbl[n,self.A[1].num]/self.A[1].step
            y = self.A[1].dat[n]/self.A[1].ma_mi
            return sum ( gr[i] * x**self.pow[i][0] * y**self.pow[i][1] for i in self.PolyR )
        
        
    def F ( self, ArS_real ) :  # не проверенно    real args
        if SvF.Use_var : gr = self.var
        else          : gr = self.grd
        x = (ArS_real[0]-self.A[0].min)/self.A[0].ma_mi
        if self.dim == 1 :
            return sum ( gr[i] * x**self.pow[i][0]     # 29
                       for i in self.PolyR )  + self.V.avr
        else :
            y = (ArS_real[1]-self.A[1].min)/self.A[1].ma_mi
            return sum ( gr[i] * x**self.pow[i][0] * y**self.pow[i][1]
                        for i in self.PolyR )  + self.V.avr

