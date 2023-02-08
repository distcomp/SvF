# -*- coding: UTF-8 -*




import SurMin as sm


def get_sigCV( Penal, itera ):
    return (Penal[0]-1)**2

sm.SurMin ( 30, [0.0001], 1e-5, [0.5], get_sigCV )

exit(0)


