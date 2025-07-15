# -*- coding: UTF-8 -*-

from   ModelFiles import *
from Table import *

def splitByEq (buf ):
    buf_sp = buf.split('=')
    if len (buf_sp) == 1:  return buf_sp[0], None
    else:                  return buf_sp[0], buf_sp[1]


def WriteCV(buf):
            arg = ','.join(buf.split(';'))
            Swr('CVmakeSets ( ' + arg + ' )')
#            Swr('make_CV_Sets ( ' + arg + ' )')
            SvF.numCV += 1
            wr('\n    if len (SvF.CV_NoRs) > 0 :')  # 23.11
            wr('        Gr.mu'+str(SvF.numCV)+' = py.Param ( range(SvF.CV_NoRs['+str(SvF.numCV)+']), mutable=True, initialize = 1 )')   #  23.11


def WritePenalty ( buf ):       # Penalty:   [Inf.Period, Imm.Period]=0.999; RR=7;    SvF.resF = None
        def wrOptName (on) :
            if on[1] == '' :           #  нет присвоения
                Swr('try: ' + on[0])
                Swr('except NameError: ' + on[0] + ' = None')
            else :
                Swr(on[0] + ' = ' + on[1] )
            wr('    ' + on[0] + ' = Penal[' + str(on[2]) + ']')
        #        print ( 'b', buf )
        OptParLen = -1
        if len(SvF.OptNames) > 0: OptParLen = SvF.OptNames[-1][2]       #  если несколько строк   Penalty:
        for s in buf.split (';') :
 #           print ('s', s)
            if len(s) == 0: continue
            if s.find ('SvF.resF') == 0:  Swr(s)
            else :
                ss = s.split('=')
                if len (ss)==1: ss.append('')
                OptParLen += 1

                ss.append (OptParLen)
                if ss[0][0] == '[' :                   #   [Inf.Period, Imm.Period]=0.999
                    for pss in ss[0][1:-1].split(',') :
  #                      print ("pss", pss)
                        opt_name = [pss, ss[1], ss[2]]
                        SvF.OptNames.append(opt_name)
                        wrOptName(SvF.OptNames[-1])
                else :
                    SvF.OptNames.append(ss)
                    wrOptName(SvF.OptNames[-1])
                Swr ( 'SvF.Penalty.append('+SvF.OptNames[-1][0]+')' )
   #     print (SvF.OptNames)
        return


def Sets_add ( all_Sets, from_ ) :    # пополняет из from_,  если уже нет в  all_Sets
        for g in from_:                                           
            if findSetByName ( all_Sets, g.name) == None :       # если еще нет
                    all_Sets.append(g)
        return all_Sets


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
#    print (leftName,'!', Fields, '!',FileName,'!', AsName, '!',where )
    WriteSelectTable(leftName, Fields, FileName, AsName, where)
    return



def WriteSelect30(buf):  ##  разбор  Select
    print (buf)
    leftName, Fields, FileName, AsName, where = ParseSelect30 ( buf )
    WriteSelectTable( leftName, Fields, FileName, AsName, where )
    return

def WriteSetString30(g):
        if g.className == 'Set':
            if is_nan(g.min):   g.min = 'SvF.curentTabl.dat(\'' + g.fld_name + '\')[:].min()'
            if is_nan(g.max):   g.max = 'SvF.curentTabl.dat(\'' + g.fld_name + '\')[:].max()'
            if is_nan(g.step):  g.step = SvF.Default_step  #-50
#            ret = 'Set(\'' + g.name + '\',' + str(g.min) + ',' + str(g.max) + ',' + str(g.step) + ',\'' + g.ind + '\',\'' + g.oname + '\')'
            ret = 'Set(\'' + g.name + '\',' + str(g.min) + ',' + str(g.max) + ',' + str(g.step) + ',\'' + g.ind + '\''')'
        else:
            ret = 'Domain (\'' + g.name + '\',' + g.A[0].name + ',' + str(g.visX)
            if g.dim == 1:
                ret = ret +')'
            else:
                ret = ret + ',' + g.A[1].name + ',' + str(g.visY) + ')'
 #       print (ret)
        return ret


def WriteSet27 ( buf ):
            if buf == '': return
            print ('buf',buf)
            g = getSet26(buf, SvF.Task.Sets)
            print (g)
            if g is None : return None
#            print ('WWWWWWWWWWW', buf, g.className )
            str = g.name + '=' + WriteSetString30(g)
            Swr(str)
            return g

def WriteDomain_24_12(buf):
    buf = buf.replace(' ','')    #  пробел после  '\\inn'
    if buf == '': return
    print('buf', buf)
    buf_sp = buf.split ('=')
    if len(buf_sp) < 2: buf_sp = buf.split ('\\inn')
    if len(buf_sp) < 2: print ('No ='); exit (-1)
    name = buf_sp[0]
    print (buf)
    a1 = '';   a2 = '';   a3 = '';    a4 = ''
    buff = '='.join (buf_sp[1:])                    #  могут быть и другие =
    for part in buff.split(';') :
        if '(' in part:  # (   )
        #    pars = parser(part)
            args = parser(part).Args(0)  # here  '['
            print(args)
            for i,a in enumerate (args) :
                if i == 0:  a1 = a
                if i == 1:  a2 = a
                if i == 2:  a3 = a
                if i == 3:  a4 = a
    Swr(name + ' = Domain(\'' + name +'\','+a1+','+a2+','+a3+','+a4+')')
    Domain (name,a1,a2,a3,a4)



def WriteSet_24_12(buf):        #  в память и в файл
    buf = buf.replace(' ','')    #  пробел после  '\\inn'
    if buf == '': return
    print('buf', buf)
    buf_sp = buf.split ('=')
    if len(buf_sp) < 2: buf_sp = buf.split ('\\inn')
    if len(buf_sp) < 2: print ('No ='); exit (-1)
    name = buf_sp[0]
    step = '-50'
    ind = ''
    Data = '\''+ name + '\''
    mi = ''
    ma = ''

    buff = '='.join (buf_sp[1:])                    #  могут быть и другие =
    for parts in buff.split(';') :
       if '[' in parts :             #  [   ]
           set = parts
           pars = parser(set)
     #      pars.myprint()
           args = pars.Args(0)   # here  '['
           print (args)

           mi = args[0]
           ma = args[1]

           if  len(args) > 2 :
               if args[2] != '': step = args[2]
           if  len(args) > 3 :
               if args[3] != '': ind = args[3]
           if  len(args) > 4 :
               if args[4] != '': Data = args[4]
       elif ('Data' in parts) : Data = parts.split('=')[1]
       elif ('Index' in parts) : ind = parts.split('=')[1]

    if mi == '':
        if '.' in Data : mi =  Data + '[:].min()'
        else           : mi = 'SvF.curentTabl.dat(' + Data + ')[:].min()'
    if ma == '':
        if '.' in Data : ma =  Data + '[:].max()'
        else           : ma = 'SvF.curentTabl.dat(' + Data + ')[:].max()'
    ind = ind.strip ('\'')                                              #   'i' -> i
    Swr(name + ' = Set(\'' + name +'\','+mi+','+ma+','+step+',\''+ind+'\','+Data+')')
    Set (name,mi,ma,step,ind,Data)    #  нужен индекс при формир StartModel
    return




import sympy as sy
#from itertools import combinations_with_replacement


def make_Polynome (smbF, fun) :             #  Polynome (6, c, X, V) ####################
    degr = 5
    coef = 'c_' + fun.name
    args = [a for a in fun.A]

    beg = smbF.find('Polynome')
    if len(smbF)>=beg+9 and smbF[beg+8] == '(' :        #  Polynome (
        end = smbF.find(')', beg)
        parts = smbF[beg+9:end].split(',')
