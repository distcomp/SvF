# -*- coding: UTF-8 -*-
from __future__ import division
from  numpy import *
from  time import *
#import os
from  os  import listdir, getcwd, chdir
from  sys import *

from Lego import *
from Task import *
from CVSets import *
from GaKru import *
from Tools import *
import Table as Tab
from MakeModel import *
from Pars      import *
from Parser    import *
from ModelFiles import *

#from PyomoEverestEnv  import *
import COMMON as co

import io

import ezodf

def ReadMng ( ) :

 MngFile()


 if co.Task == None : co.Task = TaskClass ()
 Task = co.Task


 maxSigEst = 0           # оценка сигмы скольз. среднем

 NDT = -99999.0

 global buf
 global first_char    # первый символ
 global raw_line
 #global raw_line_no_tblanc
 buf = ""
 first_char = ''

 def readLine ():
     global first_char
     global raw_line
     ret =''
     while (1):
         ret += MNGreadline()
 #        if len(ret) == 0: return 'EOF'
#         ret = ret.rstrip()                     # убираем послед. пробелы и т.д
         print (ret)
         if not (co.SModelFile is None) :  Swr(' \t\t\t\t\t\t\t\t\t\t\t# ' + ret)
         ret = ret.split('\\#')[0].rstrip()     # comment in TEX formula
         ret = ret.split(  '#')[0].rstrip()       # убираем  comment и посл. пробелы
         if len(ret) == 0: continue
         if ret[-1] == '\\':                    # продолжение строки \\
             ret = ret[:-1]
             continue
         ret = ret.replace('\t', '    ')

         for np, p in enumerate(ret) :
             if p!= ' ' : break
         if np > 0 :   first_char = ret[:np]
         else:         first_char = ''

         ret = ' '.join(ret.split())   #  line_no_tblanc
         if len(ret) == 0:continue

#         raw_line = first_char + ret
         break

     buf = ret
     buf = UTF8replace(buf, '~', ' ')       # space in formula
     buf = UTF8replace(buf, '’', "'")
     buf = UTF8replace(buf, '‘', "'")
     buf = UTF8replace(buf, '∫', '\\int')
     buf = UTF8replace(buf, '∈', '\\in ')
     buf = UTF8replace(buf, '√', 'sqrt')
     buf = UTF8replace(buf, '∙', '*')
     buf = UTF8replace(buf, 'τ', 'tau')
     buf = UTF8replace(buf, 'μ', 'muu')
     buf = UTF8replace(buf, '\\mu', 'muu')
     buf = UTF8replace(buf, '\\Delta', 'Delta')
     buf = UTF8replace(buf, 'π', 'pi')
     buf = UTF8replace(buf, 'α', 'alpha')
     buf = UTF8replace(buf, 'σ', 'sigma')
     buf = UTF8replace(buf, 'ξ', 'xi')
#     buf = UTF8replace(buf, '\'', 'apst')
     buf = UTF8replace(buf, 'Ω', 'Omega')
     buf = UTF8replace(buf, 'Δ', 'Delta')
#     print ('AFTER:', buf)

     buf = UTF8replace(buf, '\\tau', 'tau')         # TEX

     buf = UTF8replace(buf, '\\cdot', '*')
     buf = UTF8replace(buf, '\\limits', '')
     buf = UTF8replace(buf, '\\left', '')
     buf = UTF8replace(buf, '\\right', '')

     be = 0                                     # \in  ->  \inn
     while 1:
         p = buf.find('\\in', be)               # \in  ->  \inn
         if p < 0: break
         if p != buf.find('\\int', be):
             buf = buf[:p + 3] + 'n' + buf[p + 3:]
         be = p + 3


     n=0
#     print 'WWW', buf
     while n<len(buf) :
        p = buf[n]
