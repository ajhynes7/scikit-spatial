"""Module for the Vector class."""
from __future__ import annotations

import math
from typing import cast

import numpy as np
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D

from skspatial._functions import np_float
from skspatial.objects._base_array import _BaseArray1D
from skspatial.plotting import _connect_points_3d
from skspatial.typing import array_like


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
    array(2.)

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

    @classmethod
    def from_points(cls, point_a: array_like, point_b: array_like) -> Vector:
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
        array_vector_ab = cast(np.ndarray, np.subtract(point_b, point_a))

        return cls(array_vector_ab)

    def norm(self, **kwargs) -> np.float64:
        """
        Return the norm of the vector.

        Parameters
        ----------
        kwargs : dict, optional
            Additional keywords passed to :func:`numpy.linalg.norm`.

        Returns
        -------
        np.float64
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

    def unit(self) -> Vector:
        """
        Return the unit vector in the same direction as the vector.

        A unit vector is a vector with a magnitude of one.

        Returns
        -------
        Vector
            Unit vector.

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

        >>> Vector([1, 1]).unit().round(3)
        Vector([0.707, 0.707])

        >>> Vector([1, 1, 1]).unit().round(3)
        Vector([0.577, 0.577, 0.577])

        >>> Vector([0, 0]).unit()
        Traceback (most recent call last):
        ...
        ValueError: The magnitude must not be zero.

        """
        magnitude = self.norm()

        if magnitude == 0:
            raise ValueError("The magnitude must not be zero.")

        return self / magnitude

    def is_zero(self, **kwargs: float) -> bool:
        """
        Check if the vector is the zero vector.

        The zero vector in n dimensions is the vector containing n zeros.

        Parameters
        ----------
        kwargs : dict, optional
            Additional keywords passed to :func:`math.isclose`.

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
        >>> Vector([0, 0, 1e-4]).is_zero(abs_tol=1e-3)
        True

        """
        return math.isclose(self.dot(self), 0, **kwargs)

    def cross(self, other: array_like) -> Vector:
        """
        Compute the cross product with another vector.

        Parameters
        ----------
        other : array_like
             Other vector.

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

    def cosine_similarity(self, other: array_like) -> np.float64:
        """
        Return the cosine similarity of the vector with another.

        This is the cosine of the angle between the vectors.

        Parameters
        ----------
        other : array_like
            Other vector.

        Returns
        -------
        np.float64
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
        clipped = np.clip(cos_theta, -1, 1)

        return np.float64(clipped)

    @np_float
    def angle_between(self, other: array_like) -> float:
        """
        Return the angle in radians between the vector and another.

        Parameters
        ----------
        other : array_like
            Other vector.

        Returns
        -------
        np.float64
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

        return math.acos(cos_theta)

    @np_float
    def angle_signed(self, other: array_like) -> float:
        """
        Return the signed angle in radians between the vector and another.

        The vectors must be 2D.

        Parameters
        ----------
        other : array_like
            Other vector.

        Returns
        -------
        np.float64
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
        if not (self.dimension == 2 and Vector(other).dimension == 2):
            raise ValueError("The vectors must be 2D.")

        dot = self.dot(other)
        det = np.linalg.det([self, other])

        return math.atan2(det, dot)

    @np_float
    def angle_signed_3d(self, other: array_like, direction_positive: array_like) -> float:
        """
        Return the signed angle in radians between the vector and another.

        The vectors must be 3D.

        Parameters
        ----------
        other : array_like
            Other main input vector.
        direction_positive : array_like
            A vector perpendicular to the plane formed by the two main input vectors.

        Returns
        -------
        np.float64
            Signed angle between vectors in radians.

        Raises
        ------
        ValueError
            If the vectors are not 3D.
            If the positive direction vector is not perpendicular to the plane formed by the two main input vectors.

        References
        ----------
        https://stackoverflow.com/questions/5188561/signed-angle-between-two-3d-vectors-with-same-origin-within-the-same-plane

        Notes
        -----
        This method uses the convention of right-handed rotation.

        Examples
        --------
        >>> import numpy as np
        >>> from skspatial.objects import Vector

        >>> np.degrees(Vector([1, 0, 0]).angle_signed_3d([0, -1, 0], direction_positive=[0, 0, 2]))
        -90.0

        >>> np.degrees(Vector([1, 0, 0]).angle_signed_3d([0, -1, 0], direction_positive=[0, 0, -5]))
        90.0

        >>> Vector([1, 0]).angle_signed_3d([1, 0], [1, 0, 0])
        Traceback (most recent call last):
        ...
        ValueError: The vectors must be 3D.

        >>> Vector([1, 0, 4]).angle_signed_3d([1, 0, 5], [1, 0])
        Traceback (most recent call last):
        ...
        ValueError: The vectors must be 3D.

        """
        if not all([self.dimension == 3, Vector(other).dimension == 3, Vector(direction_positive).dimension == 3]):
            raise ValueError("The vectors must be 3D.")

        cross = self.cross(other)

        if not cross.is_parallel(direction_positive):
            raise ValueError(
                (
                    "The positive direction vector must be perpendicular to the plane formed by the two main input "
                    "vectors."
                ),
            )

        direction_positive = Vector(direction_positive).unit()
        return np.arctan2(cross.dot(direction_positive), self.dot(other))

    def is_perpendicular(self, other: array_like, **kwargs: float) -> bool:
        r"""
        Check if the vector is perpendicular to another.

        Two vectors :math:`u` and :math:`v` are perpendicular if

        .. math::
            u \cdot v = 0

        Parameters
        ----------
        other : array_like
            Other vector.
        kwargs : dict, optional
            Additional keywords passed to :func:`math.isclose`.

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
        return math.isclose(self.dot(other), 0, **kwargs)

    def is_parallel(self, other: array_like, **kwargs: float) -> bool:
        r"""
        Check if the vector is parallel to another.

        Two nonzero vectors :math:`u` and :math:`v` are parallel if

        .. math::
            \texttt{abs}(\texttt{cosine_similarity}(u, v)) = 1

        The zero vector is parallel to all vectors.

        Parameters
        ----------
        other : array_like
            Other vector.
        kwargs : dict, optional
            Additional keywords passed to :func:`math.isclose`.

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

        similarity = self.cosine_similarity(other)

        return math.isclose(abs(similarity), 1, **kwargs)

    def side_vector(self, other: array_like) -> int:
        """
        Find the side of the vector where another vector is directed.

        Both vectors must be 2D.

        Parameters
        ----------
        other : array_like
            Other 2D vector.

        Returns
        -------
        int
            1 if the other vector is to the right.
            0 if the other is parallel.
            -1 if the other is to the left.

        Raises
        ------
        ValueError
            If the vectors are not 2D.

        Examples
        --------
        >>> from skspatial.objects import Vector

        >>> vector_target = Vector([0, 1])

        The vector is parallel to the target vector.

        >>> vector_target.side_vector([0, 2])
        0
        >>> vector_target.side_vector([0, -5])
        0

        The vector is to the right of the target vector.

        >>> vector_target.side_vector([1, 1])
        1
        >>> vector_target.side_vector([1, -10])
        1

        The vector is to the left of the target vector.

        >>> vector_target.side_vector([-3, 4])
        -1

        The vectors are not 2D.

        >>> Vector([1]).side_vector([2])
        Traceback (most recent call last):
        ...
        ValueError: The vectors must be 2D.

        >>> Vector([1, 0, 0]).side_vector([1, 2, 3])
        Traceback (most recent call last):
        ...
        ValueError: The vectors must be 2D.

        """
        if self.dimension != 2 or Vector(other).dimension != 2:
            raise ValueError("The vectors must be 2D.")

        value_cross = np.cross(other, self)

        return int(np.sign(value_cross))

    def scalar_projection(self, other: array_like) -> np.float64:
        """
        Return the scalar projection of an other vector onto the vector.

        Parameters
        ----------
        other : array_like
            Other vector.

        Returns
        -------
        np.float64
            Scalar projection.

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
        result = self.unit().dot(other)

        return np.float64(result)

    def project_vector(self, other: array_like) -> Vector:
        """
        Project an other vector onto the vector.

        Parameters
        ----------
        other : array_like
            Other vector.

        Returns
        -------
        Vector
            Vector projection.

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

    def different_direction(self, **kwargs: float) -> Vector:
        """
        Return a simple vector that is in a different direction.

        This is useful for finding a vector perpendicular to the original,
        by taking the cross product of the original with the one in a different direction.

        Parameters
        ----------
        kwargs : dict, optional
            Additional keywords passed to :meth:`Vector.is_zero` and :meth:`Vector.is_parallel`.
            :meth:`Vector.is_zero` is used to ensure the input vector is not the zero vector,
            and :meth:`Vector.is_parallel` is used to ensure the new vector is not parallel to the input.

        Returns
        -------
        Vector
            A unit vector in a different direction from the original.

        Raises
        ------
        ValueError
            If the vector is the zero vector.

        Examples
        --------
        >>> from skspatial.objects import Vector

        >>> Vector([1]).different_direction()
        Vector([-1])
        >>> Vector([100]).different_direction()
        Vector([-1])
        >>> Vector([-100]).different_direction()
        Vector([1])
        >>> Vector([1, 0]).different_direction()
        Vector([0., 1.])
        >>> Vector([1, 1]).different_direction()
        Vector([1., 0.])
        >>> Vector([1, 1, 1, 1]).different_direction()
        Vector([1., 0., 0., 0.])

        """
        if self.is_zero(**kwargs):
            raise ValueError("The vector must not be the zero vector.")

        if self.dimension == 1:
            return Vector([-np.sign(self[0])])

        vector_different_direction = Vector(np.zeros(self.dimension))
        vector_different_direction[0] = 1

        if self.is_parallel(vector_different_direction, **kwargs):
            vector_different_direction[0] = 0
            vector_different_direction[1] = 1

        return vector_different_direction

    def plot_2d(self, ax_2d: Axes, point: array_like = (0, 0), scalar: float = 1, **kwargs) -> None:
        """
        Plot a 2D vector.

        The vector is plotted as an arrow.

        Parameters
        ----------
        ax_2d : Axes
            Instance of :class:`~matplotlib.axes.Axes`.
        point : array_like, optional
            Position of the vector tail (default is origin).
        scalar : {int, float}, optional
            Value used to scale the vector (default 1).
        kwargs : dict, optional
            Additional keywords passed to :meth:`~matplotlib.axes.Axes.arrow`.

        Examples
        --------
        .. plot::
            :include-source:

            >>> import matplotlib.pyplot as plt
            >>> from skspatial.objects import Vector

            >>> _, ax = plt.subplots()

            >>> Vector([1, 1]).plot_2d(ax, point=(-3, 5), scalar=2, head_width=0.5)

            >>> limits = ax.axis([-5, 5, 0, 10])

        """
        x, y = point
        dx, dy = scalar * self

        ax_2d.arrow(x, y, dx, dy, **kwargs)

    def plot_3d(self, ax_3d: Axes3D, point: array_like = (0, 0, 0), scalar: float = 1, **kwargs) -> None:
        """
        Plot a 3D vector.

        The vector is plotted by connecting two 3D points
        (the head and tail of the vector).

        Parameters
        ----------
        ax_3d : Axes3D
            Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
        point : array_like, optional
            Position of the vector tail (default is origin).
        scalar : {int, float}, optional
            Value used to scale the vector (default 1).
        kwargs : dict, optional
            Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot`.

        Examples
        --------
        .. plot::
            :include-source:

            >>> import matplotlib.pyplot as plt
            >>> from mpl_toolkits.mplot3d import Axes3D

            >>> from skspatial.objects import Vector

            >>> fig = plt.figure()
            >>> ax = fig.add_subplot(111, projection='3d')

            >>> Vector([-1, 1, 1]).plot_3d(ax, point=(1, 2, 3), c='r')

        """
        point_2 = np.array(point) + scalar * self

        _connect_points_3d(ax_3d, point, point_2, **kwargs)
