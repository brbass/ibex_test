import numpy as np
import itertools
from matplotlib import pyplot as plt
from ibex_io import get_data

def plot_convergence():
    # Get convergence data
    # Columns:
    # 0. Dim points
    # 1. Dim int cells
    # 2. Scattering int
    # 3. Weighting
    # 4. L2 error
    # 5. Abs error
    # 6. Num moments
    # 7. Num ordinates
    # 8. Num points
    # 9. Weighting
    # 10-12. Timing
    # 13-42. Phi err
    sca_ind, wei_ind, num_ind = 2, 3, 8
    l2_ind = 4
    data = np.genfromtxt('output.txt',
                         dtype=None,
                         usecols=range(10))
    
    # Sort data by number of points
    data = sorted(data, key=lambda data: (data[num_ind]))
    
    # Get individual arrays
    key0 = [b'basis', b'full']
    key1 = [0, 5]
    keys = [[i, j] for i, j in itertools.product(key0, key1)]
    indices = []
    for i, key in enumerate(keys):
        ind = [j for j in range(len(data)) if key[0] in data[j][wei_ind] and key[1] == data[j][sca_ind]]
        indices.append(ind)
    errors = []
    points = []
    for i in range(len(keys)):
        err = np.abs([data[j][l2_ind] for j in indices[i]])
        errors.append(err)
        pt = [data[j][num_ind] for j in indices[i]]
        points.append(pt)
        
    # Plot data
    fig, ax = plt.subplots()
    plt.xlabel("number of points")
    plt.ylabel(r"$L_2$ error")
    plt.xlim([1e3, 1e5])
    plt.ylim([1e-3, 1])
    colors = ['#66c2a5','#e78ac3','#fc8d62','#8da0cb']
    markers = ['D','s','^','v']
    styles = ["-","--","-","--"]
    lns = [[],[]]
    for i, key in enumerate(keys):
        labels = [key[0].decode(), "abs" if key[1] == 0 else "sca"]
        ln_ind = 0 if key[1] == 0 else 1
        ln = ax.loglog(points[i], errors[i], color=colors[i], marker=markers[i], linestyle=styles[i])
        lns[ln_ind].append(ln[0])
    plt.grid(True, which='major', linestyle='-', color='grey')
    plt.grid(True, which='minor', linestyle='-', color='lightgrey')
    leg1 = plt.legend(lns[0], [key0[0].decode(), key0[1].decode()], title="absorbing", loc=[0.62, 0.79])
    leg2 = plt.legend(lns[1], [key0[0].decode(), key0[1].decode()], title="scattering", loc=[0.81, 0.79])
    plt.gca().add_artist(leg1)
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
