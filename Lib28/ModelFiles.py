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

#from PyomoEverestEnv  import *
import COMMON as co

import io

import ezodf

def MngFile ( ) :
    if  len(argv)>1 :  co.mngF  = argv[1]
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
        co.mngF = mngF[file_num]
    print('\n********************** menu file = ', co.mngF, '********************')


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
    if i.kind != 'Span' : txt += i.plaintext()
    leve += 1
    for ich in range ( i.__len__() ) :
        ch = i.get_child(ich)
        txt =  allText ( ch, txt)
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

#global fi
#fi = None
#global odtBody
#global parag
#parag = 0

global lines_buf
#lines = []
lines_buf = []
global lines_pos
lines_pos = -1

def MNGreadline():
    global lines_buf
    global lines_pos

 #   global fi
#    global odtBody
#    global parag
    parag = 0
    if lines_pos == -1 :
 #   if fi is None:  # открытие файла
        if co.mngF.count('.odt'):
            fi = ezodf.opendoc(co.mngF)
            odtBody = fi.body
            while allText(odtBody[parag], '').find('BoF-SvF') != 0:
                #                    print (allText(odtBody[parag], ''))
                parag += 1
            print('START  BoF-SvF')
##        if co.mngF.count('.odt'):  # чтение файла            НЕ ТЕСТИРОВАННО      !!!!!!!!!!!!!!!
            while (1) :
              ret = ''
              while ret == '':
                parag += 1
                ret = allText(odtBody[parag], '')
                #            print_Child ( odtBody[parag] )
                print('MNGreadlineIn:' + ret + 'Len', len(ret))
                p = ret.find('TexMaths')
                if p >= 0:
                    #              while ret[p]
                    #               print (ret)
                    p_dol = ret.find('§', p)
                    p_dol2 = ret.find('§', p_dol + 1)
                    ret = ret[:p] + ret[p_dol2 + 1:]
                    p = p_dol = ret.find('§')
                    ret = ret[:p]
                    print('END_TEXMATHS:' + ret)
            #               1/0
              lines_buf.append( ret )
              if len(ret)>=3 :
                  if ret[:3] == 'EOF' : break
###            fi.close()  #  ???????       &&&&&&&&&&&&&&&
        else:  # mng
            if sys.version_info.major == 3:
                fi = open(co.mngF)  # python 3
            else:
                if isASCII():
                    fi = open(co.mngF)  # python 2
                else:
                    fi = io.open(co.mngF, encoding='utf-8')
            lines_buf = fi.readlines()
            for nl,l in enumerate(lines_buf) : lines_buf[nl] = l.rstrip()     # убираем послед. пробелы и т.д
            fi.close()
    lines_pos += 1
    if lines_pos >= len(lines_buf)  : return 'EOF'
    if lines_buf[lines_pos].upper().find('FOR:') == 0 :       #  INDEX:   FOR:  CC in [ITA, RUS] :
        index_list = lines_buf[lines_pos].strip().split()     #            0    1  2    3
#        print (index_list)
        begin_pos = lines_pos + 1
        end_pos   = begin_pos + 1
        while lines_buf[end_pos].find('EOFOR') != 0: end_pos += 1
        insert_pos = end_pos + 1
        for i in range (3,len(index_list)) :
            print('B',i, index_list[i])
            if index_list[i][ 0] == '[':    index_list[i] = index_list[i][1:]
            if len(index_list[i]) == 0: continue
            if index_list[i][-1] == ':':    index_list[i] = index_list[i][:-1]
            if len(index_list[i]) == 0: continue
            if index_list[i][-1] == ']':    index_list[i] = index_list[i][:-1]
            if len(index_list[i]) == 0: continue
   #         print(i, index_list[i])
            for j in range (begin_pos,end_pos) :
                lines_buf.insert(insert_pos,lines_buf[j].replace(index_list[1],index_list[i]))
                insert_pos += 1
        for j in range(begin_pos-1, end_pos+1):  lines_buf[j] = '#   ' + lines_buf[j]
#        for l in lines_buf :  print (l)
  #      1/0
    return lines_buf[lines_pos]

