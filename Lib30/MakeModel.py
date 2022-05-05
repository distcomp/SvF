# -*- coding: UTF-8 -*-

from   sys    import *
from Object import *

from   GridArgs  import *
from   Pars   import *
from   Lego   import *
from   Parser import *
from   ModelFiles import *
from Table import *

def grids_add ( all_grids, from_ ) :    # пополняет из from_,  если уже нет в  all_grids
        for g in from_:                                           
            if findGridByName ( all_grids, g.name) == None :       # если еще нет 
                    all_grids.append(g)
        return all_grids


def WriteSelectTable(leftName, Fields, FileName, AsName, where):  #  запись в файл
    if AsName == '': AsName = 'curentTabl'
    if where != '':
        args = ''
        for a in Fields.split(','):
            if a.strip() == '*': continue
            part = SplitIgnor(a, ' As ')
            if len(part) == 1:
                args += part[0]
            else:
                args += part[1]
            args += ', '
 #           print (args)
        args = args[:-2]
        Swr('def where_condition ( ' + args + ' ):')
        Swr('    return (' + where + ')')
    txt = ''
    if leftName != '': txt += leftName + ' = '
    txt += 'Table ( \'' + FileName + '\''
    txt += ',\'' + AsName + '\''
    txt += ',\'' + Fields + '\''
    if where != '': txt += ',' + 'where_condition'
    #        if where != '': txt +=  ',\'' + where +'\''
    txt += ' )'
    #        print (txt)
    Swr(txt)
#    addObject(AsName, 'Tbl', None)
    Table ('', AsName)      #  добавить объект

def WriteTable30(buf):  #  разбор Table
    buf = buf.strip()
#    print (buf)
    part = SplitIgnor(buf, 'Table')
 #   print (part)
    leftName = part[0][:-1]
    parts = part[1].split ('\'')
  #  print (parts)
    FileName = parts[1]
    AsName = parts[3]
    Fields = parts[5]
    if len(parts) >= 8: where = parts[7]
    else :              where = ''
    if AsName == '':  AsName = leftName
    print (leftName,'!', Fields, '!',FileName,'!', AsName, '!',where )
    WriteSelectTable(leftName, Fields, FileName, AsName, where)
    return



def WriteSelect30(buf):  ##  разбор  Select
#    buf = buf.strip()
 #   part = SplitIgnor(buf, 'Select ')
  #  leftName = part[0][:-1]
   # part = SplitIgnor(part[1], ' from ')
    #Fields = part[0]
#    part = SplitIgnor(part[1], ' where ')
 #   if len(part) == 1:
  #      where = ''
   # else:
    #    where = part[1]
#    part = SplitIgnor(part[0], ' As ')
 #   FileName = part[0]
  #  if len(part) == 2:
   #     AsName = part[1]
    #else:
     #   AsName = ''
#    if AsName == '':  AsName = leftName
 #   #       print (leftName,'!', Fields, '!',FileName,'!'+AsName+'!'+where+'!' )
  #  WriteSelectTable(leftName, Fields, FileName, AsName, where)
    leftName, Fields, FileName, AsName, where = ParseSelect30 ( buf )
    WriteSelectTable( leftName, Fields, FileName, AsName, where )
    return


def WriteGrid27 ( buf ):
            if buf == '': return
            Task = SvF.Task
            g = getGRID26(buf, Task.Grids)
##            Task.AddGrid( g )
## 30            wr( '\n    '+g.name+ ' = ' + 'Task.Grids[' + str(len(Task.Grids)-1) + ']' )    #  g__p = Task.Grids[0]
##  Если оставлять надо учесть, что FunFromFileNew добавляет Гриды в список Гридов, при компиляции нет.
            if g.className == 'Grid' :
#                print ('OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO',g.min , SvF.Compile, is_nan (g.min))
                if is_nan (g.min):   g.min = 'SvF.curentTabl.dat(\''+g.oname+'\')[:].min()'
                if is_nan (g.max):   g.max = 'SvF.curentTabl.dat(\''+g.oname+'\')[:].max()'
                if is_nan (g.step):  g.step = -50
                Swr(g.name+'=Grid(\''+g.name+'\','+str(g.min)+','+str(g.max)+','+str(g.step)
                                 +',\''+g.ind+'\',\''+g.oname+'\')')
            else :
                Swr(g.name+'=Domain (\''+g.name+'\','+g.A[0].name+','+str(g.visX))
                if g.dim==1: Swrs(')')
                else       : Swrs(','+g.A[1].name+','+str(g.visY)+')')
## 30            Swr('Task.AddGrid('+g.name+')')


def WriteVarParam26 ( buf, param ) : #, testSet, teachSet ):
        if buf == '':  return
        if SvF.printL:  print ('VarParam26:', buf, param)
        Task = SvF.Task
#        print('VarParam26:', buf, param)
        strInitBy = ''
        strFuncDomain = ''
        Lbound = None
        Ubound = None
        Finitialize = '1' #'0'
        FromFile = ''
        AddGap = False
        fun = None

        parts = buf.split(';')
        p = -1                                              #  вставляем ';'
        if   parts[0].find('<') > 0 : p=parts[0].find('<')   #    X(t) <= 0
        elif parts[0].find('>') > 0 : p=parts[0].find('>')   #   X(t) >= 0
        elif parts[0].find('=') > 0 : p=parts[0].find('=')   # Param:  H(X,Y) = DEM_Kostica.asc
        elif parts[0].find('\\inn')>0: p=parts[0].find('\\inn')   # Param:  H(X,Y) \\in [0,1]
        if p > 0 :
            parts[0] = parts[0][:p] + ';' + parts[0][p:]
            print('P0', parts[0])
            buf1 = ';'.join (parts)
            parts = buf1.split(';')

        for i, part in enumerate (parts) :