#        if ',;:+-/%()[]{}^=<>!'.find(p) >= 0:    #  without  '.*'  Select *  from  ../Trajectories.tbl where x !=to_x
#        if '.,;:+-*/%()[]{}^=<>!'.find(p) >= 0:
        if ',;:+-*/%()[]{}^=<>!'.find(p) >= 0:     #  '.'    ???
             if n+1<len(buf) :
                 if buf[n+1] == ' ' :  buf = buf[:n+1] + buf[n+2:]
             if n-1>=0 :
                 if buf[n-1] == ' ' :  buf = buf[:n-1] + buf[n:]
        n += 1
     buf_up = buf.upper()                           # ИСКЛЮЧЕНИЯ
#     p = buf_up.find ('FROM.')                     #  '.'    ???
 #    if p >= 0 : buf = buf[:p+4]+' '+buf[p+4:]
  #   buf_up = buf.upper()
   #  p = buf_up.find ('DATAPATH.')
    # if p >= 0 : buf = buf[:p+8]+' '+buf[p+8:]     #  '.'    ???
     buf_up = buf.upper()
     p = buf_up.find ('SELECT*')
     if p >= 0 : buf = buf[:p+6]+' * '+buf[p+7:]
#     if ( buf_up.find ('FROM .') < 0 and
 #         buf_up.find ('DATAPATH .') < 0 ) :            # DataPath ../    # from  ../Trajectories.tbl
  #       buf = buf.replace(' .', '.');  buf = buf.replace('. ', '.')
   #  if buf_up.find   ('SELECT *') < 0 :              # Select * from  ../Trajectories.tbl
    #     buf = buf.replace(' *', '*');  buf = buf.replace('* ', '*')

     buf = buf.replace(' \\in', '\\in')

     raw_line = first_char + buf
#     print ('bufFFFFFFFFF', buf)
     return buf


 def readStr():
     global buf

     if buf == '' : buf = readLine ()

     if len(first_char) > 0 : return buf

     for n, p in enumerate(buf) :
         if p==' ' or p=='=':
             ret = buf[:n]
             buf = buf[n + 1:]
             return ret
         if p==':' :
             ret = buf[:n + 1]
             buf = buf[n + 1:]
             return ret
     ret = buf
     buf = ''

     return ret


 def readFloat():
#     return getfloat(readStr())
     txt = readEqStr()
     if com.Preproc: return txt
     ret=getfloatNaN( txt )

     if isnan(ret) :
         print ('ERR convertion:', txt)
         exit (-1)
     return ret

 def readInt():
     txt = readEqStr()
     if com.Preproc: return txt
     ret=getfloatNaN( txt )
     if isnan(ret) :
         print ('ERR convertion:', txt)
         exit (-1)
     return int(ret)

 def readBool():
     txt = readEqStr()
     if com.Preproc: return txt
     if txt == 'True'  : return True
     if txt == 'False' : return False
     print ('ERR convertion to Bool:', txt)
     exit (-1)

 def readEqStr():
        global buf
        if buf[0] == '=' : buf=buf[1:]    #  =Server
        return  readStr()


 def readList ( ) :
    global buf
    if buf[0] == '=' : buf=buf[1:]    #  =0
#    print '|' + buf + '|'
    if buf[0] == '[' :
        bufL = buf
        buf = ''
        while bufL.count(']') == 0 :
#            print 'BbufL', bufL, 'B',buf
            bufL = bufL + ' ' + readStr()
#            print 'bufL', bufL, buf
#        print 'BufL', bufL
        s =bufL.split(']')
        buf = s[1];
        st = s[0]
#        print '\nList',  st+']'
        st = st.replace(',',' ')
        print (' List',  st+']')
#        s =st.replace('  ',' ').split('[')
        st =st.replace('  ',' ')
        st = st[1:]                    # убираем [
        if st[0] == ' ' : st = st[1:]  # убир первый пробел
#        print st
        st = st.split(' ')
        print ('LL:', st)
        return st
    elif  isfloat(buf) :
