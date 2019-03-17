import numpy as np
from dpcontracts import ensure
from numpy.linalg import matrix_rank

from .base_array import _BaseArray1D, _BaseArray2D
from .vector import Vector


class Point(_BaseArray1D):
    """Point implemented as an ndarray subclass."""

    def __new__(cls, array_like):

        return super().__new__(cls, array_like)

    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    def add(self, vector):
        """
        Add a vector to the point.

        Parameters
        ----------
        vector : array_like
            Input vector.

        Returns
        -------
        Point
            Point after adding vector.

        Examples
        --------
        >>> from skspatial.objects import Point

        >>> point = Point([1, 2, 0])
        >>> point.add([2, 9, 1])
        Point([ 3., 11.,  1.])

        >>> point.add([-1, 5, 0])
        Point([0., 7., 0.])

        """
        return self + Vector(vector)

    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    def subtract(self, vector):
        """Subtract a vector from the point."""
        return self - Vector(vector)

    @ensure("The result must be zero or greater.", lambda _, result: result >= 0)
    @ensure("The output must be a numpy scalar.", lambda _, result: isinstance(result, np.number))
    def distance_point(self, other):
        """
        Compute the distance from self to another point.

        Parameters
        ----------
        other : array_like
            Input point.

        Returns
        -------
        scalar
            Distance between points.

        Examples
        --------
        >>> from skspatial.objects import Point

        >>> point = Point([1, 2])
        >>> point.distance_point([1, 2])
        0.0

        >>> point.distance_point([-1, 2])
        2.0

        >>> Point([1, 2, 0]).distance_point([1, 2, 3])
        3.0

        """
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

        >>> Point([1, 1]).is_collinear([2, 2], [5, 5], atol=1e-7)
        True

        """
        vector_to_a = Vector.from_points(self, point_a)
        vector_to_b = Vector.from_points(self, point_b)

        return vector_to_a.is_parallel(vector_to_b, **kwargs)


class Points(_BaseArray2D):

    def __new__(cls, points):

        points = Point.normalize_dimensions(*points)
        array_2d = np.stack(points)

        return super().__new__(cls, array_2d)

    @ensure("The output length must be the input width.", lambda args, result: result.size == args.self.shape[1])
    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    def centroid(self):
        """
        Return the centroid of the points.

        Returns
        -------
        Point
            Centroid of the points.

        Examples
        --------
        >>> Points([[1, 2, 3], [2, 2, 3]]).centroid()
        Point([1.5, 2. , 3. ])

        """
        return Point(self.mean(axis=0))

    @ensure("The centered points must have the input shape", lambda args, result: result.shape == args.self.shape)
    def mean_center(self):
        """
        Mean-center the points.

        The centroid of the points is subtracted from the points.

        Returns
        -------
        Points
            (n, d) array of mean-centered points.

        Examples
        --------
        >>> Points([[4, 4, 4], [2, 2, 2]]).mean_center()
        Points([[ 1.,  1.,  1.],
                [-1., -1., -1.]])

        """
        return self - self.centroid()

    def affine_rank(self):
        """
        Return the affine rank of the points.

        The affine rank is the dimension of the smallest affine space that contains the points.
        A rank of 1 means the points are collinear, and a rank of 2 means they are coplanar.

        Returns
        -------
        int
            Affine rank of the points.

        Examples
        --------
        >>> Points([[5, 3], [-6, 20]]).affine_rank()
        1

        >>> Points([[0, 0], [1, 1], [2, 2]]).affine_rank()
        1

        >>> Points([[0, 1, 0], [1, 1, 0], [2, 2, 2]]).affine_rank()
        2

        >>> Points([[0, 0], [0, 1], [1, 0], [1, 1]]).affine_rank()
        2

        >>> Points([[1, 3, 2], [3, 4, 5], [2, 1, 5], [5, 9, 8]]).affine_rank()
        3

        """
        points_centered = self.mean_center()

        return matrix_rank(points_centered)

    def are_collinear(self):
        """Check if the points are all contained on one line."""
        return self.affine_rank() <= 1

    def are_coplanar(self):
        """Check if the points are all contained on one plane."""
        return self.affine_rank() <= 2
