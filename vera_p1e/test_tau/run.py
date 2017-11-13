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
    data["parameters"] = ["(TAU)", "(TAU_METHOD)"]
    data["values"] = [[1.0, "none"],
                      [2.0, "none"],
                      [0.05, "constant"],
                      [0.1, "constant"],
                      [0.025, "constant"]]
    data["descriptions"] = data["values"]
    data["prefix"] = "test"
    data["postfix"] = ".xml"
    data["template_filename"] = "template.xml"
    
    # Run problems
    input_filenames = full_run_from_template(data,
                                             True) # Save input files
        
if __name__ == '__main__':
    run_all(True)
