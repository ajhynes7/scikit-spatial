
Plane
-----

A :class:`~skspatial.objects.Plane` object is defined by a point and a normal vector.

>>> from skspatial.objects import Plane

>>> plane_1 = Plane(point=[0, 0, 0], normal=[0, 0, 23])

>>> plane_1
Plane(point=Point([0, 0, 0]), normal=Vector([ 0,  0, 23]))

Alternatively, a plane can be defined by three points.

>>> point_a, point_b, point_c = [0, 0], [10, -2], [50, 500]
>>> plane_2 = Plane.from_points(point_a, point_b, point_c)

>>> plane_2
Plane(point=Point([0, 0, 0]), normal=Vector([   0,    0, 5100]))

>>> plane_1.is_close(plane_2)
True

Changing the order of the points can reverse the direction of the normal vector.

>>> plane_3 = Plane.from_points(point_a, point_c, point_b)

>>> plane_3
Plane(point=Point([0, 0, 0]), normal=Vector([    0,     0, -5100]))

The planes will still be equal.

>>> plane_1.is_close(plane_3)
True
