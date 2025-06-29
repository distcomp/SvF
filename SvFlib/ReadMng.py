# -*- coding: UTF-8 -*-
from __future__ import division

from Object import *

#import COMMON as co
#from  numpy import *

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
#import COMMON as co

import io
from datetime import datetime
current_datetime = datetime.now()
print(current_datetime)



#import ezodf

def ReadMng ( ) :
# SvF.Compile = True
 to_logOut ( 'Start at   '+str(datetime.now()) )


 if SvF.EofTask == False :
    SvF.mngF = MngFile()

 coMembers   = [ k for k in SvF.__dict__.keys() if not k.startswith("__")]        #  COMMON MEMBERS
 coMembersUP = [ k.upper().encode('ascii', 'ignore') for k in coMembers ]                              #  COMMON MEMBERS UP

 SvF.Task = TaskClass()
 Task = SvF.Task

 Table('', 'SvF.curentTabl')                # чтобы обрабатывать SvF.curentTabl.Dat
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
     semicol = False
     ret =''
     while (1):
         if (len ( SvF.comment_buf ) > 0) and SvF.Comment :
             if SvF.StartModel_pos > 60:        #   чтобы выравниватть комментарии
                 Swrs( '\t#  ' + SvF.comment_buf )
             else :
                 Swrs( ' '*(60-SvF.StartModel_pos)+'#  ' + SvF.comment_buf )
             SvF.comment_buf = ''
             SvF.StartModel_pos = 0
         ret += MNGreadline()
 #        if len(ret) == 0: return 'EOF'
#         ret = ret.rstrip()                     # убираем послед. пробелы и т.д
 #        print ('R',ret, SvF.SModelFile)
#         if not (SvF.SModelFile is None) :  Swrs(' \t\t\t\t\t\t\t\t\t\t\t# ' + ret)
         SvF.comment_buf = ret
         ret = ret.split('\\#')[0].rstrip()     # comment in TEX formula
         ret = ret.split(  '#')[0].rstrip()       # убираем  comment и посл. пробелы
         if len(ret) == 0: continue
         if ret[-1] == '\\':                    # продолжение строки \\
             ret = ret[:-1]
             continue
#         ret = ret.replace('\t', '    ')
         if ret[0] == ':':
             semicol = True
  #           len(a) - len(a.lstrip())
   #          ret = ret[1:]
             first_char = ''
             break

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
     buf = UTF8replace(buf, '»', "'")
     buf = UTF8replace(buf, '«', "'")
     buf = UTF8replace(buf, '“', '"')
     buf = UTF8replace(buf, '”', '"')
 #    buf = UTF8replace(buf, '\t', "    ")
     buf = UTF8replace(buf, '—', '-')
     buf = UTF8replace(buf, '–', '-')
     buf = UTF8replace(buf, '‘', '\'')
     buf = UTF8replace(buf, '∫', '\\int')
     buf = UTF8replace(buf, 'Σ', '\\sum')
     buf = UTF8replace(buf, '∈', '\\in ')
     buf = UTF8replace(buf, '√', 'sqrt')
     buf = UTF8replace(buf, '∙', '*')
     buf = UTF8replace(buf, '·', '*')   #  другая точка

     if not SvF.UseGreek :
        buf = UTF8replace(buf, 'τ', 'tau1')       #  tau   - не ест Pioma
        buf = UTF8replace(buf, 'μ', 'muu')
        buf = UTF8replace(buf, 'π', 'pi')
        buf = UTF8replace(buf, 'α', 'alpha')
#        buf = UTF8replace(buf, 'φ', 'fi')
        buf = UTF8replace(buf, 'σ', 'sigma')
        buf = UTF8replace(buf, 'ξ', 'xi')
#        buf = UTF8replace(buf, '\'', 'apst')
        buf = UTF8replace(buf, 'Ω', 'Omega')
        buf = UTF8replace(buf, 'Δ', 'Delta')
        buf = UTF8replace(buf, 'δ', 'delta')

