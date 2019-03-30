"""Classes for the Line and Plane spatial objects."""

import inspect
from copy import deepcopy

import numpy as np
from dpcontracts import require, ensure

from skspatial.objects.point import Point
from skspatial.objects.vector import Vector


class _BaseLinePlane:
    """Private parent class for Line and Plane."""

    @require("The inputs must have the same length.", lambda args: len(args.point) == len(args.vector))
    @require("The vector cannot be the zero vector.", lambda args: not Vector(args.vector).is_zero())
    @ensure("The point must be a Point.", lambda args, _: isinstance(args.self.point, Point))
    @ensure("The vector must be a Vector", lambda args, _: isinstance(args.self.vector, Vector))
    def __init__(self, point, vector):

        self.point = Point(point)
        self.vector = Vector(vector)

    def __repr__(self):

        name_class = type(self).__name__
        name_vector = inspect.getfullargspec(type(self)).args[-1]

        repr_point = np.array_repr(self.point)
        repr_vector = np.array_repr(self.vector)

        return "{}(point={}, {}={})".format(name_class, repr_point, name_vector, repr_vector)

    def __getitem__(self, name_item):

        return getattr(self, name_item)

    def __setitem__(self, name_item, value):

        return setattr(self, name_item, value)

    def get_dimension(self):

        return self.point.get_dimension()

    def set_dimension(self, dim):

        obj_new = deepcopy(self)

        for name_item in vars(self):
            obj_new[name_item] = self[name_item].set_dimension(dim)

        return obj_new

    @require("The input must have the same type as the object.", lambda args: isinstance(args.other, type(args.self)))
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

        """
        contains_point = self.contains_point(other.point, **kwargs)
        is_parallel = self.vector.is_parallel(other.vector, **kwargs)

        return contains_point and is_parallel

    @ensure("The output must zero or greater.", lambda _, result: result >= 0)
    @ensure("The output must be a NumPy scalar.", lambda _, result: isinstance(result, np.number))
    def distance_point(self, point):
        """Compute the distance from a point to this object."""
        point_projected = self.project_point(point)

        return point_projected.distance_point(point)

    def contains_point(self, point, **kwargs):
        """Check if this spatial object contains a point."""
        distance = self.distance_point(point)

        return np.isclose(distance, 0, **kwargs)

    @ensure("The output must be zero or greater.", lambda _, result: result >= 0)
    def sum_squares(self, points):

        distances_squared = np.apply_along_axis(self.distance_point, 1, points) ** 2

        return distances_squared.sum()
