"""Private base classes for arrays."""

import numpy as np
from dpcontracts import require, ensure, types


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
    >>> from skspatial.objects.base_array import _set_dimension_1d

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
    >>> from skspatial.objects.base_array import _set_dimension_1d

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


def _to_arrays(*objs):
    """
    Convert array_like inputs to the base array class.

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
    >>> from skspatial.objects.base_array import _to_arrays
    >>> from skspatial.objects import Line

    >>> list(_to_arrays([1, 2], 1, [4, 5], 10))
    [_BaseArray([1., 2.]), 1, _BaseArray([4., 5.]), 10]

    >>> line = Line([1, 2], [4, 3])
    >>> list(_to_arrays(line, [5, 9]))
    [Line(point=Point([1., 2.]), direction=Vector([4., 3.])), _BaseArray([5., 9.])]

    """
    for obj in objs:

        if hasattr(obj, '__len__') and not hasattr(obj, 'set_dimension'):
            yield _BaseArray(obj)
        else:
            yield obj


def _normalize_dimension(*objs):
    """
    Normalize the dimensions of all arrays associated with the input objects.

    The dimension of each array is set to the largest dimension of the input arrays.

    Examples
    --------
    >>> from skspatial.objects.base_array import _normalize_dimension
    >>> from skspatial.objects import Line

    >>> line = Line([1, 2], [4, 3])

    >>> list(_normalize_dimension(line, [5]))
    [Line(point=Point([1., 2.]), direction=Vector([4., 3.])), _BaseArray([5., 0.])]

    >>> list(_normalize_dimension(line, [5, 4, 3]))
    [Line(point=Point([1., 2., 0.]), direction=Vector([4., 3., 0.])), _BaseArray([5., 4., 3.])]

    """
    # Convert objects to the base array class so we can get/set the dimension.
    objs = list(_to_arrays(*objs))

    dim_max = max([obj.get_dimension() for obj in objs])

    for obj in objs:
        yield obj.set_dimension(dim_max)


def norm_dim(func):
    """
    Decorator to normalize the dimensions of all inputs.

    The dimension of each array is set to the largest dimension of the input arrays.

    """

    def inner(*objs, **kwargs):

        objs_normalized = _normalize_dimension(*objs)
        return func(*objs_normalized, **kwargs)

    return inner


class _BaseArray(np.ndarray):
    """Private base class for spatial objects based on a single NumPy array."""

    @require("The input array must not be empty.", lambda args: len(args.array_like) > 0)
    @require("The input array must only contain finite numbers.", lambda args: np.all(np.isfinite(args.array_like)))
    def __new__(cls, array_like):

        array = np.array(array_like, dtype=float)

        # We cast the input array to be our class type.
        obj = np.asarray(array).view(cls)

        return obj

    def __array_finalize__(self, obj):

        if obj is None:
            return

    def get_dimension(self):

        if self.ndim == 1:
            return self.size
        else:
            return self.shape[0]

    @ensure(
        "The output must have the same class as the input.", lambda args, result: isinstance(result, type(args.self))
    )
    def set_dimension(self, dim):

        if self.ndim == 1:
            array = _set_dimension_1d(self, dim)
        else:
            array = _set_dimension_2d(self, dim)

        return self.__class__(array)


class _BaseArray1D(_BaseArray):
    """Private base class for spatial objects based on a single 1D NumPy array."""

    @require("The input array must be 1D.", lambda args: np.array(args.array_like).ndim == 1)
    @ensure(
        "The output must be a 1D array with the input length.",
        lambda args, result: result.shape == (len(args.array_like),),
    )
    def __new__(cls, array_like):

        return super().__new__(cls, array_like)

    @norm_dim
    def is_close(self, other, **kwargs):
        """Check if array is close to another array."""
        return np.allclose(self, other, **kwargs)

    @norm_dim
    @ensure("The output must be the same class as the input.", lambda args, result: isinstance(result, type(args.self)))
    def add(self, vector):
        """
        Add a vector to the array.

        Parameters
        ----------
        vector : Array
            Input array.

        Returns
        -------
        Array

        Examples
        --------
        >>> from skspatial.objects import Point, Vector

        >>> point = Point([1, 2])
        >>> point.add([2, 9, 1])
        Point([ 3., 11.,  1.])

        >>> point.add([-1, 5, 0])
        Point([0., 7., 0.])

        >>> vector = Vector([5, 9, 1])
        >>> vector.add([1])
        Vector([6., 9., 1])

        >>> vector.add([1, 2, 3, 4])
        Vector([6., 11., 4., 4])

        """
        return self.__class__(self + vector)

    @ensure("The output must be the same class as the input.", lambda args, result: isinstance(result, type(args.self)))
    def subtract(self, vector):

        return self.add(-np.array(vector))


class _BaseArray2D(_BaseArray):
    """Private base class for spatial objects based on a single 2D NumPy array."""

    @require("The input array must be 2D.", lambda args: np.array(args.array_like).ndim == 2)
    def __new__(cls, array_like):

        return super().__new__(cls, array_like)
