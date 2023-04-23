# -*- coding: UTF-8 -*-

from   sys import *

#from   Pars import *
from   Lego import *

import COMMON as com


NUM_SymbolStart = '1234567890.'
NUM_Symbol      = '1234567890.e'
#OPER_Symbol     = '+-*/=<>%!\'\"'
OPER_Symbol     = '+-*/=<>%!'
#OPER_Symbol     = '+-*/=^%'
NAME_Aditional  = '1234567890_'



#def findGridByName_In2List ( global_grids, local_grids, name) :
 #       ret = findGridByName ( global_grids, name)
  #      if  ret == None :  return findGridByName ( local_grids, name)
   #     else :             return ret


#                 0 1   2 34  5 6   7 8   9
#                 a \in [ -337, a_ma, h   ]
#            type       [                 ]
#            lev        1                 1
#            etc        2                 2
#                       5                 5
#                       7                 7
#                       9                 9
class  item:                                      #  etc для (,[,),]  - номера скобок и запятых
        def __init__ (self, part, type, lev ) :   #  
            self.part = part
            self.type = type            # name, fun, var, grid, intr, int, sum, \\d, \\d2, (,) ...
            self.lev  = lev             #  уровень вложения скобок  ( .. ( .. ) .. )
            self.etc  = []              # etc для (,[,),]  - номера скобок и запятых
        def myprint (self) :
            print (self.part, self.type, self.lev, self.etc)

class  parser:
    def __init__ (self, text) :
            self.text = text
            self.items = []
            self.parse ()

    def myprint (self, txt = '') :
            print (txt, 'ITEMS')
            for i, it in enumerate (self.items) : printS(i,'|'),  it.myprint()
    def join ( self, from_ = 0, to_ = 0 ) :
            equation = ''
            if to_ == 0:  to_ = len ( self.items )
            for itn in range ( from_,to_) :  equation += self.items[itn].part
#            for it in self.items : equation += it.part
            return equation
    def find_part ( self, txt, beg=0 ) :
            for itn in range(beg, len(self.items) ) :
                    if self.items[itn].part == txt : return itn
            return -1
    def find_part_lev_back ( self, txt, lev, start ) :
            for itn in range(start, 0, -1 ) :
  #              print ( itn, self.items[itn].part, txt, self.items[itn].lev, lev)
                if self.items[itn].part == txt and self.items[itn].lev == lev  : return itn
            return -1

    def find_type ( self, type, beg=0 ) :
            for itn in range(beg, len(self.items) ) :
                    if self.items[itn].type == type : return itn
            return -1
    def find_part_type ( self, part, type, beg=0 ) :
            for itn in range(beg, len(self.items) ) :
                    if self.items[itn].type == type and self.items[itn].part == part: return itn
            return -1

    def find_part_type_but_point ( self, part, type, beg=0 ) :      # чтобы исключить   x.min   x.step
            for itn in range(beg, len(self.items) ) :
                    if self.items[itn].type == type and self.items[itn].part == part:
                        if itn == len(self.items)-1 :         pass            #   variant  dot after
                        elif self.items[itn+1].part == '.' :  return -1
                        if itn == 0:                          return itn      # variant dot before
                        elif self.items[itn-1].part != '.':   return itn
            return -1

    def substAllNames (self, fin, sub) :
            for it in self.items :
                if it.part == fin : it.part = sub

    def substAllNames_but_dot (self, fin, sub) :
            for itn, it in enumerate(self.items) :
                if it.part == fin :
                    if itn + 1 < len(self.items):
                        if self.items[itn + 1].part == '.':
                            continue
                    it.part = sub

    def substAllNames_but_dot_plus (self, fin, sub) :
            quotes = 0
            for itn, it in enumerate(self.items) :
                if it.part == '\'' or it.part == '\"' :  quotes = 1 - quotes
                if quotes == 1 : continue                                 #  в строках не заменяем !
                if it.part == fin :
                    if itn + 1 < len(self.items):
                        #                        if fin == 'Y': print ('UUUUUUUUUUUUUUUUUUU', self.items[itn + 1].part)
                        if self.items[itn + 1].part == '.':
                            continue
                    if itn > 0:
                        if self.items[itn - 1].part == '.':
                            continue
                    it.part = sub



    def reparse_funs ( self, grids = None ) :
            eq = self.join ()
            par = parser ( eq )
            self.items = par.items
            self.funs ( grids )
            
        
    def Args ( self, bracket ) :
            lis = []
            if bracket >= len (self.items) : return []
            if com.printL : self.items[bracket].myprint()
            etc = self.items[bracket].etc
            for ietc in range( len(etc)-1 ) :
                elem = ''
