import numpy as np
from dpcontracts import require, ensure

from skspatial.constants import ATOL
from .base_array import _BaseArray1D


class Vector(_BaseArray1D):
    """Vector implemented as an ndarray subclass."""

    @ensure("The magnitude must be zero or greater", lambda _, result: result.magnitude >= 0)
    def __new__(cls, array_like):

        obj = super().__new__(cls, array_like)

        # Add the new attribute to the created instance.
        obj.magnitude = np.linalg.norm(obj)

        return obj

    def __array_finalize__(self, obj):

        self.magnitude = getattr(obj, 'magnitude', None)

    @classmethod
    @ensure("The output must be a vector.", lambda _, result: isinstance(result, Vector))
    def from_points(cls, point_a, point_b):
        """
        Instantiate a vector from point A to point B.

        Parameters
        ----------
        point_a : array_like
            Input point A.
        point_b : array_like
            Input point B.

        Returns
        -------
        Vector
            Vector from point A to point B.

        Examples
        --------
        >>> from skspatial.objects import Vector

        >>> Vector.from_points([0, 0], [1, 0])
        Vector([1., 0., 0.])

        >>> Vector.from_points([5, 2], [-2, 8])
        Vector([-7.,  6.,  0.])

        >>> Vector.from_points([3, 1, 1], [7, 7, 0])
        Vector([ 4.,  6., -1.])

        """
        return cls(Vector(point_b) - Vector(point_a))

    @require("The vector cannot be the zero vector.", lambda args: not args.self.is_zero())
    @ensure("The output must be a vector.", lambda _, result: isinstance(result, Vector))
    @ensure("The output must have a magnitude of one.", lambda _, result: np.isclose(result.magnitude, 1))
    def unit(self):
        """Return the unit vector of this vector."""
        return Vector(self / self.magnitude)

    def is_zero(self, **kwargs):
        """
        Check if the vector is the zero vector.

        The zero vector in n dimensions is the vector containing n zeros.

        Parameters
        ----------
        kwargs : dict, optional
            Additional keywords passed to `np.allclose`.

        Returns
        -------
        bool
            True if vector is the zero vector; false otherwise.

        Examples
        --------
        >>> from skspatial.objects import Vector

        >>> Vector([0, 0]).is_zero()
        True
        >>> Vector([1, 0]).is_zero()
        False

        >>> Vector([0, 0, 1e-4]).is_zero()
        False
        >>> Vector([0, 0, 1e-4]).is_zero(atol=1e-3)
        True

        """
        return np.allclose(self, 0, **kwargs)

    @ensure("The output must be a vector.", lambda _, result: isinstance(result, Vector))
    def add(self, other):
        """Add a vector."""
        return self + Vector(other)

    @ensure("The output must be a vector.", lambda _, result: isinstance(result, Vector))
    def subtract(self, other):
        """Subtract a vector."""
        return self - Vector(other)

    @ensure("The output must be a vector.", lambda _, result: isinstance(result, Vector))
    def cross(self, other):
        """Compute the cross product with another vector."""
        return Vector(np.cross(self, Vector(other)))

    def is_perpendicular(self, other, **kwargs):
        """
        Check if an other vector is perpendicular to self.

        Vectors u and v are perpendicular <==> Dot product of u and v is zero.

        Parameters
        ----------
        other : array_like
            Input vector.
        kwargs : dict, optional
            Additional keywords passed to `np.isclose`.

        Returns
        -------
        bool
            True if the vector is perpendicular; false otherwise.

        Examples
        --------
        >>> from skspatial.objects import Vector

        >>> Vector([0, 1]).is_perpendicular([1, 0])
        True

        >>> Vector([-1, 5]).is_perpendicular([3, 4])
        False

        >>> Vector([2, 0, 0]).is_perpendicular([0, 0, 2])
        True

        The zero vector is perpendicular to all vectors.

        >>> Vector([0, 0, 0]).is_perpendicular([1, 2, 3])
        True

        """
        return np.isclose(self.dot(other), 0, **kwargs)

    def is_parallel(self, other, **kwargs):
        """
        Check if an other vector is parallel to self.

        Two vectors are parallel iff their cross product is the zero vector.

        Parameters
        ----------
        other : array_like
            Input vector.
        kwargs : dict, optional
            Additional keywords passed to `np.isclose`.

        Returns
        -------
        bool
            True if the vector is parallel; false otherwise.

        Examples
        --------
        >>> from skspatial.objects import Vector

        >>> Vector([0, 1]).is_parallel([1, 0])
        False

        >>> Vector([-1, 5]).is_parallel([2, -10])
        True

        >>> Vector([1, 2, 3]).is_parallel([3, 6, 9])
        True

        >>> Vector([1, 2, 3, 4]).is_parallel([-2, -4, -6, -8])
        True

        The zero vector is parallel to all vectors.
        >>> Vector([1, 2, 3]).is_parallel([0, 0, 0])
        True

        """
        if Vector(self).is_zero(**kwargs) or Vector(other).is_zero(**kwargs):
            return True

        angle = self.angle_between(other)

        is_direction_same = np.isclose(angle, 0, **kwargs)
        is_direction_opposite = np.isclose(angle, np.pi, **kwargs)

        return is_direction_same or is_direction_opposite

    @require(
        "Neither vector can be the zero vector.", lambda args: not (args.self.is_zero() or Vector(args.other).is_zero())
    )
    @ensure("The output must be in range [0, pi].", lambda _, result: result >= 0 and result <= np.pi)
    @ensure("The output must be a numpy scalar.", lambda _, result: isinstance(result, np.number))
    def angle_between(self, other):
        """
        Return the angle in radians between this vector and another.

        Parameters
        ----------
        other : array_like

        Returns
        -------
        scalar
            Angle between vectors in radians.

        Examples
        --------
        >>> import numpy as np
        >>> from skspatial.objects import Vector

        >>> Vector([1, 0]).angle_between([1, 0])
        0.0

        >>> Vector([1, 1, 1]).angle_between([1, 1, 1])
        0.0

        >>> angle = Vector([1, 0]).angle_between([1, 1])
        >>> np.degrees(angle).round()
        45.0

        >>> angle = Vector([1, 0]).angle_between([-2, 0])
        >>> np.degrees(angle).round()
        180.0

        """
        cos_theta = self.dot(other) / (self.magnitude * Vector(other).magnitude)

        # Ensure that input to arccos is in range [-1, 1] so that output is real.
        cos_theta = np.clip(cos_theta, -1, 1)

        return np.arccos(cos_theta)

    @require("The vectors must have length two.", lambda args: len(args.self) == len(args.other) == 2)
    @ensure("The output is in set {-1, 0, 1}.", lambda _, result: result in {-1, 0, 1})
    def side(self, other):
        """
        Find which side a vector is compared to this vector.

        The two vectors must be 2D.

        Parameters
        ----------
        other : array_like
            Input 2D vector.

        Returns
        -------
        int
            1 if the other vector is right of self.
            0 if other is parallel to self.
            -1 if other is left of self.

        Examples
        --------
        >>> vector = Vector([0, 1])

        >>> vector.side([1, 1])
        1

        >>> vector.side([1, -10])
        1

        >>> vector.side([0, 2])
        0

        >>> vector.side([0, -5])
        0

        >>> vector.side([-3, 4])
        -1

        """
        return np.sign(Vector(other).cross(self)).astype(int)

    @ensure("The output must be parallel to self.", lambda args, result: args.self.is_parallel(result, atol=ATOL))
    def project(self, other):
        """
        Project an other vector onto self.

        Parameters
        ----------
        other : array_like
            Input vector.

        Returns
        -------
        Vector
            Projection of other vector.

        Examples
        --------
        >>> from skspatial.objects import Vector

        >>> Vector([0, 1]).project([2, 1])
        Vector([0., 1., 0.])

        >>> Vector([0, 100]).project([2, 1])
        Vector([0., 1., 0.])

        >>> Vector([0, 1]).project([9, 5])
        Vector([0., 5., 0.])

        >>> Vector([0, 100]).project([9, 5])
        Vector([0., 5., 0.])

        """
        unit_self = self.unit()

        # Scalar projection of other vector onto self.
        scalar_projection = unit_self.dot(other)

        return scalar_projection * unit_self
