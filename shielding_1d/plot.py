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

if __name__ == '__main__':
    plot_convergence()