#                print 'fromto', etc[ietc]+1, etc[ietc+1]
                for i in  range ( etc[ietc]+1, etc[ietc+1] ) :     
                    elem += self.items[i].part
                lis.append ( elem )
#            print 'Args', lis
            return lis

    def getList ( self, beg=0 ) :
            while self.items[beg].part == ' ' : beg += 1  #  пропускаем пробелы
#            print self.items[beg].part
            if self.items[beg].part == '[' :   return self.Args (beg)
            return None 
        

    def getListFloat ( self, beg=0 ) :
            lis = self.getList ( beg )
            if lis == None :  return None 
            for l in range ( len(lis) ):  lis[l] = getfloatNaN ( lis[l] )
            return lis

    def parse ( self ) :
        if com.printL : print ('PARSE', self.text)
        lev_br = 0      #   скобки  ( and [
        num = ''
        oper = ''
        name = ''
        for s in self.text :                                                    #  НАРЕЗКА
 #           print s,    
            if len (num) > 0 :                 #  parse number
                if NUM_Symbol.find(s) >= 0 :
                    num += s
                    continue
                elif s =='-' and num[-1] == 'e' :                 #  1e-2
                    num += s
                    continue
                else :
                    self.items.append(item(num, 'num', lev_br))
                    num = ''
            if len (oper) > 0 :                 #  parse operation
                if OPER_Symbol.find(s) >= 0 :
                    oper += s
                    continue
                else :
                    self.items.append(item(oper, 'oper', lev_br))
                    oper = ''
            if len (name) > 0 :                 #  parse name
#                print name    
                if ( s.isalpha() or NAME_Aditional.find(s) >= 0 ) and name != '\\inn':   #  \innCO2  на два имя
                    name += s
                    continue
                else :
                    self.items.append(item(name, 'name', lev_br))
                    name = ''
            if NUM_SymbolStart.find(s) >= 0 :          #  start number
                num += s
            elif OPER_Symbol.find(s) >= 0 :            #  start operation
                oper += s
            elif s.isalpha() or s == '\\' or s == '_' :            #  start name
                name += s
                                                        
            elif '(' == s or '[' == s or '{' == s :                 #   ()[] {}
                lev_br += 1
                self.items.append(item( s, s, lev_br ))
            elif ')' == s or ']' == s or '}' == s :
                self.items.append(item( s, s, lev_br ))
                lev_br -= 1
            else          :                             # ALL ather  , : ' '
                self.items.append(item( s, s, lev_br ))
                
            if lev_br < 0:
                print ("*****************   Too match  )))))))))))))) ****************")
                print (self.join()) #myprint()
                exit (-1)
        if num  != '' : self.items.append (item(num,  'num',  lev_br ))
        if name != '' : self.items.append (item(name, 'name', lev_br))

        if lev_br > 0:
                print ("*****************  Not enapht )))))))) ****************  lev_br =", lev_br)
                print('in', self.join())
                exit (-1)
                                                        #######  СКОБКИ   для (,[,),] in etc - номера скобок и запятых
        for itn, it in enumerate(self.items) :                                          
            if it.type == '(' or it.type == '[' or it.type == '{':
                etc = [itn]
                for p in range(itn, len (self.items) ) :         #  looking for close br
