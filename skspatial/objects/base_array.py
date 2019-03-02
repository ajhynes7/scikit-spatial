"""Base classes for spatial objects based on a single NumPy array (Point and Vector)."""

import numpy as np
from dpcontracts import require, ensure, types


class _BaseArray:
    """Private base class for Point and Vector classes."""

    @require(
        "The input length must be one to three.",
        lambda args: len(args.array_like) in [1, 2, 3],
    )
    @require(
        "The input array must only contain finite numbers.",
        lambda args: np.all(np.isfinite(args.array_like)),
    )
    @ensure(
        "The output array must be 3D.", lambda args, result: args.self.array.size == 3
    )
    def __init__(self, array_like):
        """Convert the array to 3D by appending zeros."""
        n_dimensions = len(array_like)
        array_padding = np.zeros(3 - n_dimensions)

        self.array = np.concatenate((np.array(array_like), array_padding))

    def __eq__(self, other):

        return isinstance(self, type(other)) and np.all(self.array == other.array)

    @require(
        "The input must have the same type as the object.",
        lambda args: isinstance(args.self, type(args.other)),
    )
    def is_close(self, other, **kwargs):
        """Check if array is close to another array."""
        return np.allclose(self.array, other.array, **kwargs)


class _Point(_BaseArray):
    """Private parent class for Point."""
    def __init__(self, array_like):
        super().__init__(array_like)


class _Vector(_BaseArray):
    """Private parent class for Vector."""
    def __init__(self, array_like):
        super().__init__(array_like)

    @classmethod
    @types(point_a=_Point, point_b=_Point)
    def from_points(cls, point_a, point_b):
        """
        Instantiate a vector from point A to point B.

        Parameters
        ----------
        point_a : Point
            Input point A.
        point_b : Point
            Input point B.

        Returns
        -------
        Vector
            Vector from point A to point B.

        Examples
        --------
        >>> _Vector.from_points(Point((0, 0)), Point((1, 0)))
        Vector([1. 0. 0.])

        >>> _Vector.from_points(Point((5, 2)), Point((-2, 8)))
        Vector([-7.  6.  0.])

        >>> _Vector.from_points(Point((3, 1, 1)), Point((7, 7)))
        Vector([ 4.  6. -1.])

        """
        return cls(point_b.array - point_a.array)
