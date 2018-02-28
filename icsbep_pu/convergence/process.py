#from run import get_parameters, run_case
import numpy as np
import sys
import glob
from ibex_io import get_data

def get_errors(fileout):
    # Get benchmark results
    k_bench = np.loadtxt("../multigroup_benchmark/k_eigenvalue.txt")[0]
    phi_bench = np.loadtxt("../multigroup_benchmark/mesh_tally.txt")

    # Get errors for each set of output data
    output_filenames = sorted(glob.glob("*.xml.out"))
    for output_filename in output_filenames:
        try:
            data_out = get_data(output_filename)
        except:
            print("test {} output format incorrect".format(output_filename))
            print("\t{}".format(sys.exc_info()))
            return

        # Get phi errors
        phi = data_out["phi1"][:, 0, 0]
        phi = phi / np.mean(phi)
        phi_err = phi - phi_bench
        l2_err = np.sqrt(np.sum(np.power(phi_err, 2)) / np.sum(np.power(phi_bench, 2)))
        linf_ind = np.abs(phi_err).argmax()
        linf_err = phi_err[linf_ind] / phi_bench[linf_ind]
        
        # Get k-eigenvalue error in pcm
        k = data_out["k_eigenvalue"]
        k_err = (k - k_bench) * 1e5
        
        # Output data
        for par in ["number_of_points", "weighting"]:
            fileout.write("{}\t".format(data_out[par]))
        for err in k_err, l2_err, linf_err:
            fileout.write("{}\t".format(err))
        fileout.write("\n")

def plot_slice():
    z_position = 0.0
    
    data = get_data("test_32_38_48_31_37_47_full.xml.out")
    points = data["points"]

    indices = [i for i in range(len(points)) if points[i][2] == z_position]
    if len(indices) == 0:
        print("no indices found")
        return
    slice_points = points[indices]
    slice_phi = phi[indices, 0, 0]
    # Plot data
    plt.tripcolor(slice_points[:,0], slice_points[:,1], slice_phi, shading="gouraud")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.colorbar(label="scalar flux")
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig("slice_icsbep_{}.pdf".format(z_position), bbox_inches='tight')
    plt.close()
    
if __name__ == '__main__':
    with open("output.txt", 'a') as fileout:
        get_errors(fileout)
    
