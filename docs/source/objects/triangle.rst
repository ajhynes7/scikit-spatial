
Triangle
--------

A :class:`~skspatial.objects.Triangle` object is defined by three points.

>>> from skspatial.objects import Triangle

>>> triangle = Triangle([0, 0], [1, 0], [0, 1])

>>> triangle
Triangle(point_a=Point([0, 0]), point_b=Point([1, 0]), point_c=Point([0, 1]))


The triangle can be classified as equilateral, isosceles, or scalene.

>>> triangle.classify()
'isosceles'

You can also check if it's a right triangle.

>>> triangle.is_right()
True


Parametrized methods
~~~~~~~~~~~~~~~~~~~~

Several methods are parametrized to specify a side or vertex of the triangle. For example, the `angle` method is passed a character 'A', 'B', or 'C' to denote the vertex. The angle is returned in radians.

>>> triangle.angle('A').round(3)
1.571

Because this is a common pattern for the triangle, a `multiple` method is provided to make multiple calls of the same method, such as 'angle'. This library uses the convention of vertex 'A' being across from side 'a', vertex 'B' being across from side 'b', etc.

>>> [x.round(3) for x in triangle.multiple('angle', 'ABC')]
[1.571, 0.785, 0.785]

The following line returns the three lengths of the triangle.

>>> [x.round(3) for x in triangle.multiple('length', 'abc')]
[1.414, 1.0, 1.0]


Other spatial objects
~~~~~~~~~~~~~~~~~~~~~

Some triangle methods return other spatial objects.

>>> triangle.normal()
Vector([0, 0, 1])

>>> triangle.altitude('A')
Line(point=Point([0, 0]), direction=Vector([0.5, 0.5]))

>>> triangle.orthocenter()
Point([0., 0.])
