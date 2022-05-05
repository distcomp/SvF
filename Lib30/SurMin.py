# -*- coding: cp1251 -*-
from __future__ import division
from  numpy import *
from copy   import *
from pyomo.environ import *
from pyomo.opt import SolverFactory

from SolverTools import *

import COMMON as co


#   for index, string in enumerate(strings):
#   np.linspace(0, 2, 9)  # 9 чисел от 0 до 2 включительно

# Аппроксимация полиномом 2 степени pol ( C, B1, B2) 
# 1) Стартовая процедура - набирается пул точек  B1i, B2i, SIGi
# 2) Набранные значения аппроксимируются поверхностью 2-ого порядка:
#    - точки учитываются с разными весами (чем дальше точка от текущего минимума, тем меньше вес)
#    - добавляется штраф за кривизны поверхности (за величину коэффициентов при квадратичных членах),
#      величина которого подбирается так, чтобы прогноз по значения в предыдущей точке был близок значению.
# 3) Вычисляется новые значение B1 и B2, для них вычисляется SIG. Зацикливаем на шаг 2.
# Выход по кол-ву итераций или по величине шага (приращение Бетта)
# Поиск С   (sum ( (pol ( C, B1i, B2i) - SIGi))**2/ri**(2+q) i in range(I)) + ??? (C20+C02+C11)*reg => min
#  где ri = sqrt ()
#


def CrePolyPow2 ( dim, maxP ) :            # arrays
        polyPow = []
        for i in range((maxP+1)**dim) :
            powers = zeros(dim)
            sumP = 0
            tmpP = i
            for d1 in range(dim) :
                d = dim-d1-1
                powers[d] = int( tmpP/((maxP+1)**d) )
                sumP += powers[d]
                tmpP -= powers[d] * ((maxP+1)**d)
            if sumP <= maxP : polyPow.append(powers)
        sortPow = []
        for pw in range (maxP+1) :
            for p in polyPow :
                if sum ( p ) == pw :
                    sortPow.append ( p )
        return sortPow


class Poly :                 # 
  def __init__ ( self, coef, pows ) :     # 
      self.coef  = coef
      self.pows  = pows
      self.NoPo  = len(pows)

  def Culc ( self, arg ) :         # sum i   coef[i] * arg[0]**pows[i][0] * .....
    val = 0
    for p in range ( self.NoPo ) :
        term = 1
        for d in range (len(arg)) :
            if self.pows[p][d] != 0 : term *= arg[d]**self.pows[p][d]
        val += term * self.coef[p]
    return val

  def CulcNNN ( self, arg ) :    # sum i   coef[i] * arg[0]**pows[i][0] * .....   Не годится для pyoma  :(
      return sum ( self.coef[p] * prod ( arg**self.pows[p] ) for p in range (self.NoPo) )

  def CulcShift ( self, arg, point ) :
      return point.Val + self.Culc (arg-point.Arg)


                       
def cosFi ( v1, v2 ) :
#            dim = len (v1)
 #           scalProd = sum ( v1[c]*v2[c] for c in range (dim) ) 
  #          v1_l2    = sum ( v1[c]**2    for c in range (dim) ) 
   #         v2_l2    = sum ( v2[c]**2    for c in range (dim) )
    #        return  scalProd / sqrt (v1_l2*v2_l2)                                         # cos поворота
            return   sum(v1*v2) / ( norma(v1) * norma(v2) )
        
def angleV1V2 ( v1, v2 ) :
            try:
                return  arccos ( cosFi ( v1, v2 ) )    * 180 / pi                      # угол поворота
            except :
                print ('cosFi', cosFi ( v1, v2 ))
                exit(-1)

def int_angleV1V2 ( v1, v2 ) :
            return  int ( round ( angleV1V2 ( v1, v2 ) ) )                             # угол поворота int


def norma ( v ) :
        return sqrt ( sum ( v**2 ) )


def distance ( p1, p2 ) :
        return norma ( p1.Arg-p2.Arg )


