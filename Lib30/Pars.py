# -*- coding: UTF-8 -*-

from  numpy import *
import sys
#from InData import * 
from   GridArgs  import *
from   math         import *

import COMMON as com
#import Table as Tab
#from Table import *


def SplitIgnor ( str, delim ) :
        strU   = str.upper()
        delimU = delim.upper()
        U = strU.split(delimU)
#        print 'll', len(U), U
        ret = []
        p = 0
        for u in U:
            ret.append (str[p:p+len(u)])
            p += len(u) + len (delim)
        return ret

def addDataPath (InFile) :
         if com.DataPath != '' : InFile = com.DataPath + '/' + InFile
         return InFile

def getfloatNaN (st) :
    if st is None : return NaN
    if len(st) :
        if st[0] == '=' : st=st[1:]    #  =0
    try:
        ret = float(st)
        return ret
    except ValueError:
        if len(st)==0 : return NaN
        if st[0]=='*' : return NaN

## 30        if com.Preproc: return st
        if com.Compile: return st

##30        st = com.Task.substitudeDef ( st)
        for itb, tb in enumerate ( co.Task.Tbls ) :  #  from Tbls
#            print 'tb.name', tb.name
            st = SubstitudeName ( st, tb.name+'.NoR', str(com.Task.Tbls[itb].NoR) ) 
            for ifld, fld in enumerate (tb.Flds) :
                st = st.replace ( tb.name +'.'+ fld.name+'.min', str( com.Task.Tbls[itb].Flds[ifld].tb.min(0) ) )
                st = st.replace ( tb.name +'.'+ fld.name+'.max', str( com.Task.Tbls[itb].Flds[ifld].tb.max(0) ) )
#                print 'st', st
 
                f_st = tb.name +'.'+ fld.name+'['                     #  Gb = Tab.G[0]
                if st.find ( f_st ) >=0 :
                    pos = st.find (f_st) + len(f_st)
   #                 print 'p', st[pos:]
                    num_st = st[pos:].split(']')[0]
    #                print 'Pos', num_st
                    st = st.replace ( tb.name +'.'+ fld.name+'['+num_st+']', str( com.Task.Tbls[itb].Flds[ifld].tb[int(num_st)] ) )
     #       print 'sss', st        
        for fu in com.Task.Funs :           # from Fun
            for a in fu.A :
                    st = SubstitudeName ( st, fu.V.name+'.'+a.name+'.min', str(a.min) ) 
                    st = SubstitudeName ( st, fu.V.name+'.'+a.name+'.max', str(a.max) ) 
        for gri in com.Task.Grids :           # from Grid
                    if gri.className == 'Domain' : continue
                    st = SubstitudeName ( st, gri.name+'.min',  str(gri.min)  ) 
                    st = SubstitudeName ( st, gri.name+'.max',  str(gri.max)  ) 
                    st = SubstitudeName ( st, gri.name+'.step', str(gri.step) )
                    st = SubstitudeName ( st, gri.name+'.Ub',   str(gri.Ub)   )

        parts = st.split ( 'LatLonToAzimut(' )             #  LatLonToAzimut
        if len(parts)==1 : parts = st.split ( 'LatLonToGaussKruger(' )    # LanLonToGaussKruger
        if len(parts)==2 :
            parts[1] = parts[1].split(')')[0]
#            print parts
            right = parts[1].split(',')
            if st.find ('LatLonToAzimut') >= 0 : x, y = LatLonToAzimut( float(right[0]), float(right[1]) ); 
            else                               : x, y = WGS84toGausKru( float(right[0]), float(right[0]),0 )
            return [x,y]
        
        try :
            ret = eval (st, {'floor': floor, 'ceil': ceil,'sin': sin, 'cos': cos,
                             'pi': pi, 'sqrt': sqrt, 'log': log, 'radians': radians})  
        except :
            print ('evalERR', st)
#            print com.Task.Tbls[0].Flds[1].tb.min(0)-10.0
            for to in com.Task.Tbls :  print ('Tbl:', to.name)  #   Tbls
            return NaN
        if ret is None : return NaN
        return ret


def getfloat (st) : 
    if len(st) :    
        if st[0] == '=' : st=st[1:]    #  =0
    try:
        ret = float(st)
        return ret
    except ValueError:
        if len(st)==0 : return FLOMAX
        if st[0]=='*' : return FLOMAX
