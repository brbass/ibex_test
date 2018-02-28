from ibex_io import get_data
import sys, os, math
import numpy as np

def get_errors(data):
    # Get benchmark data
    bench_dir = os.path.join(os.path.dirname(__file__), "..", "openmc", "multigroup_benchmark")
    k_bench = np.loadtxt(os.path.join(bench_dir, "k_eigenvalue.txt"))[0]
    phi_bench = np.loadtxt(os.path.join(bench_dir, "mesh", "mesh_tally.txt"))

    # Get error in phi for each group
    phi = data["phi1"][:, 0, :]
    for i, val in enumerate(phi):
        if math.isnan(val[0]) or math.isnan(val[1]):
            print("nan at index {}".format(i))
            for j in range(2):
                phi[i, j] = phi_bench[i, j] * phi[0, j] / phi_bench[0, j]
    phi = phi / np.mean(phi)
    phi_err = phi - phi_bench
    l2_err = [np.sqrt(np.sum(np.power(phi_err[:, i], 2)) / np.sum(np.power(phi_bench[:, i], 2))) for i in range(2)]
    linf_ind = [np.abs(phi_err[:, i]).argmax() for i in range(2)]
    linf_err = [phi_err[linf_ind[i], i] / phi_bench[linf_ind[i], i] for i in range(2)]

    # Get k-eigenvalue error in pcm
    k = data_out["k_eigenvalue"]
    k_err = (k - k_bench) * 1e5
    
    return l2_err, linf_err, k_err

if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("integral_error.py [fileout]")
        sys.exit()
    output_filename = sys.argv[1]
    data_out = get_data(output_filename)
    print(get_errors(data_out))
    
