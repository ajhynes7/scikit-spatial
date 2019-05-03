"""
Line-Plane Intersection
=======================

Intersect a line with a plane.

"""
import matplotlib.pyplot as plt

from skspatial.objects import Line, Plane


plane = Plane(point=[0, 0, 0], normal=[1, 1, 1])
line = Line(point=[-1, -1, 0], direction=[0, 0, 1])

point_intersection = plane.intersect_line(line)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plane.plot_3d(ax, lims_x=[-2, 2], lims_y=[-2, 2], alpha=0.2)
line.plot_3d(ax, t_1=-1, t_2=5)
point_intersection.plot_3d(ax, c='k', s=75)