## 30        if co.Preproc : return st
        if co.Compile : return st

  #      print 'gf0', st
        st = com.Task.substitudeDef ( st)
        for itb, tb in enumerate ( co.Task.Tbls ) :  #  from Tbls
#            print 'tb.name', tb.name
            st = SubstitudeName ( st, tb.name+'.NoR', str(com.Task.Tbls[itb].NoR) ) 
            for ifld, fld in enumerate (tb.Flds) :
                st = st.replace ( tb.name +'.'+ fld.name+'.min', str( com.Task.Tbls[itb].Flds[ifld].tb.min(0) ) )
                st = st.replace ( tb.name +'.'+ fld.name+'.max', str( com.Task.Tbls[itb].Flds[ifld].tb.max(0) ) )
#                print 'st', st
 
                f_st = tb.name +'.'+ fld.name+'['                     #  Gb = Tab.G[0]
                if st.find ( f_st ) >=0 :
                    pos = st.find (f_st) + len(f_st)
   #                 print 'p', st[pos:]
                    num_st = st[pos:].split(']')[0]
    #                print 'Pos', num_st
                    st = st.replace ( tb.name +'.'+ fld.name+'['+num_st+']', str( com.Task.Tbls[itb].Flds[ifld].tb[int(num_st)] ) )
     #       print 'sss', st        
        for fu in com.Task.Funs :           # from Fun
            for a in fu.A :
                    st = SubstitudeName ( st, fu.V.name+'.'+a.name+'.min', str(a.min) ) 
                    st = SubstitudeName ( st, fu.V.name+'.'+a.name+'.max', str(a.max) ) 
        for gri in com.Task.Grids :           # from Grid
                    st = SubstitudeName ( st, gri.name+'.min',  str(gri.min)  ) 
                    st = SubstitudeName ( st, gri.name+'.max',  str(gri.max)  ) 
                    st = SubstitudeName ( st, gri.name+'.step', str(gri.step) )
                    st = SubstitudeName ( st, gri.name+'.Ub',   str(gri.Ub)   )

        parts = st.split ( 'LatLonToAzimut(' )             #  LatLonToAzimut
        if len(parts)==1 : parts = st.split ( 'LatLonToGaussKruger(' )    # LanLonToGaussKruger
        if len(parts)==2 :
            parts[1] = parts[1].split(')')[0]
#            print parts
            right = parts[1].split(',')
            if st.find ('LatLonToAzimut') >= 0 : x, y = LatLonToAzimut( float(right[0]), float(right[1]) ); 
            else                               : x, y = WGS84toGausKru( float(right[0]), float(right[0]),0 )
            return [x,y]
        
        try :
            ret = eval (st, {'floor': floor, 'ceil': ceil,'sin': sin, 'cos': cos,
                             'pi': pi, 'sqrt': sqrt, 'log': log, 'radians': radians})  
        except :
            print ('evalERR', st)
#            print com.Task.Tbls[0].Flds[1].tb.min(0)-10.0
            for to in com.Task.Tbls :  print ('Tbl:', to.name)  #   Tbls
            return FLOMAX    
        return ret

def Split3part (txt,cut1,cut2) :
     p1 = txt.find(cut1)
     if p1 == -1:  return txt, '', ''
     p2 = txt.rfind(cut2)
     part1 = txt[:p1]
     part2 = txt[p1+1:p2]
     part3 = txt[p2+1:]
     return part1, part2, part3

def readList19 ( txt, cut1='[',cut2=']' ) :
     part1, part2, part3 = Split3part ( txt,cut1,cut2 )
     return part2.split(',')

def readListFloat19 (txt, cut1='[',cut2=']' ) :
     ret = readList19 (txt, cut1,cut2)
   #  print '\nRRR', ret
     for r in range(len(ret)) :  ret[r] = getfloat(ret[r])   
     return ret

#  def readGrid19 ( txt, eq_in ) :    kill in 27



def findFunGridInExpr ( expr, grid_name, op_b=')' ) :
            for fu in com.Task.Funs :
                p_fu = findNamePos ( expr, fu.V.name )
                if p_fu >= 0 :
                    print (fu.V.name, expr[p_fu:], op_b,)
                    tmp, arg, tmp = getArgsFromBrackets (expr[p_fu:], op_b)    
