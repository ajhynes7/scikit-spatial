"""
Plane-Plane Intersection
========================

"""
from skspatial.objects import Plane
from skspatial.plotting import plot_3d


plane_a = Plane([0, 0, 0], [-1, 0, 1])
plane_b = Plane([1, 0, 0], [1, 0, 1])

line_intersection = plane_a.intersect_plane(plane_b)


plot_3d(
    plane_a.plotter(lims_x=[-5, 5], lims_y=[-2, 2], alpha=0.2),
    plane_b.plotter(lims_x=[-5, 5], lims_y=[-2, 2], alpha=0.2),
    line_intersection.plotter(t_1=-1, c='k'),
)
