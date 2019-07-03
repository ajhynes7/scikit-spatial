"""Module for base class of Circle and Sphere."""

import numpy as np

from skspatial.objects._base_composite import _BaseComposite
from skspatial.objects.point import Point
from skspatial.objects.vector import Vector


class _BaseSphere(_BaseComposite):
    """Private parent class for Circle and Sphere."""

    def __init__(self, point, radius):

        if radius <= 0:
            raise ValueError("The radius must be positive.")

        self.point = Point(point)
        self.radius = radius

        self.dimension = self.point.dimension

    def __repr__(self):

        name_class = type(self).__name__

        repr_point = np.array_repr(self.point)

        return f"{name_class}(point={repr_point}, radius={self.radius})"

    def project_point(self, point):
        """
        Project a point onto the surface of the circle or sphere.

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
        array([0.707, 0.707])

        >>> circle.project_point([-6, 3]).round(3)
        array([-0.894,  0.447])

        >>> circle.project_point([0, 0])
        Traceback (most recent call last):
        ...
        ValueError: The point must not be the center of the circle or sphere.

        >>> from skspatial.objects import Sphere

        >>> Sphere([0, 0, 0], 2).project_point([1, 2, 3]).round(3)
        array([0.535, 1.069, 1.604])

        """
        if self.point.is_equal(point):
            raise ValueError(
                "The point must not be the center of the circle or sphere."
            )

        vector_to_point = Vector.from_points(self.point, point)

        return self.point + self.radius * vector_to_point.unit()
