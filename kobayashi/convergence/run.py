import copy
from ibex_io import full_run_from_template
from ibex_io import full_save_from_template
from ibex_io import get_data
import numpy as np
import sys
import math

def get_parameters():
    # Get sets of points and cells
    parameters = []
    procs = []
    #point_cases = [11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 39, 41]
    #point_cases = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 35, 40, 42]
    point_cases = [35, 40, 42]
    #point_cases = [15, 17, 25, 29, 31, 35]#[16, 18, 24, 30, 35, 36]
    #point_cases = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 40]
    for points in point_cases:
        num_points = np.power(points, 3)
        mem = num_points * 0.0012
        proc = int(np.floor(100./mem))
        if proc < 1:
            print("case with {} points can't run with 0 procs".format(points))
        else:
            if proc > 4:
                proc = 4
            cells = int(math.ceil((points - 1)/10.0))*10
            for weighting in ["full", "basis"]:
                for sca_int in [0, 5]:
                    parameters.append([points, cells, sca_int, weighting])
                    procs.append(proc)
    proc_cases = np.unique(procs)[::-1]
    data = []
    for i, proc in enumerate(proc_cases):
        local_data = []
        for local_proc, parameter in zip(procs, parameters):
            if local_proc == proc:
                local_data.append(parameter)
        data.append(local_data)
        
    return proc_cases, data

def run_case(num_procs,
             parameters,
             run = True):
    # Get number of threads
    if num_procs == 1:
        num_threads = 4
    elif num_procs == 2:
        num_threads = 2
    else:
        num_threads = 1
    thread_parameters = [parameter + [num_threads] for parameter in parameters]
        
    # Set up data list
    data = {}
    if run:
        data["executable"] = "ibex"
    else:
        data["executable"] = "echo"
    data["num_procs"] = num_procs
    data["parameters"] = ["(POINTS)",
                          "(CELLS)",
                          "(SCA_INT)",
                          "(WEIGHTING)",
                          "(NUM_THREADS)"]
    data["values"] = thread_parameters
    data["descriptions"] = copy.deepcopy(data["values"])
    for desc in data["descriptions"]:
        if desc[2] == 0:
            desc[2] = "abs"
        else:
            desc[2] = "sca"
    data["prefix"] = "test"
    data["postfix"] = ".xml"
    data["template_filename"] = "template.xml"
    
    # Run case
    if run:
        input_filenames = full_run_from_template(data,
                                                 True) # Save input files
    else:
        input_filenames = full_save_from_template(data,
                                                  True)
        
def run_all(run = True):
    # Run cases
    procs, data_cases = get_parameters()
    for proc, local_data in zip(procs, data_cases):
        run_case(proc, # num procs
                 local_data,
                 run)
            
if __name__ == '__main__':
    run_all(True)
 
