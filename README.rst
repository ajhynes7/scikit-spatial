
scikit-spatial: Spatial objects and computations in 3D
======================================================

Point and Vector
----------------

The two basic spatial objects are the `Point` and `Vector`.

They are instantiated with an `array_like` object, which can be passed to `np.array()`.

>>> import numpy as np
>>> from skspatial import Point

>>> point_1 = Point([1, 2])
>>> point_2 = Point((1, 2))
>>> point_3 = Point(np.array([1, 2]))

>>> point_1 == point_2 == point_3
True

The input `array_like` must have a length of one to three. However, zeros are padded to the end so that the `Point` or `Vector` is always 3D. This is done for two main reasons:

- It ensures that the `Point` and `Vector` objects always have the same dimension.
- It ensures that the output of `np.cross` is also a 3D array.

>>> Point([1])
Point([1. 0. 0.])

>>> Point([1, 2])
Point([1. 2. 0.])

>>> Point([1, 1, 1])
Point([1. 1. 1.])

>>> Point([1, 1, 1, 1])
Traceback (most recent call last):
...
dpcontracts.PreconditionError: The input length must one to three.


The `Point` stores a numpy array which can be accessed.

>>> point = Point([5.2, 7.1])
>>> point.array
array([5.2, 7.1, 0. ])

>>> point.array.size
3

The `Vector` is similar to a `Point`, but it has additional functionality.

A `Vector` has a magnitude attribute.

>>> from skspatial import Vector
>>> vector = Vector([1, 1])

>>> round(vector.magnitude, 3)
1.414

The unit vector can also be obtained.

>>> vector_unit = vector.unit()

>>> vector_unit.array.round(3)
array([0.707, 0.707, 0.   ])

One vector can be projected onto another.

>>> from skspatial.projection import project_vector

>>> vector_u = Vector([5, 9])
>>> vector_v = Vector([1, 0])

>>> project_vector(vector_u, vector_v)
Vector([5. 0. 0.])

Points and vectors are not equal.

>>> Point([1, 2]) == Vector([1, 2])
False


Line
----

A `Line` is defined by a `Point` and a `Vector`. The direction of the line is the unit vector of the input `Vector`.

>>> from skspatial import Line

>>> line_1 = Line(Point([0, 0]), Vector([5, 0]))

>>> line_1
Line(point=Point([0. 0. 0.]), direction=Vector([1. 0. 0.]))


The `Point` and `Vector` inputs are not interchangeable.

>>> Line(Vector([0, 0]), Point([5, 0]))
Traceback (most recent call last):
...
dpcontracts.PreconditionError: The inputs must be a point and a vector.


Alternatively, a `Line` can be defined by two points.

>>> line_2 = Line.from_points(Point([0, 0]), Point([100, 0]))

>>> line_1 == line_2
True

The distance from a `Point` to a `Line` can be found.

>>> from skspatial.distance import dist_point_line

>>> dist_point_line(Point([20, 75]), line_1)
75.0

A `Point` can be projected onto a `Line`, returning a new `Point`.

>>> from skspatial.projection import project_point_line

>>> project_point_line(Point([50, 20]), line_1)
Point([50.  0.  0.])


Plane
-----

A `Plane` is defined by a `Point` and a `Vector`. The normal vector of the plane is the unit vector of the input `Vector`.

>>> from skspatial import Plane

>>> plane_1 = Plane(Point([0, 0]), Vector([0, 0, 23]))

>>> plane_1
Plane(point=Point([0. 0. 0.]), normal=Vector([0. 0. 1.]))

Alternatively, a plane can be defined by three points.

>>> point_a, point_b, point_c = Point([0, 0]), Point([10, -2]), Point([50, 500])
>>> plane_2 = Plane.from_points(point_a, point_b, point_c)

>>> plane_1 == plane_2
True

However, changing the order of the points can reverse the direction of the normal vector.

>>> plane_3 = Plane.from_points(point_a, point_c, point_b)

>>> plane_3
Plane(point=Point([0. 0. 0.]), normal=Vector([ 0.  0. -1.]))

>>> plane_1 == plane_3
False

Again, a `Point` and a `Vector` are not interchangeable.

>>> Plane.from_points(point_a, point_b, Vector([50, 500]))
Traceback (most recent call last):
...
dpcontracts.PreconditionError: The inputs must be three points.