#        print (parts)
        for ip,p in enumerate (parts):
            if   ip==0:
                if p!='': degr = int(p)                 #  Polynome ()
            elif ip==1: coef = p
            else:       args = [a for a in parts[2:]]
    else :                                              #  Polynome
        end = beg + 8

    def find_combinations(N, S):
        result = []

        def backtrack(current, remaining, depth):
            if depth == N:
                if remaining == 0:
                    result.append(current[:])
                return
            for i in range(remaining + 1):
                current.append(i)
                backtrack(current, remaining - i, depth + 1)
                current.pop()

        backtrack([], S, 0)
        return result

    pol = ''
    coef_num = 0
    for d in range(degr + 1):
        for comb in find_combinations(len(args), d):
            if pol !='': pol += '+'
            pol += coef + '[' + str(coef_num) + ']'
            coef_num += 1
            for iarg, arg in enumerate(comb) :
                if   arg >= 2: pol += '*' + args[iarg] + '**' + str(arg)
                elif arg == 1: pol += '*' + args[iarg]
        print (pol)
#        print (find_combinations(len(args), d))
 #   1/0



 #   pol = ''
  #  for p in range (degr+1) :
   #     if p >= 1: pol += '+'
    #    pol += coef + '[' + str(p) + ']'
     #   if p >=1: pol += '*'+args[0]+'**' + str(p)
  #  print (pol)

    print (smbF[0:beg]+pol+smbF[end+1:])
    if getFun (coef) is None :         #  coef  is not defined
        WriteVarParam26 ( coef + '[' + str(coef_num) + ']' , False)
        to_logOut('Var:  ' + coef + '[' + str(coef_num) + '] was added')
#        WriteVarParam26 ( coef + '[' + str(degr+1) + ']' , False)
 #       to_logOut('Var:  ' + coef + '[' + str(degr+1) + '] was added')

    return smbF[0:beg]+pol+smbF[end+1:]




def make_Fourier (smbF, fun) :        # Fourier (t, 5, T, c)
    pars = parser(smbF)
#    pars.myprint()
    i_pol = pars.find_part('Fourier')
#    print (i_pol)
    lenAgs = len (pars.items[i_pol+1].etc)-1
    if lenAgs >=1 \
       and pars.items[i_pol+1].etc[1] - pars.items[i_pol+1].etc[0] == 2:       #  ( 5 ...
            ncoef = int ( pars.items[i_pol+2].part )
    else :          ncoef = 5                                                    #  ( )  -> (8)
    if lenAgs >=2 : ω = pars.items[i_pol+4].part                #  ω
    else :          ω = 'ω_' + fun.name
    if lenAgs >=3 : coef = pars.items[i_pol+6].part             #  c
    else :          coef = 'c_' + fun.name
    if lenAgs >=4 : arg = pars.items[i_pol+8].part             # t     x,y ???
    else :          arg = fun.A[0]

#    ncoef = pars.items[i_pol+2].part            #   6
 #   ω = pars.items[i_pol+4].part             #  c
  #  coef = pars.items[i_pol+6].part             #  c
   # arg = pars.items[i_pol + 8].part  # 6
    pol = ''
    for p in range (int(ncoef)) :
        n = int((p+1)/2)
     #   print (p, n)
        if p >= 1: pol += '+'
        if   p == 0:    pol += coef +'[0]/2'
        elif p%2 == 1:  pol += coef +'['+str(p)+']*cos('+ ω +'*'+str(n)+'*'+arg+')'
        else :          pol += coef +'['+str(p)+']*sin('+ ω +'*'+str(n)+'*'+arg+')'
    print (pol)
    pars.items[i_pol].part = pol
    for i in pars.items[i_pol + 1:i_pol+lenAgs*2+2]: i.part = ''
#    for i in pars.items[i_pol + 1:i_pol+10]: i.part = ''  # убираем лишнее
    print ('JV',ω )
    if getFun (ω) is None :         #  coef  is not defined
        WriteVarParam26 ( ω , False)
        to_logOut('Var:  ' + ω  + ' was added')
    if getFun (coef) is None :         #  coef  is not defined
        WriteVarParam26 ( coef + '[' + str(ncoef) + ']' , False)
        to_logOut('Var:  ' + coef + '[' + str(ncoef) + '] was added')

#    print (pars.join())
    return  pars.join()

def make_smbFun(smbF, fun):
    print('make_smbFun', smbF);
    if smbF.find('Polynome') >= 0: smbF = make_Polynome (smbF, fun)
    if smbF.find('Fourier') >= 0:   smbF = make_Fourier (smbF, fun)
 #   1/0
    if fun.dim == 1:
        variables = sy.symbols(fun.A[0] + ',')
    else:
        variables = sy.symbols(fun.A[0] + ',' + fun.A[1])
    """"
    def gr_add_brack(txt):  # add  []  ДЛЯ ПО
        part = txt.split(Coeff_name)
        ret = part[0]
        for p in part[1:]:
 #           print (p)
            for i, char in enumerate(p):
                if not char.isdigit() :
                    ret += Coeff_name + '[' + p[:i] + ']' + p[i:]
                    break
                elif i == len(p) - 1 :
                    ret += Coeff_name + '[' + p + ']'
                    break
        return ret
    """
#
    smbF = smbF.replace('[', '(').replace(']', ')')  # Заменяем  []  ->  ()
    smbFx  = str(sy.diff(smbF,  variables[0])) + ' '   #   for  last gr7 ->gr[7]?
    smbFxx = str(sy.diff(smbFx, variables[0])) + ' '
    print('smbF  ', smbF)
    print('smbFx ', smbFx)
    print('smbFxx', smbFxx)
    smbFxx_2 = '('+smbFxx+')**2'
    print('smbFxx_2', smbFxx_2)
    if fun.Int_smbFxx_2 is None :
        Int_smbFxx_2 = str(sy.integrate(smbFxx_2, variables[0]))
        ######
    else :  Int_smbFxx_2 = None
    print('\nIntegral', Int_smbFxx_2)

    py_names = dir(py)
    def Write_def_smbFun(f_name, f_txt):
        if f_txt is None : return
        obj, eqPars, constraint_Sets, dif_minus, dif_plus = ParseEQUATION(f_txt, [])
        for fu in SvF.Task.Funs:
            if fu.dim != 0:
                eqPars.substAllNames_but_dot_plus(fu.V.name, SvF.funPrefix + fu.V.name)
            else:
                eqPars.substAllNames_but_dot_plus(fu.V.name, SvF.funPrefix + fu.V.name + '()')
        f_txt = eqPars.join()
        Swr('def ' + fun.name + '_' + f_name + '(Args) :')
        Swr('   ' + fun.A[0] + ' = Args[0]')
        if fun.dim == 2: Swr('   ' + fun.A[1] + ' = Args[1]')
        for f_nam in py_names: f_txt = f_txt.replace(f_nam,'py.'+f_nam)    #  добавляем к функциям py.
#        Swr('   return ' + gr_add_brack(f_txt))
        Swr('   return ' + f_txt)
        Swr(fun.name + '.' + f_name + ' = ' + fun.name + '_' + f_name + '')
#    obj, eqPars, constraint_Sets, dif_minus, dif_plus = ParseEQUATION(smbF, [])

    Write_def_smbFun('smbF', smbF)
    Write_def_smbFun('smbFx', smbFx)
    Write_def_smbFun('smbFxx', smbFxx)
    Write_def_smbFun('Int_smbFxx_2', Int_smbFxx_2)

    if fun.dim == 2:
        smbFy  = str(sy.diff(smbF,  variables[1])) + ' '
        smbFxy = str(sy.diff(smbFx, variables[1])) + ' '
        smbFyy = str(sy.diff(smbFy, variables[1])) + ' '
        print('smbFy',  smbFy)
        print('smbFxy', smbFxy)
        print('smbFyy', smbFyy)
        Write_def_smbFun('smbFy', smbFy)
        Write_def_smbFun('smbFxy', smbFxy)
        Write_def_smbFun('smbFyy', smbFyy)



