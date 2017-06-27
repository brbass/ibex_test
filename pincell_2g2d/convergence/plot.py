import os, sys, subprocess, itertools, multiprocessing, functools
import numpy as np
import xml.etree.ElementTree as et
#import matplotlib; matplotlib.use('agg')
from matplotlib import pyplot as plt
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
    plt.savefig("{}.pdf".format(output))
    plt.close()
    return

def plot_eigenvectors(data,
                      output):
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
