"""
Plane-Line Intersection
=======================

"""
from skspatial.objects import Line, Plane
from skspatial.plotting import plot_3d


plane = Plane(point=[0, 0, 0], normal=[1, 1, 1])
line = Line(point=[-1, -1, 0], direction=[0, 0, 1])

point_intersection = plane.intersect_line(line)


plot_3d(
    plane.plotter(lims_x=[-2, 2], lims_y=[-2, 2], alpha=0.2),
    line.plotter(t_2=5),
    point_intersection.plotter(c='k', s=75),
)