def WriteVarParam26 ( buf, param ) :
        if buf == '':  return
        if SvF.printL:  print ('VarParam26:', buf, param)
        Task = SvF.Task
#        print('VarParam26:', buf, param)
        strInitBy = ''
        strFuncDomain = ''
        f_name = ''
        fun_args = []
        fun_args_str = ''       #  't,v'
        dim = 0
        dop_args = ''
        PolyPow  = -1
        Type     = ''
        Period   = ''
        Domain   = ''
        ReadFrom = ''
        Data     = ''
        smbFun   = ''
        f_type = 'g'
        Lbound = None
        Ubound = None
        Finitialize = '' #'0'
        AddGap = False

        fun = None
        parts = buf.split(';')
        p = -1                                              #  вставляем ';'
        if   parts[0].find(')<') > 0 : p=parts[0].find(')<')+1   #    X(t) <= 0
        elif parts[0].find(')>') > 0 : p=parts[0].find(')>')+1   #   X(t) >= 0
        elif parts[0].find(')=') > 0 : p=parts[0].find(')=')+1   # Param:  H(X,Y) = DEM_Kostica.asc
# ??        elif parts[0].find(')\\inn')>0: p=parts[0].find(')\\inn')+1   # Param:  H(X,Y) \\in [0,1]
        if p > 0 :
            parts[0] = parts[0][:p] + ';' + parts[0][p:]
 #           print('P0', parts[0])
            buf1 = ';'.join (parts)
            parts = buf1.split(';')

        for i, part in enumerate (parts) :
## 30                part = Task.substitudeDef ( part )
                part_blanck = part
                part = part.replace(' ','')
                if part == '' :   continue
                up_part = part.upper()
                print('PART:', part, up_part)
                pars = parser ( part )
         #       pars.myprint()
                print ('PART:', part )
        #        print ('PART1{:', pars.items[1].part )

                if i==0 :                                       #  Функция VAR:    x ( t, Degree=8 )
                    f_name = pars.items[0].part
                    if len (pars.items) > 1:
                        if pars.items[1].part == '[' :              #  tensor  dim > 0
                            f_type = 'tensor'
                    for a in pars.Args(1) :
                        if '=' in a :
                            dop_p = a.split('=')[0]
                            if dop_p == 'Degree' :
                                PolyPow = int(a.split('=')[1])
       #                         type = "p"
                                continue                            # not adding to  dop_arg
                            if dop_p == 'Type' :
                                Type = a.split('=')[1]
                                continue
                            dop_args += ',' + a
                        else :
                            fun_args.append (a)
                    fun_args_str = ','.join(fun_args)
                    dim = len (fun_args)
                    if dim == 0 :   f_type = 'tensor'
                    print (pars.Args(1), dop_args, fun_args, fun_args_str)
                    fun = Fun(pars.items[0].part ,fun_args, param, PolyPow )     # here  '('
                elif part.find('Degree')==0 :                        #  Функция VAR:    x ( t ); Degree=8
                            PolyPow = int(part.split('=')[1])
                            fun.PolyPow = PolyPow
                            fun.type = 'p'
                elif part.find('Type')==0 :
                            Type = part.split('=')[1]
                elif part.find('Period')==0 :
                            Period = part.split('=')[1]
                elif part.find('Domain') == 0:
                            Domain = part.split('=')[1]
                elif part.find('Data')==0 :
                            Data = part
                elif part[0] == '=' :
                            smbFun = part[1:]
                elif part.find('Int_smbFxx_2=False') == 0:
                            fun.Int_smbFxx_2 = ''
        #        elif part.find('Coeff')==0 :
         #                   Coeff = part.split('=')[1][1:-1]      #  убираем кавычки
      #          elif part.find('Fun')==0 :
       #                     smbFun = part.split('=')[1][1:-1]
                elif part.find('Finitialize=') == 0:   # Param:  H(X,Y) = DEM_Kostica.asc?   or H(X,Y) = 1
                            Finitialize = part.split('=')[1]
#                elif part[0] == '=' :             # Param:  H(X,Y) = DEM_Kostica.asc   or H(X,Y) = 1
 #                           Finitialize = part[1:]
                elif part.find('<<') == 0:
                        if len (part[2:]) > 0:
                            ReadFrom = part[2:]
                        else:
                            ReadFrom = fun.NameArds() + '.sol'
                        if ReadFrom[0] != '\'' and ReadFrom[0] != '\"' : ReadFrom = '\"' + ReadFrom + '\"'
                elif part.find('ReadFrom')==0 :
                            ReadFrom = part.split('=')[1]
                elif part.find('>') == 0:  # > 3
                        p = max(part.find('>'), part.find('>=') + 1)
                        Lbound = part[p + 1:]
                elif part.find('<') == 0:                                   # <6        # elif <  after  <<
                    p = max(part.find('<'), part.find('<=') + 1)
                    Ubound = part[p + 1:]
                elif part.find('ReadFrom')==0 :
                            ReadFrom = part.split('=')[1]
                elif part.find('\\inn') > 0:
                        args, SetOrDom = part.split('\\inn')
                        print (args, SetOrDom);
                        g = findSetByName ( Task.Sets,SetOrDom )  #getSet26(SetOrDom, Task.Sets)
                #        print (g.name)
                        if args == fun_args_str and g is None:  Domain = SetOrDom   # Q,VPD ∈ QV - Domain
                        elif args in fun_args and isnotNone (g) :                 # t ∈ T  - Set
                            num_arg = fun_args.index(args)
                            fun_args[num_arg] = SetOrDom
                            fun_args_str = ','.join(fun_args)
                        else:
                            print('**************** Cant understand :', part)
                            exit(-1)

                #                elif getSet26 ( pars, Task.Sets ) != None :   #  Грид
 #                       gr = SvF.LastSet
  #                      print('PART1:', part,  gr.name, gr.className)
                #        1/0
   #                     if SvF.printL:  print ('gr.name:', gr.name, gr.className)
    #                    if gr.name == '__No__Name__' : gr.name = fun.V.name
     #                   if gr.name == fun.V.name :              #  bounds     for x(t)    x ∈ [ -10.,10 ];
      #                      Lbound = gr.min
       #                     Ubound = gr.max
        #                    if SvF.printL:  print ('LG:', Lbound)                         #   Polynome  не проверено !!!!!!!!!!!!!!!!!!!!!!!!!!
         #                   if SvF.printL:  print ('UG:', Ubound)
          #              else :
           #                 if gr.className == 'Domain' :    #  PHqt  ( Q, T );  Q,T ∈ QT;
            #                    fun.domain = gr
             #                   args = part.split('\\in')[0].split(',')
              #               #   print (args)
               #              #   1/0
                #                for ia,a in enumerate(fun.A) :
                 #                   gri = Set (findSetByName ( Task.Sets, gr.A[args.index(a)].name ))
                  #                  gri.name = a
                   #                 fun.A[ia] = gri
                    #            continue
                     #       for ia, a in enumerate(fun.A):
                      #          if SvF.printL:  print ('Arg:', a, type(a), type('abc'),)
                       #         if type(a) != type('abc') : continue
#                       #         print gr.name, a
                         #       if gr.name == a :
#                                    fun.A[ia] = Set (gr)
                          #          fun.A[ia] = (gr)
