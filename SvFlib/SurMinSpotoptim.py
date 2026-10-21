# -*- coding: utf-8 -*-
import numpy as np
from copy   import *

from spotoptim import SpotOptim
from spotoptim.plot.visualization import plot_progress, plot_surrogate
from spotoptim.sampling.design import generate_qmc_lhs_design
import matplotlib.pyplot as plt

import Compare
import COMMON as co
from SurMin import SetAllArgs, Point, AddPoint

init_x_to_y_dict = None

def evaluate_initial_points(CVNumOfIter, inArg, steps, getVal, dim, iter=None, bounds=None):
    """

    """
    print(f"Initial points are being evaluated, InitialPoints is {co.Initial_points}")
    step = 0.1
    points = []

    # Use old Sokolov's algorithm for picking initial points if chosen
    if co.Initial_points.lower() == "Old".lower():
        print("Old algorithm for picking initial points is chosen")
        par_der = []   # deriv

        for itera in range (min(dim+1, CVNumOfIter)) :
            print(f"Started iteration {itera} of SurMinMethod with CVNumOfIter={CVNumOfIter}, dim={dim}")
            if itera == 0 :
                #allArgs = SetAllArgs(inArg, co.Penalty, co.OptStep)
                Val = getVal(inArg)
                print ('\nITER', itera, 'start', Val, 'st', np.nan,  inArg, '\n')
                points = [Point (inArg, Val, Num=0, initial=True)]

            elif itera <= dim :
                nArg = inArg.copy()
                step_i = steps[itera-1]
                Nattempt = 2
                for attempt in range (Nattempt) :
                    nArg[itera-1] += step_i
                    #AllArgs = SetAllArgs(nArg, co.Penalty, co.OptStep)
                    Val = getVal(inArg)
                    Arg, mi, grad = AddPoint ( points, nArg, Val, initial=True)
                    print ('\nITER', itera, mi, Val, grad, 'st', step_i, nArg, '\n')
                    if mi != '***' : break
                    if attempt != Nattempt-1 :
                        nArg[itera - 1] -= step_i
                        if attempt == 0 :  step_i = - step_i
                        else            :  step_i *= -0.05
                steps[itera - 1] = step_i                           # 24.05
                par_der.append(grad*np.sign(step_i))
                if (itera == dim) :
                    min_step = min([abs(steps[ipd] / pd) for ipd, pd in enumerate(par_der)])
                    step = np.sqrt(sum((pd * min_step) ** 2 for pd in par_der))
                    print('par_der', par_der, 'min_step', min_step, step)

    # Extract already evaluated set of initial points from a .res file if chosen               
    elif co.Initial_points.strip()[-4:] == ".res":
        print(f"Initial points are extracted from {co.Initial_points}")
        mode, res_file = (x.strip() for x in co.Initial_points.strip().split(":"))

        if mode.lower() == "initial":
            iterations, vals, args, initial_count = Compare.get_points(res_file, only_initial=True)
        elif mode.lower() == "all":
            iterations, vals, args, initial_count = Compare.get_points(res_file, only_initial=False)

        for iteration in range(len(vals)):
            args_to_append = np.array([])
            for n, arg in enumerate(args[iteration]):
                 if co.OptStep[n] != 0:
                    args_to_append = np.append(args_to_append, arg)

            if iteration < initial_count:
                points.append(Point(args_to_append, vals[iteration], iteration, initial=True))
            else:
                points.append(Point(args_to_append, vals[iteration], iteration, initial=False))
    
    # Use uniform distribution from spotoptim
    elif (co.Initial_points.strip().lower().startswith("qms_lhs") == True or 
          co.Initial_points.strip().lower().startswith("qms-lhs") == True) and bounds is not None:
        _, points_number = co.Initial_points.strip().lower().split(":")
        points_number = int(points_number)
        X = generate_qmc_lhs_design(bounds, n_design=points_number, seed=0)

        for i in range(X.shape[0]):
            val = getVal(X[i])
            points.append(Point(X[i], val, i, initial=True))

    # Wrong option chosen
    else: 
        print(f"Wrong SvF.InitialPoints option: {co.Initial_points}")
        raise ValueError("Wrong SvF.InitialPoints option")

    print(f"Args of initial points: ", [p.Arg for p in points])
    print(f"Vals of initial points: ", [p.Val for p in points])
    return points, step
         

