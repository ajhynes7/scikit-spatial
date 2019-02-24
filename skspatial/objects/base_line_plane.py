
from dpcontracts import require, ensure

from .array import Point, Vector


class _BaseLinePlane:
    """Private parent class for Line and Plane."""

    @require(
        "The inputs must be a point and a vector.",
        lambda args: isinstance(args.point, Point) and isinstance(args.vector, Vector),
    )
    def __init__(self, point, vector):

        self.point = point
        self.vector = vector.unit()

    def __eq__(self, other):

        return vars(self) == vars(other)

    @require(
        "The input must have the same type as the object.",
        lambda args: isinstance(args.other, type(args.self)),
    )
    def is_close(self, other, **kwargs):

        close_point = self.point.is_close(other.point, **kwargs)
        close_vector = self.vector.is_close(other.vector, **kwargs)

        return close_point and close_vector

    def distance(self, point):
        """Compute the distance from a point to this object."""
        point_projected = self.project(point)

        return point.distance(point_projected)

