# -*- coding: cp1251 -*-
from __future__ import division
#from  numpy import *
#from pyomo.environ import *
from Object import *

from Lego import *
from Task import *


class Polyline (Object):
    def __init__( self, X, Y, Z=None, name='' ):     #  Polyline([1,2,3],..)    Polyline("X","Y",..)    Polyline(fun1,fun2,..)
            Object.__init__(self, name, 'Polyline')
            if X is None : return               # для регистрации на этапе компиляции
            if ( type(X) == type ([])
                or str(type(X)) == '<class \'range\'>'
                or str(type(X)) == '<class \'numpy.ndarray\'>'
               ) :
                self.X = X
                self.Y = Y
                self.Z = Z
            elif type(X) == type ('abc') :
                self.X =  SvF.currentTab.getFieldData(X)
                self.Y =  SvF.currentTab.getFieldData(Y)
                if not (Z is None) :
                    self.Z = SvF.currentTab.getFieldData(Z)
#            elif str(type(X)) == '<class \'range\'>' :
 #               self.X = X
  #              self.Y = Y
   #             self.Z = Z
    #        elif str(type(X)) == '<class \'numpy.ndarray\'>' :
     #           self.X = X
      #          self.Y = Y
       #         self.Z = Z
            else :              # Fun
                print (type(X))
                self.X = []
                self.Y = []
                for i in X.A[0].NodS :
                    self.X.append( X.grdNaNreal(i) )
                    self.Y.append( Y.grdNaNreal(i) )

    def Save(self, fName=''):
        if fName == '':
                fName = self.name + ".txt"
        try:
            fi = open(fName, "w")
        except IOError as e:
            print("Can''t open file: ", fName)
            return
        fi.write('\tX\tY\t#SvFver_62_tbl\n')
        print ("LLL", len(self.X))
        for i in range (len(self.X)):
            fi.write(str(self.X[i]) + "\t" + str(self.Y[i]) + '\n')
        fi.close()


    def Draw(self, mask, pixSize=1, Val=None):
        for p in range(len(self.X)):
            if Val is None:
                pixVal = self.Z[p]
            else:
                pixVal = Val
            if p == 0:
                xe = mask.A[0].ValToInd(self.X[0])
                ye = mask.A[1].ValToInd(self.Y[0])
            else:
                xb = xe
                yb = ye
                xe = mask.A[0].ValToInd(self.X[p])
                ye = mask.A[1].ValToInd(self.Y[p])
                dx = xe - xb
                dy = ye - yb
                if dx == 0 and dy == 0: continue
                if abs(dx) >= abs(dy):
                    for x in range(xb, xe + sign(xe - xb), sign(xe - xb)):
                        y = int(yb + (x - xb) * dy / dx + 0.5)
                        #                    if Val is None :
                        #                       mask.grd[x, y] = self.Z[p]
                        #                  else :
                        #                     mask.grd[x, y] = Val
#                        mask.grd[x, y] = pixVal
                        mask.PutPixel (x,y,pixVal, pixSize)
                else:
                    for y in range(yb, ye + sign(ye - yb), sign(ye - yb)):
                        x = int(xb + (y - yb) * dx / dy + 0.5)
                        #                    if Val is None :
                        #                       mask.grd[x, y] = self.Z[p]
                        #                  else :
                        #                     mask.grd[x, y] = Val
#                        mask.grd[x, y] = pixVal
                        mask.PutPixel (x,y,pixVal, pixSize)


def set_datValbyMask( CS,datVal, Mask,MaskVal ):  #  if Mask[..] == MaskVal  ->>  CS[..] = datVal
    for i in CS.sR :
        x = CS.A[0].dat[i]+CS.A[0].min
        y = CS.A[1].dat[i]+CS.A[1].min
        mask_i = Mask.A[0].ValToInd (x)
        mask_j = Mask.A[1].ValToInd (y)
        if Mask.grd[mask_i,mask_j] == MaskVal :
            CS.V.dat[i] = datVal
 #           print (i,mask_i,mask_j)
