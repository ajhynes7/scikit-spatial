"""
2D Line-Line Intersection
=========================

Intersect two 2D lines.

"""
import matplotlib.pyplot as plt

from skspatial.objects import Line


line_a = Line(point=[0, 0], direction=[1, 1.5])
line_b = Line(point=[5, 0], direction=[-1, 1])

point_intersection = line_a.intersect_line(line_b)


_, ax = plt.subplots()

line_a.plot_2d(ax, t_1=3)
line_b.plot_2d(ax, t_1=4)
point_intersection.plot_2d(ax, c='k', s=75, zorder=3)

plt.show()
