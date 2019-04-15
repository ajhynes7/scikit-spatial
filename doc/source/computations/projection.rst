
Projection
==========

Vector-Vector Projection
------------------------ 

Project a vector onto a vector.

>>> from skspatial.objects import Vector

>>> vector_a = Vector([1, 0])

>>> vector_a.project_vector([22, 9])  # Project vector B onto vector A.
Vector([22.,  0.])


Point-Line Projection
---------------------

Project a point onto a line.

>>> from skspatial.objects import Line

>>> line = Line(point=[0, 0, 0], direction=[1, 1, 0])

>>> line.project_point([5, 5, 3])
Point([5., 5., 0.])


Point-Plane Projection
----------------------

Project a point onto a plane.

>>> from skspatial.objects import Plane

>>> plane = Plane(point=[0, 0, 0], normal=[0, 0, 2])

>>> plane.project_point([5, 9, -3])
Point([5., 9., 0.])



Vector-Line Projection
----------------------

Project a vector onto a line.

>>> line = Line([-1, 5, 3], [3, 4, 5])

>>> line.project_vector([1, 1, 1])
Vector([0.72, 0.96, 1.2 ])


Vector-Plane Projection
-----------------------

Project a vector onto a plane.

>>> plane = Plane([0, 4, 0], [0, 1, 1])

>>> plane.project_vector([2, 4, 8])
Vector([ 2., -2.,  2.])