## 30                part = Task.substitudeDef ( part )
                part_blanck = part
                part = part.replace(' ','')
                if part == '' :   continue
                up_part = part.upper()
                pars = parser ( part )
                if SvF.printL:  print ('PART:', part)
#                print('PART:', part, up_part, i)

                if i==0 :                                       #  Функция  X(t)
                    fun = Fun(pars.items[0].part ,pars.Args(1), param )
                elif part[0] == '=' :             # Param:  H(X,Y) = DEM_Kostica.asc   H(Y,Y) = 1
                            Finitialize = part[1:]
                elif part.find('<<') == 0:
                            FromFile = part[2:]
                elif getGRID26 ( pars, Task.Grids ) != None :   #  Грид
                        gr = SvF.LastGrid
                        if SvF.printL:  print ('gr.name:', gr.name, gr.className)
                        if gr.name == '__No__Name__' : gr.name = fun.V.name
                        if gr.name == fun.V.name :              #  bounds     for x(t)    x ∈ [ -10.,10 ];
                            Lbound = gr.min
                            Ubound = gr.max
                            if SvF.printL:  print ('LG:', Lbound)                         #   Polynome  не проверено !!!!!!!!!!!!!!!!!!!!!!!!!!
                            if SvF.printL:  print ('UG:', Ubound)
                        else :
                            if gr.className == 'Domain' :    #  PHqt  ( Q, T );  Q,T ∈ QT;
                                fun.domain = gr
                                args = part.split('\\in')[0].split(',')
     #                           print (args)
                             #   1/0
                                for ia,a in enumerate(fun.A) :
                                    gri = Grid (findGridByName ( Task.Grids, gr.A[args.index(a)].name ))
                                    gri.name = a
                                    fun.A[ia] = gri
                                continue
                            for ia, a in enumerate(fun.A):
                                if SvF.printL:  print ('Arg:', a, type(a), type('abc'),)
                                if type(a) != type('abc') : continue
#                                print gr.name, a
                                if gr.name == a :
#                                    fun.A[ia] = Grid (gr)
                                    fun.A[ia] = (gr)
#                                    fun.A[ia] = Arg (gr)
                                    if SvF.printL: print ('ArgName:', fun.A[ia].name)
                                    break
                            else :
                                    print ('********  NO USE FOR ARG GRID ', gr.name, '*********************')
                                    exit(-1)

#                elif part.find('\\in')==0 :
 #                           p = max (part.find('>'), part.find('>=')+1)
  #                          Lbound = getfloat(part[p+1:])
   #                         if SvF.printL:  print ('Lbound=', Lbound)
                elif part.find('>') == 0:
                            p = max(part.find('>'), part.find('>=') + 1)
#                            Lbound = getfloat(part[p + 1:])
                            Lbound = part[p + 1:]
                            if SvF.printL:  print('Lbound=', Lbound)
                elif part.find('<')==0 :
                            p = max (part.find('<'), part.find('<=')+1)
#                            Ubound = getfloat(part[p+1:])
                            Ubound = part[p+1:]
                            if SvF.printL:  print ('Ubound=', Ubound)

                elif up_part.find('POLYPOW')==0 :
                            fun.PolyPow = int(part.split('=')[1])
                            fun.type = 'p'
                            fun.sizeP = PolySize(fun.dim, fun.PolyPow )

                elif up_part.find('VARTYPE')==0 :     fun.type = part.split('=')[1]
                elif up_part.find('DATAFILE')>=0 :    fun.DataReadFrom = 'Select * from '+ part.split('=')[1]
                elif up_part.find('SELECT')>=0 :      fun.DataReadFrom = part_blanck
#                elif up_part.find('INITIALIZE')>=0 :  Finitialize = part.split('=')[1]   # 22.12.19

#                elif part.find('\\in')>=0 :                                     #  не проверено и не понятно  ???????????????????
 #                           tmp = part.split('\\in')
  #                          if tmp[0].find(',')>=0 :  strFuncDomain = tmp[1]           # Function Domain для NDT
   #                         else :   all_grids.append ( readGrid19 ( part, '\\in' ) )
                elif up_part.find('INITBY')>=0 :    #  для явного задания NDT   #  не проверено
                            strInitBy = up_part[6:]
                elif up_part == 'ADDGAP' :
                    AddGap = True
#############################################################   ПРАВИТЬ !!!!!!!!!!!
                elif part.find (fun.V.name) >=0:    #  Нужно искать  ИМЯ а не подстроку !!!!!!!!!!!!!!!!!!!!!!!
                    parts[i] = 'EQ:' + part
                    if SvF.printL:  print ('treated as EQ:',  parts[i])
                else :
                    print ('**************** Cant understand :', part)
                    exit (-1)

        if fun.dim == 1 and type(fun.A[0]) == type('abc') :        # Domain
 #           print ('11111111111111111', fun.A[0]);  1/0
            if not findGridByName ( Task.Grids,fun.A[0] ) is None:
