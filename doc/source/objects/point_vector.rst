
Point and Vector
----------------

The two basic spatial objects are the :class:`~skspatial.objects.Point`, which represents a position in space, and the :class:`~skspatial.objects.Vector`, which represents an arrow through space.

They are instantiated with an ``array_like`` object, which is an object that can be passed to :func:`numpy.array`.

>>> import numpy as np
>>> from skspatial.objects import Point

>>> point_1 = Point([1, 2])
>>> point_2 = Point((1, 2))
>>> point_3 = Point(np.array([1, 2]))

>>> np.array_equal(point_1, point_2)
True

>>> np.array_equal(point_1, point_3)
True


:class:`~skspatial.objects.Point` and :class:`~skspatial.objects.Vector` are both subclasses of the NumPy :class:`~numpy.ndarray`, which gives them all the functionality of a regular NumPy array.

>>> point_1
Point([1, 2])

>>> point_1.size
2

>>> point_1.shape
(2,)


The magnitude of a vector is found with the :meth:`~skspatial.objects.Vector.norm` method.

>>> from skspatial.objects import Vector

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

>>> vector_u.project_vector(vector_v)  # Project vector v onto vector u.
Vector([5., 0.])
