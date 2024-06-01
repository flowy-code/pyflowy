import pyflowy as pfy
import numpy as np
import matplotlib.pyplot as plt


def add_lobe(lobe, topography, new_height_data):
    intersection_data = topography.compute_intersection(lobe, None)

    for indices, fraction in intersection_data:
        # print("indices={},{}; frac={}\n".format(indices[0], indices[1], fraction))
        new_height_data[indices[0], indices[1]] += fraction * lobe.thickness


lobe = pfy.flowycpp.Lobe()
lobe.semi_axes = [8, 2]
lobe.thickness = 20.0
lobe.set_azimuthal_angle(np.pi / 4)
lobe.center = [20, 10]

extent = lobe.extent_xy()

perimeter = np.array(lobe.rasterize_perimeter(30))

x_data = np.linspace(0, 40, 40)
y_data = np.linspace(0, 20, 20)
height_data = np.zeros(shape=(len(x_data), len(y_data)))

height_data = np.array([[0 for j in range(len(y_data))] for i in range(len(x_data))])

topography = pfy.flowycpp.Topography(height_data, x_data, y_data)

bbox = topography.bounding_box(lobe.center, extent[0], extent[1])

# Add the lobe
# topography.add_lobe(lobe, None)
new_height_data = np.copy(topography.height_data)
add_lobe(lobe, topography, new_height_data)

# print(bbox.idx_x_higher, bbox.idx_y_higher)

# Plot
cell = topography.cell_size()
# plt.pcolormesh(x_data+0.5*cell, y_data+0.5*cell, topography.height_data.T)
plt.pcolormesh(x_data + 0.5 * cell, y_data + 0.5 * cell, new_height_data.T)
plt.axvline(x_data[bbox.idx_x_lower], color="black")
plt.axvline(x_data[bbox.idx_x_higher], color="black")
plt.axhline(y_data[bbox.idx_y_lower], color="black")
plt.axhline(y_data[bbox.idx_y_higher], color="black")
plt.plot(perimeter[:, 0], perimeter[:, 1], color="white")

plt.show()
