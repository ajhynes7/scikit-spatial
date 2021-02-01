"""Functions to plot spatial objects in 2D."""

from functools import singledispatch

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from skspatial.objects.circle import Circle
from skspatial.objects.line import Line
from skspatial.objects.point import Point
from skspatial.objects.points import Points
from skspatial.objects.triangle import Triangle
from skspatial.objects.vector import Vector
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
    xs = [point_a[0], point_b[0]]
    ys = [point_a[1], point_b[1]]

    ax_2d.plot(xs, ys, **kwargs)


@singledispatch
def plot_2d(point: Point, ax_2d: Axes, **kwargs) -> None:
    """
    Plot a point on a 2D scatter plot.

    Parameters
    ----------
    point : Point
        Input point.
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

        >>> point = Point([1, 2])

        >>> _, ax = plt.subplots()
        >>> plot_2d(point, ax, c='k', s=100)

    """
    _scatter_2d(ax_2d, point.reshape(1, -1), **kwargs)


@plot_2d.register  # type: ignore[no-redef]
def _(vector: Vector, ax_2d: Axes, point: array_like = (0, 0), scalar: float = 1, **kwargs) -> None:
    """
    Plot a 2D vector.

    The vector is plotted as an arrow.

    Parameters
    ----------
    vector: Vector
        Input vector.
    ax_2d : Axes
        Instance of :class:`~matplotlib.axes.Axes`.
    point : array_like, optional
        Position of the vector tail (default is origin).
    scalar : {int, float}, optional
        Value used to scale the vector (default 1).
    kwargs : dict, optional
        Additional keywords passed to :meth:`~matplotlib.axes.Axes.arrow`.

    Examples
    --------
    .. plot::
        :include-source:

        >>> import matplotlib.pyplot as plt

        >>> from skspatial.objects import Vector

        >>> vector = Vector([1, 1])

        >>> _, ax = plt.subplots()
        >>> plot_2d(vector, ax, point=(-3, 5), scalar=2, head_width=0.5)
        >>> limits = ax.axis([-5, 5, 0, 10])

    """
    x, y = point
    dx, dy = scalar * vector

    ax_2d.arrow(x, y, dx, dy, **kwargs)


@plot_2d.register  # type: ignore[no-redef]
def _(points: Points, ax_2d: Axes, **kwargs) -> None:
    """
    Plot points on a 2D scatter plot.

    Parameters
    ----------
    points : Points
        Input points.
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

        >>> points = Points([[1, 2], [3, 4], [-4, 2], [-2, 3]])

        >>> fig, ax = plt.subplots()
        >>> plot_2d(points, ax, c='k')

    """
    _scatter_2d(ax_2d, points, **kwargs)


@plot_2d.register  # type: ignore[no-redef]
def _(line: Line, ax_2d: Axes, t_1: float = 0, t_2: float = 1, **kwargs) -> None:
    """
    Plot a 2D line.

    The line is plotted by connecting two 2D points.

    Parameters
    ----------
    line : Line
        Input line.
    ax_2d : Axes
        Instance of :class:`~matplotlib.axes.Axes`.
    t_1, t_2 : {int, float}
        Parameters to determine points 1 and 2 along the line.
        These are passed to :meth:`Line.to_point`.
        Defaults are 0 and 1.
    kwargs : dict, optional
        Additional keywords passed to :meth:`~matplotlib.axes.Axes.plot`.

    Examples
    --------
    .. plot::
        :include-source:

        >>> import matplotlib.pyplot as plt
        >>> from skspatial.objects import Line

        >>> line = Line([1, 2], [3, 4])

        >>> _, ax = plt.subplots()
        >>> plot_2d(line, ax, t_1=-2, t_2=3, c='k')
        >>> plot_2d(line.point, ax, c='r', s=100, zorder=3)
        >>> grid = ax.grid()

    """
    point_1 = line.to_point(t_1)
    point_2 = line.to_point(t_2)

    _connect_points_2d(ax_2d, point_1, point_2, **kwargs)


@plot_2d.register  # type: ignore[no-redef]
def _(circle: Circle, ax_2d: Axes, **kwargs) -> None:
    """
    Plot a circle in 2D.

    Parameters
    ----------
    circle : Circle
        Input circle.
    ax_2d : Axes
        Instance of :class:`~matplotlib.axes.Axes`.
    kwargs : dict, optional
        Additional keywords passed to :Class:`matplotlib.patches.Circle`.

    Examples
    --------
    .. plot::
        :include-source:

        >>> import matplotlib.pyplot as plt

        >>> from skspatial.objects import Circle

        >>> circle = Circle([-2, 3], 3)

        >>> fig, ax = plt.subplots()
        >>> plot_2d(circle, ax, fill=False)
        >>> plot_2d(circle.point, ax)
        >>> limits = plt.axis([-10, 10, -10, 10])

    """
    artist_circle = plt.Circle(circle.point, circle.radius, **kwargs)

    ax_2d.add_artist(artist_circle)


@plot_2d.register  # type: ignore[no-redef]
def _(triangle: Triangle, ax_2d: Axes, part: str = "points", **kwargs: str) -> None:
    """
    Plot a triangle in 2D.

    Parameters
    ----------
    triangle : Triangle
        Input triangle.
    ax_2d : Axes
        Instance of :class:`~matplotlib.axes.Axes`.
    part : str, optional
        Part of the triangle to plot.
        Either 'points' or 'lines' (default 'points').
    kwargs : dict, optional
        Additional keywords passed to :meth:`~skspatial.objects.point.plot_2d` or
        :meth:`~skspatial.objects.line.plot_2d`.

    Examples
    --------
    .. plot::
        :include-source:

        >>> import matplotlib.pyplot as plt

        >>> from skspatial.objects import Triangle

        >>> triangle = Triangle([0, 0], [1, 0], [0, 1])

        >>> _, ax = plt.subplots()
        >>> plot_2d(triangle, ax, part='points', s=100, zorder=3)
        >>> plot_2d(triangle, ax, part='lines', c='k')

    """
    if part == "points":

        for point in triangle.multiple("point", "ABC"):
            plot_2d(point, ax_2d, **kwargs)

    elif part == "lines":

        for line in triangle.multiple("line", "abc"):
            plot_2d(line, ax_2d, **kwargs)
