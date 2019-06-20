"""Module for the Point class."""

from skspatial.objects._base_array import _BaseArray1D
from skspatial.objects.vector import Vector
from skspatial.plotting import _scatter_2d, _scatter_3d


class Point(_BaseArray1D):
    """
    A point in space implemented as a 1D array.

    The array is a subclass of :class:`numpy.ndarray`.

    Parameters
    ----------
    array : array_like
        Input array.

    Attributes
    ----------
    dimension : int
        Dimension of the point.

    Raises
    ------
    ValueError
        If the array is empty, the values are not finite,
        or the dimension is not one.

    Examples
    --------
    >>> from skspatial.objects import Point

    >>> point = Point([1, 2, 3])

    >>> point.dimension
    3

    The object inherits methods from :class:`numpy.ndarray`.

    >>> point.mean()
    Point(2.)

    >>> Point([])
    Traceback (most recent call last):
    ...
    ValueError: The array must not be empty.

    >>> import numpy as np

    >>> Point([1, 2, np.nan])
    Traceback (most recent call last):
    ...
    ValueError: The values must all be finite.

    >>> Point([[1, 2], [3, 4]])
    Traceback (most recent call last):
    ...
    ValueError: The array must be 1D.

    """

    def __new__(cls, array):
        """Create a new Point object."""
        return super().__new__(cls, array)

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

    def plot_2d(self, ax_2d, **kwargs):
        """
        Plot the point on a 2D scatter plot.

        Parameters
        ----------
        ax_2d : Axes
            Instance of :class:`~matplotlib.axes.Axes`.
        kwargs : dict, optional
            Additional keywords passed to :meth:`~matplotlib.axes.Axes.scatter`.

        """
        _scatter_2d(ax_2d, self.reshape(1, -1), **kwargs)

    def plot_3d(self, ax_3d, **kwargs):
        """
        Plot the point on a 3D scatter plot.

        Parameters
        ----------
        ax_3d : Axes3D
            Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
        kwargs : dict, optional
            Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.scatter`.

        """
        _scatter_3d(ax_3d, self.reshape(1, -1), **kwargs)
