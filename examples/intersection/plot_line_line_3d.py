"""
3D Line-Line Intersection
=========================

Intersect two 3D lines.

"""
import matplotlib.pyplot as plt

from skspatial.objects import Line


line_a = Line(point=[0, 0, 0], direction=[1, 1, 1])
line_b = Line(point=[1, 1, 0], direction=[-1, -1, 1])

point_intersection = line_a.intersect_line(line_b)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

line_a.plot_3d(ax)
line_b.plot_3d(ax)
point_intersection.plot_3d(ax, c='k', s=75)

plt.show()
