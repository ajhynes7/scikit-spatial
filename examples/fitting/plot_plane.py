"""
3D Plane of Best Fit
====================

Fit a plane to multiple 3D points.

"""

from skspatial.objects import Plane, Points
from skspatial.plotting import plot_3d

points = Points([[0, 0, 0], [1, 3, 5], [-5, 6, 3], [3, 6, 7], [-2, 6, 7]])

plane = Plane.best_fit(points)


plot_3d(
    points.plotter(c='k', s=50, depthshade=False),
    plane.plotter(alpha=0.2, lims_x=(-5, 5), lims_y=(-5, 5)),
)
