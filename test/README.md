# Piecewise aproximation of functions to be identified which constitute composition function

Demonstration examples relating to inverse problems with ordinary differential equations 
of 1st and 2nd order by CHKS-PW and SOS2 representation of pw-functions.

All examples may be run by 

`$ python mainTestScaledOdePW.py ...` command with the following options:

	$ python mainTestScaledOdePW --help
 	usage: mainTestScaledOdePW.py [-h] [-pr PREFIX] [-wd WORKDIR] [-dt DATETIME]
                              [-s {ipopt,scip}] [-o {1,2,0}]
                              [-ode1 {exp,square}] [-pw2sos] [-sos2] [-log]
                              [-t TLOUPND [TLOUPND ...]]
                              [-x XLOUPN [XLOUPN ...]]
                              [-Fx FXLOUP [FXLOUP ...]] [-eps EPSILON]
                              [-reg REGCOEFF] [-err ERRDATA] [-eta]
                              [-dur DURATION]

	optional arguments:
	  -h, --help            show this help message and exit
 	  -pr PREFIX, --prefix PREFIX
                        Prefix of problem name (default: OdePw)
	  -wd WORKDIR, --workdir WORKDIR
                        working directory (default: tmp)
	  -dt DATETIME, --datetime DATETIME
                        Time of start (default: 12/12/2022-10:47:15)
	  -s {ipopt,scip}, --solver {ipopt,scip}
                        solver to use (default: ipopt)
	  -o {1,2,0}, --order {1,2,0}
                       ODE order 1 or 2 (reduced form), 0 - SPLINE (default: 2)
	  -ode1 {exp,square}, --ode1 {exp,square}
                        type of ODE1 (default: exp)
	  -pw2sos, --pw2sos     use PW to get initial solution for SOS2 (default: False)
	  -sos2, --sos2         use SOS2 for discretization (default: False)
	  -log, --log           use LOG for discretization (default: False)
	  -t TLOUPND [TLOUPND ...], --tLoUpND TLOUPND [TLOUPND ...]
                        t: Lo Up N number of data (default: [0.0, 3.0, 10, 5])
	  -x XLOUPN [XLOUPN ...], --xLoUpN XLOUPN [XLOUPN ...]
                        x: Lo Up N (default: [-1.5, 1.5, 5])
	  -Fx FXLOUP [FXLOUP ...], --FxLoUp FXLOUP [FXLOUP ...]
                        Lo Up limits for Fx (default: [-100.0, 100.0])
	  -eps EPSILON, --epsilon EPSILON
                        Epsilon to smooth pos() (default: 0.01)
	  -reg REGCOEFF, --regcoeff REGCOEFF
                        Regularization coefficient (default: 0.005)
	  -err ERRDATA, --errdata ERRDATA
                        Error of data (default: 0.1)
	  -eta, --useEta  use Eta in discretization (default: False)
	  -dur DURATION, --duration DURATION

The following examples of ODE1 are implemented:

`dx/dt = x, x(t) = exp(t)` (denoted above and below by **exp**)

`dx/dt = x^2, x(t) = 1/(1-t)` (denoted above and below by **square**)

and one example of ODE2:

`d^2x/d^2t = -4x, x(t) = sin(2*t) + cos(2*t)`

Examples of run with important limits on x(t) and F(x) values:

	$ python -ipopt  -o 1 -ode1 exp --tLoUpND 0.0 3. 20 8  --xLoUpN .0 25.0 10 --FxLoUp .0 26. -reg .1 -err 0. -eps 0.001
	$ python -pw2sos -o 1 -ode1 exp --tLoUpND 0.0 3. 20 8  --xLoUpN .0 25.0 10 --FxLoUp .0 26. -reg .1 -err 0. -eps 0.001

	$ python  -o 1 -ode1 square  --tLoUpND 0.0 .8 20 8  --xLoUpN -.1 6. 14 --FxLoUp -.1 26. -reg .01 -err 0.1 -eps 0.001
	$ python -pw2sos -o 1 -ode1 square --tLoUpND 0.0 .8 20 8  --xLoUpN -.1 6. 14 --FxLoUp -.1 26. -reg .01 -err 0.1 -eps 0.001

	$ python -o 2         --tLoUpND 0. 3. 20 8 --xLoUpN -1.5 1.5 10 --FxLoUp -7.0 7. -reg .1 -err .2
	$ python -pw2sos -o 2 --tLoUpND 0. 3. 20 8 --xLoUpN -1.5 1.5 10 --FxLoUp -7.0 7. -reg .1 -err .2



