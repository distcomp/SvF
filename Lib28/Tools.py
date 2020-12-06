# -*- coding: cp1251 -*-

from  numpy import *
import sys

FLOMAX = sys.float_info.max

def tetta (x) :
    return 0.5 + 0.5 * x / (.001+x*x)**0.5
#    return 0.5 + 0.5 * x / sqrt (.001+x*x)


def tetta_old (x) :
    if   x < 0 :  return 0
    elif x > 0 :  return 1
    else       :  return 0.5

def floatGradNaN ( txt ) :
        try:
            return float(txt)
        except:
#            if txt is None: return NaN
            print ('TXT',txt)
            try :
                gra = txt.index('°')
                print ('TXT',txt,gra)
                if gra >= 0:
                    return float(txt[:gra]) + float(txt[gra + 1:]) / 60.
            except:   return NaN


def strTOnum (txt) :
    num = 0
    for i, s in enumerate (txt) : num = num * 256 + ord(s)
    return num

def numTOstr (num) :
    txt = ''
    while num > 0 :
        txt = chr (num%256) + txt
        num = num // 256
    return txt

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def printS ( *ss ) :    # если в конце собранной строки стоит '|' - то нет '\n'
    st = ''
    for i,s in enumerate(ss) :
        if i!=0 : st += ' ' + str(s)
        else    : st += str(s)
    if st[-1] == '|' :  st =  st[:-1]
    else             :  st += '\n'
    sys.stdout.write(st)
    return

                                            #  1-ЫЙ столбец НЕ отделяет !
def ReadSvF ( ReadFrom, printL=0 ) :      # return ftype, vers, cols, x1, tbl
        ftype = 'tbl'
        vers  = 0
        x1 = []
        try :
            fi = open ( ReadFrom, "r")
        except IOError as e:
            print ("не удалось открыть файл", ReadFrom)
            return None, None, None, None, None;
        else :
            if printL : print ("ReadSol from", ReadFrom, )
            cols = fi.readline().split()
            if isfloat(cols[0]) :                       # это число а не имя - таблица без назв столбцов
                fi.seek(0)
                tbl = loadtxt (fi,'double')
                cols = ['name'+str(c) for c in range(tbl.shape[1]) ]
            else :
                for c in cols :
                    if c.find ('#SvFver_') >= 0 :
                        parts = c[8:].split('_')
                        vers = int(parts[0])
                        ftype = parts[1]
                if vers == 0 :                          # file without '#SvFver_'
                    tbl = loadtxt (fi,'double')
                else :         
                    cols = cols[:-1]
                    if ftype == 'tbl' :                             # tbt
                        tbl = loadtxt (fi,'double')
                    else :                                          # matr2
                        x1_txt = fi.readline().split()
                        x1 = [ float(x) for x in x1_txt ]
                        tbl = loadtxt (fi,'double')
            if printL : print  (str(vers)+'_'+ftype, 'names:', cols, "shape", tbl.shape)
            return ftype, vers, cols, x1, tbl

def WriteSvFtbl ( OutName, cols, tb, printL=0 ) :    
    with open(OutName,'w') as f:
        for c in cols : print >>f, c,
        print >>f, '#SvFver_62_tbl',
        for s in range ( tb.shape[0] ) :
            print >>f, ''
            for c in range ( tb.shape[1] ) : 
                print >>f, '\t', tb[s,c],
    if printL : print ("Write to", OutName, '62_tbl', 'names:', cols, "shape", tb.shape)