#        print (i, CS.A[0].dat[i]+CS.A[0].min,CS.A[1].dat[i],CS.V.dat[i]+CS.A[1].min ,
 #              Mask.A[0].ValToInd (CS.A[0].dat[i]+CS.A[0].min), Mask.A[1].ValToInd (CS.A[1].dat[i]+CS.A[1].min))


def ArctanToGrad(DX):
    ret = DX.CopyMtr(True)
    for x in ret.A[0].NodS:
        for y in ret.A[1].NodS:
            ret.grd[x, y] = arctan ( ret.grd[x, y] ) / pi * 180.
    return ret

def Oper_log10(DX):
    ret = DX.CopyMtr(True)
    for x in ret.A[0].NodS:
        for y in ret.A[1].NodS:
            ret.grd[x, y] = log10 ( ret.grd[x, y] )
    return ret



def reverse01(mask):
    for x in mask.A[0].NodS:
        for y in mask.A[1].NodS:
            mask.grd[x,y] = 1 - mask.grd[x,y]


def putMask (Cs,mask) :                 # маска чаще
    for x in mask.A[0].NodS:
        x_cor = mask.A[0].min + mask.A[0].step * x
        xCs = int(floor((x_cor - Cs.A[0].min)/Cs.A[0].step ) )
        if xCs < 0 :          continue
        if xCs > Cs.A[0].Ub : continue
        for y in mask.A[1].NodS:
            y_cor = mask.A[1].min + mask.A[1].step * y
            yCs = int(floor((y_cor - Cs.A[1].min) / Cs.A[1].step))
            if yCs < 0:          continue
            if yCs > Cs.A[1].Ub: continue
            if mask.grd[x, y] == 0 :  Cs.grd[xCs,yCs] = Cs.NDT

def ClosePolygon (Border) :
        Border.append (Border[0])
        Border.append (Border[1])

def DrawPolygon (mask,Polyg,Val):
        for p in range (int(len(Polyg)/2)) :
            if p==0 :
                xe=mask.A[0].ValToInd (Polyg[0])
                ye=mask.A[1].ValToInd (Polyg[1])
            else :    
                xb=xe    
                yb=ye
                xe=mask.A[0].ValToInd (Polyg[2*p])
                ye=mask.A[1].ValToInd (Polyg[2*p+1])
                dx = xe - xb
                dy = ye - yb
                if dx==0 and dy==0 : continue
                if abs(dx) >= abs(dy) :
                    for x in range ( xb, xe+sign(xe-xb), sign(xe-xb)) :
                        y = int ( yb + (x-xb)*dy/dx+0.5 )
                        mask.grd[x,y] = Val
                else :
                    for y in range ( yb, ye+sign(ye-yb), sign(ye-yb)) :
                        x = int ( xb + (y-yb)*dx/dy+0.5 )
                        mask.grd[x,y] = Val


def FloodFillOutBorder (mask,BordVal,FillVal):
        frame = mask.makeBorder()
        for xy in frame :   mask.FloodFill (xy, BordVal,FillVal)

def setNDTbyMask (H, mask, maskNDT ):
        for x in H.A[0].NodS :
            for y in H.A[1].NodS :
                  if mask.grd[x,y] == maskNDT :
                        H.grd[x,y] = H.NDT

def setNDTbyNoMask (H, mask, maskNDT ):
        for x in H.A[0].NodS :
            for y in H.A[1].NodS :
                  if mask.grd[x,y] != maskNDT :
                        H.grd[x,y] = H.NDT

def setNDTbyCond (H, Cond, Val ):
        for x in H.A[0].NodS :
            for y in H.A[1].NodS :
                  if Cond == '<' and H.grd[x,y] < Val :  H.grd[x,y] = H.NDT




def Minus (H1,H2) :
    ret = H1.CopyMtr()
    ret.param = True
    ret.V.name = H1.V.name + '-' + H2.V.name
#    print ret.V.name
    if H1.param == False and H2.param == True :
        for i in ret.A[0].NodS :
            for j in ret.A[1].NodS :
                ret.grd[i,j] = H1.grd[i,j]() - H2.grd[i,j]
    else :
        ret.grd = H1.grd - H2.grd
    return ret

