import numpy as np
from dpcontracts import require, ensure
from numpy.linalg import norm


class _BaseArray3D:
    """Private parent class for Point and Vector classes."""

    @require(
        "The input length must one to three.", lambda args: len(args.arr) in [1, 2, 3]
    )
    def __init__(self, arr):
        """Convert the array to 3D by appending zeros."""
        n_dimensions = len(arr)
        array_padding = np.zeros(3 - n_dimensions)

        self.array = np.concatenate((np.array(arr), array_padding))

    def __eq__(self, other):

        return type(self) == type(other) and np.all(self.array == other.array)

    def is_close(self, other, **kwargs):
        """Check if array is close to another array."""
        return np.allclose(self.array, other.array, **kwargs)


class Point(_BaseArray3D):
    def __init__(self, arr):

        super().__init__(arr)

    def __repr__(self):

        return f"Point({self.array})"

    @require("The input must be a vector.", lambda args: isinstance(args.other, Vector))
    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    def add(self, other):

        return Point(self.array + other.array)


class Vector(_BaseArray3D):
    def __init__(self, arr):

        super().__init__(arr)

        self.magnitude = norm(self.array)

    def __repr__(self):

        return f"Vector({self.array})"

    def __eq__(self, other):

        return type(self) == type(other) and np.all(self.array == other.array)

    @ensure(
        "The output must be a vector with a magnitude of one.",
        lambda _, result: isinstance(result, Vector)
        and np.isclose(result.magnitude, 1),
    )
    def unit(self):

        return Vector(self.array / self.magnitude)

    @classmethod
    @require(
        "The inputs must be two points.",
        lambda args: isinstance(args.point_a, Point)
        and isinstance(args.point_b, Point),
    )
    @ensure(
        "The output must be a vector." "", lambda _, result: isinstance(result, Vector)
    )
    def from_points(cls, point_a, point_b):
        """
        Define a vector from two points.

        The vector is from point A to point B.
        """
        return cls(point_b.array - point_a.array)

    @require(
        "The inputs must be two vectors.",
        lambda args: all(isinstance(x, Vector) for x in args),
    )
    @ensure(
        "The output must be a number.", lambda _, result: isinstance(result, np.number)
    )
    def dot(self, other):

        return np.dot(self.array, other.array)

    def cross(self, other):

        return np.cross(self.array, other.array)