def SurMinSpotoptimMethod ( CVNumOfIter, inArg, steps, getVal, Task=None) :
    """
    Method does surrogate optimization based on spotoptim module's toolkit. 
    Initial points set is constructed by evaluate_initial_points method.
    Main optimization loop is entirely spotoptim's optimizer.

    Args:
        CVNumOfIter (int): maximum number of performed iterations in optimization process.
        stepsIN - initial optimization steps. If any is set to 0 then the according coefficient isn't optimized.
        InArg - Initial value of regularization parameters 
        getVal (function): link to an evaluation method which serves as a blackbox and provides values 
            for the upper level of surrogate optimization.
        Task (Task object): link to a SvF Task object to which calculations belong. 

    Returns:
        list[SvF Point objects]: list of all points calculated throughout optimization
    """

    global init_x_to_y_dict
    init_x_to_y_dict = dict()

    Arg = []
    for ia, a in enumerate(inArg) :
        if steps[ia] != 0 :
            Arg.append(a)
    Arg = np.array (Arg)
    dim = len (Arg)

    print(f"co.Penalty = {co.Penalty}")
    # Immediately calculate and return value from one initial point if iterations are 0
    if CVNumOfIter == 0:
            #AllArgs = SetAllArgs(inArg, co.Penalty, co.OptStep)
            Val = getVal (Arg)
            points = [Point (Arg, Val, Num=0, initial=True)]
            for p in points:  p.prin()
            return points, nan

    # Bounds for each optimization parameter. Should be changed sometimes according to problem's specifics. 
    # regularization parameters too low or too high (relatively) can result in solver error.
    bounds =  [[co.Low_bound, co.High_bound] for _ in range(dim)]
    
    # Evaluate set of initial points for optimization
    points, _ = evaluate_initial_points(CVNumOfIter, Arg, steps, getVal, dim, bounds=bounds)

    # Update of cached initial points in the global dictionary.
    init_x_to_y_dict.clear()
    init_x_to_y_dict.update({
        tuple(np.asarray(p.Arg).flatten()): float(p.Val)
        for p in points
    })
    
    print(f"dim = {dim}, CVNumOfIter = {CVNumOfIter}, len(points) = {len(points)}")

    # Count number of initial points
    initial_n = len(points) 

    # Main optimization loop with spotoptim
    if CVNumOfIter > dim:
        # Output of optimization parameters
        # print(f"Args of initial points: ", [p.Arg for p in points])
        # print(f"Vals of initial points: ", [p.Val for p in points])
        print(f"MAIN OPTIMIZATION LOOP HAS STARTED WITH SPOTOPTIM")
        print(f"Acquisition mode is set to {co.Acquisition_mode}")
        print(f"Low and high bounds for each dimension are [{co.Low_bound},{co.High_bound}]")

        # Numpy array of custom initial points for optimizer
        X_init = np.array([np.asarray(point.Arg).flatten()
                            for point in points]) 

        print(f"X_init = {X_init}")

        # Define spotoptim optimizer
        opt = SpotOptim(
            fun=getVal,
            bounds=bounds,
            acquisition=co.Acquisition_mode,
            max_iter=CVNumOfIter, # Вероятно стоит поменять принцип подсчёта итераций (!!!)
            n_initial=0,
            selection_method='distant',
            n_jobs=1,
            verbose=True,
            tensorboard_log=False,
            tensorboard_clean=True
        )

        # Run optimization
        result = opt.optimize(X0=X_init)
        print(f"points = {points}, result.X = {result.X}, result.y = {result.y}")

        # Add points evaluated in optimization to an array of initial points
        new_points = points + [Point(result.X[i], result.y[i], i, initial=False) for i in range(initial_n, result.X.shape[0])]
        print(f"Args of result points: ", [p.Arg for p in new_points])
        print(f"Vals of result points: ", [p.Val for p in new_points])

        # Save all points in Task object for custom plots
        Task.OptPoints = new_points

        # show graphs from spotoptim or save them in files
        ShowGraphs = co.Show_spotoptim_graphs

        # Plot and save graph of CV error from number of optimizer iterations
        plot_progress(opt, show=ShowGraphs)
        plt.savefig("Surrogate_CVError_to_iter.png", dpi=200)
        plt.close()

        # For two regularization coefficients plot spotoptim 2D graph of the surrogate surface and prediction certainty 
        if dim == 2: 
            plot_surrogate(opt, show=ShowGraphs)
            plt.savefig("Surrogate_2D_surface.png", dpi=200)
            plt.close()


        points = new_points

    return points


def get_sigCV_for_spotoptim(Penal_only_optimized):
    from SvFstart62 import get_sigCV
    model_penal = co.Penalty.copy()

    #print(f"НАСТОЯЩЕЕ ПЕРЕДАННОЕ ЗНАЧЕНИЕ = {Penal_only_optimized}")
    Penal_only_optimized = np.atleast_2d(np.array(Penal_only_optimized))
    # Get complete set of regularization coefficients, including unoptimized.
    #Penal = SetAllArgs(Penal_only_optimized, SvF.Penalty, SvF.OptStep)
    Penal = Penal_only_optimized 
    Penal = np.atleast_2d(np.array(Penal))

    print(f"Penal_only_optimized = {Penal}",
          f"SvF.Penalty = {co.Penalty}", 
          f"SvF.OptStep = {co.OptStep}")
    print(f"PRINTING init_x_to_y_dict: on {co.NoFuncCalls} = {init_x_to_y_dict}")
    #print(f"Penal.shape[0] = {Penal.shape[0]}, Penal.ndim = {Penal.ndim}")
    if Penal.shape[0] == 1:
        if Penal.ndim == 2:
            Penal = Penal[0]
            Penal = SetAllArgs(Penal, model_penal, co.OptStep)

    else:
        print("В get_sigCV передано несколько точек - возвращаю значения для точек инициализации")
        print(f"Массив возвращаемых значений: {np.array(list(init_x_to_y_dict.values()))}")
        return np.array(list(init_x_to_y_dict.values()))
    
    print(f"Penal after 'squeeze': {Penal}")

    return get_sigCV(Penal)
