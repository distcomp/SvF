# SvF
**SvF** stands for "Simplicity vs Fitting" and is a short title of a method of balanced regularized identification of mathematical models by experimental data.

The SvF-technology proposes a promising area of applied mathematics, combining methods of structural mathematical modeling, optimization, adaptive regularization and distributed computing.

The author of the SvF-technology is [Alexander Sokolov](https://scholar.google.ru/citations?user=mtE_u_YAAAAJ&hl=en&oi=sra), [sashasok](https://gitlab.com/sashasok). 

The technology and underlying mathematical algorithms are described in the following articles:  
1. Sokolov A. V., Voloshinov V. V. Model Selection by Balanced Identification: the Interplay of Optimization and Distributed Computing // Open Computer Science, 2020, 10 — p. 283–295. [DOI: 10.1515/comp-2020-0116](https://doi.org/10.1515/comp-2020-0116)  
2. Соколов, А.В.; Волошинов, В.В. Выбор математической модели: баланс между сложностью и близостью к измерениям. International Journal of Open Information
Technologies, 2018, 6(9) C. 33-41, [PDF](http://injoit.org/index.php/j1/article/view/612)

Current repository is the public version of the [private SvF repository](https://gitlab.com/sashasok/svf).

# How to cite
Please, cite the first of the above articles if you'll use the technology.

# How to install
Current implementation of the SvF-technolosy is based on [Everest Python API](https://gitlab.com/everest/python-api) and [SSOP Everest Application](https://optmod.distcomp.org/apps/vladimirv/solve-set-opt-probs), which have to be cloned from their Git-repos. **So, use the following command for correct cloning**

`$ git clone --recurse-submodules https://github.com/distcomp/SvF.git`

or, if you have public key attached to your GITHUB account, then you can use another command:

`$ git clone --recurse-submodules git@github.com:distcomp/SvF.git`

If you know Russian read the Section 1 (software requirements) of [User Manual](https://github.com/distcomp/SvF/blob/main/SvF_UserGuide29v02.pdf) :

1. OS Linux is the default recommendation
2. Python 3.7.4+ (to save disk space, it is recommended to use the [Miniconda Python environment](https://docs.conda.io/en/latest/miniconda.html)
3. Basic Python packages are (depending on the actual set of packages of your Python environment some other packages may be missed and should be installed according to *ModuleNotFoundError* messages)
	* numpy 1.6.+
   	* matplotlib 1.5.+
   	* [Pyomo](http://www.pyomo.org/) 6.+, [Installation](https://pyomo.readthedocs.io/en/stable/installation.html) 
4. For solving NLP problems (Nonlinear Mathematical Programming Problems with continuous variables and differentiable functions) you need [Ipopt](https://github.com/coin-or/Ipopt) solver. 
	* For regular installation see native [Ipopt documentation](https://coin-or.github.io/Ipopt/INSTALL.html).
	* Full functional build with additional Linear Algebra libraries may be found here [https://gitlab.com/ssmir/solver-build-scripts](https://gitlab.com/ssmir/solver-build-scripts) (contact with this installation pack developers for disclosure of unclear details)
	* For demonstrative or testing purposes "light" Ipopt build may be istalled as Python package:  
$ conda install -c conda-forge ipopt  
see [Pyomo documentation](https://pyomo.readthedocs.io/en/stable/installation.html#using-conda)
5. For large-scale calculations, it is desirable to use the [Everest platform](http://everest.distcomp.org/), in particular, the [SSOP application](https://optmod.distcomp.org/apps/vladimirv/solve-set-opt-probs), which allows you to solve in parallel a set of optimization problems on computing resources connected to the Everest Optimization Portal [Everest Opt](https://optmod.distcomp.org). To do this, you will need to register on the site [https://everest.distcomp.org](https://everest.distcomp.org) or [https://optmod.distcomp.org](https://optmod.distcomp.org).

# Test run  
1. Open Bash-script runSvF30.sh in any text editor and set correct value to the system environment variable SVFLIBPATH (a path to **SvF/Lib30** folder at your system)
2. Open in your system console some of subfolders in Examples folder, e.g.   
 **SvF/Examples/3-ThermalConductivity/MSD(Dreg11x11)Curv(T)M0**,  
   and run the command  
   `$ bash ../../../runSvF30.sh`
   
# Try local or remote solver

All description of mathematical model, references to experimental data (e.g. in text or Spreadshet formats), settings and options of SvF-algorithm are presented in a special Task-file. You can find examples of these files in "terminal" subfolders of **SvF/Examples** folder. Possible extensions of task-files may be **.mng** (text format) or **.odt** (Libre/OpenOffice Writer). Among other options there is one, which tells SvF-system how to solve optimization problems arisen: "locally" (by solver installed at the system where Python SvF-application is running) or "remotely" (by Everest optimization service).

These options are: **Runmode** or **RunSolver**. Not going in deep details for beginners you may set these option either to  
**P&P** -  to solve all problems by local solver  
or  
**S&S** - to solve all problems by remote solvers.

E.g. in task-file **MSD(Dreg11x11)+Curv(T):M=0.odt** in example model  
 **SvF/Examples/3-ThermalConductivity/MSD(Dreg11x11)Curv(T)M0**  
  the *Runmode* option is in the first line. You can chage its value and run example by the command (from this folder)  
   `$ bash ../../../runSvF30.sh`

## Try remote solver

To try remote solvers you can set the proper value of **Runmode** option (in *.odt task-file)  
`Runmode = 'S&S'`

Then you must to get special **token-file** which is required to use Everest-services by Everest Python API. 

To get the token you must be a registered user of sites [https://everest.distcomp.org](https://everest.distcomp.org) or [https://optmod.distcomp.org](https://optmod.distcomp.org).  
 If so, you can get a standard (7 days valid token) by the following command (you will be asked to enter your Everest password):  
 
`$ python everest.py get-token -server_uri https://optmod.distcomp.org -u YOUR_EVEREST_LOGIN -l ssop | tee .token`  

Run that command in **SvF/pyomo-everest/python-api** folder and *.token* file will appear.

After that switch to **SvF/Examples/3-ThermalConductivity/MSD...** folder and try to run SvF-application   
   `$ bash ../../../runSvF30.sh`

	

