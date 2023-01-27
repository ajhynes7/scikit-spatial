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
from skspatial.objects.vector import Vector
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

    @classmethod
    def from_points(cls, point_a: array_like, point_b: array_like, point_c: array_like, **kwargs) -> Circle:
        """
        Instantiate a circle from three points.

        Parameters
        ----------
        point_a, point_b, point_c: array_like
            Three points defining the circle. The points must be 2D.
        kwargs: dict, optional
            Additional keywords passed to :meth:`Points.are_collinear`.

        Returns
        -------
        Circle
            Circle containing the three input points.

        Raises
        ------
        ValueError
            If the points are not 2D.
            If the points are collinear.

        Examples
        --------
        >>> from skspatial.objects import Circle

        >>> Circle.from_points([-1, 0], [0, 1], [1, 0])
        Circle(point=Point([-0.,  0.]), radius=1.0)

        >>> Circle.from_points([1, 0, 0], [0, 1], [1, 0])
        Traceback (most recent call last):
        ...
        ValueError: The points must be 2D.

        >>> Circle.from_points([0, 0], [1, 1], [2, 2])
        Traceback (most recent call last):
        ...
        ValueError: The points must not be collinear.

        """

        def _minor(array, i: int, j: int):
            subarray = array[
                np.array(list(range(i)) + list(range(i + 1, array.shape[0])))[:, np.newaxis],
                np.array(list(range(j)) + list(range(j + 1, array.shape[1]))),
            ]
            return np.linalg.det(subarray)

        point_a = Point(point_a)
        point_b = Point(point_b)
        point_c = Point(point_c)

        if any(point.dimension != 2 for point in [point_a, point_b, point_c]):
            raise ValueError("The points must be 2D.")

        if Points([point_a, point_b, point_c]).are_collinear(**kwargs):
            raise ValueError("The points must not be collinear.")

        x_a, y_a = point_a
        x_b, y_b = point_b
        x_c, y_c = point_c

        matrix = np.array(
            [
                [0, 0, 0, 1],
                [x_a**2 + y_a**2, x_a, y_a, 1],
                [x_b**2 + y_b**2, x_b, y_b, 1],
                [x_c**2 + y_c**2, x_c, y_c, 1],
            ],
        )

        M_00 = _minor(matrix, 0, 0)
        M_01 = _minor(matrix, 0, 1)
        M_02 = _minor(matrix, 0, 2)
        M_03 = _minor(matrix, 0, 3)

        x = 0.5 * M_01 / M_00
        y = -0.5 * M_02 / M_00

        radius = math.sqrt(x**2 + y**2 + M_03 / M_00)

        return cls([x, y], radius)

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

    def intersect_circle(self, other: Circle) -> Tuple[Point, Point]:
        """
        Intersect the circle with another circle.

        A circle intersects a circle at two points.

        Parameters
        ----------
        other : Circle
            Other circle.

        Returns
        -------
        point_a, point_b : Point
            The two points of intersection.

        Raises
        ------
        ValueError
            If the centres of the circles are coincident.
            If the circles are separate.
            If one circle is contained within the other.

        References
        ----------
        http://paulbourke.net/geometry/circlesphere/

        Examples
        --------
        >>> from skspatial.objects import Circle

        >>> circle_a = Circle([0, 0], 1)
        >>> circle_b = Circle([2, 0], 1)

        >>> circle_a.intersect_circle(circle_b)
        (Point([1., 0.]), Point([1., 0.]))

        >>> circle_a.intersect_circle(Circle([0, 0], 2))
        Traceback (most recent call last):
        ...
        ValueError: The centres of the circles are coincident.

        >>> circle_a.intersect_circle(Circle([3, 0], 1))
        Traceback (most recent call last):
        ...
        ValueError: The circles do not intersect. These circles are separate.

        >>> Circle([0, 0], 3).intersect_circle(Circle([1, 0], 1))
        Traceback (most recent call last):
        ...
        ValueError: The circles do not intersect. One circle is contained within the other.

        """
        d = self.point.distance_point(other.point)

        if d == 0:
            raise ValueError("The centres of the circles are coincident.")

        if d > self.radius + other.radius:
            raise ValueError("The circles do not intersect. These circles are separate.")

        if d < abs(self.radius - other.radius):
            raise ValueError("The circles do not intersect. One circle is contained within the other.")

        a = (self.radius**2 - other.radius**2 + d**2) / (2 * d)

        h = math.sqrt(self.radius**2 - a**2)

        point_middle = self.point + a * Vector.from_points(self.point, other.point) / d

        pm = np.array([1, -1])

        X = point_middle[0] + pm * h * (self.point[1] - other.point[1]) / d
        Y = point_middle[1] - pm * h * (self.point[0] - other.point[0]) / d

        point_a = Point([X[0], Y[0]])
        point_b = Point([X[1], Y[1]])

        return point_a, point_b

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

        mp = np.array([-1, 1])  # Array to compute minus/plus.
        sign = -1 if d_y < 0 else 1

        coords_x = (determinant * d_y + mp * sign * d_x * root) / d_r_squared
        coords_y = (-determinant * d_x + mp * abs(d_y) * root) / d_r_squared

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

        References
        ----------
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
