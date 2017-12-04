import numpy as np
from matplotlib import pyplot as plt
from ibex_io import get_data
# from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

def plot_convergence():
    # Get convergence data
    data = np.genfromtxt('output_plot.txt', dtype=None , delimiter="\t")
    
    # Sort data by number of points
    data = sorted(data, key=lambda data: (data[1]))

    # Get individual arrays
    keys = [[b'basis', b'square'], [b'basis', b'scaled'], [b'full', b'square'], [b'full', b'scaled']]
    indices = []
    for i, key in enumerate(keys):
        ind = [j for j in range(len(data)) if key[0] in data[j][2] and key[1] in data[j][0]]
        indices.append(ind)
    errors = []
    points = []
    for i in range(len(keys)):
        err = np.abs([data[j][3] for j in indices[i]])
        errors.append(err)
        pt = [data[j][1] for j in indices[i]]
        points.append(pt)
        
    # Plot data
    plt.figure()
    plt.xlabel("number of points")
    plt.ylabel(r"$k$-eigenvalue error (pcm)")
    plt.xlim([1e3, 1e5])
    plt.ylim([10, 1e3])
    colors = ['#66c2a5','#e78ac3','#fc8d62','#8da0cb']
    markers = ['D', 's', '^', 'v']
    styles = ['-', '--', '-', '--']
    labels = ["basis", "basis", "full", "full"]
    ln_group = [0, 1, 0, 1]
    lns = [[],[]]
    for i, key in enumerate(keys):
        ln = plt.loglog(points[i], errors[i],
                        marker=markers[i],
                        color=colors[i],
                        linestyle=styles[i],
                        label=labels[i])
        lns[ln_group[i]].append(ln[0])
    plt.grid(True, which='major', linestyle='-', color='grey')
    plt.grid(True, which='minor', linestyle='-', color='lightgrey')
    leg1 = plt.legend(lns[0], [labels[0], labels[2]],
                      title="square", loc=[0.05, 0.05])#loc=[0.62, 0.81])
    leg2 = plt.legend(lns[1], [labels[1], labels[3]],
                      title="scaled", loc=[0.25, 0.05])#loc=[0.81, 0.81])
    plt.gca().add_artist(leg1)
    plt.savefig("convergence_vera1e.pdf", bbox_inches='tight')
    plt.show()
    plt.close()

def plot_eigenvector(fileout,
                     description,
                     zoomed = False):
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
        if zoomed:
            axins = inset_axes(ax,
                               width="40%",
                               height="40%",
                               loc=1)
            axins.tripcolor(points[:,0], points[:,1], phi[:,0, g], shading='gouraud')
            axins.set_xlim(0.39, 0.45)
            axins.set_ylim(-0.03, 0.03)
            plt.xticks([], [], visible=False)
            plt.yticks([], [], visible=False)
            mark_inset(ax, axins, loc1=2, loc2=4,
                       fc='none', ec='0.0',
                       color='k', linewidth=0.5)
        plt.tight_layout()
        plt.savefig("eigenvector_vera1e_{}_{}.pdf".format(description, g), bbox_inches='tight')
        #plt.show()
        plt.close()
        
if __name__ == '__main__':
    # plot_eigenvector("test_scaled12_1.0_full_1024.xml.out",
    #                  "scaled12")
    # plot_eigenvector("test_scaled12_1.0_full_1024.xml.out",
    #                  "scaled12_zoom",
    #                  True)
    # plot_eigenvector("test_scaled8_0.0_full_1024.xml.out",
    #                  "scaled8_0.0")
    # plot_eigenvector("test_scaled8_1.0_full_1024.xml.out",
    #                  "scaled8_1.0")
    # plot_eigenvector("test_square7_1.0_full_1024.xml.out",
    #                  "square7")
    plot_convergence()
