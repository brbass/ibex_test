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
    data["parameters"] = ["(POINTS_FILE)"]
    data["values"] = [["vera1e_mesh_6_0.1_0.02.xml"], ["vera1e_mesh_8_0.05_0.005.xml"], ["vera1e_mesh_10_0.05_0.001.xml"]]
    data["descriptions"] = [[6], [8], [10]]
    data["prefix"] = "test"
    data["postfix"] = ".xml"
    data["template_filename"] = "template.xml"
                    
    # Run problems
    input_filenames = full_run_from_template(data,
                                             True) # Save input files
        
if __name__ == '__main__':
    run_all(True)
