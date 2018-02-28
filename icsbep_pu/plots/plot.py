import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt
import matplotlib as mpl

def get_cuboid_points(l1, l2, l3):
    points = np.array([[-l1, -l2, -l3],
                       [l1, -l2, -l3],
                       [l1, l2, -l3],
                       [-l1, l2, -l3],
                       [-l1, -l2, l3],
                       [l1, -l2, l3],
                       [l1, l2, l3],
                       [-l1, l2, l3]])
    return points

def get_ellipsoid_points(rx, ry, rz):
    num_angles = 20
    u = np.linspace(0, 2*np.pi, num_angles)
    v = np.linspace(0, np.pi, num_angles)

    x = rx * np.outer(np.cos(u), np.sin(v))
    y = ry * np.outer(np.sin(u), np.sin(v))
    z = rz * np.outer(np.ones_like(u), np.cos(v))
    
    return x, y, z

def plot_icsbep():
    # Get points on surface of ellipsoid
    xe, ye, ze =  get_ellipsoid_points(4.3652, 5.2382, 6.5478)

    # Get cube points
    pointsc = get_cuboid_points(20.2284/2, 24.2741/2, 30.3426/2)
    # pointsc = get_cuboid_points(10.1142, 12.1371, 15.1713)
    verts = [[pointsc[0],pointsc[1],pointsc[2],pointsc[3]],
             [pointsc[4],pointsc[5],pointsc[6],pointsc[7]], 
             [pointsc[0],pointsc[1],pointsc[5],pointsc[4]], 
             [pointsc[2],pointsc[3],pointsc[7],pointsc[6]], 
             [pointsc[1],pointsc[2],pointsc[6],pointsc[5]],
             [pointsc[4],pointsc[7],pointsc[3],pointsc[0]], 
             [pointsc[2],pointsc[3],pointsc[7],pointsc[6]]]
    
    # Set preliminary data
    colors = ['#1b9e77','#d95f02','#7570b3']
    labels = ['Pu', 'Th']

    # Create axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect('equal')
    
    # Plot ellipsoid
    ax.plot_surface(xe, ye, ze,
                    linewidth=0.5,
                    edgecolors=colors[0],
                    #color=colors[0],
                    cmap=plt.get_cmap('winter'),
                    #cmap=plt.get_cmap('Greens'),
                    alpha=0.3)
    fakeline = mpl.lines.Line2D([0],[0],linestyle="none", c=colors[0], marker='o', markersize=4.7)
    
    # Plot cuboid
    cuboid = ax.scatter3D(pointsc[:, 0], pointsc[:, 1], pointsc[:, 2],
                          color=colors[1],
                          label=labels[1])
    collection = Poly3DCollection(verts, 
                                  linewidths=1,
                                  edgecolors=colors[1],
                                  alpha=.1)
    collection.set_facecolor(colors[1])
    ax.add_collection3d(collection)

    # Save plot
    ax.view_init(elev=20, azim=-70)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.legend([fakeline, cuboid], [labels[0], labels[1]], numpoints=1, loc=[0.7, 0.81])
    plt.savefig("icsbep_pu_th.pdf",
                bbox_inches='tight')
    plt.show()
    plt.close()
    
if __name__ == '__main__':
    plot_icsbep()