def MinusVal (H1,Val) :
    ret = H1.CopyMtr()
    ret.param = True
    ret.V.name = H1.V.name 
    ret.grd = H1.grd - Val
    return ret


def MultVal (H1,Val) :
    ret = H1.CopyMtr()
    ret.param = True
    ret.V.name = H1.V.name 
#    ret.grd = H1.grd * Val
    for i in ret.A[0].NodS :
        for j in ret.A[1].NodS :
            if not np.isnan(ret.grd[i,j]): ret.grd[i,j] *= Val
    return ret

def CutMargins (H, mSize) :
    A0 = H.A[0]
    A1 = H.A[1]
    x_s = int( mSize/A0.step )
    y_s = int( mSize/A1.step )
    A0.min += x_s * A0.step
    A1.min += y_s * A1.step
    A0.max -= x_s * A0.step
    A1.max -= y_s * A1.step
    A0.Ub -= 2*x_s
    A1.Ub -= 2*y_s
    A0.makeSets()
    A1.makeSets()
    grd = np.zeros ( (A0.Ub+1, A1.Ub+1),np.float64 )
    for i in A0.NodS :
        for j in A1.NodS :
            if H.param:  grd[i,j] = H.grd[i+x_s,j+y_s]
            else :       grd[i,j] = H.grd[i+x_s,j+y_s]()
    H.grd = grd

def reGrid (H, nStepX, nStepY) :   #  if nStepX > H.A[0].step - среднее по сетке с шагом  nStepX, nStepY
    aX = cnstrArg (H.A[0].name, H.A[0].min-H.A[0].step*0.5+nStepX*0.5, H.A[0].max+H.A[0].step*0.5-nStepX*0.5, nStepX)
    aY = cnstrArg (H.A[1].name, H.A[1].min-H.A[1].step*0.5+nStepY*0.5, H.A[1].max+H.A[1].step*0.5-nStepY*0.5, nStepY)
    ret = cnstrFun2([aX, aY], H.V.name, H.NDT)
    ret.A[0].Aprint()
    ret.A[1].Aprint()
    if nStepX > H.A[0].step :           # среднее по сетке с шагом  nStepX, nStepY
        nX = int ( nStepX / H.A[0].step + 1e-10 )
        nY = int ( nStepY / H.A[1].step + 1e-10 )
        for x in ret.A[0].NodS :
          for y in ret.A[1].NodS :
            nn = 0
            for i in range(nX) :
                for j in range(nY):
                    if H.grd[nX*x+i,nY*y+j] != H.NDT :
                        ret.grd[x,y] += H.grd[nX*x+i,nY*y+j]
                        nn += 1
            if nn == 0 : ret.grd[x,y] = ret.NDT
            else       : ret.grd[x,y] /= nn
    else :                              #  разделить ячейкм для мелкой сетки с шагом  nStepX, nStepY
        nX = int ( H.A[0].step / nStepX + 1e-10 )
        nY = int ( H.A[1].step / nStepY + 1e-10 )
        for x in H.A[0].NodS :
          for y in H.A[1].NodS :
            for i in range(nX) :
                for j in range(nY):
                    ret.grd[nX*x+i,nY*y+j] = H.grd[x,y]
    return ret

def Split (H, nStepX, nStepY) :   #  разделить ячейкм для сетки с шагом  nStepX, nStepY
    nX = int(nStepX / H.A[0].step+0.00000001)
    nY = int(nStepY / H.A[1].step+0.00000001)
    aX = cnstrArg (H.A[0].name, H.A[0].min-H.A[0].step*0.5+nStepX*0.5, H.A[0].max+H.A[0].step*0.5-nStepX*0.5, nStepX)
    aY = cnstrArg (H.A[1].name, H.A[1].min-H.A[1].step*0.5+nStepY*0.5, H.A[1].max+H.A[1].step*0.5-nStepY*0.5, nStepY)

    ret = cnstrFun2([aX, aY], H.V.name, H.NDT)
    ret.A[0].Aprint()
    ret.A[1].Aprint()
    for x in ret.A[0].NodS :
        for y in ret.A[1].NodS :
            nn = 0
            for i in range(nX) :
                for j in range(nY):
                    if H.grd[nX*x+i,nY*y+j] != H.NDT :
                        ret.grd[x,y] += H.grd[nX*x+i,nY*y+j]
                        nn += 1
            if nn == 0 : ret.grd[x,y] = ret.NDT
            else       : ret.grd[x,y] /= nn
    return ret


