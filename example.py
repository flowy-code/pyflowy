import flowpy as fpy
import numpy as np
import matplotlib.pyplot as plt

# print( fpy.flowpycpp.add(1,2) )

lobe = fpy.flowpycpp.Lobe()
lobe.semi_axes = [4, 2]
lobe.thickness = 20.0
lobe.set_azimuthal_angle(np.pi / 4)
lobe.center = [20, 10]

perimeter = np.array(lobe.rasterize_perimeter(30))

x_data = np.linspace(0, 40, 40)
y_data = np.linspace(0, 20, 20)
height_data = np.zeros(shape=(len(x_data), len(y_data)))

height_data = np.array(
    [[i + j for j in range(len(y_data))] for i in range(len(x_data))]
)

topography = fpy.flowpycpp.Topography(height_data, x_data, y_data)

for p in perimeter:
    print(topography.height_and_slope(p))

budding_point = topography.find_preliminary_budding_point(lobe, 30)


new_lobe = fpy.flowpycpp.Lobe()
new_lobe.set_azimuthal_angle(0)
new_lobe.semi_axes = [2, 3]

topography.add_lobe(lobe)

plt.pcolormesh(x_data, y_data, topography.height_data.T)
plt.plot(budding_point[0], budding_point[1], marker="o", color="black", ms=12)

plt.plot(perimeter[:, 0], perimeter[:, 1], color="black")
plt.gca().set_box_aspect(1)
plt.show()
