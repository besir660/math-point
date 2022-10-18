#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 15:32:20 2022

@author: besir
"""
import numpy as np
import sys
import os
import time

sys.path.append(os.path.relpath("lib"))
from xyz import *
from point_cloud import *

camera_position = [-24,48,0]
camera_rotation = -4
focal_length = 19
color_code = [0,0,0]
boundary = 10
filename = "point.tiff"
img_size = 3000
focal_plane = 10
pan = [-2,9]

p_0 = np.array([0.1, 0., 0.])
last_p = p_0

start = time.time()
# **************** Generate World Coordinates ******************
# xyz = axis
# xyz = createSphere(10, 100)

xyz = lorenz(p_0, 10., 28., 2.667, 0.005, 50000)
# xyz = torus(5, 1, 500, 100)
# xyz = createCube_from_corners(corners,50)
# xyz = createRec_from_corners(s_corners,10)
# xyz = fast_rotate_surface(0.0001, 1, 500, 100, 'x*np.log(x)')
# xyz = surface ((-30,30), (-30,30), (500,500), '5*sin(0.5-np.sqrt(x**2 + y**2))')
print(f'{time.time() - start} seconds!')

A = 5
#xyz = surface ((-boundary,boundary), (-boundary, boundary), (1000,1000), f'{A}*sin(-np.sqrt(x**2 + y**2))/np.sqrt(x**2 + y**2)')
xyz_ = PointCloud(xyz, camera_position, camera_rotation, focal_length, 1, boundary,pan)
xyz_p = xyz_.xyz_p

save_image(xyz_p, color_code, filename, img_size,focal_plane, filter = 'SMOOTH')