def SaveProfil ( H, XY, step, fName ) :       #  рабртаем в ГК
      Ax = H.A[0]
      Ay = H.A[1]
      V = H.V
      if fName == '' :  fName = V.name + "(" +Ax.name+ ',' +Ay.name+ ")SvF.Pro"
      fi = open(fName, "w")
      fi.write(Ax.name + '\t' + Ay.name + '\tl\t' + V.name + "_SvF")  # загол

      profLen = 0.
      for xy in range(0, len(XY)-2, 2):
        p1 = [XY[0+xy], XY[1+xy]]
        p2 = [XY[2+xy], XY[3+xy]]
#        print p1,p2

        d = [ p2[0] - p1[0], p2[1] - p1[1] ]
        L = np.sqrt ( d[0]**2 + d[1]**2 )
        N = int(np.ceil((L/step))+1)
        h = [ d[0]/(N-1), d[1]/(N-1) ]
        hh = np.sqrt(h[0]**2+h[1]**2)
#        print 'd', d, 'L', L, 'N', N, 'h', h

        for n in range(N) :
                if xy != 0 and n == 0 : continue
#                dp = [ h[0] * n, h[1] * n ]
                p = [ p1[0] + h[0] * n, p1[1] + h[1] * n ]
                fi.write ( "\n" + str(p[0]) +  "\t" + str(p[1]) +   "\t" + str(profLen) )
                profLen += hh
                if H.param :
                        fi.write ( "\t" + str(H.F([p[0], p[1]])   ) )
                else :
                        fi.write ( "\t" + str(H.F([p[0], p[1]])() ) )
      fi.close()
      print ("END of SaveProfil")




def makeDXDY(H, on_min_0 = True):   #  наклон по x и y
    Hg = H.grd

    h = H.A[0].step
    DX = H.CopyMtr( True, 'DX' )
    for x in H.A[0].NodS:
        for y in H.A[1].NodS:
            if x == 0:
                d = (Hg[x + 1, y] - Hg[x, y]) / h
            elif x == H.A[0].Ub:
                d = (Hg[x, y] - Hg[x - 1, y]) / h
            elif on_min_0 and Hg[x, y] < Hg[x - 1, y] and Hg[x, y] < Hg[x + 1, y]:  d = 0  # min
            else:
                d = (Hg[x + 1, y] - Hg[x - 1, y]) / (2 * h)
            DX.grd[x, y] = d

    h = H.A[1].step
    DY = H.CopyMtr( True, 'DY' )
    for x in H.A[0].NodS:
        for y in H.A[1].NodS:
            if y == 0:
                d = (Hg[x, y + 1] - Hg[x, y]) / h
            elif y == H.A[1].Ub:
                d = (Hg[x, y] - Hg[x, y - 1]) / h
            elif on_min_0 and Hg[x, y] < Hg[x, y - 1] and Hg[x, y] < Hg[x, y + 1]:  d = 0
            else:
                d = (Hg[x, y + 1] - Hg[x, y - 1]) / (2 * h)
            DY.grd[x, y] = d
    return DX, DY