#                                    fun.A[ia] = Arg (gr)
                           #         if SvF.printL: print ('ArgName:', fun.A[ia].name)
                            #        break
                  #          else:
                   #                 print ('********  NO USE FOR ARG GRID ', gr.name, '*********************')
                    #                exit(-1)

#                elif part.find('\\in')==0 :
 #                           p = max (part.find('>'), part.find('>=')+1)
  #                          Lbound = getfloat(part[p+1:])
   #                         if SvF.printL:  print ('Lbound=', Lbound)

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
#                elif part.find (fun.V.name+'=') ==0 \
 #                 or part.find (fun.V.name+'('+fun_args_str+')=') ==0 :   #  smbFun !!!!!!!!!!!!!!!!!!!!!!!
  #                  smbFun = part.split('=')[1]
                    #############################################################   ПРАВИТЬ !!!!!!!!!!!
                elif part.find (fun.V.name) >=0:    #  Нужно искать  ИМЯ а не подстроку !!!!!!!!!!!!!!!!!!!!!!!
                    parts[i] = 'EQ:' + part
                    if SvF.printL:  print ('treated as EQ:',  parts[i])
                else :
                    print ('**************** Cant understand :', part)
                    exit (-1)

        if f_type != 'tensor' :
            for a in fun_args:          #  проверяем Аргументы
                if findSetByName ( Task.Sets,a ) is None:
                    WriteSet_24_12(a + '=[,,]')   #WriteGrid27 ( a + '=[,,]')              #    Дописываем  Set

        if f_type != 'tensor' :
          if dim == 1 and type(fun.A[0]) is str :        # Domain  <class 'str'>
            if not findSetByName ( Task.Sets,fun.A[0] ) is None:
#                print 'LL'
                gr = SvF.LastSet
 #               print '2', gr.name
                if gr.className == 'Domain':  # PHqt  ( QT );
                    fun.domain = gr
                    fun.A[0] = Set(gr.A[0])
                    if len (gr.A) == 2:
                        fun.A.append (Set(gr.A[1]))
                        fun.dim = 2


#        if FromFile != '' :                 #
 #           st = f_name +' = FunFromFileNew (\'' +FromFile + '\',1,True).Rename (\''+fun.V.name+'\','+fun_args_str +')'
  #          Swr ( st )
   #     else :
    #      f_str = 'Fun(\''+f_name+'\',['+ fun_args_str + ']'       #    write  into the  StartModel

        #if dim == 0 :  f_str = 'Tensor(\''+f_name+'\',['+ fun_args_str + ']'
        #else :
        if  f_type == 'tensor':   f_str = 'Tensor(\'' + f_name + '\',[' + fun_args_str + ']'
        else :                  f_str = 'Fun(\''+f_name+'\',['+ fun_args_str + ']'       #    write  into the  StartModel

        if param == True : f_str += ', param='  + str(param)                #  добавление аргументов
        if PolyPow  != -1 and not ('Degree' in dop_args):   f_str += ', Degree='   + str(PolyPow)
        if Type     != '' and Type != 'Cycle' and not ('Type' in dop_args):     f_str += ', Type=\''   + Type+ '\''
        if Period   != '' and not ('Period' in dop_args):   f_str += ', Period='   + Period
        if Domain   != '' and not ('Domain' in dop_args):   f_str += ', Domain='   + Domain
        if ReadFrom != '' and not ('ReadFrom' in dop_args): f_str += ', ReadFrom=' + ReadFrom
        if Data     != '' and not ('Data'     in dop_args): f_str += ', ' + Data
        if Finitialize != '' and not ('Finitialize' in dop_args): f_str += ', Finitialize=' + Finitialize
#       if smbFun != '' :  f_str += ', smbFun=\''+smbFun+'\', Coeff=\''+Coeff+'\''
        if dop_args != '' : f_str += dop_args
        f_str += ')'

        if   Type == 'Cycle' :    Swr (f_name+' = Cycle' + f_str)
        elif Type == 'SPWLi' or Type == 'SPWL' : Swr (f_name+' = SPWL' + f_str)
        elif smbFun != '' :     Swr (f_name+' = smb'+f_str)
        elif PolyPow < 0  :     Swr (f_name+' = '+f_str)
        else :                  Swr (f_name+' = p'+f_str)                                  #  pFun

        if AddGap :   Swr ( f_name+'.AddGap( )'); #AddGap=False

        #if dim == 0:      Swr(f_name + '.grd = ' + Finitialize)

        if f_type == 'tensor' :
            if   dim==1 : fun_args_str = 'i'
            elif dim==2 : fun_args_str = 'i,j'

        def_part = 'def ' + SvF.funPrefix + f_name + '(' + fun_args_str + ') : '    # def fE (t) : return E.F([t])
        ret_part = 'return ' + f_name + '.F([' + fun_args_str + '])'
        Swr(def_part + ret_part)

        if smbFun != '':
            #            print (smbFun, Coeff)
            make_smbFun(smbFun, fun)
#            1 / 0
        #       if fun.PolyPow >=0 :
  #          make_smbF(fun)                          ############  24.11
        #       if fun.PolyPow >=0:     fun = pFun(fun)
 #       SvF.ReadFrom = ''
## 30        Task.AddFun ( fun )
        Task.Funs[-1].Oprint()

 #       if Finitialize == '': Finitialize = '1'   #  ????????????
        if not param:  # Param
            if PolyPow >= 0:  # Poly
                wr('\n    ' + f_name + '.var = py.Var ( range (' + f_name + '.sizeP' + ') )' ) #, initialize =  ' + Finitialize + ')') # ?? Finitialize copy from grd
                wr('    Gr.' + f_name + ' =  ' + f_name + '.var')
            else:  # Set
  ##              if not fun.param:  # Var
                    wr('\n    ' + f_name + '.var = py.Var ( ')
                    for di in range(dim):
                        if f_type == 'tensor':
                            wrs('range (' + f_name + '.Sizes[' + str(di) + ']),')

                        else :
                            wrs(f_name + '.A[' + str(di) + '].NodS,')
                    #                      wrs ( 'domain='+str(fun.domain_)+',' )
                    wrs('domain=Reals')
      #              wrs('domain=complex,')
                    if not (Lbound is None and Ubound is None):
                        wrs(', bounds=(' + str(Lbound) + ',' + str(Ubound) + ')')
                    wrs(' )')
#                    wrs(' initialize = ' + Finitialize + ' )')
                    wr('    Gr.' + f_name + ' =  ' + f_name + '.var')

 #24           if PolyPow < 0:  # Set
    #            wr('    ' + f_name + '.InitByData()')
#            if not fun.neNDT is None:  # 27
            if  Domain != '':  # 2412
                    wr('    ' + f_name + '.Fix()')
            if  Type == 'Cycle' :
                if Period == '' :
                    WriteModelEQ31( f_name + '.var[0] = '  + f_name + '.var['+f_name+'.A[0].Ub]' )
                else :
                    WriteModelEQ31(f_name + '.var[0] = ' + SvF.funPrefix + f_name + '(' + f_name + '.Period)' )
#                    WriteModelEQ31(f_name + '.var[0] = ' + SvF.funPrefix + f_name + '(' + Period + ')' )
#                wr('    ' + f_name + '.var[0] = ' + f_name + '.var[' + f_name + '.A[0].Ub]')

            #      if isnotNone(fun.domain):  # 27
       #         wr('    ' + f_name + '.Fix()')

            if SvF.numCV >= 0:
                wr('    ' + f_name + '.mu = Gr.mu' + str(SvF.numCV) + ';')
     #24       if PolyPow >= 0 :  # Poly
        #        wr('    ' + f_name + '.var[0].value = ' + Finitialize)
        # EQ:
            if PolyPow >= 0:  # Poly
                if not Lbound is None:      WriteModelEQ31(f_name+'('+fun_args_str + ')>=' + str(Lbound))
                if not Ubound is None:      WriteModelEQ31(f_name+'('+fun_args_str + ')<=' + str(Ubound))



            for part in parts:
                if part.find('EQ:') == 0:    WriteModelEQ31(part[3:])


