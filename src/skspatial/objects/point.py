"""Module for the Point class."""
import numpy as np
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D

from skspatial.objects._base_array import _BaseArray1D
from skspatial.objects.vector import Vector
from skspatial.plotting import _scatter_2d
from skspatial.plotting import _scatter_3d
from skspatial.typing import array_like


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
    array(2.)

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

    def distance_point(self, other: array_like) -> np.float64:
        """
        Return the distance to another point.

        Parameters
        ----------
        other : array_like
            Other point.

        Returns
        -------
        np.float64
            Distance between the points.

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

    def plot_2d(self, ax_2d: Axes, **kwargs) -> None:
        """
        Plot the point on a 2D scatter plot.

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
            >>> from skspatial.objects import Point

            >>> _, ax = plt.subplots()

            >>> Point([1, 2]).plot_2d(ax, c='k', s=100)

        """
        _scatter_2d(ax_2d, self.reshape(1, -1), **kwargs)

    def plot_3d(self, ax_3d: Axes3D, **kwargs) -> None:
        """
        Plot the point on a 3D scatter plot.

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

            >>> from skspatial.objects import Point

            >>> fig = plt.figure()
            >>> ax = fig.add_subplot(111, projection='3d')

            >>> Point([1, 2, 3]).plot_3d(ax, c='k', s=100)

        """
        _scatter_3d(ax_3d, self.reshape(1, -1), **kwargs)