def Curv (H) :           # сумма 2-х произв  d2/dxx + d2/dyy
    hh = H.A[0].step * H.A[0].step
    Hg = H.grd

    D2y = H.CopyMtr( True, 'D2y' )
    for x in H.A[0].NodS:
        for y in H.A[1].mNodSm:
            D2y.grd[x, y] = (Hg[x, y-1] - 2* Hg[x, y] + Hg[x, y+1]) / hh
    for x in H.A[0].NodS:
        D2y.grd[x, 0] = D2y.grd[x, 1]
        D2y.grd[x, H.A[1].Ub] = D2y.grd[x, H.A[1].Ub-1]

    D2x = H.CopyMtr(True, 'D2x')
    for y in H.A[1].NodS:
        for x in H.A[0].mNodSm:
            D2x.grd[x, y] = (Hg[x-1, y] - 2 * Hg[x, y] + Hg[x+1, y]) / hh
    for y in H.A[1].NodS:
        D2x.grd[0, y] = D2x.grd[1, y]
        D2x.grd[H.A[0].Ub, y] = D2x.grd[H.A[0].Ub-1, y]

    Cur = H.CopyMtr(True, 'Curv')
    for x in H.A[0].NodS:
        for y in H.A[1].NodS:
            Cur.grd[x, y] = D2x.grd[x, y] + D2y.grd[x, y]

    return Cur


def XpartYpart(DX, DY):
    Xp = DX.CopyMtr(True,'Xpart')
    Yp = DX.CopyMtr(True,'Ypart')
    for y in Xp.A[0].NodS:
        for x in Xp.A[1].NodS:
            xy = abs(DX.grd[y, x]) + abs(DY.grd[y, x])      ########################  np.sqrt ?
            if xy == 0:
                Xp.grd[y, x] = 0
                Yp.grd[y, x] = 0
                print ('Grad=0', x, y)
            else:
                Xp.grd[y, x] = - DX.grd[y, x] / xy       #if Xp.grd[y,x] > 0 доля потока в ячейку х+1,  else в ячейку х-1
                Yp.grd[y, x] = - DY.grd[y, x] / xy
    print ("End of XpartYpart(DX, DY)")
    return Xp, Yp

def makeIncline (DX,DY) :
             ret = DX.CopyMtr(True,'Slope')
             for x in ret.A[0].NodS :
                for y in ret.A[1].NodS :
                    ret.grd[x,y] = np.sqrt(DX.grd[x,y]**2+DY.grd[x,y]**2)
             return ret


def makeAngle(DX, DY):   #grad
    ret = DX.CopyMtr()
    ret.V.name = 'Angle'
    ret.param = True
    for y in ret.A[0].NodS:
        for x in ret.A[1].NodS:
            ret.grd[y, x] = arctan2(DX.grd[y, x], DY.grd[y, x])/pi*180.
            #                   if ( DX.grd[y,x]==0 and DY.grd[y,x]==0 ) : print 'ret.grd[y,x]',ret.grd[y,x]
    return ret

def makeAngleRad(DX, DY):
    ret = DX.CopyMtr()
    ret.V.name = 'Angle'
    ret.param = True
    for y in ret.A[0].NodS:
        for x in ret.A[1].NodS:
            ret.grd[y, x] = arctan2(DX.grd[y, x], DY.grd[y, x])
    return ret


def makeFlowPond(H, Xp, Yp, flow_int, Pond):
    h = H.A[0].step
    Flow = H.makeMtrParamVnameSetG ('Flow',flow_int)
    Fl = Flow.grd
    Htbl = np.zeros(((H.A[0].Ub + 1) * (H.A[1].Ub + 1), 3), np.float64)
    m = 0
    for x in H.A[0].NodS:
        for y in H.A[1].NodS:
            Htbl[m, 0] = - H.grd[x, y]
            Htbl[m, 1] = x
            Htbl[m, 2] = y
            m += 1
    print ("Htbl", Htbl[0, :], '\n', Htbl[-1, :])
    ii = argsort(Htbl[:, 0], axis=0)
    print ("Htbl", Htbl[ii[0], :], '\n', Htbl[ii[-1], :])

    Out = 0
    PondVal = 0
    for t in range(Htbl.shape[0]):
        x = Htbl[ii[t], 1]
        y = Htbl[ii[t], 2]
        FLxy = max(Fl[x, y] - Pond.grd[x, y], 0)
        PondVal += (Fl[x, y]-FLxy)

        if Xp.grd[x, y] == 0 and Yp.grd[x, y] == 0:  print ("****Grad=0****', x, y")

        if Xp.grd[x, y] < 0 :
            if x != 0:   Fl[x - 1, y] += FLxy * abs(Xp.grd[x, y])        # вниз
            else : Out += FLxy * abs(Xp.grd[x, y])
        elif Xp.grd[x, y] > 0 :
            if x != H.A[0].Ub :  Fl[x + 1, y] += FLxy * abs(Xp.grd[x, y])
            else : Out += FLxy * abs(Xp.grd[x, y])
 #       else:  print 'Xp=0', x, y
        if Yp.grd[x, y] < 0 :
            if y != 0:   Fl[x, y - 1] += FLxy * abs(Yp.grd[x, y])
            else : Out += FLxy * abs(Yp.grd[x, y])
        elif Yp.grd[x, y] > 0 :
            if y != H.A[1].Ub :  Fl[x, y + 1] += FLxy * abs(Yp.grd[x, y])
            else: Out += FLxy * abs(Yp.grd[x, y])
