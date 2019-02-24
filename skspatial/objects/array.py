"""Objects based on a single NumPy array (Point and Vector)."""

import numpy as np
from dpcontracts import require, ensure


class _BaseArray3D:
    """Private parent class for Point and Vector classes."""

    @require(
        "The input length must be one to three.",
        lambda args: len(args.arr) in [1, 2, 3],
    )
    @require(
        "The input array must only contain finite numbers.",
        lambda args: np.all(np.isfinite(args.arr)),
    )
    @ensure(
        "The output array must be 3D.", lambda args, result: args.self.array.size == 3
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

    @require("The input must be a point.", lambda args: isinstance(args.other, Point))
    def distance(self, other):
        """Compute the distance from this point to another point."""
        vector = Vector.from_points(self, other)

        return vector.magnitude


class Vector(_BaseArray3D):
    @ensure(
        "The magnitude must be zero or positive.",
        lambda args, result: args.self.magnitude >= 0,
    )
    def __init__(self, arr):

        super().__init__(arr)

        self.magnitude = np.linalg.norm(self.array)

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

    def is_zero(self, **kwargs):
        """
        Check if the vector is the zero vector.

        The zero vector in n dimensions is the vector containing n zeros.

        Parameters
        ----------
        self : Vector
        kwargs : dict, optional
            Additional keywords passed to `np.allclose`.

        Returns
        -------
        bool
            True if vector is the zero vector; false otherwise.

        Examples
        --------
        >>> Vector([0, 0]).is_zero()
        True
        >>> Vector([1, 0]).is_zero()
        False

        >>> Vector([0, 0, 1e-4]).is_zero()
        False
        >>> Vector([0, 0, 1e-4]).is_zero(atol=1e-3)
        True

        """
        return np.allclose(self.array, 0, **kwargs)

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

    @require("The input must be a vector.", lambda args: isinstance(args.other, Vector))
    @ensure(
        "The output must be a vector.", lambda _, result: isinstance(result, Vector)
    )
    def project(self, other):
        """
        Project an other vector onto this vector.

        Parameters
        ----------
        other: Vector

        Returns
        -------
        Vector
            Projection of other vector onto this vector.

        Examples
        --------
        >>> Vector([0, 1]).project(Vector([2, 1]))
        Vector([0. 1. 0.])

        >>> Vector([0, 100]).project(Vector([2, 1]))
        Vector([0. 1. 0.])

        >>> Vector([0, 1]).project(Vector([9, 5]))
        Vector([0. 5. 0.])

        >>> Vector([0, 100]).project(Vector([9, 5]))
        Vector([0. 5. 0.])

        """
        unit_self = self.unit()

        # Scalar projection of other vector onto self.
        scalar_projection = other.dot(unit_self)

        return unit_self.scale(scalar_projection)

    @require("The input must be a vector.", lambda args: isinstance(args.other, Vector))
    def is_perpendicular(self, other, **kwargs):
        """
        Check if an other vector is perpendicular to self.

        Vectors u and v are perpendicular <==> Dot product of u and v is zero.

        Parameters
        ----------
        other: Vector
        kwargs : dict, optional
            Additional keywords passed to `np.isclose`.

        Returns
        -------
        bool
            True if the vector is perpendicular; false otherwise.

        Examples
        --------
        >>> Vector([0, 1]).is_perpendicular(Vector([1, 0]))
        True

        >>> Vector([-1, 5]).is_perpendicular(Vector([3, 4]))
        False

        >>> Vector([2, 0, 0]).is_perpendicular(Vector([0, 0, 2]))
        True

        The zero vector is perpendicular to all vectors.

        >>> Vector([0, 0, 0]).is_perpendicular(Vector([1, 2, 3]))
        True

        """
        return np.isclose(self.dot(other), 0, **kwargs)

    @require("The input must be a vector.", lambda args: isinstance(args.other, Vector))
    def is_parallel(self, other, **kwargs):
        """
        Check if an other vector is parallel to self.

        Two vectors are parallel iff their cross product is the zero vector.

        Parameters
        ----------
        other: Vector
        kwargs : dict, optional
            Additional keywords passed to `np.allclose`.

        Returns
        -------
        bool
            True if the vector is parallel; false otherwise.

        Examples
        --------
        >>> Vector([0, 1]).is_parallel(Vector([1, 0]))
        False

        >>> Vector([-1, 5]).is_parallel(Vector([2, -10]))
        True

        >>> Vector([1, 2, 3]).is_parallel(Vector([3, 6, 9]))
        True

        >>> Vector([0, 0, 0]).is_parallel(Vector([3, 4, -1]))
        True

        >>> Vector([1, 2, 3]).is_parallel(Vector([2, 4, 6]))
        True

        """
        vector_cross = self.cross(other)

        return vector_cross.is_zero(**kwargs)

    @require("The input must be a vector.", lambda args: isinstance(args.other, Vector))
    @ensure("The output must be a float.", lambda _, result: isinstance(result, float))
    def angle_between(self, other):
        """
        Return the angle in radians between this vector and another.

        Parameters
        ----------
        other : Vector

        Returns
        -------
        float
            Angle between vectors.

        Examples
        --------
        >>> Vector([1, 0]).angle_between(Vector([1, 0]))
        0.0

        >>> Vector([1, 1, 1]).angle_between(Vector([1, 1, 1]))
        0.0

        >>> angle = Vector([1, 0]).angle_between(Vector([1, 1]))
        >>> round(np.degrees(angle))
        45.0

        >>> angle = Vector([1, 0]).angle_between(Vector([-2, 0]))
        >>> round(np.degrees(angle))
        180.0

        """
        cos_theta = self.dot(other) / (self.magnitude * other.magnitude)

        # Ensure that input to arccos is in range [-1, 1] so that output is real.
        cos_theta = np.clip(cos_theta, -1, 1)

        return np.arccos(cos_theta)