#                print 'LL'
                gr = SvF.LastGrid
 #               print '2', gr.name
                if gr.className == 'Domain':  # PHqt  ( QT );
                    fun.domain = gr
                    fun.A[0] = Grid(gr.A[0])
                    if len (gr.A) == 2:
                        fun.A.append (Grid(gr.A[1]))
                        fun.dim = 2

        f_name = fun.V.name
        Prefix_name = SvF.funPrefix + f_name
        dim = fun.dim

        if FromFile != '' :                 #
            st = f_name + ' = FunFromFileNew (\'' + FromFile + '\',1,True).Rename (\''+fun.V.name+'\''
            for a in fun.A :  st += ',\''+a+'\''
            st += ')'
            Swr ( st )
        else :
          f_str = 'Fun(\''+fun.V.name+'\',['        #    write  into the  StastModel
 #         if fun.DataReadFrom != '' :
  #          Swr (f_name+'.DataReadFrom = \'' + fun.DataReadFrom + '\'' )
          for ia, a in enumerate (fun.A) :          #  Аргументы
            if ia!=0 : f_str += ','
            if type(a) == type('abc'):
                if findGridByName ( Task.Grids,a ) is None:
                    WriteGrid27 ( a + '=[,,]')              #    Дописываем  Grid
                f_str += a
            else :                                          #  Как это может быть?   Устарело  ?
                f_str += 'Grid(\''+a.name+'\','+str(a.min)+','+str(a.max)+','+str(a.step)\
                               +',\''+a.ind+'\',\''+a.oname+'\')'
                print ('Grid(\''+a.name+'\','+str(a.min)+','+str(a.max)+','+str(a.step)\
                               +',\''+a.ind+'\',\''+a.oname+'\')')
          f_str += '],' + str(fun.param)+','+str(fun.PolyPow)+','+Finitialize+', \'' + fun.DataReadFrom + '\') '
          if fun.PolyPow < 0 :
#            Swr (fun.V.name+' = '+f_str+',-1,'+Finitialize+'); ')
            Swr (fun.V.name+' = '+f_str)                                                #  Fun
            if fun.type == 'G':  Swr (fun.V.name+'.type = \'G\'; ')
          else :
            Swr (fun.V.name+' = p'+f_str)                                               #  pFun
  #          Swr(fun.V.name + ' = pFun(' + f_str + ',' + str(fun.PolyPow) + '))')

          if not fun.domain is None :
            Swr(fun.V.name + '.domain = ' + fun.domain.name )
##30          Swr ('Task.InitializeAddFun ( '+fun.V.name+ ', \''+ Finitialize +'\' )')
  #        Swr ('Task.InitializeAddFun ( '+fun.V.name )
   #       if Finitialize is None : Swrs (' )')
    #      else :                   Swrs ( ', \''+ Finitialize +'\' )')
## 30g+          Swr( fun.V.name + '__f = ' + fun.V.name)
          if AddGap :   Swr ( fun.V.name+'.AddGap( )'); #AddGap=False

        if   dim == 0  :  Swr( Prefix_name + ' = ' + f_name + '.grd')  #
        else:                                            # def fE (t) : return E.F([t])
            def_part = 'def ' + Prefix_name + '('
            ret_part = 'return ' + f_name + '.F(['
            for i, a in enumerate( fun.A ) :
                if i>0: arg = ','+getName(a)
                else  : arg =     getName(a)
                def_part += arg
                ret_part += arg
            def_part += ') : '
            ret_part += '])'
            Swr(def_part + ret_part)                     # def fE (t) : return E.F([t])

 #       if fun.PolyPow >=0:     fun = pFun(fun)

 #       SvF.ReadFrom = ''

## 30        Task.AddFun ( fun )
        Task.Funs[-1].Oprint()

        if 0:   #not SvF.Preproc :   30
            if strInitBy != '' :
                        print ('strInitBy', readListFloat19 (strInitBy,'(',cut2=')' ) )
                        ar = readListFloat19 (strInitBy,'(',cut2=')' )
                        Task.Funs[-1].InitBy (ar[0],ar[1],ar[2])     # -1  !!!!!!!!!!!!!!!!!!!
            if strFuncDomain != '' :
                        print ( strFuncDomain, getFun(strFuncDomain).name )
                        Fdomain = getFun(strFuncDomain)
                        for a0 in Fdomain.A[0].NodS :
                            for a1 in Fdomain.A[1].NodS :
                                SvF.Task.Funs[-1].neNDT[a0,a1] = Fdomain.grd[a0,a1]
                        SvF.Task.Funs[-1].calcNDTparam()
            if AddGap : SvF.Task.Funs[-1].AddGap()

#        if not SvF.MakeModel : return

        f = SvF.ModelFile
        f_num = len ( Task.Funs ) -1
        d = Task.Funs[f_num]
#        f_str = 'Funs['+str(f_num)+ ']'
        if Finitialize is None  : Finitialize = '1'
#        f_name = d.V.name
        if not d.param :                                                 # 30g+
            pass                                                        # 30g+
        #    wr(' \t\t\t\t\t\t\t\t\t\t\t# '+buf )
        #    wr('    ' + f_name + ' = ' + f_str + ';  ' + f_name + '__f = ' + f_name )
        if  d.param :                                                 # Param
                    pass
                   #   wr ( '    '+ f_name + '__i = ' + f_str+'.grd' )   ###### 30g+
        else :
            if d.PolyPow >= 0:   # Poly
