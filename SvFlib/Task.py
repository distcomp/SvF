# -*- coding: cp1251 -*-
from __future__ import division

from Object import *
#from  numpy import *
from  pyomo.environ import *
#from pyomo.opt import SolverFactory

#from PyomoEverestEnv import *
##from InData    import *
from Polynome  import * 
from MakeModel import *

from Lego_pFun  import *
from Lego_smbFun  import *
from Lego_SPWLFun import *
from Lego_CycleFun import *

#import Lego
from Pars  import *
from Draw  import *

#import copy
from copy   import *
from shutil import move

def Var_to_Grd():
    for f in SvF.Task.Funs:
        if not f.param:
            f.var_to_grd()

def Grd_to_Var():
    for f in SvF.Task.Funs:
        if not f.param:
            f.grd_to_var()

def FillNaNAll () :
        for f in SvF.Task.Funs:
            if not f.param:
                f.FillNaN ()


class TaskClass :
    def __init__ (self, Name='') :
        self.Mng = None
        self.Name = Name
        self.Gr      = ''
        self.Sets    = []
        self.Funs    = []
        self.Tbls    = []
        self.Objects = []
#        self.Sets    = SvF.Sets
 #       self.Funs    = SvF.Funs     #  Проблеммы с Funs  м.б. в Pyoma
  #      self.Tbls    = SvF.Tbls
   #     self.Objects = SvF.Objects
        self.createGr  = None
        self.Delta     = None
        self.DeltaVal  = None
        self.defMSD    = None
        self.defMSDVal = None
        self.print_res = None
        self.OBJ_U     = None

    #    Table('', 'SvF.curentTabl')


    def ReadSols (self, ext = '' ) : #, printL = 0 ) :
        for f in self.Funs :
            if f.param : continue
            if ext == ''       :  f_n = ''
            elif f.type == 'p' :  f_n = f.nameFun() + '.p' + ext
            else               :  f_n = f.nameFun() + ext
            if f.ReadSol(f_n ) == False :
              if f.type != 'tensor' :
                f.InitByData ()
        return

    def SaveSols (self, ext = '' ) : #, printL = 0 ) :
        for f in self.Funs :
            if f.param : continue
            print ("E", ext)
            if ext == ''       :  f_n = ''
            elif f.type == 'p' :  f_n = f.nameFun() + '.p' + ext
            else               :  f_n = f.nameFun() + ext
            f.SaveSol(f_n )#, printL)
        return

    def RenameSols (self, old, new ) :
        for f in self.Funs :
            if f.param : continue
            fName = f.nameFun()
            move( fName+old, fName+new )
#            if f.maxP != -1 :
            if f.type == 'p' :
                move( fName+".p"+old, fName+".p"+new )
        return

    def Draw (self, param ) :
        if SvF.Compile:  return
        if len(param) == 0:
            for f in self.Funs:
                if f.type == 'tensor' : continue
                if f.dim > 0: DrawComb(f.name)
        else:
            DrawComb(param)
        return

    def DrawVar ( self ) :
        if SvF.Compile:  return

        for f in self.Funs:
                if f.dim > 0 and f.param == False: DrawComb(f.V.name)

    def DrawErr (self ) :
        if SvF.Compile:  return

        for f in self.Funs:
                if f.dim > 0 and f.param == False and \
                    not ((f.A[0].dat is None) or (f.V.dat is None)):
                       DrawComb(f.V.name+';DrawErr')
