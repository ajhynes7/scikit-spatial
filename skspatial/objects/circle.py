"""Module for the Circle class."""

import matplotlib.pyplot as plt
import numpy as np

from skspatial.objects._base_sphere import _BaseSphere
from skspatial.objects.point import Point


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
        If the radius is not positive, or if the point is not 2D.

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

    def __init__(self, point, radius):

        super().__init__(point, radius)

        if self.point.dimension != 2:
            raise ValueError("The point must be 2D.")

    def circumference(self):
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
        return np.float64(2 * np.pi * self.radius)

    def area(self):
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
        return np.float64(np.pi * self.radius ** 2)

    def intersect_line(self, line):
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

        >>> circle.intersect_line(Line(point=[0, 0], direction=[1, 1]))
        (Point([-0.70710678, -0.70710678]), Point([0.70710678, 0.70710678]))

        >>> circle.intersect_line(Line(point=[1, 2], direction=[1, 1]))
        (Point([-1.,  0.]), Point([0., 1.]))

        If the line is tangent to the circle, the two intersection points are the same.

        >>> circle.intersect_line(Line(point=[1, 0], direction=[0, 1]))
        (Point([1., 0.]), Point([1., 0.]))

        The circle does not have to be centered on the origin.

        >>> Circle([2, 3], 5).intersect_line(Line([1, 1], [2, 3]))
        (Point([-0.53846154, -1.30769231]), Point([5., 7.]))

        >>> circle.intersect_line(Line(point=[5, 0], direction=[1, 1]))
        Traceback (most recent call last):
        ...
        ValueError: The line does not intersect the circle.

        """
        # Two points on the line.
        # Copy the line point to avoid changing the line itself.
        point_1 = np.copy(line.point)
        point_2 = point_1 + line.direction.unit()

        # Translate the points on the line to mimic the circle being centered on the origin.
        point_1 -= self.point
        point_2 -= self.point

        x_1, y_1 = point_1
        x_2, y_2 = point_2

        d_x = x_2 - x_1
        d_y = y_2 - y_1

        # Pre-compute variables common to x and y equations.
        d_r_squared = d_x ** 2 + d_y ** 2
        determinant = x_1 * y_2 - x_2 * y_1
        discriminant = self.radius ** 2 * d_r_squared - determinant ** 2

        if discriminant < 0:
            raise ValueError("The line does not intersect the circle.")

        root = np.sqrt(discriminant)

        pm = np.array([-1, 1])  # Array to compute plus/minus.
        sign = -1 if d_y < 0 else 1

        coords_x = (determinant * d_y + pm * sign * d_x * root) / d_r_squared
        coords_y = (-determinant * d_x + pm * abs(d_y) * root) / d_r_squared

        point_a = Point([coords_x[0], coords_y[0]])
        point_b = Point([coords_x[1], coords_y[1]])

        # Translate the intersection points back from origin circle to real circle.
        point_a += self.point
        point_b += self.point

        return point_a, point_b

    def plot_2d(self, ax_2d, **kwargs):
        """
        Plot the circle in 2D.

        Parameters
        ----------
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

            >>> fig, ax = plt.subplots()
            >>> Circle([0, 0], 1).plot_2d(ax, fill=False)
            >>> limits = plt.axis([-2, 2, -2, 2])

        """
        circle = plt.Circle(self.point, self.radius, **kwargs)

        ax_2d.add_artist(circle)
