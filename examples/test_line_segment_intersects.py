import flowpy as fpy
import numpy as np
import matplotlib.pyplot as plt

lobe = fpy.flowpycpp.Lobe()
lobe.semi_axes = [8, 2]
lobe.thickness = 20.0
lobe.set_azimuthal_angle(np.pi / 4)
lobe.center = [20, 10]

def plot_lines_intersect(x1, x2):
    plt.plot( [x1[0], x2[0]], [x1[1], x2[1]] )

    intersection = lobe.line_segment_intersects(x1, x2) 
    if intersection is None:
        print("no intersection")
        return
    
    p1 = intersection[0]
    p2 = intersection[1]
    print("p1= ", p1)
    print("p2= ", p2)
    plt.plot( [p1[0], p2[0]], [p1[1], p2[1]], ls="none", marker="o", color="r" )


# extent = lobe.extent_xy()

perimeter = np.array(lobe.rasterize_perimeter(30))

x1 = np.array([0, 5.0])
x2 = np.array([15, 6])


# Plot
plt.plot(perimeter[:, 0], perimeter[:, 1], color="black")
plot_lines_intersect(x1, x2)

plt.show()