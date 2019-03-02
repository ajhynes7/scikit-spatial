from dpcontracts import ensure, types

from .base_array import _Point, _Vector


class Point(_Point):
    def __init__(self, array_like):

        super().__init__(array_like)

    def __repr__(self):

        return f"Point({self.array})"

    @types(vector=_Vector)
    def add(self, vector):
        """Return a new point by adding a vector."""
        return Point(self.array + vector.array)

    @types(vector=_Vector)
    def subtract(self, vector):
        """Return a new point by subtracting a vector."""
        return self.add(vector.reverse())

    @types(other=_Point)
    @ensure("The result must be zero or greater.", lambda _, result: result >= 0)
    def distance(self, other):
        """Compute the distance from this point to another point."""
        vector = _Vector.from_points(self, other)

        return vector.magnitude

    @types(point_a=_Point, point_b=_Point)
    def is_collinear(self, point_a, point_b, **kwargs):
        """
        Check if this point is collinear to two other points A and B.

        Points A, B, C are collinear if vector AB is parallel to vector AC.

        Parameters
        ----------
        point_a : Point
            Input point A.
        point_b : Point
            Input point B.

        kwargs : dict, optional
            Additional keywords passed to `np.allclose`.

        Returns
        -------
        bool
            True if points are collinear; false otherwise.

        Examples
        --------
        >>> Point([0, 1]).is_collinear(Point([1, 0]), Point([1, 2]))
        False

        >>> Point([1, 1]).is_collinear(Point([2, 2]), Point([5, 5]), atol=1e-7)
        True

        """
        vector_to_a = _Vector.from_points(self, point_a)
        vector_to_b = _Vector.from_points(self, point_b)

        return vector_to_a.is_parallel(vector_to_b, **kwargs)
