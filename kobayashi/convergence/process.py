import numpy as np
import sys
import glob
from ibex_io import get_data

def get_benchmark(description):
    if description == "abs":
        return  [5.95659, 1.37185, 5.00871e-1, 2.52429e-1, 1.50260e-1,
                 5.95286e-2, 1.53283e-2, 4.17689e-3, 1.18533e-3, 3.46846e-4,
                 4.70754e-1, 1.69968e-1, 8.68334e-2, 5.25132e-2,
                 1.33378e-2, 1.45867e-3, 1.75364e-4, 2.24607e-5, 3.01032e-6,
                 5.50247e-2, 4.80754e-2, 3.96765e-2, 3.16366e-2,
                 2.35303e-2, 5.83721e-3, 1.56731e-3, 4.53113e-4, 1.37079e-4]
    else:
        return [8.29260, 1.87028, 7.13986e-1, 3.84685e-1, 2.53984e-1,
                1.37220e-1, 4.65913e-2, 1.58766e-2, 5.47036e-3, 1.85082e-3,
                6.63233e-1, 2.68828e-1, 1.56683e-1, 1.04405e-1,
                3.02145e-2, 4.06555e-3, 5.86124e-4, 8.66059e-5, 1.12892e-5,
                1.27890e-1, 1.13582e-1, 9.59578e-2, 7.82701e-2,
                5.67030e-2, 1.88631e-2, 6.46624e-3, 2.28099e-3, 7.93924e-4]

def save_output(fileout,
                contained_string):

    # Get benchmark result
    phi_bench = get_benchmark(contained_string)
    
    # Get error for each matching filename
    output_filenames = sorted(glob.glob("*{}*.xml.out".format(contained_string)))
    for output_filename in output_filenames:
        # Load data
        try:
            data_out = get_data(output_filename)
        except:
            print("test {} output format incorrect".format(output_filename))
            print("\t{}".format(sys.exc_info()))
            return
        # Get error
        phi_calc = data_out["phi1"][:, 0, 0]
        phi_err = phi_calc - phi_bench
        l2_err = np.sqrt(np.sum(np.power(phi_err, 2)) / np.sum(np.power(phi_bench, 2)))
        abs_err = np.sum(np.divide(np.abs(phi_err), phi_bench)) / (1. * len(phi_bench))
        linf_ind = np.abs(phi_err).argmax()
        linf_err = phi_err[linf_ind]
        linf_rel_ind = np.abs(phi_err / phi_bench).argmax()
        linf_rel_err = phi_err[linf_rel_ind] / phi_bench[linf_rel_ind]

        print(phi_err[17], contained_string, data_out["number_of_points"])
        
        # Save data
        for par in ["number_of_points", "weighting", "number_of_moments", "number_of_ordinates"]:
            fileout.write("{}\t".format(data_out[par]))
        for val in [contained_string, l2_err, abs_err, linf_ind, linf_err, linf_rel_ind, linf_rel_err]:
            fileout.write("{}\t".format(val))
        fileout.write("\n")
        # for par in ["spatial_initialization", "sweep_initialization", "solve"]:
        #     fileout.write("{}\t".format(data_out["timing"][par]))
        # for err in phi_err:
        #     fileout.write("{}\t".format(err))
            
    return

if __name__ == '__main__':
    with open("output.txt", 'a') as fileout:
        for contained_string in "abs", "sca":
            save_output(fileout,
                        contained_string)
    
