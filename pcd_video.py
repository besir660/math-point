#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 18:49:19 2022

@author: besir
"""
import cv2
import numpy as np
import glob

img_array = []
for i in range(1,len(glob.glob('animation/img/*.tiff'))):
    filename = f'animation/img/pcd_{i}.tiff'
    print(filename)
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)


out = cv2.VideoWriter('animation/project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 50, size)
 
for i in range(len(img_array)):
    print(i)
    out.write(img_array[i])
out.release()
cv2.destroyAllWindows()