#    elif  '-0123456789.'.count(buf[0])  :   # isfloat
        ret = buf.split(' ')
        buf = ''
        return ret
    else :
#        print 'B', buf
        ret = [buf]
        buf = ''
        return ret
#        rName = readStr()
        return deepcopy( Task.getDef(rName) )
#        return deepcopy( Task.getDef(rName) )


 def readListFloat ( ) :
     ret = readList ( )
     for r in range(len(ret)) :  ret[r] = getfloat(ret[r])
#     if len (ret) == 1 :                # подпорка против [[-100.87615926405576, 169.6292943760991]]
 #       if type(ret[0]) is list : ret = ret[0]
     return ret

# def LeftLow(rect) :
#     if rect[0] > rect[2] : sw = rect[0]; rect[0] = rect[2]; rect[2] = sw
#     if rect[1] > rect[3] : sw = rect[1]; rect[1] = rect[3]; rect[3] = sw
#     return rect


 def getMinMax(polygon) :
     xmi = polygon[0]
     xma = polygon[0]
     ymi = polygon[1]
     yma = polygon[1]
     for p in range (int(len(polygon)/2)) :
         xmi = min ( xmi, polygon[2*p] )
         xma = max ( xma, polygon[2*p] )
         ymi = min ( ymi, polygon[2*p+1] )
         yma = max ( yma, polygon[2*p+1] )
     return [xmi, ymi, xma, yma]


#*********************************************  NEW 18 *******************************

 def getNameOld ( txt ):   # delete 2020-02
        name = txt
        min_pos = len(txt)
        razd = ''
        ost = ''
        for delim in [ '(',')', '{','}' , ',' ] :
            pos = txt.find (delim)
            if pos !=-1 and pos < min_pos :
                min_pos = pos
        if min_pos < len(txt) :
            name = txt[:min_pos]
            razd = txt[min_pos]
            ost  = txt[min_pos+1:]
#        print name+'|'+razd+'|'+ost+'|'
        return name, razd, ost

 global EmptyBuf

 def Is (Q, qqq) :
     global EmptyBuf
     if Q == qqq.upper() :
         EmptyBuf = True
         return True
     return False
#     return ( Q == qqq.upper() )

 old_qlf = ''

 while 1 :
    global EmptyBuf
    EmptyBuf = False
    qlf = readStr()
    if len (first_char) > 0 :
        if old_qlf != '' :   qlf = old_qlf
    else  : old_qlf = ''
    glfCase = qlf
    Q = qlf.upper()
    if Q[-1] == ':' :  old_qlf = Q   # if Q in ['GRID:','VAR:','PARAM:','EQ:', 'DEF:','CODE:', 'OBJ:'] :
    printS  (Q+' |')

    if   Is(Q, "TaskName" )   : co.TaskName = readEqStr(); nSwr( 'co.TaskName = \''+co.TaskName+'\''); nSwr( 'print(co.TaskName)')
    elif Is(Q, "ChDir" )      :
                    new_cwd = readEqStr();
                    os.chdir(new_cwd);   sys.path.append(os.getcwd())
                    printS ( '*******************  change CWD:', getcwd() )
    elif Is(Q, "VERSION" )    : co.Version  = readFloat();   nSwr( 'co.Version = ',co.Version)      #27
    elif Is(Q, "Debag"  )     : co.Preproc  = False                                       #27
    elif Is(Q, "Preproc"  )   : co.Preproc  = True                                         #27
    elif Is(Q, "Compile"  )   : co.Preproc  = True                                         #27
    elif Is(Q, "printL"  )    : co.printL   = readInt();     nSwr( 'co.printL = ',co.printL )  #27
    elif Is(Q, "CVNUMOFITER") : co.CVNumOfIter = readInt();  nSwr( 'co.CVNumOfIter = ', co.CVNumOfIter)  #27
    elif Is(Q, "CVSTEP" )     : co.CVstep      = readInt();  nSwr( 'co.CVstep   = ',co.CVstep) #27
