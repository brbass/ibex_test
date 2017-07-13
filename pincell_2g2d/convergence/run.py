import os, sys, subprocess, itertools, multiprocessing, functools
import numpy as np
import xml.etree.ElementTree as et
import matplotlib; matplotlib.use('Agg')
from matplotlib import pyplot as plt
from ibex_io import get_data

def get_filename(weighting,
                 radius,
                 points_description,
                 output = False):
    filename = "ibex_{}_{}_{}.xml".format(points_description,
                                          weighting,
                                          radius)
    if output:
        filename = filename + ".out"
    return filename

def get_mesh_data(description):
    if description == "pincell":
        return [["pincell_clad_0.4095_0.475_1.254_{}_{}_{}.xml".format(3*i, i, 8*i),"{0} {0}".format(24*i), "pincell_{}".format(i)] for i in range(2, 7)]
    elif description == "square":
        return [["square_1.254_{}.xml".format(10*i),"{0} {0}".format(20*i - 1), "square_{}".format(i)] for i in range(1, 7)]
    else:
        print("no value for description found")
        
def run_problem(mesh_data,
                weighting,
                radius):
    # Get mesh values
    points_filename = mesh_data[0]
    dimensional_cells = mesh_data[1]
    points_description = mesh_data[2]
    
    # Get template file
    template_filename = "template.xml"
    template_file = open(template_filename, "r")
    input_string = template_file.read()
    template_file.close()
    
    # Get input string
    input_string = input_string.replace("(WEIGHTING)", weighting)
    input_string = input_string.replace("(DIMENSIONAL_CELLS)", dimensional_cells)
    input_string = input_string.replace("(POINTS_FILE)", points_filename)
    input_string = input_string.replace("(FLUX_FILE)", get_filename("weight",
                                                                    radius,
                                                                    points_description,
                                                                    True))
    input_string = input_string.replace("(RADIUS)", str(radius))
    
    # Save input file
    input_filename = get_filename(weighting,
                                  radius,
                                  points_description)
    input_file = open(input_filename, "w")
    input_file.write(input_string)
    input_file.close()
    executable = "ibex"
    command = "{} {}".format(executable, input_filename)
    print("start {}".format(input_filename))
    subprocess.call([command], shell=True)
    print("end {}".format(input_filename))
    return

def run_all(weighting,
            radius,
            description):
    mesh_data_vals = get_mesh_data(description)
    for mesh_data in mesh_data_vals:
        run_problem(mesh_data,
                    weighting,
                    radius)
    return

def plot_all(weighting,
             radius,
             description):
    k_benchmark = 1.24379490
    mesh_data_vals = get_mesh_data(description)
    point_vals = np.zeros(len(mesh_data_vals))
    err_vals = np.zeros(len(mesh_data_vals))
    for i, mesh_data in enumerate(mesh_data_vals):
        points_description = mesh_data[2]
        filename = get_filename(weighting,
                                radius,
                                points_description,
                                True)
        try:
            data = get_data(filename)
            point_vals[i] = data["number_of_points"]
            err_vals[i] = np.abs(data["k_eigenvalue"] - k_benchmark) * 1e5
        except:
            print("{} failed".format(filename))
    plt.figure()
    plt.xlabel("number of points")
    plt.ylabel("error in pcm")
    plt.semilogy(point_vals, err_vals, basey=10)
    plt.ylim([10, 10**3])
    plt.savefig("convergence_plot_{}_{}_{}.pdf".format(description, weighting, radius), bbox_inches='tight')
    plt.close()
    return
    
def plot_together(radius):
    plt.figure(figsize=(5.5, 5.5))
    plt.xlabel("number of points")
    plt.ylabel("error in pcm")
    plt.ylim([10, 10**3])
    markers = ['D', '^', 's', 'v']
    j = 0
    for weighting in ["weight", "flux"]:
        for description in ["square", "pincell"]:
            k_benchmark = 1.24379490
            mesh_data_vals = get_mesh_data(description)
            point_vals = np.zeros(len(mesh_data_vals))
            err_vals = np.zeros(len(mesh_data_vals))
            for i, mesh_data in enumerate(mesh_data_vals):
                points_description = mesh_data[2]
                filename = get_filename(weighting,
                                        radius,
                                        points_description,
                                        True)
                try:
                    data = get_data(filename)
                    point_vals[i] = data["number_of_points"]
                    err_vals[i] = np.abs(data["k_eigenvalue"] - k_benchmark) * 1e5
                except:
                    print("{} failed".format(filename))
            if weighting == "weight":
                label = "flat, {}".format(description)
            else:
                label = "flux, {}".format(description)
            plt.semilogy(point_vals, err_vals, marker=markers[j], basey=10, label=label)
            j = j + 1
            print(weighting, description, 2 * np.log(err_vals[-4] / err_vals[-3]) / np.log(point_vals[-3] / point_vals[-4]))
            print(err_vals)
    plt.grid(True, which='major', linestyle='-', color='grey')
    plt.grid(True, which='minor', linestyle='-', color='lightgray')
    plt.minorticks_on()
    plt.legend()
    plt.savefig("convergence_plot_{}.pdf".format(radius), bbox_inches='tight')
    plt.close()
    
if __name__ == '__main__':
    radii = [3.0]
    weightings = ["weight", "flux"]
    descriptions = ["square", "pincell"]
    for radius in radii:
        # for description in descriptions:
        #     for weighting in weightings:
        #         run_all(weighting,
        #                 radius,
        #                 description)
        plot_together(radius)
