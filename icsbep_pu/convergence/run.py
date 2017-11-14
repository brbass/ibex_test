from ibex_io import full_run_from_template
from ibex_io import full_save_from_template
from ibex_io import get_data
import copy
import numpy as np
import sys

def get_parameters():
    # Get sets of points and cells
    point_sets = []
    cell_sets = []
    for xpts in range(10, 29, 2):
        ypts = int(np.rint(xpts * 1.2))
        zpts = int(np.rint(xpts * 1.5))
        point_sets.append([xpts, ypts, zpts])
        cell_sets.append([xpts-1, ypts-1, zpts-1])

    # Get estimated memory
    procs = []
    for point_set in point_sets:
        num_points = np.prod(point_set)
        mem = num_points * 0.0012 # Estimated memory from Kobayashi
        proc = int(np.floor(100./mem))
        if proc < 1:
            print("case can't run with 0 procs")
        elif proc > 4:
            proc = 4
        procs.append(proc)
    print(procs)
    # Get sets of points and cells that will run using the same number of procs
    proc_cases = np.unique(procs)
    data = []
    for i, proc in enumerate(proc_cases):
        local_data = []
        for local_proc, point_set, cell_set in zip(procs, point_sets, cell_sets):
            if local_proc == proc:
                local_data.append(point_set + cell_set)
        data.append(local_data)
    return proc_cases, data

def run_case(num_procs,
             point_sets,
             run = True):
    # Set up data list
    data = {}
    if run:
        data["executable"] = "ibex"
    else:
        data["executable"] = "echo"
    data["num_procs"] = num_procs
    data["parameters"] = ["(POINTS1)",
                          "(POINTS2)",
                          "(POINTS3)",
                          "(CELLS1)",
                          "(CELLS2)",
                          "(CELLS3)",
                          "(WEIGHTING)"]
    data["values"] = []
    for weighting in ["full", "basis"]:
        for point_set in point_sets:
            data["values"].append(point_set + [weighting])
    data["descriptions"] = data["values"]
    data["prefix"] = "test"
    data["postfix"] = ".xml"
    data["template_filename"] = "template.xml"

    # Run cases
    input_filenames = full_run_from_template(data,
                                             True) # Save input files
    
    # Get output
    # for i, input_filename in enumerate(input_filenames):
    #     try:
    #         data_out = get_data("{}.out".format(input_filename))
    #     except:
    #         print("test {} failed to output data".format(input_filename))
    #         print("\t{}".format(sys.exc_info()))
    
def run_all(run = True):
    # Get cases
    procs, data_cases = get_parameters()

    # Run cases that share a number of procs
    for proc, local_data in zip(procs, data_cases):
        run_case(proc,
                 local_data,
                 run)
        
if __name__ == '__main__':
    run_all(True)
