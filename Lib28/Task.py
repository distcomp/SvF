# -*- coding: cp1251 -*-
from __future__ import division
from  numpy import *
from  pyomo.environ import *
#from pyomo.opt import SolverFactory

#from PyomoEverestEnv import *
##from InData    import *
from Polynome  import * 
from MakeModel import * 
#from Lego     import *
import Lego
from Pars  import *
from Draw  import *

#import copy
from copy   import *
from shutil import move

import COMMON as co




class TaskClass :
    def __init__ (self, Name='') :
        self.Mng = None
        self.Name = Name
        self.Gr    = ''
        self.Grids = []
        self.Funs  = []
        self.Def   = []
        self.Tbls  = []
        self.Objects  = []
        self.createGr  = None
        self.Delta     = None
        self.DeltaVal  = None
        self.defMSD    = None
        self.defMSDVal = None
        self.print_res = None
        self.OBJ_U     = None


    def AddTbl(self, tbl) :
                self.Tbls.append ( tbl )

    def KillTbl(self, name) :
                ind = self.getTblNum (name) 
                if ind >= 0 : del  self.Tbls[ind]

    def getTblNum (self, name) :
        for tn, to in enumerate (self.Tbls) :
 #           print (to.name, name)
            if to.name == name:  return tn
        return -1

    def getTbl (self, name) :
        for t in self.Tbls:
            if t.name == name:
                return t
        return None

    def getTblFieldNums (self, name_col) :
        p = name_col.split('.')
        tb_num = self.getTblNum ( p[0] )
        if tb_num == -1 :  return -1,-1
        fld_num = self.Tbls[tb_num].getFieldNum ( p[1] )
        return tb_num,fld_num

    def getTbl_tbl (self, name_col) :
        tb_num, fld_num = self.getTblFieldNums (name_col)
        if tb_num == -1 or fld_num == -1 : return None
        return self.Tbls[tb_num].Flds[fld_num].tb
    
#        p = name_col.split('.')
 #       name = p[0]
  #      col  = p[1]
   #     for to in self.Tbls:
    #        if to.name == name:
     #           for fld in to.Flds  :
      #              if fld.name == col : return fld.tb
       # return None


    def AddDef(self, name, defList) :
            self.Def.insert(0,[name, defList])

    def getDefNum (self, name) :
        for nd in range(len(self.Def)) :
#            if self.Def[nd][0] == name.upper():  return nd
            if self.Def[nd][0] == name:  return nd
        return -1

    def getDef (self, name) :
        for nd in self.Def:
#            if nd[0] == name.upper():
            if nd[0] == name:
                return nd[1][:]
        return []

    def AddGrid(self, gri) :
                self.Grids.append ( gri )

    def getGridNum (self, gri) :
        if gri[0] == ' ' : gri = gri[1:]
        for nu in range(len(self.Grids)) :
            if self.Grids[nu].name == gri:  return nu
        return -1


    def getGrid (self, name) :
        for ng in self.Grids:
#            ng.Gprint()
            if ng.name == name:
                return deepcopy(ng)
        return None

    def substitudeDef (self, st) :
####        st = name
        for nd in self.Def :
            if len (nd[1]) == 1:
                st = SubstitudeName ( st, nd[0], str(nd[1][0]) )
####            st = st.replace(nd[0],str(nd[1][0]))
        for ng in self.Grids:
            if ng.className != 'Grid' : continue
            st = SubstitudeName ( st, ng.name+'.max',  str(ng.max)  )
            st = SubstitudeName ( st, ng.name+'.min',  str(ng.min)  ) 
            st = SubstitudeName ( st, ng.name+'.step', str(ng.step) ) 
            st = SubstitudeName ( st, ng.name+'.Up',   str(int(ng.Ub)) ) 
        return st


    def AddFun ( self, fun ):
            if fun.V == 0 : return            # FuncR - empty
            self.Funs.append ( fun )
            addObject(fun.V.name, 'Fun', fun)

    def InitializeAddFun(self, fun, ini=None):
            if fun.V == 0: return
            fun = fun.Initialize( ini )
        #    s=fun.A[0].name
            self.Funs.append(fun)
            addObject(fun.V.name, 'Fun', fun)

            #   s1=self.Funs[-1].A[0].name
            if co.printL: print ('InitializeAdd',); self.Funs[-1].myprint()

#    def FixAllFun (self) :
 #       for f in self.Funs :   f.Fix()

    def getFunNum (self, name) :
        if name[0] == ' ' : name = name[1:]
        for nu in range(len(self.Funs)) :
            if self.Funs[nu].V.name == name:  return nu
        return -1

    def getFun (self, name) :
        if name[0] == ' ' : name = name[1:]
        for f in self.Funs :
#            print f.V.name, name
            if f.V.name == name:  return f
        return None

    def ReadSols (self, ext = '' ) : #, printL = 0 ) :
        for f in self.Funs :
            if f.param : continue
#            if ext == '' : f_n = ''
 #           else :         f_n = f.nameFun() + ext
            if ext == ''       :  f_n = ''
            elif f.type == 'p' :  f_n = f.nameFun() + '.p' + ext
            else               :  f_n = f.nameFun() + ext
            f.ReadSol(f_n ) #, printL)
        return

    def SaveSols (self, ext = '' ) : #, printL = 0 ) :
        for f in self.Funs :
            if f.param : continue
            if ext == ''       :  f_n = ''
            elif f.type == 'p' :  f_n = f.nameFun() + '.p' + ext
            else               :  f_n = f.nameFun() + ext
#            else :         f_n = f.nameFun() + ext
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
        if co.Preproc:  return
        if len(param) == 0:
            for f in self.Funs:
                if f.dim > 0: DrawComb(f.V.name)
        else:
            DrawComb(param)
        return

    def DrawVar ( self ) :
        if co.Preproc:  return
        for f in self.Funs:
                if f.dim > 0 and f.param == False: DrawComb(f.V.name)

    def DrawErr (self ) :
        if co.Preproc:  return
        for f in self.Funs:
                if f.dim > 0 and f.param == False and \
                    not ((f.A[0].dat is None) or (f.V.dat is None)):
                       DrawComb(f.V.name+';DrawErr')
