"""Module for the Vector class."""

import numpy as np
from dpcontracts import require, ensure, types
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D

from skspatial._constants import ATOL
from skspatial._plotting import _connect_points_3d
from skspatial.objects._base_array import _BaseArray1D


class Vector(_BaseArray1D):
    """Vector implemented as an ndarray subclass."""

    def __new__(cls, array_like):
        """Create a new Vector object."""
        obj = super().__new__(cls, array_like)

        return obj

    @classmethod
    @ensure("The output must be a vector.", lambda _, result: isinstance(result, Vector))
    def from_points(cls, point_a, point_b):
        """
        Instantiate a vector from point A to point B.

        Parameters
        ----------
        point_a, point_b : array_like
            Points defining the vector.

        Returns
        -------
        Vector
            Vector from point A to point B.

        Examples
        --------
        >>> from skspatial.objects import Vector

        >>> Vector.from_points([0, 0], [1, 0])
        Vector([1., 0.])

        >>> Vector.from_points([5, 2], [-2, 8])
        Vector([-7.,  6.])

        >>> Vector.from_points([3, 1, 1], [7, 7, 0])
        Vector([ 4.,  6., -1.])

        """
        return cls(Vector(point_b).subtract(point_a))

    @ensure("The magnitude must be zero or greater", lambda _, result: result >= 0)
    def norm(self, **kwargs):
        """
        Return the norm of the vector.

        Parameters
        ----------
        kwargs : dict, optional
            Additional keywords passed to :func:`numpy.linalg.norm`.

        Returns
        -------
        scalar
            Norm of the vector.

        Examples
        --------
        >>> from skspatial.objects import Vector

        >>> vector = Vector([1, 2, 3])

        >>> vector.norm().round(3)
        3.742

        >>> vector.norm(ord=1)
        6.0

        >>> vector.norm(ord=0)
        3.0

        """
        return np.linalg.norm(self, **kwargs)

    @require("The vector cannot be the zero vector.", lambda args: not args.self.is_zero())
    @ensure("The output must be a vector.", lambda _, result: isinstance(result, Vector))
    @ensure("The output must have a magnitude of one.", lambda _, result: np.isclose(result.norm(), 1))
    def unit(self):
        """Return the unit vector of this vector."""
        return Vector(self / self.norm())

    def is_zero(self, **kwargs):
        """
        Check if the vector is the zero vector.

        The zero vector in n dimensions is the vector containing n zeros.

        Parameters
        ----------
        kwargs : dict, optional
            Additional keywords passed to :func:`numpy.allclose`.

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

    def dot(self, other):
        """Return the dot product with another array."""
        return np.dot(self, other)

    @ensure("The output must be a vector.", lambda _, result: isinstance(result, Vector))
    @ensure("The output must be a 1D array with length three.", lambda _, result: result.shape == (3,))
    def cross(self, other):
        """
        Compute the cross product with another vector.

        Parameters
        ----------
        other : array_like
             Input vector.

        Returns
        -------
        Vector
            3D vector perpendicular to both inputs.

        Examples
        --------
        >>> from skspatial.objects import Vector

        >>> Vector([1, 0]).cross([0, 1])
        Vector([0., 0., 1.])

        >>> Vector([2, 5]).cross([1, 1])
        Vector([ 0.,  0., -3.])

        >>> Vector([1, 0]).cross([0, 1])
        Vector([0., 0., 1.])

        >>> Vector([1, 1, 1]).cross([0, 1, 0])
        Vector([-1.,  0.,  1.])

        """
        # Convert to 3D vectors so that cross product is also 3D.
        vector_a = self.set_dimension(3)
        vector_b = Vector(other).set_dimension(3)

        return Vector(np.cross(vector_a, vector_b))

    def cosine_similarity(self, other):
        """
        Return the cosine similarity of this vector with another.

        This is the cosine of the angle between the vectors.

        Parameters
        ----------
        other : array_like
            Input vector.

        Returns
        -------
        scalar
            Cosine similarity.

        Examples
        --------
        >>> from skspatial.objects import Vector

        >>> Vector([1, 0]).cosine_similarity([0, 1])
        0.0

        >>> Vector([30, 0]).cosine_similarity([0, 20])
        0.0

        >>> Vector([1, 0]).cosine_similarity([-1, 0])
        -1.0

        >>> Vector([1, 0]).cosine_similarity([1, 1]).round(3)
        0.707

        """
        cos_theta = self.dot(other) / (self.norm() * Vector(other).norm())

        # Ensure that the output is in the range [-1, 1],
        # so that the angle theta is defined.
        return np.clip(cos_theta, -1, 1)

    @require(
        "Neither vector can be the zero vector.", lambda args: not (args.self.is_zero() or Vector(args.other).is_zero())
    )
    @ensure("The output must be in range [0, pi].", lambda _, result: result >= 0 and result <= np.pi)
    @ensure("The output must be a NumPy scalar.", lambda _, result: isinstance(result, np.number))
    def angle_between(self, other):
        """
        Return the angle in radians between this vector and another.

        Parameters
        ----------
        other : array_like
            Input vector.

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
        cos_theta = self.cosine_similarity(other)

        return np.arccos(cos_theta)

    def is_perpendicular(self, other, **kwargs):
        """
        Check if an other vector is perpendicular to self.

        Vectors u and v are perpendicular <==> Dot product of u and v is zero.

        Parameters
        ----------
        other : array_like
            Input vector.
        kwargs : dict, optional
            Additional keywords passed to :func:`numpy.isclose`.

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
            Additional keywords passed to :func:`numpy.isclose`.

        Returns
        -------
        bool
            True if the vector is parallel; false otherwise.

        Examples
        --------
        >>> from skspatial.objects import Vector

        >>> Vector([0, 1]).is_parallel([1, 0])
        False

        >>> Vector([1, 1]).is_parallel([1, 1])
        True

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
            # The zero vector is perpendicular to all vectors.
            return True

        return np.isclose(np.abs(self.cosine_similarity(other)), 1, **kwargs)

    @require("The vectors must have length two.", lambda args: len(args.self) == len(args.other) == 2)
    @ensure("The output must be in the set {-1, 0, 1}.", lambda _, result: result in {-1, 0, 1})
    def side_vector(self, other):
        """
        Find the side of the vector where another vector is directed.

        Both vectors must be 2D.

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
        >>> from skspatial.objects import Vector

        >>> vector = Vector([0, 1])

        >>> vector.side_vector([1, 1])
        1

        >>> vector.side_vector([1, -10])
        1

        >>> vector.side_vector([0, 2])
        0

        >>> vector.side_vector([0, -5])
        0

        >>> vector.side_vector([-3, 4])
        -1

        """
        return np.sign(np.cross(other, self)).astype(int)

    def scalar_projection(self, other):
        """
        Return the scalar projection of an other vector onto this vector.

        Parameters
        ----------
        other : array_like
            Input vector.

        Returns
        -------
        scalar
            Scalar projection of other vector onto self.

        Examples
        --------
        >>> from skspatial.objects import Vector

        >>> Vector([0, 1]).scalar_projection([2, 1])
        1.0

        >>> Vector([-1, -1]).scalar_projection([1, 0]).round(3)
        -0.707

        >>> Vector([0, 100]).scalar_projection([9, 5])
        5.0

        >>> Vector([5, 0]).scalar_projection([-10, 3])
        -10.0

        """
        return self.unit().dot(other)

    @ensure(
        "The vector projection must be parallel to self.", lambda args, result: args.self.is_parallel(result, atol=ATOL)
    )
    def project_vector(self, other):
        """
        Project an other vector onto this vector.

        Parameters
        ----------
        other : array_like
            Input vector.

        Returns
        -------
        Vector
            Vector projection of other vector onto self.

        Examples
        --------
        >>> from skspatial.objects import Vector

        >>> Vector([0, 1]).project_vector([2, 1])
        Vector([0., 1.])

        >>> Vector([0, 100]).project_vector([2, 1])
        Vector([0., 1.])

        >>> Vector([0, 1]).project_vector([9, 5])
        Vector([0., 5.])

        >>> Vector([0, 100]).project_vector([9, 5])
        Vector([0., 5.])

        """
        return self.dot(other) / self.dot(self) * self

    @types(ax_2d=Axes)
    @require("The vector must be 2D.", lambda args: args.self.get_dimension() == 2)
    @require("The point must be 2D.", lambda args: len(args.point) == 2)
    def plot_2d(self, ax_2d, point=(0, 0), **kwargs):
        """
        Plot a 2D vector.

        The vector is plotted as an arrow.

        Parameters
        ----------
        ax_2d : Axes
            Instance of :class:`~matplotlib.axes.Axes`.
        point : array_like, optional
            Position of the vector tail (default is origin).
        kwargs : dict, optional
            Additional keywords passed to :meth:`~matplotlib.axes.Axes.arrow`.

        """
        ax_2d.arrow(*point, *self, **kwargs)

    @types(ax_3d=Axes3D)
    @require("The vector must be 3D.", lambda args: args.self.get_dimension() == 3)
    @require("The point must be 3D.", lambda args: len(args.point) == 3)
    def plot_3d(self, ax_3d, point=(0, 0, 0), **kwargs):
        """
        Plot a 3D vector.

        The vector is plotted by connecting two 3D points
        (the head and tail of the vector).

        Parameters
        ----------
        ax_3d : Axes
            Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
        point : array_like, optional
            Position of the vector tail (default is origin).
        kwargs : dict, optional
            Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot`.

        """
        point_2 = Vector(point) + self
        _connect_points_3d(ax_3d, point, point_2, **kwargs)
