# -*- coding: UTF-8 -*-

from  numpy import *

#from InData import *
from Lego   import *
from Tools  import *

import COMMON as co

 ############################## 20 #################################
def AddMargin ( tSet, CVmargin, NoR ) :
    old_e = -1
    retSet = []
    for elem_t in tSet :
        retSet.append([])
        for ne in range(len(elem_t)) :
            befo = False
            afte = False
            if ne == 0 :
                if elem_t[ne] > 0:      befo = True
            elif ne == len(elem_t)-1 :
                if elem_t[ne] < NoR-1:  afte = True
            elif elem_t[ne] > elem_t[ne-1]+1 :
                befo = True
                afte = True
            if afte :
                for m in range (CVmargin) :
                    if elem_t[ne-1]+m+1 >= NoR :  break
                    retSet[-1].append(elem_t[ne-1]+m+1)
            if befo :
                for m in range (CVmargin) :
                    if elem_t[ne]+m-CVmargin < 0 : continue
                    retSet[-1].append(elem_t[ne]+m-CVmargin)
            retSet[-1].append(elem_t[ne])
        retSet[-1] = list(set(retSet[-1]))
    return  retSet                             


def MakeSets_byParam ( curTab, CVparam, CVstep=0, CVmargin=0) :   #  sort if margin !
    num = curTab.getFieldNum ( CVparam )      #IndexCol( CVparam )
    if num < 0 :
        print ("Unknown  Param", CVparam)
        exit(-1)
    if co.printL :  print ('MakeSets_byParam',  CVparam, CVstep, CVmargin, 'tbl_num', num,)

    NoR = curTab.NoR
    subTbl = curTab.Flds[num].tb
     
    unique_par = list(set(subTbl.tolist()))
    if co.printL : print ('unique_par', len(unique_par), unique_par)
    
    if CVstep <= 0 : CVstep = len (unique_par) # каждое значение - множество
    else :           CVstep = int( CVstep )

    testSet = []
    for s in range(CVstep) : testSet.append ([])

    for num in range ( NoR ) :
        testSet[unique_par.index(subTbl[num]) % CVstep].append(num)

    if CVmargin == 0 :
        teachSet =  testSet
    else :
        teachSet = AddMargin ( testSet, CVmargin, NoR )
                        
        
#    print len(unique_par), 'sizes test/teach',
    if co.printL > 0 :
        for s in range(CVstep) : print (str(len(testSet[s]))+'/'+str(len(teachSet[s])),)
    co.CV_NoR = NoR
    co.CV_NoSets = len (testSet)
    print ("EofMakeSets_byParam, Unique param.num =", len(unique_par), 'Parts=', CVstep, "\n")
    return testSet, teachSet
    
                                                        # MakeSets_byParts 7 1583  - 7 раз по 1583 (полтлра литра :)
def MakeSets_byParts ( NoR, CVstep=7, CVpart_size=1, CVmargin=0) :
    print  (CVpart_size, CVstep, CVmargin,)

    if CVstep == 0 : CVstep = ceil (NoR/CVpart_size) #
    else :           CVstep = int( CVstep )

    testSet = []
    for s in range(CVstep) : testSet.append ([])

    n = 0
    num = 0
    while (1) :
        nS = n % CVstep
        for p in range(CVpart_size) :
            testSet[nS].append(num)
            num += 1
            if num == NoR: break
        if num == NoR: break
        n += 1
    if CVmargin == 0 :
        teachSet =  testSet
    else :
        teachSet = AddMargin ( testSet, CVmargin, NoR )
                        
    co.CV_NoR = NoR
    co.CV_NoSets = len (testSet)

    for s in range(CVstep) : print (str(len(testSet[s]))+'/'+str(len(teachSet[s])),)
    print ("END of MakeSets_byParam")
    return testSet, teachSet



#    удалено в 27
#  def CV_Sets(Fun0 ) :  удалено в 27
#  def  makeParamSets ( Fun0, CVparam, CVstep ) :
#  def makeStepSets ( NoR, CVstep ):
#  def makePartSets ( NoR, CVpartSize, CVside ) :
