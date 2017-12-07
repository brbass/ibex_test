import os, sys, subprocess, itertools, multiprocessing, functools
import numpy as np
import xml.etree.ElementTree as et
import matplotlib; matplotlib.use('agg')
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from ibex_io import get_data
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

def plot_points(data,
                output,
                include_points = True,
                include_ifba = False,
                zoomed = False):
    # Add background image
    col = ['#66c2a5','#fc8d62','#e78ac3','#8da0cb','#a6d854', 'k']
    alpha=1.0
    fig, axmain = plt.subplots()
    if zoomed:
        axins = inset_axes(axmain,
                           width="40%",
                           height="40%",
                           loc=4,
                           axes_kwargs=dict(zorder=10))
        axins.set_xlim(0.39, 0.45)
        axins.set_ylim(-0.03, 0.03)
        plt.xticks([], [], visible=False)
        plt.yticks([], [], visible=False)
        mark_inset(axmain, axins, loc1=2, loc2=1,
                   fc='none', ec='0.0',
                   zorder=10, color='k',
                   linewidth=0.5)
    axes = [axmain, axins] if zoomed else [axmain]
    for i, ax in enumerate(axes):
        # Add shapes
        box = plt.Rectangle((-0.627, -0.627), 1.254, 1.254, zorder=1, color=col[0], label="moderator", alpha=alpha)
        circle1 = plt.Circle((0, 0), radius=0.4096, zorder=5, color=col[1], label='fuel', alpha=alpha)
        circle4 = plt.Circle((0, 0), radius=0.4106, zorder=4, color=col[4], label='ifba', alpha=alpha)
        circle2 = plt.Circle((0, 0), radius=0.418, zorder=3, color=col[2], label='gap', alpha=alpha)
        circle3 = plt.Circle((0, 0), radius=0.475, zorder=2, color=col[3], label='clad', alpha=alpha)
        ax.add_patch(circle1)
        if include_ifba:
            ax.add_patch(circle4)
        ax.add_patch(circle2)
        ax.add_patch(circle3)
        ax.add_patch(box)
        
        # Add points
        if include_points:
            points = data["points"]
            size = 0.1 if len(points) > 3000 else 0.25
            size = size if i == 0 else 2
            ax.scatter(points[:,0], points[:,1], s=size, color='k', zorder=7, label='centers')
    
    # Add plot options
    plt.sca(axmain)
    plt.axis('scaled')
    plt.xlabel(r"$x$")
    plt.ylabel(r"$y$")
    leg = plt.legend(framealpha=0.9, scatterpoints=3, loc=1)
    leg.set_zorder(10)

    # Add inset if applicable
    
    # Save plot
    #plt.show()
    plt.savefig("{}.pdf".format(output), bbox_inches='tight')
    plt.close()
    return

def plot_eigenvector(output_file,
                     output_name):
    # Get data from output file
    data = get_data(output_file)
    num_groups = data["number_of_groups"]
    num_points = data["number_of_points"]
    num_moments = data["number_of_moments"]
    phi = np.abs(data["phi"])
    points = data["points"]

    # Normalize eigenvector
    phi = phi / np.mean(phi[:, 0, :])

    # Plot data
    for g in range(num_groups):
        plt.figure(g)
        plt.tripcolor(points[:, 0], points[:, 1], phi[:, 0, g], shading='gouraud')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.colorbar(label="scalar flux")
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig("{}_{}.pdf".format(output_name, g))
        plt.close()

def plot_all():
    # plot_points(get_data("test_scaled4_1.0_full_512.xml.out"),
    #             "points_pincell",
    #             True,
    #             False)
    # plot_points(get_data("test_square5_1.0_full_512.xml.out"),
    #             "points_square",
    #             True,
    #             False)
    # plot_points(get_data("test_scaled4_1.0_full_512.xml.out"),
    #             "points_pincell_zoom",
    #             True,
    #             True,
    #             True)
    # plot_points(get_data("test_square5_1.0_full_512.xml.out"),
    #             "points_square_zoom",
    #             True,
    #             True,
    #             True)
    # plot_points(get_data("test_scaled12_1.0_full_512.xml.out"),
    #             "points_pincell_zoom_big",
    #             True,
    #             True,
    #             True)
    # plot_points(get_data("test_scaled2_1.0_full_512.xml.out"),
    #             "vera1e_geometry",
    #             False,
    #             True,
    #             True)
    # plot_points(get_data("test_mult0.006_1.0_full_237_1.xml.out"),
    #             "vera1e_mult",
    #             True,
    #             True,
    #             True)
    plot_eigenvector("test_mult27_0.0125_0.00625_1.0_full_512_1.xml.out",
                     "vera1b_eigenvector")
    
if __name__ == '__main__':
    plot_all()
