import os, sys, subprocess, itertools, multiprocessing, functools
import numpy as np
import xml.etree.ElementTree as et
from matplotlib import pyplot as plt

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
    points_data = [["pincell_clad_0.4095_0.475_1.254_5_2_10.xml", "20 20"],
                   ["pincell_clad_0.4095_0.475_1.254_10_4_20.xml", "40 40"],
                   ["pincell_clad_0.4095_0.475_1.254_20_8_40.xml", "80 80"]]
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
    tau_vals = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
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
                 points_test_num):
    # Get input commands
    tau_vals, input_data = get_tau_commands(weighting,
                                            radius,
                                            points_test_num)

    # Create multi
    num_procs = 4
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
    for input_data in input_data_vals:
        filename = get_filename(*input_data,
                                True)
        
        
        
    
    
if __name__ == '__main__':
    # run_tau_vals("weight",
    #              3.0,
    #              0)
    # run_tau_vals("flux",
    #              3.0,
    #              0)
    plot_tau_vals("weight",
                  3.0,
                  0)
    plot_tau_vals("flux",
                  3.0,
                  0)