class Point :                 # 
    def __init__ ( self, Arg, Val=0, Num=0 ) :     # 
        self.Arg  = Arg.copy()
        self.Val  = Val
        self.Num  = Num
        self.wieght = 0
      
    def prin(self) :
        print ('Num', self.Num, 'Val', self.Val, 'Arg', self.Arg)


def AddPoint ( points, Arg, Val ) :
    poi = Point ( Arg, Val, len(points) )
    grad = (Val - points[-1].Val) / distance (poi, points[-1])
    points.append ( poi )
    if points[-2].Val < points[-1].Val :    # swap
        poin = deepcopy (points[-2])
        points[-2] = points[-1] 
        points[-1] = poin
        ismin = '***'
    else :
        ismin = 'min'
    return points[-1].Arg, ismin, grad


def wieght ( np, points, farWieght ) :
                dim = len (points[-1].Arg)
                if np < len(points)-1-dim : return exp ( - distance (points[np],points[-1]) * farWieght )
                else                    : return 1
#                return exp ( - distance (points[np],points[-1]) * farWieght )


def wieghtCulc ( points, farWieght ) : 
    for ip, p in enumerate(points) :
        p.wieght = wieght ( ip, points, farWieght )


        
def CulcCoef ( opt, points, curvPenal, farWieght ) :
                dim = len(points[0].Arg)
                wieghtCulc ( points, farWieght )
                lastWeight = sum ( points[ip].wieght  for ip in range (len(points)-dim-1) )
                normDist   = sum ( points[ip].wieght  for ip in range (len(points)-1    ) )
                partWeight = lastWeight / normDist
#                print 'normDist', normDist, lastWeight, partWeight

                CM = ConcreteModel()

                polPow = CrePolyPow2 ( dim, 2 )
                polLen = len(polPow)
                CM.Cpoly  = Var (range(polLen), domain=Reals, initialize = 1 )
                pol = Poly (CM.Cpoly, polPow)
                
                CM.Cpoly[0].value = 0;    CM.Cpoly[0].fixed = True
                
                def obj_expression(CM):
                    return ( 1 / normDist
                              * sum ( (pol.Culc(points[p].Arg-points[-1].Arg)-(points[p].Val-points[-1].Val))**2
                                  * points[p].wieght for p in range (len(points)-1) )
                           + curvPenal
                              * sum ( CM.Cpoly[c]**2 for c in range (dim+1, polLen) )
                           )
                CM.OBJ = Objective(rule=obj_expression)
                
                results = opt.solve(CM)                        
                CM.solutions.load_from(results)
                if str(results.solver.termination_condition) != 'optimal':
                    print ("Stst:", results.solver.termination_condition, '\n')
                    
                obj = CM.OBJ()
#                print 'CM.OBJ', obj
                if polLen > dim and obj > 0 :
                    partPen = curvPenal * sum (CM.Cpoly[c]()**2 for c in range (dim+1, polLen)) / obj
                else :    partPen = 0

                pol.coef = array([ CM.Cpoly[c]() for c in range(polLen) ])
                return pol, partWeight, partPen



def Prognose ( opt, pol, point, step ) :
                dim = len(point.Arg)
                CMP = ConcreteModel()

                norm = sqrt ( sum ( pol.coef**2 ) ) 
                def ini_circ (CMP, c): return - pol.coef[c+1] / norm * step * 0.999999
                CMP.nInc  = Var ( range(dim), domain=Reals, initialize = ini_circ )

                def nInc_ge(CMP,a) :
                    if  step < 0.7*point.Arg[a] : return Constraint.Skip                            #  что бы избежать потери точности
                    else                        : return ( CMP.nInc[a] >= - 0.7*point.Arg[a] )      #  for Arg >= 0
                CMP.cnInc_ge = Constraint( range (dim), rule=nInc_ge )

                def circArg(CMP) :  return ( sum ((CMP.nInc[a])**2 for a in range(dim)) / step**2 <= 1 )