#                  wr ( '    ' + f_name + '__i = Var ( range (PolySize(' + str(d.dim)+','+str(d.PolyPow)+') ), initialize = 0 )' )
                  wr ( '\n    ' + f_name + '.var = Var ( range (' + str(d.sizeP) + '), initialize = 0 )' )
                  wr('    Gr.' + f_name + ' =  ' + f_name + '.var')
        #        wr('    ' + f_name + '__i = Var ( range (' + str(d.sizeP) + '), initialize = 0 )')
         #       wr('    ' + f_name + '.var = ' + f_name + '__i ; Gr.' + f_name + ' =  ' + f_name + '__i')
            #                  wr('    ' + f_name + '.grd = ' + f_name + '__i ; Gr.' + f_name + ' =  ' + f_name + '__i')
            else :            # Grid
                  if not d.param :                                                 # Var
#                      wr ( '    ' + f_name + '__i = Var ( ' )          # 30g+
                      wr ( '\n    ' + f_name + '.var = Var ( ' )
                      for di in range (d.dim) :
#                          wrs ( f_str+'.A['+str(di)+'].NodS,' )        # 30g+
                          wrs ( f_name+'.A['+str(di)+'].NodS,' )
#                          f.write(f_str + '.A[' + str(di) + '].NodS,')
                      wrs ( 'domain='+str(d.domain_)+',' )
#                      f.write( 'domain='+str(d.domain_)+',' )
                      if not (Lbound is None and Ubound is None):
                          wrs ( ' bounds=('+str(Lbound)+','+str(Ubound)+'),')
                      wrs ( ' initialize = '+Finitialize+' )' )
          #            f.write(' initialize = ' + Finitialize + ' )')
                      wr ( '    Gr.'+f_name+' =  ' + f_name + '.var' )
          ##            wr('    ' + f_name + '.var = ' + f_name + '__i ; Gr.' + f_name + ' =  ' + f_name + '__i') # 30g+

            if d.PolyPow < 0:   # Grid
                      wr( '    '+f_name+'.InitByData()' )
        if not d.neNDT is None:                     #27
            wr( '    '+f_name+'.Fix()' )

        if not d.param :                                                 # 30g+
#          if   dim == 0  :  wr('    ' + Prefix_name + ' = ' + f_name + '__i')  # =  __i   # 30g+
          if   dim == 0  :  wr('    ' + Prefix_name + ' = ' + f_name + '.var')  # =  __i
          elif dim == 1:
            wr('    def ' + Prefix_name + '(' + getName(fun.A[0]) + ') : return '
                        + f_name + '.F([' + getName(fun.A[0]) + '])')  # def fE (t) : return E.F([t])
          elif dim == 2:
            wr('    def ' + SvF.funPrefix + f_name + '(' + getName(fun.A[0]) + ',' + getName(fun.A[1]) + ') : return '
                        + f_name + '.F([' + getName(fun.A[0]) + ',' + getName(fun.A[1]) + '])')
          elif dim == 3:
            wr('    def ' + SvF.funPrefix + f_name + '(' + getName(fun.A[0]) + ',' + getName(fun.A[1]) + ',' + getName(fun.A[2]) + ') : return '
                        + f_name + '.F([' + getName(fun.A[0]) + ',' + getName(fun.A[1]) + ',' + getName(fun.A[2]) +'])')

        if d.PolyPow >= 0 and not d.param:   # Poly
            wr ( '    ' + f_name + '.var[0].value = ' + Finitialize )
# EQ:
        if d.PolyPow >= 0:   # Poly
            if not Lbound is None :
                WriteModelEQ26 ( parts[0] + '>=' + str(Lbound)  )
            if not Ubound is None :
                WriteModelEQ26 ( parts[0] + '<=' + str(Ubound)  )
                
        for part in parts :
#            print 'P:', part
            if part.find('EQ:') == 0:    WriteModelEQ26 ( part[3:] )


def fromTEX(equation) :
#    equation = UTF8replace(equation, '\\cdot', '*')
 #   equation = UTF8replace(equation, '\\limits', '')
  #  equation = UTF8replace(equation, '\\left',   '')
   # equation = UTF8replace(equation, '\\right',  '')
    print ('TEXsubst', equation)

    sel = parser(equation)
    repars = True
    while (repars) :
        repars = False
        for itn, it in enumerate(sel.items) :
            if it.type == 'name' or it.type == 'fun' :
                if it.part == '\\frac' :                    #  \frac{d}{dro}(Df) = Pdf
                    repars = True
                    it.part = ''
                    sel.items[itn+1].part = ''
                    pos = sel.items[itn+1].etc[1]
                    sel.items[pos].part = '/'
                    pos += 1
                    sel.items[pos].part = ''
                    pos = sel.items[pos].etc[1]
                    sel.items[pos].part = ''
                    pos += 1
                    if sel.items[pos].part == '{' :   #  замена  {}  ()
                        sel.items[pos].part = '('
                        pos = sel.items[pos].etc[1]
                        sel.items[pos].part = ')'
                if it.part.find ('\\int_') == 0 :        # INTEGRAL  запись  ∫_{0}^{rp}{d(x)*expr} -> ∫(0,rp,d(x)*expr)
                    repars = True
                    it.type = 'int'
                    lim_min = it.part.split('_')[1]
                    print ('lim_min', lim_min)
