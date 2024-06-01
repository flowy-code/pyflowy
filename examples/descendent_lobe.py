import pyflowy as pfy
import numpy as np
import matplotlib.pyplot as plt
import math

def compute_descendent_lobe_position( descendent_lobe, parent_lobe, final_budding_point ):
    direction_to_new_lobe = ( final_budding_point - parent_lobe.center ) / np.linalg.norm( final_budding_point - parent_lobe.center )
    new_lobe_center = final_budding_point + direction_to_new_lobe * descendent_lobe.semi_axes[0]
    return new_lobe_center

def compute_lobe_axes( lobe, slope, input, lobe_dimensions ):
    slope_norm = np.linalg.norm( slope, 2 )

    # Factor for the lobe eccentricity
    aspect_ratio = min( input.max_aspect_ratio, 1.0 + input.aspect_ratio_coeff * slope_norm )
    # breakpoint()
    # aspect_ratio = 2.0

    # Compute the semi-axes of the lobe
    semi_major_axis = np.sqrt( lobe_dimensions.lobe_area / np.pi ) * np.sqrt( aspect_ratio )
    semi_minor_axis = np.sqrt( lobe_dimensions.lobe_area / np.pi ) / np.sqrt( aspect_ratio )
    return semi_major_axis, semi_minor_axis

# Input parameters (we just construct this here)
input = pfy.flowycpp.InputParams()
input.source = "file.asc"
input.total_volume = 20
input.prescribed_avg_lobe_thickness = 1
# Required for calculating the lobe_area
input.n_flows = 1
input.min_n_lobes = 1
input.max_n_lobes = 1
# For perturb angle and inertial contribution
input.max_slope_prob = 1  # 0.5
input.inertial_exponent = 0.0
# Aspect ratio info required to create the descendent lobe axes
input.max_aspect_ratio = 2.5
input.aspect_ratio_coeff = 2.0

# Create a Simulation object
simulation = pfy.flowycpp.Simulation(input, None)
# Topography data
x_data = np.linspace(0, 40, 40)
y_data = np.linspace(0, 20, 20)
height_data = np.zeros(shape=(len(x_data), len(y_data)))
height_data = np.array(
    [[i + j for j in range(len(y_data))] for i in range(len(x_data))]
)
topography = pfy.flowycpp.Topography(height_data, x_data, y_data)
simulation.topography = topography

# Parent lobe
parent_lobe = pfy.flowycpp.Lobe()
parent_lobe.semi_axes = [6, 2]
parent_lobe.thickness = 20.0
parent_lobe.center = [20, 10]
# Descendent lobe
descendent_lobe = pfy.flowycpp.Lobe()
descendent_lobe.thickness = 20.0

# Find the height and slope at the parent center and perturb the angle accordingly
height_parent_center, slope_parent_center = topography.height_and_slope(
    parent_lobe.center
)
simulation.perturb_lobe_angle(parent_lobe, slope_parent_center)
# Perimeter of the parent lobe, rasterized so you can see it
perimeter = np.array(parent_lobe.rasterize_perimeter(30))
print("Azimuthal angle of the parent in pi", parent_lobe.get_azimuthal_angle()/np.pi)

#### Now we are done changing the parent lobe

budding_point = topography.find_preliminary_budding_point(parent_lobe, 30)
simulation.perturb_lobe_angle(descendent_lobe, slope_parent_center) # This should have set the azimuthal angle

simulation.add_inertial_contribution( descendent_lobe, parent_lobe, slope_parent_center )

angle_diff             = parent_lobe.get_azimuthal_angle() - descendent_lobe.get_azimuthal_angle()
final_budding_point = parent_lobe.point_at_angle( np.pi - angle_diff )
height_budding_point, slope_budding_point = topography.height_and_slope( final_budding_point )
print("Azimuthal angle of the descendent in pi ", descendent_lobe.get_azimuthal_angle()/np.pi)
# Compute the lobe axes and center of the new descendent lobe
simulation.compute_lobe_axes( descendent_lobe, slope_budding_point ) 
# major_axis, minor_axis = compute_lobe_axes( descendent_lobe, slope_budding_point, input, lobe_dimensions )
# descendent_lobe.semi_axes = [major_axis, minor_axis]
print("Axes = ", descendent_lobe.semi_axes)
# Compute the final descendent center 
new_lobe_center = compute_descendent_lobe_position( descendent_lobe, parent_lobe, final_budding_point )
descendent_lobe.center             = new_lobe_center
print("new lobe center ", new_lobe_center)
perimeter_descendent = np.array(descendent_lobe.rasterize_perimeter(30))

# Representation of the topography
plt.pcolormesh(x_data, y_data, topography.height_data.T)
plt.plot(perimeter[:, 0], perimeter[:, 1], color="black") # parent lobe
plt.plot(perimeter_descendent[:, 0], perimeter_descendent[:, 1], color="red") # descendent lobe
# Budding points
plt.plot(budding_point[0], budding_point[1], marker="o", color="black", ms=12)
plt.plot(final_budding_point[0], final_budding_point[1], marker=".", color="red", ms=12)
plt.plot(new_lobe_center[0], new_lobe_center[1], marker=".", color="green", ms=12)

plt.gca().set_box_aspect(1)
plt.show()
plt.savefig("descendent.png", dpi=300)