""""
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
"""
#        if not SvF.MakeModel : return
"""""
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
                  wr ( '\n    ' + f_name + '.var = py.Var ( range (' + f_name +'.sizeP' + '), initialize = 0 )' )
                  wr('    Gr.' + f_name + ' =  ' + f_name + '.var')
            else :            # Set
                  if not d.param :                                                 # Var
                      wr ( '\n    ' + f_name + '.var = py.Var ( ' )
                      for di in range (d.dim) :
                          wrs ( f_name+'.A['+str(di)+'].NodS,' )
#                      wrs ( 'domain='+str(d.domain_)+',' )
                      wrs ( 'domain=Reals,' )
                      if not (Lbound is None and Ubound is None):
                          wrs ( ' bounds=('+str(Lbound)+','+str(Ubound)+'),')
                      wrs ( ' initialize = '+Finitialize+' )' )
                      wr ( '    Gr.'+f_name+' =  ' + f_name + '.var' )

            if d.PolyPow < 0:   # Set
                      wr( '    '+f_name+'.InitByData()' )
 
        if not d.param:
          if SvF.numCV >= 0:
            wr('    ' + f_name + '.mu = Gr.mu'+str(SvF.numCV)+';')
        if d.PolyPow >= 0 and not d.param:   # Poly
            wr ( '    ' + f_name + '.var[0].value = ' + Finitialize )
# EQ:
        if d.PolyPow >= 0:   # Poly
            if not Lbound is None :
                WriteModelEQ31 ( parts[0] + '>=' + str(Lbound)  )
            if not Ubound is None :
                WriteModelEQ31 ( parts[0] + '<=' + str(Ubound)  )
                
        for part in parts :
            if part.find('EQ:') == 0:    WriteModelEQ31 ( part[3:] )
"""

def fromTEXplus(equation) :
    equation = equation.replace('  ',' ')
    equation = equation.replace(' _','_')     #  нижний предел интеграла
    print ('TEXsubst', equation)
  #  if SvF.UseHomeforPower :    equation = UTF8replace(equation, '^', '**')
   # else :                      equation = UTF8replace(equation, '^', '')
    sel = parser(equation)
    sel.myprint()
    repars = True
    def del_figure (sel, pos):                      #  удаляет фигурные скобки
        if  sel.items[pos].part != '{' :  return pos
        sel.items[pos].part = ''                    # {  ->  ''
        sel.items[sel.items[pos].etc[1]].part = ''  # }  ->  ''
        return  sel.items[pos].etc[1]

    while (repars) :
        equation = sel.join()
        sel = parser(equation)
        repars = False
        for itn, it in enumerate(sel.items) :
            print ('itn=', itn)
            if it.type == 'name' or it.type == 'fun' :
                if it.part == '\\frac' :                    #  \frac{d}{dro}(Df) = Pdf
#                    repars = True
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
                    repars = True
                    break
                if it.part.find ('\\int_') == 0 :        # INTEGRAL  запись  ∫_{0}^{rp}{d(x)*expr} -> ∫(0,rp,d(x)*expr)
#                    repars = True
                    print(it.part)
                    it.part = it.part.replace('_','(',1)               #   _ -> )
                    if len (it.part) > 5:               #   ∫_0^{rp}{d(x)*expr}
                        print (it.part)
                        pos = itn
                    else :                              # {lim_min}  in   int_{lim_min}
                        pos_min = itn+1
                        pos = del_figure(sel, itn+1)
                        if pos == itn+1 :
                            print ('Не хватает {    ', sel.myprint() )
                            exit (33)
                        pos += 1
                        print ('KKK',sel.join())

                    if sel.items[pos].part == '^' :      #      ^{rp}
                        sel.items[pos].part = ','
                        pos = del_figure(sel, pos+1)
                        body_pos = pos+1
    #                    print('AA', sel.join())
                        pos = del_figure(sel, body_pos)               # { body }
#                        print (pos, body_pos)
                        if pos == body_pos :
                            print ('Не хватает {    ', sel.myprint() )
                            exit (33)
                        sel.items[body_pos].part = ','
                        sel.items[pos].part = ')'
                    else :
                        sel.items[pos-1].part = ','
                        pos_in = sel.find_part('\inn',pos_min)
                        print (sel.items[pos_in].part)
                        d_name = 'd' + sel.items[pos_in-1].part
                        pos_d_name = sel.find_part(d_name, pos_in)
                        sel.items[pos_d_name].part = ')'
                        if sel.items[pos_d_name-1].part == '*' : sel.items[pos_d_name-1].part = ''
                    print ('BB',sel.join())
 #                   1/0
#                        if sel.items[itn+1].part == '{' :
 #                       print(it.part, '{')
  #                      sel.items[itn+1].part = ''                      #  {  ->  ''
   #                     sel.items[sel.items[itn+1].etc[1]].part = ''    #  }  ->  ''
    #                    pos = sel.items[itn+1].etc[1]+1
     #               else :
##                    it.type = 'int'
         #           lim_min = it.part.split('_')[1]
          #          print ('lim_min|'+ lim_min+'|')
       #             1/0
#                    UTF8replace (it.part,'\\int_','\\int(')
   #                 print (it.part)
       #             it.part=it.part[0:4]+'('+lim_min
  #                  print(it.part)
    #                pos = itn+1
     #               if len (lim_min) == 0 :                     # {lim_min}  in   int_{lim_min}
      #                  sel.items[itn+1].part = ''
       #                 sel.items[sel.items[itn+1].etc[1]].part = ''
        #                pos = sel.items[itn+1].etc[1]+1
         #           print ('min', itn, sel.join())
#                    print (sel.items[pos].part)
 #                   1/0
  #                  sel.items[pos].part = ','
   #                 pos += 1                                    # lim_max
    #                if sel.items[pos].part == '{' :
     #                   sel.items[pos].part = ''
      #                  pos = sel.items[pos].etc[1]
       #                 sel.items[pos].part = ''
        #            sel.items[pos].part += ','
         #           print (itn, sel.join())
          #          pos += 1                                    # { body }
           #         sel.items[pos].part = ''
            #        pos = sel.items[pos].etc[1]
             #       sel.items[pos].part = ')'
                    repars = True
                    break

                if it.part.find('\\sum_') == 0:  # SUMMA  запись  ∫_{0}^{rp}{d(x)*expr} -> ∫(0,rp,d(x)*expr)
#                    repars = True
                    it.type = 'sum'
#                    print ('it.partTT', it.part, itn, sel.items[itn].part)
                    lim_min = it.part.split('_')[1]
 #                   print('lim_min |'+ lim_min+'|')
                    #                    UTF8replace (it.part,'\\int_','\\int(')
                    #                 print (it.part)
                    it.part = it.part[0:4] + '(' + lim_min
                    #                  print(it.part)
                    pos = itn + 1
  #                  print('it.part', it.part, sel.items[itn].part, sel.items[itn + 1].part, sel.items[itn + 2].part)
                    if len(lim_min) == 0:  # {lim_min}  in   int_{lim_min}
   #                     print (sel.items[itn + 1].part)
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
                    repars = True
                    break

    #                if repars :
 #                   equation = sel.join()
  #                  sel = parser(equation)
   #                 break