#                    UTF8replace (it.part,'\\int_','\\int(')
   #                 print (it.part)
                    it.part=it.part[0:4]+'('+lim_min
  #                  print(it.part)
                    pos = itn+1
                    if len (lim_min) == 0 :                     # {lim_min}  in   int_{lim_min}
                        sel.items[itn+1].part = ''
                        sel.items[sel.items[itn+1].etc[1]].part = ''
                        pos = sel.items[itn+1].etc[1]+1
                    sel.items[pos].part = ','
                    pos += 1                                    # lim_max
                    if sel.items[pos].part == '{' :
                        sel.items[pos].part = ''
                        pos = sel.items[pos].etc[1]
                        sel.items[pos].part = ''
                    sel.items[pos].part += ','
                    pos += 1                                    # { body }
                    sel.items[pos].part = ''
                    pos = sel.items[pos].etc[1]
                    sel.items[pos].part = ')'

                if it.part.find('\\sum_') == 0:  # SUMMA  запись  ∫_{0}^{rp}{d(x)*expr} -> ∫(0,rp,d(x)*expr)
                    repars = True
                    it.type = 'sum'
                    print ('it.partTT', it.part, itn, sel.items[itn].part)
                    lim_min = it.part.split('_')[1]
                    print('lim_min |'+ lim_min+'|')
                    #                    UTF8replace (it.part,'\\int_','\\int(')
                    #                 print (it.part)
                    it.part = it.part[0:4] + '(' + lim_min
                    #                  print(it.part)
                    pos = itn + 1
                    print('it.part', it.part, sel.items[itn].part, sel.items[itn + 1].part, sel.items[itn + 2].part)
                    if len(lim_min) == 0:  # {lim_min}  in   int_{lim_min}
                        print (sel.items[itn + 1].part)
                        sel.items[itn + 1].part = ''
                        sel.items[sel.items[itn + 1].etc[1]].part = ''
                        pos = sel.items[itn + 1].etc[1] + 1
                    sel.items[pos].part = ','
                    pos += 1  # lim_max
                    if sel.items[pos].part == '{':
                        sel.items[pos].part = ''
                        pos = sel.items[pos].etc[1]
                        sel.items[pos].part = ''
                    sel.items[pos].part += ','
                    pos += 1  # { body }
                    sel.items[pos].part = ''
                    pos = sel.items[pos].etc[1]
                    sel.items[pos].part = ')'

                if repars :
                    equation = sel.join()
                    sel = parser(equation)
                    print ('Tex', it.part, equation );  sel.myprint()
                    break
#    print ("********************************", SvF.UseHomeforPower)
#    1/0
    if SvF.UseHomeforPower :     equation = UTF8replace(equation, '^', '**')
    else :                      equation = UTF8replace(equation, '^', '')
    return equation

def ParseEQUATION ( equation, all_grids ) :
        Task = SvF.Task
        Funs = Task.Funs

#        print 'Beg:', equation
        dif_minus = []                               # DERIV     (H2O((t+1.0))-H2O(t))/1.0==-E(t)*2.0736+WF*WD(t)
        dif_plus = []                               # DERIV 2

        equation = fromTEX(equation)

        eqPars   = parser ( equation )
                                           #  Добавляем опущенные Аргументы
        if SvF.printL:  print ('ParseEQUATION'); eqPars.myprint()
        reparse = True
        while reparse :
          reparse = False
          for iit, it in enumerate(eqPars.items) :
            if it.type == 'name' :                  # нет  (
                if iit < len(eqPars.items)-1 :
                    if eqPars.items[iit+1].part == '.' : continue          #  F.Complex...
                for f in Funs :
                    if f.V.name == it.part and len(f.A) > 0:
                        for ia,a in enumerate( f.A ) :
                            if ia == 0:  it.part += '('
                            else      :  it.part += ','
                            if type( f.A[ia] ) == type('abc') : it.part += f.A[ia]
                            else                              : it.part += f.A[ia].name
                        it.part += ')'
                        if SvF.printL:  print ('NewPart',  it.part)
                        reparse = True
          if reparse :  eqPars   = parser ( eqPars.join() )
        if SvF.printL:  eqPars.myprint()
        

                        
        for it in eqPars.items :
            if it.lev == 0 and  ( it.part[0] in [ '=', '<', '>' ] )  :     # '='  ->  '=='  '=-/ -> ==-
                if SvF.printL : it.myprint()
                if   len (it.part) == 1 :                        it.part += '=' 
                elif len (it.part) == 2 and it.part[1] != '=' :  it.part  = it.part[0] + '=' + it.part[1:] #  '=-'  -> '==-'
                
                if SvF.printL : print ('AFTER') ;  it.myprint()

        print ('ALL_Grids B', len(all_grids))
        for g in all_grids : print (g.name)

        for g in Task.Grids:                                       # пополняем  all_grids  из общих Гридов
            if findGridByName ( all_grids, g.name) == None :       # если еще нет 
#                if eqPars.find_part_type ( g.name, 'name' ) >= 0 : # пока ищем in name
                if eqPars.find_part_type_but_point( g.name, 'name' ) >= 0 :  # чтобы исключить   x.min   x.step
                    all_grids.append(g)

#        print ('ALL_Grids A', len(all_grids))
 #       for g in all_grids : print (g.name)

