import numpy as np
from dpcontracts import require, ensure


def norm_dim(func):

    def inner(*args):

        # Ensure all arrays have the same length.
        arrays = _BaseArray1D.normalize_dimensions(*args)

        return func(*arrays)

    return inner


class _BaseArray1D(np.ndarray):
    """Private base class for spatial objects based on a single 1D NumPy array."""

    @require("The input array must not be empty.", lambda args: len(args.array_like) > 0)
    @require("The input array must be 1D.", lambda args: np.array(args.array_like).ndim == 1)
    @require("The input array must only contain finite numbers.", lambda args: np.all(np.isfinite(args.array_like)))
    @ensure("The output must be a 1D array with the input length.", lambda args, result: result.shape == (len(args.array_like),))
    def __new__(cls, array_like):

        array = np.array(array_like, dtype=float)

        # We cast the input array to be our class type.
        obj = np.asarray(array).view(cls)

        return obj

    def __array_finalize__(self, obj):

        if obj is None:
            return

    @norm_dim
    def dot(self, other):
        """Return the dot product with another array."""
        return np.dot(self, other)

    @norm_dim
    def is_close(self, other, **kwargs):
        """Check if array is close to another array."""
        return np.allclose(self, other, **kwargs)

    @require(
        "The desired dimension cannot be less than the array dimension.", lambda args: args.dim >= args.self.size,
    )
    @ensure(
        "The output must have the desired dimensions.", lambda args, result: result.shape == (args.dim,),
    )
    @ensure("The output must have the same class as the input.", lambda args, result: isinstance(result, type(args.self)))
    def set_dimension(self, dim):
        """
        Set the desired dimension (length) of the 1D array.

        Parameters
        ----------
        dim : int
            Desired dimension of the array.
            Must be greater or equal to the current array dimension.

        Returns
        -------
        array
            Array with the same type as the input.

        Examples
        --------
        >>> from skspatial.objects import Point, Vector

        >>> Point([1, 1]).set_dimension(3)
        Point([1., 1., 0.])

        >>> Vector([1, 1]).set_dimension(4)
        Vector([1., 1., 0., 0.])

        >>> Vector([1, 1]).set_dimension(1)
        Traceback (most recent call last):
        ...
        dpcontracts.PreconditionError: The desired dimension cannot be less than the array dimension.

        """
        n_zeros = dim - self.size
        array_padded = np.pad(self, (0, n_zeros), 'constant')

        return self.__class__(array_padded)

    @classmethod
    def normalize_dimensions(cls, *arrays):

        dim_max = np.max([len(x) for x in arrays])

        return [cls(x).set_dimension(dim_max) for x in arrays]


class _BaseArray2D(np.ndarray):
    """Private base class for spatial objects based on a single 2D NumPy array."""

    @require("The input array must only contain finite numbers.", lambda args: np.all(np.isfinite(args.array_like)))
    def __new__(cls, array_like):

        # We cast the input array to be our class type.
        obj = np.asarray(array_like).view(cls)

        return obj

    def __array_finalize__(self, obj):

        if obj is None:
            return

    @require(
        "The points dimension cannot be greater than the desired dimension.", lambda args: args.dim > args.self.shape[1],
    )
    @ensure(
        "The output must have the desired dimensions.", lambda args, result: result.shape == (len(args.self), args.dim),
    )
    def set_dimension(self, dim):
        """
        Change the dimension of the points.

        """
        n_rows, n_cols = self.shape
        padding = np.zeros((n_rows, dim - n_cols))

        return np.hstack([self, padding])
