from mesh_functions import *
import numpy as np

def get_points(num_radii,
               max_delta):
    # Set parameters
    r0 = 0.4096
    r1 = 0.4106
    r = 0.0
    dr0 = -0.001
    a = np.power((r - r0) / dr0, 1. / (num_radii - 1.))
    l = 1.26
    l2 = l / 2
    if a > 2:
        print("delta multiplication factor large: a = ", a)
    ind_add = int(np.ceil(l2 / max_delta))
    
    # Get points and spacing for each radius
    points_ifba = [0.4096, 0.4106]
    delta_ifba = [0.001, 0.001]
    delta_fuel = [min(max_delta, np.abs(dr0 * (np.power(a, n - 1) - np.power(a, n - 2)))) for n in range(2, num_radii + 2 + ind_add)]
    points_fuel = [r0 - delta_fuel[0]]
    for i in range(num_radii + ind_add - 1):
        point = points_fuel[-1] - delta_fuel[i + 1]
        if point >= 0:
            if point < delta_fuel[-2] / 4:
                point = 0.
            points_fuel.append(point)
    delta_fuel = delta_fuel[0:len(points_fuel)]
    delta_mod = [min(max_delta, np.abs(dr0 * (np.power(a, n - 1) - np.power(a, n - 2)))) for n in range(2, num_radii + 2 + ind_add)]
    points_mod = [r1 + delta_mod[0]]
    for i in range(num_radii + ind_add - 1):
        point = points_mod[-1] + delta_mod[i + 1]
        points_mod.append(point)
    
    # Combine sets of points
    points_r = np.concatenate((points_fuel, points_ifba, points_mod))
    delta_r = np.abs(np.concatenate((delta_fuel, delta_ifba, delta_mod)))
    indices = np.argsort(points_r)
    points_r = points_r[indices]
    delta_r = delta_r[indices]
    
    # Get full set of points
    points = []
    for i, (r, delta) in enumerate(zip(points_r, delta_r)):
        # if i == 0:
        #     points_temp = [[0., 0.]]
        # else:
        points_temp = get_ring_points(r, delta)
        for point_temp in points_temp:
            points.append(point_temp)

    # Get distance to ignore near boundary
    index = (np.abs(points_r - l2)).argmin()
    delta_l = delta_r[index]
    l_ignore = (l2 - delta_l / 2)

    # Remove those points outside boundary
    points_all = points
    points = []
    for point in points_all:
        if np.abs(point[0]) < l_ignore and np.abs(point[1]) < l_ignore:
            points.append(point)

    # Add points along boundary
    num_intervals_l = int(np.ceil(l / delta_l))
    num_points_l = num_intervals_l + 1
    delta_l = l / num_intervals_l
    for sign in [-1, 1]:
        for i in range(num_points_l):
            points.append([sign * l2, -l2 + delta_l * i])
            points.append([-l2 + delta_l * i, sign * l2])

    # Return result
    num_points = len(points)
    points = np.array(points)
    return num_points, points

def output_points(num_radii,
                  max_delta):
    # Get points and output path
    num_points, points = get_points(num_radii, max_delta)
    print("mesh has {} points".format(num_points))
    output_path = "vera1e_mesh_{}_{}.xml".format(num_radii,
                                                 max_delta)

    # Get node and add input data
    node = xml_points(2, # dimension
                      num_points,
                      points)
    et.SubElement(node, "num_radii").text = str(num_radii)
    et.SubElement(node, "max_delta").text = str(max_delta)
    
    # Output xml node
    et.ElementTree(node).write(output_path,
                               pretty_print=True,
                               xml_declaration=True)
    
    # Plot if desired
    if True:
        plt.figure()
        plt.scatter(points[:, 0], points[:, 1], s=2)
        plt.axes().set_aspect('equal')
        plt.show()
        
    
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print("vera1e_mesh.py [num_radii max_delta]")
        sys.exit()
    num_radii = int(sys.argv[1])
    max_delta = float(sys.argv[2])
    output_points(num_radii, max_delta)

