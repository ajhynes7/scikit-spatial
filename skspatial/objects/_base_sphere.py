"""Module for base class of Circle and Sphere."""

import numpy as np

from skspatial.objects._base_composite import _BaseComposite
from skspatial.objects.point import Point
from skspatial.objects.vector import Vector


class _BaseSphere(_BaseComposite):
    """Private parent class for Circle and Sphere."""

    def __init__(self, point, radius):

        if radius <= 0:
            raise ValueError("The radius must be greater than zero.")

        self.point = Point(point)
        self.radius = radius

        self.dimension = self.point.dimension

    def __repr__(self):

        name_class = type(self).__name__

        repr_point = np.array_repr(self.point)

        return f"{name_class}(point={repr_point}, radius={self.radius})"

    def diameter(self):

        return 2 * self.radius

    def circumference(self):

        return 2 * np.pi * self.radius

    def project_point(self, point):

        vector_to_point = Vector.from_points(self.point, point)

        return self.point + self.radius * vector_to_point.unit()
