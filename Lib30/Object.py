# -*- coding: cp1251 -*-
from __future__ import division

import COMMON as SvF            #   общий импорт
from  numpy import *            #    -- / ---

class Object :
    def __init__ ( self, name='', Otype='NoType' ): #, object=None) :   #
        self.name = name
        self.Otype = Otype
        if self.name != '' :  self.Add()

    def Add (self):
        SvF.Task.Objects.insert( 0, self )
#        print ('OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO', self.name, self.Otype )
        if   self.Otype == 'Fun'   :  SvF.Task.Funs.append ( self )
        elif self.Otype == 'Table' :  SvF.Task.Tbls.insert (0, self )
        elif self.Otype == 'Grid'  :  SvF.Task.Grids.append ( self )
#        elif self.Otype == 'Grid'  :  SvF.Task.Grids.insert (0, self )

    def Oprint (self):
        print ( self.Otype, self.name )

def addObject(object):
    object.Add()

def getObject(name):
    for o in SvF.Task.Objects :
#        o.Oprint()
        if o.name == name: return o
    return None

def getObjectNotGrid(name):
    for o in SvF.Task.Objects :
        if o.Otype == 'Grid' : continue
#        print ('getObjectNotGrid', o.name, name)
        o.Oprint()
        if o.name == name: return o
    return None
##################################################################            Grid
def findGridByName(grids, name):   #  ищем в    grids  !!
        for g in grids:
            #            print 'G', g.name, name, g.step
            if g.name == name:
                SvF.LastGrid = g
                return g
        return None

def getGridNum (gri) :
        if gri[0] == ' ' : gri = gri[1:]
        for nu, gr in enumerate (SvF.Task.Grids) :
            if gr.name == gri:  return nu
        return -1
##################################################################            Fun
def getFunNum (name) :
        if name[0] == ' ' : name = name[1:]
        for nu in reversed( range(len(SvF.Task.Funs)) ) :
            if SvF.Task.Funs[nu].V.name == name:  return nu
        return -1

def getFun (name) :
        if name[0] == ' ' : name = name[1:]
        for f in reversed ( SvF.Task.Funs ):  ## 30
 #           print (f.name, f.V.name, name, f.type)
            if f.name == name:  return f
        return None

        ##################################################################            Table


#def KillTbl( name):
 #   ind = SvF.Task.getTblNum(name)
  #  if ind >= 0: del SvF.Task.Tbls[ind]


#def getTblNum(name):
 #   for tn, to in enumerate(SvF.Task.Tbls):
  #      print(to.name, name)
   #     if to.name == name:  return tn
    #return -1


def getTbl( name):
    for t in SvF.Task.Tbls:
        if t.name == name:  return t
    return None


def getTblFieldNums( name_col):
    p = name_col.split('.')
    tb_num = SvF.Task.getTblNum(p[0])
    if tb_num == -1:  return -1, -1
    fld_num = SvF.Task.Tbls[tb_num].getFieldNum(p[1])
    #        print ( 'getTblFieldNums', name_col, tb_num, fld_num )
    return tb_num, fld_num


def getTbl_tbl( name_col):
    tb_num, fld_num = SvF.Task.getTblFieldNums(name_col)
    if tb_num == -1 or fld_num == -1: return None
    return SvF.Task.Tbls[tb_num].Flds[fld_num].tb


