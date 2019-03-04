"""Classes for the Line and Plane spatial objects."""

from dpcontracts import require, ensure, types

from .array_objects import Point, Vector


class _BaseLinePlane:
    """Private parent class for Line and Plane."""

    @types(point=Point, vector=Vector)
    @require("The vector cannot be the zero vector.", lambda args: not args.vector.is_zero())
    def __init__(self, point, vector):

        self.point = point
        self.vector = vector.unit()

    def __eq__(self, other):

        return vars(self) == vars(other)

    @require("The input must have the same type as the object.", lambda args: isinstance(args.other, type(args.self)))
    def is_close(self, other, **kwargs):

        close_point = self.point.is_close(other.point, **kwargs)
        close_vector = self.vector.is_close(other.vector, **kwargs)

        return close_point and close_vector

    @types(point=Point)
    @ensure("The output must zero or greater.", lambda _, result: result >= 0)
    def distance_point(self, point):
        """Compute the distance from a point to this object."""
        point_projected = self.project_point(point)

        return point.distance_point(point_projected)
