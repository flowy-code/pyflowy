import flowpy as fpy
import numpy as np
import matplotlib.pyplot as plt

lobe = fpy.flowpycpp.Lobe()
lobe.semi_axes = [1-1e-14, 1-1e-14]
lobe.thickness = 20.0
lobe.set_azimuthal_angle(0)
lobe.center = [0, 0]



def add_cell(idx_x, idx_y, height_data, frac):
    height_data[idx_x, idx_y] += frac


extent = lobe.extent_xy()
perimeter = np.array(lobe.rasterize_perimeter(2048))

x_data      = np.arange( -3, 3, 1.0 )
y_data      = np.arange( -3, 3, 1.0 )

height_data = np.zeros(shape=(len(x_data), len(y_data)))
topography = fpy.flowpycpp.Topography(height_data, x_data, y_data)


# Iterate over the y_direction and scan the intersection with the ellipse in x direction


class IntersectionData:
    def __init__(self, lobe, topography) -> None:

        # one set per row, organized in these lists
        self.enclosed_cells = []
        self.intersected_cells = []

        # Row wise start and end of the enclosed cells
        self.idx_x_enclosed_start = []
        self.idx_x_enclosed_end = []

        self.lobe = lobe
        extent = lobe.extent_xy()

        self.topography = topography
        # We scan the extents of the ellipse row wise
        self.n_lines_scan = 120
        self.y_space = np.linspace(
            lobe.center[1] - extent[1], lobe.center[1] + extent[1], self.n_lines_scan
        )

        self.line_segment_intersects = []

        self.idx_y_min = int(
            np.floor((lobe.center[1] - extent[1] - y_data[0] / self.topography.cell_size()))
        )
        self.idx_y_max = int(
            np.floor(
                (lobe.center[1] + extent[1] - y_data[0] / self.topography.cell_size())
            )
        )
        self.n_rows = self.idx_y_max - self.idx_y_min + 1

    def perform_line_segment_computations(self):
        for y in self.y_space:
            # Compute the index of the current row
            # Then we get the intersections of the lobe with the current scan line
            x1 = np.array([lobe.center[0] - extent[0], y])
            x2 = np.array([lobe.center[0] + extent[0], y])
            points = lobe.line_segment_intersects(x1, x2)
            self.line_segment_intersects.append(points)

    # This function scans the lobe and find all enclosed cells, as well as the intersecting cells
    def find_cells(self):

        idx_x_left =  -np.ones(self.n_rows+1, dtype=int) #-1 signals the absence of an intersection
        idx_x_right = -np.ones(self.n_rows+1, dtype=int) #-1 signals the absence of an intersection

        self.intersected_cells = [[] for _ in range(self.n_rows)]
        self.enclosed_cells = [[] for _ in range(self.n_rows)]

        # For each row in the extent we record the x_values at which the bottom of the row intersects the lobe
        # We iterate up to the inclusion of self.idx_max+1 to get the top of the last row
        for idx_row, idx_y in enumerate(range(self.idx_y_min, self.idx_y_max+2)):
            print(f"idx_row/nrows = {idx_row} / {self.n_rows}")
            y = self.topography.y_data[idx_y]
            x1 = np.array([lobe.center[0] - extent[0], y])
            x2 = np.array([lobe.center[0] + extent[0], y])
            points = lobe.line_segment_intersects(x1, x2)

            if points is not None:
                p1 = points[0]
                p2 = points[1]

                idx_x_left[idx_row] = int(
                    np.floor((p1[0] - x_data[0]) / topography.cell_size())
                )
                idx_x_right[idx_row] = int(
                    np.floor((p2[0] - x_data[0]) / topography.cell_size())
                )

            idx_x_left_cur = idx_x_left[idx_row]
            idx_x_right_cur = idx_x_right[idx_row]

            # The bottom of the next row, is the top of the previous one
            if idx_row > 0:

                idx_x_left_prev = idx_x_left[idx_row - 1]
                idx_x_right_prev = idx_x_right[idx_row - 1]

                # We treat the first and last row separately.
                # We know that there are no intersections a the bottom of the first row, since that is how the extent is defines.
                if(idx_y == self.idx_y_min + 1):
                    for idx_x in range(idx_x_left_cur, idx_x_right_cur+1):
                        self.intersected_cells[0].append([idx_x, idx_y - 1, 0.5])
                elif(idx_y == self.idx_y_max + 1):
                    # self.intersected_cells[idx_row - 1].append([idx_x_left_cur, idx_y - 1, 0.5])
                    for idx_x in range(idx_x_left_prev, idx_x_right_prev+1):
                        self.intersected_cells[idx_row - 1].append([idx_x, idx_y - 1, 0.5])
                else:
                    start_left = min(idx_x_left_prev, idx_x_left[idx_row])
                    stop_left = max(idx_x_left_prev, idx_x_left[idx_row])
                    for idx_x in range(start_left, stop_left+1):
                        self.intersected_cells[idx_row - 1].append([idx_x, idx_y - 1, 0.5])

                    start_right = min(idx_x_right_prev, idx_x_right[idx_row])
                    stop_right = max(idx_x_right_prev, idx_x_right[idx_row])
                    for idx_x in range(start_right, stop_right+1):
                        self.intersected_cells[idx_row - 1].append([idx_x, idx_y - 1, 0.5])

                    for idx_x in range(stop_left+1, start_right):
                        self.enclosed_cells[idx_row - 1].append([idx_x, idx_y-1, 1.0])



idata = IntersectionData(lobe, topography)
idata.find_cells()

plt.axhline(y_data[idata.idx_y_max])
plt.axhline(y_data[idata.idx_y_min])


new_heights = np.zeros_like(topography.height_data)


# for row_set in idata.enclosed_cells:
#     for [idx_x, idx_y, frac] in row_set:
#         print(idx_x, idx_y, frac)
#         add_cell(idx_x, idx_y, new_heights, frac)


# for row_set in idata.intersected_cells:
print(idata.intersected_cells)

for row_d in idata.intersected_cells:
    for [idx_x, idx_y, frac] in row_d:
        print(idx_x, idx_y, frac)
        add_cell(idx_x, idx_y, new_heights, frac)


for row_d in idata.enclosed_cells:
    for [idx_x, idx_y, frac] in row_d:
        print(idx_x, idx_y, frac)
        add_cell(idx_x, idx_y, new_heights, frac)



# for row_set in idata.intersected_cells_right:
#     for [idx_x, idx_y, frac] in row_set:
#         print(idx_x, idx_y, frac)
#         add_cell(idx_x, idx_y, new_heights, frac)


# for [idx_x, idx_y, frac] in idata.intersected_cells_right:
#     print(idx_x, idx_y, frac)
#     add_cell(idx_x, idx_y, new_heights, frac)

# for p in intersection_points:
#     plt.plot(  [p[0]], [p[1]], marker="o", color="white")

# Plot
cell = topography.cell_size()
        
for x in x_data:
    plt.axvline(x, color="grey", zorder=99)

for y in y_data:
    plt.axhline(y, color="grey", zorder=99)        

plt.pcolormesh(x_data + 0.5 * cell, y_data + 0.5 * cell, new_heights.T)
# plt.axvline(x_data[bbox.idx_x_lower], color="black")
# plt.axvline(x_data[bbox.idx_x_higher], color="black")
# plt.axhline(y_data[bbox.idx_y_lower], color="black")
# plt.axhline(y_data[bbox.idx_y_higher], color="black")
plt.plot(perimeter[:, 0], perimeter[:, 1], color="white")

plt.show()
