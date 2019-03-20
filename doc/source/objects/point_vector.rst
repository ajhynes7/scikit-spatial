
Point and Vector
----------------

The two basic spatial objects are the `Point` and `Vector`. 

They are instantiated with an `array_like` object, which is an object that can be passed to `np.array()`.

>>> import numpy as np
>>> from skspatial.objects import Point

>>> point_1 = Point([1, 2])
>>> point_2 = Point((1, 2))
>>> point_3 = Point(np.array([1, 2]))

>>> np.array_equal(point_1, point_2)
True

>>> np.array_equal(point_1, point_3)
True

The `Point` and `Vector` are both subclasses of the NumPy `ndarray`, which gives them all the functionality of a regular NumPy array.

>>> point_1.size
2

>>> point_1.shape
(2,)


>>> point_1
Point([1., 2.])


A `Point` can be viewed as a position in space, and a `Vector` as an arrow through space.

Thus, a `Point` plus a `Vector` returns a `Point`.

>>> from skspatial.objects import Vector

>>> Point([-5, 8]).add(Vector([1, 1]))
Point([-4.,  9.])


A `Vector` plus a `Vector` returns another `Vector`.

>>> Vector([1, 1]).add(Vector([2, -5]))
Vector([ 3., -4.])


The magnitude of the vector is found with the `norm` method.

>>> vector = Vector([1, 1])
>>> vector.norm().round(3)
1.414

The unit vector can also be obtained.

>>> vector_unit = vector.unit()

>>> vector_unit.round(3)
array([0.707, 0.707])

One vector can be projected onto another.

>>> vector_u = Vector([1, 0])
>>> vector_v = Vector([5, 9])

>>> vector_u.project(vector_v)  # Project vector v onto vector u.
Vector([5., 0.])
