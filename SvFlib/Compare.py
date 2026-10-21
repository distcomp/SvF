import COMMON as co
from  os  import listdir, getcwd
import re
import numpy as np
import matplotlib.pyplot as plt


def find_res_files():
    """
    Find all .res files in the current directory

    Returns:
        list[str]: names of all .res files
    """
    res_files = []
    files = listdir(getcwd())
    for f in files:
        p  = f.rfind('.res')
        if p + 4 == len(f):
                res_files.append(f)
    return res_files


def get_points(filename, only_initial=False):
    """
    Extract information about results of optimization from .res file

    Args:
        filename (str) - full name (with .res) of results file
        only_initial (bool) - if True returns data only for initial points

    Returns:
        ndarray[int] - array of number of iterations of optimization
        ndarray[float] - array of results on each iteration of optimization
        ndarray[list[float]] - array of points evaluated in optimization
        int - number of initial points
    """
        
    with open(filename) as f:
        lines = f.readlines()

    iterations = []
    vals = []
    args = []
    initial_count = 0
    
    buffer = ""
    points_extract = False
    
    # Read .res file line by line
    for line in lines:
        # Line processing begins only if block containing point data is reached
        if re.search(r'^Points:', line):
            points_extract = True
        elif re.search(r'^addStrToRes:', line):
            points_extract = False
        elif re.search(r'^Time:', line):
            points_extract = False

        if points_extract == False:
            continue 

        # If line contains start of a point data then make it the buffer
        if re.search(r'Num\s+\d+\s+Val', line):
            buffer = line.strip()
        else:
            # Else add line to the previous buffer (because single point data can span multiple lines)
            buffer += " " + line.strip()
        
        # Extract data from the buffer if points data in it is complete
        if buffer and ']' in buffer and '[' in buffer:
            # Теперь buffer содержит целую запись, даже если она была на нескольких строках
            
            # Skip the line if it doesn't contain initianl point and only initial points are needed
            if only_initial and 'INIT' not in buffer:
                buffer = ""
                continue
            
            # Find lines with optimization point data in them using regular expression
            match = re.search(r'Num\s+(\d+)\s+Val\s+([\d\.]+)\s+Arg\s+\[([^\]]+)\]', buffer)
            
            # Extract data for found points
            if match:
                iterations.append(int(match.group(1)))
                vals.append(float(match.group(2)))
                args.append([float(arg) for arg in match.group(3).split()])
                
                # Check if the point is in initial set
                if 'INITIAL' in buffer:
                    initial_count += 1
            
            # Clear buffer for the next points
            buffer = "" 
    
    # Sort points by iteration number (they're sometimes mixed in process)
    sorted_indices = np.argsort(iterations)
    
    return (np.array(iterations)[sorted_indices],
            np.array(vals)[sorted_indices],
            np.array(args)[sorted_indices],
            initial_count)



