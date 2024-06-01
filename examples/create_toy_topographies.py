import pyflowy as pfy
import numpy as np
import matplotlib.pyplot as plt

# First we create a topograhy with constant sloe
x_data = np.linspace(0, 10000, 1000)
y_data = np.linspace(0, 10000, 1000)


def height(x, y):
    return 5e-2 * x


height_data = np.array([[height(x, y) for y in y_data] for x in x_data])

asc_file = pfy.flowycpp.AscFile()
asc_file.x_data = x_data
asc_file.y_data = y_data
asc_file.height_data = height_data
asc_file.cell_size = x_data[1] - x_data[0]
asc_file.save("constant_slope.asc")


# Then we create a saddle topography
x_data = np.linspace(0, 10000, 1000)
y_data = np.linspace(0, 10000, 1000)


def height(x, y, center):
    return -1e-4 * (x - center[0]) * (y - center[1])


center = np.array([np.mean(x_data), np.mean(y_data)])
height_data = np.array([[height(x, y, center) for y in y_data] for x in x_data])

asc_file = pfy.flowycpp.AscFile()
asc_file.x_data = x_data
asc_file.y_data = y_data
asc_file.height_data = height_data
asc_file.cell_size = x_data[1] - x_data[0]
asc_file.save("saddle.asc")

# Then we create a flat topography
x_data = np.linspace(0, 50000, 5000)
y_data = np.linspace(0, 50000, 5000)


def height(x, y, center):
    return 0.0


center = np.array([np.mean(x_data), np.mean(y_data)])
height_data = np.array([[height(x, y, center) for y in y_data] for x in x_data])

asc_file = pfy.flowycpp.AscFile()
asc_file.x_data = x_data
asc_file.y_data = y_data
asc_file.height_data = height_data
asc_file.cell_size = x_data[1] - x_data[0]
asc_file.save("flat.asc")
