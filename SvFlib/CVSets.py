# -*- coding: UTF-8 -*-

#from  numpy import *
import numpy as np

#from InData import *
from Lego   import *
from Tools  import *

import COMMON as SvF

def CVmakeSets ( NoR =0, CV_NumSets =7, CV_Unit=1,  CV_Margin=0, NumOfIter=None ) :  #, CV_Border=None ) :
    if not isnotNone(NumOfIter):  SvF.CVNumOfIter = NumOfIter
    if type(CV_Unit) is type(1):
        if NoR == 0:
            if SvF.curentTabl is None:
                print ('SvF.curentTabl is None')
                return
            NoR = SvF.curentTabl.NoR
        CVarray = [ int(i/CV_Unit) for i in range(NoR)]
        print (CVarray)
    else:
        if type(CV_Unit) is str:
            CV_Unit = SvF.curentTabl.dat(CV_Unit)
        CVarray = CV_Unit.tolist()

    NoR = len(CVarray)
#    print ('CVarray',CVarray)
    unique_par = list(set(CVarray))
    print('unique_par', NoR, len(unique_par), unique_par)

    CV_NumSets = min (len(unique_par), int(CV_NumSets))

    SvF.ValidationSets = [[] for _ in range(CV_NumSets)]
    for num in range(NoR):
        SvF.ValidationSets[unique_par.index(CVarray[num]) % CV_NumSets].append(num)
#    print ('**************ValidationSets',SvF.ValidationSets)

    SvF.notTrainingSets = deepcopy (SvF.ValidationSets)

    if CV_Margin > 0 :
        for s in range (CV_NumSets) :
            set_nTrain = set ()
            for i in SvF.notTrainingSets[s] :
                for ad in range (i-CV_Margin,i+CV_Margin+1):
                    if ad >= 0 and ad < NoR :  set_nTrain.add (ad)
            SvF.notTrainingSets[s] = list(set_nTrain)
#    print ('*********************** notTrainingSets *******',SvF.notTrainingSets)

    SvF.TrainingSets = [[] for _ in range(CV_NumSets)]
    for s in range(CV_NumSets):
        SvF.TrainingSets[s] = Substract (range(NoR), SvF.notTrainingSets[s])  #[x for x in range(NoR) if x not in ValidationSets[set] ]
#    print ('********************** TrainingSets ***',SvF.TrainingSets)

    SvF.CV_NoRs.append(NoR)
    print ('CVmakeSets    SvF.CV_NoRs', SvF.CV_NoRs, CV_NumSets)
    SvF.CV_NoSets = len (SvF.ValidationSets)

 ############################## 21.10 #################################
def make_CV_Sets ( NoR =0, NoSubSets =7, ValidationPartSize=1,  Data =None, Margin=0, Border=None ) :
 #   print (NoR, Param, Data)
    if Data is None :
        if NoR == 0:
            if SvF.curentTabl is None:
                print ('SvF.curentTabl is None')
                return
            NoR = SvF.curentTabl.NoR
        MakeSets_byParts(NoR, NoSubSets, ValidationPartSize, Margin)
    else :
        if type(Data) is str:
            Data = SvF.curentTabl.dat(Data)
        SvF_MakeSets_byParam( Data, NoSubSets, Margin, Border )


    #elems
def AddMarginBor ( tSet, CVmargin, NoR, border=None ) :   #  tSet  [ [...], [...] ... [...] ]
    notTrainingSets = deepcopy(tSet)                                  #  e
    for ne, elems in enumerate(tSet) :
        for e in elems :
            for m in range(1,CVmargin+1) :
                num = e+m
                if num >= NoR : break
                if ( not border is None) and border[num] and border[num-1] :  break
                notTrainingSets[ne].append(num)
            for m in range(1,CVmargin+1) :
                num = e-m
                if num < 0 : break
                if ( not border is None) and border[num] and border[num+1] :  break
#                if( not border is None) and border[num] : break
                notTrainingSets[ne].append(num)
        notTrainingSets[ne] = sorted(list( set (notTrainingSets[ne]) ) )  # убирает повторы и сортирует
    return  notTrainingSets


                        # CVstep = NoSubSets