#        else:  print 'Yp=0', x, y
    print ("\nOUTFLOW = ", Out*h*h, 'PondVal', PondVal*h*h, Out*h*h+PondVal*h*h, (H.A[0].Ub+1)*(H.A[1].Ub+1)*flow_int*h*h)
    return Flow



def makeFlow(H, Xp, Yp, flow_int):
    Flow = H.makeMtrParamVnameSetG ('Flow',flow_int)
    Fl = Flow.grd
    grd_init = Fl[0,0]
    Htbl = np.zeros(((H.A[0].Ub + 1) * (H.A[1].Ub + 1), 3), np.float64)
    m = 0
    for x in H.A[0].NodS:
        for y in H.A[1].NodS:
            Htbl[m, 0] = - H.grd[x, y]
            Htbl[m, 1] = x
            Htbl[m, 2] = y
            m += 1
    print ("Htbl", Htbl[0, :], '\n', Htbl[-1, :])
    ii = argsort(Htbl[:, 0], axis=0)
    print ("Htbl", Htbl[ii[0], :], '\n', Htbl[ii[-1], :])

    Out = 0
    for t in range(Htbl.shape[0]):
        x = Htbl[ii[t], 1]
        y = Htbl[ii[t], 2]
        FLxy = Fl[x, y]

        if Xp.grd[x, y] == 0 and Yp.grd[x, y] == 0:  print ("****Grad=0****', x, y")

        if Xp.grd[x, y] < 0 :
            if x != 0:   Fl[x - 1, y] += FLxy * abs(Xp.grd[x, y])        # вниз
            else : Out += FLxy * abs(Xp.grd[x, y])
        elif Xp.grd[x, y] > 0 :
            if x != H.A[0].Ub :  Fl[x + 1, y] += FLxy * abs(Xp.grd[x, y])
            else : Out += FLxy * abs(Xp.grd[x, y])
 #       else:  print 'Xp=0', x, y
        if Yp.grd[x, y] < 0 :
            if y != 0:   Fl[x, y - 1] += FLxy * abs(Yp.grd[x, y])
            else : Out += FLxy * abs(Yp.grd[x, y])
        elif Yp.grd[x, y] > 0 :
            if y != H.A[1].Ub :  Fl[x, y + 1] += FLxy * abs(Yp.grd[x, y])
            else: Out += FLxy * abs(Yp.grd[x, y])
#        else:  print 'Yp=0', x, y
    print ("\nOUTFLOW = ", Out, (H.A[0].Ub+1)*(H.A[1].Ub+1)*grd_init)
    return Flow

def Flood(H):
    print ('Flood*****************************************')  # Заполнение луж и лужищ'
    Hg = H.grd
    Htbl = np.zeros(((H.A[0].Ub + 1) * (H.A[1].Ub + 1), 3), np.float64)
    m = 0
    for x in H.A[0].NodS:
        for y in H.A[1].NodS:
            Htbl[m, 0] = - Hg[x, y]
            Htbl[m, 1] = x
            Htbl[m, 2] = y
            m += 1
#    print "Htbl", Htbl[0, :], '\n', Htbl[-1, :]
    ii = argsort(Htbl[:, 0], axis=0)
