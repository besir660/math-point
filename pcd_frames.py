#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 12:32:16 2022

@author: besir
"""
import numpy as np
import sys
import os
import time

sys.path.append(os.path.relpath("lib"))
from xyz import *
from point_cloud import *

# camera_position = [0,143,125]
# camera_rotation = 0
# focal_length = 277
# canvas = 50
# focal = 30
# color_code = [100,100,100]
# img_size = 2000

camera_position = [-48,167,50]
camera_rotation = 35
focal_length = 200
color_code = [0,0,0]
boundary = 100
filename = "point.tiff"
img_size = 300
focal_plane = 36
pan = [-20,20]
frames = 500



# omega = 0.1 # radians per sec
# A = 8 #amplitude    
# for t in range(0,50):
#     #points = fast_rotate_surface(0.1,50, 1000, 1000, f'{A}*sin({omega}*{t}-x)/x')
#     points = surface ((-canvas,canvas), (-canvas, canvas), (1000,1000), f'{A}*sin({omega}*{t}-np.sqrt(x**2 + y**2))/np.sqrt(x**2 + y**2)')
#     pcd = PointCloud(points, camera_position, camera_rotation, focal_length,1, focal)
#     save_image(pcd.xyz_p,color_code,"./animation/img/pcd_{}.tiff".format(str(t)),img_size, focal)

p_0 = np.array([[1.0, 0., 0.]])
start = time.time()

points = p_0
for t in range(1,frames):
    p_0 = lorenz(p_0, 10., 28., 2.667, 0.005, 1)
    #points = np.stack([points, p_0], axis = 0)
    points = np.concatenate((points, p_0), axis = 0)
    pcd = PointCloud(points, camera_position, camera_rotation, focal_length, 1, boundary,pan)
    #save_image(pcd.xyz_p,color_code,"./animation/img/pcd_{}.tiff".format(str(t)),img_size, focal_plane, filter = 'GaussianBlur(radius=1)')
    save_image(pcd.xyz_p,color_code,"./animation/img/pcd_{}.tiff".format(str(t)),img_size, focal_plane)




# for t in range(1,10000):
#     points = lorenz(p_0, 10., 28., 2.667, 0.005, t)
#     pcd = PointCloud(points, camera_position, camera_rotation, focal_length, 1, boundary,pan)
#     #save_image(pcd.xyz_p,color_code,"./animation/img/pcd_{}.tiff".format(str(t)),img_size, focal_plane, filter = 'GaussianBlur(radius=1)')
#     save_image(pcd.xyz_p,color_code,"./animation/img/pcd_{}.tiff".format(str(t)),img_size, focal_plane)
    
print(f'{time.time()-start} seconds!')