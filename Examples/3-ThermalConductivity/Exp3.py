# -*- coding: UTF-8 -*-

import random
from math import *


random.seed('aa63357799.874')
#random.seed('aa633577666.874')
#random.seed('aa6336577666.874')
#random.seed('abc63.08')

def T (x,t) :
    return 2 * (t+1) / ( (x+1)**2 + (t+1)**2 ) * 100

mean = 0
msd = 0
num = 0
aErr = []


if (0):                                          #  RND
 with open('Exp3Rnd.dat', 'w') as f:
  print ('t', 'x', 'T  Err  Terr', '#SvFver_62_tbl', file = f)
  for n in range (1000) :
        t = random.uniform(0, 5)
        x = random.uniform(0, 2)
        TT = T(x,t)
        Err = random.gauss(0, 2)
        mean += Err
        msd  += Err**2
        num  += 1
        aErr.append(Err)
        print (t, x, TT, Err, TT+Err)
        print ( t, x, TT, Err, TT+Err, file = f)
else:                                             #  11x6
 with open('Exp3.dat', 'w') as f:
  print ('t', 'x', 'T  Err  Terr', '#SvFver_62_tbl', file = f)
  for t in range (10+1):
    for x in range (10+1):
        xx = x *0.2
        tt = t *0.5
        TT = T(xx,tt)
        Err = random.gauss(0, 2)
        mean += Err
        msd  += Err**2
        num  += 1
        aErr.append(Err)
        print (tt, xx, TT, Err, TT+Err)
        print ( tt, xx, TT, Err, TT+Err, file = f)

mean = mean/num
msd  = sqrt(msd/num)
print ( 'mean=',mean,'msd=',msd)
msd = sum ( (e-mean)**2 for e in aErr )
print ( 'msd=',sqrt(msd/num))


exit(0)


#####################################

f_n = 'Spring5.dat'
f_formula = 'formula.dat'
f_d = 'd.dat'

N = 81
#min_t_o = -0.9
#min_t_o = -1.
min_t_o = 0.

min_t =  -1.0
max_t =  2.5
#min_t =   .0
#max_t =  3.5
step = (max_t-min_t)/(N-1)

K =    1.4
omega = sqrt(K)
mu =   0.4
xr =   1.2
#xr =   0.9
Err =  0.1
#Err =  0.05

print ( 'K=', K, 'omega=', omega, 'mu=', mu, 'xr=', xr )

print ('step', step )

mean = 0
sig = 0
num = []
for n in range ( N ):
    num.append ( random.gauss(0, 1) )
    mean = mean + num[-1]
    sig  = sig  + num[-1]**2
mean = mean / N 
sig  = sqrt (sig  / N)
print ('  I', mean, sig)

sig = 0
for n in num :
    sig  = sig  + (n-mean)**2
sig  = sqrt (sig  / N)
print (' II',  sig)
    



with open(f_formula, 'w') as f:
    print >> f, 't', 'x', '#SvFver_62_tbl'
    for i in range (N) :
        t = min_t+step*i
        fu = sin ( omega * (t+min_t_o) ) * exp ( -mu/2*(t+min_t_o) ) + xr
        print >> f, t, fu

with open(f_d, 'w') as f:
    print >> f, 't', 'd', '#SvFver_62_tbl'
    for i in range (N) :
        numb = (num[i]-mean)/sig
        t = min_t+step*i
        fu = sin ( omega * (t+min_t_o) ) * exp ( -mu/2*(t+min_t_o) ) + xr
        print >> f, t, fu+Err*numb

with open(f_n, 'w') as f:
#    print >> f, 't', 'data', '#SvFver_62_tbl'
#    print >> f, 't', 'x', 'x(t)', '#SvFver_62_tbl'
    print >> f, 't', 'x(t)', 'x', '#SvFver_62_tbl'
    sigma = 0
    mean1 = 0
    for i in range (N) :
        numb = (num[i]-mean)/sig
        mean1 = mean1 + numb
        sigma  = sigma  + numb**2
        t = min_t+step*i
#        fu = sin (t) * exp (mu*(t-min_t)) + x0
        fu = sin ( omega * (t+min_t_o) ) * exp ( -mu/2*(t+min_t_o) ) + xr
#        print >> f, x, fu, fu+0.2*num, num
#        print >> f, t, fu+Err*numb, fu
        print >> f, t, fu, fu+Err*numb
    sigma  = sqrt (sigma / N)
    mean1 = mean1 / N 
    print ('III', mean1, sigma, sigma*Err)


