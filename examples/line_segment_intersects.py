import pyflowy as pfy
import numpy as np
import matplotlib.pyplot as plt

lobe = pfy.flowycpp.Lobe()
lobe.semi_axes = [2, 1]
lobe.set_azimuthal_angle(np.pi / 4)
lobe.center = [1, 2]


def plot_lines_intersect(x1, x2):
    plt.plot([x1[0], x2[0]], [x1[1], x2[1]])

    intersection = lobe.line_segment_intersects(x1, x2)

    if intersection is None:
        print("no intersection")
        p1 = [float("nan"), float("nan")]
        p2 = [float("nan"), float("nan")]
    else:
        p1 = intersection[0]
        p2 = intersection[1]
    print("x1 = [ {}, {} ] ".format(*x1))
    print("x2 = [ {}, {} ] ".format(*x2))
    print("p1 = [ {}, {} ] ".format(*p1))
    print("p2 = [ {}, {} ] ".format(*p2))
    print("\n")
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], ls="none", marker="o", color="r")


# extent = lobe.extent_xy()

perimeter = np.array(lobe.rasterize_perimeter(30))


# Plot
plt.plot(perimeter[:, 0], perimeter[:, 1], color="black")

x1 = lobe.center
x2 = [2, 2]
plot_lines_intersect(x1, x2)

x1 = lobe.center
x2 = [4, 4]
plot_lines_intersect(x1, x2)

x1 = [-1, -1]
x2 = [4, 4]
plot_lines_intersect(x1, x2)

x1 = [-1, -1]
x2 = [4, -4]
plot_lines_intersect(x1, x2)

x1 = [0, 2.5]
x2 = [0.5, 2.5]
plot_lines_intersect(x1, x2)

x1 = [0, 3.0]
x2 = [-0.5, 3.0]
plot_lines_intersect(x1, x2)

plt.show()