def SvF_MakeSets_byParam( arr, CVstep=0, CVmargin=0, border=None ):  # sort if margin !
    if SvF.printL:  print('MakeSets_byParam', CVstep, CVmargin )

    NoR = len(arr)
    unique_par = list(set(arr.tolist()))
    print('unique_par', len(unique_par), unique_par)

    if CVstep <= 0:
        CVstep = len(unique_par)  # каждое значение - множество
    else:
        CVstep = int(CVstep)

    ValidationSets = [[] for _ in range(CVstep)]
    for num in range(NoR):
        ValidationSets[unique_par.index(arr[num]) % CVstep].append(num)

    TrainingSets = [[] for _ in range(CVstep)]

    for set in range(CVstep):
        TrainingSets[set] = Substract (range(NoR), ValidationSets[set])  #[x for x in range(NoR) if x not in ValidationSets[set] ]
    print ('********************************************',TrainingSets[set])


    if CVmargin == 0:
        notTrainingSets = ValidationSets  # notTrainingSets содержит кого выбрасываем, т.е учим на тех кто не попал в notTrainingSets
    else:
        notTrainingSets = AddMarginBor(ValidationSets, CVmargin, NoR, border)

    #    print len(unique_par), 'sizes test/teach',
    if SvF.printL > 0:
        for s in range(CVstep): print(str(len(ValidationSets[s])) + '/' + str(len(notTrainingSets[s])), )
    SvF.CV_NoRs.append(NoR)
    SvF.CV_NoSets = len(ValidationSets)
    SvF.ValidationSets  = ValidationSets    #  номера точек тестирования
    SvF.notTrainingSets = notTrainingSets   #  номера точек которые выбрасываются
    SvF.TrainingSets = TrainingSets
    print("EofMakeSets_byParam, Unique param.num =", len(unique_par), 'Parts=', CVstep, "\n")
#    for nSet in range (CVstep) :
 #          print (nSet, ' ValidationSets', ValidationSets[nSet], '\n   notTrainingSets', notTrainingSets[nSet] )
  #  1/0


                                                    # MakeSets_byParts 7 1583  - 7 раз по 1583 (полтлра литра :)
def MakeSets_byParts ( NoR, CVstep=7, CVpart_size=1, CVmargin=0) :
    print  (CVpart_size, CVstep, CVmargin)

    if CVstep == 0:  CVstep = int(np.ceil (NoR/CVpart_size))
    else:            CVstep = int( CVstep )

    ValidationSets = [[] for _ in range(CVstep)]

    n = 0
    num = 0
    while (1) :
        nS = n % CVstep
        for p in range(CVpart_size) :
            ValidationSets[nS].append(num)
            num += 1
         #   print (nS,num, CVstep, NoR)
            if num == NoR: break
        if num == NoR: break
        n += 1
    if CVmargin == 0:
        notTrainingSets = ValidationSets
    else :
        notTrainingSets = AddMarginBor ( ValidationSets, CVmargin, NoR )

    TrainingSets = [[] for _ in range(CVstep)]
    for set in range(CVstep):
        TrainingSets[set] = Substract (range(NoR), ValidationSets[set])  #[x for x in range(NoR) if x not in ValidationSets[set] ]
    print ('********************************************',TrainingSets[set])

#    for set in range(CVstep):
 #       TrainingSets[set] = [x for x in range(NoR) if x not in notTrainingSets[set] ]

    SvF.CV_NoRs.append(NoR)
    print ('SvF.CV_NoRs', SvF.CV_NoRs)
    SvF.CV_NoSets = len (ValidationSets)

    for s in range(CVstep) : print (str(len(ValidationSets[s]))+'/'+str(len(notTrainingSets[s])),)
    print ("END of MakeSets_byParam")
    SvF.ValidationSets  = ValidationSets
    SvF.notTrainingSets = notTrainingSets
    SvF.TrainingSets = TrainingSets

#    return ValidationSets, notTrainingSets



#    удалено в 27
#  def CV_Sets(Fun0 ) :  удалено в 27
#  def  makeParamSets ( Fun0, CVparam, CVstep ) :
#  def makeStepSets ( NoR, CVstep ):
#  def makePartSets ( NoR, CVpartSize, CVside ) :
