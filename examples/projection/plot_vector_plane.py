"""
Vector-Plane Projection
=======================

Project a vector onto a plane.

"""
from skspatial.objects import Plane
from skspatial.objects import Vector
from skspatial.plotting import plot_3d


plane = Plane([0, 0, 0], [0, 0, 1])
vector = Vector([1, 1, 1])

vector_projected = plane.project_vector(vector)


_, ax = plot_3d(
    plane.plotter(lims_x=(-5, 5), lims_y=(-5, 5), alpha=0.3),
    vector.plotter(point=plane.point, color='k'),
    vector_projected.plotter(point=plane.point, color='r', linewidth=2, zorder=3),
)

ax.set_zlim([-1, 1])