def MNGreadlineOLD():   ####  KILL
        global fi
        global odtBody
        global parag
        if fi is None:  # открытие файла
            if co.mngF.count('.odt'):
                fi = ezodf.opendoc(co.mngF)
                odtBody = fi.body
                while allText(odtBody[parag], '').find('BoF-SvF') != 0:
                    #                    print (allText(odtBody[parag], ''))
                    parag += 1
                print('START  BoF-SvF')
            else:  # mng
                if sys.version_info.major == 3:
                    fi = open(co.mngF)  # python 3
                else:
                    if isASCII():
                        fi = open(co.mngF)  # python 2
                    else:
                        fi = io.open(co.mngF, encoding='utf-8')
        if co.mngF.count('.odt'):  # чтение файла
            ret = ''
            while ret == '':
                parag += 1
                ret = allText(odtBody[parag], '')
                #            print_Child ( odtBody[parag] )
                print('MNGreadlineIn:' + ret + 'Len', len(ret))
                p = ret.find('TexMaths')
                if p >= 0:
                    #              while ret[p]
                    #               print (ret)
                    p_dol = ret.find('§', p)
                    p_dol2 = ret.find('§', p_dol + 1)
                    ret = ret[:p] + ret[p_dol2 + 1:]
                    p = p_dol = ret.find('§')
                    ret = ret[:p]
                    print('END_TEXMATHS:' + ret)
            #               1/0
            return ret
        else:
            return fi.readline()


def Swr(str):
    if co.SModelFile is None : startStartModel ()
    co.SModelFile.write('\n' + str)

def Swrs(str):
    if co.SModelFile is None : startStartModel ()
    co.SModelFile.write(str)

def nSwr(a1,a2='',a3=''):
    if co.SModelFile is None : startStartModel ()
    co.SModelFile.write( '\n'+str(a1)+str(a2)+str(a3) )

def startStartModel () :
#    print (getcwd(), ')))))))))))))))))))))))))))))))))))))))))))))))))))')
    co.SModelFile = open('StartModel.py', 'w')
    Swrs('# -*- coding: UTF-8 -*-')
#    Swr('BIsum = sum')
    Swr('import sys')
    Swr('import platform')
    Swr('LibVersion = \'Lib28\'')
    Swr('if platform.system() == \'Windows\':')
    Swr('    path_SvF = \"C:/_SvF/\"')
    Swr('else:')
    # Swr('    path_SvF = \"/home/sokol/C/_SvF/\"')
    Swr('    path_SvF = \"' + co.path_SvF + '\"')
    Swr('sys.path.append(path_SvF + LibVersion)')
    Swr('sys.path.append(path_SvF + \"Pyomo_Everest/pe\")')

    Swr('import COMMON as co')
    Swr('co.path_SvF = path_SvF')
    Swr('co.tmpFileDir = co.path_SvF + \'TMP/\'')

    Swr('from CVSets import *')
    Swr('from Table  import *')
    Swr('from Task   import *')
    Swr('from MakeModel import *')
    Swr('from GIS import *')
    Swr('\nco.Task = TaskClass()')
    Swr('Task = co.Task')
    Swr('co.mngF = \'' + co.mngF + '\'')
    Swr('co.Preproc = False')

def wr(str):
     if com.ModelFile is None:  startModel ()
     if com.ModelFile == 1:  return
     com.ModelFile.write('\n' + str)

def wrs(str):
     if com.ModelFile is None:  startModel ()
     if com.ModelFile == 1:  return
     com.ModelFile.write(str)

def startModel () :
     com.ModelFile = open('Model.py', 'w')
     f = com.ModelFile
     wr('from __future__ import division')
     wr('from  numpy import *')
 #    wr('import  numpy as np')
     wr('\nfrom Lego import *')
     wr('from pyomo.environ import *')
     wr('\ndef createGr ( Task, Penal ) :')
     wr('    Funs = Task.Funs')
     wr('    Gr = ConcreteModel()')
     wr('    Task.Gr = Gr')
     wr('    if com.CV_NoR > 0:')
     wr('        Gr.mu = Param ( range(com.CV_NoR), mutable=True, initialize = 1 )')
 #    wr('        for f in Funs :')
  #   wr('            if (not f.param) and (not f.V.dat is None):')
   #  wr('                f.mu  = Gr.mu')
    # wr('                f.testSet  = co.testSet')
     #wr('                f.teachSet = co.teachSet')

