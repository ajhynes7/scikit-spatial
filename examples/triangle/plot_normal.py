"""
Triangle with Normal Vector
===========================

Plotting a triangle with its normal vector. The tail of the vector is set to be the triangle centroid.

"""
from skspatial.objects import Triangle
from skspatial.plotting import plot_3d


triangle = Triangle([0, 0, 1], [1, 1, 0], [0, 2, 1])

centroid = triangle.centroid()

plot_3d(
    triangle.plotter(c='k', zorder=3),
    centroid.plotter(c='r'),
    triangle.normal().plotter(point=centroid, scalar=0.2, c='r'),
    *[x.plotter(c='k', zorder=3) for x in triangle.multiple('line', 'abc')],
)