#    elif Is(Q, "OptStep"   )  : co.OptStep    = readFloat(); nSwr( 'co.OptStep  = ',co.OptStep)
    elif Is(Q, "OptStep"   )  : co.OptStep    = readListFloat(); nSwr( 'co.OptStep  = ',co.OptStep)
    elif Is(Q, "ExitStep"  )  : co.ExitStep   = readFloat(); nSwr( 'co.ExitStep = ',co.ExitStep)
    elif(Is(Q, "RunSolver" ) or
         Is(Q, "RunMode"   ) ) : co.RunMode = readEqStr();   nSwr( 'co.RunMode = \''+co.RunMode+'\'')
    elif Is(Q, "Penalty"   )  : co.mngPenalty = readListFloat();  nSwr( 'co.mngPenalty = ',co.mngPenalty)

    elif Is(Q,"py_max_iter")                   : co.py_max_iter                   = readInt();   nSwr( 'co.py_max_iter = ',co.py_max_iter)
    elif Is(Q,"py_tol")                        : co.py_tol                        = readFloat(); nSwr( 'co.py_tol = ',co.py_tol)
    elif Is(Q,"py_warm_start_bound_push")      : co.py_warm_start_bound_push      = readFloat(); nSwr( 'co.py_warm_start_bound_push = ',co.py_warm_start_bound_push)
    elif Is(Q,"py_warm_start_mult_bound_push") : co.py_warm_start_mult_bound_push = readFloat(); nSwr( 'co.py_warm_start_mult_bound_push = ',co.py_warm_start_mult_bound_push)
    elif Is(Q,"py_constr_viol_tol")            : co.py_constr_viol_tol            = readFloat(); nSwr( 'co.py_constr_viol_tol = ',co.py_constr_viol_tol)

    elif Is(Q, "resFile"   )  : co.resF = readEqStr();       nSwr( 'co.resF = \''+co.resF+'\'')
    elif Is(Q, "useNaN" )     :
                        if len (buf) >= 4 :  co.useNaN = readBool()
                        else              :  co.useNaN = True;
                        nSwr( 'co.useNaN = ' + str(co.useNaN) )
    elif Is(Q, "Select")      :
                                tmp = buf.split('from')[1].split('As')   # ... from a.txt As Tb
                                if len (tmp)==2 :
                                    tb_name = tmp[1].replace(' ','')
                                    Swr( tb_name + ' = Tab.Select ( \''+buf+'\' )')
                                else :
                                    Swr ( 'Tab.Select ( \''+buf+'\' )')                   #27
                                if not co.Preproc : DataR = Tab.Select ( buf ) ;   # 27  !!!!!!!!!!!!!!!!!!!!!!!
    elif Is(Q, "DrawErr") :     Swr( '\nTask.DrawErr ()');                Task.DrawErr()
    elif Is(Q, "Draw") :        Swr( '\nTask.Draw (  \'' + buf + '\' )'); Task.Draw (buf)
    elif Is(Q, "DrawVar") :     Swr( '\nTask.DrawVar ()');                Task.DrawVar ()
    elif Is(Q, "DrawTransp") :  Swr( '\nco.DrawTransp = True' );          co.DrawTransp = True
    elif Is(Q, "MarkerSize") :  co.MarkerSize = readFloat();   nSwr( 'co.MarkerSize  = ',co.MarkerSize)
    elif Is(Q, "MarkerColor") : co.MarkerColor = readEqStr();   nSwr( 'co.MarkerColor  = \''+co.MarkerColor+'\'')
    elif Is(Q, "DataMarkerSize"): co.DataMarkerSize = readFloat(); nSwr( 'co.DataMarkerSize  = ',co.DataMarkerSize)
    elif Is(Q, "DataLineWidth"): co.DataLineWidth = readFloat(); nSwr( 'co.DataLineWidth  = ',co.DataLineWidth)
    elif Is(Q, "LineWidth"): co.LineWidth = readFloat(); nSwr( 'co.LineWidth  = ',co.LineWidth)
    elif Is(Q, "LineColor"): co.LineColor = readEqStr(); nSwr( 'co.LineColor  = \''+co.LineColor+'\'')
    elif(Is(Q, "GRID:") or
         Is(Q, "SET:")  ) :  WriteGrid27 ( buf )
    elif Is(Q, "VAR:"   ) :  WriteVarParam26 ( buf, False )
    elif Is(Q, "PARAM:" ) :  WriteVarParam26 ( buf, True )
    elif Is(Q, "EQ:")     :  WriteModelEQ26 ( buf )
    elif Is(Q, "DIF1")    :  co.DIF1 = readEqStr();  nSwr( 'co.DIF1 = \''+co.DIF1+'\'') #27
    elif Is(Q, "Use^forPower") :  co.UseHomeforPower = readBool(); nSwr( 'co.seHomeforPower = '+co.UseHomeforPower ) #28
    elif Is(Q, "OBJL:" )  :  WriteModelOBJ19 ( Q,buf )
    elif Is(Q, "OBJU:" )  :
                            WriteModelOBJ_U (buf)
                            if not co.Preproc :  SvFstart19p(Task)
    elif Is(Q, "OBJ:" ):
                            WriteModelOBJ19 ( Q,buf )
                            if not co.Preproc : SvFstart19p ( Task )
    elif Is(Q, "EoF"):
