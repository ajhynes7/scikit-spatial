import numpy as np
from dpcontracts import require, ensure


class _BaseArray1D(np.ndarray):
    """Private base class for spatial objects based on a single 1D numpy array."""

    @require("The input array must be 1D.", lambda args: np.array(args.array_like).ndim == 1)
    @require("The input length must be one to three.", lambda args: len(args.array_like) in [1, 2, 3])
    @require("The input array must only contain finite numbers.", lambda args: np.all(np.isfinite(args.array_like)))
    @ensure("The output must be a 1D array with length three.", lambda _, result: result.shape == (3,))
    def __new__(cls, array_like):

        array = np.array(array_like)

        # Ensure the array has length three.
        padding = np.zeros(3 - array.size)
        array = np.concatenate((array, padding))

        # We cast the input array to be our class type.
        obj = np.asarray(array).view(cls)

        return obj

    def __array_finalize__(self, obj):

        if obj is None:
            return

    def dot(self, other):
        """Return the dot product with another array."""
        return np.dot(self, _BaseArray1D(other))

    def is_close(self, other, **kwargs):
        """Check if array is close to another array."""
        return np.allclose(self, _BaseArray1D(other), **kwargs)
