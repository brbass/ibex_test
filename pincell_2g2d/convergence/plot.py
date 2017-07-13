import os, sys, subprocess, itertools, multiprocessing, functools
import numpy as np
import xml.etree.ElementTree as et
import matplotlib; matplotlib.use('agg')
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from ibex_io import get_data

def plot_points(data,
                output):
    # Add background image
    col = ['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854', 'k']
    alpha=1.0
    fig, ax = plt.subplots()
    box = plt.Rectangle((-0.627, -0.627), 1.254, 1.254, zorder=1, color=col[0], label="moderator", alpha=alpha)
    circle1 = plt.Circle((0, 0), radius=0.4095, zorder=3, color=col[1], label='fuel', alpha=alpha)
    circle2 = plt.Circle((0, 0), radius=0.475, zorder=2, color=col[2], label='clad', alpha=alpha)
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.add_patch(box)

    # Add points
    points = data["points"]
    plt.scatter(points[:,0], points[:,1], s=2, color='k', zorder=4, label='centers')
    
    # Add plot options
    plt.axis('scaled')
    plt.xlabel(r"$x$")
    plt.ylabel(r"$y$")
    leg = plt.legend(framealpha=0.9, scatterpoints=3)

    # Save plot
    #plt.show()
    plt.savefig("{}.pdf".format(output), bbox_inches='tight')
    plt.close()
    return

def plot_eigenvectors(data,
                      output):
    # Get data
    num_groups = data["number_of_groups"]
    num_points = data["number_of_points"]
    num_moments = data["number_of_moments"]
    phi = np.abs(data["phi"])*100
    points = data["points"]
    def fmt(x, pos):
        return r'{:.3f}'.format(x)
        # a, b = '{:.2f}'.format(x).split('f')
        # b = int(b)
        # return r'${} \times 10^{{{}}}$'.format(a, b)

    for g in range(num_groups):
        # Plot data
        #plt.figure()
        plt.figure(figsize=(5.5, 4.125))
        plt.tripcolor(points[:, 0], points[:, 1], phi[:, 0, g], shading='gouraud')

        # Plot options
        plt.xlabel("x")
        plt.ylabel("y")
        plt.colorbar(label="scalar flux", format=ticker.FuncFormatter(fmt))
        plt.axis('equal')
        plt.tight_layout()
        #print(plt.gcf().get_size_inches())
        
        # Save plot
        plt.savefig("{}_g{}.pdf".format(output, g), bbox_inches='tight')
        plt.close()
    #plt.show()
    return

def plot_all():
    plot_points(get_data("ibex_pincell_3_weight_3.0.xml.out"),
                "points_pincell")
    plot_points(get_data("ibex_square_3_weight_3.0.xml.out"),
                "points_square")
    plot_eigenvectors(get_data("ibex_pincell_6_flux_3.0.xml.out"),
                      "eigenvectors_pincell")

if __name__ == '__main__':
    plot_all()
