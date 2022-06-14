"""Private base classes for arrays."""
import warnings
from typing import Type
from typing import TypeVar

import numpy as np

from skspatial._functions import _allclose
from skspatial.objects._base_spatial import _BaseSpatial
from skspatial.typing import array_like

# Create generic variables that can be 'Parent' or any subclass.
Array = TypeVar('Array', bound='_BaseArray')

Array1D = TypeVar('Array1D', bound='_BaseArray1D')

Array2D = TypeVar('Array2D', bound='_BaseArray2D')


class _BaseArray(np.ndarray, _BaseSpatial):
    """Private base class for spatial objects based on a single NumPy array."""

    def __new__(cls: Type[Array], array: array_like) -> Array:

        with warnings.catch_warnings():

            warnings.filterwarnings("error")

            try:
                np.array(array)

            except np.VisibleDeprecationWarning as error:
                if str(error).startswith("Creating an ndarray from ragged nested sequences"):
                    raise ValueError("The array must not contain sequences with different lengths.")

        if np.size(array) == 0:
            raise ValueError("The array must not be empty.")

        if not np.isfinite(array).all():
            raise ValueError("The values must all be finite.")

        # We cast the input array to be our class type.
        obj = np.asarray(array).view(cls)

        return obj

    def __array_wrap__(self, array: np.ndarray) -> np.ndarray:
        """
        Return regular :class:`numpy.ndarray` when default NumPy method is called.

        >>> from skspatial.objects import Vector
        >>> vector = Vector([1.234, 2.1234, 3.1234])

        >>> vector.sum().round()
        6.0

        >>> vector.mean().round(2)
        2.16

        """
        return array

    def to_array(self) -> np.ndarray:
        """
        Convert the object to a regular NumPy ndarray.

        Examples
        --------
        >>> from skspatial.objects import Point

        >>> point = Point([1, 2, 3])

        >>> point.to_array()
        array([1, 2, 3])

        """
        return np.array(self)

    def is_close(self, other: array_like, **kwargs: float) -> bool:
        """
        Check if the array is close to another.

        Parameters
        ----------
        other : array_like
            Other array.
        kwargs : dict, optional
            Additional keywords passed to :func:`math.isclose`.

        Returns
        -------
        bool
            True if the arrays are close; false otherwise.

        """
        return bool(_allclose(self, other, **kwargs).all())

    def is_equal(self, other: array_like) -> bool:
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

    def round(self, decimals: int = 0) -> Array:  # type: ignore[override]  # noqa: A003
        """
        Round the array to the given number of decimals.

        Refer to :func:`np.around` for the full documentation.

        Examples
        --------
        >>> from skspatial.objects import Point, Vector

        >>> Vector([1, 1, 1]).unit().round(3)
        Vector([0.577, 0.577, 0.577])

        >>> Point([1, 2, 3.532]).round(2)
        Point([1.  , 2.  , 3.53])

        """
        return np.around(self, decimals=decimals, out=self)


class _BaseArray1D(_BaseArray):
    """Private base class for spatial objects based on a single 1D NumPy array."""

    def __new__(cls: Type[Array1D], array: array_like) -> Array1D:

        obj = super().__new__(cls, array)  # pytype: disable=wrong-arg-count

        if obj.ndim != 1:
            raise ValueError("The array must be 1D.")

        obj.dimension = obj.size

        return obj

    def __array_finalize__(self, _) -> None:

        self.dimension = self.size

    def set_dimension(self: Array1D, dim: int) -> Array1D:
        """
        Set the dimension (length) of the 1D array.

        Parameters
        ----------
        dim : int
            Desired dimension.
            Must be greater than or equal to the current dimension.

        Returns
        -------
        ndarray
            (dim,) array.

        Raises
        ------
        ValueError
            If the desired dimension is less than the current dimension.

        Examples
        --------
        >>> from skspatial.objects import Point

        >>> Point([1]).set_dimension(2)
        Point([1, 0])

        >>> Point([1, 2]).set_dimension(4)
        Point([1, 2, 0, 0])

        >>> Point([1, 2, 3]).set_dimension(2)
        Traceback (most recent call last):
        ...
        ValueError: The desired dimension cannot be less than the current dimension.

        """
        if dim < self.dimension:
            raise ValueError("The desired dimension cannot be less than the current dimension.")

        n_zeros = dim - self.size
        array_padded = np.pad(self, (0, n_zeros), 'constant')

        return self.__class__(array_padded)


class _BaseArray2D(_BaseArray):
    """Private base class for spatial objects based on a single 2D NumPy array."""

    def __new__(cls: Type[Array2D], array: array_like) -> Array2D:

        obj = super().__new__(cls, array)  # pytype: disable=wrong-arg-count

        if obj.ndim != 2:
            raise ValueError("The array must be 2D.")

        obj.dimension = obj.shape[1]

        return obj

    def set_dimension(self: Array2D, dim: int) -> Array2D:
        """
        Set the dimension (width) of the 2D array.

        E.g., each row of the array represents a point in space.
        The width of the array is the dimension of the points.

        Parameters
        ----------
        dim : int
            Desired dimension.
            Must be greater than or equal to the current dimension.

        Returns
        -------
        ndarray
            (N, dim) array.

        Raises
        ------
        ValueError
            If the desired dimension is less than the current dimension.

        Examples
        --------
        >>> from skspatial.objects import Points

        >>> points = Points([[1, 0], [2, 3]])

        >>> points.set_dimension(3)
        Points([[1, 0, 0],
                [2, 3, 0]])

        >>> points.set_dimension(5)
        Points([[1, 0, 0, 0, 0],
                [2, 3, 0, 0, 0]])

        >>> Points([[1, 2, 3], [4, 5, 6]]).set_dimension(2)
        Traceback (most recent call last):
        ...
        ValueError: The desired dimension cannot be less than the current dimension.

        """
        if dim < self.dimension:
            raise ValueError("The desired dimension cannot be less than the current dimension.")

        array_padded = np.pad(self, ((0, 0), (0, dim - self.dimension)), 'constant')

        return self.__class__(array_padded)

    def __array_finalize__(self, _) -> None:

        try:
            self.dimension = self.shape[1]

        except IndexError:
            self.dimension = None