#                    print 'P', p, self.items[p].type    
                    if self.items[p].type == ',' and self.items[p].lev == it.lev:  etc.append ( p )
                    if (self.items[p].type == ')' or self.items[p].type == ']' or self.items[p].type == '}') \
                            and self.items[p].lev == it.lev :
                        etc.append ( p )
                        it.etc = etc
                        self.items[p].etc = etc
 #                       print '\nAdd ', itn; it.myprint()
                        break
#                 0 1   2 34  5 6   7 8   9
#                 a \in [ -337, a_ma, ha  ]
#            type       [                 ]
#            lev        1                 1
#            etc        2                 2
#                       5                 5
#                       7                 7
#                       9                 9
        for itn, it in enumerate ( self.items[0:-1] ) :           ########   ФУНКЦИя =  имя + ОТКР скобка
#            print '\nCur it', itn; it.myprint()
            if it.type == 'name' and ( self.items[itn+1].type == '(' or self.items[itn+1].type == '[' ) :   it.type = 'fun' 
#        self.myprint("AFTER BR")
        if com.printL : print (self.join(),)
        if com.printL : print ('PARSE_END')

    def funs ( self, grids ) :    #  заменяем на fun ( если '(' )  и вычисляем указатели на разделители аргументов (на ( , ) )  
        Task = com.Task           #  заменяем name  на    var,  grid, int  - integral

        for itn, it in enumerate(self.items) :
            if it.type == 'name' or it.type == 'fun' :
                if   it.part == '\\intr':  it.type = 'intr'              #  заменяем  name  на  intr  - integral  rectangle
                elif it.part == '\\int':   it.type = 'int'               #  заменяем  name  на  int  - integral
                elif it.part == '\\sum':   it.type = 'sum'               #  заменяем  name  на  int  - integral
                elif it.part == '\\d':     it.type = '\\d'               #  заменяем  name  на
                elif it.part == '\\d2':    it.type = '\\d2'              #  заменяем  name  на
                else:
                    if not getFun  ( it.part ) is None :
                        it.type = 'var'                                         #  заменяем  name  на  var#5
                        continue
                        
                    if findGridByName ( grids, it.part ) == None : continue
                    it.type = 'grid'                                        #  заменяем  name  на  grid

        if com.printL : self.myprint()
        if com.printL : print (self.join())
        if com.printL : print ('FUN END')
        return   # grids


    def integral ( self, all_grids ) :       #        ∫( 0,ta,d(t)*mu(-r*t,ap) )     or    ∫( 0,ta,dt*mu(-r*t,ap) )

#        Task = com.Task
        integral_grids = []

        int_type = 'int'
        p_int = self.find_type ( 'int' )          #
        if p_int == -1 :
            int_type = 'intr'
            p_int = self.find_type ( 'intr' )          #
        if p_int == -1 :     return []
        if com.printL : print ('START INTEGRAL')
        while p_int >= 0 :
#            p_int = self.find_type ( 'int' )
 #           if p_int == -1 :    
  #              p_int = self.find_type ( 'intr' )          #
            args = self.Args (p_int+1)
            while args[-1][0] == ' ' : args[-1] = args[-1][1:]    #  убираем первые пробеля
            if args[-1][0] != 'd' :
               print ('**************** d(t)  or  dt  shoud be in the begining  ***************')
               exit (-1)
            p_mult = args[-1].find ( '*' )
            dt = args[-1][1:p_mult]
            dt = dt.replace ( '(', '' ).replace ( ')', '' )             #  (t)  -> t
            body = args[-1][p_mult+1 : ]
            dt_grid = findGridByName ( all_grids, dt )
            print ('dt_grid', dt_grid, dt)
            integral_grids.append ( dt_grid )                      #  ГРИДЫ ПО КОТОРЫМ ИДЕТ ИНТЕГРИРОВАНИЕ 
            step = dt+'.step'       #  str(dt_grid.step)
 #           print ('STEP dt_grid.step=',step, dt_grid.min)
            if len (args) == 3 :
                mi = args[0]   
                ma = args[1]
            else:    
                mi = str(dt_grid.min)   
                ma = str(dt_grid.max)
            dt__i = dt_grid.ind       # индекс грида
 #           print dt__i
            body = SubstitudeName ( body, dt, dt__i )  # подставляем индекс грида