#                def circArg(CMP) :  return ( sum ((CMP.nInc[a])**2 for a in range(dim)) <= step**2 )
                CMP.cnInc = Constraint( rule=circArg )

                def obj_expression(CMP):  return ( pol.Culc(CMP.nInc) )
                CMP.OBJ = Objective(rule=obj_expression)

                try:
                    results = opt.solve(CMP)                        
                    CMP.solutions.load_from(results)
                    if str(results.solver.termination_condition) != 'optimal':
                        print ("Stst:", results.solver.termination_condition, '\n')
                        print ("************Попробуем линейный вариант (вручную)")
                        for a in range(dim) :
                            CMP.nInc[a].value = - pol.coef[a+1] / norm * step * 1 
                except:
                    print ("EXCEPT ************Попробуем линейный вариант (вручную)")
                    for a in range(dim) :
                        CMP.nInc[a].value = - pol.coef[a+1] / norm * step * 1 
                    

                print ('Incr:    ', [ CMP.nInc[a]() for a in range(dim) ], sum ( (CMP.nInc[a]())**2 for a in range(dim))/step**2 )
                prognVal = CMP.OBJ()
                if  sum ( (CMP.nInc[a]())**2 for a in range(dim))/step**2  < 0.94 : Constr = 'Inside'
                else :   Constr = 'Const'
#                print prognVal, point.Val, pol.Culc(CMP.nInc)(), \
 #                     'ang', int_angleV1V2 ( [ CMP.nInc[a]() for a in range(dim) ],pol.coef[1:dim+1] )
                Incr = array([ CMP.nInc[a]() for a in range(dim) ]) 
                return  prognVal+point.Val, Incr+point.Arg, Constr, Incr
#                return  prognVal+point.Val, array([ CMP.nInc[a]()+point.Arg[a] for a in range(dim) ]), \
 #                                   Constr, array([ CMP.nInc[a]()              for a in range(dim) ])

    
#maxpartPen = .5
maxpartPen = .001
#maxpartPen = 1e-4 #0.3 #0.1
minpartPen = 1e-5

def arrange_farWieght_curvPenal (opt, points, curvPenal, farWieght, Val, nArg) :
 #       print "sAR", '  ', farWieght, curvPenal
        dim = len (nArg)
        for n in range(100) :                    # загоняем partPen в границы
            pol, partWeight, partPen = CulcCoef (opt, points, curvPenal, farWieght)
            if   partWeight > maxpartPen :  farWieght *= 1.07
            elif partWeight < minpartPen :  farWieght /= 1.07
            else                         : break
#            print 'QQQQQQQQQQQQQQ', n, farWieght, 'pW', partWeight
        prognVal = pol.CulcShift (nArg, points[-1])
        print ("+AR", '**', farWieght, 'pW', partWeight, curvPenal, partPen, (Val-prognVal), )
        
        farWieghtN = farWieght * 1.001
        pol, partWeight, partPen = CulcCoef (opt, points, curvPenal, farWieghtN)
        prognValN = pol.CulcShift (nArg, points[-1])
        dW = (prognValN-prognVal)/0.001

        curvPenalN = curvPenal * 1.001
        pol, partWeight, partPen = CulcCoef (opt, points, curvPenalN, farWieght)
        prognValN = pol.CulcShift (nArg, points[-1])
        dP = (prognValN-prognVal)/0.001

        if dW==0 :  return farWieght, curvPenal

        delteVal = Val-prognVal    #  > 0 если прогноз ниже
#        ad = 0.03
        ad = 0.05
        if abs (dP) <= abs(dW) :  addW = ad; addP = ad* abs(dP/dW)
        else                   :  addP = ad; addW = ad* abs(dW/dP)
        if dW * delteVal > 0 :  multW=1+addW
        else                 :  multW=1-addW
        if dP * delteVal > 0  : multP=1+addP
        elif dP == 0          : multP=1
        else                  : multP=1-addP

        print ('dW', dW, multW, 'dP', dP, multP, delteVal)

