"""Module for the Point class."""

import numpy as np

from skspatial.objects._base_array import _BaseArray1D
from skspatial.objects.vector import Vector
from skspatial.typing import array_like


class Point(_BaseArray1D):
    """
    A point in space implemented as a 1D array.

    The array is a subclass of :class:`numpy.ndarray`.

    Parameters
    ----------
    array : array_like
        Input array.

    Attributes
    ----------
    dimension : int
        Dimension of the point.

    Raises
    ------
    ValueError
        If the array is empty, the values are not finite,
        or the dimension is not one.

    Examples
    --------
    >>> from skspatial.objects import Point

    >>> point = Point([1, 2, 3])

    >>> point.dimension
    3

    The object inherits methods from :class:`numpy.ndarray`.

    >>> point.mean()
    array(2.)

    >>> Point([])
    Traceback (most recent call last):
    ...
    ValueError: The array must not be empty.

    >>> import numpy as np

    >>> Point([1, 2, np.nan])
    Traceback (most recent call last):
    ...
    ValueError: The values must all be finite.

    >>> Point([[1, 2], [3, 4]])
    Traceback (most recent call last):
    ...
    ValueError: The array must be 1D.

    """

    def distance_point(self, other: array_like) -> np.float64:
        """
        Return the distance to another point.

        Parameters
        ----------
        other : array_like
            Other point.

        Returns
        -------
        np.float64
            Distance between the points.

        Examples
        --------
        >>> from skspatial.objects import Point

        >>> point = Point([1, 2])
        >>> point.distance_point([1, 2])
        0.0

        >>> point.distance_point([-1, 2])
        2.0

        >>> Point([1, 2, 0]).distance_point([1, 2, 3])
        3.0

        """
        vector = Vector.from_points(self, other)

        return vector.norm()
