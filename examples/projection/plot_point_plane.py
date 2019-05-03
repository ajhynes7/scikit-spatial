"""
Point-Plane Projection
======================

Project a point onto a plane.

"""
import matplotlib.pyplot as plt

from skspatial.objects import Point, Vector, Plane


plane = Plane(point=[0, 0, 2], normal=[1, 0, 2])
point = Point([5, 9, 3])

point_projected = plane.project_point(point)
vector_projection = Vector.from_points(point, point_projected)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plane.plot_3d(ax, lims_x=(0, 10), lims_y=(0, 15), alpha=0.3)
point.plot_3d(ax, s=75, c='k')

point_projected.plot_3d(ax, c='r', s=75, zorder=3)
vector_projection.plot_3d(ax, point, c='k', linestyle='--')

plt.show()