#    print ('@@@@@@@@@@@@', equation, SvF.UseHomeforPower)
    if SvF.UseHomeforPower:
        equation = UTF8replace(equation, '^', '**')
    else:
        equation = UTF8replace(equation, '^', '')
    sel = parser(equation)


    if SvF.UsePrime and equation.find("'") >= 0:     #   G' > 0
        for ip in range(len(sel.items) - 1):
            if sel.items[ip].part == "'" :
#                print (sel.items[ip-1].part,sel.items[ip-1].type, sel.items[ip].part,sel.items[ip].type )
                fname = sel.items[ip-1].part
                f= getFun(fname)
 #               print (f.name)
                if (len(f.A)) > 1:
                    print ('Only for one argument')
                    exit (-1)
                sel.items[ip - 1].part = 'd/d'+f.A[0]+'('+ fname +')'
                sel.items[ip].part = ""
        equation = sel.join()
        sel = parser(equation)
    print ('>>>', equation)
   # 1/0

                            #    d/dt(Vac(t))  ->  \d(t,Vac(t))
    if equation.find ('d/d') >= 0 :
      for ip in range(len(sel.items) - 3):
        if sel.items[ip].part == 'd' and sel.items[ip + 1].part == '/' and sel.items[ip + 2].part[0] == 'd':
            sel.items[ip].part = '\d'
            sel.items[ip + 1].part = '('
            sel.items[ip + 2].part = sel.items[ip + 2].part[1:]
            sel.items[ip + 3].part = ','
      equation = sel.join()
      sel = parser(equation)

    if equation.find ('d2/d') >= 0 :            #  \d2t2(x(t))  ->  \d2(t,x(t))
      for ip in range(len(sel.items) - 3):
        if sel.items[ip].part == 'd2' and sel.items[ip + 1].part == '/' and sel.items[ip + 2].part[0] == 'd':
            sel.items[ip].part = '\d2'          #  'd2' -> '\d2'
            sel.items[ip + 1].part = '('
            sel.items[ip + 2].part = sel.items[ip + 2].part[1:-1]       # dt2 ->  t
            sel.items[ip + 3].part = ','
      equation = sel.join()
#      print (equation)
 #     1/0
#      sel = parser(equation)

#    if SvF.UseHomeforPower :    equation = UTF8replace(equation, '^', '**')
 #   else :                      equation = UTF8replace(equation, '^', '')
    return equation


def ParseEQUATION ( equation, all_Sets, Mode = 'EQ' ) :
        Task = SvF.Task
        Funs = Task.Funs

        dif_minus = []                               # DERIV     (H2O((t+1.0))-H2O(t))/1.0==-E(t)*2.0736+WF*WD(t)
        dif_plus = []                               # DERIV 2

#        equation = fromTEXplus(equation)
        eqPars   = parser ( equation )
                                           #  Добавляем опущенные Аргументы
        if SvF.printL:  print ('ParseEQUATION'); eqPars.myprint()
        reparse = True
        while reparse :
          reparse = False
          quotes = 0
          for iit, it in enumerate(eqPars.items) :
            if it.part == '\'' or it.part == '\"':  quotes = 1 - quotes
            if quotes == 1: continue                    # в строках не работаем !
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

   #     print ('ALL_Sets B', len(all_Sets))
  #      for g in all_Sets : print (g.name)

 #       if Mode == 'EQ' :
        for g in Task.Sets:                                       # пополняем  all_Sets  из общих Гридов
            if findSetByName ( all_Sets, g.name) == None :       # если еще нет
                if eqPars.find_part_type_but_point( g.name, 'name' ) >= 0 :  # чтобы исключить   x.min   x.step  tab.t
                    all_Sets.append(g)

        eqPars.funs( all_Sets )                                        #  ... name -> Set
        dif_minus, dif_plus  = eqPars.dif1 ( dif_minus, dif_plus, all_Sets )
        dif_minus, dif_plus  = eqPars.dif2 ( dif_minus, dif_plus, all_Sets )
        eqPars.summa(all_Sets)
        print ('555', eqPars.join())
        integral_Sets = eqPars.integral( all_Sets )                  # лучше оставить последним - там всякие for и sum
        equation = eqPars.join()
        if SvF.printL : print ('END PARSE', equation)

        constraint_Sets=[]                         #  фигурируют в EQ  но не как  d(t)
        for g in all_Sets :
            if SvF.printL : print (g.name)
            if findSetByName ( integral_Sets, g.name) == None :            #
                constraint_Sets.append(g)

        return  equation, eqPars, constraint_Sets, dif_minus, dif_plus



def ParseEQplus31 ( buf, Mode = 'EQ' ):
    Task = SvF.Task
 #   print('BB2:', buf)
    buf = buf.rstrip()
    if buf == '': return
    if buf[-1] == ';' : buf = buf[:-1]          # Убираем последний ;

    buf = fromTEXplus(buf)

    all_Sets = []  # local (заданные в EQ  после ; and global Sets    explicit
    explicit_Sets =[]  # explicit Sets  for String

    if buf.find('\\inn') < 0 :
        equation = buf
    else :
        parts = buf.split(';')  # ; отделяет Гриды and conditions
        parts = list(filter(('').__ne__, parts))  # удаляет пустые элементы ''
        if SvF.printL:  print(parts)

        equation = parts[0]  # первая часть !

        for part_blanc in parts[1:]:  # Omi(t)  = nC3(t) / nC(t) * 100.   ; t \in tu3
            part = part_blanc.replace(' ', '')
            p = part.find('\\inn')
            if p >= 0:
                Set_n = part[p + 4:]
            else: break                         #
            ind_n = part[:p]
            gr = findSetByName(Task.Sets, Set_n)
            #            print (':', part, p, ind_n, Set_n)
            if gr is None:
                Set_n = '_g' + str(SvF._Num);  SvF._Num += 1  # новое имя грида   _g0
                part = Set_n + part[p:]
                gr = WriteSet27(part)
                if gr is None:                                      #  t ∈ [0, tMax,  st, tt]
                    print('Can\'t treat  |' + part + '|  in  ' + buf)
                    exit(-1)
            all_Sets.append(gr)
            explicit_Sets.append(gr)
            eqPars = parser(equation)
            eqPars.substAllNames_but_dot(ind_n, Set_n)
            equation = eqPars.join()
#    print("EE", equation)

    equation, eqPars, constraint_Sets, dif_minus, dif_plus = ParseEQUATION(equation, all_Sets, Mode)

 #   print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE' + equation, len(all_Sets) )
    for g in constraint_Sets:
        eqPars.substAllNames_but_dot(g.name, g.ind)  ## 30g+
        eqPars.substAllNames(g.name + '__p', g.name)
 #       print('substAllNames', eqPars.join())
 #   eqPars.myprint()
    for fu in Task.Funs:
        if fu.dim != 0 :
            eqPars.substAllNames_but_dot_plus(fu.V.name, SvF.funPrefix + fu.V.name)
        else :
            eqPars.substAllNames_but_dot_plus(fu.V.name, SvF.funPrefix + fu.V.name + '()')

    equation = eqPars.join()
#    print('2EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE' + equation)
    if SvF.printL: print('EQAFTER', equation)
    return equation, constraint_Sets, dif_plus, dif_minus, explicit_Sets

eqNUM = 0

