import numpy as np
from matplotlib import pyplot as plt
from ibex_io import get_data
import matplotlib as mpl

def plot_convergence():
    # Get convergence data
    data = np.genfromtxt('output_plot.txt', dtype=None , delimiter="\t")
    
    # Sort data by number of points
    data = sorted(data, key=lambda data: (data[1]))

    # Get individual arrays
    keys = [b'basis', b'full']
    indices = []
    for i, key in enumerate(keys):
        ind = [j for j in range(len(data)) if key in data[j][2]]
        indices.append(ind)
    errors = []
    points = []
    for i in range(len(keys)):
        err = np.abs([[data[j][3], data[j][4]] for j in indices[i]])
        errors.append(err)
        pt = [data[j][1] for j in indices[i]]
        points.append(pt)
        
    # Plot data
    plt.figure()
    plt.xlabel("number of points")
    plt.ylabel(r"relative $L_2$ error")
    plt.xlim([1e1, 1e4])
    plt.ylim([1e-6, 1e0])
    colors = [['#66c2a5','#fc8d62'],['#e78ac3','#8da0cb']]
    markers = [['D','^'], [ 's','v']]
    styles = [['-', '-'], ['--', '--']]
    labels = [["basis", "full"], ["basis", "full"]]
    lns = [[],[]]
    for i, key in enumerate(keys):
        for g in range(2):
            ln = plt.loglog(points[i], errors[i][:, g],
                            marker=markers[g][i],
                            color=colors[g][i],
                            linestyle=styles[g][i],
                            label=labels[g][i])
            lns[g].append(ln[0])
    plt.grid(True, which='major', linestyle='-', color='grey')
    plt.grid(True, which='minor', linestyle='-', color='lightgrey')
    leg1 = plt.legend(lns[0], labels[0],
                      title="group 1", loc=[0.62, 0.81])
    leg2 = plt.legend(lns[1], labels[1],
                      title="group 2", loc=[0.81, 0.81])
    plt.gca().add_artist(leg1)
    plt.savefig("shielding1d_convergence.pdf", bbox_inches='tight')
    plt.show()
    plt.close()
    return

def plot_geometry():
    colors = ['#fc8d62','#8da0cb','#66c2a5','#e78ac3']
    labels = ["source", "moderator", "absorber"]
    surfaces = [0., 0.5, 3.0, 4.0]
    height = 1.5
    
    fig, ax = plt.subplots()
    for i, (xmin, xmax) in enumerate(zip(surfaces[:-1], surfaces[1:])):
        box = plt.Rectangle((xmin, 0), xmax - xmin, height, zorder=1, color=colors[i], label=labels[i])
        ax.add_patch(box)
    ax.set_xlim([0, 4])
    ax.set_ylim([0, height])
    plt.axis('scaled')
    plt.xticks([0, 0.5, 1.0, 3.0, 4.0])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.xlabel(r"$x$")
    plt.legend(loc='upper right', framealpha=0.9)
    plt.savefig("shielding1d_geometry.pdf", bbox_inches='tight')
    return
    
def plot_solution(output_file):
    data = get_data(output_file)
    num_groups = data["number_of_groups"]
    num_points = data["number_of_points"]
    phi = data["phi"]
    points = data["points"]
    
    labels = ["fast", "thermal"]
    colors = ['#66c2a5','#fc8d62','#e78ac3','#8da0cb']
    styles = ['-', '--']
    
    plt.figure()
    for g in range(num_groups):
        plt.plot(points[:, 0], phi[:, 0, g],
                 label=labels[g], color=colors[g], linestyle=styles[g])
    plt.grid(True, which='major', linestyle='-', color='lightgrey')
    plt.grid(True, which='minor', linestyle='-', color='lightgrey')
    plt.xlabel("x")
    plt.ylabel("scalar flux")
    plt.legend()
    plt.savefig("shielding1d_solution.pdf", bbox_inches='tight')
    
    return

if __name__ == '__main__':
    # plot_convergence()
    # plot_geometry()
    plot_solution("test_2560_full_1.0.xml.out")
