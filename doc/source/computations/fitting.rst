
Fitting
=======


Line of Best Fit
----------------

Find the best fitting line of multiple points.

>>> from skspatial.objects import Line

>>> points = [[0, 0], [1, 2], [2, 1], [2, 3], [3, 2]]
>>> line = Line.best_fit(points)

The point on the line is the centroid of the points.

>>> line.point
Point([1.6, 1.6])

The line direction is a unit vector.

>>> line.direction
Vector([0.70710678, 0.70710678])


Plane of Best Fit
-----------------

Find the best fitting plane of multiple 3D points.

>>> from skspatial.objects import Plane

>>> points = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]

>>> plane = Plane.best_fit(points)

The point on the plane is the centroid of the points.

>>> plane.point
Point([0.25, 0.25, 0.25])

The plane normal is a unit vector.

>>> plane.normal
Vector([-0.57735027, -0.57735027, -0.57735027])