def WriteModelEQ31 ( buf ):
        if buf == '': return

        equation, constraint_Sets, dif_plus, dif_minus, explicit_Sets = ParseEQplus31(buf, 'EQ')
        b_if = ''                                                           # Constraint.Skip
        if equation[:3] == 'if ':
            colon = equation.split(':')
            if len(colon) > 1:
                 b_if = 'if not (' + colon[0][2:] + ') : '
                 equation = ''.join(colon[1:])

        for i, e in enumerate( equation ):      #    ,<   ->   <=
            if e in ['!', '=', '<', '>']:
                if equation[i+1] == '=' : break
    #            print ('BS', e, equation)
                equation = equation[:i+1]+ '=' + equation[i+1:]
     #           print ('AS', equation)
                break

        global eqNUM
        eqName = 'EQ'+str(eqNUM)
        eqNUM += 1

        if SvF.printL:  print (eqName)

        wr(' \t\t\t\t\t\t\t\t# '+buf )
        wr ( '    def '+eqName+' (Gr' )                   # def EQ*(Gr,t) :
        for g in constraint_Sets :
            wrs ( ','+g.ind )
        wrs ( ') :' )
#        if b_if != '' :  wr('        if not ('+b_if+') : return Constraint.Skip')         #  Constraint.Skip
        if b_if != '' :  wr('        ' + b_if + 'return py.Constraint.Skip')         #  Constraint.Skip
        wr('        return (')
        wr('          '+equation)
        wr('        )')
        wr('    Gr.con'+eqName+' = py.Constraint(')
        for ng, g in enumerate(constraint_Sets) :
            if SvF.printL:  g.Gprint()
            my_range = 'FlNodS'
            if g.name in dif_plus:  my_range  = 'm' + my_range
            if g.name in dif_minus: my_range  = my_range + 'm'
#            wrs ( g.name + '__p.' + my_range + ',')
            wrs(g.name + '.' + my_range + ',')
        wrs('rule='+eqName+' )')                                                    # rule=DifEQ )

        return


def WriteString31(buf):
    if buf == '': return
 #   print ('WriteString31________________', buf, SvF.Substitude, (not SvF.Substitude) )
    if SvF.Substitude == False :
        Swr( buf )
        return
    if buf[0] == ':' :
        Swr( buf[1:] )
        return


    for i, s in enumerate (buf) :                                   # НЕ ТИПИЧНЫЕ СТРОКИ
        if s!=' ' : break
#    print (i)
    if buf[i:].find('Draw ') == 0 :
        Swr(' '*i + 'Task.Draw ( \'' + buf[i+5:] + '\' )' );  return
    elif buf[i:].find('DrawErr') == 0:
        Swr(' ' * i + 'Task.DrawErr ()');   return
    elif buf[i:].find('DrawVar') == 0:
        Swr(' ' * i + 'Task.DrawVar ()');   return
    elif buf[i:].find('Draw') == 0:
        Swr(' ' * i + 'Task.Draw (\'\')');      return

    equation, constraint_Sets, dif_plus, dif_minus, explicit_Sets = ParseEQplus31(buf, 'String')
#    if equation.find('dayVac')>=0:     1/0
    equation = Treat_FieldNames(equation)
    eqPars = parser(equation)
#    eqPars.myprint()
    p_eq = eqPars.find_part_type('=', 'oper')
    if p_eq > 0:                                    # A_Immun(t9) = ∫_{m
        bracket_clo = p_eq - 1
        if eqPars.items[bracket_clo].part == ')':
            bracket_ope = eqPars.find_part_lev_back ( '(', eqPars.items[bracket_clo].lev, bracket_clo )
            p_fname = bracket_ope-1
            ffname = eqPars.items[p_fname].part
            pref_p = ffname.find(SvF.funPrefix)
            print (pref_p, ffname)
            fname = ffname [len(SvF.funPrefix):]
            print (fname)
            fun = getFun (fname)
            if not (fun is None) :
                part_plus = fname + '.grd'
                if fun.dim == 0:                  #  не понятно
                    pass
                elif (fun.type[0] == 'g') and fun.dim == 1:       # 2407
                    eqPars.items[p_fname].part = part_plus + '[' + fun.name + '.A[0].IndByVal ('
                    eqPars.items[bracket_ope].part = ''
                    eqPars.items[bracket_clo].part = ')]'

#            elif self.type == 'g' and self.dim == 2:
 #               x = (ArS_real[0] - self.A[0].min) / self.A[0].step
  #              y = (ArS_real[1] - self.A[1].min) / self.A[1].step
   #             return self.interpol(2, x, y)
    #        elif self.type == 'g' and self.dim == 3:
     #           x = (ArS_real[0] - self.A[0].min) / self.A[0].step
      #          y = (ArS_real[1] - self.A[1].min) / self.A[1].step
       #         z = (ArS_real[2] - self.A[2].min) / self.A[2].step
                else :
                    print ( "dim >= 2 not ready yet" );  exit(-1)
                equation = eqPars.join()
            eqPars.myprint()
            print (eqPars.join())       #   в езультатк   A_Immun.grd[A_Immun.A[0].indByVal (tt)]=sum (
 #           1/0

    level = 0                                   # уровень (сдвиг) в тексте
#    for ng, g in enumerate(constraint_Sets):

    for ng, g in enumerate(explicit_Sets):
        if SvF.printL:  g.Gprint()
        my_range = 'FlNodS'
        if g.name in dif_plus:  my_range = 'm' + my_range
        if g.name in dif_minus: my_range = my_range + 'm'
        Swr(level*' '+ 'for ' + g.ind + ' in ' + g.name + '.' + my_range + ':')
        level += 4

    Swr(level*' '+ equation)
#    if len (constraint_Sets) > 0:
    if len (explicit_Sets) > 0:
   #     print (equation)
    #    eqPars.myprint()
        p_eq = eqPars.find_part_type ('=', 'oper')
 #       1/0
    return


def WriteModelDef26 ( code ):                       #   DEF:
#        if not SvF.MakeModel : return
        if code == '' : return
#        code = SvF.Task.substitudeDef (code)

        code, eqPars, constraint_Sets, dif_minus, dif_plus = ParseEQUATION ( code, SvF.Task.Sets )
        
        parts = code.split('==')
        wr ( '    def '+parts[0]+': return '+parts[1]+'\n' )    # Code  for r in T.A[0].NodS:  T.gap[r,21]=0

def WriteModelCode26 ( code ):                      #   CODE:
        if code == '':  return
#        code = SvF.Task.substitudeDef (code)
        wr ( '    '+code)                                 # Code  for r in T.A[0].NodS:  T.gap[r,21]=0


def WriteModelOBJ19 ( Q, obj ):                        #   OBJ:
        print ('************OBJ', obj)
 #       if len(SvF.OptNames) > 0 :
#            Swr ('def fromPenalty():')      # в параметры оптимизации
  #          for  on in SvF.OptNames:
#                Swr ('    ' + on[0] + ' = SvF.Penalty['+str(i)+']')
   #             print (on)
    #            wr('    ' + on[0] + ' = SvF.Penalty[' + str(on[2]) + ']')
  #          Swr('if SvF.fromPenalty is None :  SvF.fromPenalty = fromPenalty')
#
 #           def fromPenalty():
  #              Inf.Period = SvF.Penalty[0]
   #             RR = SvF.Penalty[1]
    #            print('Inf.Period', Inf.Period)

 #           SvF.fromPenalty = fromPenalty
        if SvF.ObjToReadSols :
            Swr('Task.ReadSols()')
            return
        if SvF.OptMode == 'SurMin' :
            Swr ('SvF.ObjectiveFun = ' + obj)
            Swr('\nfrom SvFstart62 import SvFstart19')
            Swr('\nSvFstart19 ( Task )')  # 27   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            return
        Task = SvF.Task
        Funs = Task.Funs

        obj = fromTEXplus(obj)
