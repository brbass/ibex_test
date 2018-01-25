from ibex_io import full_run_from_template
from ibex_io import full_save_from_template
import copy
import sys
import numpy as np
import xml.etree.ElementTree as et

def get_data():
    # Set up data list
    data = {}
    data["executable"] = "ibex"
    data["num_procs"] = 8
    data["parameters"] = ["(RBF)",
                          "(INT_ORDS)",
                          "(NEIGHBORS)",
                          "(POINTS)",
                          "(CELLS)"]
    data["values"] = []
    data["descriptions"] = []
    for rbf, neighbor_cases in zip(["wendland11", "wendland33"],
                                   [[6, 8, 10, 12, 14], [8, 10, 12, 14, 16, 18]]):
        for int_ords in [8, 16, 32]:
            for neighbors in neighbor_cases:
                for points in [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]:
                    if neighbors <= points:
                        cells = points - 1
                        data["values"].append([rbf,
                                               int_ords,
                                               neighbors,
                                               points,
                                               cells])
                    
    data["descriptions"] = data["values"]
    data["prefix"] = "test"
    data["postfix"] = ".xml"
    data["template_filename"] = "template.xml"
    
    return data

def run_all(run = True):
    # Get data
    data = get_data()
    
    # Run case
    if run:
        input_filenames = full_run_from_template(data,
                                                 True) # Save input files
    else:
        input_filenames = full_save_from_template(data,
                                                  True) # Save input files

if __name__ == '__main__':
    run_all(True)
