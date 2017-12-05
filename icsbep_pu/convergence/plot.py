import numpy as np
from matplotlib import pyplot as plt
from ibex_io import get_data
# from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

# Data columns:
# 0: points; 1: basis/full; 2: k-eigenvalue err; 3: l2 error; 4: linf error

def plot_convergence():
    # Get convergence data
    data = np.genfromtxt('output.txt', dtype=None , delimiter="\t")
    
    # Sort data by number of points
    data = sorted(data, key=lambda data: (data[0]))
    
    # Get individual arrays
    keys = [b'basis', b'full']
    indices = []
    for i, key in enumerate(keys):
        ind = [j for j in range(len(data)) if key[0] in data[j][1]]
        indices.append(ind)
    k_errors = []
    l2_errors = []
    points = []
    for i in range(len(keys)):
        k_err = np.abs([data[j][2] for j in indices[i]])
        l2_err = np.abs([data[j][3] for j in indices[i]])
        k_errors.append(k_err)
        l2_errors.append(l2_err)
        point = [data[j][0] for j in indices[i]]
        points.append(point)
    
    # Plot data
    colors = ['#66c2a5','#fc8d62','#e78ac3','#8da0cb']
    markers = ['D', '^', 's', 'v']
    styles = ['-', '--']
    labels = [key.decode() for key in keys]
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    lns = []
    for i, key in enumerate(keys):
        ln1 = ax1.loglog(points[i], k_errors[i], marker=markers[i], color=colors[i], linestyle=styles[0], label="{}".format(labels[i]))
        ln2 = ax2.loglog(points[i], l2_errors[i], marker=markers[2 + i], color=colors[2 + i], linestyle=styles[1], label="{}".format(labels[i]))
        lns.append(ln1)
        lns.append(ln2)
    ax1.set_xlabel("number of points")
    ax1.set_ylabel(r"$k$-eigenvalue error (pcm)")
    ax1.set_xlim([1e3, 1e5])
    ax1.set_ylim([1e2, 1e4])
    ax1.grid(True, which='major', linestyle='-', color='grey')
    ax1.grid(True, which='minor', linestyle='-', color='lightgrey')
    ax1.legend(title=r"$k$-eigenvalue", loc=[0.59, 0.79])
    ax2.set_ylabel(r"relative $L_2$ error")
    ax2.set_ylim([1e-3, 1e-1])
    ax2.legend(title=r"$L_2$", loc=[0.81, 0.79])
    plt.savefig("icsbep_convergence.pdf", bbox_inches='tight')
    plt.show()
    plt.close()

if __name__ == '__main__':
    plot_convergence()
