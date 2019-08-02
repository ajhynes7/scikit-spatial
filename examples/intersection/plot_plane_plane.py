"""
Plane-Plane Intersection
========================

"""
from skspatial.objects import Plane
from skspatial.plotting import plot_3d


plane_a = Plane([0, 0, 0], [1, 0, 0])
plane_b = Plane([0, 0, 0], [1, 0, 1])

line_intersection = plane_a.intersect_plane(plane_b)


plot_3d(
    plane_a.plotter(alpha=0.2),
    plane_b.plotter(alpha=0.2),
    line_intersection.plotter(t_1=-1, c='k'),
)
