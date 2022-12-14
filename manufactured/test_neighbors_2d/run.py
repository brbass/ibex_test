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
    data["num_procs"] = 4
    data["parameters"] = ["(RBF)",
                          "(NEIGHBORS)",
                          "(POINTS)",
                          "(CELLS)"]
    data["values"] = []
    data["descriptions"] = []
    neighbor_cases = [8, 10, 12, 14, 16, 18]
    for rbf in ["wendland10", "wendland11", "wendland12", "wendland13", "wendland30", "wendland31", "wendland32", "wendland33"]:
        for neighbors in neighbor_cases:
            for points in [8, 16, 32, 64, 128]:
                cells = points - 1
                data["values"].append([rbf,
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