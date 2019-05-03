"""
Plane-Plane Intersection
========================

Intersect a plane with another plane.

"""
import matplotlib.pyplot as plt

from skspatial.objects import Plane


plane_a = Plane([0, 0, 0], [-1, 0, 1])
plane_b = Plane([1, 0, 0], [1, 0, 1])

line_intersection = plane_a.intersect_plane(plane_b)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plane_a.plot_3d(ax, lims_x=[-5, 5], lims_y=[-2, 2], alpha=0.2)
plane_b.plot_3d(ax, lims_x=[-5, 5], lims_y=[-2, 2], alpha=0.2)
line_intersection.plot_3d(ax, t_1=-1, t_2=1, c='k')

plt.show()
