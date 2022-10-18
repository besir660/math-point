import open3d as o3d
import numpy as np



from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import sys
import os

sys.path.append(os.path.relpath("lib"))
from xyz import *

omega = 0.1 # radians per sec
A = 5 #amplitude
points = surface ((-100,100), (-100,100), (500,500), f'{A}*sin(np.sqrt(x**2 + y**2))/np.sqrt(x**2 + y**2)')    
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

vis = o3d.visualization.Visualizer()
vis.create_window()
vis.add_geometry(pcd)

for t in range(0,7200):
    #points = fast_rotate_surface(0.1,50, 1000, 1000, f'{A}*sin({omega}*{t}-x)/x')
    points = surface ((-30,30), (-30,30), (1000,1000), f'{A}*sin(-{omega}*{t}+np.sqrt(x**2 + y**2))/np.sqrt(x**2 + y**2)')
    pcd.points = o3d.utility.Vector3dVector(points)
    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()
vis.destroy_window()
