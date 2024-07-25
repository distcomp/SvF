[0.116622]
x(t)  MSD% 14.786693855827112 MSD 0.09092454374846508
Estim -1
    OBJ =0.03590549257285315
    60.8	sum(Gr.mu0[i]()*(x.V.dat[i]-fx(x.A[0].dat[i]+tmin))**2 for i in range ( 0, 20+1 ) )/x.V.sigma2/sum(Gr.mu0[i]() for i in range ( 0, 20+1 ) ) =0.02186463151859553
    39.1	Penal[0]*sum ( (int(i__T!=tmin+step)+int(i__T!=tmax-step))/2*T.step*(((fx((i__T+T.step))+fx((i__T-T.step))-2*fx(i__T))/T.step**2))**2 for i__T in myrange (tmin+step,tmax-step,T.step) )/14.5 =0.01404086105425762
addStrToRes: 