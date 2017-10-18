import numpy as np
import itertools
from matplotlib import pyplot as plt
from ibex_io import get_data

def plot_convergence():
    # Get convergence data
    # Columns:
    # 0. Dim points
    # 1. Tau
    # 2. Weighting
    # 3. Dim int cells
    # 4. Scattering int
    # 5. L2 error
    # 6. Abs error
    # 7. Num moments
    # 8. Num ordinates
    # 9. Num points
    # 10. Weighting
    # 11-13. Timing
    # 14-43. Phi err
    data = np.genfromtxt('output.txt', dtype=None , delimiter="\t")
    
    # # Sort data by number of points
    data = sorted(data, key=lambda data: (data[9]))

    # # Get individual arrays
    key0 = [b'basis', b'full']
    key1 = [1.0]#[0.5, 1.0]
    key2 = [0, 5]
    keys = [[i, j, k] for i, j, k in itertools.product(key0, key1, key2)]
    indices = []
    for i, key in enumerate(keys):
        ind = [j for j in range(len(data)) if key[0] in data[j][2] and key[1] == data[j][1] and key[2] == data[j][4]]
        indices.append(ind)
    errors = []
    points = []
    for i in range(len(keys)):
        err = np.abs([data[j][5] for j in indices[i]])
        errors.append(err)
        pt = [data[j][9] for j in indices[i]]
        points.append(pt)

    # Plot data
    plt.figure()
    plt.xlabel("number of points")
    plt.ylabel(r"relative $L_2$ error")
    plt.ylim([10e-4, 1])
    markers = ['D', '^', 's', 'v']
    for i, key in enumerate(keys):
        labels = [key[0].decode(), "abs" if key[2] == 0 else "sca"]
        plt.semilogy(points[i], errors[i], marker=markers[i], label="{}, {}".format(labels[0], labels[1]))
    plt.grid(True, which='major', linestyle='-', color='grey')
    plt.grid(True, which='minor', linestyle='-', color='lightgrey')
    plt.legend()
    plt.savefig("convergence_kobayashi.pdf", bbox_inches='tight')
    plt.show()
    plt.close()

def plot_slices(fileout,
                description,
                z_position):
    # Get data
    data = get_data(fileout)
    points = data["points"]
    phi = data["phi"]

    # Get data for local slice
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
    #plt.savefig("slice_kobayashi_{}_{}.pdf".format(description, position), bbox_inches='tight')
    plt.show()
    plt.close()
    
    
    
if __name__ == '__main__':
    plot_convergence()
    # plot_slices("test_41_1.0_full_40_sca.xml.out",
    #             "41_sca",
    #             55.)
