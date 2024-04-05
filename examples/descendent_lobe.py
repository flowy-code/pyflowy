import flowpy as fpy
import numpy as np
import matplotlib.pyplot as plt

# Input parameters (we just construct this here)
input = fpy.flowpycpp.InputParams()
input.source = "file.asc"
input.total_volume = 1
input.prescribed_avg_lobe_thickness = 1
# For perturb angle and inertial contribution
input.max_slope_prob = 0.6  # 0.5
input.inertial_exponent = 0.125

# Create a Simulation object
simulation = fpy.flowpycpp.Simulation(input, None)
# Topography data
x_data = np.linspace(0, 40, 40)
y_data = np.linspace(0, 20, 20)
height_data = np.zeros(shape=(len(x_data), len(y_data)))
height_data = np.array(
    [[i + j for j in range(len(y_data))] for i in range(len(x_data))]
)
topography = fpy.flowpycpp.Topography(height_data, x_data, y_data)
simulation.topography = topography


# Parent lobe
parent_lobe = fpy.flowpycpp.Lobe()
parent_lobe.semi_axes = [8, 2]
parent_lobe.thickness = 20.0
parent_lobe.center = [20, 10]
# Perimeter of the parent lobe, rasterized so you can see it
# Descendent lobe
descendent_lobe = fpy.flowpycpp.Lobe()
descendent_lobe.thickness = 20.0

# Find the height and slope at the parent center and perturb the angle accordingly
height_parent_center, slope_parent_center = topography.height_and_slope(
    parent_lobe.center
)
simulation.perturb_lobe_angle(parent_lobe, slope_parent_center)
perimeter = np.array(parent_lobe.rasterize_perimeter(30))

#### Now we are done changing the parent lobe

budding_point = topography.find_preliminary_budding_point(parent_lobe, 30)
simulation.perturb_lobe_angle(descendent_lobe, slope_parent_center) # This should have set the azimuthal angle

simulation.add_inertial_contribution( descendent_lobe, parent_lobe, slope_parent_center )

angle_diff = parent_lobe.get_azimuthal_angle() - descendent_lobe.get_azimuthal_angle()
print(angle_diff)
final_budding_point = 2.0*parent_lobe.center - parent_lobe.point_at_angle( angle_diff )




# Representation of the topography
plt.pcolormesh(x_data, y_data, topography.height_data.T)
plt.plot(perimeter[:, 0], perimeter[:, 1], color="black")
plt.plot(budding_point[0], budding_point[1], marker="o", color="black", ms=12)
plt.plot(final_budding_point[0], final_budding_point[1], marker=".", color="red", ms=12)


plt.gca().set_box_aspect(1)
# plt.show()
plt.savefig("descendent.png", dpi=300)




# # Find the preliminary budding point, from the center of the parent lobe to the point of lowest elevation on the perimeter

# height_budding_point, slope_budding_point = topography.height_and_slope(budding_point)

# print(height_parent_center, slope_parent_center)
# print(height_budding_point, slope_budding_point)

# # Perturb the lobe angle, but you need the slope of the parent first
# descendent_lobe.set_azimuthal_angle( np.arctan2( slope_parent_center[1], slope_parent_center[0] ) )

# # Add the inertial contribution


# # Representation of the topography
# plt.pcolormesh(x_data, y_data, topography.height_data.T)
# # Preliminary budding point
# plt.plot(final_budding_point[0], final_budding_point[1], marker="o", color="red", ms=12)
# plt.plot(perimeter[:, 0], perimeter[:, 1], color="black")

# plt.gca().set_box_aspect(1)
# # plt.show()
# plt.savefig("descendent.png", dpi=300)