#####??        eqPars = parser ( equation )
        eqPars.funs( all_grids )                                        #  ... name -> grid
        dif_minus, dif_plus  = eqPars.dif1 ( dif_minus, dif_plus, all_grids )
        dif_minus, dif_plus  = eqPars.dif2 ( dif_minus, dif_plus, all_grids )
        eqPars.summa(all_grids)
        integral_grids = eqPars.integral( all_grids )                       # лучше оставить последним - там всякие for и sum
 #       for itn, it in enumerate( eqPars.items ) :
  #          if it.part == '.' and eqPars.items[itn-1].type == 'var'  :  it.part = '__p.'
        equation = eqPars.join()
        if SvF.printL : print ('END PARSE', equation)
       # print('END PARSE                                                            ', equation)
#        print 'INTids', len(integral_grids)
 #       for g in integral_grids : print g.name 

        constraint_grids=[]                         #  фигурируют в EQ  но не как  d(t)
        for g in all_grids :
            if SvF.printL : print (g.name)
            if findGridByName ( integral_grids, g.name) == None :            #  
                constraint_grids.append(g)

  #      print 'con Grids', len(constraint_grids)
   #     for g in constraint_grids: print g.name
   
        return  equation, eqPars, constraint_grids, dif_minus, dif_plus

eqNUM = 0

def WriteModelEQ26 ( buf ):
#        if not SvF.MakeModel : return
        if buf == '' : return
        global eqNUM
        eqName = 'EQ'+str(eqNUM)
        if SvF.printL:  print (eqName)
        Task = SvF.Task

        b_if = ''                                   #  Constraint.Skip
#        print (buf,  buf[:2])
        if buf[:2] == 'if' :
            if_p = buf.split(':')
            if len(if_p) > 1 :
                b_if = 'if not (' + if_p[0][2:] + ') : '
                buf = ''.join(if_p[1:])


        parts = buf.split(';')                      #  ; отделяет Гриды and conditions
        parts = list(filter(('').__ne__, parts))    # удаляет пустые элементы ''
        if SvF.printL:  print (eqName, parts)
        
        equation = parts[0]                       #  первая часть !
        equation = equation.replace(' ','')
        
        all_grids = []                              #  local (заданные в EQ  после ; and global grids
#        b_if = ''                                   #  Constraint.Skip
        for part in parts[1: ] :
            print (parts[1: ])
   ###         1/0
###            if not SvF.Preproc : part = Task.substitudeDef ( part )
            part = Task.substitudeDef(part)
            gr = getGRID26 (part, Task.Grids)
            if gr is None :
                print ('Can\'t treat  |' +part+ '|  in  '+buf)
                exit(-1)
            all_grids.append ( gr )
            WriteGrid27 (part)                   ############# 25/11/2021   перенести в Model ?

        equation, eqPars, constraint_grids, dif_minus, dif_plus = ParseEQUATION ( equation, all_grids )

        for g in constraint_grids:
#            eqPars.substAllNames (g.name, g.ind)
            eqPars.substAllNames_but_dot (g.name, g.ind)                ## 30g+
            eqPars.substAllNames (g.name+'__p', g.name)
        for fu in Task.Funs:
            eqPars.substAllNames_but_dot(fu.V.name, SvF.funPrefix+fu.V.name)
##            eqPars.substAllNames(fu.V.name, SvF.funPrefix+fu.V.name)

        equation = eqPars.join()
        if SvF.printL : print ('EQAFTER', equation)

        f = SvF.ModelFile                            #   WRITE
        wr(' \t\t\t\t\t\t\t\t\t\t\t# '+buf )
        wr ( '    def '+eqName+' (Gr' )                   # def EQ*(Gr,t) :
        for g in constraint_grids :
            wrs ( ','+g.ind )
        wrs ( ') :' )
#        if b_if != '' :  wr('        if not ('+b_if+') : return Constraint.Skip')         #  Constraint.Skip
        if b_if != '' :  wr('        ' + b_if + 'return Constraint.Skip')         #  Constraint.Skip
        wr('        return (')
        wr('          '+equation)
        wr('        )')
        wr('    Gr.con'+eqName+' = Constraint(')                                  
        for ng, g in enumerate(constraint_grids) : 
            if SvF.printL:  g.Gprint()
            my_range = 'FlNodS'
            if g.name in dif_plus:  my_range  = 'm' + my_range
            if g.name in dif_minus: my_range  = my_range + 'm'
#            wrs ( g.name + '__p.' + my_range + ',')
            wrs(g.name + '.' + my_range + ',')
#            wrs('myrange('+str(g.min) )
 #           if g.name in dif_plus:   f.write ('+'+str(g.step)+','+str(g.max))           # myrange(0+1,179),
  #          else :                   f.write (','+str(g.max))                           # myrange(0,179),
   #         if g.name in dif_minus:  f.write ('-'+str(g.step)+','+str(g.step)+'),')     # myrange(0,179-1),
    #        else :                   f.write (','+str(g.step)+'),')                     # myrange(0,179),
        wrs('rule='+eqName+' )')                                                    # rule=DifEQ )

        eqNUM += 1
        return

def WriteModelDef26 ( code ):                       #   DEF:
#        if not SvF.MakeModel : return
        if code == '' : return
#        code = SvF.Task.substitudeDef (code)

        code, eqPars, constraint_grids, dif_minus, dif_plus = ParseEQUATION ( code, SvF.Task.Grids )
        
        parts = code.split('==')
        wr ( '    def '+parts[0]+': return '+parts[1]+'\n' )    # Code  for r in T.A[0].NodS:  T.gap[r,21]=0

def WriteModelCode26 ( code ):                      #   CODE:
        if code == '':  return
