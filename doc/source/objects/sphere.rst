
Sphere
------

A :class:`~skspatial.objects.Sphere` object is defined by a 3D point and a radius. The point is the center of the sphere.

>>> from skspatial.objects import Sphere

>>> sphere = Sphere([0, 0, 0], 1)

>>> sphere
Sphere(point=Point([0, 0, 0]), radius=1)


The surface area and volume of the sphere can be calculated.

>>> sphere.surface_area().round(3)
12.566

>>> sphere.volume().round(3)
4.189


An error is raised if the point is not 2D.

>>> Sphere([0, 0], 1)
Traceback (most recent call last):
...
ValueError: The point must be 3D.