#                        if objective == 'N':  buf = 'OBJ: N';
                        print ('EoF ************ END OF READ MNG ********************* EoF')
                        co.SModelFile.close()
                        return Task
    elif Is(Q, "MakeSets_byParam") :
            args = buf.split(' ');  args[0] = '\''+ args[0] + '\''
            Swr('co.testSet, co.teachSet = MakeSets_byParam ( co.curentTabl, '+','.join(args)+' )' )
            if not co.Preproc:
                args = buf.split(' '); CVstep=0; CVmargin=0
                if len (args) > 1: CVstep   = int(args[1])
                if len (args) > 2: CVmargin = int(args[2])
                co.testSet, co.teachSet = MakeSets_byParam(co.curentTabl, args[0], CVstep, CVmargin)
    elif Is(Q, "MakeSets_byParts") :
            args = buf.split(' ')
            Swr('co.testSet, co.teachSet = MakeSets_byParts ( co.curentTabl.NoR, '+','.join(args)+' )' )
            if not co.Preproc:
                CVstep=7;  CVpartSize = 1;  CVmargin=0        # по умолчанию
                if len (args) > 0: CVstep     = int(args[0])
                if len (args) > 1: CVpartSize = int(args[1])
                if len (args) > 2: CVmargin   = int(args[2])
                co.testSet, co.teachSet = MakeSets_byParts(co.curentTabl.NoR, CVstep, CVpartSize, CVmargin)
    elif Is(Q, "WriteSvFtbl" ):
                    Swr( '\nco.curentTabl.WriteSvFtbl (  \'' + buf + '\' )')
                    if not co.Preproc: co.curentTabl.WriteSvFtbl ( readEqStr() )
    elif Is(Q, "DataPath")  : co.DataPath = readEqStr(); nSwr( 'co.DataPath = \''+co.DataPath+'\'')
    elif Is(Q, "SavePoints" )     :
                        if len (buf) >= 4 :  co.SavePoints = readBool()
                        else              :  co.SavePoints = True;
                        nSwr( 'co.SavePoints = ' + str(co.SavePoints) )

 #   elif Is(Q, "SaveDeriv" )  :  co.SaveDeriv = True; nSwr( 'co.SaveDeriv = True')
    elif Is(Q, "CODE:") :    WriteModelCode26 ( buf )
    elif Is(Q, "EoD")   :    co.curentTabl = None;   Swr('co.curentTabl = None')

