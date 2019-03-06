
Plane
-----

A `Plane` is defined by a `Point` and a `Vector`. The normal vector of the plane is the unit vector of the input `Vector`.

>>> from skspatial.objects import Point, Vector, Plane

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

