
Points
------

The :class:`~skspatial.objects.Points` class represents multiple points in space.

While :class:`~skspatial.objects.Point` and :class:`~skspatial.objects.Vector` objects are instantiated with a 1D array, a :class:`~skspatial.objects.Points` object is instantiated with a 2D array.

>>> from skspatial.objects import Points

>>> points = Points([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


The centroid of the points is a :class:`~skspatial.objects.Point`.

>>> points.centroid()
Point([4., 5., 6.])


The points can be mean-centered, meaning that the centroid is treated as the origin of a new coordinate system.

>>> points_centered, centroid = points.mean_center()

>>> points_centered
Points([[-3., -3., -3.],
        [ 0.,  0.,  0.],
        [ 3.,  3.,  3.]])

The original centroid is also returned by the method.

>>> centroid
Point([4., 5., 6.])


The affine rank is the dimension of the smallest affine space that contains all the points.
For example, if the points are contained by a line, the affine rank is one.

>>> points.affine_rank()
1

The affine rank is used to test for concurrency, collinearity and coplanarity.

>>> points.are_concurrent()
False
>>> points.are_collinear()
True
>>> points.are_coplanar()
True
