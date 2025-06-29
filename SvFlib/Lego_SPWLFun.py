from Lego import *

class SPWLFun (Fun) :
    def __init__(self, Vname='', As=[], param=False, Finitialize=0, DataReadFrom='', Data=[], Type='', Domain=None, ReadFrom=''):
        Fun.__init__(self, Vname, As, param, -1, Finitialize, DataReadFrom, Data, Type, Domain, ReadFrom)
#        if SvF.Compile: return  # ???

    def interpol(self, lev, X, Y=0, Z=0):  # X,Y,Z  в шагах
        if self.param or not SvF.Use_var:           gr = self.grd
        else:                                       gr = self.var  # 29
        if lev == 2:
            if self.type == 'gSPWLi':  # 'G_ind':
                def ind_0_1(x):
                    return 0.5 * x / py.sqrt(SvF.Epsilon + x ** 2) - 0.5 * (x - 1) / py.sqrt(
                        SvF.Epsilon + (x - 1) ** 2)
                ret = 0  # tetta(1 - dX) * tetta(dX)
                for i in self.A[0].NodSm:
                    dX = X - i
                    for j in self.A[1].NodSm:
                        if isnotNone(self.domain_SPWL):
                            if self.domain_SPWL[i, j] == 0: continue
                            if self.domain_SPWL[i, j + 1] == 0: continue
                            if self.domain_SPWL[i + 1, j] == 0: continue
                            if self.domain_SPWL[i + 1, j + 1] == 0: continue
                        dY = Y - j
                        ret += ((gr[i, j] * (1 - dX) + gr[i + 1, j] * dX) * (1 - dY)
                                + (gr[i, j + 1] * (1 - dX) + gr[i + 1, j + 1] * dX) * dY
                                ) * ind_0_1(dX) * ind_0_1(dY)
                return ret
        if lev == 1:
            if self.type == 'gG':  # !!!! Сдвиг на КОНСТАНТУ !!!!!   Что это 2025.01
                def η(x):
                    return py.sqrt(x ** 2 + SvF.Epsilon)
                #                dgr = [0.0]
                #               for n in self.A[0].mNodS:  dgr.append ( gr[n] - gr[n - 1] )
                #              ret = gr[0]+0.5*(dgr[1] + dgr[self.A[0].Ub])*X  # gr[0]+0.5*dgr[self.A[0].Ub]*X VVV
                ret = gr[0] + (gr[1] - gr[0] + gr[self.A[0].Ub] - gr[self.A[0].Ub - 1]) * X  # ABC
                for n in self.A[0].mNodSm:  # for n in self.A[0].NodSm: VVV
                    ret += (gr[n + 1] - 2 * gr[n] + gr[n - 1]) * (η(X - n) - n)  # (dgr[n+1]-dgr[n])
                return ret * 0.5
            if self.type == 'gSPWL':  # 'G7': #
                def η(x):
                    return py.sqrt(x ** 2 + SvF.Epsilon)
                ##                dgr = [0.0]
                ##               for n in self.A[0].mNodS:  dgr.append(gr[n] - gr[n - 1])
                ##              ret = 0.5 * (gr[0] + gr[self.A[0].Ub]) + 0.5*dgr[1]* X + 0.5*dgr[self.A[0].Ub] * (X-self.A[0].Ub)
                dgr_1 = gr[1] - gr[0]
                dgr_Ub = gr[self.A[0].Ub] - gr[self.A[0].Ub - 1]
                ret = (gr[0] + gr[self.A[0].Ub]) + dgr_1 * X + dgr_Ub * (X - self.A[0].Ub)
                for n in self.A[0].mNodSm:
                    ret += (gr[n + 1] - 2 * gr[n] + gr[n - 1]) * η(X - n)
                return ret * 0.5

            if self.type == 'gSPWLi':  # 'G_ind':      #      0       1
                def ind_0_1(x):  # _____|-------\_______
                    return 0.5 * x / py.sqrt(SvF.Epsilon + x ** 2) - 0.5 * (x - 1) / py.sqrt(
                        SvF.Epsilon + (x - 1) ** 2)
                ret = 0
                for i in self.A[0].NodSm:
                    dX = X - i
                    ret += (gr[i] * (1 - dX) + gr[i + 1] * dX) * ind_0_1(dX)  # tetta(1 - dX) * tetta(dX)
                return ret

        
