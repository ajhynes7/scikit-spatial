"""Module for the Points class."""
from __future__ import annotations

from typing import cast

import numpy as np
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D
from numpy.linalg import matrix_rank

from skspatial.objects._base_array import _BaseArray2D
from skspatial.objects.point import Point
from skspatial.plotting import _scatter_2d
from skspatial.plotting import _scatter_3d


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
    array([3. , 3. , 1.5])

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

    def unique(self) -> Points:
        """
        Return unique points.

        The output contains the unique rows of the original array.

        Returns
        -------
        Points
            (N, D) array of N unique points with dimension D.

        Examples
        --------
        >>> from skspatial.objects import Points

        >>> points = Points([[1, 2, 3], [2, 3, 4], [1, 2, 3]])

        >>> points.unique()
        Points([[1, 2, 3],
                [2, 3, 4]])

        """
        return Points(np.unique(self, axis=0))

    def centroid(self) -> Point:
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
        centroid_ = cast(np.ndarray, self.mean(axis=0))

        return Point(centroid_)

    def mean_center(self, return_centroid: bool = False):
        """
        Mean-center the points by subtracting the centroid.

        Parameters
        ----------
        return_centroid : bool, optional
            If True, also return the original centroid of the points.

        Returns
        -------
        points_centered : (N, D) Points
            Array of N mean-centered points with dimension D.
        centroid : (D,) Point, optional
            Original centroid of the points. Only provided if `return_centroid` is True.

        Examples
        --------
        >>> from skspatial.objects import Points

        >>> points_centered, centroid = Points([[4, 4, 4], [2, 2, 2]]).mean_center(return_centroid=True)
        >>> points_centered
        Points([[ 1.,  1.,  1.],
                [-1., -1., -1.]])

        >>> centroid
        Point([3., 3., 3.])

        The centroid of the centered points is the origin.

        >>> points_centered.centroid()
        Point([0., 0., 0.])

        """
        centroid = self.centroid()
        points_centered = self - centroid

        if return_centroid:
            return points_centered, centroid

        return points_centered

    def normalize_distance(self) -> Points:
        """
        Normalize the distances of the points from the origin.

        The normalized points lie within a unit sphere centered on the origin.

        Returns
        -------
        Points
            Normalized points.

        Examples
        --------
        >>> from skspatial.objects import Points

        >>> points = Points([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        >>> points.normalize_distance().round(3)
        Points([[0.072, 0.144, 0.215],
                [0.287, 0.359, 0.431],
                [0.503, 0.574, 0.646]])

        The transformation can be chained with mean centering.

        >>> points.mean_center().normalize_distance().round(3)
        Points([[-0.577, -0.577, -0.577],
                [ 0.   ,  0.   ,  0.   ],
                [ 0.577,  0.577,  0.577]])

        """
        distances_to_points = np.linalg.norm(self, axis=1)

        return self / distances_to_points.max()

    def affine_rank(self, **kwargs) -> np.int64:
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
        np.int64
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
        points_centered = self.unique().mean_center()

        return matrix_rank(points_centered, **kwargs)

    def are_concurrent(self, **kwargs) -> bool:
        """
        Check if the points are all contained in one point.

        Parameters
        ----------
        kwargs : dict, optional
            Additional keywords passed to :func:`numpy.linalg.matrix_rank`

        Returns
        -------
        bool
            True if points are concurrent; false otherwise.

        Examples
        --------
        >>> from skspatial.objects import Points

        >>> Points([[0, 0], [1, 1], [1, 1]]).are_concurrent()
        False

        >>> Points([[1, 1], [1, 1], [1, 1]]).are_concurrent()
        True

        """
        return self.affine_rank(**kwargs) == 0

    def are_collinear(self, **kwargs) -> bool:
        """
        Check if the points are all contained in one line.

        Parameters
        ----------
        kwargs : dict, optional
            Additional keywords passed to :func:`numpy.linalg.matrix_rank`

        Returns
        -------
        bool
            True if points are collinear; false otherwise.

        Examples
        --------
        >>> from skspatial.objects import Points

        >>> Points(([0, 0, 0], [1, 2, 3], [2, 4, 6])).are_collinear()
        True

        >>> Points(([0, 0, 0], [1, 2, 3], [5, 2, 0])).are_collinear()
        False

        >>> Points(([0, 0], [1, 2], [5, 2], [6, 3])).are_collinear()
        False

        """
        return self.affine_rank(**kwargs) <= 1

    def are_coplanar(self, **kwargs) -> bool:
        """
        Check if the points are all contained in one plane.

        Parameters
        ----------
        kwargs : dict, optional
            Additional keywords passed to :func:`numpy.linalg.matrix_rank`

        Returns
        -------
        bool
            True if points are coplanar; false otherwise.

        Examples
        --------
        >>> from skspatial.objects import Points

        >>> Points([[1, 2], [9, -18], [12, 4], [2, 1]]).are_coplanar()
        True

        >>> Points([[1, 2], [9, -18], [12, 4], [2, 2]]).are_coplanar()
        True

        >>> Points([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]).are_coplanar()
        False

        """
        return self.affine_rank(**kwargs) <= 2

    def plot_2d(self, ax_2d: Axes, **kwargs) -> None:
        """
        Plot the points on a 2D scatter plot.

        Parameters
        ----------
        ax_2d : Axes
            Instance of :class:`~matplotlib.axes.Axes`.
        kwargs : dict, optional
            Additional keywords passed to :meth:`~matplotlib.axes.Axes.scatter`.

        Examples
        --------
        .. plot::
            :include-source:

            >>> import matplotlib.pyplot as plt

            >>> from skspatial.objects import Points

            >>> fig, ax = plt.subplots()
            >>> points = Points([[1, 2], [3, 4], [-4, 2], [-2, 3]])
            >>> points.plot_2d(ax, c='k')

        """
        _scatter_2d(ax_2d, self, **kwargs)

    def plot_3d(self, ax_3d: Axes3D, **kwargs) -> None:
        """
        Plot the points on a 3D scatter plot.

        Parameters
        ----------
        ax_3d : Axes3D
            Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
        kwargs : dict, optional
            Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.scatter`.

        Examples
        --------
        .. plot::
            :include-source:

            >>> import matplotlib.pyplot as plt
            >>> from mpl_toolkits.mplot3d import Axes3D

            >>> from skspatial.objects import Points

            >>> fig = plt.figure()
            >>> ax = fig.add_subplot(111, projection='3d')

            >>> points = Points([[1, 2, 1], [3, 2, -7], [-4, 2, 2], [-2, 3, 1]])
            >>> points.plot_3d(ax, s=75, depthshade=False)

        """
        _scatter_3d(ax_3d, self, **kwargs)
