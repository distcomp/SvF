# -*- coding: cp1251 -*-
from __future__ import division
#from  numpy import *

from copy   import *
#from shutil import move


def CreDeriv1Pow ( polyPow, Cin, xyz ) :
        derPow = deepcopy(polyPow)
        C      = deepcopy(Cin)
        if len(C) == 0:   C = [1 for j in range(len(derPow)) ]
        for p in range(len(derPow)) :
            if derPow[p][xyz] == 0 :
                C[p] = 0
            else:
                C[p] *= derPow[p][xyz]
                derPow[p][xyz] -= 1
        return  derPow, C

def CreDeriv2Pow ( polyPow, xyz1, xyz2 ) :
         d1, C = CreDeriv1Pow ( polyPow, [], xyz1 )
         return CreDeriv1Pow ( d1, C, xyz2 )

def PolySize ( dim, maxP ) :
        size = 0
        for i in range((maxP+1)**dim) :
            sumP = 0
            tmpP = i
#            print "i", i 
            for d1 in range(dim) :
                d = dim-d1-1
                power = int( tmpP/((maxP+1)**d) )
                sumP += power
#                print "d", d, "power", power, "tmpP", tmpP, "sumP", sumP 
                tmpP -= power * ((maxP+1)**d)
#            print "sumP", sumP 
            if sumP <= maxP : size += 1
##        print "PolySize", size
#        return range(size)
        return  size

def CrePolyPow ( dim, maxP ) :
        polyPow = []
        for p1 in range(maxP+1) :
            if dim == 1 :
                polyPow.append([p1])
            else :
                for p2 in range(p1+1) :
                    polyPow.append([p1-p2,p2])
        return polyPow
                    

def CrePolyPow1 ( dim, maxP ) :
        polyPow = []
        for i in range((maxP+1)**dim) :
            powers = [[0] for j in range(dim) ]
            sumP = 0
            tmpP = i
            for d1 in range(dim) :
                d = dim-d1-1
                powers[d] = int( tmpP/((maxP+1)**d) )
                sumP += powers[d]
                tmpP -= powers[d] * ((maxP+1)**d)
            if sumP <= maxP : polyPow.append(powers)
        sortPow = []
        for pw in range (maxP+1) :
            for p in polyPow :
                if sum ( p[i] for i in range (dim) ) == pw :
                    sortPow.append ( p )
        return sortPow




