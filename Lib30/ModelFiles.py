# -*- coding: UTF-8 -*-
from __future__ import division
#from  numpy import *
from  time import *
#import os
from  os  import listdir, getcwd, chdir
from  sys import *

from Object import *


from Lego import *
from Task import *
from CVSets import *
from GaKru import *
from Tools import *
import Table as Tab
from MakeModel import *
from Pars      import *
from Parser    import *

#from PyomoEverestEnv  import *
#import COMMON as co

import io

import ezodf

def MngFile ( ) :
    if  len(argv)>1 :  return argv[1]
    else :
        mngF = []
        files = listdir(getcwd())
        print('Choiсe file number: ')
        for f in files:
            p = f.rfind('.')
            if p >=0 :
                if f[p:] == '.mng' or f[p:] == '.odt':
                    mngF.append (f)
                    print('   ', len(mngF), ' - ', f)
        if len (mngF) > 1:  file_num = int(input())-1
        else :              file_num = 0
        print('\n********************** menu file = ', mngF[file_num], '********************')
        return mngF[file_num]



def isASCII():
    try:
        fi = open(mngF)
        fi.readline().decode('ASCII')
    except UnicodeDecodeError:
        print('UTF-8')
        fi.close()
        return False
    else:
        print('ASCII')
        fi.close()
        return True


leve = 0

def allText ( i, txt) :
    global leve
#    print(leve, 'kind:  ', i.kind, '   tail:  ', i.tail, '   text:  ', i.plaintext(), i.__len__() )  #, i.get_attr('./Object 1'), i.get_attr('.//Object 1'), i.get_attr('href='))
#    print ('Allt:'+txt+'E')
#    if i.kind == 'Span' : return txt  #  будь остарожен там может быть формула
#    print('txt000000', leve, txt)
    if i.kind != 'Span' : txt += i.plaintext()
 #   print('txt111111', leve, txt)
    leve += 1
    for ich in range ( i.__len__() ) :
        ch = i.get_child(ich)
        txt =  allText ( ch, txt)
  #      print ('txt222222', leve, txt )
    leve -= 1
    return txt

def print_Child (i) :
    global leve
    print('Parag:', leve, 'kind:  ', i.kind, '   tail:  ', i.tail, '   text:'+i.plaintext()+'E', i.__len__() )  #, i.get_attr('./Object 1'), i.get_attr('.//Object 1'), i.get_attr('href='))
    leve += 1
    for ich in range ( i.__len__() ) :
      ch = i.get_child(ich)
      print_Child (ch)
    leve -= 1


global lines_buf
#lines = []
lines_buf = []
global lines_pos
lines_pos = -1

def readMNGfile ( fName ):
    lines_buf = []
    print ('fNane', fName)
    if fName.count('.odt'):
        fi = ezodf.opendoc(fName)
        start = False
        for odtParag in fi.body :
            if not start :                                      #  мотаем до BoF-SvF
                if allText(odtParag, '').find('BoF-SvF') == 0:
#                    print('START  BoF-SvF')
                    start = True
                continue
            ret = allText(odtParag, '')
#           print_Child ( odtBody[parag] )
#            print('MNGreadlineIn:' + ret + 'Len', len(ret))
            p = ret.find('TexMaths')
            if p >= 0:
                    #              while ret[p]
 #                   print ('ret0000', ret)
                    p_dol = ret.find('§', p)
                    p_dol2 = ret.find('§', p_dol + 1)
                    ret = ret[:p] + ret[p_dol2 + 1:]
                    p = p_dol = ret.find('§')
                    ret = ret[:p]
#                    print('\nTEXMATHS:' + ret)
                    ret = UTF8replace(ret, '\\begin{array}{l}', '')
                    ret = ret.replace('\\begin{array}{l}', '')
                    ret = ret.replace('\\begin{array}{c}', '')
                    ret = ret.replace('\\end{array}', '')
                    ret = ret.replace('\\\\', '')
#                    print('END_TEXMATHS:' + ret)
            if ret != '' :
                lines_buf.append(ret)
                if len(ret) >= 3:
                    if ret[:3] == 'EOF': break
    ###            fi.close()  #  ???????       &&&&&&&&&&&&&&&
    else:  # mng
        if sys.version_info.major == 3:
            fi = open(fName)  # python 3
        else:
            if isASCII():
                fi = open(fName)  # python 2
            else:
                fi = io.open(fName, encoding='utf-8')
        lines_buf = fi.readlines()
        fi.close()
##    tab_str = ' ' * SvF.TabSize
    buf = []
    for l in lines_buf:
        line_b = l.rstrip()  # убираем послед. пробелы и т.д
        line_b = line_b.replace('\t', SvF.TabString )  # заменяем табы
        if len(line_b.replace(' ', '')): buf.append(line_b)  # не добавляем строки из пробелов
#    lines_buf = buf

    return buf



def MNGreadline():
    global lines_buf
    global lines_pos

    if lines_pos == -1 :  lines_buf = readMNGfile(SvF.mngF)

    lines_pos += 1
    if lines_pos >= len(lines_buf)  : return 'EOF'
    if lines_buf[lines_pos].upper().find('FOR:') == 0 :       #  INDEX:   FOR:  CC in [ITA, RUS] :
        index_list = lines_buf[lines_pos].strip().split()     #            0    1  2    3
