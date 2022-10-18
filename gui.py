import tkinter as tk
from tkinter.messagebox import showinfo
# importing the choosecolor package
from tkinter import colorchooser
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import sys
import os

sys.path.append(os.path.abspath("lib"))
from xyz import *
from point_cloud import *


def update_world(a):
    global xyz
    global xyz_
    global focal_length
    global plot_limit
    global focal

    camera_position = np.array([w1.get(), w2.get(), w3.get()])  # camera is assumed to be pointing towards the origin
    camera_rotation = w4.get()
    focal_length = w5.get()
    p = perspective_check.get()
    pan_x = w_pan_x.get()
    pan_y = w_pan_y.get()

    del xyz_

    xyz_ = PointCloud(xyz, camera_position, camera_rotation, focal_length, 1, focal, (pan_x, pan_y))

    fig.clear()
    canvas.draw_idle()
    
    xs = xyz_.xyz_p[:, 0]
    ys = xyz_.xyz_p[:, 1]

    fig.clear()
    plt3 = fig.add_subplot(111)
    plt3.scatter(xs, ys, s=0.01)
    plt3.set_xlim([-plot_limit, plot_limit])
    plt3.set_ylim([-plot_limit, plot_limit])
    canvas.draw_idle()


def choose_color():
    global color_code
    # variable to store hexadecimal code of color
    color_code = colorchooser.askcolor(title="Choose color")[0]


def save_img():
    global xyz_
    global color_code
    global focal
    save_image(xyz_.xyz_p,color_code,"gui.tiff",w_imgsize.get(),focal)
 

camera_position = [0,50,50]
camera_rotation = 0
focal_length = 235
focal = 100
color_code = [0,0,0]
canvas = 10
plot_limit = canvas
slider_limit = 2000

# **************** Generate World Coordinates ******************
xyz = lorenz([-1.0, 0., 0.], 10., 28., 2.667, 0.005, 500000)
#xyz = [[0,0,0]]
A = 10
#xyz = surface ((-canvas,canvas), (-canvas, canvas), (100,100), f'{A}*sin(-np.sqrt(x**2 + y**2))/np.sqrt(x**2 + y**2)')

xyz_ = PointCloud(xyz, camera_position, camera_rotation, focal_length, 1, focal)


# ******************** GUI ***************************************************************
    
window = tk.Tk()
window.title('Camera Projection')
window.geometry('1500x1200')
window.columnconfigure([0, 4], minsize=250)
window.rowconfigure([0, 6], minsize=100)

perspective_check = tk.IntVar(value=1)

frame1 = tk.Frame(master=window, width=200, height=200, relief=tk.RAISED)
frame1.pack()
frame2 = tk.Frame(master=window, width=200, height=400, )
frame2.pack()

funcs = ('5*sin(-np.sqrt(x**2 + y**2))/np.sqrt(x**2 + y**2)', 'x**2 + y**2')


function = tk.StringVar(value=funcs)

fig = plt.figure(figsize=(8, 8))
canvas = FigureCanvasTkAgg(fig, master=frame2)
canvas.draw()
canvas.get_tk_widget().grid(row=5, column=0, ipadx=40, ipady=20)
toolbar = NavigationToolbar2Tk(canvas, window)
toolbar.update()
canvas.get_tk_widget().grid(row=6, column=0, ipadx=40, ipady=20)
# **** WIDGETS ************

w1 = tk.Scale(master=frame1, from_=-slider_limit, to=slider_limit, command=update_world, label='camera x',
              orient=tk.HORIZONTAL, length=200)
w1.grid(row=0, column=0)
w1.set(camera_position[0])
# ***********
w2 = tk.Scale(master=frame1, from_=-slider_limit, to=slider_limit, command=update_world, label='camera y',
              orient=tk.HORIZONTAL, length=200)
w2.grid(row=0, column=1)
w2.set(camera_position[1])
# ***********
w3 = tk.Scale(master=frame1, from_=-slider_limit, to=slider_limit, command=update_world, label='camera z',
              orient=tk.HORIZONTAL, length=200)
w3.set(camera_position[2])
w3.grid(row=0, column=2)
# **********
w4 = tk.Scale(master=frame1, from_=-180, to=180, command=update_world, label='camera rotation',
              orient=tk.HORIZONTAL, length=200)
w4.grid(row=1, column=0)
w4.set(camera_rotation)
# **********
w5 = tk.Scale(master=frame1, from_=1, to=500, command=update_world, label='focal length',
              orient=tk.HORIZONTAL, length=200)
w5.set(focal_length)
w5.grid(row=1, column=1, pady=20)
# **********
w_pan_x = tk.Scale(master=frame1, from_=-500, to=500, command=update_world, label='Pan (X)',
              orient=tk.HORIZONTAL, length=200)
w_pan_x.set(0)
w_pan_x.grid(row=2, column=1, pady=20)
# **********
w_pan_y = tk.Scale(master=frame1, from_=500, to=-500, command=update_world, label='Pan (Y)',
              orient=tk.VERTICAL, length=200)
w_pan_y.set(0)
w_pan_y.grid(row=2, column=2, pady=20)
# **********
w_perspective = tk.Checkbutton(master=frame1, variable=perspective_check, text="perspective")
w_perspective.grid(row=1, column=6, sticky=tk.W, padx=20)
# **********
w_imgsize = tk.Scale(master=frame1, from_=100, to=5000, label='image size',
                     orient=tk.HORIZONTAL, length=200)
w_imgsize.grid(row=2, column=4)
w_imgsize.set(2000)
# ************
w_save = tk.Button(master=frame1, command=save_img, text="Save Image")
w_save.grid(row=2, column=5, sticky=tk.W, padx=20)
# ************
w_color = tk.Button(master=frame1, text="Select color", command=choose_color)
w_color.grid(row=3, column=5, sticky=tk.W, padx=20)
# ***************************************************************************************
window.mainloop()
# **************************** GUI END **************************************************
