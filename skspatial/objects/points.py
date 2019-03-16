from dpcontracts import ensure
from numpy.linalg import matrix_rank

from .base_array import _BaseArray2D
from .point import Point


class Points(_BaseArray2D):

    def __new__(cls, array_like):

        return super().__new__(cls, array_like)

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
