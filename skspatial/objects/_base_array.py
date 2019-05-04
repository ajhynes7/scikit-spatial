"""Private base classes for arrays."""

import numpy as np
from dpcontracts import require, ensure, types


class _BaseArray(np.ndarray):
    """Private base class for spatial objects based on a single NumPy array."""

    @require("The input array must only contain finite numbers.", lambda args: np.all(np.isfinite(args.array_like)))
    def __new__(cls, array_like):

        array = np.array(array_like, dtype=float)

        # We cast the input array to be our class type.
        obj = np.asarray(array).view(cls)

        return obj

    @classmethod
    def _to_arrays(cls, *objs):
        """
        Convert array_like inputs to an array class.

        Other spatial objects (e.g., Line) are ignored.

        Parameters
        ----------
        objs
            Input objects

        Yields
        ------
        object
            Object converted to BaseArray if it was an array_like.
            Otherwise, the same object is yielded.

        Examples
        --------
        >>> from skspatial.objects import Point, Line

        >>> list(Point._to_arrays([1, 2], 1, [4, 5], 10))
        [Point([1., 2.]), 1, Point([4., 5.]), 10]

        >>> line = Line([1, 2], [4, 3])
        >>> list(Point._to_arrays(line, [5, 9]))
        [Line(point=Point([1., 2.]), direction=Vector([4., 3.])), Point([5., 9.])]

        """
        for obj in objs:

            if hasattr(obj, '__len__') and not hasattr(obj, 'set_dimension'):
                yield cls(obj)
            else:
                yield obj

    @classmethod
    def normalize_dimension(cls, *objs):
        """
        Normalize the dimensions of all arrays associated with the input objects.

        The dimension of each array is set to the largest dimension of the input arrays.
        Array-like objects (e.g. `list`, `ndarray`) are converted
        to the input spatial array class (e.g. `Point`).

        Objects that are already a spatial array (e.g. `Vector`) do not change type.

        Yields
        ------
        object
            Spatial object with the largest dimension of the inputs.

        Examples
        --------
        >>> from skspatial.objects import Point, Points, Vector, Line

        >>> line = Line([1, 2], [4, 3])
        >>> point, line = Point.normalize_dimension([5, 0, 5], line)

        >>> point
        Point([5., 0., 5.])

        >>> line
        Line(point=Point([1., 2., 0.]), direction=Vector([4., 3., 0.]))

        >>> points = Points([[1, 2], [4, 5]])
        >>> vector, points = Vector.normalize_dimension([6, 4, 7, 1], points)

        >>> vector
        Vector([6., 4., 7., 1.])

        >>> points
        Points([[1., 2., 0., 0.],
                [4., 5., 0., 0.]])

        >>> vector = Vector([0, 1, 1])
        >>> point, vector = Point.normalize_dimension([1, 2], vector)

        >>> point
        Point([1., 2., 0.])

        >>> vector
        Vector([0., 1., 1.])

        """
        # Convert objects to the base array class so we can get/set the dimension.
        objs = list(cls._to_arrays(*objs))

        dim_max = max([obj.get_dimension() for obj in objs])

        for obj in objs:
            yield obj.set_dimension(dim_max)


class _BaseArray1D(_BaseArray):
    """Private base class for spatial objects based on a single 1D NumPy array."""

    @require("The input array must be 1D.", lambda args: np.array(args.array_like).ndim == 1)
    @require("The length must be greater than one.", lambda args: len(args.array_like) > 1)
    @ensure(
        "The output must be a 1D array with the input length.",
        lambda args, result: result.shape == (len(args.array_like),),
    )
    def __new__(cls, array_like):

        return super().__new__(cls, array_like)

    def get_dimension(self):

        return self.size

    def set_dimension(self, dim):

        array = _set_dimension_1d(self, dim)
        return self.__class__(array)

    def is_close(self, other, **kwargs):
        """Check if array is close to another array."""
        return np.allclose(self, other, **kwargs)

    @ensure("The output must be the same class as the input.", lambda args, result: isinstance(result, type(args.self)))
    def add(self, array):
        """
        Add an array to self.

        Parameters
        ----------
        array : array_like
            Input array.

        Returns
        -------
        Array

        Examples
        --------
        >>> from skspatial.objects import Point, Vector

        >>> point = Point([1, 2, 0])
        >>> point.add([2, 9, 1])
        Point([ 3., 11.,  1.])

        >>> point.add([-1, 5, 0])
        Point([0., 7., 0.])

        >>> vector = Vector([5, 9, 1])
        >>> vector.add([1, 0, 0])
        Vector([6., 9., 1.])

        >>> Vector([5, 9, 1, 0]).add([1, 2, 3, 4])
        Vector([ 6., 11.,  4.,  4.])

        """
        return self.__class__(np.add(self, array))

    @ensure("The output must be the same class as the input.", lambda args, result: isinstance(result, type(args.self)))
    def subtract(self, array):
        """Subtract an array from self."""
        return self.__class__(np.subtract(self, array))


class _BaseArray2D(_BaseArray):
    """Private base class for spatial objects based on a single 2D NumPy array."""

    @require("The input array must be 2D.", lambda args: np.array(args.array_like).ndim == 2)
    @require("The input array must have more than one column.", lambda args: np.array(args.array_like).shape[1] > 1)
    def __new__(cls, array_like):

        return super().__new__(cls, array_like)

    def get_dimension(self):

        return self.shape[1]

    def set_dimension(self, dim):

        array = _set_dimension_2d(self, dim)
        return self.__class__(array)


@types(array=np.ndarray, dim=int)
@require("The array must be 1D.", lambda args: args.array.ndim == 1)
@require("The desired dimension cannot be less than the array dimension.", lambda args: args.array.size <= args.dim)
@ensure("The output must have the desired dimensions.", lambda args, result: result.shape == (args.dim,))
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

    >>> _set_dimension_1d(np.array([1, 2]), 1)
    Traceback (most recent call last):
    ...
    dpcontracts.PreconditionError: The desired dimension cannot be less than the array dimension.

    """
    n_zeros = dim - array.size

    return np.pad(array, (0, n_zeros), 'constant')


@types(array=np.ndarray, dim=int)
@require("The array must be 2D.", lambda args: args.array.ndim == 2)
@require(
    "The points dimension cannot be greater than the desired dimension.", lambda args: args.array.shape[1] <= args.dim
)
@ensure(
    "The output must have the desired dimensions.", lambda args, result: result.shape == (len(args.array), args.dim)
)
def _set_dimension_2d(array, dim):
    """
    Change the dimension (width) of a 2D NumPy array.

    E.g., each row of the array represents a point in space.
    The width of the array is the dimension of the points.

    Parameters
    ----------
    array : ndarray
        (n, d) input array of n rows with dimension d.
    dim : int
        Desired dimension.
        Must be greater than or equal to the current dimension d.

    Returns
    -------
    ndarray
        (n, dim) array.

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
    dpcontracts.PreconditionError: The array must be 2D.

    """
    n_cols = array.shape[1]

    return np.pad(array, ((0, 0), (0, dim - n_cols)), 'constant')
