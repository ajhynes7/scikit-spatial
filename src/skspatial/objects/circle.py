"""Module for the Circle class."""
from __future__ import annotations

import math
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from skspatial._functions import np_float
from skspatial.objects._base_sphere import _BaseSphere
from skspatial.objects.line import Line
from skspatial.objects.point import Point
from skspatial.objects.points import Points
from skspatial.typing import array_like


class Circle(_BaseSphere):
    """
    A circle in 2D space.

    The circle is defined by a 2D point and a radius.

    Parameters
    ----------
    point : (2,) array_like
        Center of the circle.
    radius : {int, float}
        Radius of the circle/

    Attributes
    ----------
    point : (2,) Point
        Center of the circle.
    radius : {int, float}
        Radius of the circle.
    dimension : int
        Dimension of the circle.

    Raises
    ------
    ValueError
        If the radius is not positive.
        If the point is not 2D.

    Examples
    --------
    >>> from skspatial.objects import Circle

    >>> circle = Circle([2, 5], 3)

    >>> circle
    Circle(point=Point([2, 5]), radius=3)

    >>> circle.dimension
    2

    >>> circle.area().round(2)
    28.27

    >>> Circle([0, 0, 0], 1)
    Traceback (most recent call last):
    ...
    ValueError: The point must be 2D.

    >>> Circle([0, 0], 0)
    Traceback (most recent call last):
    ...
    ValueError: The radius must be positive.

    """

    def __init__(self, point: array_like, radius: float):

        super().__init__(point, radius)

        if self.point.dimension != 2:
            raise ValueError("The point must be 2D.")

    @np_float
    def circumference(self) -> float:
        r"""
        Return the circumference of the circle.

        The circumference :math:`C` of a circle with radius :math:`r` is

        .. math:: C = 2 \pi r

        Returns
        -------
        np.float64
            Circumference of the circle.

        Examples
        --------
        >>> from skspatial.objects import Circle

        >>> Circle([0, 0], 1).area().round(2)
        3.14

        >>> Circle([0, 0], 2).area().round(2)
        12.57

        """
        return 2 * np.pi * self.radius

    @np_float
    def area(self) -> float:
        r"""
        Return the area of the circle.

        The area :math:`A` of a circle with radius :math:`r` is

        .. math:: A = \pi r ^ 2

        Returns
        -------
        np.float64
            Area of the circle.

        Examples
        --------
        >>> from skspatial.objects import Circle

        >>> Circle([0, 0], 1).area().round(2)
        3.14

        >>> Circle([0, 0], 2).area().round(2)
        12.57

        """
        return np.pi * self.radius**2

    def intersect_line(self, line: Line) -> Tuple[Point, Point]:
        """
        Intersect the circle with a line.

        A line intersects a circle at two points.

        Parameters
        ----------
        line : Line
            Input line.

        Returns
        -------
        point_a, point_b : Point
            The two points of intersection.

        Raises
        ------
        ValueError
            If the line does not intersect the circle.

        References
        ----------
        http://mathworld.wolfram.com/Circle-LineIntersection.html

        Examples
        --------
        >>> from skspatial.objects import Circle, Line

        >>> circle = Circle([0, 0], 1)

        >>> circle.intersect_line(Line(point=[0, 0], direction=[1, 0]))
        (Point([-1.,  0.]), Point([1., 0.]))

        >>> point_a, point_b = circle.intersect_line(Line(point=[0, 0], direction=[1, 1]))

        >>> point_a.round(3)
        Point([-0.707, -0.707])

        >>> point_b.round(3)
        Point([0.707, 0.707])

        >>> circle.intersect_line(Line(point=[1, 2], direction=[1, 1]))
        (Point([-1.,  0.]), Point([0., 1.]))

        If the line is tangent to the circle, the two intersection points are the same.

        >>> circle.intersect_line(Line(point=[1, 0], direction=[0, 1]))
        (Point([1., 0.]), Point([1., 0.]))

        The circle does not have to be centered on the origin.

        >>> point_a, point_b = Circle([2, 3], 5).intersect_line(Line([1, 1], [2, 3]))

        >>> point_a.round(3)
        Point([-0.538, -1.308])

        >>> point_b.round(3)
        Point([5., 7.])

        >>> circle.intersect_line(Line(point=[5, 0], direction=[1, 1]))
        Traceback (most recent call last):
        ...
        ValueError: The line does not intersect the circle.

        """
        # Two points on the line.
        point_1 = line.point
        point_2 = point_1 + line.direction.unit()

        # Translate the points on the line to mimic the circle being centered on the origin.
        point_translated_1 = point_1 - self.point
        point_translated_2 = point_2 - self.point

        x_1, y_1 = point_translated_1
        x_2, y_2 = point_translated_2

        d_x = x_2 - x_1
        d_y = y_2 - y_1

        # Pre-compute variables common to x and y equations.
        d_r_squared = d_x**2 + d_y**2
        determinant = x_1 * y_2 - x_2 * y_1
        discriminant = self.radius**2 * d_r_squared - determinant**2

        if discriminant < 0:
            raise ValueError("The line does not intersect the circle.")

        root = math.sqrt(discriminant)

        pm = np.array([-1, 1])  # Array to compute minus/plus.
        sign = -1 if d_y < 0 else 1

        coords_x = (determinant * d_y + pm * sign * d_x * root) / d_r_squared
        coords_y = (-determinant * d_x + pm * abs(d_y) * root) / d_r_squared

        point_translated_a = Point([coords_x[0], coords_y[0]])
        point_translated_b = Point([coords_x[1], coords_y[1]])

        # Translate the intersection points back from origin circle to real circle.
        point_a = point_translated_a + self.point
        point_b = point_translated_b + self.point

        return point_a, point_b

    @classmethod
    def best_fit(cls, points: array_like) -> Circle:
        """
        Return the sphere of best fit for a set of 2D points.

        Parameters
        ----------
        points : array_like
             Input 2D points.

        Returns
        -------
        Circle
            The circle of best fit.

        Raises
        ------
        ValueError
            If the points are not 2D.
            If there are fewer than three points.
            If the points are collinear.

        Reference
        ---------
        https://meshlogic.github.io/posts/jupyter/curve-fitting/fitting-a-circle-to-cluster-of-3d-points/

        Examples
        --------
        >>> import numpy as np

        >>> from skspatial.objects import Circle

        >>> points = [[1, 1], [2, 2], [3, 1]]
        >>> circle = Circle.best_fit(points)

        >>> circle.point
        Point([2., 1.])

        >>> np.round(circle.radius, 2)
        1.0

        """
        points = Points(points)

        if points.dimension != 2:
            raise ValueError("The points must be 2D.")

        if points.shape[0] < 3:
            raise ValueError("There must be at least 3 points.")

        if points.affine_rank() != 2:
            raise ValueError("The points must not be collinear.")

        n = points.shape[0]
        A = np.hstack((2 * points, np.ones((n, 1))))
        b = (points**2).sum(axis=1)
        c = np.linalg.lstsq(A, b, rcond=None)[0]

        center = c[:2]
        radius = np.sqrt(c[2] + c[0] ** 2 + c[1] ** 2)

        return cls(center, radius)

    def plot_2d(self, ax_2d: Axes, **kwargs) -> None:
        """
        Plot the circle in 2D.

        Parameters
        ----------
        ax_2d : Axes
            Instance of :class:`~matplotlib.axes.Axes`.
        kwargs : dict, optional
            Additional keywords passed to :class:`matplotlib.patches.Circle`.

        Examples
        --------
        .. plot::
            :include-source:

            >>> import matplotlib.pyplot as plt

            >>> from skspatial.objects import Circle

            >>> circle = Circle([-2, 3], 3)

            >>> fig, ax = plt.subplots()
            >>> circle.plot_2d(ax, fill=False)
            >>> circle.point.plot_2d(ax)
            >>> limits = plt.axis([-10, 10, -10, 10])

        """
        circle = plt.Circle(self.point, self.radius, **kwargs)

        ax_2d.add_artist(circle)
