
Point and Vector
----------------

The two basic spatial objects are the `Point` and `Vector`.

They are instantiated with an `array_like` object, which can be passed to `np.array()`.

>>> import numpy as np
>>> from skspatial.objects import Point

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
dpcontracts.PreconditionError: The input length must be one to three.


The `Point` stores a numpy array which can be accessed.

>>> point = Point([5.2, 7.1])
>>> point.array
array([5.2, 7.1, 0. ])

>>> point.array.size
3

A `Point` can be viewed as a position in space, and a `Vector` as an arrow through space.

Thus, a `Point` plus a `Vector` returns a `Point`

>>> from skspatial.objects import Vector

>>> Point([-5, 8]).add(Vector([1, 1]))
Point([-4.  9.  0.])

while a `Point` plus a `Point` is undefined.

>>> Point([-5, 8]).add(Point([1, 1]))
Traceback (most recent call last):
...
dpcontracts.PreconditionError: the types of arguments must be valid


A `Vector` plus a `Vector` returns another `Vector`.

>>> Vector([1, 1]).add(Vector([2, -5]))
Vector([ 3. -4.  0.])

A `Vector` has a magnitude attribute.

>>> vector = Vector([1, 1])
>>> vector.magnitude.round(3)
1.414

The unit vector can also be obtained.

>>> vector_unit = vector.unit()

>>> vector_unit.array.round(3)
array([0.707, 0.707, 0.   ])

One vector can be projected onto another.

>>> vector_u = Vector([1, 0])
>>> vector_v = Vector([5, 9])

>>> vector_u.project_vector(vector_v)  # Project vector v onto vector u.
Vector([5. 0. 0.])

Points and vectors are not equal.

>>> Point([1, 2]) == Vector([1, 2])
False