#            print 'BB', body
            if int_type == 'int' :
#                txt = 'sum ( fromiter( (('+dt__i+'!='+mi +')+('+ dt__i+'!='+ma+'))/2*'+step + '*' + body + ' for ' + dt__i + ' in myrange (' + mi + ',' + ma + ',' + step + ') ) )'
                txt = 'sum ( (('+dt__i+'!='+mi +')+('+ dt__i+'!='+ma+'))/2*'+step + '*' + body + ' for ' + dt__i + ' in myrange (' + mi + ',' + ma + ',' + step + ') )'
            else :
#                txt = 'sum ( fromiter( '+step + '*' + body + ' for ' + dt__i + ' in myrange (' + mi + ',' + ma + '-' + step + ',' + step + ') ) )'
                txt = 'sum ( '+step + '*' + body + ' for ' + dt__i + ' in myrange (' + mi + ',' + ma + '-' + step + ',' + step + ') )'
            for j in range (self.items[p_int+1].etc[0], self.items[p_int+1].etc[-1]+1 ) :  self.items[j].part = ''   #  очишаем все
            self.items[p_int].part = txt                
            self.reparse_funs ( all_grids )
            int_type = 'int'
            p_int = self.find_type ( 'int' )          #
            if p_int == -1 :
                int_type = 'intr'
                p_int = self.find_type ( 'intr' )          #
#            p_int = self.find_type ( 'int' )          #
#            if p_int == -1 :    
 #               p_int = self.find_type ( 'intr' )          #

        if com.printL : print (self.join())
        if com.printL : print ('INTEG END', len(integral_grids))
        return integral_grids


    def summa(self, all_grids):  # Σ(i=0,20,mu[i]*(x.V.dat[i]-x(x.A[0].dat[i]))**2)
        if com.printL : print ('START SUM')

        while self.find_type ( 'sum' ) >= 0 :
            p_sum = self.find_type('sum')
            args = self.Args (p_sum+1)
            inde = args[0].split('=')[0]
            lim_mi = args[0].split('=')[1]
            body = 'sum(' + args[-1] + ' for ' + inde + ' in range ( ' + lim_mi + ', ' + args[1] + '+1 ) )'
 #           print (body)
            for j in range (self.items[p_sum+1].etc[0], self.items[p_sum+1].etc[-1]+1 ) :  self.items[j].part = ''   #  очишаем все
            self.items[p_sum].part = body
            self.reparse_funs ( all_grids )
            return




    def dif1  ( self, dif_minus, dif_plus, grids ) :       #  DIF 1      \d(t,H2O(t))
        if self.text.find ('\\d') == -1: return  dif_minus, dif_plus
        self.reparse_funs ( grids ) 
 ##       print (self.join())
#        if self.find_type ( '\\d' ) == -1 :     return  dif_minus
        if com.printL : print ('DIF '+ com.SchemeD1[-1])
        for itn, it in enumerate(self.items) :
            if it.type == '\\d' :                        # par = [ '\d',  '\d',  lev, ]
                args = self.Args (itn+1)
#                print (args)
                fun_name = args[1][:args[1].find ('(')]
#                print ('fun_nameFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF', fun_name)
                if getFun(fun_name).type == 'p' :                   # Polynome
 #                   print ('pppppppppppp', getFun (fun_name).V.name)
                    dif1 = fun_name + '.dF_dX'+ args[1][args[1].find ('('):]  ## 30g+
    #                dif1 = fun_name + '__f.dF_dX' + args[1][args[1].find('('):]
                #                    print (dif1)
