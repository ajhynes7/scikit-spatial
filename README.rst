
==============
scikit-spatial 
==============

Spatial objects and computations in 3D
======================================


.. image:: https://img.shields.io/pypi/v/scikit-spatial.svg
         :target: https://pypi.python.org/pypi/scikit-spatial

.. image:: https://img.shields.io/travis/ajhynes7/scikit-spatial.svg
         :target: https://travis-ci.org/ajhynes7/scikit-spatial

.. image:: https://readthedocs.org/projects/scikit-spatial/badge/?version=latest
         :target: https://scikit-spatial.readthedocs.io/en/latest/?badge=latest
         :alt: Documentation Status

.. image:: https://codecov.io/gh/ajhynes7/scikit-spatial/branch/master/graph/badge.svg
         :target: https://codecov.io/gh/ajhynes7/scikit-spatial

.. image:: https://pyup.io/repos/github/ajhynes7/scikit-spatial/shield.svg
         :target: https://pyup.io/account/repos/github/ajhynes7/scikit-spatial/


This package provides spatial objects in 3D (Point, Vector, Line, and Plane) based on NumPy arrays.
It also includes computations using these objects, such as projecting a point onto a line, or finding the angle between two vectors.


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
>>> round(vector.magnitude, 3)
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


Line
----

A `Line` is defined by a `Point` and a `Vector`. The direction of the line is the unit vector of the input `Vector`.

>>> from skspatial.objects import Line

>>> line_1 = Line(Point([0, 0]), Vector([5, 0]))

>>> line_1
Line(point=Point([0. 0. 0.]), direction=Vector([1. 0. 0.]))


The `Point` and `Vector` inputs are not interchangeable.

>>> Line(Vector([0, 0]), Point([5, 0]))
Traceback (most recent call last):
...
dpcontracts.PreconditionError: the types of arguments must be valid


Alternatively, a `Line` can be defined by two points.

>>> line_2 = Line.from_points(Point([0, 0]), Point([100, 0]))

>>> line_1 == line_2
True

The distance from a `Point` to a `Line` can be found.

>>> line_1.distance_point(Point([20, 75]))
75.0

A `Point` can be projected onto a `Line`, returning a new `Point`.

>>> line_1.project_point(Point([50, 20]))
Point([50.  0.  0.])


Plane
-----

A `Plane` is defined by a `Point` and a `Vector`. The normal vector of the plane is the unit vector of the input `Vector`.

>>> from skspatial.objects import Plane

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
dpcontracts.PreconditionError: the types of arguments must be valid


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
