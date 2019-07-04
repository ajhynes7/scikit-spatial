"""Module for the Vector class."""

import numpy as np

from skspatial.objects._base_array import _BaseArray1D
from skspatial.plotting import _connect_points_3d


class Vector(_BaseArray1D):
    """
    A vector implemented as a 1D array.

    The array is a subclass of :class:`numpy.ndarray`.

    Parameters
    ----------
    array : array_like
        Input array.

    Attributes
    ----------
    dimension : int
        Dimension of the vector.

    Raises
    ------
    ValueError
        If the array is empty, the values are not finite,
        or the dimension is not one.

    Examples
    --------
    >>> from skspatial.objects import Vector

    >>> vector = Vector([1, 2, 3])

    >>> vector.dimension
    3

    The object inherits methods from :class:`numpy.ndarray`.

    >>> vector.mean()
    Vector(2.)

    >>> Vector([])
    Traceback (most recent call last):
    ...
    ValueError: The array must not be empty.

    >>> import numpy as np

    >>> Vector([1, 2, np.nan])
    Traceback (most recent call last):
    ...
    ValueError: The values must all be finite.

    >>> Vector([[1, 2], [3, 4]])
    Traceback (most recent call last):
    ...
    ValueError: The array must be 1D.

    """

    def __new__(cls, array):
        """Create a new Vector object."""
        return super().__new__(cls, array)

    @classmethod
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
        Vector([1, 0])

        >>> Vector.from_points([5, 2], [-2, 8])
        Vector([-7,  6])

        >>> Vector.from_points([3, 1, 1], [7, 7, 0])
        Vector([ 4,  6, -1])

        """
        return cls(np.subtract(point_b, point_a))

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

    def unit(self):
        """
        Return the unit vector of this vector.

        Returns
        -------
        Vector
            Unit vector in same direction as original vector.

        Raises
        ------
        ValueError
            If the magnitude of the vector is zero.

        Examples
        --------
        >>> from skspatial.objects import Vector

        >>> Vector([1, 0]).unit()
        Vector([1., 0.])

        >>> Vector([-20, 0]).unit()
        Vector([-1.,  0.])

        >>> Vector([1, 1]).unit()
        Vector([0.70710678, 0.70710678])

        >>> Vector([1, 1, 1]).unit()
        Vector([0.57735027, 0.57735027, 0.57735027])

        >>> Vector([0, 0]).unit()
        Traceback (most recent call last):
        ...
        ValueError: The magnitude must not be zero.

        """
        magnitude = self.norm()

        if magnitude == 0:
            raise ValueError("The magnitude must not be zero.")

        return self / magnitude

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
        Vector([0, 0, 1])

        >>> Vector([2, 5]).cross([1, 1])
        Vector([ 0,  0, -3])

        >>> Vector([1, 0]).cross([0, 1])
        Vector([0, 0, 1])

        >>> Vector([1, 1, 1]).cross([0, 1, 0])
        Vector([-1,  0,  1])

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

        Raises
        ------
        ValueError
            If either vector has a magnitude of zero.

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

        >>> Vector([0, 0]).cosine_similarity([1, 1])
        Traceback (most recent call last):
        ...
        ValueError: The vectors must have non-zero magnitudes.

        """
        denom = self.norm() * Vector(other).norm()

        if denom == 0:
            raise ValueError("The vectors must have non-zero magnitudes.")

        cos_theta = self.dot(other) / denom

        # Ensure that the output is in the range [-1, 1],
        # so that the angle theta is defined.
        return np.clip(cos_theta, -1, 1)

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

    def angle_signed(self, other):
        """
        Return the signed angle in radians between two 2D vectors.

        Parameters
        ----------
        other : array_like
            Input vector.

        Returns
        -------
        scalar
            Signed angle between vectors in radians.

        Raises
        ------
        ValueError
            If the vectors are not 2D.

        Examples
        --------
        >>> import numpy as np
        >>> from skspatial.objects import Vector

        >>> Vector([1, 0]).angle_signed([1, 0])
        0.0

        >>> np.degrees(Vector([1, 0]).angle_signed([0, 1]))
        90.0

        >>> np.degrees(Vector([1, 0]).angle_signed([0, -1]))
        -90.0

        >>> Vector([1, 0, 0]).angle_signed([0, -1, 0])
        Traceback (most recent call last):
        ...
        ValueError: The vectors must be 2D.

        """
        other = Vector(other)

        if not (self.dimension == 2 and other.dimension == 2):
            raise ValueError("The vectors must be 2D.")

        dot = self.dot(other)
        det = np.linalg.det([self, other])

        return np.arctan2(det, dot)

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
        if self.is_zero(**kwargs) or Vector(other).is_zero(**kwargs):
            # The zero vector is perpendicular to all vectors.
            return True

        return np.isclose(np.abs(self.cosine_similarity(other)), 1, **kwargs)

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

        Raises
        ------
        ValueError
            If the vectors are not 2D.

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

        >>> Vector([1, 0, 0]).side_vector([1, 2, 3])
        Traceback (most recent call last):
        ...
        ValueError: The vectors must be 2D.

        """
        value_cross = np.cross(other, self)

        if value_cross.ndim != 0:
            raise ValueError("The vectors must be 2D.")

        return np.sign(value_cross).astype(int)

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

    def plot_2d(self, ax_2d, point=(0, 0), scalar=1, **kwargs):
        """
        Plot a 2D vector.

        The vector is plotted as an arrow.

        Parameters
        ----------
        ax_2d : Axes
            Instance of :class:`~matplotlib.axes.Axes`.
        point : array_like, optional
            Position of the vector tail (default is origin).
        scalar : scalar, optional
            Value used to scale the vector (default 1).
        kwargs : dict, optional
            Additional keywords passed to :meth:`~matplotlib.axes.Axes.arrow`.

        """
        x, y = point
        dx, dy = scalar * self

        ax_2d.arrow(x, y, dx, dy, **kwargs)

    def plot_3d(self, ax_3d, point=(0, 0, 0), scalar=1, **kwargs):
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
        scalar : scalar, optional
            Value used to scale the vector (default 1).
        kwargs : dict, optional
            Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot`.

        """
        point_2 = np.array(point) + scalar * self

        _connect_points_3d(ax_3d, point, point_2, **kwargs)
