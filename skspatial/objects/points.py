"""Module for the Points class."""

import numpy as np
from numpy.linalg import matrix_rank

from skspatial.objects._base_array import _BaseArray2D
from skspatial.objects.point import Point
from skspatial.plotting import _scatter_2d, _scatter_3d


class Points(_BaseArray2D):
    """
    Multiple points in space implemented as a 2D array.

    The array is a subclass of :class:`numpy.ndarray`.
    Each row in the array represents a point in space.

    Parameters
    ----------
    points : array_like
        (N, D) array representing N points with dimension D.

    Raises
    ------
    ValueError
        If the array is empty, the values are not finite,
        or the dimension is not two.

    Examples
    --------
    >>> from skspatial.objects import Points

    >>> points = Points([[1, 2, 0], [5, 4, 3]])

    >>> points
    Points([[1, 2, 0],
            [5, 4, 3]])

    >>> points.dimension
    3

    The object inherits methods from :class:`numpy.ndarray`.

    >>> points.mean(axis=0)
    Points([3. , 3. , 1.5])

    >>> Points([])
    Traceback (most recent call last):
    ...
    ValueError: The array must not be empty.

    >>> import numpy as np

    >>> Points([[1, 2], [1, np.nan]])
    Traceback (most recent call last):
    ...
    ValueError: The values must all be finite.

    >>> Points([1, 2, 3])
    Traceback (most recent call last):
    ...
    ValueError: The array must be 2D.

    """

    def __new__(cls, points):
        """Create a new Points object."""
        return super().__new__(cls, points)

    def unique(self):
        """
        Return unique points.

        The output contains the unique rows of the original array.

        Returns
        -------
        Points
            (N, D) array of N unique points with dimension D.

        """
        return self.__class__(np.unique(self, axis=0))

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

    def mean_center(self):
        """
        Mean-center the points.

        The centroid of the points is subtracted from the points.

        Returns
        -------
        points_centered : (N, D) Points
            Array of N mean-centered points with dimension D.
        centroid : (D,) Point
            Centroid of the points.

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
            Additional keywords passed to :func:`numpy.linalg.matrix_rank`

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
        """
        Check if the points are all contained in one point.

        Parameters
        ----------
        kwargs : dict, optional
            Additional keywords passed to :func:`numpy.linalg.matrix_rank`

        """
        return self.affine_rank(**kwargs) == 0

    def are_collinear(self, **kwargs):
        """
        Check if the points are all contained in one line.

        Parameters
        ----------
        kwargs : dict, optional
            Additional keywords passed to :func:`numpy.linalg.matrix_rank`

        """
        return self.affine_rank(**kwargs) <= 1

    def are_coplanar(self, **kwargs):
        """
        Check if the points are all contained in one plane.

        Parameters
        ----------
        kwargs : dict, optional
            Additional keywords passed to :func:`numpy.linalg.matrix_rank`

        """
        return self.affine_rank(**kwargs) <= 2

    def plot_2d(self, ax_2d, **kwargs):
        """
        Plot the points on a 2D scatter plot.

        Parameters
        ----------
        ax_2d : Axes
            Instance of :class:`~matplotlib.axes.Axes`.
        kwargs : dict, optional
            Additional keywords passed to :meth:`~matplotlib.axes.Axes.scatter`.

        """
        _scatter_2d(ax_2d, self, **kwargs)

    def plot_3d(self, ax_3d, **kwargs):
        """
        Plot the points on a 3D scatter plot.

        Parameters
        ----------
        ax_3d : Axes3D
            Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
        kwargs : dict, optional
            Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.scatter`.

        """
        _scatter_3d(ax_3d, self, **kwargs)
