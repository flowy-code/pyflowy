import flowpy as fpy
import numpy as np
import matplotlib.pyplot as plt


def create_topography(
    height_cb, filename, xdim=10000, ydim=10000, res=10, lower_left_corner=[0, 0]
):

    # First we create a topograhy with constant slope
    x_data = np.arange(lower_left_corner[0], xdim + lower_left_corner[0], res)
    y_data = np.arange(lower_left_corner[1], ydim + lower_left_corner[1], res)

    height_data = np.array([[height_cb(x, y) for y in y_data] for x in x_data])

    asc_file = fpy.flowpycpp.AscFile()
    asc_file.x_data = x_data
    asc_file.y_data = y_data
    asc_file.data = height_data

    asc_file.save(filename)


def height_const_slope(x, y):
    return 5e-2 * x


create_topography(height_const_slope, filename="constant_slope")


def height_parabola(x, y):
    return -1e-4 * (x - 5000) * (y - 5000)


create_topography(height_parabola, filename="parabola")


def height_flat(x, y):
    return 0.0


create_topography(height_flat, filename="flat")
