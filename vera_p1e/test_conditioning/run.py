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
    data["num_procs"] = 3
    data["parameters"] = ["(ORDINATES)", "(FILL)", "(NEIGHBORS)", "(TAU)"]
    data["values"] = [[32, 1.0, 8, 1.0],
                      [32, 1.0, 8, 2.0],
                      [32, 1.0, 10, 1.0],
                      [32, 2.0, 8, 1.0],
                      [64, 1.0, 8, 1.0]]
    data["descriptions"] = data["values"]
    data["prefix"] = "test"
    data["postfix"] = ".xml"
    data["template_filename"] = "template.xml"
    
    # Run problems
    input_filenames = full_run_from_template(data,
                                             True) # Save input files
        
if __name__ == '__main__':
    run_all(True)
