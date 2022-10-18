import open3d as o3d
import numpy as np



from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import sys
import os

sys.path.append(os.path.abspath("/Users/besir/math/point-cloud/lib/"))
from xyz import *

def custom_draw_geometry(pcd):
    # The following code achieves the same effect as:
    # o3d.visualization.draw_geometries([pcd])
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.run()
    vis.destroy_window()
    

A = 5 #amplitude
canvas = 100

points = surface ((-canvas,canvas), (-canvas, canvas), (1000,1000), f'{A}*sin(-np.sqrt(x**2 + y**2))/np.sqrt(x**2 + y**2)')


# point_cloud = lp.read("./2020_Drone_M.las")

# points = np.vstack((point_cloud.x,point_cloud.y,point_cloud.z)).transpose()
# p = points[::5]

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

# vis = o3d.visualization.Visualizer()
# vis.create_window()
# vis.add_geometry(pcd)

# o3d.io.write_point_cloud("./lorenz.ply", pcd)
# pcd_load = o3d.io.read_point_cloud("./lorenz.ply")

o3d.visualization.draw_geometries([pcd]) 
# custom_draw_geometry(pcd)
# custom_draw_geometry(pcd2)