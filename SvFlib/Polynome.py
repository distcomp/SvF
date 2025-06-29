# -*- coding: cp1251 -*-
from __future__ import division
#from  numpy import *

from copy   import *
#from shutil import move

class Monom () :                                #  проба 24.11
    def __init__(self, coef, par_num, vars=[], pows=[]):
        self.coef = coef
        self.par_num = par_num
        self.pows = pows
        self.vars = vars

class Polyno () :
    def __init__(self, txt, par_name, var_names):   # без  скобок
        self.Size = 0
        self.monoms = []
        self.txt = txt.replace (' ','')
        self.par_name = par_name
        self.var_names = var_names
        self.make_monoms()

    def make_monoms(self):
        mon_txt = []       # мономы
        print (self.txt)
        t_last = -1
        for nt, t in enumerate (self.txt) :    # делим на мономы
   #         print (nt,t)
            if t == '+' or t=='-' :
                mon_txt.append (self.txt[max(t_last,0):nt])
                t_last = nt
            elif nt == len(self.txt)-1 :
                mon_txt.append(self.txt[max(t_last, 0):nt+1])   # last monom
        #mon_txt.append(self.txt[max(t_last, 0):nt])
        print (mon_txt, self.var_names)

        for m in mon_txt :
            if len(m) == 0: continue
            coef = 1
            if   m[0] == '+':
                m = m[1:]
            elif m[0] == '-':
                m = m[1:]; coef = -1

            parts1 = m.split('*')          # '**' ->  ''
            parts = []
            mode = ''
            for np in range (len(parts1)):   #  собираем X**4
                if parts1[np] == '' : mode = '**'
                elif mode == '**':
                    parts[-1] += '**' + parts1[np]
                    mode = ''
                else :    parts.append(parts1[np])
            print (m, parts)

            vars = [];  pows = []; par_num =-1
            for np, p in enumerate(parts):
                if p[0].isdigit():
                    coef *= float(p)
                    print ('co', coef)
                    continue
                for nv, v in enumerate (self.var_names):
                    if p.find(v)==0:
                        vars.append(nv)
                        if v == p: pows.append(1)
                        else:      pows.append(int(p[len(v)+2:]))
                if p.find (self.par_name) ==0 :
                    par_num = int(p[len(self.par_name):])
            self.monoms.append (Monom(coef, par_num, vars, pows))
            print ('****', coef, par_num, vars, pows)
        print ('L',len(self.monoms))
 #       1/0

    def Calc (self, gr, vars):
        ret = 0
 #       print (vars)
        for m in self.monoms :
            mon_val = m.coef
            if m.par_num >= 0 :
                mon_val *= gr[m.par_num]
#            for nv in range (len(m.vars)):
            for nv, va in enumerate (m.vars):
                if m.pows[nv] == 1:
                    mon_val *= vars[va]
                else :
                    mon_val *= vars[va]**m.pows[nv]
            ret += mon_val
#            print ('mon_val', ret, mon_val, m.coef )
        return ret

"""""
            mode = ''
            for np, p in enumerate (parts) :
                if mode == 'var':
                    if p == '' :
                        mode = 'var_pow'
                        continue
                if mode == 'var_pow' :
                    print ('vp', p)
                    continue
                print ('p',p)
                if p[0].isdigit():
                    coef *= float(p)
                    print ('co', coef)
                    continue
                if p in self.var_names :
                    print ('var', p)
                    var_pow = 1
                    mode = 'var'
                    continue
                print ('par' , p)
"""""
        #   for t in m :
          #      coef = 1
           #     if t == '+': continue
            #    if t == '-': coef = -1

  #      1/0

"""        
        mon_txt = self.txt.split('+')
        t in self.txt :
            print (t)
            plus_minus = False
            coef = 0
            if   t == '-' :
                coef = -1; plus_minus = True
            elif t == '+' :
                coef = +1; plus_minus = True
            else

   
            #      sizeP = 0
            part = txt.split('gr')
            print(part)
            ret = part[0]
            for p in part[1:]:
                for i, char in enumerate(p):
                    if not char.isdigit():
                        ret += 'gr[' + p[:i] + ']' + p[i:]
                        #                  sizeP = max (sizeP, int (p[:i]))
                        #                  print (ret)
                        break
            #       print('sizeP', sizeP)
            return ret  # , sizeP
"""
"""
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
"""
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
                    
"""
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
"""



