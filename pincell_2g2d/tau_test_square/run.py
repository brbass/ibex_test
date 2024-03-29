import os, sys, subprocess, itertools, multiprocessing, functools
import numpy as np
import xml.etree.ElementTree as et
import matplotlib; matplotlib.use('Agg')
from matplotlib import pyplot as plt
from ibex_io import get_data

def get_filename(tau,
                 weighting,
                 supg,
                 radius,
                 points_test_num,
                 output = False):
    filename = "ibex_{}_{}_{}_{}_{}.xml".format(tau,
                                                weighting,
                                                supg,
                                                radius,
                                                points_test_num)
    if output:
        filename = filename + ".out"
    return filename
    
def run_problem(tau,
                weighting,
                supg,
                radius,
                points_test_num):
    # Get data for points
    points_data = [["square_1.254_{}.xml".format(10*i),"{0} {0}".format(10*i - 1)] for i in range(2, 8)]
    points_data = points_data[points_test_num]
    points_filename = points_data[0]
    dimensional_cells = points_data[1]
    
    # Get template file
    template_filename = "template.xml"
    template_file = open(template_filename, "r")
    input_string = template_file.read()
    template_file.close()
    
    # Get input string
    input_string = input_string.replace("(TAU)", str(tau))
    input_string = input_string.replace("(WEIGHTING)", weighting)
    input_string = input_string.replace("(DIMENSIONAL_CELLS)", dimensional_cells)
    input_string = input_string.replace("(POINTS_FILE)", points_filename)
    input_string = input_string.replace("(SUPG)", str(supg))
    input_string = input_string.replace("(FLUX_FILE)", get_filename(tau,
                                                                    "weight",
                                                                    supg,
                                                                    radius,
                                                                    points_test_num,
                                                                    True))
    
    # Save input file
    input_filename = get_filename(tau,
                                  weighting,
                                  supg,
                                  radius,
                                  points_test_num)
    input_file = open(input_filename, "w")
    input_file.write(input_string)
    input_file.close()
    executable = "ibex"
    command = "{} {}".format(executable, input_filename)
    print("start {}".format(input_filename))
    subprocess.call([command], shell=True)
    print("end {}".format(input_filename))
    

def get_tau_commands(weighting,
                     radius,
                     points_test_num):
    tau_vals = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    supg = "true"
    input_data = []
    for tau in tau_vals:
        input_data.append([tau,
                           weighting,
                           supg,
                           radius,
                           points_test_num])
    return tau_vals, input_data
    
def run_tau_vals(weighting,
                 radius,
                 points_test_num,
                 num_procs=4):
    # Get input commands
    tau_vals, input_data = get_tau_commands(weighting,
                                            radius,
                                            points_test_num)

    # Create multiprocessing pool
    print("creating {} processes to run {} problems".format(num_procs,
                                                            len(input_data)))
    pool = multiprocessing.Pool(processes=num_procs)

    # Run problems
    pool.starmap(run_problem, input_data)

    
    
def plot_tau_vals(weighting,
                  radius,
                  points_test_num):
    tau_vals, input_data_vals = get_tau_commands(weighting,
                                                 radius,
                                                 points_test_num)
    k_benchmark = 1.24379490
    err_vals = np.zeros(len(tau_vals))
    for i, input_data in enumerate(input_data_vals):
        filename = get_filename(*input_data,
                                True)
        try:
            data = get_data(filename)
            err_vals[i] = np.abs(data["k_eigenvalue"] - k_benchmark) * 1e5
        except:
            print("{} failed".format(filename))
    plt.figure()
    plt.xlabel(r"$\tau$")
    plt.ylabel(r"error in pcm")
    plt.semilogy(tau_vals, err_vals)
    plt.savefig("tau_plot_{}_{}_{}.pdf".format(weighting, radius, points_test_num), bbox_inches='tight')
    plt.close()
    
if __name__ == '__main__':
    radius = 3.0
    num_procs = [4, 4, 3, 1, 1]
    test_nums = [0, 1, 2, 3, 4]
    weightings = ["weight", "flux"]
    # for test_num in test_nums:
    #     for weighting in weightings:
    #         run_tau_vals(weighting,
    #                      radius,
    #                      test_num,
    #                      num_procs[test_num])
    for test_num in test_nums:
        for weighting in weightings:
            plot_tau_vals(weighting,
                          radius,
                          test_num)