#    print "Htbl", Htbl[ii[0], :], '\n', Htbl[ii[-1], :]

    for t in range(Htbl.shape[0]):
        x = Htbl[ii[t], 1]
        y = Htbl[ii[t], 2]
#        if Incline.grd[x,y] != 0 : continue

        minH = Hg[x, y]
        if H.Border(x,y) : continue
        if Hg[x - 1, y] < minH: continue    # не яма
        if Hg[x + 1, y] < minH: continue
        if Hg[x, y - 1] < minH: continue
        if Hg[x, y + 1] < minH: continue
#        if Incline.grd[x,y] != 0 :
 #           print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&', x,y, H.Border(x,y)
  #          continue
   #     print '++++++++++++++++++++++++++++++++++', x,y, H.Border(x,y)

        print ('+++++++++++++++++++++++++++++++++  start x,y', x,y, minH)
        Flo = [[x,y]]               #  прудик
        Borxy = [[-10,-10]]         #  граничные точки - бережок
        Bor = []                    #  бережок и его высота

        for i in range(300000) :
 #           print 'x,y', x, y
            minH = Hg[x, y]
#            Flo.append ([x,y])
#            print 'Flo', Flo

            nei = H.Neighbors(x, y)
            for n in nei :
                if Flo.count([n[0], n[1]]) : continue
                if Borxy.count([n[0], n[1]]) : continue
                if Hg[n[0], n[1]] < minH:
                    print ("Merge into", n[0], n[1], Hg[n[0], n[1]])
                    break
                Bor.append([Hg[n[0], n[1]], n[0], n[1]])
            else :
                Bor.sort()
                x = Bor[0][1]
                y = Bor[0][2]
                Flo.append([x, y])
                Bor = Bor[1:][:]  # .remove(0)
                Borxy = []
                for b in Bor: Borxy.append([b[1], b[2]])
                if H.Border(x, y):
                    print ("Merge across the border") #   Сливаем за кардон (границу)
                    break
                continue
            break
        print ('BorS', Bor)
        print ('Flo', Flo)
        #                     коррекция высоты
        FloN = [[Flo[-1][0],Flo[-1][1],0]]           # соседи точки слива, последний элемент кол-во рукопожатий
        Flo.remove([FloN[-1][0],FloN[-1][1]])
        for hand in range(300000) :        # кол-во рукопожатий
            for f in FloN :
                if f[2] == hand :
                    Nei = H.Neighbors(f[0],f[1])
                    for n in Nei :
                        if Flo.count([n[0],n[1]]) :
                            FloN.append([n[0],n[1],hand+1])
                            Flo.remove([n[0],n[1]])
            if len (Flo) == 0 : break

        step =  minH * 1e-10
        Bor.sort()
        if Bor[-1][0] <= minH + step * FloN[-1][2] :
            print ("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Better to repeat")
        for f in FloN :
            Hg[f[0],f[1]] = minH + step * f[2]          #     коррекция высоты
        print ('********************', minH, len(FloN))
    return H


def FromBorder ( H, Xp, Yp, lev = 0.01 ) :
    FB = H.makeMtrParamVnameSetG ('FromBorder',0)

    for x in FB.A[0].NodS:                         # углы могу попасть дважду, но это не страшно
        if Yp.grd[x, 0] < 0         : FB.grd[x,0] = 1
        if Yp.grd[x, FB.A[1].Ub] > 0: FB.grd[x, FB.A[1].Ub] = 1
    for y in FB.A[1].NodS:
        if Xp.grd[0, y] < 0         : FB.grd[0,y] = 1
        if Xp.grd[FB.A[0].Ub, y] > 0: FB.grd[FB.A[0].Ub,y] = 1

    FB = makeFlow(H, Xp, Yp, FB)
    for x in FB.A[0].NodS:                                # log
        for y in FB.A[1].NodS:
            f = FB.grd[x, y]
            if f != 0 : f = exp(f)
            if f >= lev :  FB.grd[x, y] = 1
            else        :  FB.grd[x, y] = 0
    return FB



