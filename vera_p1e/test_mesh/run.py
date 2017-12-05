import copy
from ibex_io import full_run_from_template
from ibex_io import full_save_from_template
from ibex_io import get_data
import sys

def run_all(run = True):
    # Set up data list
    data = {}
    if run:
        data["executable"] = "~/code/ibex_parallel/bin/ibex"
    else:
        data["executable"] = "echo"
    data["num_procs"] = 4
    data["parameters"] = ["(POINTS_FILE)", "(CELLS)"]
    mesh_params = [[19, 0.04, 0.004, 512],
                   [22, 0.02, 0.002, 512],
                   [25, 0.01, 0.001, 1024],
                   [28, 0.005, 0.0005, 1024]]
    data["values"] = [["vera1e_mesh_{}_{}_{}.xml".format(i, j, k),
                       str(l)] for (i, j, k, l) in mesh_params]
    data["descriptions"] = [["{}_{}_{}".format(i, j, k),
                             str(l)] for (i, j, k, l) in mesh_params]
    data["prefix"] = "test"
    data["postfix"] = ".xml"
    data["template_filename"] = "template.xml"
    
    # Run problems
    input_filenames = full_run_from_template(data,
                                             True) # Save input files
        
if __name__ == '__main__':
    run_all(True)
