from mesh_functions import *
import numpy as np

def get_points(num_radii,
               max_delta,
               initial_delta):
    # Set parameters
    initial_delta = np.abs(initial_delta)
    r0 = 0.4101 - initial_delta / 2
    r1 = 0.4101 + initial_delta / 2
    r = 0.0
    dr0 = -initial_delta
    a = np.power((r - r0) / dr0, 1. / (num_radii - 1.))
    l = 1.26
    l2 = l / 2
    if a > 2:
        print("delta multiplication factor large: a = ", a)
    ind_add = int(np.ceil(l2 / max_delta))
    
    # Get points and spacing for each radius
    points_ifba = [r0, r1]
    delta_ifba = [initial_delta, initial_delta]
    delta_fuel = [min(max_delta, initial_delta * np.power(a, n + 1)) for n in range(0, num_radii + ind_add)]
    points_fuel = [r0 - delta_fuel[0]]
    for i in range(num_radii + ind_add - 1):
        point = points_fuel[-1] - delta_fuel[i + 1]
        if point >= 0:
            if point < delta_fuel[-2] / 4:
                point = 0.
            points_fuel.append(point)
    delta_fuel = delta_fuel[0:len(points_fuel)]
    delta_mod = [min(max_delta, initial_delta * np.power(a, n + 1)) for n in range(0, num_radii + ind_add)]
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
    spacing_r = [delta_r[0]]
    for i in range(1, len(points_r) - 1):
        spacing_r.append((delta_r[i + 1] + delta_r[i - 1]) / 2)
    spacing_r.append(delta_r[-1])

    # Get full set of points
    points = []
    for i, (r, spacing) in enumerate(zip(points_r, spacing_r)):
        points_temp = get_ring_points(r, spacing)
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
            pos = -l2 + delta_l * i
            points.append([pos, sign * l2])
        for i in range(1, num_points_l - 1):
            pos = -l2 + delta_l * i
            points.append([sign * l2, pos])
            
    # Return result
    num_points = len(points)
    points = np.array(points)
    return num_points, points

def output_points(num_radii,
                  max_delta,
                  initial_delta):
    # Get points and output path
    num_points, points = get_points(num_radii, max_delta, initial_delta)
    print("mesh has {} points".format(num_points))
    output_path = "vera1e_mesh_{}_{}_{}.xml".format(num_radii,
                                                    max_delta,
                                                    initial_delta)

    # Get node and add input data
    node = xml_points(2, # dimension
                      num_points,
                      points)
    et.SubElement(node, "num_radii").text = str(num_radii)
    et.SubElement(node, "max_delta").text = str(max_delta)
    et.SubElement(node, "initial_delta").text = str(initial_delta)
    
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
    if (len(sys.argv) != 4):
        print("vera1e_mesh.py [num_radii max_delta initial_delta]")
        sys.exit()
    num_radii = int(sys.argv[1])
    max_delta = float(sys.argv[2])
    initial_delta = float(sys.argv[3])
    output_points(num_radii, max_delta, initial_delta)

