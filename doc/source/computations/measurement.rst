
Measurement
===========


Vector-Vector Angle
-------------------

Measure the angle between two vectors.
The angle is returned in radians.

>>> import numpy as np
>>> from skspatial.objects import Vector

>>> vector_a = Vector([1, 0, 0])
>>> vector_b = Vector([0, 0, 1])

>>> angle = vector_a.angle_between(vector_b)
>>> np.degrees(angle).round()
90.0

>>> vector_a = Vector([1, 5])
>>> vector_b = Vector([-2, 1])

>>> angle = vector_a.angle_between(vector_b)
>>> np.degrees(angle).round()
75.0


Point-Point Distance
--------------------

Measure the distance between two points.

>>> from skspatial.objects import Point

>>> point_a = Point([1, 0, 0])
>>> point_b = Point([0, 0, 1])

>>> point_a.distance_point(point_b).round(3)
1.414


Point-Line Distance
--------------------

Measure the distance from a point to a line.

>>> from skspatial.objects import Line

>>> line = Line(Point([1, 2, 0]), Vector([2, 4, 1]))
>>> point = Point([9, -3, -2])

>>> line.distance_point(point).round(3)
9.554


Point-Plane Distance
--------------------

Measure the distance from a point to a plane.

>>> from skspatial.objects import Plane

>>> plane = Plane(Point([0, 0]), Vector([0, 0, 1]))
>>> plane.distance_point(point)
2.0

Measure the signed distance from a point to a plane.

>>> plane.distance_point_signed(point)
-2.0


Line-Line Distance
------------------

Measure the distance between two lines.

There are three cases:

1. The lines intersect (i.e., they are coplanar and not parallel)

>>> line_a = Line(Point([1, 2]), Vector([4, 3]))
>>> line_b = Line(Point([-4, 1]), Vector([7, 23]))

>>> line_a.distance_line(line_b)
0.0

2. The lines are parallel.

>>> line_a = Line(Point([0, 0]), Vector([1, 0]))
>>> line_b = Line(Point([0, 5]), Vector([-1, 0]))

>>> line_a.distance_line(line_b)
5.0

3. The lines are skew.

>>> line_a = Line(Point([0, 0, 0]), Vector([1, 0, 1]))
>>> line_b = Line(Point([1, 0, 0]), Vector([1, 1, 1]))

>>> line_a.distance_line(line_b).round(3)
0.707


Area of Triangle
----------------

Measure the area of a triangle defined by three points.
The points are the vertices of the triangle.

>>> from skspatial.measurement import area_triangle

>>> point_a = Point([0, 0])
>>> point_b = Point([2, 0])
>>> point_c = Point([1, 1])

>>> area_triangle(point_a, point_b, point_c)
1.0

>>> point_a = Point([3, -5, 1])
>>> point_b = Point([5, 2, 1])
>>> point_c = Point([9, 4, 2])

>>> area = area_triangle(point_a, point_b, point_c)
>>> area.round(2)
12.54


Volume of Tetrahedron
---------------------

Measure the area of a tetrahedron defined by four points.
The points are the vertices of the tetrahedron.

>>> from skspatial.measurement import volume_tetrahedron

>>> point_a = Point([0, 0])
>>> point_b = Point([1, 0])
>>> point_c = Point([0, 1])
>>> point_d = Point([1, 1])

>>> volume_tetrahedron(point_a, point_b, point_c, point_d)
0.0

>>> point_a = Point([0, 0])
>>> point_b = Point([1, 0])
>>> point_c = Point([0, 1])
>>> point_d = Point([0, 0, 1])

>>> volume = volume_tetrahedron(point_a, point_b, point_c, point_d)
>>> volume.round(3)
0.167
