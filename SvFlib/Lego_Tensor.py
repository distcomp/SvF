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


##### ********************************************************** #######
class Tensor (Object) :
    def __init__ (self, name, Sizes = None, Finitialize = 1, param=False, ReadFrom='') :
        Object.__init__(self, name, 'Fun')
        self.name = name
        self.grd = None
        self.var = None
        self.param = param
        self.type = 'tensor'
        self.A = []             #  Arg     25.01   ???
        self.Finitialize = Finitialize
        if Sizes is None : return
        self.dim = len(Sizes)
        self.Allocate_tensor(Sizes)
    #    self.gr  = self.grd                 # 25.10
        self.ReadFrom = ReadFrom
        if ReadFrom != '':
            if self.ReadSol(ReadFrom) == False : exit (-1)
        self.gr = self.grd  # 25.10


    def Allocate_tensor(self, Sizes) :
        self.Sizes = Sizes
        dim = len (Sizes)
        if dim == 0:
                self.grd = self.Finitialize
        elif dim == 1:
                self.grd = np.ones((Sizes[0]), np.float64)
                self.grd[:] = self.Finitialize                     #  by default = 1
        elif dim == 2:
                self.grd = np.ones((Sizes[0],Sizes[1]), np.float64)
                self.grd[:,:] = self.Finitialize                     #  by default = 1
        elif dim == 3:
                self.grd = np.ones((Sizes[0],Sizes[1],Sizes[2]), np.float64)
                self.grd[:,:,:] = self.Finitialize                     #  by default = 1

    def set_gr_grd_or_var(self):
        if SvF.Use_var == True and self.param != True:
            self.gr = self.var
        else :
            self.gr = self.grd

    def F ( self, ij ) :
          if self.dim == 0:                           #  31
                return self.gr
#                if SvF.Use_var: return self.var
 #               else          : return self.grd
          elif self.dim == 1:
                return self.gr[ij[0]]
  #              if SvF.Use_var: return self.var[ij[0]]
   #             else          : return self.grd[ij[0]]

    def nameFun(self):
            name = self.name
#            name = self.V.name
            if len(self.A) > 0:
                name += '('
                for ar in self.A:
                    if type(ar) == type('abc'):  name += ar + ','
                    else:                        name += ar.name + ','
                name = name[0:-1]  # -1 убрать запятую
                name += ')'
            return name


    def ReadSol(self, fName='', printL=0):
        from ModelFiles import to_logOut
        if fName == '':  fName = SvF.Prefix + self.name + ".sol"
        fi, Etc, Ver, Type = Get_File_Etc_Ver_Type (fName)
#        print ('FFFFFFFFFFFFFFFFFFfi', Etc, Ver, Type)
        if fi is None : return False
        print("ReadSol from", fName) #, head)
        dat = np.loadtxt(fi, 'double')
        if self.dim == 0:
            self.grd = float(dat)
        elif self.dim == 1:
#            print(Etc)            #  ['cl[1]']
            if Type == 'tensor' and Etc[0].split('[')[1].split(']')[0] =='1': dat_size = 1 #  ['cl[1]']
            else : dat_size = dat.shape[0]
            for i in range(max(dat_size, self.Sizes[0])):
                    if dat_size == 1 : da = dat
                    elif i < dat_size:   da = dat[i]
                    else :
                        da = self.grd[i-1] * 0.1
                        to_logOut(str(da)+' was added while reading fName #' + str(i))
                    if i >= self.Sizes[0] :
                        to_logOut(str(dat[i])+' was ammited while reading fName #' + str(i))
                        continue
                    self.grd[i] = da  # !  gr  !
 #             print (self.grd)
  #            1/0
        elif self.dim == 2:
            print ("Not Ready Yet")  #############################
        fi.close()
        return True

    def File_SaveSol(self, ext='.sol', fName=''):      #  25.07
#            print('Before SaveSol to ', fName, self.type)
            if fName == '':   fName = SvF.Prefix + self.nameFun() + ext
            try:
                fi = open(fName, "w")
            except IOError as e:
                print("Can''t open file: ", fName)
                return None, None
            return fi, fName


    def SaveSol(self, fName=''):  ## OLD
#            if SvF.printL > 0: print('Before SaveSol to ', fName, self.type)
 #           if fName == '':   fName = SvF.Prefix + self.nameFun() + ".sol"
  #          if SvF.printL > 0: print('SaveSol to ', fName, self.type)
   #         try:
    #            fi = open(fName, "w")
     #       except IOError as e:
      #          print("Can''t open file: ", fName)
       #         return
            fi, fName = self.File_SaveSol('.sol', fName)
            if not fi is None:
                if self.dim == 0:
                    fi.write(self.name + '\t#SvFver_70_tensor')
                    v = self.grdNaNreal()
                    fi.write( '\n' + str_val(v))
                elif self.dim == 1:
                    fi.write(self.name + '[' + str(self.Sizes[0]) + ']\t#SvFver_70_tensor')
                    for i in range (self.Sizes[0]) :
                        v = self.grdNaNreal(i)
                        fi.write( '\n' + str_val(v) )


    def FillNaN(self):
        if self.dim == 0: return

    def grdNaNreal (self, i=None,j=None,k=None) :
        if self.dim == 0 :
            return self.grd
        elif self.dim == 1 :
            return self.grd[i]

    """""
    def grd_to_var (self) :
        if self.var is None:  return
        if self.param : return
        if   self.dim == 0:
                self.var.value = self.grd
        elif self.dim == 1:
            for i in range (self.Sizes[0]) :
                self.var[i].value = self.grd[i]
    
    def var_to_grd (self) :
        if self.var is None:  return
        if self.param : return
#        print ('var_to_grd',self.type,self.dim)
        if   self.dim == 0:
            self.grd = self.var.value
        elif self.dim == 1:
            for i in range (self.Sizes[0]) :
                self.grd[i] = self.var[i].value
    """""

    def var_to_grd (self) :
            if self.var is None:  return
            if self.param : return
            if   self.dim == 0:   self.grd = self.var.value
            elif self.dim == 1:
                for i in range(self.Sizes[0]):  self.grd[i] = self.var[i].value
#                for i in self.A[0].NodS:  self.grd[i] = self.var[i].value
#                self.grd[:] = self.var[:].value
            elif self.dim == 2:
                for i in self.A[0].NodS:
                    for j in self.A[1].NodS:  self.grd[i,j] = self.var[i,j].value
            elif self.dim == 3:
                for i in self.A[0].NodS:
                    for j in self.A[1].NodS:
                        for k in self.A[2].NodS:
                            self.grd[i,j,k] = self.var[i,j,k].value

    def grd_to_var(self):
        if self.var is None:  return
        if self.param: return
        if self.dim == 0:
                self.var.value = self.grd
        elif self.dim == 1:
#                for i in self.A[0].NodS:
                for i in range(self.Sizes[0]):
                    #                    self.var[i].value = self.grd[i]
                    self.var[i].set_value(self.grd[i], skip_validation=True)
        elif self.dim == 2:
                for i in self.A[0].NodS:
                    #                    for j in self.A[1].NodS:  self.var[i,j].value = self.grd[i,j]
                    for j in self.A[1].NodS:  self.var[i, j].set_value(self.grd[i, j], skip_validation=True)

        elif self.dim == 3:
                for i in self.A[0].NodS:
                    for j in self.A[1].NodS:
                        for k in self.A[2].NodS:
                            #                            self.var[i,j,k].value = self.grd[i,j,k]
                            self.var[i, j, k].set_value(self.grd[i, j, k], skip_validation=True)


##### ********************************************************** #######