#        for n in range (100) :
#        for n in range (50) :
        for n in range (25) :
            farWieghtN = farWieght * multW
            curvPenalN = curvPenal * multP
            pol, partWeight, partPen = CulcCoef (opt, points, curvPenalN, farWieghtN)
            if multW > 1 and partWeight < minpartPen : break                    #  выход по малости влияния
            if multW < 1 and partWeight > maxpartPen : break                    #  выход по избыточному влиянию
            prognValN = pol.CulcShift (nArg, points[-1])
            if delteVal > 0 :
                if prognValN >= Val : break         #  перестарались
                elif prognValN <= prognVal : break  #  прогноз ухудшился
                else :
                    prognVal  = prognValN
                    curvPenal = curvPenalN
                    farWieght = farWieghtN
            else :
                if prognValN <= Val : break         #  перестарались
                elif prognValN >= prognVal : break  #  прогноз ухудшился
                else :
                    prognVal  = prognValN
                    curvPenal = curvPenalN
                    farWieght = farWieghtN
        print ("+AR", n, farWieght, 'pW', partWeight, curvPenal, partPen, (Val-prognVal))
        return farWieght, curvPenal


def condition ( points, farWieght, opt ) :
    dim = len(points[0].Arg)
    M = ConcreteModel()
    M.plane  = Var ( range(dim+1), domain=Reals, initialize = 1 )              # Нормальное уравнение плоскости :
    def Eq1 (M) : return ( sum ( M.plane[i]**2 for i in range(dim) ) == 1 )    #     сумма квадратов равна единице
    M.cEq1 = Constraint( rule=Eq1 )
    def Eq2 (M) : return ( M.plane[dim] <= 0 )                                 #     свободный .. <=0
    M.cEq2 = Constraint( rule=Eq2 )

    normDist = sum ( p.wieght for p in points )
    
    def point_plane2 ( point ) :
        return  ( sum (M.plane[i]*point.Arg[i] for i in range(dim))+M.plane[dim] )**2
                
    def obj_expression(M):
        return  sum ( point_plane2( p ) * p.wieght for p in points ) / normDist
    M.OBJ = Objective(rule=obj_expression)

    results = opt.solve(M)                        
    M.solutions.load_from(results)
    if str(results.solver.termination_condition) != 'optimal':
                    print ("Stst:", results.solver.termination_condition, '\n')
    obus = sqrt ( M.OBJ() )
 #   for cp in range(dim+1): print cp, M.plane[cp]() 
#    print 'obus', obus
#    return obus, [M.plane[c]() for c in range(dim+1)]
    return obus, array([M.plane[c]() for c in range(dim)])

def SetAllArgs (Arg, InArg, stepsIN ) :
    a_in = 0
    for iss,s in enumerate (stepsIN) :
        if s != 0:
            InArg[iss] = Arg[a_in]
            a_in += 1
    return InArg




def SurMin ( CVNumOfIter, stepsIN, ExitStep, InArg, getVal, opt11 ) :
    old_points = []
    old_cCos = []
    old_stepMult = 1
    firstDerec = True
    opt = Factory ( None, 10000, 1e-9 )

    Arg = []
    steps = []
    for ia, a in enumerate(InArg) :
        if stepsIN[ia] != 0 :
            Arg.append(a)
            steps.append (stepsIN[ia])
    Arg = array (Arg)
    dim = len (Arg)

    curvPenal = 0.001
    farWieght = 2/dim/abs(steps[0])
    #  exp ( - farWieght * dist...
    print ('\nstart  farWieght', farWieght)
    step = 1e37
    if CVNumOfIter == 0:
            AllArgs = SetAllArgs(Arg, InArg, stepsIN)
            Val = getVal ( AllArgs, -1 )
            points = [Point (Arg, Val, 0)]
            for p in points:  p.prin()
            return points, NaN

    for itera in range (CVNumOfIter) :
        if itera == 0 :
            AllArgs = SetAllArgs(Arg, InArg, stepsIN)
            Val = getVal ( AllArgs, itera )
#            Val = getVal ( Arg, itera )
            print ('\nITER', itera, 'start', Val, 'st', NaN,  Arg, '\n')
            points = [Point (Arg, Val, 0)]

        elif itera <= dim :
            nArg = Arg.copy()
