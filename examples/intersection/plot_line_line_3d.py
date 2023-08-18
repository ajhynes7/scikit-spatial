"""
3D Line-Line Intersection
=========================

"""
from skspatial.objects import Line
from skspatial.plotting import plot_3d


line_a = Line(point=[0, 0, 0], direction=[1, 1, 1])
line_b = Line(point=[1, 1, 0], direction=[-1, -1, 1])

point_intersection = line_a.intersect_line(line_b)


plot_3d(
    line_a.plotter(),
    line_b.plotter(),
    point_intersection.plotter(c='k', s=75),
)
