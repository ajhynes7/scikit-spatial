"""
Vector-Plane Projection
=======================

Project a vector onto a plane.

"""
import matplotlib.pyplot as plt

from skspatial.objects import Vector, Plane


plane = Plane([0, 0, 0], [0, 0, 1])
vector = Vector([1, 1, 1])

vector_projected = plane.project_vector(vector)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plane.plot_3d(ax, lims_x=(-5, 5), lims_y=(-5, 5), alpha=0.3)
vector.plot_3d(ax, plane.point, color='k')

vector_projected.plot_3d(ax, plane.point, color='r', linewidth=2, zorder=3)

ax.set_zlim([-1, 1])
plt.show()