#            if stepIN > 0 : stepp = stepIN
 #           else          : stepp = Arg[itera-1] * (-stepIN)
            step_i = steps[itera-1]
            Nattempt = 5
            for attempt in range (Nattempt) :
                nArg[itera-1] += step_i
                AllArgs = SetAllArgs(nArg, InArg, stepsIN)
                Val = getVal(AllArgs, itera)
#                Val = getVal ( nArg, itera )
                Arg, mi, grad = AddPoint ( points, nArg, Val )
                print ('\nITER', itera, mi, Val, grad, 'st', step_i, nArg, '\n')
                if mi != '***' : break
                if attempt != Nattempt-1 :
                    nArg[itera - 1] -= step_i
                    if attempt == 0 :  step_i = - step_i
                    else            :  step_i *= -0.05
            step = min (step, abs(step_i))
        elif firstDerec :   #itera == dim + 1 :
            pol, tmp, tmp1 = CulcCoef (opt, points, curvPenal, farWieght)                              # CulcCoef
            if co.printL: print ('coef', pol.coef[:dim+1], '\n    ', pol.coef[dim+1:])
            old_coef = deepcopy (pol.coef)                                                  # для вычисления угла поворота
            prognVal, nArg, Constr, nIncr = Prognose ( opt, pol, points[-1], abs (step) )        # Prognose
            AllArgs = SetAllArgs(nArg, InArg, stepsIN)
            Val = getVal ( AllArgs, itera )
#            Val = getVal ( nArg, itera )                                                        # getVal
            prognErr = abs (Val-prognVal)/(points[-1].Val-prognVal)         # погрешность прогноза:  0 - отлично
            Arg, mi, grad = AddPoint ( points, nArg, Val )                                     #  AddPoint
            print ('\nITER', itera, Constr, mi, 'grd', grad, 'Er', prognErr, 'st', step, 'Pr', prognVal, Val, '\n\t', nArg , '\n')
            if grad < 0 and Constr == 'Const' :
                if    prognErr < 0.05:  step *= 3
                elif  prognErr < 0.09:  step *= 2
                elif  prognErr < 0.19:  step *= 1.2
            else                              : firstDerec = False
            if prognErr > 0.3 :
                firstDerec = False      # 28
                step /= 3
        else :
            if len(old_points) > 0 : 
                farWieght, curvPenal = arrange_farWieght_curvPenal (opt, old_points, curvPenal, farWieght, Val, nArg)
                farWieght *= ( distance (old_points[-dim-2],old_points[-1]) / distance (points[-dim-2],points[-1]) )
                print ('farWieght dist', farWieght)
            pol, tmp, tmp1 = CulcCoef (opt, points, curvPenal, farWieght)                              # CulcCoef
            if co.printL: print ('coef', pol.coef[:dim+1], '\n    ', pol.coef[dim+1:])
            ang_pov = int_angleV1V2 ( old_coef[1:dim+1], pol.coef[1:dim+1] )   # angle поворота линейных членов полинома
            print ('ang_pov' , ang_pov)
            old_coef = deepcopy (pol.coef)

            ostep = step                                                # step    выбор шага
            if old_stepMult >= 1 :
                if   prognErr < 0.01 and ang_pov <  5 : stepMult = 5
                elif prognErr < 0.05 and ang_pov < 15 : stepMult = 3
                elif prognErr < 0.1  and ang_pov < 24 : stepMult = 2
                elif prognErr < 0.15 and ang_pov < 30 : stepMult = 1
                elif prognErr < 0.2  and ang_pov < 34 : stepMult = 0.9
                elif prognErr < 0.4  and ang_pov < 37 : stepMult = 0.5
                elif prognErr < 0.5  and ang_pov < 45 : stepMult = 0.3
                elif prognErr < 1    and ang_pov < 80 : stepMult = 0.2
                else                                  : stepMult = 0.1
            else :
                if   prognErr < 0.05  : stepMult = 3          
                elif prognErr < 0.1   : stepMult = 2
                elif prognErr < 0.15  : stepMult = 1
                elif prognErr < 0.2   : stepMult = 0.9
                elif prognErr < 0.4   : stepMult = 0.5
                elif prognErr < 0.5   : stepMult = 0.3
                elif prognErr < 1     : stepMult = 0.2
                else                  : stepMult = 0.1
            old_stepMult = stepMult
            step*= stepMult
            if Constr=='Inside' and step > ostep : step = ostep  #  если ограничение по шагу нет, шаг не увеличиваем
            prognVal, nArg, Constr, nIncr = Prognose ( opt, pol, points[-1], step )                        # Prognose
 
            if dim > 1 :
              cond, cCos = condition ( points, farWieght, opt )               # обусловленность
              if co.printL: print ('Cond', cond, 'cCos', cCos)
              if co.printL: print ('cCos_Incr', int_angleV1V2 ( nIncr,cCos ))
              
              if len(old_cCos) > 0 :
