import copy
from ibex_io import full_run_from_template
from ibex_io import full_save_from_template
from ibex_io import get_data
import numpy as np
import sys
import math


def run_case(num_procs,
             fileout,
             run = True):
    # Set up data list
    for executable, description in zip(["~/code/ibex_parallel/bin/ibex"], ["big"]):
        data = {}
        if run:
            data["executable"] = executable
        else:
            data["executable"] = "echo"
        data["num_procs"] = num_procs
        data["parameters"] = ["(NUM_THREADS)"]
        data["values"] = [[i] for i in range(1, 5)]
        data["descriptions"] = data["values"]
        data["prefix"] = "test_{}".format(description)
        data["postfix"] = ".xml"
        data["template_filename"] = "template.xml"
        
        # Run cases
        input_filenames = full_run_from_template(data,
                                                 True) # Save input files
        # Get output
        for i, input_filename in enumerate(input_filenames):
            try:
                # Get output data
                output_filename = "{}.out".format(input_filename)
                data_out = get_data(output_filename)
                
                # Get errors
                phi_trunc = data_out["phi1"]
                
                # Save data
                for val in [data["values"][i][0], phi_trunc[0], phi_trunc[1]]:
                    fileout.write("{}\t".format(val))
            except:
                print("test {} failed to output data".format(input_filename))
                print("\t{}".format(sys.exc_info()))
            fileout.write("\n")
        
def run_all(run = True):
    # Run cases
    with open("output.txt", 'a') as fileout:
        run_case(1, # num cases to run at once
                 fileout,
                 run)
            
if __name__ == '__main__':
    run_all(True)
