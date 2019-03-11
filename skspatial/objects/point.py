import numpy as np
from dpcontracts import ensure

from .base_array import _BaseArray1D
from .vector import Vector


class Point(_BaseArray1D):
    """Point implemented as an ndarray subclass."""

    def __new__(cls, array_like):

        return super().__new__(cls, array_like)

    @ensure("The result must be zero or greater.", lambda _, result: result >= 0)
    @ensure("The output must be a numpy scalar.", lambda _, result: isinstance(result, np.number))
    def distance_point(self, other):
        """Compute the distance from self to another point."""
        vector = Vector.from_points(self, other)

        return vector.magnitude

    def is_collinear(self, point_a, point_b, **kwargs):
        """
        Check if this point is collinear to two other points A and B.

        Points A, B, C are collinear if vector AB is parallel to vector AC.

        Parameters
        ----------
        point_a : array_like
            Input point A.
        point_b : array_like
            Input point B.

        kwargs : dict, optional
            Additional keywords passed to `np.allclose`.

        Returns
        -------
        bool
            True if points are collinear; false otherwise.

        Examples
        --------
        >>> Point([0, 1]).is_collinear([1, 0], [1, 2])
        False

        >>> Point([1, 1]).is_collinear(Point([2, 2]), Point([5, 5]), atol=1e-7)
        True

        """
        vector_to_a = Vector.from_points(self, point_a)
        vector_to_b = Vector.from_points(self, point_b)

        return vector_to_a.is_parallel(vector_to_b, **kwargs)
