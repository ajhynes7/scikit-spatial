"""
Cylinder-Line Intersection
==========================

"""

from skspatial.objects import Cylinder, Line
from skspatial.plotting import plot_3d

cylinder = Cylinder([0, 0, 0], [0, 0, 1], 1)
line = Line([0, 0, 0], [1, 0, 0.7])

point_a, point_b = cylinder.intersect_line(line, infinite=False)


plot_3d(
    line.plotter(c='k'),
    cylinder.plotter(alpha=0.2),
    point_a.plotter(c='r', s=100),
    point_b.plotter(c='r', s=100),
)
