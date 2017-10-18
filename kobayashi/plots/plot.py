import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt

def get_cube_points(l):
    return np.array([[0., 0., 0.],
                     [l, 0., 0.],
                     [l, l, 0.],
                     [0., l, 0.],
                     [0., 0., l],
                     [l, 0., l],
                     [l, l, l],
                     [0., l, l]])

def plot_p1():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colors = ['#1b9e77','#d95f02','#7570b3']
    labels = ["Reg. 1 (Source)", "Reg. 2 (Void)", "Reg. 3"]
    for i, length in enumerate([10., 50., 100.]):
        # Plot points
        points = get_cube_points(length)
        ax.scatter3D(points[:, 0], points[:, 1], points[:, 2],
                     color=colors[i],
                     label=labels[i])
        
        # Plot sides
        verts = [[points[0],points[1],points[2],points[3]],
                 [points[4],points[5],points[6],points[7]], 
                 [points[0],points[1],points[5],points[4]], 
                 [points[2],points[3],points[7],points[6]], 
                 [points[1],points[2],points[6],points[5]],
                 [points[4],points[7],points[3],points[0]], 
                 [points[2],points[3],points[7],points[6]]]
        collection = Poly3DCollection(verts, 
                                      linewidths=1,
                                      edgecolors=colors[i],
                                      alpha=.1)
        #collection.set_label(length)
        collection.set_facecolor(colors[i])
        ax.add_collection3d(collection)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.legend()
    plt.savefig("kobayashi_p1_problem.pdf",
                bbox_inches='tight')
    # plt.show()
    plt.close()
    
if __name__ == '__main__':
    plot_p1()
