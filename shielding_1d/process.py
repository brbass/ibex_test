import numpy as np
import sys
import glob
from ibex_io import get_data

def get_errors(fileout,
               contained_string):
    # Get benchmark results
    phi_bench = np.loadtxt("openmc/mesh_tally.txt")
    # phi_bench = np.loadtxt("yak/phi_average_1000_500.txt")
    
    # Get errors for each set of output data
    output_filenames = sorted(glob.glob("*{}*.xml.out".format(contained_string)))
    for output_filename in output_filenames:
        try:
            data_out = get_data(output_filename)
        except:
            print("test {} output format incorrect".format(output_filename))
            print("\t{}".format(sys.exc_info()))
            return
        
        # Get phi errors
        phi = data_out["phi1"][:, 0, :]
        phi_err = phi - phi_bench
        l2_err = [np.sqrt(np.sum(np.power(phi_err[:, i], 2)) / np.sum(np.power(phi_bench[:, i], 2))) for i in range(2)]
        linf_ind = [np.abs(phi_err[:, i]).argmax() for i in range(2)]
        linf_err = [phi_err[linf_ind[i], i] / phi_bench[linf_ind[i], i] for i in range(2)]
        
        # Output data
        fileout.write("{}\t".format(contained_string))
        for par in ["number_of_points", "weighting"]:
            fileout.write("{}\t".format(data_out[par]))
        for err in l2_err[0], l2_err[1], linf_err[0], linf_err[1]:
            fileout.write("{}\t".format(err))
        fileout.write("\n")
            
if __name__ == '__main__':
    with open("output.txt", 'a') as fileout:
        for contained_string in "0.0", "0.5", "1.0":
            get_errors(fileout,
                       contained_string)