#        print (index_list)
        begin_pos = lines_pos + 1
        end_pos   = begin_pos
        otstup = 0
        while lines_buf[end_pos][otstup] == ' ': otstup += 1
#        print ('otstup', otstup, '|'+lines_buf[end_pos]+'|' )
        if otstup > 0:
            while lines_buf[end_pos][0] == ' ': end_pos += 1
            insert_pos = end_pos
        else :
            while lines_buf[end_pos].find('EOFOR') != 0: end_pos += 1
            insert_pos = end_pos + 1
        for i in range (3,len(index_list)) :
#            print('B',i, index_list[i])
            if index_list[i][ 0] == '[':    index_list[i] = index_list[i][1:]
            if len(index_list[i]) == 0: continue
            if index_list[i][-1] == ':':    index_list[i] = index_list[i][:-1]
            if len(index_list[i]) == 0: continue
            if index_list[i][-1] == ']':    index_list[i] = index_list[i][:-1]
            if len(index_list[i]) == 0: continue
   #         print(i, index_list[i])
            for j in range (begin_pos,end_pos) :
 #               print ('LB'+lines_buf[j]+'|')
                lines_buf.insert(insert_pos,lines_buf[j][otstup:].replace(index_list[1],index_list[i]))
                insert_pos += 1
        if otstup :
            for j in range(begin_pos-1, end_pos):  lines_buf[j] = '#   ' + lines_buf[j]
        else :
            for j in range(begin_pos-1, end_pos+1):  lines_buf[j] = '#   ' + lines_buf[j]
    else :                                                          #  while - если вложенные INCLUDE:
      while lines_buf[lines_pos].upper().find('INCLUDE:') == 0 :   #  INCLUDE:   file_incl_name
        incl_name = lines_buf[lines_pos].strip().split()[1]
        lines_buf[lines_pos] = '# ' + lines_buf[lines_pos]
        incl_buf = readMNGfile(incl_name)
        for nl, l in enumerate( incl_buf ):     #  вставка новых в буфер
            lines_buf.insert(lines_pos+nl, l ) #l.rstrip('\n'))
#        print('END_INCLUDE:::', incl_name, lines_buf[lines_pos] )
    return lines_buf[lines_pos]



def Swr(str):
    if SvF.SModelFile is None : startStartModel ()
    SvF.SModelFile.write('\n' + str)

def Swrs(str):
    if SvF.SModelFile is None : startStartModel ()
    SvF.SModelFile.write(str)

def nSwr(a1,a2='',a3=''):
    if SvF.SModelFile is None : startStartModel ()
    SvF.SModelFile.write( '\n'+str(a1)+str(a2)+str(a3) )

def startStartModel () :
#    print (getcwd(), ')))))))))))))))))))))))))))))))))))))))))))))))))))')
    SvF.SModelFile = open('StartModel.py', 'w')
    Swrs('# -*- coding: UTF-8 -*-')
#    Swr('BIsum = sum')
    Swr('import sys')
    Swr('import platform')
    Swr('LibVersion = \'Lib29\'')
    Swr('if platform.system() == \'Windows\':')
    Swr('    path_SvF = \"C:/_SvF/\"')
    Swr('else:')
    # Swr('    path_SvF = \"/home/sokol/C/_SvF/\"')
    Swr('    path_SvF = \"' + SvF.path_SvF + '\"')
    Swr('sys.path.append(path_SvF + LibVersion)')
    Swr('sys.path.append(path_SvF + \"Everest/python-api\")')
    Swr('sys.path.append(path_SvF + \"pyomo-everest/ssop\")')
    Swr('import COMMON as SvF')
    Swr('SvF.path_SvF = path_SvF')
    Swr('SvF.tmpFileDir = SvF.path_SvF + \'TMP/\'')

    Swr('from CVSets import *')
    Swr('from Table  import *')
    Swr('from Task   import *')
    Swr('from MakeModel import *')
    Swr('from GIS import *')
    Swr('\nSvF.Task = TaskClass()')
    Swr('Task = SvF.Task')
    Swr('SvF.mngF = \'' + SvF.mngF + '\'')
## 30    Swr('SvF.Preproc = False')

def wr(str):
     if SvF.ModelFile is None:  startModel ()
     if SvF.ModelFile == 1:  return
     SvF.ModelFile.write('\n' + str)

def wrs(str):
     if SvF.ModelFile is None:  startModel ()
     if SvF.ModelFile == 1:  return
     SvF.ModelFile.write(str)

def startModel () :
     SvF.ModelFile = open('Model.py', 'w')
     f = SvF.ModelFile
     wr('from __future__ import division')
     wr('from  numpy import *')
 #    wr('import  numpy as np')
     wr('\nfrom Lego import *')
     wr('from pyomo.environ import *')
     wr('\ndef createGr ( Task, Penal ) :')
     wr('    Funs = Task.Funs')
     wr('    Gr = ConcreteModel()')
     wr('    Task.Gr = Gr')
     wr('    if SvF.CV_NoR > 0:')
     wr('        Gr.mu = Param ( range(SvF.CV_NoR), mutable=True, initialize = 1 )')
 #    wr('        for f in Funs :')
  #   wr('            if (not f.param) and (not f.V.dat is None):')
   #  wr('                f.mu  = Gr.mu')
    # wr('                f.testSet  = SvF.testSet')
     #wr('                f.teachSet = SvF.teachSet')

