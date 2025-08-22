[0.11581284651785796]
x(t)  CV% 18.602191744954645 CV 0.11438634042355061 MSD% 14.781608534305244 MSD 0.09089327370637869
Estim 18.602191744954645
    OBJ =0.03666037743016522
    62.9	sum(Gr.mu[i]()*(x.V.dat[i]-fx(x.A[0].dat[i]+tmin))**2 for i in range ( 0, 20+1 ) )/x.V.sigma2/sum(Gr.mu[i]() for i in range ( 0, 20+1 ) ) =0.023086204574161988
    37.0	Penal[0]*sum ( ((i__T!=tmin+step)+(i__T!=tmax-step))/2*T.step*(((fx((i__T+T.step))+fx((i__T-T.step))-2*fx(i__T))/T.step**2))**2 for i__T in myrange (tmin+step,tmax-step,T.step) )/14.5 =0.013574172856003226
Step: 4.825528712434829e-08
Points:Num 1 Val 18.602224065179115 Arg [0.11697082]
Num 2 Val 18.602226921840032 Arg [0.11465456]
Num 3 Val 18.60219176360921 Arg [0.1158706]
Num 4 Val 18.602191748625625 Arg [0.11580979]
Num 0 Val 18.602191745160347 Arg [0.11581269]
Num 5 Val 18.60219174496412 Arg [0.11581283]
Num 6 Val 18.602191744954645 Arg [0.11581285]
addStrToRes: 