#                    tmp, in_br, tmp = getFromBrackets (expr[p_fu:],op_b)
 #                   arg = in_br.split(',')
                    for a_n, a_t in enumerate(arg) :
                        if findNamePos ( a_t, grid_name ) >= 0 :
                            return fu.A[a_n], fu
            return None, None

  
def findNamePos ( txt, name, beg=0 ) :   # name         in formula
        tx = txt[beg : ]
#        print  'findNamePos',    txt, name,  beg,  tx, len(name)
        be = 0
        while tx.find (name, be) >=0 :
            p = tx.find (name, be)
            be = p + len(name)
  #          print 'W', p, be
            if p > 0 :
                if ' .,;:+-*/%()[]{}^=<>!'.find(tx[p-1         ]) < 0 : continue
 #               print 'p1=', ' .,;:+-*/()[]{}^='.find(tx[p-1         ])
            if p + len(name)< len(tx) :
                if ' .,;:+-*/%()[]{}^=<>!'.find(tx[p+ len(name)]) < 0 : continue
  #              print 'p2=', ' .,;:+-*/()[]{}^='.find(tx[p+ len(name)])
   #         print  't',   txt[p-1], 'p1=', ' .,;:+-*/()[]{}^='.find(txt[p-1         ])
            return p+beg;
        return -1


def SubstitudeName ( expr, find, subs ) :
            if subs == 'nan' : return expr       # 22/04/20
 #           print 'SubstitudeName', expr, find, subs
            beg = 0
            while ( findNamePos ( expr[beg:], find ) >= 0 ):
                pos = findNamePos ( expr[beg:], find )
#                print "PPPPPPP", pos, expr[pos+beg:]
                expr = expr[0:pos+beg] + subs + expr[beg+pos+len(find):]
 #               print expr
#                beg = beg+pos+len(subs)-len(find)
                beg = beg+pos+len(subs)
  #              print beg
 #               1/0
            return expr
            


def findCloseB (txt, op_b) :
        if op_b == '(' : cl_b = ')'
        if op_b == '{' : cl_b = '}'
        if op_b == '[' : cl_b = ']'
        num = 0
        for p,s in enumerate(txt) :
#            print 'S', s 
            if s==op_b :
                num+=1
                if num==1: op=p
            if s==cl_b :
                num-=1 ;
 #               print 'P',p
                if num==0: return op, p
        return -1
        
def getFromBrackets ( in_txt, op_b, beg_txt=0 )  :         #  достает из скобок
        txt = in_txt[beg_txt:]
#        print 'getFromBrackets Beg',txt        
        for o,s in enumerate(txt) :
            if s == op_b :
#               print '1', txt[o:]
                op, cl = findCloseB (txt,op_b)
                beg   = txt[    :op]
                in_br = txt[op+1:cl]
                end   = txt[cl+1:  ]
#                print 'getFromBrackets Ret', in_txt[:beg_txt]+beg, in_br, end
                return in_txt[:beg_txt]+beg, in_br, end
        return None,'',''


def splitArgs (txt) :
        Args = []
        num = 0
        beg = 0
        for p,s in enumerate(txt) :
            if   s=='(' :  num+=1
            elif s==')' :  num-=1 
            elif s==']' :  num-=1 
            elif s=='[' :  num-=1 
            elif s==',' and num==0:
                Args.append ( txt[beg:p] )
                beg = p+1
        Args.append ( txt[beg:] )
#        print txt, Args
        return Args

def getArgsFromBrackets (txt, op_b)  :         #  достает из скобок список через ,
        beg, in_br, end = getFromBrackets (txt, op_b)
#        print 'getArgsFromBracketsB', in_br
        args = splitArgs (in_br)
#        print 'getArgsFromBracketsA', args 
        return beg, args, end


def UTF8replace ( buf, what, on ) :
        beg = 0
        while buf.find ( what, beg ) >= 0 :                          #     √  ->  SQRT
            p = buf.find ( what, beg )
            buf = buf[:p] + on + buf[p+len(what):]    #  UTF-8
            beg = p + len(on)
        return buf