############################################# 27
    elif Is(Q, "TBL:") :  Tab.TblOperation(buf);
    elif Is(Q, "DEF:") :  WriteModelDef26 ( buf )

    elif Is(Q, "LocolSolverName" ) :  co.LocalSolverName = readEqStr()
    elif Is(Q, "SolverName"      ) :  co.SolverName      = readEqStr()
    elif Is(Q, "Hack_Stab"       ) :  co.Hack_Stab  = bool(readStr()=='True');

    elif ( Is(Q,"DataFile") or
           Is(Q,"DataFile_Npp") ):   Tab.Select ( '* from '+buf )
#    elif Is(Q, "NoMakeModel" )   :   co.MakeModel = False;
    elif Is(Q, "CVNoBorder" )   :  co.CVNoBorder    = True
    elif Is(Q, "NotCulcBorder") :  co.NotCulcBorder = True
    elif qlf == "TASK"          :  co.Task.Name = readEqStr(); print (co.Task.Name)
#    elif qlf == "CVPARTSIZE" :  co.CVpartSize = int(readStr());  Mng.CVside = float(readStr())
#    elif qlf == "CVPARAM"    :  Mng.CVparam = readStr(); FuncR.Col.append ( Col(Mng.CVparam) );  #  print 'CVparamN', len(FuncR.Col)

 #   elif Is(Q, "SortedBy")   :  FuncR.SortedBy.name = readStr()

#    elif Is(Q, "Grid")         : gri, buf = readGrid(buf); Task.Grids.append ( gri )

#    elif Is(Q, "TranspGrid" )  :  co.TranspGrid  = 'Y'
#    elif Is(Q, "SaveGrid"   )  :  co.SaveGrid    = 'Y'
    elif Is(Q, "SaveSol") :
                            if len(buf) == 0 :  Task.SaveSol()
                            else             :  Task.getFun(readStr()).SaveSol('')
    elif Is(Q, "Prefix"   )    :  co.Prefix = readStr()

#    elif Is(Q, "OptStep"   ) : co.OptStep     = readFloat()
 #   elif Is(Q, "ExitStep"  ) : co.ExitStep     = readFloat()
    elif Is(Q,"OptMode")     : co.OptMode = readEqStr()

    else :
        if True : # co.Preproc :
            tmp = raw_line.split('Select ')   #27   в одну строку !!!!!!!!!!!!!
 #           print 'tmp', tmp
            if len (tmp) == 2:
                Swr(tmp[0] + ' Select ( \'' + tmp[1] + '\' )')
 #               buf = ''
            else :
                Swr(raw_line)
                if raw_line[0] != ' ' :             # 20.01.19
                  raw_part = raw_line.split('=')  #  если = и в левой части нет ( [  добавляем в Def
                  if len(raw_part)==2:
                    if raw_part[0].find('(') < 0 and raw_part[0].find('[') < 0 and   \
                       raw_part[1].find('(') < 0 and raw_part[1].find('[') < 0:
                            Swr('Task.AddDef(\''+raw_part[0].strip()+'\',['+raw_part[1].strip()+'])')
            if co.Preproc : buf = ''
        if not co.Preproc :
#          string = glfCase + buf
          string = raw_line
          string = string.replace(' ','')
          if string.upper().find("AZIMUTINIT") >= 0:         #  AzimutInit ( 67.92, 32.83 )
            b, arg, e = getFromBrackets (string, '(')
            args = arg.split(',')
            AzimutInit ( float(args[0]), float(args[1]) )
            continue
          parts = string.split('=')
          if len(parts) == 2:
            beg, args, end = getArgsFromBrackets (parts[0], '(')  # MU(50,50) = 10
            if not beg is None :
#                print beg, args, end
                f = Task.getFun ( beg )
                if not f is None :
                    f.SetPointValue ( args, parts[1] )
                    buf = ''
                continue

            buf = parts[1]  # чтоб потом достать из buf
