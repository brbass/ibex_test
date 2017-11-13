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
    data["parameters"] = ["(POINTS_FILE)", "(CELLS)"]
    mesh_params = [[18, 0.00625, 0.00125, 256],
                   [16, 0.0125, 0.0025, 128],
                   [14, 0.025, 0.005, 64],
                   [12, 0.05, 0.01, 32]]
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
