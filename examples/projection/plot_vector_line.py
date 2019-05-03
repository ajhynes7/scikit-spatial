"""
3D Vector-Line Projection
=========================

Project a vector onto a line.

"""
import matplotlib.pyplot as plt

from skspatial.objects import Vector, Line


line = Line([0, 0, 0], [1, 1, 2])
vector = Vector([1, 1, 0.1])

vector_projected = line.project_vector(vector)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

line.plot_3d(ax, t_1=-1, t_2=1, c='k', linestyle='--')
vector.plot_3d(ax, line.point, color='k')
vector_projected.plot_3d(ax, line.point, color='r', linewidth=2, zorder=3)

plt.show()