#                    1/0
                else :                                                      # grid func
                    gr_name = args[0]
 ##                   print (args[1], gr_name, '(' + gr_name + '+' + gr_name + '__p.step)')
                    plus_st  = SubstitudeName(args[1], gr_name, '(' + gr_name + '+' + gr_name + '__p.step)')  # t -> t+1
                    minus_st = SubstitudeName(args[1], gr_name, '(' + gr_name + '-' + gr_name + '__p.step)')  # t -> t+1
   ##                 print ('plus_st', plus_st, 'minus_st', minus_st)

                    for Sch in reversed(com.SchemeD1) :
#                        print ('                                                             ', gr_name, Sch)
                        parts = Sch.split(' ')
                        Scheme = parts[0]
                        if len(parts)== 1:   break
                        elif parts[1] == gr_name: break
                    if   Scheme == 'Forward' :
                        dif1 = '(' + plus_st + '-' + args[1] + ')/'+gr_name+'__p.step'
                        dif_minus.append(gr_name)
                    elif Scheme == 'Central' :
                        dif1 = '(' + plus_st + '-' + minus_st + ')/'+gr_name+'__p.step *0.5'
                        dif_minus.append(gr_name)
                        dif_plus.append(gr_name)
                    elif Scheme == 'Backward' :
                        dif1 = '(' + args[1] + '-' + minus_st + ')/'+gr_name+'__p.step'
                        dif_plus.append(gr_name)
#                        print ("Not implemented yet:   " + com.SchemeD1);  exit (-1)
                    else :
     ##                   print('\n**********************com.SchemeD1', com.SchemeD1[-1])
                        1 / 0
                it.part = '';  it.type = ''
                for p in range ( self.items[itn+1].etc[0]+1, self.items[itn+1].etc[-1] ) :
                    self.items[p].part = ''
                self.items[p-1].part = dif1
#                    dif_minus.append ( gr_name)
        self.reparse_funs ( grids ) 
##        self.myprint()
#        1/0
        if com.printL : print (self.join ())
        if com.printL : print ('DIF END')
        return  dif_minus, dif_plus
            
    def dif2 ( self, dif_minus, dif_plus, grids ) :       #  \d2(t,x(t))
#        if self.find_type ( '\d2' ) == -1 :     return  dif_minus, dif_plus
#        find_d2 = False
#        for ip in range( len(self.items)-3 ) :
 #           if self.items[ip].part == 'd2' and self.items[ip+1].part == '/' and self.items[ip+2].part[0] == 'd' :
  #              self.items[ip  ].part = '\d2'	                #  'd2' -> 'd2'
   #             self.items[ip+1].part = '('                    #    /  ->  (
    #            self.items[ip+2].part = self.items[ip+2].part[1:-1]   #   dt2 ->  t
     #           self.items[ip+3].part = ','                    #   (   ->  ,
      #          find_d2 = True
       # if not find_d2 : return  dif_minus, dif_plus
        #self.reparse_funs ( grids )

        if com.printL : print ('DIF2', self.join())
        for itn, it in enumerate(self.items) :
            if it.type == '\\d2' :                        # par =  '\d2',  '\d2',  lev,        (  etc ->  '(', 't', ',', 'x(t)', ')' ]
#                    print '\nCur it', itn; it.myprint()
 #                   print self.Args (itn+1)
                    args = self.Args (itn+1)
                    gr_name = args[0]  
  #                  print 'gr_name', gr_name
####                    step = str( findGridByName ( grids, gr_name ).step )    #  ищем в глоб и лок
############## НЕ ПРОВЕРЕНО №№№№№№№№№№№№№№№№№№№№№№№№
                    cop  = SubstitudeName ( args[1], gr_name, '('+gr_name+'+'+gr_name+'__p.step)' )   # t -> t+1
                    copM = SubstitudeName ( args[1], gr_name, '('+gr_name+'-'+gr_name+'__p.step)' )   # t -> t-1
                    dif2 = '(' + cop + '+' + copM + '-2*'+args[1]+ ')/'+gr_name+'__p.step**2'