#        code = SvF.Task.substitudeDef (code)
        wr ( '    '+code)                                 # Code  for r in T.A[0].NodS:  T.gap[r,21]=0


def WriteModelOBJ19 ( Q, obj ):                        #   OBJ:
#        if not SvF.MakeModel : return
        Task = SvF.Task
        Funs = Task.Funs
        f = SvF.ModelFile

        if len(obj)==0 :        #   obj по умолчанию   -   OBJ:
            for fu in Funs :
              if fu.param : continue
              if len (fu.A) == 1:
                obj += fu.V.name + '.MSDnan() + ' + fu.V.name + '.Complexity(Penal[0])'   # x.MSD() + x.Complexity(Penal[0])
              else :
                obj += fu.V.name + '.MSDnan() + ' + fu.V.name + '.Complexity(Penal[0],Penal[1])'

        MsdType = ''
        Delta_Formula = 'Gr.F[fNum].Ftbl(n)-tbl[n]'  #  ПРОВЕРИТЬ  !!!!  заменить   Gr.F ->  Task.Funs

        obj, eqPars, constraint_grids, dif_minus, dif_plus = ParseEQUATION ( obj, [] )

####################################################  ЗАПЛАТКА ###############   ∫(t_min,t_max,dT∙(d2/dT2(x(T)))**2)
        for g in Task.Grids:
                eqPars.substAllNames(g.name + '__p', g.name)
####################################################

        for fu in Task.Funs:
            eqPars.substAllNames_but_dot(fu.V.name, SvF.funPrefix + fu.V.name)

 #       eqPars.substAllNames_but_dot('Compl', 'Complexity')

        obj = eqPars.join()
        beg = 0
        while 1:                                                                    #  Add []
            beg = obj.find('.Compl', beg)
            if beg < 0 : break
            if    obj.find('.Compl(',     beg) == beg :     beg +=  len('.Compl(')
            elif  obj.find('.Complexity(',beg) == beg :     beg +=  len('.Complexity(')
            elif  obj.find('.ComplCycle(',beg) == beg :     beg +=  len('.ComplCycle(')
            elif  obj.find('.ComplCyc0E(',beg) == beg :     beg +=  len('.ComplCyc0E(')
            elif  obj.find('.ComplSig2(', beg) == beg :     beg +=  len('.ComplSig2(')
            elif  obj.find('.ComplMean2(',beg) == beg :     beg +=  len('.ComplMean2(')
            else : break
            if obj[beg] == '[' : continue
            begi, in_br, end = getFromBrackets ( obj, '(', beg-1 )
            obj = begi + '([' + in_br + '])' + end
        if SvF.printL:  print ('OBJ:', obj)

        obj, eqPars, constraint_grids, dif_minus, dif_plus = ParseEQUATION ( obj, [] )

        SvF.lenPenalty = 0
        for itn, it in enumerate (eqPars.items) :
            if it.part == 'Penal' :
                SvF.lenPenalty = max (SvF.lenPenalty, int(eqPars.items[itn+2].part)+1 )

 #       if not SvF.MakeModel : return


        if obj == 'N' :
          obj = ''
          penNum = 0
          for fu in Funs :
            if fu.param : continue
            if len(fu.A) == 0 : continue
            if len(obj) > 0 :  obj += '+'
            obj += fu.V.name + '.Complexity(['
            for a in fu.A :
                if a != fu.A[0] : obj += ','
                obj += 'Penal[' + str(penNum) + ']'
                penNum += 1
            obj += '])/' + fu.V.name + '.V.sigma2'
            obj += ' + ' + fu.V.name + '.MSDnan()'
            SvF.lenPenalty = penNum
        else :
          objP = obj.split('defMSD')
          if len(objP) == 2 :  #>1
            p_plus = objP[0].rfind('+')
            if p_plus <= 0 : p_plus = 0
            fNum = getFunNum(objP[0][p_plus+1:-1])
#            print objP
            beg, delta, end = getFromBrackets (objP[1],'(')
            if beg == None :  beg, delta, end = getFromBrackets (objP[1],'{')  #  стары1 вариант
            MsdType = beg
            print ('MsdType=', beg, delta, end)
  #          print 'DELTA1', delta
            if delta !='' and delta !=' ' :
                for ifu, fu in enumerate ( SvF.Task.Funs ) :
                    pf = delta.find (fu.V.name)
                    if pf>=0 : delta = delta.replace(fu.V.name, 'Gr.F['+str(ifu)+'].Ftbl(n)' )  # replace   f for  Gr.F[...
#                print 'DELTA2', delta
                Delta_Formula = delta
            if SvF.printL:  print (delta)
            obj = objP[0][:p_plus+1] + 'defMSD(Gr,'+str(fNum)+')'+end
            if SvF.printL:  print (obj)
#       Penalty
        if len (SvF.Penalty) == 0 :
#            print '********C', obj.count('Penal[')
            for p in range(obj.count('Penal[')) : SvF.Penalty.append (.1)

        for itn, it in enumerate(eqPars.items):
            if it.part == 'MSD' or it.part == 'MSDnan' : # or it.part == 'MSDcheck'
                fn = (eqPars.items[itn-2].part)
                wr('\n    ' + fn + '.mu = Gr.mu;')
                wrs(' ' + fn + '.testSet = SvF.testSet;')
                wrs(' ' + fn + '.teachSet = SvF.teachSet;')
