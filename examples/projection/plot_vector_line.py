"""
3D Vector-Line Projection
=========================

Project a vector onto a line.

"""
from skspatial.objects import Vector, Line
from skspatial.plotting import plot_3d


line = Line([0, 0, 0], [1, 1, 2])
vector = Vector([1, 1, 0.1])

vector_projected = line.project_vector(vector)


plot_3d(
    line.plotter(t_1=-1, t_2=1, c='k', linestyle='--'),
    vector.plotter(point=line.point, color='k'),
    vector_projected.plotter(point=line.point, color='r', linewidth=2, zorder=3),
)
