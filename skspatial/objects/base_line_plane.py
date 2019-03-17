"""Classes for the Line and Plane spatial objects."""

import inspect

import numpy as np
from dpcontracts import require, ensure

from skspatial.objects.point import Point
from skspatial.objects.vector import Vector


class _BaseLinePlane:
    """Private parent class for Line and Plane."""

    @require("The vector cannot be the zero vector.", lambda args: not Vector(args.vector).is_zero())
    @ensure("The point is a Point.", lambda args, _: isinstance(args.self.point, Point))
    @ensure("The vector is a Vector", lambda args, _: isinstance(args.self.vector, Vector))
    def __init__(self, point, vector):

        # Ensure that the point and vector have the same length.
        point, vector = Point.normalize_dimensions(point, vector)

        self.point = Point(point)
        self.vector = Vector(vector).unit()

    def __repr__(self):

        name_class = type(self).__name__
        name_vector = inspect.getfullargspec(type(self)).args[-1]

        repr_point = np.array_repr(self.point)
        repr_vector = np.array_repr(self.vector)

        return f"{name_class}(point={repr_point}, {name_vector}={repr_vector})"

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

        >>> plane_a = Plane(point=[0, 0], normal=[0, 0, 5])
        >>> plane_b = Plane(point=[23, 45], normal=[0, 0, -20])
        >>> plane_a.is_close(plane_b)
        True

        """
        contains_point = self.contains_point(other.point, **kwargs)
        is_parallel = self.vector.is_parallel(other.vector, **kwargs)

        return contains_point and is_parallel

    @ensure("The output must zero or greater.", lambda _, result: result >= 0)
    @ensure("The output must be a numpy scalar.", lambda _, result: isinstance(result, np.number))
    def distance_point(self, point):
        """Compute the distance from a point to this object."""
        point_projected = self.project_point(point)

        return point_projected.distance_point(point)
