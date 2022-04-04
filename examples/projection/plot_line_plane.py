"""
Line-Plane Projection
=======================

Project a line onto a plane.

"""
from skspatial.objects import Line
from skspatial.objects import Plane
from skspatial.plotting import plot_3d

plane = Plane([0, 1, 0], [0, 1, 0])
line = Line([0, -1, 0], [1, -2, 0])

line_projected = plane.project_line(line)


plot_3d(
    plane.plotter(lims_x=(-5, 5), lims_y=(-5, 5), alpha=0.3),
    line.plotter(t_1=-2, t_2=2, color='k'),
    line_projected.plotter(t_1=-2, t_2=4, color='r'),
)