#     print ('AFTER:', buf)
     buf = UTF8replace(buf, '\\mu', 'muu')
     buf = UTF8replace(buf, '\\Delta ', 'Delta')
     buf = UTF8replace(buf, '\\Delta', 'Delta')

     buf = UTF8replace(buf, '\\tau', 'tau1')         # TEX   tau   - не ест Pioma

     buf = UTF8replace(buf, '\\cdot', '*')
     buf = UTF8replace(buf, '\\limits', '')
     buf = UTF8replace(buf, '\\left', '')
     buf = UTF8replace(buf, '\\right', '')
     buf = UTF8replace(buf, '\\!', '')
     buf = UTF8replace(buf, '\\partial ', 'd')       #  частная производная
     buf = UTF8replace(buf, '\\partial', 'd')       #  частная производная
     buf = UTF8replace(buf,  '∂', 'd')       #  частная производная


     while 1:           # \color {red}  ->  ''
         p = buf.find('\\color')
         if p < 0: break
         p_br = buf.find('}',p)
         buf = buf[:p] + buf[p_br+1:]
 #        print( buf)
  #       1/0

     be = 0                                     # \in  ->  \inn
     while 1:
         p = buf.find('\\in', be)               # \in  ->  \inn
         if p < 0: break
         if p != buf.find('\\int', be):
             buf = buf[:p + 3] + 'n' + buf[p + 3:]
         be = p + 3
 #    print ('\nret********', '|'+buf+'|')

     n=0
     if SvF.Substitude and (semicol==False):
       quotes= 0
       while n<len(buf) :
         p = buf[n]
         if p == '\'' or p == '\"' :   #  а не в строке ли мы?
             quotes = 1 - quotes
         if quotes == 0:                                            # remove blancks
#         if ',;:+-/%()[]{}^=<>!'.find(p) >= 0:    #  without  '.*'  Select *  from  ../Trajectories.tbl where x !=to_x
#         if '.,;:+-*/%()[]{}^=<>!'.find(p) >= 0:
           if ',;:+-*/%()[]{}^=<>!'.find(p) >= 0:     #  '.'    ???
             if n+1<len(buf) :
                 if buf[n+1] == ' ' :
                     if buf[n+2:].find ('for ') == 0: n+=1; continue    # ИСКЛЮЧЕНИЯ
                     if buf[n+2:].find ('sum ') == 0: n+=1; continue    # ИСКЛЮЧЕНИЯ
                     buf = buf[:n+1] + buf[n+2:]
             if n-1>=0 :
                 if buf[n-1] == ' ' :
                     buf = buf[:n-1] + buf[n:]
                     continue
         n += 1
                                                    # ИСКЛЮЧЕНИЯ
  #   print ('\nbuf1********', '|'+buf+'|')

     buf_up = buf.upper()
     p = buf_up.find ('SELECT*')
     if p >= 0 : buf = buf[:p+6]+' * '+buf[p+7:]
     print ('\nbuf2********', '|'+buf+'|')

     p = buf_up.find ('FROM/')
     if p >= 0 : buf = buf[:p+4]+' '+buf[p+4:]

     buf = buf.replace(' \\in', '\\in')

     raw_line = first_char + buf
  #   print ('bufFFFFFFFFF', buf, raw_line, '|'+first_char+'|')
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
     txt = readEqStr()
#     if SvF.Compile : return txt     14.08.22
     ret=getfloatNaN( txt )
     if np.isnan(ret) :
         print ('ERR convertion:', txt)
         exit (-1)
     return ret

 def readInt():
     txt = readEqStr()
#     if SvF.Compile : return txt     14.08.22
     ret=getfloatNaN( txt )
     if np.isnan(ret) :
         print ('ERR convertion:', txt)
         exit (-1)
     return int(ret)

 def readBool():
     txt = readEqStr()
 #    if SvF.Compile : return txt                   14.08.22

     if txt == 'True'  : return True
     if txt == 'False' : return False
     print ('ERR convertion to Bool:', txt)
     exit (-1)

 def readEqStr():
        global buf
        if buf[0] == '=' : buf=buf[1:]    #  =Server
        if buf[0] == '\'' and buf[-1] == '\'' :
            return buf[1:-1]  # 30g+
        if buf[0] == '"' and buf[-1] == '"':
            return buf[1:-1]  # 30g+
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
    if Q[-1] == ':' :  old_qlf = Q   # if Q in ['GRID:','VAR:','PARAM:','EQ:', 'DEF:','CODE:', 'OBJ:', 'Set:', Penalty] :
    printS  (Q+' |')

#    print  (Q+'|', ord(Q[0]))
    Q = Q.replace ('USE^FORPOWER', 'USEHOMEFORPOWER')
    Qasc = Q.encode('ascii', 'ignore')
    if (Qasc in coMembersUP ) :    #  Win редактор гадит в первую строку !!!!!
#        print('Mem****************************', Q, Qasc)
 #       1./0
        n = coMembersUP.index(Qasc)
 #       print ('Q',Q)
  #      print (coMembersUP[n], coMembers[n])
        if coMembersUP[n] == 'SVFPREFIX' :
            if buf[0] == '\'' or buf[0] == '\"' :  buf = buf[1:-1]
            coMembersUP = [buf.upper() + k for k in coMembersUP]
