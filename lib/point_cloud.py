#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 11:51:09 2021

@author: besir
"""

import numpy as np


class PointCloud:
    """
    Receives point cloud and camera data and produces a camera view of the world which is stored in xyz_p \n
    Keyword Arguments
    xyz -- nx3 matrix of world coordinates\n
    camera position -- coordinates of the camera\n
    camera rotation -- rotation of camera around the axis pointing from camera position to origin\n
    focal length -- focal length of camera lens\n
    perspective -- 0 means no perspective, i.e. projected x y coordinates not scaled by distance (default 1)\n
    screen -- dimension of focal plane, single dimension so plane is calculated as a square of 2 * screen size (default 20)\n
    """
    
    def __init__(self, xyz, camera_position, camera_rotation, focal_length, perspective=1, boundary = 20, pan_v = [0,0]):
        self.xyz = xyz
        self.camera_position = np.array(camera_position)
        self.camera_rotation = np.array(camera_rotation)
        self.focal_length = focal_length
        self.perspective = perspective
        self.boundary = boundary
        self.pan_v = pan_v
        self.rotation_axis = [-self.camera_position[1], self.camera_position[0], 0] # set rotation axis orthogonal to camera vector
        self.rotation_axis = self.rotation_axis / np.linalg.norm(self.rotation_axis) # normalize rotation axis
        self.z_angle = - np.arccos(self.camera_position[2] / np.linalg.norm(self.camera_position)) # camera position in rotated world, moves camera to the z_axis
        self.camera_r = self.rotate(camera_position, self.rotation_axis, self.z_angle).flatten()
        self.xyz_r = self.rotate(self.rotate(self.xyz, self.rotation_axis, self.z_angle), [0, 0, 1], #first rotate the world so that camera aligns to z-axis, and then rotate by camera rotation
                                 np.radians(self.camera_rotation))
        self.xyz_p = self.project(self.translate3D(self.xyz_r, self.camera_r), self.focal_length)
        self.xyz_p = self.translate2D(self.xyz_p, pan_v)
        self.crop()

    def rotate(self, xyz, rotation_axis, angle): #using matrix form of rodriques formula
        xyz = np.array(xyz)
        rotation_axis = np.array(rotation_axis)
        if angle != 0:
            if np.shape(xyz) == (3,):
                xyz = xyz.reshape(1, 3)
            x, y, z = rotation_axis[0], rotation_axis[1], rotation_axis[2]
            K = np.array([[0, -z, y],
                          [z, 0, -x],
                          [-y, x, 0]])
            R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * np.matmul(K, K)
            result = np.matmul(R, xyz.transpose()).transpose()
            return result
        else:
            return xyz

    def translate3D(self, xyz_, trans_vec):
        if np.shape(xyz_) == (3,):
            xyz_ = xyz_.reshape(1, 3)

        arr_size = np.shape(xyz_)[0]
        # translation matrix T
        T = [[1, 0, 0, trans_vec[0]],
             [0, 1, 0, trans_vec[1]],
             [0, 0, 1, trans_vec[2]],
             [0, 0, 0, 1]]

        xyzw = np.c_[xyz_, np.ones(arr_size)]  # add a column of 1's to xyz so we can multiply with translation matrix

        r_ = np.dot(T, xyzw.transpose()).transpose()[:, :3]

        return r_
    
    def translate2D(self, xy_, trans_vec):
        arr_size = np.shape(xy_)[0]
        # translation matrix T
        # translation matrix T
        T = [[1, 0, trans_vec[0]],
             [0, 1, trans_vec[1]],
             [0, 0, 1]]

        xyw = np.c_[xy_, np.ones(arr_size)]  # add a column of 1's to xyz so we can multiply with translation matrix

        r_ = np.dot(T, xyw.transpose()).transpose()[:, :2]

        return r_


    def project(self, xyz, f):
        if self.perspective:
            xy = xyz[:, :2] / xyz[:, 2:3] * f
            return xy
        else:
            xy = xyz[:, :2] * f
            return xy


    def crop(self):
            self.xyz_p = np.delete(self.xyz_p, np.where(self.xyz_p >= self.boundary)[0], axis=0)
            self.xyz_p = np.delete(self.xyz_p, np.where(self.xyz_p <= -self.boundary)[0], axis=0)