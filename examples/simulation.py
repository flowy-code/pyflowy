import pyflowy as pfy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

def select_parent_lobe(idx_descendent):
    return idx_descendent-1

def compute_descendent_lobe_position( descendent_lobe, parent_lobe, final_budding_point ):
    direction_to_new_lobe = ( final_budding_point - parent_lobe.center ) / np.linalg.norm( final_budding_point - parent_lobe.center )
    new_lobe_center = final_budding_point + direction_to_new_lobe * descendent_lobe.semi_axes[0]
    return new_lobe_center

# Input parameters (we just construct this here)
input = pfy.flowycpp.InputParams()
input.source = "file.asc"
input.total_volume = 20
input.prescribed_lobe_area = 20
input.vent_coordinates = np.array([[20,10]])
input.npoints = 30 # ellipse rasterization
input.prescribed_avg_lobe_thickness = 1
input.n_init = 1 # One initial lobe 
# Required for calculating the thickness 
input.n_flows = 1
input.min_n_lobes = 1
input.max_n_lobes = 1
# For perturb angle and inertial contribution
# max_slope_prob = 0 => all the directions have the same probability;
# max_slope_prob > 0 => the maximum slope direction has a larger
#                       probaiblity, and it increases with increasing
# 			value of the parameter;
# max_slope_prob = 1 => the direction of the new lobe is the maximum
# 			slope direction.
input.max_slope_prob = 1  # 0.5
# inertial_exponent = 0 => the max probability direction for the new lobe is the
#                          max slope direction;
# inertial_exponent > 0 => the max probability direction for the new lobe takes
#                          into account also the direction of the parent lobe and
#                          the inertia increaes with increasing exponent
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

# Reproduce the simulation.run loop 
n_lobes = 3
lobes = [] # List, equivalent to simulation.lobes
budding_point_list = []
thickness = 1 # All lobes have the same thickness

for idx_lobe in range(input.n_init):
    lobe_cur = pfy.flowycpp.Lobe()
    
    simulation.compute_initial_lobe_position( 0, lobe_cur )
    lobe_cur_thickness = thickness
    height_lobe_center, slope_lobe_center = topography.height_and_slope( lobe_cur.center )
    simulation.perturb_lobe_angle( lobe_cur, slope_lobe_center )
    simulation.compute_lobe_axes( lobe_cur, slope_lobe_center )
    lobes.append(lobe_cur)

# Skip initial lobes and go over the rest
for idx_lobe in range(input.n_init, n_lobes):
    lobe_cur = pfy.flowycpp.Lobe()

    idx_parent = select_parent_lobe( idx_lobe )
    lobe_parent = lobes[idx_parent]

    preliminary_budding_point = topography.find_preliminary_budding_point( lobe_parent, input.npoints )
    height_lobe_center, slope_parent = topography.height_and_slope( lobe_parent.center )

    # Perturb and add inertial contribution (also set the azimuthal angle of the descendent lobe in these functions)
    simulation.perturb_lobe_angle( lobe_cur, slope_parent )
    simulation.add_inertial_contribution( lobe_cur, lobe_parent, slope_parent )

    # Final budding point
    angle_diff             = lobe_parent.get_azimuthal_angle() - lobe_cur.get_azimuthal_angle()
    final_budding_point = lobe_parent.point_at_angle( - angle_diff )
    budding_point_list.append(final_budding_point)
    height_budding_point, slope_budding_point = topography.height_and_slope( final_budding_point )

    # compute the new lobe axes and get the lobe center and thickness
    simulation.compute_lobe_axes( lobe_cur, slope_budding_point )
    # simulation.compute_descendent_lobe_position( lobe_cur, lobe_parent, final_budding_point ) # does not work!!
    new_lobe_center = compute_descendent_lobe_position( lobe_cur, lobe_parent, final_budding_point )
    lobe_cur.center             = new_lobe_center
    lobe_cur.thickness = thickness # Set to constant for now

    lobes.append(lobe_cur)

# Representation of the topography
plt.pcolormesh(x_data, y_data, topography.height_data.T)

# Plot the lobes 
colormap = plt.cm.bwr
norm = Normalize(vmin=0, vmax=n_lobes - 1) # Normalize index to range [0, 1] for colormap
scalar_map = ScalarMappable(norm=norm, cmap=colormap)

for i in range(n_lobes):
    color = scalar_map.to_rgba(i)
    perimeter = np.array(lobes[i].rasterize_perimeter(input.npoints))
    plt.plot(perimeter[:, 0], perimeter[:, 1], color=color, label=f'Lobe {i}')
    plt.plot(lobes[i].center[0], lobes[i].center[1], marker="o", color="black", ms=12)

for budding_point in budding_point_list:
    plt.plot(budding_point[0], budding_point[1], marker=".", color="red", ms=12)

plt.gca().set_box_aspect(1)
plt.show()
plt.savefig("simulation_test.png", dpi=300)
