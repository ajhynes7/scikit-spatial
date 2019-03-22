import numpy as np
from dpcontracts import ensure
from numpy.linalg import matrix_rank

from skspatial.objects.base_array import _BaseArray1D, _BaseArray2D
from skspatial.objects.vector import Vector


class Point(_BaseArray1D):
    """Point implemented as an ndarray subclass."""

    def __new__(cls, array_like):

        return super().__new__(cls, array_like)

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

        return vector.norm()


class Points(_BaseArray2D):
    """
    Multiple points in space represented as a 2D NumPy array.

    Each row in the array represents a point in space.

    Parameters
    ----------
    points : {array_like, sequence}
        Multiple points in space.
        Either an array_like or a sequence of array_likes.
        The points must all have the same length.

    Examples
    --------
    >>> import numpy as np
    >>> from skspatial.objects import Points

    >>> points = ([1, 2, 0], [5, 4, 3], [4, 0, 0])

    >>> Points(points)
    Points([[1., 2., 0.],
            [5., 4., 3.],
            [4., 0., 0.]])

    >>> array = np.array([[1, 2], [5, 4]])

    >>> Points(array)
    Points([[1., 2.],
            [5., 4.]])

    """

    def __new__(cls, points):

        array_2d = np.stack(points)

        return super().__new__(cls, array_2d)

    @ensure("The output must be Points.", lambda _, result: isinstance(result, Points))
    @ensure(
        "The output points must have the same dimension.", lambda args, result: result.shape[1] == args.self.shape[1]
    )
    @ensure(
        "There must be fewer or an equal number of rows.", lambda args, result: result.shape[0] <= args.self.shape[0]
    )
    def unique(self):
        """
        Return unique points.

        The output contains the unique rows of the original array.

        Returns
        -------
        Points
            (n, d) array of n unique points with dimension d.

        """
        return self.__class__(np.unique(self, axis=0))

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
        >>> from skspatial.objects import Points

        >>> Points([[1, 2, 3], [2, 2, 3]]).centroid()
        Point([1.5, 2. , 3. ])

        """
        return Point(self.mean(axis=0))

    @ensure("The first output must have type Points", lambda _, result: isinstance(result[0], Points))
    @ensure("The second output must have type Point", lambda _, result: isinstance(result[1], Point))
    @ensure("The centered points must have the input shape", lambda args, result: result[0].shape == args.self.shape)
    @ensure("The centroid must have shape (dim,).", lambda args, result: result[1].shape == (args.self.shape[1],))
    def mean_center(self):
        """
        Mean-center the points.

        The centroid of the points is subtracted from the points.

        Returns
        -------
        points_centered : Points
            (n, dim) array of mean-centered points.
        centroid : Point
            (dim,) array for the centroid of the points.

        Examples
        --------
        >>> from skspatial.objects import Points

        >>> points, centroid = Points([[4, 4, 4], [2, 2, 2]]).mean_center()
        >>> points
        Points([[ 1.,  1.,  1.],
                [-1., -1., -1.]])

        >>> centroid
        Point([3., 3., 3.])

        """
        centroid = self.centroid()
        points_centered = self - centroid

        return points_centered, centroid

    def affine_rank(self, **kwargs):
        """
        Return the affine rank of the points.

        The affine rank is the dimension of the smallest affine space that contains the points.
        A rank of 1 means the points are collinear, and a rank of 2 means they are coplanar.

        Parameters
        ----------
        kwargs : dict, optional
            Additional keywords passed to `np.linalg.matrix_rank`.

        Returns
        -------
        int
            Affine rank of the points.

        Examples
        --------
        >>> from skspatial.objects import Points

        >>> Points([[5, 5], [5, 5]]).affine_rank()
        0

        >>> Points([[5, 3], [-6, 20]]).affine_rank()
        1

        >>> Points([[0, 0], [1, 1], [2, 2]]).affine_rank()
        1

        >>> Points([[0, 0], [1, 0], [2, 2]]).affine_rank()
        2

        >>> Points([[0, 1, 0], [1, 1, 0], [2, 2, 2]]).affine_rank()
        2

        >>> Points([[0, 0], [0, 1], [1, 0], [1, 1]]).affine_rank()
        2

        >>> Points([[1, 3, 2], [3, 4, 5], [2, 1, 5], [5, 9, 8]]).affine_rank()
        3

        """
        # Remove duplicate points so they do not affect the centroid.
        points_centered, _ = self.unique().mean_center()

        return matrix_rank(points_centered, **kwargs)

    def are_concurrent(self, **kwargs):
        """Check if the points are all contained in one point."""
        return self.affine_rank(**kwargs) == 0

    def are_collinear(self, **kwargs):
        """Check if the points are all contained in one line."""
        return self.affine_rank(**kwargs) <= 1

    def are_coplanar(self, **kwargs):
        """Check if the points are all contained in one plane."""
        return self.affine_rank(**kwargs) <= 2

    def is_close(self, other, **kwargs):
        """Check if this set of points is close to another."""
        return np.allclose(self, other, **kwargs)
