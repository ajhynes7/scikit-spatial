import numpy as np
from dpcontracts import require


class _BaseArray1D(np.ndarray):
    """Private base class for spatial objects based on a single 1D numpy array."""

    @require("The input array must be 1D.", lambda args: np.array(args.array_like).ndim == 1)
    @require("The input array must only contain finite numbers.", lambda args: np.all(np.isfinite(args.array_like)))
    def __new__(cls, array_like):

        n_dimensions = len(array_like)
        array_padding = np.zeros(3 - n_dimensions)

        array = np.concatenate((np.array(array_like), array_padding))

        # We cast the input array to be our class type.
        obj = np.asarray(array).view(cls)

        return obj

    def __array_finalize__(self, obj):

        if obj is None:
            return

    def is_close(self, other, **kwargs):
        """Check if array is close to another array."""
        return np.allclose(self, other, **kwargs)
