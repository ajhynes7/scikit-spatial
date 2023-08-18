"""
2D Line-Line Intersection
=========================

"""
from skspatial.objects import Line
from skspatial.plotting import plot_2d


line_a = Line(point=[0, 0], direction=[1, 1.5])
line_b = Line(point=[5, 0], direction=[-1, 1])

point_intersection = line_a.intersect_line(line_b)


plot_2d(
    line_a.plotter(t_1=3),
    line_b.plotter(t_1=4),
    point_intersection.plotter(c='k', s=75, zorder=3),
)
