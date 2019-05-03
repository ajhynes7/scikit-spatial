"""
2D Vector-Vector Projection
===========================

Project a vector onto another vector.

"""
import matplotlib.pyplot as plt

from skspatial.objects import Vector


vector_a = Vector([1, 1])
vector_b = Vector([2, 0])

vector_projected = vector_b.project_vector(vector_a)

_, ax = plt.subplots()

vector_a.plot_2d(ax, color='k', head_width=0.1)
vector_b.plot_2d(ax, color='k', head_width=0.1)
vector_projected.plot_2d(ax, color='r', head_width=0.1)

plt.axis([-0.5, 2.5, -0.5, 1.5])
plt.show()
