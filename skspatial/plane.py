import numpy as np
from dpcontracts import require, ensure

from .array import Point, Vector
from .properties import are_collinear


class Plane:
    @require(
        "The inputs must be a point and a vector.",
        lambda args: isinstance(args.point, Point) and isinstance(args.normal, Vector),
    )
    def __init__(self, point, normal):

        self.point = point
        self.normal = normal.unit()

    def __repr__(self):

        return f"Plane(point={self.point}, normal={self.normal})"

    @classmethod
    @require(
        "The inputs must be three points.",
        lambda args: all(isinstance(x, Point) for x in args[1:]),
    )
    @require(
        "The points must all be different.",
        lambda args: args.point_a != args.point_b != args.point_c,
    )
    @require(
        "The points must not be collinear.",
        lambda args: not are_collinear(args.point_a, args.point_b, args.point_c),
    )
    @ensure(
        "The output must be a plane." "", lambda _, result: isinstance(result, Plane)
    )
    def from_points(cls, point_a, point_b, point_c):
        """Define a plane from three 3D points."""
        vector_ab = Vector.from_points(point_a, point_b)
        vector_ac = Vector.from_points(point_a, point_c)

        vector_normal = Vector(np.cross(vector_ab.array, vector_ac.array))

        return cls(point_a, vector_normal)
