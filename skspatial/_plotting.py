"""Private functions used for plotting spatial objects with Matplotlib."""

import numpy as np
from dpcontracts import types
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D


@types(ax_2d=Axes)
def _scatter_2d(ax_2d, points, **kwargs):
    """
    Plot points on a 2D scatter plot.

    Parameters
    ----------
    ax_2d : Axes
        Instance of :class:`~matplotlib.axes.Axes`.
    points : array_like
        2D points.
    kwargs : dict, optional
        Additional keywords passed to :meth:`~matplotlib.axes.Axes.scatter`.

    """
    array = np.array(points)
    ax_2d.scatter(array[:, 0], array[:, 1], **kwargs)


@types(ax_3d=Axes3D)
def _scatter_3d(ax_3d, points, **kwargs):
    """
    Plot points on a 3D scatter plot.

    Parameters
    ----------
    ax_3d : Axes3D
        Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
    points : array_like
        3D points.
    kwargs : dict, optional
        Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.scatter`.

    """
    array = np.array(points)
    ax_3d.scatter(array[:, 0], array[:, 1], array[:, 2], **kwargs)


@types(ax_2d=Axes)
def _connect_points_2d(ax_2d, point_a, point_b, **kwargs):
    """
    Plot a line between two 2D points.

    Parameters
    ----------
    ax_2d : Axes
        Instance of :class:`~matplotlib.axes.Axes`.
    point_a, point_b : array_like
        The two 2D points to be connected.
    kwargs : dict, optional
        Additional keywords passed to :meth:`~matplotlib.axes.Axes.plot`.

    """
    xs = [point_a[0], point_b[0]]
    ys = [point_a[1], point_b[1]]

    ax_2d.plot(xs, ys, **kwargs)


@types(ax_3d=Axes3D)
def _connect_points_3d(ax_3d, point_a, point_b, **kwargs):
    """
    Plot a line between two 3D points.

    Parameters
    ----------
    ax_3d : Axes3D
        Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
    point_a, point_b : array_like
        The two 3D points to be connected.
    kwargs : dict, optional
        Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot`.

    """
    xs = [point_a[0], point_b[0]]
    ys = [point_a[1], point_b[1]]
    zs = [point_a[2], point_b[2]]

    ax_3d.plot(xs, ys, zs, **kwargs)
