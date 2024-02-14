"""
2D Vector-Vector Projection
===========================

Project a vector onto another vector.

"""

from skspatial.objects import Vector
from skspatial.plotting import plot_2d

vector_a = Vector([1, 1])
vector_b = Vector([2, 0])

vector_projected = vector_b.project_vector(vector_a)


_, ax = plot_2d(
    vector_a.plotter(color='k', head_width=0.1),
    vector_b.plotter(color='k', head_width=0.1),
    vector_projected.plotter(color='r', head_width=0.1),
)

ax.axis([-0.5, 2.5, -0.5, 1.5])
