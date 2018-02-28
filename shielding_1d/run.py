from ibex_io import full_run_from_template
from ibex_io import full_save_from_template
from ibex_io import get_data
import copy
import numpy as np
import sys

def run_all(num_procs,
            run = True):
    # Set up data list
    data = {}
    if run:
        data["executable"] = "ibex"
    else:
        data["executable"] = "echo"
    data["num_procs"] = num_procs
    data["parameters"] = ["(POINTS)",
                          "(WEIGHTING)",
                          "(TAU)"]
    data["values"] = []
    for points in [10, 15, 20, 30, 40, 60, 80, 120,
                   160, 240, 320, 480, 640, 960, 1280, 1920,
                   2560, 3840, 5120, 7680, 10240]:
        for weighting in ["full", "basis"]:
            for tau in [1.0]:
                data["values"].append([points,
                                       weighting,
                                       tau])
    data["descriptions"] = data["values"]
    data["prefix"] = "test"
    data["postfix"] = ".xml"
    data["template_filename"] = "template.xml"
    
    # Run cases
    if run:
        input_filenames = full_run_from_template(data,
                                                 True) # Save input files
    else:
        input_filenames = full_save_from_template(data,
                                                  True)
    
    # Get output
    # for i, input_filename in enumerate(input_filenames):
    #     try:
    #         data_out = get_data("{}.out".format(input_filename))
    #     except:
    #         print("test {} failed to output data".format(input_filename))
    #         print("\t{}".format(sys.exc_info()))

    return input_filenames

if __name__ == '__main__':
    run_all(4, # num procs
            True)