#            print('PPP', coMembersUP)
        else :
            if   coMembers[n] == "TaskName" and buf[0] != '\'' and buf[0] != '\"' : buf = '\'' + buf + '\''
            elif coMembers[n] == 'useNaN' and buf == '' :  buf = 'True'
            elif Is(Q, "SchemeD1"):
                SvF.SchemeD1.append(readEqStr());  buf = '\"'+SvF.SchemeD1[-1]+'\"'    # 30
            elif Is(Q, "ObjToReadSols"):
                SvF.ObjToReadSols = readBool(); continue
            elif Is(Q, "funPrefix"):
                SvF.funPrefix = readEqStr(); continue
            elif Is(Q, "UseGreek"):
                SvF.UseGreek = readBool(); continue
            elif Is(Q, "Substitude"):
                SvF.Substitude = readBool();  continue
            elif Is(Q, "UseHomeforPower"):
                SvF.UseHomeforPower = readBool();  continue
            elif Is(Q, "UsePrime"):
                SvF.UsePrime = readBool();  continue
            elif Is(Q, "TabSize"):
                TabSize = readInt();   SvF.TabString = ' ' * TabSize;  continue
            elif Is(Q, "Default_step"):
                SvF.Default_step = readFloat();  continue
            elif Is(Q, "OptMode"):
                SvF.OptMode = readEqStr(); continue

            Swr('SvF.' + coMembers[n] + ' = ' + buf)
#            print ('QQQQQQQQQQQQMEM', Q, buf)
        buf = ''
#    if   Is(Q, "TaskName" )   : SvF.TaskName = readEqStr(); nSwr( 'SvF.TaskName = \''+SvF.TaskName+'\''); nSwr( 'print(SvF.TaskName)')
    elif Is(Q, "ChDir" )      :
                    new_cwd = readEqStr()  #; print ('AAA', new_cwd)
                    os.chdir(new_cwd);   sys.path.append(os.getcwd())
#                    printS ( '*******************  change CWD:', getcwd() )
    elif Is(Q, "SetStartDir") :
                    os.chdir(SvF.startDir);
    elif Is(Q, "DataLineWidth"): print ( '*********************** use DLW' );  exit (-1)  ##########################

    elif(Is(Q, "GRID:") or
         Is(Q, "SET:")  ) :
 #                   buf = Treat_FieldNames(buf)
#                    WriteGrid27 ( buf )
                    WriteSet_24_12(Treat_FieldNames(buf))

    elif Is(Q, "DOMAIN:"): WriteDomain_24_12(Treat_FieldNames(buf))

    elif Is(Q, "VAR:"   ) :  WriteVarParam26 ( buf, False )
    elif Is(Q, "PARAM:" ) :  WriteVarParam26 ( buf, True )
    elif Is(Q, "EQ:")     :  WriteModelEQ31 ( buf )

    elif (Is(Q, "PENALTY:")
       or Is(Q, "OPTPAR:") ):
                                  WritePenalty ( buf )

    elif Is(Q, "OBJL:" )  :  WriteModelOBJ19 ( Q,buf )
    elif Is(Q, "OBJU:" )  :
                            WriteModelOBJ_U (buf)
 ##                           if not SvF.Preproc :  SvFstart19p(Task)
    elif Is(Q, "OBJ:" ):
                            WriteModelOBJ19 ( Q,buf )
##                            if not SvF.Preproc : SvFstart19p ( Task )
    elif(Is(Q, "EoF") or
         Is(Q, "EoTask") ):
#                        if objective == 'N':  buf = 'OBJ: N';
                        print ('OptMode', SvF.OptMode)
                        print ('EoF ************', Q, ' in READ MNG ********************* EoF')
                        if not SvF.SModelFile is None:  SvF.SModelFile.close()
                        if Q == 'EOTASK' :  SvF.EofTask = True
                        else:               SvF.EofTask = False
 #                       SvF.Compile = False
                        return Task

    elif Is(Q, 'CV:'):  WriteCV (Treat_FieldNames(buf))

    elif Is(Q, "MakeSets_byParam") :                #  out of date      24-12-26
            args = buf.split(' ');  #args[0] = '\''+ args[0] + '\''
            SvF.numCV += 1
            col_name = '.dat(\''+args[0]+'\')'
            Swr('SvF_MakeSets_byParam ( SvF.curentTabl'+col_name+', '+','.join(args[1:])+' )' )
            wr('    Gr.mu'+str(SvF.numCV)+' = py.Param ( range(SvF.CV_NoRs['+str(SvF.numCV)+']), mutable=True, initialize = 1 )')   #  23.11

    elif Is(Q, "MakeSets_byParts") :                #  out of date      24-12-26
            args = buf.split(' ')
            SvF.numCV += 1
            Swr('SvF.ValidationSets, SvF.notTrainingSets = MakeSets_byParts ( SvF.curentTabl.NoR, '+','.join(args)+' )' )
            wr('    Gr.mu'+str(SvF.numCV)+' = py.Param ( range(SvF.CV_NoRs['+str(SvF.numCV)+']), mutable=True, initialize = 1 )')   #  23.11
    elif Is(Q, "WriteSvFtbl" ):
                    Swr( '\nSvF.curentTabl.WriteSvFtbl (  \'' + buf + '\' )')