#                    step = str(findGridByName(grids, gr_name).step)  # ищем в глоб и лок
 #                   cop = SubstitudeName(args[1], gr_name, '(' + gr_name + '+' + step + ')')  # t -> t+1
  #                  copM = SubstitudeName(args[1], gr_name, '(' + gr_name + '-' + step + ')')  # t -> t-1
   #                 dif2 = '(' + cop + '+' + copM + '-2*' + args[1] + ')/' + step + '**2'
  ##                  print ('dif2:', dif2)
                    it.part = '';  it.type = ''
                    for p in range ( self.items[itn+1].etc[0]+1, self.items[itn+1].etc[-1] ) :
#                        print self.items[p].part
                        self.items[p].part = ''
                    self.items[p-1].part = dif2
                    dif_minus.append ( gr_name)
                    dif_plus.append ( gr_name)
                    if com.printL : print (self.join ())
        self.reparse_funs ( grids )
#        self.myprint()        
        if com.printL : print (self.join ())
        if com.printL : print ('DIF2 END')
        return  dif_minus, dif_plus



                                        #  txt как строка так и parse
def  getGRID26 ( txt, grids = []) :   #  if not list    # находим по имени и заменяем
    #            print ('T', txt)
                if com.printL : print ('getGRID26', txt)
                if type (txt) == type ('abc') :    pars = parser ( txt )
                else:                              pars = txt
                
                for delim in ['\\inn', '='] :
                        p = pars.find_part ( delim )
                        if p >= 0:  break
                else :  return None

                if p==0 :
                    name = '__No__Name__'
                else :
                    name = pars.join(0,p).replace(' ','')  #items [ pars.find_type ( 'name' ) ].part
                if com.printL : print ('NA', name, p)

                pDS = pars.find_part ( 'DataSet' )                  # outofdate  #27
                if pDS <  0: pDS = pars.find_part ( 'Domain' )
                if pDS >= 0:
                    arg = pars.Args(pDS+1)
                    if com.printL: print('len (arg)=', len (arg))
                    arg[0] = findGridByName ( grids, arg[0] )
                    if len (arg) >= 3 : arg[2] = findGridByName ( grids, arg[2] )
                    if len (arg) == 2 : return Domain ( name, arg[0],arg[1])
                    if len (arg) == 3 : return Domain ( name, arg[0], arg[1], arg[2])
                    if len (arg) == 4 : return Domain ( name, arg[0], arg[1], arg[2], arg[3])
                lis = pars.getList ( p+1 )
                if com.printL : print ('lis', lis)
                if not lis is None :
                        while len(lis) < 5 : lis.append (None)
                        lis[0] = getfloatNaN ( lis[0] )   # min
                        lis[1] = getfloatNaN ( lis[1] )
                        lis[2] = getfloatNaN ( lis[2] )
 #                       if isnan(lis[3])  :  lis[3]= ''   #  for ind
 #                       for l in range(4) :
  #                          if lis[l] == ''
 #                       print ('L', lis)
    #                    if not com.Preproc:
#                            if isnan(lis[2]) :  lis[2]=-50
                        return Grid ( name, lis[0], lis[1], lis[2], lis[3], lis[4] )

                elif delim == '\\inn':                          #  looking for in other grids
                        p = pars.find_type ( 'name', p+1 )
   #                     print 'p', p
                        if p >= 0 : 
#                            print 'pp33', p, pars.items [ p ].part
                            g = findGridByName ( grids, pars.items [ p ].part)       # находим по имени и заменяем
                            if g is None :
                                co.LastGrid = None
                            else:
                                co.LastGrid = g
                                if com.printL: print ('g.name', g.name)
                                if g.className == 'Grid' :
#                                    return Grid ( name, g.min, g.max, g.step, g.ind, g.oname )
                                    return Grid ( name, g.min, g.max, g.step, g.ind, name )    # !!!???  16.11.2020
                                else :
                                    return g
                return None;


        
