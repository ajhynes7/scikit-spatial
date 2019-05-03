"""
2D Point-Line Projection
========================

Project a point onto a line.

"""
import matplotlib.pyplot as plt

from skspatial.objects import Point, Line


line = Line(point=[0, 0], direction=[1, 1])
point = Point([5, 3])

point_projected = line.project_point(point)


_, ax = plt.subplots()

line.plot_2d(ax, t_2=5, c='k')
point.plot_2d(ax, s=75, c='k')
point_projected.plot_2d(ax, c='r', s=75, zorder=3)

plt.axis('equal')
plt.show()
