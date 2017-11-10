import copy
from ibex_io import full_run_from_template
from ibex_io import full_save_from_template
from ibex_io import get_data
import sys

def run_all(run = True):
    # Set up data list
    data = {}
    if run:
        data["executable"] = "ibex"
    else:
        data["executable"] = "echo"
    data["num_procs"] = 4
    data["parameters"] = ["(POINTS_FILE)"]
    initial_delta = [0.001, 0.002, 0.005, 0.01]
    data["values"] = [["vera1e_mesh_12_0.05_{}.xml".format(i)] for i in initial_delta]
    data["descriptions"] = [[i] for i in initial_delta]
    data["prefix"] = "test"
    data["postfix"] = ".xml"
    data["template_filename"] = "template.xml"
                    
    # Run problems
    input_filenames = full_run_from_template(data,
                                             True) # Save input files
        
if __name__ == '__main__':
    run_all(True)