#        defName = glfCase
 #       if readStr() == '=':
            defList = readListFloat()
            print ('=', defList)
    #        Task.AddDef(defName, defList)
            Task.AddDef(parts[0], defList)
            buf = ''
          else:
            print ("********* Can't Understand: ", Q);  exit (-1)
    if EmptyBuf : buf = ''




 while 0 :  ######################################################################################

    if Is(Q,"Polygon") :
                            defName = readStr()
                            defList = ReadPolygon(DataR.InFile)
                            Task.AddDef(defName, defList)
    elif Is(Q,"getMinMax") :
                    dn = Task.getDefNum(readStr())
                    rect = getMinMax(Task.Def[dn][1][:])
                    Task.Def[dn][1] = rect
#                    print 'MinMax', rect
    elif Is(Q,'GetRectLastFunc' ):
                        defName = readStr()
                        defList = [Task.Funs[0].A[0].min,Task.Funs[0].A[1].min,
                                   Task.Funs[0].A[0].max,Task.Funs[0].A[1].max]
    #                    print defName, defList
                        Task.AddDef(defName, defList)
    elif Is(Q,"RECTANGLE") :
                          rect = readListFloat()
                          rect = getMinMax (rect)
                          FuncR.A[0].min = rect[0]; FuncR.A[1].min = rect[1];
                          FuncR.A[0].max = rect[2]; FuncR.A[1].max = rect[3];
    elif Is(Q,"XYin"):
                    rect = readListFloat()
                    rect = getMinMax(rect)
                    DataR.Rect = rect
    elif Is(Q,"RoundOut"):
                    dn = Task.getDefNum(readStr())
                    rect = getMinMax(Task.Def[dn][1][:])
                    val = readFloat()
                    rect[0] = val * floor(rect[0]/val)
                    rect[1] = val * floor(rect[1]/val)
                    rect[2] = val * ceil (rect[2]/val)
                    rect[3] = val * ceil (rect[3]/val)
#                    print "RoundOut", Task.Def[dn][0], rect
                    Task.Def[dn][1] = rect
    elif Is(Q,'RoundOutGrid05'):
                    dn = Task.getDefNum(readStr())
                    rect = getMinMax(Task.Def[dn][1][:])
                    val = readFloat()
                    val05 = val/2
                    rec = deepcopy(rect)
                    rec[0] = val05 * round(rect[0]/val05)
                    rec[1] = val05 * round(rect[1]/val05)
                    rec[2] = val05 * round(rect[2]/val05)
                    rec[3] = val05 * round(rect[3]/val05)
#                    if abs(val*int(rect[0]/val)-rect[0]) < 0.001*val : rect[0] -= val05
 #                   if abs(val*int(rect[1]/val)-rect[1]) < 0.001*val : rect[1] -= val05
  #                  if abs(val*int(rect[2]/val)-rect[2]) < 0.001*val : rect[2] += val05
   #                 if abs(val*int(rect[3]/val)-rect[3]) < 0.001*val : rect[3] += val05
                    if abs(val*int(rec[0]/val)-rec[0]) < 0.001*val : rec[0] -= val05
                    if abs(val*int(rec[1]/val)-rec[1]) < 0.001*val : rec[1] -= val05
                    if abs(val*int(rec[2]/val)-rec[2]) < 0.001*val : rec[2] += val05
                    if abs(val*int(rec[3]/val)-rec[3]) < 0.001*val : rec[3] += val05
                    if abs(rec[0]-rect[0]) > val05 : rec[0] += val
                    if abs(rec[1]-rect[1]) > val05 : rec[1] += val
                    if abs(rec[2]-rect[2]) > val05 : rec[2] -= val
                    if abs(rec[3]-rect[3]) > val05 : rec[3] -= val
