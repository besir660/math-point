#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 22:52:26 2021

@author: besir
"""
import numpy as np
from tqdm import tqdm
from PIL import Image
from PIL import ImageFilter
from pyquaternion import Quaternion

pi = np.pi
sin = np.sin
cos = np.cos


def Rotate_Q(xyz_, x_angle, y_angle, z_angle):
    # ******************* ROTATION using a QUATERNION ***********************

    # calculate the rotation quaternion from the Euler angles.
    # this method is slower than matrix rotation in case of vector rotation
    # however we do this in the interest of learning/understanding quaternions
    #
    # The points in space should provided as a n x 3 matrix of coordinates,
    # it would be easier if they wer provided as and 3 x n matrix of column vectors,
    # this would eliminate the need to transpose the xyz matrix - note for improvement
    #
    # we need to handle the special case where only a single vector is received,
    # this probably could also be improved by better use of numpy array properties
    # - note for future improvement as well

    # ******************* ROTATION using QUATERNION ***********************

    if np.shape(xyz_) == (3,):
        count = 1
    else:
        count = np.shape(xyz_)[0]

    q_z = Quaternion(np.cos(z_angle / 2), 0, 0, np.sin(z_angle / 2))
    q_y = Quaternion(np.cos(y_angle / 2), 0, np.sin(y_angle / 2), 0)
    q_x = Quaternion(np.cos(x_angle / 2), np.sin(x_angle / 2), 0, 0)
    q_r = (q_x * q_y * q_z).normalised

    if count == 1:
        wxyz = np.insert(xyz_, 0, 0)
        r_ = np.zeros(3)
    else:
        wxyz = np.c_[np.zeros(count), xyz_]
        r_ = np.zeros((count, 3))

    for i in tqdm(range(0, count)):
        if count == 1:
            v = Quaternion(wxyz)
            v_r = q_r * v * q_r.conjugate
            r_ = v_r.imaginary
        else:
            v = Quaternion(wxyz[i])
            v_r = q_r * v * q_r.conjugate
            r_[i] = v_r.imaginary

    return r_



def frange(start, stop, step):
    i = start
    while i <= stop:
        yield i
        i += step
        

def sphere(c, r, N):
    lst = []
    thetas = [(2 * pi * i) / N for i in range(N)]
    phis = [(pi * i) / N for i in range(N)]
    for theta in thetas:
        for phi in phis:
            x = c[0] + r * sin(phi) * cos(theta)
            y = c[1] + r * sin(phi) * sin(theta)
            z = c[2] + r * cos(phi)
            lst.append((x, y, z))
    return lst


def createCube(step):
    xyz_ = np.array([[0.0, 0.0, 0.0]])
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in frange(k, 1, step):
                    xyz_ = np.append(xyz_, [[i, j, l]], axis=0)
                for l in frange(j, 1, step):
                    xyz_ = np.append(xyz_, [[i, l, k]], axis=0)
                for l in frange(i, 1, step):
                    xyz_ = np.append(xyz_, [[l, j, k]], axis=0)
    return xyz_


def lorenz(p0, s, r, b, dt, nums):
    lxyz = np.zeros((nums+1, 3), dtype=np.float64)
    lxyz[0] = p0
    x_dot = 0
    y_dot = 0
    z_dot = 0
    for i in range(nums):
        x = lxyz[i][0]
        y = lxyz[i][1]
        z = lxyz[i][2]
        x_dot = s * (y - x)
        y_dot = r * x - y - x * z
        z_dot = x * y - b * z
        lxyz[i + 1] = [x + x_dot * dt, y + y_dot * dt, z + z_dot * dt]
    if nums  == 1:
        return lxyz[1].reshape(1,3)
    else:
        return lxyz


def torus(R, r, Rstep, rstep):
    xyz_ = np.array([0, 0, 0])
    d_phi = (2 * np.pi) / Rstep
    d_theta = (2 * np.pi) / rstep
    for phi in tqdm(frange(0, 2 * np.pi, d_phi)):
        for theta in frange(0, 2 * np.pi, d_theta):
            x = (R + r * np.cos(theta)) * np.cos(phi)
            y = (R + r * np.cos(theta)) * np.sin(phi)
            z = r * np.sin(theta)
            xyz_ = np.vstack((xyz_, [x, y, z]))
    return xyz_


def fast_rotate_surface(x1, x2, xstep, theta_step, eq_str):
    d_x = (x2-x1) / xstep
    d_theta = (2 * pi) / theta_step
    x_range = np.arange(x1,x2,d_x).reshape(xstep,1)
    theta_range = np.arange(0,2*pi,d_theta).reshape(1,theta_step)
    x_theta_range = cos(theta_range)
    y_theta_range = sin(theta_range)
    x_ = (x_range * x_theta_range).flatten(order = 'F')
    y_ = (x_range * y_theta_range).flatten(order = 'F')
    
    f = eval("lambda x: " + eq_str)
    x_z_range = f(x_range)
    z_ = np.tile(x_z_range, theta_step).flatten(order = 'F')
    
    xyz_ = np.stack((x_,y_,z_), axis = 1)
    return xyz_


def surface(x, y, step, eq_str):
    dx = (x[1] - x[0])/step[0] 
    dy = (y[1] - y[0])/step[1] 
    x_range = np.arange(x[0],x[1],dx)
    y_range = np.arange(y[0],y[1],dy)
    x_column = np.repeat(x_range,step[1])
    y_column = np.tile(y_range,step[0])
    f = eval("lambda x,y: " + eq_str)
    z_column = f(x_column, y_column)
    xyz_ = np.stack((x_column, y_column , z_column), axis = 1)
    return xyz_


def pixel(c2d, img_size, c_arr, focal, crop = 1, padding = 0):
    """
    converts 2d coordinates to pixel coordinates\n
    origin of world coordinates is placed in the image center and x,y coordinates are shifted and flipped and x coordinate reversed\n

    Parameters
    ----------
    c2d : projected 2d coordinates on the foacl plane\n
    img_size : image cnvas size\n
    padding : padding\n
    c_arr : RGB color array nx3\n
    focal : focal plane width/2\n

    Returns
    -------
    pixels : nx5 array of pixel coordinates and RGB values

    """
    
    one = np.ones((len(c2d), 1))
    scale = img_size / (2*focal)
    c2d *= scale
    c2d = np.concatenate((c2d, c_arr), axis=1)
    half = int(img_size/2) - 1
    origin = [half,half]
    #crop coordinates outside the image area
    c2d = np.delete(c2d, np.where(c2d[:,[0,1]] > half)[0], axis=0)
    c2d = np.delete(c2d, np.where(c2d[:,[0,1]] < -half)[0], axis=0)
    #convert world coordinates to pixel coordinates
    pixels = c2d
    pixels[:,[0,1]] = pixels[:,[0,1]] + origin
    pixels[:,[0,1]] = np.flip(pixels[:,[0,1]], axis = 1)*[-1,1]
    pixels = pixels.astype(int)
    #remove duplicate pixels
    pixels = np.unique(pixels, axis=0)

    return pixels


def save_image(xy_,color_code, filename, img_size, focal=30, bg_color = (255, 255, 255), filter =''):
    rgb = np.eye(3, 3) * color_code
    shape = np.shape(xy_)
    color_arr = np.ones(shape[0] * 3).reshape(3, shape[0])
    color_arr = np.matmul(rgb, color_arr).transpose()
    pixels = pixel(xy_, img_size, color_arr,focal)
    img = Image.new('RGB', (img_size, img_size), color=bg_color)
    imgarr = np.array(img)
    imgarr.setflags(write=1)
    imgarr[pixels[:,0],pixels[:,1]] = pixels[:, [2, 3, 4]]
    output = Image.fromarray(imgarr)
    if filter != '':
        output = eval(f"output.filter(ImageFilter.{filter})")
    output.save(filename)
