import copy
from ibex_io import full_run_from_template
from ibex_io import full_save_from_template
from ibex_io import get_data
import numpy as np
import sys

def run_case(num_procs,
             num_points,
             fileout,
             run = True):
    # Set up data list
    data = {}
    data["executable"] = "ibex"
    data["num_procs"] = num_procs
    data["parameters"] = ["(NUM_POINTS)",
                          "(TAU)",
                          "(WEIGHTING)",
                          "(INT_CELLS)",
                          "(SCA_INT)"]
    data["values"] = []
    integration_cells = num_points - 1
    for tau in [1.0, 0.5]:
        for weighting in ["basis", "full"]:
            for sca_int in [0, 5]:
                data["values"].append([num_points,
                                       tau,
                                       weighting,
                                       integration_cells,
                                       sca_int])
    data["descriptions"] = copy.deepcopy(data["values"])
    for desc in data["descriptions"]:
        if desc[4] == 0:
            desc[4] = "abs"
        else:
            desc[4] = "sca"
    data["prefix"] = "test"
    data["postfix"] = ".xml"
    data["template_filename"] = "template.xml"
    
    # Run case
    if run:
        input_filenames = full_run_from_template(data,
                                                 True) # Save input files
    else:
        input_filenames = full_save_from_template(data,
                                                  False) # Save input files
        
    # Get output
    for i, input_filename in enumerate(input_filenames):
        try:
            # Get output data
            output_filename = "{}.out".format(input_filename)
            data_out = get_data(output_filename)
            
            # Get errors
            phi_trunc = np.delete(data_out["phi1"], 19)
            if data["values"][i][4] == 0:
                phi_bench = [5.95659, 1.37185, 5.00871e-1, 2.52429e-1, 1.50260e-1,
                             5.95286e-2, 1.53283e-2, 4.17689e-3, 1.18533e-3, 3.46846e-4,
                             4.70754e-1, 1.69968e-1, 8.68334e-2, 5.25132e-2,
                             1.33378e-2, 1.45867e-3, 1.75364e-4, 2.24607e-5, 3.01032e-6,
                             5.50247e-2, 4.80754e-2, 3.96765e-2, 3.16366e-2,
                             2.35303e-2, 5.83721e-3, 1.56731e-3, 4.53113e-4, 1.37079e-4]
            else:
                phi_bench = [8.29260, 1.87028, 7.13986e-1, 3.84685e-1, 2.53984e-1,
                             1.37220e-1, 4.65913e-2, 1.58766e-2, 5.47036e-3, 1.85082e-3,
                             6.63233e-1, 2.68828e-1, 1.56683e-1, 1.04405e-1,
                             3.02145e-2, 4.06555e-3, 5.86124e-4, 8.66059e-5, 1.12892e-5,
                             1.27890e-1, 1.13582e-1, 9.59578e-2, 7.82701e-2,
                             5.67030e-2, 1.88631e-2, 6.46624e-3, 2.28099e-3, 7.93924e-4]
            phi_err = phi_trunc - phi_bench
            l2_err = np.sqrt(np.sum(np.power(phi_err, 2)) / np.sum(np.power(phi_bench, 2)))
            abs_err = np.sum(np.divide(np.abs(phi_err), phi_bench)) / (1. * len(phi_bench))
            
            # Save data
            for val in [data["values"][i][0], data["values"][i][1], data["values"][i][2], data["values"][i][3], data["values"][i][4], l2_err, abs_err]:
                fileout.write("{}\t".format(val))
            for par in ["number_of_moments", "number_of_ordinates", "number_of_points", "weighting"]:
                fileout.write("{}\t".format(data_out[par]))
            for par in ["spatial_initialization", "sweep_initialization", "solve"]:
                fileout.write("{}\t".format(data_out["timing"][par]))
            for err in phi_err:
                fileout.write("{}\t".format(err))
        except:
             print("test {} failed to output data".format(input_filename))
             print("\t{}".format(sys.exc_info()))
        fileout.write("\n")
        
def run_all(run = True):
    # Run cases
    with open("output.txt", 'a') as fileout:
        for num_points, num_procs in zip([11, 21, 31, 41], [4, 4, 2, 1]):
            run_case(num_procs, # num procs
                     num_points,
                     fileout,
                     run)
            
if __name__ == '__main__':
    run_all(False)
