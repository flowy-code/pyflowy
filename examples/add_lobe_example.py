import pyflowy as pfy
import numpy as np
import matplotlib.pyplot as plt

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

height_data = np.array(
    [[i + j for j in range(len(y_data))] for i in range(len(x_data))]
)

topography = pfy.flowycpp.Topography(height_data, x_data, y_data)

for p in perimeter:
    print(topography.height_and_slope(p))

budding_point = topography.find_preliminary_budding_point(lobe, 30)


new_lobe = pfy.flowycpp.Lobe()
new_lobe.set_azimuthal_angle(0)
new_lobe.thickness = 20
new_lobe.center = [20, 10]
new_lobe.semi_axes = [8, 2]
new_lobe_perimeter = np.array(new_lobe.rasterize_perimeter(30))
new_lobe_extent = new_lobe.extent_xy()


topography.add_lobe(lobe, None)
topography.add_lobe(new_lobe, None)

cell = topography.cell_size()
plt.pcolormesh(x_data+0.5*cell, y_data+0.5*cell, height_data.T)

plt.axvline(lobe.center[0] + extent[0], color="black")
plt.axvline(lobe.center[0] - extent[0], color="black")
plt.axhline(lobe.center[1] + extent[1], color="black")
plt.axhline(lobe.center[1] - extent[1], color="black")

plt.axvline(new_lobe.center[0] + new_lobe_extent[0], color="white")
plt.axvline(new_lobe.center[0] - new_lobe_extent[0], color="white")
plt.axhline(new_lobe.center[1] + new_lobe_extent[1], color="white")
plt.axhline(new_lobe.center[1] - new_lobe_extent[1], color="white")


plt.plot(budding_point[0], budding_point[1], marker="o", color="black", ms=12)

plt.plot(perimeter[:, 0], perimeter[:, 1], color="black")
plt.plot(new_lobe_perimeter[:, 0], new_lobe_perimeter[:, 1], color="white")

plt.gca().set_box_aspect(1)
plt.show()
