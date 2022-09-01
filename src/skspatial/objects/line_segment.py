"""Module for the LineSegment class."""
from __future__ import annotations

import math

import numpy as np
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D

from skspatial.objects.line import Line
from skspatial.objects.point import Point
from skspatial.objects.vector import Vector
from skspatial.plotting import _connect_points_2d
from skspatial.plotting import _connect_points_3d
from skspatial.typing import array_like


class LineSegment:
    """
    A line segment in space.

    The line segment is defined by two points.

    Parameters
    ----------
    point_a, point_b : array_like
        The two endpoints of the line segment.

    Attributes
    ----------
    point_a, point_b : Point
        The two endpoints of the line segment.

    Raises
    ------
    ValueError
        If the two endpoints are equal.

    Examples
    --------
    >>> from skspatial.objects import LineSegment

    >>> segment = LineSegment([0, 0], [1, 0])

    >>> segment
    LineSegment(point_a=Point([0, 0]), point_b=Point([1, 0]))

    >>> LineSegment([0, 0], [0, 0])
    Traceback (most recent call last):
    ...
    ValueError: The endpoints must not be equal.

    """

    def __init__(self, point_a: array_like, point_b: array_like):

        self.point_a = Point(point_a)
        self.point_b = Point(point_b)

        if self.point_a.is_close(self.point_b):
            raise ValueError("The endpoints must not be equal.")

    def __repr__(self) -> str:

        repr_point_a = np.array_repr(self.point_a)
        repr_point_b = np.array_repr(self.point_b)

        return f"LineSegment(point_a={repr_point_a}, point_b={repr_point_b})"

    def contains_point(self, point: array_like, **kwargs) -> bool:
        """
        Check if a point is on the line segment.

        Parameters
        ----------
        point : array_like

        Returns
        -------
        bool
            True if the point is on the line segment; false otherwise.

        Examples
        --------
        >>> from skspatial.objects import LineSegment

        >>> segment = LineSegment([0, 0], [1, 0])

        >>> segment.contains_point([0, 0])
        True
        >>> segment.contains_point([0.5, 0])
        True
        >>> segment.contains_point([2, 0])
        False
        >>> segment.contains_point([0, 1])
        False

        """
        vector_a = Vector.from_points(point, self.point_a)
        vector_b = Vector.from_points(point, self.point_b)

        if vector_a.is_zero(**kwargs) or vector_b.is_zero(**kwargs):
            return True

        similarity = vector_a.cosine_similarity(vector_b)

        return math.isclose(similarity, -1, **kwargs)

    def intersect_line_segment(self, other: LineSegment) -> Point:
        """
        Intersect the line segment with another.

        Parameters
        ----------
        other : LineSegment

        Returns
        -------
        Point
            The intersection point of the two line segments.

        Raises
        ------
        ValueError
            If the line segments do not intersect.

        Examples
        --------
        >>> from skspatial.objects import LineSegment

        >>> segment_a = LineSegment([-1, 0], [1, 0])
        >>> segment_b = LineSegment([0, -1], [0, 1])

        >>> segment_a.intersect_line_segment(segment_b)
        Point([0., 0.])

        >>> segment_b = LineSegment([0, 1], [0, 2])

        >>> segment_a.intersect_line_segment(segment_b)
        Traceback (most recent call last):
        ...
        ValueError: The line segments must intersect.

        """
        line_a = Line.from_points(self.point_a, self.point_b)
        line_b = Line.from_points(other.point_a, other.point_b)

        point_intersection = line_a.intersect_line(line_b)

        point_on_segment_a = self.contains_point(point_intersection)
        point_on_segment_b = other.contains_point(point_intersection)

        if not (point_on_segment_a and point_on_segment_b):
            raise ValueError("The line segments must intersect.")

        return point_intersection

    def plot_2d(self, ax_2d: Axes, **kwargs) -> None:
        """
        Plot a 2D line segment.

        The line segment is plotted by connecting two 2D points.

        Parameters
        ----------
        ax_2d : Axes
            Instance of :class:`~matplotlib.axes.Axes`.
        kwargs : dict, optional
            Additional keywords passed to :meth:`~matplotlib.axes.Axes.plot`.

        Examples
        --------
        .. plot::
            :include-source:

            >>> import matplotlib.pyplot as plt
            >>> from skspatial.objects import LineSegment

            >>> _, ax = plt.subplots()

            >>> segment = LineSegment([0, 0], [1, 1])

            >>> segment.plot_2d(ax, c='k')

            >>> segment.point_a.plot_2d(ax, c='b', s=100, zorder=3)
            >>> segment.point_b.plot_2d(ax, c='r', s=100, zorder=3)

            >>> grid = ax.grid()

        """
        _connect_points_2d(ax_2d, self.point_a, self.point_b, **kwargs)

    def plot_3d(self, ax_3d: Axes3D, **kwargs) -> None:
        """
        Plot a 3D line segment.

        The line segment is plotted by connecting two 3D points.

        Parameters
        ----------
        ax_3d : Axes3D
            Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
        kwargs : dict, optional
            Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot`.

        Examples
        --------
        .. plot::
            :include-source:

            >>> import matplotlib.pyplot as plt
            >>> from mpl_toolkits.mplot3d import Axes3D

            >>> from skspatial.objects import LineSegment

            >>> fig = plt.figure()
            >>> ax = fig.add_subplot(111, projection='3d')

            >>> segment = LineSegment([1, 2, 3], [0, 1, 1])

            >>> segment.point_a.plot_3d(ax, c='b', s=100, zorder=3)
            >>> segment.point_b.plot_3d(ax, c='r', s=100, zorder=3)

            >>> segment.plot_3d(ax, c='k')

        """
        _connect_points_3d(ax_3d, self.point_a, self.point_b, **kwargs)
