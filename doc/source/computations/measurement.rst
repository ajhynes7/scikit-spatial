
Measurement
===========


Vector-Vector Angle
-------------------

Measure the angle between two vectors.
The angle is returned in radians.

>>> import numpy as np
>>> from skspatial.objects import Vector

>>> vector = Vector([1, 0, 0])

>>> angle = vector.angle_between([0, 0, 1])
>>> np.degrees(angle).round()
90.0

>>> angle = Vector([1, 5]).angle_between([-2, 1])
>>> np.degrees(angle).round()
75.0


Point-Point Distance
--------------------

Measure the distance between two points.

>>> from skspatial.objects import Point

>>> point = Point([1, 0, 0])
>>> point.distance_point([0, 0, 1]).round(3)
1.414


Point-Line Distance
--------------------

Measure the distance from a point to a line.

>>> from skspatial.objects import Line

>>> line = Line(point=[1, 2, 0], direction=[2, 4, 1])

>>> line.distance_point([9, -3, -2]).round(3)
9.554


Point-Plane Distance
--------------------

Measure the distance from a point to a plane.

>>> from skspatial.objects import Plane

>>> point = [5, 7, -2]
>>> plane = Plane(point=[0, 0, 0], normal=[0, 0, 1])

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

>>> line_a = Line([1, 2], [4, 3])
>>> line_b = Line([-4, 1], [7, 23])

>>> line_a.distance_line(line_b)
0.0

2. The lines are parallel.

>>> line_a = Line([0, 0], [1, 0])
>>> line_b = Line([0, 5], [-1, 0])

>>> line_a.distance_line(line_b)
5.0

3. The lines are skew.

>>> line_a = Line([0, 0, 0], [1, 0, 1])
>>> line_b = Line([1, 0, 0], [1, 1, 1])

>>> line_a.distance_line(line_b).round(3)
0.707


Area of Triangle
----------------

Measure the area of a triangle defined by three points.
The points are the vertices of the triangle.

>>> from skspatial.measurement import area_triangle

>>> area_triangle([0, 0], [2, 0], [1, 1])
1.0

>>> area = area_triangle([3, -5, 1], [5, 2, 1], [9, 4, 2])
>>> area.round(2)
12.54


Volume of Tetrahedron
---------------------

Measure the area of a tetrahedron defined by four points.
The points are the vertices of the tetrahedron.

>>> from skspatial.measurement import volume_tetrahedron

>>> volume_tetrahedron([0, 0], [1, 0], [0, 1], [1, 1])
0.0

>>> volume = volume_tetrahedron([0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1])
>>> volume.round(3)
0.167
