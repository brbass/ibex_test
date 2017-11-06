import numpy as np
from matplotlib import pyplot as plt
from ibex_io import get_data
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

def plot_convergence():
    # Get convergence data
    data = np.genfromtxt('output.txt', dtype=None , delimiter="\t")
    
    # Sort data by number of points
    data = sorted(data, key=lambda data: (data[6]))

    # Get individual arrays
    keys = [[b'basis', b'square'], [b'basis', b'scaled'], [b'full', b'square'], [b'full', b'scaled']]
    indices = []
    for i, key in enumerate(keys):
        ind = [j for j in range(len(data)) if key[0] in data[j][7] and key[1] in data[j][0]]
        indices.append(ind)
    errors = []
    points = []
    for i in range(len(keys)):
        err = [data[j][-1] for j in indices[i]]
        errors.append(err)
        pt = [data[j][6] for j in indices[i]]
        points.append(pt)
        
    # Plot data
    plt.figure()
    plt.xlabel("number of points")
    plt.ylabel("error in pcm")
    plt.ylim([0.1, 100])
    markers = ['D', '^', 's', 'v']
    for i, key in enumerate(keys):
        plt.semilogy(points[i], errors[i], marker=markers[i], label="{}, {}".format(key[0].decode(), key[1].decode()))
    plt.grid(True, which='major', linestyle='-', color='grey')
    plt.grid(True, which='minor', linestyle='-', color='lightgrey')
    plt.legend()
    plt.savefig("convergence_vera1b.pdf", bbox_inches='tight')
    #plt.show()
    plt.close()

def plot_eigenvector(fileout,
                     description):
    # Get problem data
    data = get_data(fileout)

    num_groups = data["number_of_groups"]
    phi = data["phi"]
    points = data["points"]
    
    for g in range(num_groups):
        fig, ax = plt.subplots()
        plt.tripcolor(points[:,0], points[:,1], phi[:,0, g], shading='gouraud')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.colorbar(label="scalar flux")
        plt.axis('equal')
        plt.savefig("eigenvector_vera1b_{}_{}.pdf".format(description, g), bbox_inches='tight')
        plt.show()
        plt.close()
    
if __name__ == '__main__':
    plot_convergence()
    plot_eigenvector("test_scaled12_1.0_full_512.xml.out",
                     "scaled12")
    plot_eigenvector("test_scaled8_1.0_full_512.xml.out",
                     "scaled8_1.0")
    plot_eigenvector("test_scaled8_0.0_full_256.xml.out",
                     "scaled8_0.0")
    plot_eigenvector("test_square7_1.0_full_512.xml.out",
                     "square7")