def compare_results():
    """
    Draw graphs of optimization progress of different tasks solved beforehand for comparison.
    
    Initial points are scattered in the left area and optimization progress 
    is shown as the line of best result over the iterations for each task.
    """

    # Get names of processed .res files
    if co.ResFilesToCompare.lower() == "All".lower():
        # If All option was used find all .res files in the directory
        target_res_files = find_res_files()
    else:
        # Otherways, take the inputted array of names
        target_res_files = co.ResFilesToCompare.strip().strip('[]').split(',')
        target_res_files = [file.strip().strip('"\'') for file in target_res_files]

    # define colors for each graph
    color_list = []
    print("!!!!!!!!!!!!!!!!!", co.ResGraphColors)
    if co.ResGraphColors != []:
        color_list = co.ResGraphColors
        color_list = color_list.strip().strip('[]').split(',')
        color_list = [color_name.strip().strip('"\'') for color_name in color_list]
        
        if len(color_list) != len(target_res_files):
            print("Error in choosing colors for comparison graph")
            color_list = []
    if color_list == []:
        #default_colormap = plt.cm.tab10
        default_colormap = plt.get_cmap('tab10')
        
        color_list = [default_colormap(i % default_colormap.N) for i in range(len(target_res_files))]


    # define labels for each graph
    label_list = []
    if co.ResLegendNames != []:
        label_list = co.ResLegendNames
        label_list = label_list.strip().strip('[]').split(',')
        label_list = [label_name.strip().strip('"\'') for label_name in label_list]
        
        if len(color_list) != len(target_res_files):
            print("Error in choosing labels for comparison graph")
            label_list = []
    if label_list == []:
        label_list = [target_res_files[i] for i in range(len(target_res_files))]

    print(f"Target res files = {target_res_files}")
    print(f"co.Tail_start = {co.Tail_start}")
    print(f"co.ResGraphColors = {co.ResGraphColors}")
    print(f"co.color_list = {color_list}")
    tail_start = int(co.Tail_start)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    did_plot_initial = False
   
    # Draw data from each .res file
    for i, res_file in enumerate(target_res_files):
        iterations, vals, args, initial_count = get_points(res_file)
        print(f"In {res_file:}")
        print(f"Vals: {vals}")
        print(f"Args: {args}")
        print(f"Iterations: {iterations}")
        print(f"Initial count: {initial_count}")

        if did_plot_initial == False:
            did_plot_initial = True
            ax1.axvspan(0, initial_count, alpha=0.15, color="gray", zorder=0)

            ax1.scatter(
                iterations[0:initial_count],
                vals[0:initial_count],
                alpha=0.6,
                s=50,
                label=f"Начальные точки (n={initial_count})",
                color="gray",
                edgecolors="black",
                linewidth=0.5,
                zorder=2,
            )
        # Plot best-so-far curve starting after initial design
        history = vals

        # Best so far across all evaluations
        best_so_far = np.minimum.accumulate(history)
        # Start the red line after initial design
        x_best = iterations[initial_count:]
        y_best = best_so_far[initial_count:]

        ax1.plot(
            x_best,
            y_best,
            linewidth=2,
            label=label_list[i],
            color=color_list[i]
        )

        if (tail_start > initial_count):
            ax2.plot(
                x_best[tail_start - initial_count:],
                y_best[tail_start - initial_count:],
                linewidth=2,
                label=label_list[i],
                color=color_list[i]
            )

    ax1.set_xlabel("Номер итерации", fontsize=11)
    ax1.set_ylabel("Ошибка кросс-валидации", fontsize=11)
    ax2.set_xlabel("Номер итерации", fontsize=11)
    ax2.set_ylabel("Ошибка кросс-валидации", fontsize=11)
    ax1.ticklabel_format(style='plain', useOffset=False, axis='both')
    ax2.ticklabel_format(style='plain', useOffset=False, axis='both')

    title1 = "Прогресс оптимизации"
    ax1.set_title(title1, fontsize=12)

    title2 = "Хвост прогресса оптимизации"
    ax2.set_title(title2, fontsize=12)

    ax1.legend(fontsize=10)
    ax2.legend(fontsize=10)
    # ax1.yscale("log")
    ax1.grid(True, alpha=0.3)
    ax2.grid(True, alpha=0.3)

    # plt.savefig('Comparison_of_optimization_strategies.pdf', format='eps', bbox_inches='tight')
    # plt.savefig('Osc-2.tiff', 
    #         format='tiff', 
    #         dpi=300, 
    #         bbox_inches='tight',
    #         pil_kwargs={'compression': 'jpeg'}) 

    plt.savefig('E-2.pdf', 
            format='pdf', 
            bbox_inches='tight',   
            dpi=300,              
            facecolor='white',     
            edgecolor='none')    
    # plt.savefig('Comparison_of_optimization_strategies.tiff', dpi=300, format='tiff', bbox_inches='tight')
    plt.tight_layout()
    plt.show()
