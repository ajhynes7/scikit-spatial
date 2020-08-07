"""Private functions used for plotting spatial objects with Matplotlib."""

from typing import Any, Callable, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D

from skspatial.typing import array_like


def _scatter_2d(ax_2d: Axes, points: array_like, **kwargs) -> None:
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


def _scatter_3d(ax_3d: Axes3D, points: array_like, **kwargs) -> None:
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

    Raises
    ------
    ValueError
        If the axis is not an instance of Axes3D.

    """
    if not isinstance(ax_3d, Axes3D):
        raise ValueError("Axis must be instance of class Axes3D.")

    array = np.array(points)
    ax_3d.scatter(array[:, 0], array[:, 1], array[:, 2], **kwargs)


def _connect_points_2d(ax_2d: Axes, point_a: array_like, point_b: array_like, **kwargs) -> None:
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
    point_a = np.array(point_a)
    point_b = np.array(point_b)

    xs = [point_a[0], point_b[0]]
    ys = [point_a[1], point_b[1]]

    ax_2d.plot(xs, ys, **kwargs)


def _connect_points_3d(ax_3d: Axes3D, point_a: array_like, point_b: array_like, **kwargs) -> None:
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

    Raises
    ------
    ValueError
        If the axis is not an instance of Axes3D.

    """
    if not isinstance(ax_3d, Axes3D):
        raise ValueError("Axis must be instance of class Axes3D.")

    point_a = np.array(point_a)
    point_b = np.array(point_b)

    xs = [point_a[0], point_b[0]]
    ys = [point_a[1], point_b[1]]
    zs = [point_a[2], point_b[2]]

    ax_3d.plot(xs, ys, zs, **kwargs)


def _plotter(obj: Any, **kwargs) -> Union[Callable[[Axes], None], Callable[[Axes3D], None]]:
    """Return a function that plots the object when passed a matplotlib axes."""
    if obj.dimension == 2:

        if not hasattr(obj, 'plot_2d'):
            raise ValueError("The object cannot be plotted in 2D.")

        return lambda ax: obj.plot_2d(ax, **kwargs)

    if obj.dimension == 3:

        if not hasattr(obj, 'plot_3d'):
            raise ValueError("The object cannot be plotted in 3D.")

        return lambda ax: obj.plot_3d(ax, **kwargs)

    raise ValueError("The dimension must be 2 or 3.")


def plot_2d(*plotters: Callable) -> Tuple:
    """Plot multiple spatial objects in 2D."""
    fig, ax = plt.subplots()

    for plotter in plotters:
        plotter(ax)

    return fig, ax


def plot_3d(*plotters: Callable) -> Tuple:
    """Plot multiple spatial objects in 3D."""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for plotter in plotters:
        plotter(ax)

    return fig, ax