#        print ('############OBJ', obj)

        if len(obj)==0 :        #   obj по умолчанию   -   OBJ:
            for fu in Funs :
              if fu.param : continue
              if len (fu.A) == 1:
                obj += fu.V.name + '.MSDnan() + ' + fu.V.name + '.Complexity(Penal[0])'   # x.MSD() + x.Complexity(Penal[0])
              else :
                obj += fu.V.name + '.MSDnan() + ' + fu.V.name + '.Complexity(Penal[0],Penal[1])'

        MsdType = ''
        Delta_Formula = 'Gr.F[fNum].Ftbl(n)-tbl[n]'  #  ПРОВЕРИТЬ  !!!!  заменить   Gr.F ->  Task.Funs

        obj, eqPars, constraint_Sets, dif_minus, dif_plus = ParseEQUATION ( obj, [] )

####################################################  ЗАПЛАТКА ###############   ∫(t_min,t_max,dT∙(d2/dT2(x(T)))**2)
        for g in Task.Sets:
                eqPars.substAllNames(g.name + '__p', g.name)
####################################################

  #      for n, name  in enumerate( SvF.PenaltyNames ):
   #             eqPars.substAllNames(name, 'Penal['+str(n)+']')


        for fu in Task.Funs:
            eqPars.substAllNames_but_dot_plus(fu.V.name, SvF.funPrefix + fu.V.name)

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

        obj, eqPars, constraint_Sets, dif_minus, dif_plus = ParseEQUATION ( obj, [] )

#        SvF.lenPenalty = 0
 #       for itn, it in enumerate (eqPars.items) :
  #          if it.part == 'Penal' :
   #             SvF.lenPenalty = max (SvF.lenPenalty, int(eqPars.items[itn+2].part)+1 )

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
#            SvF.lenPenalty = penNum
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
     #       print ('MsdType=', beg, delta, end)
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

        if SvF.numCV == -1 and SvF.OptMode == 'SvF':   # CV по умолчанию  2023.11
#            wr('\n    SvF.ValidationSets, SvF.notTrainingSets = MakeSets_byParts(SvF.curentTabl.NoR, SvF.CVstep)')  # CV_Sets (fu )
#            wr('\n    MakeSets_byParts(SvF.curentTabl.NoR, SvF.CVstep)')  # CV_Sets (fu )
            #wr('\n    make_CV_Sets(0, 7)')  # CV_Sets (fu )
            wr('\n    make_CV_Sets(0, SvF.CVstep)')  # CV_Sets (fu )    -   25.05
#make_CV_Sets ( NoR =0, NoSubSets =7, Param ='', Data =None ) :
#            wr('\n    Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )')  # 23.11
            wr('\n    if len (SvF.CV_NoRs) > 0 :')  # 23.11
            wr('\n       Gr.mu0 = py.Param ( range(SvF.CV_NoRs[0]), mutable=True, initialize = 1 )')  # 23.11

        for itn, it in enumerate(eqPars.items):        #  2023.11
            if it.part == 'MSD' or it.part == 'MSDnan' or it.part == 'MSDrel' : # or it.part == 'MSDcheck'
                fn = (eqPars.items[itn-2].part)
                wrs('\n    SvF.fun_with_mu.append(getFun(\''+fn+'\'))')
#                if SvF.numCV == -1 :
                if 1 :
                    wr('    if ' + fn + '.mu is None : '+ fn + '.mu = Gr.mu0')
                    wr('    ' + fn + '.ValidationSets = SvF.ValidationSets')
                    wr('    ' + fn + '.notTrainingSets = SvF.notTrainingSets')
                    wr('    ' + fn + '.TrainingSets = SvF.TrainingSets')
            elif it.part[0:3] == 'MSD':
                fn = (eqPars.items[itn-2].part)
                wr( '    ' + fn + '.mu = None' )

        wr(' \t\t\t\t\t\t\t\t\t\t\t# ' + obj)
        wr('    def obj_expression(Gr):  \n        return (')
        wr('             ' + obj )                             #   Gr.F[1].Complexity ( [Penal[0]] ) + Gr.F[0].MSD()
        wr('        )  \n    Gr.OBJ = py.Objective(rule=obj_expression)  \n')
        wr('    return Gr\n')        # end of    createGr ( Task, Penal ) :

 #                       Swr('Task.Delta     = Delta')
  #                      Swr('Task.DeltaVal  = DeltaVal')
   #                     Swr('Task.defMSD    = defMSD')
    #                    Swr('Task.defMSDVal = defMSDVal')

#        f.write( '\ndef print_res(Task, Penal, f__f):\n' )                            #  print_res
 #       f.write( '\n    Gr = Task.Gr' )
        wr( 'def print_res(Task, Penal, f__f):\n' )                            #  print_res
        if len(SvF.OptNames) > 0 :                      # to OptPar
            for i, on in enumerate (SvF.OptNames):
                wr('    ' + on[0] + ' = Penal[' + str(on[2]) + ']')
        wr( '    Gr = Task.Gr' )
        for nf, fu in enumerate( Task.Funs ) :
            if obj.find(fu.V.name+'.') >= 0 :
                wr( '\n    '+fu.V.name+ ' = ' + 'Task.Funs[' + str(nf) + ']' )    #  f__p = Gr.F[1]
#        f.write ( '\n\n    OBJ_ = Gr.OBJ ()' )
        wr ( '\n    OBJ_ = Gr.OBJ ()' )
 #       f.write ( '\n    print  \'    OBJ =\', OBJ_' )
  #      f.write ( '\n    print >> f__f,  \'\\n    OBJ =\', OBJ_\n' )
        wr('    print (  \'    OBJ =\', OBJ_ )')
        wr('    f__f.write ( \'\\n    OBJ =\'+ str(OBJ_)+\'\\n\')\n')
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
            p_mu = part.find('Gr.mu0[')          # 29  OBJ:  Σ(i=0,20,(x.V.dat[i]-x(x.A[0].dat[i]+t_min))**2) / x.V.sigma2 + x.Complexity(Penal[0])
            if p_mu >= 0 :
                p_mu_end = part.find(']', p_mu)
                repl = part[p_mu:p_mu_end+1]
      #          print (repl)
                part = part.replace(repl,repl+'()')
       #         print (part)
  #              1/0

#            if p == ' ': continue     # если нет штрафа
            wrs( '    tmp = (' + part + ')\n' )   # 29
            wrs( '    stmp = str(tmp)\n')
#            f.write( '    print       \'    \',int(tmp/OBJ_*1000)/10,\'\\t' + part + ' =\', tmp\n' )
 #           f.write( '    print >> f__f, \'    \',int(tmp/OBJ_*1000)/10,\'\\t' + part + ' =\', tmp\n' )
            wrs( '    print (      \'    \',int(tmp/OBJ_*1000)/10,\'\\t' + part + ' =\', stmp )\n' )
            wrs( '    f__f.write ( \'    \'+str(int(tmp/OBJ_*1000)/10)+\'\\t' + part + ' =\'+ stmp+\'\\n\')\n' )
#            f.write( '    print       \'    \',int(tmp/Gr.OBJ()*1000)/10,\'\\t' + p + ' =\', tmp\n' )
 #           f.write( '    print >> f, \'    \',int(tmp/Gr.OBJ()*1000)/10,\'\\t' + p + ' =\', tmp\n' )
            from_ = to_ + 2
        wr( '    return\n' )
        print ('Model was built')
        if  Q.upper() == 'OBJ:' :
            endObjStartModel()

def WriteModelOBJ_U (buf) :
        wr ('\ndef OBJ_U (Task):\n')
        for fu in range ( len( SvF.Task.Funs ) ) :
            wr( '    '+SvF.Task.Funs[fu].V.name+ ' = ' + 'Task.Funs[' + str(fu) + ']' )    #  f__p = Gr.F[1]
        wr ('    return '+buf)
        wr ('SvF.Task.OBJ_U = OBJ_U')
        endObjStartModel()


