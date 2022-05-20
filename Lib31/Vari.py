# -*- coding: cp1251 -*-

from Object import *

#class Vari (Object):                  #  var  ###################################
class Vari ():                  #  var  ###################################
  def __init__ (self, name) :
#      Object.__init__ ( self, name, 'Vari')
      self.name  = name
      self.oname = name
      self.draw_name = name
      self.avr     = 0          #  для вычитания
      self.sigma   = 1
      self.sigma2  = 1
      self.average = 0
#      self.Lbound  = None # min
#      self.Ubound  = None
      self.dat     = None



 # def Oprint(self) :
  #    print ('Oprint', self.Otype, self.name, "avr", self.avr, "sig", self.sigma)

  def Normalization (self, VarNormalization) :    ####  из dat вычитаем  self.avr
        if self.dat is None :  return
        NoR = 0
        self.average = 0
        for m in self.dat:
            if  not isnan(m):
                self.average += m
                NoR += 1
        if NoR ==0:
            self.dat = None
            return
        self.average = self.average / NoR

        if NoR ==1 :
            self.sigma2 = 1
        else :
            self.sigma2 = 0
            for m in self.dat:
                if  not isnan(m):
                    self.sigma2 += (m-self.average)**2
            self.sigma2 =  self.sigma2 / (NoR-1) 
        self.sigma = sqrt ( self.sigma2 )

        if VarNormalization :  ########################################== 'Y' :
            self.avr = self.average
            for m in self.dat :
               if not isnan(m):  m -= self.avr
        else :
            self.avr = 0

