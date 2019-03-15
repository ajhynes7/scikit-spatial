import numpy as np
from dpcontracts import require, ensure


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

    def dot(self, other):
        """Return the dot product with another array."""
        return np.dot(self, _BaseArray1D(other))

    def is_close(self, other, **kwargs):
        """Check if array is close to another array."""
        return np.allclose(self, _BaseArray1D(other), **kwargs)
