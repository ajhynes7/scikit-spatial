Cylinder
--------

A :class:`~skspatial.objects.Cylinder` object is defined by a point, a vector, and a radius.

The point is the centre of the cylinder base. The vector is normal to the base, and the length of the cylinder is the length of this vector.
The point and vector must be 3D.

>>> from skspatial.objects import Cylinder

>>> cylinder = Cylinder(point=[0, 0, 0], vector=[0, 0, 5], radius=1)

>>> cylinder
Cylinder(point=Point([0, 0, 0]), vector=Vector([0, 0, 5]), radius=1)

>>> cylinder.length()
5.0

>>> cylinder.volume().round(3)
15.708

You can check if a point is inside (or on the surface of) the cylinder.

>>> cylinder.is_point_within([0, 0, 0])
True
>>> cylinder.is_point_within([0, 0, 5])
True
>>> cylinder.is_point_within([1, 0, 3])
True
>>> cylinder.is_point_within([2, 0, 3])
False
