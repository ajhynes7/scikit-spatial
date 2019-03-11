"""Classes for the Line and Plane spatial objects."""

import numpy as np
from dpcontracts import require, ensure

from skspatial.objects.point import Point
from skspatial.objects.vector import Vector


class _BaseLinePlane:
    """Private parent class for Line and Plane."""

    @require("The vector cannot be the zero vector.", lambda args: not Vector(args.vector).is_zero())
    @ensure("The point is a Point.", lambda args, _: isinstance(args.self.point, Point))
    @ensure("The vector is a Vector", lambda args, _: isinstance(args.self.vector, Vector))
    def __init__(self, point=[0, 0, 0], vector=[1, 0, 0]):

        self.point = Point(point)
        self.vector = Vector(vector).unit()

    def __repr__(self):

        name_class = type(self).__name__

        repr_point = np.array_repr(self.point)
        repr_vector = np.array_repr(self.vector)

        return f"{name_class}(point={repr_point}, normal={repr_vector})"

    @require("The input must have the same type as the object.", lambda args: isinstance(args.other, type(args.self)))
    def is_close(self, other, **kwargs):

        close_point = self.point.is_close(other.point, **kwargs)
        close_vector = self.vector.is_close(other.vector, **kwargs)

        return close_point and close_vector

    @ensure("The output must zero or greater.", lambda _, result: result >= 0)
    @ensure("The output must be a numpy scalar.", lambda _, result: isinstance(result, np.number))
    def distance_point(self, point):
        """Compute the distance from a point to this object."""
        point_projected = self.project_point(point)

        return point.distance_point(point_projected)
