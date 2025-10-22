# -*- coding: UTF-8 -*-
from Lego import *

class CycleFun (Fun) :
    def __init__(self, Vname='', As=[], param=False, Finitialize=0, DataReadFrom='', Data=[], Domain=None, ReadFrom='', Period=0):
        Fun.__init__( self, Vname, As, param, -1, Finitialize, DataReadFrom, Data, 'gCycle', Domain, ReadFrom)
        if SvF.Compile: return  # ???
        self.Period = Period / self.A[0].step
        if Period == 0: self.Period = self.A[0].Ub

#    def interpol(self, lev, X, Y=0, Z=0):  # X,Y,Z  в шагах
    def interpolNode(self, argNode, lev=1):  # argNode =[ X,Y,..]  в шагах
            X = argNode[0]        #  на всякий случай, Х меняется
#            X = copy(argNode[0])        #  на всякий случай, Х меняется
            if self.param or not SvF.Use_var:   gr = self.grd
            else:                               gr = self.var  # 29
            #       print ("Use", SvF.Use_var)
            if 1 :   #if lev == 1:
                while X < 0:            X += self.Period
                while X > self.Period:  X -= self.Period
#                while X < 0:  X += self.A[0].Ub  # +1
 #               while X > self.A[0].Ub:  X -= self.A[0].Ub

                Xi = ifloor(X)  # int(floor ( X ))
                if Xi < 0: Xi = 0
                if Xi == self.A[0].Ub: Xi = self.A[0].Ub - 1
                dX = X - Xi
                if abs(dX) < 1e-10:                     return gr[Xi]
                if abs(dX - 1) < 1e-10:                 return gr[Xi + 1]
                return gr[Xi] * (1 - dX) + gr[Xi + 1] * dX


    def grdCycle (self, x) :                                    #  Устарело
        if self.param or not SvF.Use_var:  gr = self.grd
        else:                              gr = self.var  # 29
        if x==-1             : return gr[self.A[0].Ub]
        if x==self.A[0].Ub+1 : return gr[0]
        return gr[x]

    def NDTCycle (self, x) :                                 #  Устарело
        if x==-1             : return self.fneNDT(self.A[0].Ub)
        if x==self.A[0].Ub+1 : return self.fneNDT(0)
        return self.fneNDT(x)

    def INTxxcycle(self):                                 #  Устарело
            if self.type[0] == 'g' :
                if self.dim == 1:
                    return sum(self.NDTCycle(x - 1) * self.NDTCycle(x) * self.NDTCycle(x + 1) * self.f_gap(x) *
                               (self.grdCycle(x - 1) - 2 * self.grdCycle(x) + self.grdCycle(x + 1)) ** 2
                               for x in self.A[0].NodS) / (self.Nxx+2) / (1. / self.A[0].Ub) ** 4
            print ("INTxx:  No cycle")
            exit (-1)

    def ComplCycle ( self, bets ) :                                 #  Устарело
            return    bets[0]**4 * self.INTxxcycle ( )


    def grdCyc0E (self, x) :
        if self.param or not SvF.Use_var:  gr = self.grd
        else:                              gr = self.var  # 29
        if x==self.A[0].Ub+1 : return gr[1]
        if x==-1             : return gr[self.A[0].Ub]  #  не нужно
        return gr[x]

    def NDTCyc0E (self, x) :
        if x==self.A[0].Ub+1 : return self.fneNDT(1)
        if x==-1             : return self.fneNDT(self.A[0].Ub)   #  не нужно
        return self.fneNDT(x)

    def INTxxcyc0E(self):
            if self.type[0] == 'g':
                if self.dim == 1:
                    return sum(self.NDTCyc0E(x - 1) * self.NDTCyc0E(x) * self.NDTCyc0E(x + 1) * self.f_gap(x) *
                               (self.grdCyc0E(x - 1) - 2 * self.grdCyc0E(x) + self.grdCyc0E(x + 1)) ** 2
                               for x in self.A[0].mNodS) / (self.Nxx+1) / (1. / self.A[0].Ub) ** 4
            print ("INTxx:  No cycle")
            exit (-1)


    def ComplCyc0E ( self, bets ) :                 #28    первая точка должна быть равна последней
            return    bets[0]**4 * self.INTxxcyc0E ( )

    def Complexity ( self, bets ) :
            return self.ComplCyc0E ( bets )

    def Compl ( self, bets ) :
            return self.ComplCyc0E ( bets )


