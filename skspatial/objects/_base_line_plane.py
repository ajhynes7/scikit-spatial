"""Classes for the Line and Plane spatial objects."""

import inspect
from copy import deepcopy

import numpy as np

from skspatial.objects._base_array import _BaseArray1D
from skspatial.objects.point import Point
from skspatial.objects.vector import Vector


class _BaseLinePlane:
    """Private parent class for Line and Plane."""

    def __init__(self, point, vector):

        self.point = Point(point)
        self.vector = Vector(vector)

        if self.point.dimension != self.vector.dimension:
            raise ValueError("The point and vector must have the same dimension.")

        if self.vector.is_zero(atol=0, rtol=0):
            raise ValueError("The vector must not be the zero vector.")

        self.dimension = self.point.dimension

    def __repr__(self):

        name_class = type(self).__name__
        name_vector = inspect.getfullargspec(type(self)).args[-1]

        repr_point = np.array_repr(self.point)
        repr_vector = np.array_repr(self.vector)

        return "{}(point={}, {}={})".format(
            name_class, repr_point, name_vector, repr_vector
        )

    def __getitem__(self, name_item):

        return getattr(self, name_item)

    def __setitem__(self, name_item, value):

        return setattr(self, name_item, value)

    def set_dimension(self, dim):

        obj_new = deepcopy(self)

        for name_item in vars(self):

            attribute = self[name_item]

            if isinstance(attribute, _BaseArray1D):
                obj_new[name_item] = attribute.set_dimension(dim)

        return obj_new

    def is_close(self, other, **kwargs):
        """
        Check if line/plane is almost equivalent to another line/plane.

        The points must be close and the vectors must be parallel.

        Parameters
        ----------
        other : object
             Line or Plane.

        Returns
        -------
        bool
            True if the objects are almost equivalent; false otherwise.

        Raises
        ------
        ValueError
            If the input doesn't have the same type as the object.

        Examples
        --------
        >>> from skspatial.objects import Line, Plane

        >>> line_a = Line(point=[0, 0], direction=[1, 0])
        >>> line_b = Line(point=[0, 0], direction=[-2, 0])
        >>> line_a.is_close(line_b)
        True

        >>> line_b = Line(point=[50, 0], direction=[-4, 0])
        >>> line_a.is_close(line_b)
        True

        >>> line_b = Line(point=[50, 29], direction=[-4, 0])
        >>> line_a.is_close(line_b)
        False

        >>> plane_a = Plane(point=[0, 0, 0], normal=[0, 0, 5])
        >>> plane_b = Plane(point=[23, 45, 0], normal=[0, 0, -20])
        >>> plane_a.is_close(plane_b)
        True

        >>> line_a.is_close(plane_a)
        Traceback (most recent call last):
        ...
        ValueError: The input must have the same type as the object.

        """
        if not isinstance(other, type(self)):
            raise ValueError("The input must have the same type as the object.")

        contains_point = self.contains_point(other.point, **kwargs)
        is_parallel = self.vector.is_parallel(other.vector, **kwargs)

        return contains_point and is_parallel

    def distance_point(self, point):
        """Compute the distance from a point to this object."""
        point_projected = self.project_point(point)

        return point_projected.distance_point(point)

    def contains_point(self, point, **kwargs):
        """Check if this spatial object contains a point."""
        distance = self.distance_point(point)

        return np.isclose(distance, 0, **kwargs)

    def sum_squares(self, points):

        distances_squared = np.apply_along_axis(self.distance_point, 1, points) ** 2

        return distances_squared.sum()
