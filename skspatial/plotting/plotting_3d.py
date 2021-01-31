"""Functions to plot spatial objects in 3D."""

from functools import singledispatch
from typing import Optional

import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from skspatial.objects.line import Line
from skspatial.objects.plane import Plane
from skspatial.objects.point import Point
from skspatial.objects.points import Points
from skspatial.objects.sphere import Sphere
from skspatial.objects.triangle import Triangle
from skspatial.objects.vector import Vector
from skspatial.typing import array_like


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

    xs = [point_a[0], point_b[0]]
    ys = [point_a[1], point_b[1]]
    zs = [point_a[2], point_b[2]]

    ax_3d.plot(xs, ys, zs, **kwargs)


def _plot_surface(
    obj,
    ax_3d: Axes3D,
    kwargs_for_mesh: Optional[dict],
    kwargs_for_plot_surface: Optional[dict],
):
    """Plot the 3D surface of a spatial object."""
    if kwargs_for_mesh is None:
        kwargs_for_mesh = {}

    if kwargs_for_plot_surface is None:
        kwargs_for_plot_surface = {}

    X, Y, Z = obj.to_mesh(**kwargs_for_mesh)
    ax_3d.plot_surface(X, Y, Z, **kwargs_for_plot_surface)


@singledispatch
def plot_3d(point: Point, ax_3d: Axes3D, **kwargs) -> None:
    """
    Plot a point on a 3D scatter plot.

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
    _scatter_3d(ax_3d, point.reshape(1, -1), **kwargs)


@plot_3d.register  # type: ignore[no-redef]
def _(vector: Vector, ax_3d: Axes3D, point: array_like = (0, 0, 0), scalar: float = 1, **kwargs) -> None:
    """
    Plot a 3D vector.

    The vector is plotted by connecting two 3D points
    (the head and tail of the vector).

    Parameters
    ----------
    ax_3d : Axes3D
        Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
    point : array_like, optional
        Position of the vector tail (default is origin).
    scalar : {int, float}, optional
        Value used to scale the vector (default 1).
    kwargs : dict, optional
        Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot`.

    Examples
    --------
    .. plot::
        :include-source:

        >>> import matplotlib.pyplot as plt
        >>> from mpl_toolkits.mplot3d import Axes3D

        >>> from skspatial.objects import Vector

        >>> fig = plt.figure()
        >>> ax = fig.add_subplot(111, projection='3d')

        >>> Vector([-1, 1, 1]).plot_3d(ax, point=(1, 2, 3), c='r')

    """
    point_2 = np.array(point) + scalar * vector

    _connect_points_3d(ax_3d, point, point_2, **kwargs)


@plot_3d.register  # type: ignore[no-redef]
def _(self: Points, ax_3d: Axes3D, **kwargs) -> None:
    """
    Plot points on a 3D scatter plot.

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


@plot_3d.register  # type: ignore[no-redef]
def _(line: Line, ax_3d: Axes3D, t_1: float = 0, t_2: float = 1, **kwargs) -> None:
    """
    Plot a 3D line.

    The line is plotted by connecting two 3D points.

    Parameters
    ----------
    ax_3d : Axes3D
        Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
    t_1, t_2 : {int, float}
        Parameters to determine points 1 and 2 along the line.
        These are passed to :meth:`Line.to_point`.
        Defaults are 0 and 1.
    kwargs : dict, optional
        Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot`.

    Examples
    --------
    .. plot::
        :include-source:

        >>> import matplotlib.pyplot as plt
        >>> from mpl_toolkits.mplot3d import Axes3D

        >>> from skspatial.objects import Line

        >>> fig = plt.figure()
        >>> ax = fig.add_subplot(111, projection='3d')

        >>> line = Line([1, 2, 3], [0, 1, 1])

        >>> line.plot_3d(ax, c='k')
        >>> line.point.plot_3d(ax, s=100)

    """
    point_1 = line.to_point(t_1)
    point_2 = line.to_point(t_2)

    _connect_points_3d(ax_3d, point_1, point_2, **kwargs)


@plot_3d.register(Plane)  # type: ignore[no-redef]
@plot_3d.register(Sphere)  # type: ignore[no-redef]
def _(
    obj,
    ax_3d: Axes3D,
    kwargs_for_mesh: Optional[dict] = None,
    kwargs_for_plot_surface: Optional[dict] = None,
):
    _plot_surface(obj, ax_3d, kwargs_for_mesh, kwargs_for_plot_surface)


@plot_3d.register  # type: ignore[no-redef]
def _(triangle: Triangle, ax_3d: Axes3D, part: str = "points", **kwargs: str) -> None:
    """
    Plot a triangle in 3D.

    Parameters
    ----------
    ax_3d : Axes3D
        Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
    part : str, optional
        Part of the triangle to plot.
        Either 'points' or 'lines' (default 'points').
    kwargs : dict, optional
        Additional keywords passed to :meth:`~skspatial.objects.Point.plot_3d` or
        :meth:`~skspatial.objects.Line.plot_3d`.

    Examples
    --------
    .. plot::
        :include-source:

        >>> import matplotlib.pyplot as plt
        >>> from skspatial.objects import Triangle

        >>> triangle = Triangle([0, 0], [1, 0], [0, 1])

        >>> _, ax = plt.subplots()

        >>> triangle.plot_2d(ax, part='points', s=100, zorder=3)
        >>> triangle.plot_2d(ax, part='lines', c='k')

    """
    if part == "points":
        for point in triangle.multiple("point", "ABC"):
            point.plot_3d(ax_3d, **kwargs)

    elif part == "lines":
        for line in triangle.multiple("line", "abc"):
            line.plot_3d(ax_3d, **kwargs)
