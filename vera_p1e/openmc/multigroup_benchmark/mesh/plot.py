import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl

def plot_tally():
    # Setup mesh
    dimension = 2
    num_cells_d = 100
    num_points_d = num_cells_d + 1
    num_cells = num_cells_d**2
    num_points = num_points_d**2
    length = 1.26
    points_d = np.linspace(-length/2, length/2, num=num_points_d, endpoint=True)

    # Get all points on cell edges
    points = np.empty((num_points, dimension))
    for i, x in enumerate(points_d):
        for j, y in enumerate(points_d):
            k = i + num_points_d * j
            points[k] = [x, y]

    # Get two triangles for each Cartesian cell
    num_triangles_per_cell = 2
    num_triangles = num_triangles_per_cell * num_cells
    triangles = np.empty((num_triangles, 3))
    for i in range(num_cells_d):
        for j in range(num_cells_d):
            k = i + num_cells_d * j
            ul = i + num_points_d * j
            ur = ul + 1
            ll = i + num_points_d * (j + 1)
            lr = ll + 1
            triangles[num_triangles_per_cell * k] = [ul, ll, lr]
            triangles[1 + num_triangles_per_cell * k] = [ul, lr, ur]
    tri = mpl.tri.Triangulation(points[:, 0], points[:, 1], triangles=triangles)
    
    # Get mesh tally in appropriate form
    num_groups = 2
    tally = np.loadtxt("mesh_tally.txt")#[:, [1, 0]]
    phi = np.empty((num_triangles, num_groups))
    for i in range(num_cells):
        for j in range(num_triangles_per_cell):
            k = j + num_triangles_per_cell * i
            phi[k, :] = tally[i, :]
    
    for g in range(num_groups):
        plt.figure()
        #plot.set_edgecolor('face')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("group " + str(g))
        plt.axis('equal')
        plot = plt.tripcolor(tri, phi[:, g],
                             shading='flat',
                             linewidth=0,
                             edgecolors='none',
                             rasterized=True,
                             linestyle='None')
        plt.colorbar(label=r"$|\phi(x, y)|$")
        plt.tight_layout()
        plt.savefig("openmc_verap1e_{}.pdf".format(g),
                    bbox_inches='tight',
                    dpi=1200)
        plt.close()
    #plt.show()

if __name__ == '__main__':
    plot_tally()
