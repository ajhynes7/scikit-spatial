"""Objects based on a single NumPy array (Point and Vector)."""

import numpy as np
from dpcontracts import require, ensure
from numpy.linalg import norm


class _BaseArray3D:
    """Private parent class for Point and Vector classes."""

    @require(
        "The input length must be one to three.",
        lambda args: len(args.arr) in [1, 2, 3],
    )
    def __init__(self, arr):
        """Convert the array to 3D by appending zeros."""
        n_dimensions = len(arr)
        array_padding = np.zeros(3 - n_dimensions)

        self.array = np.concatenate((np.array(arr), array_padding))

    def __eq__(self, other):

        return isinstance(self, type(other)) and np.all(self.array == other.array)

    @require(
        "The input must have the same type as the object.",
        lambda args: isinstance(args.self, type(args.other)),
    )
    def is_close(self, other, **kwargs):
        """Check if array is close to another array."""
        return np.allclose(self.array, other.array, **kwargs)


class Point(_BaseArray3D):
    def __init__(self, arr):

        super().__init__(arr)

    def __repr__(self):

        return f"Point({self.array})"

    @require(
        "The input must be a vector.", lambda args: isinstance(args.vector, Vector)
    )
    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    def add(self, vector):
        """Return a new point by adding a vector."""
        return Point(self.array + vector.array)

    @require(
        "The input must be a vector.", lambda args: isinstance(args.vector, Vector)
    )
    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    def subtract(self, vector):
        """Return a new point by subtracting a vector."""
        return self.add(vector.reverse())


class Vector(_BaseArray3D):
    def __init__(self, arr):

        super().__init__(arr)

        self.magnitude = norm(self.array)

    def __repr__(self):

        return f"Vector({self.array})"

    @classmethod
    @require(
        "The inputs must be two points.",
        lambda args: all(isinstance(x, Point) for x in [args.point_a, args.point_b]),
    )
    @ensure(
        "The output must be a vector.", lambda _, result: isinstance(result, Vector)
    )
    def from_points(cls, point_a, point_b):
        """Instantiate the vector from point A to point B."""
        return cls(point_b.array - point_a.array)

    @ensure(
        "The output must be a vector.", lambda _, result: isinstance(result, Vector)
    )
    def reverse(self):
        """Return the vector with the same magnitude in the opposite direction."""
        return Vector(-self.array)

    @ensure(
        "The output must be a vector.", lambda _, result: isinstance(result, Vector)
    )
    def scale(self, scalar):
        """Return the result of scaling the vector."""
        return Vector(scalar * self.array)

    @ensure(
        "The output must be a vector with a magnitude of one.",
        lambda _, result: isinstance(result, Vector)
        and np.isclose(result.magnitude, 1),
    )
    def unit(self):
        """Return the unit vector of this vector."""
        return self.scale(1 / self.magnitude)

    @require("The input must be a vector.", lambda args: isinstance(args.other, Vector))
    @ensure(
        "The output must be a vector.", lambda _, result: isinstance(result, Vector)
    )
    def add(self, other):
        """Add an other vector to this vector."""
        return Vector(self.array + other.array)

    @require("The input must be a vector.", lambda args: isinstance(args.other, Vector))
    @ensure(
        "The output must be a vector.", lambda _, result: isinstance(result, Vector)
    )
    def subtract(self, other):
        """Subtract an other vector from this vector."""
        return self.add(other.reverse())

    @require("The input must be a vector.", lambda args: isinstance(args.other, Vector))
    @ensure("The output must be a float.", lambda _, result: isinstance(result, float))
    def dot(self, other):
        """Compute the dot product with another vector."""
        return np.dot(self.array, other.array)

    @require("The input must be a vector.", lambda args: isinstance(args.other, Vector))
    @ensure(
        "The output must be a vector with the same dimension as the input.",
        lambda args, result: isinstance(result, Vector)
        and result.array.size == args.other.array.size,
    )
    def cross(self, other):
        """Compute the cross product with another vector."""
        return Vector(np.cross(self.array, other.array))
