"""Private base classes for arrays."""

import numpy as np


class _BaseArray(np.ndarray):
    """Private base class for spatial objects based on a single NumPy array."""

    def __new__(cls, array_like):

        if np.size(array_like) == 0:
            raise ValueError("The array must not be empty.")

        if not np.isfinite(array_like).all():
            raise ValueError("The values must all be finite.")

        # We cast the input array to be our class type.
        obj = np.asarray(array_like).view(cls)

        return obj

    def __array_finalize__(self, obj):
        """
        Finalize creation of the array.

        This function is required for adding extra attributes to a subclass of ndarray.
        Without it, an array constructed from another may not have the extra attributes
        (e.g., a projection of a vector onto another vector).

        Examples
        --------
        >>> from skspatial.objects import Vector, Points

        >>> vector_a = Vector([1, 0])
        >>> vector_b = vector_a.project_vector([1, 1])

        Without __array_finalize__, this vector will not have the dimension attribute.

        >>> vector_a.dimension == vector_b.dimension
        True

        The same applies for 2D arrays.

        >>> points = Points([[1, 2, 3], [4, 5, 6]])
        >>> points_centered, centroid = points.mean_center()

        >>> points.dimension == points_centered.dimension
        True

        """
        self.dimension = getattr(obj, 'dimension', None)

    def is_close(self, other, **kwargs):
        """
        Check if the array is close to another.

        Parameters
        ----------
        other : array_like
            Other array.
        kwargs : dict, optional
            Additional keywords passed to :func:`numpy.allclose`

        Returns
        -------
        True if the arrays are close; false otherwise.

        """
        return np.allclose(self, other, **kwargs)

    def is_equal(self, other):
        """
        Check if the array is equal to another.

        Parameters
        ----------
        other : array_like
            Other array.

        Returns
        -------
        bool
            True if the arrays are equal; false otherwise.

        """
        return np.array_equal(self, other)

    def plotter(self, **kwargs):
        """Return a function that plots the object when passed a matplotlib axes."""
        if self.dimension == 2:
            return lambda ax: self.plot_2d(ax, **kwargs)

        elif self.dimension == 3:
            return lambda ax: self.plot_3d(ax, **kwargs)


class _BaseArray1D(_BaseArray):
    """Private base class for spatial objects based on a single 1D NumPy array."""

    def __new__(cls, array_like):

        array = super().__new__(cls, array_like)

        if array.ndim != 1:
            raise ValueError("The array must be 1D.")

        array.dimension = array.size

        return array

    def set_dimension(self, dim):

        array = _set_dimension_1d(self, dim)
        return self.__class__(array)


class _BaseArray2D(_BaseArray):
    """Private base class for spatial objects based on a single 2D NumPy array."""

    def __new__(cls, array_like):

        array = super().__new__(cls, array_like)

        if array.ndim != 2:
            raise ValueError("The array must be 2D.")

        array.dimension = array.shape[1]

        return array

    def set_dimension(self, dim):

        array = _set_dimension_2d(self, dim)
        return self.__class__(array)


def _set_dimension_1d(array, dim):
    """
    Set the desired dimension (length) of the 1D array.

    Parameters
    ----------
    array : ndarray
        (d,) input array of with dimension d.
    dim : int
        Desired dimension.
        Must be greater than or equal to the current dimension d.

    Returns
    -------
    ndarray
        (dim,) array.

    Examples
    --------
    >>> import numpy as np
    >>> from skspatial.objects._base_array import _set_dimension_1d

    >>> _set_dimension_1d(np.array([1]), 2)
    array([1, 0])

    >>> _set_dimension_1d(np.array([1, 2]), 4)
    array([1, 2, 0, 0])

    >>> _set_dimension_1d(np.array([[1, 2], [2, 3]]), 1)
    Traceback (most recent call last):
    ...
    ValueError: The array must be 1D.

    >>> _set_dimension_1d(np.array([1, 2]), 1)
    Traceback (most recent call last):
    ...
    ValueError: The desired dimension cannot be less than the current dimension.

    """
    if array.ndim != 1:
        raise ValueError("The array must be 1D.")

    if dim < array.size:
        raise ValueError(
            "The desired dimension cannot be less than the current dimension."
        )

    n_zeros = dim - array.size

    return np.pad(array, (0, n_zeros), 'constant')


def _set_dimension_2d(array, dim):
    """
    Change the dimension (width) of a 2D NumPy array.

    E.g., each row of the array represents a point in space.
    The width of the array is the dimension of the points.

    Parameters
    ----------
    array : (N, D) ndarray
        Array of N rows with dimension D.
    dim : int
        Desired dimension.
        Must be greater than or equal to the current dimension d.

    Returns
    -------
    ndarray
        (N, dim) array.

    Examples
    --------
    >>> import numpy as np
    >>> from skspatial.objects._base_array import _set_dimension_2d

    >>> array = np.array([[1, 0], [2, 3]])

    >>> _set_dimension_2d(array, 3)
    array([[1, 0, 0],
           [2, 3, 0]])

    >>> _set_dimension_2d(array, 5)
    array([[1, 0, 0, 0, 0],
           [2, 3, 0, 0, 0]])

    >>> _set_dimension_2d(np.array([1, 2]), 3)
    Traceback (most recent call last):
    ...
    ValueError: The array must be 2D.

    """
    if array.ndim != 2:
        raise ValueError("The array must be 2D.")

    n_cols = array.shape[1]

    return np.pad(array, ((0, 0), (0, dim - n_cols)), 'constant')
