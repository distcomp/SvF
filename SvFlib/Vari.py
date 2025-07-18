# -*- coding: cp1251 -*-
from   copy   import *
from Object import *


class Vari ():                  #  var  ###################################
  def __init__ (self, name, fld_name = '') :
      from Table import getCurrentFieldData
#      Object.__init__ ( self, name, 'Vari')
      self.name  = name
      self.oname = name
      self.axe_name = ''
      self.leg_name = ''
      self.title_name = ''
      self.draw_name = name
      self.data_name = name + '-data'
      if fld_name == '' :   self.fld_name = name
      else :                self.fld_name = fld_name
      self.avr     = 0          #  ��� ���������
      self.sigma   = 1
      self.sigma2  = 1
      self.average = 0
#      self.Lbound  = None # min
#      self.Ubound  = None
      if SvF.Compile: return  ##############################################################
      self.dat     = getCurrentFieldData (self.fld_name)


 # def Oprint(self) :
  #    print ('Oprint', self.Otype, self.name, "avr", self.avr, "sig", self.sigma)

  def Normalization (self, VarNormalization) :    ####  �� dat ��������  self.avr
        if self.dat is None :  return
        NoR = 0
        self.average = 0
        for m in self.dat:
            if  not np.isnan(m):
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
                if  not np.isnan(m):
                    self.sigma2 += (m-self.average)**2
            self.sigma2 =  self.sigma2 / (NoR-1) 
        self.sigma = np.sqrt ( self.sigma2 )

        if VarNormalization :  ########################################== 'Y' :
            self.avr = self.average
            for m in self.dat :
               if not np.isnan(m):  m -= self.avr
        else :
            self.avr = 0

