# -*- coding: UTF-8 -*-

from  numpy import *

#from InData import *
from Lego   import *
from Tools  import *

import COMMON as co

 ############################## 21.10 #################################

                                                               #elems
def AddMarginBor ( tSet, CVmargin, NoR, border ) :   #  tSet  [ [...], [...] ... [...] ]
    teachSet = deepcopy(tSet)                                  #  e
    for ne, elems in enumerate(tSet) :
        for e in elems :
            for m in range(1,CVmargin+1) :
                num = e+m
                if num >= NoR : break
                if ( not border is None) and border[num] and border[num-1] :  break
                teachSet[ne].append(num)
            for m in range(1,CVmargin+1) :
                num = e-m
                if num < 0 : break
                if ( not border is None) and border[num] and border[num+1] :  break
#                if( not border is None) and border[num] : break
                teachSet[ne].append(num)
        teachSet[ne] = sorted(list( set (teachSet[ne]) ) )
    return  teachSet



def SvF_MakeSets_byParam( arr, CVstep=0, CVmargin=0, border=None ):  # sort if margin !
    if co.printL:  print('MakeSets_byParam', CVstep, CVmargin )

    NoR = len(arr)
    unique_par = list(set(arr.tolist()))
    if co.printL: print('unique_par', len(unique_par), unique_par)

    if CVstep <= 0:
        CVstep = len(unique_par)  # каждое значение - множество
    else:
        CVstep = int(CVstep)

    testSet = []
    for s in range(CVstep): testSet.append([])

    for num in range(NoR):
        testSet[unique_par.index(arr[num]) % CVstep].append(num)

    if CVmargin == 0:
        teachSet = testSet  # teachSet содержит кого выбрасываем, т.е учим на тех кто не попал в teachSet
    else:
        teachSet = AddMarginBor(testSet, CVmargin, NoR, border)

    #    print len(unique_par), 'sizes test/teach',
    if co.printL > 0:
        for s in range(CVstep): print(str(len(testSet[s])) + '/' + str(len(teachSet[s])), )
    co.CV_NoR = NoR
    co.CV_NoSets = len(testSet)
    co.testSet  = testSet
    co.teachSet = teachSet
    print("EofMakeSets_byParam, Unique param.num =", len(unique_par), 'Parts=', CVstep, "\n")
#    for nSet in range (CVstep) :
 #          print (nSet, 'testSet', testSet[nSet], '\nteachSet', teachSet[nSet] )
 #   1/0


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