#                wrs(' ' + fn + '.CVval = zeros('+ fn +'.NoR, float64)')   #  move to testEstim

        wr(' \t\t\t\t\t\t\t\t\t\t\t# ' + obj)
        wr('    def obj_expression(Gr):  \n        return (')
        wr('             ' + obj )                             #   Gr.F[1].Complexity ( [Penal[0]] ) + Gr.F[0].MSD()
        wr('        )  \n    Gr.OBJ = Objective(rule=obj_expression)  \n')
        f.write('\n    return Gr\n')        # end of    createGr ( Task, Penal ) :

 #                       Swr('Task.Delta     = Delta')
  #                      Swr('Task.DeltaVal  = DeltaVal')
   #                     Swr('Task.defMSD    = defMSD')
    #                    Swr('Task.defMSDVal = defMSDVal')

        f.write( '\ndef print_res(Task, Penal, f__f):\n' )                            #  print_res
        f.write( '\n    Gr = Task.Gr' )
        for nf, fu in enumerate( Task.Funs ) :
            if obj.find(fu.V.name) >= 0 :
                wr( '\n    '+fu.V.name+ ' = ' + 'Task.Funs[' + str(nf) + ']' )    #  f__p = Gr.F[1]
        f.write ( '\n\n    OBJ_ = Gr.OBJ ()' )
 #       f.write ( '\n    print  \'    OBJ =\', OBJ_' )
  #      f.write ( '\n    print >> f__f,  \'\\n    OBJ =\', OBJ_\n' )
        f.write('\n    print (  \'    OBJ =\', OBJ_ )')
        f.write('\n    f__f.write ( \'\\n    OBJ =\'+ str(OBJ_)+\'\\n\')\n')
#        obj_parts = obj.replace(' ', '').split('+')   ##############    ' '->'' !!!!!!!
 #       if len (obj_parts) > 1 :
  #        for p in obj_parts :                              #  OBJ по частям  by parts

        from_ = 0;  to_ = 0                                 #  OBJ по частям  by parts
        for itn, it in enumerate(eqPars.items) :
          if it.part == '+' and it.lev == 0 or itn == len(eqPars.items)-1 :     # + or last element
            if itn == 0 :                                               # певый +
              from_ = 1
              continue
            if it.part == '+' :  to_ = itn-1
            else              :  to_ = itn                              # last
            if from_ <= 1  and  to_ == itn : break                      # единственный элемент
            part = eqPars.join ( from_, to_+1 )
            p_mu = part.find('Gr.mu[')          # 29  OBJ:  Σ(i=0,20,(x.V.dat[i]-x(x.A[0].dat[i]+t_min))**2) / x.V.sigma2 + x.Complexity(Penal[0])
            if p_mu >= 0 :
                p_mu_end = part.find(']', p_mu)
                repl = part[p_mu:p_mu_end+1]
                print (repl)
                part = part.replace(repl,repl+'()')
                print (part)
  #              1/0

#            if p == ' ': continue     # если нет штрафа
            f.write( '    tmp = (' + part + ')\n' )   # 29
            f.write( '    stmp = str(tmp)\n')
#            f.write( '    print       \'    \',int(tmp/OBJ_*1000)/10,\'\\t' + part + ' =\', tmp\n' )
 #           f.write( '    print >> f__f, \'    \',int(tmp/OBJ_*1000)/10,\'\\t' + part + ' =\', tmp\n' )
            f.write( '    print (      \'    \',int(tmp/OBJ_*1000)/10,\'\\t' + part + ' =\', stmp )\n' )
            f.write( '    f__f.write ( \'    \'+str(int(tmp/OBJ_*1000)/10)+\'\\t' + part + ' =\'+ stmp+\'\\n\')\n' )
#            f.write( '    print       \'    \',int(tmp/Gr.OBJ()*1000)/10,\'\\t' + p + ' =\', tmp\n' )
 #           f.write( '    print >> f, \'    \',int(tmp/Gr.OBJ()*1000)/10,\'\\t' + p + ' =\', tmp\n' )
            from_ = to_ + 2
        f.write( '\n    return\n' )
        print ('Model was built')
        if  Q.upper() == 'OBJ:' :
#            SvF.ModelFile.close()
 #           SvF.ModelFile = 1    #  >> Null
            WrStart27()


def WrStart27 () :
    SvF.ModelFile.close()
    SvF.ModelFile = 1  # >> Null

    with open('Model.py', 'r') as mf:
        lines = mf.readlines()
        for nl, l in enumerate(lines):
            if nl > 0: Swrs(l)
    Swr('\nSvF.Task.createGr  = createGr')
    Swr('\nSvF.Task.print_res = print_res')
    Swr('\nSvF.lenPenalty = ' + str(SvF.lenPenalty))
    Swr('\nfrom SvFstart62 import SvFstart19')
    Swr('\nSvFstart19 ( Task )')  # 27   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def WriteModelOBJ_U (buf) :
        wr ('\ndef OBJ_U (Task):\n')
        for fu in range ( len( SvF.Task.Funs ) ) :
            wr( '    '+SvF.Task.Funs[fu].V.name+ ' = ' + 'Task.Funs[' + str(fu) + ']' )    #  f__p = Gr.F[1]
        wr ('    return '+buf)
        wr ('SvF.Task.OBJ_U = OBJ_U')
#        SvF.ModelFile.close()
 #       SvF.ModelFile = 1  # >> Null
        WrStart27()



