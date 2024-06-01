import pyflowy as pfy
import numpy as np
import matplotlib.pyplot as plt

asc_file = pfy.flowycpp.AscFile("topo.asc")
height_data = asc_file.height_data
x_data = asc_file.x_data
y_data = asc_file.y_data

topography = pfy.flowycpp.Topography(
    asc_file.height_data, asc_file.x_data, asc_file.y_data
)

x_data_interp = np.linspace(np.min(x_data), np.max(x_data), 500)
y_data_interp = np.linspace(np.min(y_data), np.max(y_data), 500)
height_data_interp = np.array(
    [
        [topography.height_and_slope([x, y])[0] for x in x_data_interp]
        for y in y_data_interp
    ]
)

plt.pcolormesh(x_data, y_data, topography.height_data.T)
plt.pcolormesh(x_data_interp, y_data_interp, height_data_interp.T)


x_vent = 288830
y_vent = 2150362

x1 = np.array([x_vent, y_vent])
x2 = np.array([x_data[10], y_data[10]])

dir = (x2 - x1) / np.linalg.norm(x2 - x1)
dist = np.linalg.norm(x2 - x1)

tspace = np.linspace(0, dist, 10000)
line = np.array([x1 + t * dir for t in tspace])

plt.plot(line[:, 0], line[:, 1])
plt.show()

heights = [topography.height_and_slope(p)[0] for p in line]
indices = [topography.locate_point(p) for p in line]
heights2 = [topography.height_data[i[0], i[1]] for i in indices]

slope = [topography.height_and_slope(p)[1].T @ dir for p in line]

grad = np.gradient(heights, tspace[1] - tspace[0])

plt.plot(tspace, heights, label="heights")
plt.plot(tspace, heights2, label="heights")
plt.legend()
plt.show()

plt.plot(tspace, grad, label="grad")
plt.plot(tspace, slope, label="slope")
plt.legend()
plt.show()