#                    print rec[0]-rect[0]
 #                   print rec[1]-rect[1]
  #                  print rec[2]-rect[2]
   #                 print rec[3]-rect[3]
                    print ("RoundOutGrid05", Task.Def[dn][0], rec)
                    Task.Def[dn][1] = rec
#                    Task.Def[dn][1] = rect
    elif Is(Q,"Extend"):
                        dn = Task.getDefNum(readStr())
                        rect = getMinMax(Task.Def[dn][1][:])
                        rdel = readFloat()
                        rect[0] -= rdel;  rect[1] -= rdel;  rect[2] += rdel;  rect[3] += rdel
                        print ("Extend", Task.Def[dn][0], rect)
                        Task.Def[dn][1] = rect
    elif Is(Q,"GaussKrugerToWGS84"):
                        dn = Task.getDefNum(readStr())
                        rect = getMinMax(Task.Def[dn][1][:])
                        rect[1], rect[0] = GausKruToWGS84(rect[0], rect[1], 0)
                        rect[3], rect[2] = GausKruToWGS84(rect[2], rect[3], 0)
#                        print rect
                        Task.Def[dn][1] = rect
    elif Is(Q,"WGS84ToGaussKruger"):
                        dn = Task.getDefNum(readStr())
                        rect = getMinMax(Task.Def[dn][1][:])
                        rect[0], rect[1] = WGS84toGausKru(rect[1], rect[0], 0)
                        rect[2], rect[3] = WGS84toGausKru(rect[3], rect[2], 0)
#                        print 'GaussKruger rect', rect
                        Task.Def[dn][1] = rect

    elif Is(Q, "ToGaussKruger"):   DataR.ToGaussKruger = True

    elif Is(Q, "DIM" )      :  FuncR.dim = int(readStr())


    elif qlf == "VARNORMALIZATION" :  co.VarNormalization = True

    elif qlf == "READNAMETBLFROM" :
                                    ReadNameTblFrom  = readStr()
                                    if len(DataPath)==0 : FuncR.ReadFrom = ReadNameTblFrom
                                    else                : FuncR.ReadFrom = DataPath+ '/' + ReadNameTblFrom
    elif qlf == "READGRIDFROM"    :  ReadGridFrom     = readStr()

    elif qlf == "STABFILE"        :  StabFile         = readStr()

    elif qlf == "NAMEF"     :  FuncR.V.append ( Vari(readStr()) )

    elif qlf == "NAMEX"     :  FuncR.A.append ( Arg(readStr()) )
    elif qlf == "NAMEY"     :  FuncR.A.append ( Arg(readStr()) )
    elif qlf == "STEPX"     :  FuncR.A[0].step = float(readStr())
    elif qlf == "STEPY"     :  FuncR.A[1].step = float(readStr())
    elif qlf == "VISX"      :  FuncR.A[0].vis  = float(readStr())
    elif qlf == "VISY"      :  FuncR.A[1].vis  = float(readStr())
    elif qlf == "ADDARG"    :  FuncR.A.append(Arg(readStr())); FuncR.A[-1].step=float(readStr()); FuncR.A[-1].vis=float(readStr())

    elif qlf == "MINX"      :  FuncR.A[0].min  = float(readStr())
    elif qlf == "MINY"      :  FuncR.A[1].min  = float(readStr())
    elif qlf == "MAXX"      :  FuncR.A[0].max  = float(readStr())
    elif qlf == "MAXY"      :  FuncR.A[1].max  = float(readStr())
    elif qlf == "NODATA"    :  FuncR.NDT       =NDT       = float(readStr())
    elif Is(Q,"AddCol"  )   :  FuncR.Col.append ( Col(readStr()) )

    elif qlf == "MAXSIGEST" :  maxSigEst = float(readStr());

def  SvFstart19p ( Task ):
#        star = imp.load_source('', 'SvFstart62.py')
 #       star.SvFstart19 ( Task )
        from SvFstart62 import SvFstart19  #*
        SvFstart19 ( Task )

