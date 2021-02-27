"""Module for base class of Circle and Sphere."""
import numpy as np

from skspatial._functions import _contains_point
from skspatial.objects._base_spatial import _BaseSpatial
from skspatial.objects.point import Point
from skspatial.objects.vector import Vector
from skspatial.typing import array_like


class _BaseSphere(_BaseSpatial):
    """Private parent class for Circle and Sphere."""

    def __init__(self, point: array_like, radius: float):

        if radius <= 0:
            raise ValueError("The radius must be positive.")

        self.point = Point(point)
        self.radius = radius

        self.dimension = self.point.dimension

    def __repr__(self) -> str:

        name_class = type(self).__name__

        repr_point = np.array_repr(self.point)

        return f"{name_class}(point={repr_point}, radius={self.radius})"

    def distance_point(self, point: array_like) -> np.float64:
        """Return the distance from a point to the circle/sphere."""
        distance_to_center = self.point.distance_point(point)

        return abs(distance_to_center - self.radius)

    def contains_point(self, point: array_like, **kwargs: float) -> bool:
        """Check if the circle/sphere contains a point."""
        return _contains_point(self, point, **kwargs)

    def project_point(self, point: array_like) -> Point:
        """
        Project a point onto the circle or sphere.

        Parameters
        ----------
        point : array_like
            Input point.

        Returns
        -------
        Point
            Point projected onto the circle or sphere.

        Raises
        ------
        ValueError
            If the input point is the center of the circle or sphere.

        Examples
        --------
        >>> from skspatial.objects import Circle

        >>> circle = Circle([0, 0], 1)

        >>> circle.project_point([1, 1]).round(3)
        Point([0.707, 0.707])

        >>> circle.project_point([-6, 3]).round(3)
        Point([-0.894,  0.447])

        >>> circle.project_point([0, 0])
        Traceback (most recent call last):
        ...
        ValueError: The point must not be the center of the circle or sphere.

        >>> from skspatial.objects import Sphere

        >>> Sphere([0, 0, 0], 2).project_point([1, 2, 3]).round(3)
        Point([0.535, 1.069, 1.604])

        """
        if self.point.is_equal(point):
            raise ValueError("The point must not be the center of the circle or sphere.")

        vector_to_point = Vector.from_points(self.point, point)

        return self.point + self.radius * vector_to_point.unit()