#                  print 'old_cCos',  old_cCos
                  cCos_old_cCos = int_angleV1V2 ( cCos, old_cCos )  # cos old and new cond
                  if co.printL: print ('cCos_old_cCos' , cCos_old_cCos)
                  if dim>2 and abs (cCos_old_cCos-90.) > 30 :                 #  недостаточно _|_
                      pro =  old_cCos * cos (cCos_old_cCos*pi/180.)
                      cCos = cCos - pro
                      norm = norma ( cCos )
                      cCos = cCos/norm
                      print ('_|_ang', int_angleV1V2 ( cCos, old_cCos ))
#              old_cCos = deepcopy(cCos) 
              old_cCos = cCos.copy() 
              print ('****Cond', cond, 'cCos', cCos, 'step', step)
#              if prognErr >= 0.2 or cond < 1e-3 :
              if 1 :  
                malt = 0.03
                for i in range (10) :
#                    nnArg = array([ nArg[a]+cCos[a]*step*malt for a in range(dim) ])       #  шаг в сторону +
                    nnArg = nArg + cCos*step*malt                                  #  шаг в сторону +
                    prognValN = pol.CulcShift (nnArg, points[-1])
#                    mnArg = array([ nArg[a]-cCos[a]*step*malt for a in range(dim) ])       #  шаг в сторону -
                    mnArg = nArg - cCos*step*malt                                  #  шаг в сторону -
                    mprognValN = pol.CulcShift (mnArg, points[-1])                  #    берем кто меньше
                    if mprognValN < prognValN :
                        prognValN = mprognValN
                        nnArg     = mnArg
                        si = '-'
                    else : si = '+'   
                    print ('NNNN', si, prognVal, prognValN, points[-1].Val, nnArg)
                    malt *= 0.1
                    if prognValN < points[-1].Val : break
                nArg = nnArg
#                nArg = array(nnArg)
                prognVal = prognValN
            
            AllArgs = SetAllArgs(nArg, InArg, stepsIN)
            Val = getVal ( AllArgs, itera )
#            Val = getVal ( nArg, itera )                                                        # getVal
            print ('\t\t\topEr', prognErr, 'ang', ang_pov, 'ost', ostep, 'st',step, stepMult)
            prognErr = abs (Val-prognVal)/(points[-1].Val-prognVal)         # погрешность прогноза:  0 - отлично
            old_points = deepcopy (points)
            delta = Val - points[-1].Val
            Arg, mi, grad = AddPoint ( points, nArg, Val )                                     #  AddPoint

            print ('\nITER',itera, Constr, mi, 'grd',grad, 'pEr',prognErr, 'P', prognVal, Val, \
                  '\n\t', nArg, 'delta', delta, '\n')
            if distance ( points[-2], points[-1] ) < ExitStep:
                print ('***************  ExitIncr')
                break       
        if abs(step) < ExitStep:
            print ('***************  ExitStep', abs(step), '<', ExitStep)
            break       

    for p in points :  p.prin()
    return points, step

