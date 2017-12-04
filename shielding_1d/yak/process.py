import sys
import numpy as np
import xml.etree.ElementTree as et
from matplotlib import pyplot as plt

def plot_phi_dfem(output_filename):
    node = et.parse(output_filename).getroot()
    num_cells = int(node.findtext("finite_element_mesh/number_of_elements"))
    num_nodes = int(node.findtext("finite_element_mesh/number_of_nodes"))
    num_groups = int(node.findtext("energy_discretization/number_of_groups"))
    num_moments = int(node.findtext("gauss_legendre_ordinates/number_of_moments"))

    phi_data = np.fromstring(node.findtext("solution/phi"), dtype=float, sep="\t")

    dx = 4./num_cells
    points = np.zeros(num_nodes * num_cells)
    for i in range(num_cells):
        points[num_nodes * i] = i * dx
        points[1 + num_nodes * i] = (i + 1) * dx

    phi = np.zeros((num_cells * num_nodes, num_moments, num_groups))
    for i in range(num_cells):
        for m in range(num_moments):
            for g in range(num_groups):
                for n in range(num_nodes):
                    k = n + num_nodes * (g + num_groups * (m + num_moments * i))
                    phi[n + num_nodes * i, m, g] = phi_data[k]
                    
    plt.figure()
    for g in range(num_groups):
        plt.plot(points, phi[:, 0, g], label=g)
    plt.xlabel(r"$x$")
    plt.ylabel(r"$\phi$")
    plt.legend()
    plt.show()

def output_phi_integral(output_filename):
    node = et.parse(output_filename).getroot()
    num_cells = int(node.findtext("finite_element_mesh/number_of_elements"))
    num_nodes = int(node.findtext("finite_element_mesh/number_of_nodes"))
    num_groups = int(node.findtext("energy_discretization/number_of_groups"))
    num_moments = int(node.findtext("gauss_legendre_ordinates/number_of_moments"))

    phi_data = np.fromstring(node.findtext("solution/phi"), dtype=float, sep="\t")
    
    phi = np.zeros((num_cells, num_nodes, num_moments, num_groups))
    for i in range(num_cells):
        for m in range(num_moments):
            for g in range(num_groups):
                for n in range(num_nodes):
                    k = n + num_nodes * (g + num_groups * (m + num_moments * i))
                    phi[i, n, m, g] = phi_data[k]
    
    phi_average = np.zeros((num_cells, num_groups))
    for i in range(num_cells):
        for g in range(num_groups):
            phi_average[i, g] = np.mean(phi[i, :, 0, g])
    np.savetxt("phi_average.txt", phi_average, delimiter="\t")
    
if __name__ == '__main__':
    #plot_phi_dfem("dfem_benchmark.xml.out")
    output_phi_integral("dfem_benchmark.xml.out")
