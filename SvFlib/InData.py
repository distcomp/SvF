# -*- coding: cp1251 -*-

#from  numpy import *
import numpy as np

from  GaKru import *

import sys

import COMMON as com
#from   Table import *

from   GridArgs  import *

import openpyxl

#class Rectangle :                  #  Rectangle  ############

 #   def __init__ ( self ) :
  #      self.xMi = 0
   #     self.yMi = 0
    #    self.xMa = 0
     #   self.yMa = 0

#     30
#def ReadPolygon ( InFile ):
 #     print ("\nInPolygonFile: ", InFile)
  #    try :
   #         fi = open ( InFile, "r")
    #  except IOError as e:
     #       print ("не удалось открыть файл", InFile)
      #      return None
#      else :
 #       ret = []
  #      while (1):
   #        line = fi.readline().split()
    #       if len (line) == 0 : break
     #      for l in line :
      #         xy = l.split(',')
       #        ret.append (float(xy[0]))
        #       ret.append (float(xy[1]))
#        fi.close()
 #       return ret
        


def ReadSetInf ( ReadFrom, printL=0, Rect = [] ) :
      try :
            fi = open ( ReadFrom, "r")
      except IOError as e:
            print ("не удалось открыть файл", ReadFrom)
            return None, None, None, None;
      else :
              cols = ['X','Y','Z']
              grdX      = int(fi.readline().split()[1])
              grdY      = int(fi.readline().split()[1])
              XLLCORNER = float(fi.readline().split()[1])
              YLLCORNER = float(fi.readline().split()[1])
              CELLSIZE  = float(fi.readline().split()[1])
              NDT  = float(fi.readline().split()[1])
              if printL: print ("ReadSol from", ReadFrom, cols)
              if printL: print (grdX, grdY, XLLCORNER, YLLCORNER, CELLSIZE, NDT)
 #             print Rect
#              print (Rect[0] - XLLCORNER - CELLSIZE/2 ) / CELLSIZE - 1e-10
 #             print (Rect[2] - XLLCORNER - CELLSIZE/2 ) / CELLSIZE + 1e-10
  #            print (Rect[1] - YLLCORNER - CELLSIZE/2 ) / CELLSIZE - 1e-10
   #           print (Rect[3] - YLLCORNER - CELLSIZE/2 ) / CELLSIZE + 1e-10
              if len (Rect) == 4 :
                  xmi = int ( np.ceil( (Rect[0] - XLLCORNER - CELLSIZE/2 ) / CELLSIZE - 1e-10 ) )    # !!!!!!!!!!!
                  xma = int (floor( (Rect[2] - XLLCORNER - CELLSIZE/2 ) / CELLSIZE + 1e-10 ) )    # !!!!!!!!!!!
                  yma = grdY - 1 - int ( np.ceil( (Rect[1] - YLLCORNER - CELLSIZE/2 ) / CELLSIZE - 1e-10 ))
                  ymi = grdY - 1 - int (floor( (Rect[3] - YLLCORNER - CELLSIZE/2 ) / CELLSIZE + 1e-10 ))
                  print ("|||", xmi, xma, ymi, yma)
                  XLLCORNER += CELLSIZE * xmi
                  YLLCORNER += CELLSIZE * (grdY-1-yma)
                  grdX = xma-xmi+1
                  grdY = yma-ymi+1

                  gr = np.zeros((grdY, grdX),np.float64)
                  for s in range(ymi) : line = fi.readline()
                  for s in range(grdY):
                      line = fi.readline().split()
                      for c in range (grdX) :
                          gr[s][c] = float(line[c+xmi])
              else :
                  gr = np.loadtxt (fi,'double')

              for s in range(gr.shape[0]) : # grdY):
                  for c in range (gr.shape[1]): #grdX) :
                      if gr[s][c] == NDT : gr[s][c] = nan

              gr_rev = np.zeros((grdY, grdX),np.float64)
              for s in range(grdY) : gr_rev[s][:] = gr[grdY-1-s][:]

              x1 = [] #np.zeros(grdX, np.float64)
              x2 = [] #np.zeros(grdY, np.float64)
              for i in range(grdX): x1.append( XLLCORNER + CELLSIZE * (i + 0.5) )
#              for i in range(grdX): x1[i] = XLLCORNER + CELLSIZE * (i + 0.5)
              for j in range(grdY): x2.append( YLLCORNER + CELLSIZE * (grdY-1 - j + 0.5) )
              x2 = sorted ( x2 )
              fi.close()
              if printL: print (gr_rev.shape)
      return cols, x1, x2, gr_rev


def Get_Ver_Typ_cols ( head ):
            head = head.strip()
#            print head
            p_ver = head.find ('#SvFver_')
 #           print 'p_ver', p_ver
            if p_ver > 0 :
#                print 'head[p_ver:]', head[p_ver:]
                parts = head[p_ver+8:].split('_')
 #               print parts                 
                FileVer = int(parts[0])
                InFileTyp = parts[1]
                cols = head[0:p_ver].split()
#                print "RDcols: ", self.cols
                return FileVer, InFileTyp,  cols
            else :
                return 0, None, None

def Get_File_Etc_Ver_Type (ReadFrom ):   # Ver = 0, если чужой файл
    try:
        fi = open(ReadFrom, "r")
    except IOError as e:
        print("не удалось открыть файл", ReadFrom)
        return None, None, None, None;

    line1 = fi.readline()
    head = line1.strip()
    p_ver = head.find('#SvFver_')
    if p_ver > 0:
        parts = head[p_ver + 8:].split('_')
        Ver = int(parts[0])
        Type = parts[1]
        Etc = head[0:p_ver].split()
        return fi, Etc, Ver, Type
    else:
        return fi, line1, 0, None


def ReadSolInf ( ReadFrom, printL=0 ) :
      try :
            fi = open ( ReadFrom, "r")
      except IOError as e:
            print ("не удалось открыть файл", ReadFrom)
            return None, None, None, None;
      else :
              if printL : print ("ReadSol from", ReadFrom)
              Ver,Typ,cols = Get_Ver_Typ_cols ( fi.readline() )
#              print (Ver, Typ, cols)
#              cols = fi.readline().split()
#              if printL : print "ReadSol from", ReadFrom,  cols,
              if not Ver > 0 :
                  print ("**************** Файл:", ReadFrom, 'не является решением')
                  exit (-1)
              if Typ != 'tbl' :                                   # 2-мерный
                  x_poi = fi.readline().split()
                  x1 = np.zeros( len(x_poi), np.float64 )
                  for j in range(len(x1)) : x1[j] = float(x_poi[j])
              else :                                                  # 1-мерный
                  x1  = []    #   ?????????????????
              tb = np.loadtxt (fi,'double')
              fi.close()
              if printL : print ("shape", tb.shape)
#              x2 = []
 #             for i in range(tb.shape[0]) : x2.append(tb[i,0])
  #            print (ReadFrom, tb, tb.shape)
              if str(tb.shape) == '()':    # функция число без аргументов
                  grd = tb
                  x2 = []
   #               print (grd)
              else:
                x2 = tb[:,0]
                if Typ == 'tbl':
                  grd = tb[:,1]
                else :
                  grd = np.delete(tb, range(0, 1), 1)
#      print 'q',x1,'f', x2
      return cols, x1, x2, grd

##############################

####   УБРАН БОЛЬШОЙ КУСОК -  СМ ВЕРСИЯ  29 !!!!!!