## 30                    if not SvF.Preproc: SvF.curentTabl.WriteSvFtbl ( readEqStr() )
    elif Is(Q, "DataPath")  : SvF.DataPath = readEqStr(); nSwr( 'SvF.DataPath = \''+SvF.DataPath+'\'')
    elif Is(Q, "SavePoints" )     :
                        if len (buf) >= 4 :  SvF.SavePoints = readBool()
                        else              :  SvF.SavePoints = True;
                        nSwr( 'SvF.SavePoints = ' + str(SvF.SavePoints) )

 #   elif Is(Q, "SaveDeriv" )  :  SvF.SaveDeriv = True; nSwr( 'SvF.SaveDeriv = True')
    elif Is(Q, "CODE:") or Is(Q, "Code:"):
                            r_line = raw_line.split("CODE:")
                            if len(r_line)==2 : raw_line = r_line[1]    # 17.01.22 убираем CODE:
                            WriteModelCode26 ( raw_line ) #buf )
    elif Is(Q, "EoD")   :    SvF.curentTabl = None;   Swr('SvF.curentTabl = None')

############################################# 27
    elif Is(Q, "TBL:") :  Tab.TblOperation(buf)
    elif Is(Q, "DEF:") :  WriteModelDef26 ( buf )
    elif Is(Q, "Hack_Stab"       ) :  SvF.Hack_Stab  = bool(readStr()=='True');
    elif Is(Q, "CVNoBorder" )   :  SvF.CVNoBorder    = True
    elif Is(Q, "NotCulcBorder") :  SvF.NotCulcBorder = True
    elif qlf == "TASK"          :  SvF.Task.Name = readEqStr(); print (SvF.Task.Name)
    elif Is(Q, "SaveSol") :
                            if len(buf) == 0 :  Task.SaveSol()
                            else             :  getFun(readStr()).SaveSol('')
    elif Is(Q, "Prefix"   )    :  SvF.Prefix = readStr()

 #   elif Is(Q,"OptMode")     : SvF.OptMode = readEqStr()

    else :
            raw_upp = raw_line.upper()
            if raw_upp.find('SELECT ') >= 0:
                #         print (raw_line)
                WriteSelect30(Treat_FieldNames(raw_line))
            elif raw_upp.find('TABLEWHERE') >= 0:
                WriteTable30(Treat_FieldNames(raw_line))
            else :
#                print ('\nraw_line       =', raw_line)
                WriteString31(raw_line)
            buf = ''
    if EmptyBuf : buf = ''



 while 0 :  ######################################################################################

    if Is(Q,"Polygon") :
                            defName = readStr()
                            defList = ReadPolygon(DataR.InFile)
 ## 30                           Task.AddDef(defName, defList)
    elif Is(Q,"getMinMax") :
                    dn = Task.getDefNum(readStr())
     ## 30               rect = getMinMax(Task.Def[dn][1][:])
                    Task.Def[dn][1] = rect
#                    print 'MinMax', rect
    elif Is(Q,'GetRectLastFunc' ):
                        defName = readStr()
                        defList = [Task.Funs[0].A[0].min,Task.Funs[0].A[1].min,
                                   Task.Funs[0].A[0].max,Task.Funs[0].A[1].max]
    #                    print defName, defList
    ## 30                    Task.AddDef(defName, defList)
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
                    rect[2] = val * np.ceil (rect[2]/val)
                    rect[3] = val * np.ceil (rect[3]/val)
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


    elif qlf == "VARNORMALIZATION" :  SvF.VarNormalization = True

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

##def  SvFstart19p ( Task ):
## 30        from SvFstart62 import SvFstart19  #*
  ##      SvFstart19 ( Task )

