"""Module for the Triangle class."""
import math
from itertools import combinations
from typing import Sequence

import numpy as np
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D

from skspatial._functions import np_float
from skspatial.objects._base_spatial import _BaseSpatial
from skspatial.objects.line import Line
from skspatial.objects.point import Point
from skspatial.objects.points import Points
from skspatial.objects.vector import Vector
from skspatial.typing import array_like


class Triangle(_BaseSpatial):
    """
    A triangle represented by three points in space.

    Parameters
    ----------
    point_a, point_b, point_c : array_like
        The three vertices of the triangle.

    Attributes
    ----------
    point_a, point_b, point_c : Point
        The three vertices of the triangle.
    dimension : int
        Dimension of the triangle.

    Raises
    ------
    ValueError
        If the points do not have the same dimension.
        If the points are collinear.

    Examples
    --------
    >>> from skspatial.objects import Triangle

    >>> triangle = Triangle([0, 0], [1, 0], [0, 1])

    >>> triangle
    Triangle(point_a=Point([0, 0]), point_b=Point([1, 0]), point_c=Point([0, 1]))

    >>> triangle.dimension
    2

    >>> Triangle([0, 0, 0], [1, 0], [0, 1])
    Traceback (most recent call last):
    ...
    ValueError: The points must have the same dimension.

    >>> Triangle([0, 0], [0, 1], [0, 2])
    Traceback (most recent call last):
    ...
    ValueError: The points must not be collinear.

    """

    def __init__(self, point_a: array_like, point_b: array_like, point_c: array_like):

        self.point_a = Point(point_a)
        self.point_b = Point(point_b)
        self.point_c = Point(point_c)

        if not (self.point_a.dimension == self.point_b.dimension == self.point_c.dimension):
            raise ValueError("The points must have the same dimension.")

        if Points([self.point_a, self.point_b, self.point_c]).are_collinear():
            raise ValueError("The points must not be collinear.")

        self.dimension = self.point_a.dimension

    def __repr__(self) -> str:

        repr_a = np.array_repr(self.point_a)
        repr_b = np.array_repr(self.point_b)
        repr_c = np.array_repr(self.point_c)

        return f"Triangle(point_a={repr_a}, point_b={repr_b}, point_c={repr_c})"

    def multiple(self, name_method: str, inputs: Sequence) -> tuple:
        """
        Return multiple properties of the triangle.

        Parameters
        ----------
        name_method : str
            Name of the triangle method.
        inputs : Sequence
            Sequence of different inputs to the method.

        Returns
        -------
        tuple
            Multiple outputs from the triangle method.

        Examples
        --------
        >>> from math import degrees
        >>> from skspatial.objects import Triangle

        >>> triangle = Triangle([0, 0], [0, 1], [1, 0])

        >>> lengths = triangle.multiple('length', 'abc')
        >>> [round(x, 3) for x in lengths]
        [1.414, 1.0, 1.0]

        >>> angles = triangle.multiple('angle', 'ABC')
        >>> [round(degrees(x), 3) for x in angles]
        [90.0, 45.0, 45.0]

        """
        method = getattr(self, name_method)

        return tuple(method(x) for x in inputs)

    def normal(self) -> Vector:
        r"""
        Return a vector normal to the triangle.

        The normal vector is calculated as

        .. math::
            v_{AB} \times v_{AC}

        where :math:`v_{AB}` is the vector from vertex A to vertex B.

        Returns
        -------
        Vector
            Normal vector.

        Examples
        --------
        >>> from skspatial.objects import Triangle

        >>> Triangle([0, 0], [1, 0], [0, 1]).normal()
        Vector([0, 0, 1])

        The normal vector is not necessarily a unit vector.

        >>> Triangle([0, 0], [2, 0], [0, 2]).normal()
        Vector([0, 0, 4])

        The direction of the normal vector is dependent on the order of the vertices.

        >>> Triangle([0, 0], [0, 1], [1, 0]).normal()
        Vector([ 0,  0, -1])

        """
        vector_ab = Vector.from_points(self.point_a, self.point_b)
        vector_ac = Vector.from_points(self.point_a, self.point_c)

        return vector_ab.cross(vector_ac)

    def area(self) -> np.float64:
        """
        Return the area of the triangle.

        The points are the vertices of the triangle. They must be 3D or less.

        Returns
        -------
        np.float64
            The area of the triangle.

        References
        ----------
        http://mathworld.wolfram.com/TriangleArea.html

        Examples
        --------
        >>> from skspatial.objects import Triangle

        >>> Triangle([0, 0], [0, 1], [1, 0]).area()
        0.5

        >>> Triangle([0, 0], [0, 2], [1, 1]).area()
        1.0

        >>> Triangle([3, -5, 1], [5, 2, 1], [9, 4, 2]).area().round(2)
        12.54

        """
        return 0.5 * self.normal().norm()

    def perimeter(self) -> np.float64:
        """
        Return the perimeter of the triangle.

        Returns
        -------
        np.float64
            The perimeter of the triangle.

        Examples
        --------
        >>> from skspatial.objects import Triangle

        >>> Triangle([0, 0], [0, 1], [1, 0]).perimeter().round(3)
        3.414

        >>> Triangle([0, 1], [1, 1], [2, 0]).perimeter().round(3)
        4.65

        """
        result = np.sum(self.multiple('length', 'abc'))

        return np.float64(result)

    def point(self, vertex: str) -> Point:
        """
        Return a point (vertex) of the triangle.

        Parameters
        ----------
        vertex: str
            'A', 'B', or 'C'.

        Returns
        -------
        Point
            A vertex of the triangle.

        Raises
        ------
        ValueError
            If the vertex is not 'A', 'B', or 'C'.

        Examples
        --------
        >>> from skspatial.objects import Triangle

        >>> triangle = Triangle([0, 0], [1, 0], [0, 1])

        >>> triangle.point('A')
        Point([0, 0])

        >>> triangle.point('B')
        Point([1, 0])

        >>> triangle.point('C')
        Point([0, 1])

        >>> triangle.point('D')
        Traceback (most recent call last):
        ...
        ValueError: The vertex must be 'A', 'B', or 'C'.

        """
        if vertex == 'A':
            return self.point_a

        if vertex == 'B':
            return self.point_b

        if vertex == 'C':
            return self.point_c

        raise ValueError("The vertex must be 'A', 'B', or 'C'.")

    def line(self, side: str) -> Line:
        """
        Return the line along a side of the triangle.

        Parameters
        ----------
        side: str
            'a', 'b', or 'c'.
            Side 'a' is the side across from vertex 'A'.

        Returns
        -------
        Line
            Line along the side.

        Raises
        ------
        ValueError
            If the side is not 'a', 'b', or 'c'.

        Examples
        --------
        >>> from skspatial.objects import Triangle

        >>> triangle = Triangle([0, 0], [1, 0], [0, 1])

        >>> triangle.line('a')
        Line(point=Point([1, 0]), direction=Vector([-1,  1]))

        >>> triangle.line('b')
        Line(point=Point([0, 1]), direction=Vector([ 0, -1]))

        >>> triangle.line('c')
        Line(point=Point([0, 0]), direction=Vector([1, 0]))

        >>> triangle.line('d')
        Traceback (most recent call last):
        ...
        ValueError: The side must be 'a', 'b', or 'c'.

        """
        if side == 'a':
            point_1, point_2 = self.point_b, self.point_c

        elif side == 'b':
            point_1, point_2 = self.point_c, self.point_a

        elif side == 'c':
            point_1, point_2 = self.point_a, self.point_b

        else:
            raise ValueError("The side must be 'a', 'b', or 'c'.")

        return Line.from_points(point_1, point_2)

    def length(self, side: str) -> np.float64:
        """
        Return a side length of the triangle.

        Side 'a' is the side across from vertex 'A'.
        The side length is the distance between vertices 'B' and 'C'.

        Parameters
        ----------
        side: str
            'a', 'b', or 'c'.

        Returns
        -------
        np.float64
            Side length.

        Raises
        ------
        ValueError
            If the side is not 'a', 'b', or 'c'.

        Examples
        --------
        >>> from skspatial.objects import Triangle

        >>> triangle = Triangle([0, 0], [1, 0], [0, 1])

        >>> triangle.length('a').round(3)
        1.414
        >>> triangle.length('b')
        1.0
        >>> triangle.length('c')
        1.0

        >>> triangle.length('d')
        Traceback (most recent call last):
        ...
        ValueError: The side must be 'a', 'b', or 'c'.

        """
        return self.line(side).direction.norm()

    @np_float
    def angle(self, vertex: str) -> float:
        """
        Return an interior angle of the triangle.

        The angle is in radians.

        Parameters
        ----------
        vertex: str
            'A', 'B', or 'C'.

        Returns
        -------
        np.float64
            Interior angle.

        Raises
        ------
        ValueError
            If the vertex is not 'A', 'B', or 'C'.

        Examples
        --------
        >>> from skspatial.objects import Triangle

        >>> triangle = Triangle([0, 0], [1, 0], [0, 1])

        >>> triangle.angle('A').round(3)
        1.571
        >>> triangle.angle('B').round(3)
        0.785
        >>> triangle.angle('C').round(3)
        0.785

        >>> triangle.angle('D')
        Traceback (most recent call last):
        ...
        ValueError: The vertex must be 'A', 'B', or 'C'.

        """
        a, b, c = self.multiple('length', 'abc')

        if vertex == 'A':
            arg = (b**2 + c**2 - a**2) / (2 * b * c)

        elif vertex == 'B':
            arg = (a**2 + c**2 - b**2) / (2 * a * c)

        elif vertex == 'C':
            arg = (a**2 + b**2 - c**2) / (2 * a * b)

        else:
            raise ValueError("The vertex must be 'A', 'B', or 'C'.")

        return math.acos(arg)

    def centroid(self) -> Point:
        """
        Return the centroid of the triangle.

        Returns
        -------
        Point
            Centroid of the triangle.

        Examples
        --------
        >>> from skspatial.objects import Triangle

        >>> Triangle([0, 0], [0, 1], [1, 0]).centroid().round(3)
        Point([0.333, 0.333])

        >>> Triangle([0, 0, 0], [1, 2, 3], [4, 5, 6]).centroid().round(3)
        Point([1.667, 2.333, 3.   ])

        """
        return Points([self.point_a, self.point_b, self.point_c]).centroid()

    def altitude(self, vertex: str) -> Line:
        """
        Return the line of an altitude of the triangle.

        An altitude is a line segment through a vertex and perpendicular to the opposite side.

        Parameters
        ----------
        vertex: str
            'A', 'B', or 'C'.

        Returns
        -------
        Line
            Altitude line.

        Raises
        ------
        ValueError
            If the vertex is not 'A', 'B', or 'C'.

        Examples
        --------
        >>> from skspatial.objects import Triangle

        >>> triangle = Triangle([0, 0], [1, 1], [2, 0])

        >>> triangle.altitude('A')
        Line(point=Point([0, 0]), direction=Vector([1., 1.]))

        >>> triangle.altitude('B')
        Line(point=Point([1, 1]), direction=Vector([ 0., -1.]))

        >>> triangle.altitude('C')
        Line(point=Point([2, 0]), direction=Vector([-1.,  1.]))

        >>> triangle.altitude('D')
        Traceback (most recent call last):
        ...
        ValueError: The vertex must be 'A', 'B', or 'C'.

        """
        if vertex == 'A':
            point_proj = self.line('a').project_point(self.point_a)
            return Line.from_points(self.point_a, point_proj)

        if vertex == 'B':
            point_proj = self.line('b').project_point(self.point_b)
            return Line.from_points(self.point_b, point_proj)

        if vertex == 'C':
            point_proj = self.line('c').project_point(self.point_c)
            return Line.from_points(self.point_c, point_proj)

        raise ValueError("The vertex must be 'A', 'B', or 'C'.")

    def orthocenter(self) -> Point:
        """
        Return the orthocenter of the triangle.

        The orthocenter is the intersection point of the three altitudes.

        Returns
        -------
        Point
            Orthocenter of the triangle.

        Examples
        --------
        >>> from skspatial.objects import Triangle

        >>> Triangle([0, 0], [0, 1], [1, 0]).orthocenter()
        Point([0., 0.])

        >>> Triangle([0, 0], [1, 2], [2, 0]).orthocenter()
        Point([1. , 0.5])

        """
        line_alt_a = self.altitude('A')
        line_alt_b = self.altitude('B')

        return line_alt_a.intersect_line(line_alt_b)

    def classify(self, **kwargs: float) -> str:
        """
        Classify the triangle as equilateral, isosceles, or scalene.

        Parameters
        ----------
        kwargs : dict, optional
            Additional keywords passed to :func:`math.isclose`.

        Returns
        -------
        str
            'equilateral', 'isosceles', or 'scalene'.

        Examples
        --------
        >>> import math
        >>> from skspatial.objects import Triangle

        >>> Triangle([0, 0], [1, 0], [1, 1]).classify()
        'isosceles'

        >>> Triangle([0, 0], [1, 0], [0, 1]).classify()
        'isosceles'

        >>> Triangle([0, 0], [1, 0], [0, 2]).classify()
        'scalene'

        >>> Triangle([0, 0], [1, 0], [0.5, math.sin(math.pi / 3)]).classify()
        'equilateral'

        This triangle is approximately equilateral.

        >>> triangle = Triangle([0, 0], [1, 0], [0.5, 0.866])

        >>> triangle.classify()
        'isosceles'

        >>> triangle.classify(rel_tol=1e-3)
        'equilateral'

        """
        lengths = self.multiple('length', 'abc')

        pairs = combinations(lengths, 2)
        n_pairs_close = sum(math.isclose(a, b, **kwargs) for a, b in pairs)

        if n_pairs_close == 3:
            return 'equilateral'

        if n_pairs_close == 1:
            return 'isosceles'

        return 'scalene'

    def is_right(self, **kwargs: float) -> bool:
        """
        Check if the triangle is a right triangle.

        A right triangle with sides :math:`abc`, satisfies the Pythagorean theorem

        .. math::
            a^2 + b^2 = c^2

        Parameters
        ----------
        kwargs : dict, optional
            Additional keywords passed to :func:`math.isclose`.

        Returns
        -------
        bool
            True if the triangle is a right triangle; false otherwise.

        Examples
        --------
        >>> from skspatial.objects import Triangle

        >>> Triangle([0, 0], [0, 1], [1, 0]).is_right()
        True

        >>> Triangle([0, 0], [0, 1], [1, 1]).is_right()
        True

        >>> Triangle([0, 0], [1, 2], [2, 0]).is_right()
        False

        This triangle is approximately a right triangle.

        >>> triangle = Triangle([0, 0], [100, 0], [101, 100])

        >>> triangle.is_right()
        False

        >>> triangle.is_right(rel_tol=1e-2)
        True

        """
        a, b, c = sorted(self.multiple('length', 'abc'))

        return math.isclose(a**2 + b**2, c**2, **kwargs)

    def plot_2d(self, ax_2d: Axes, part: str = 'points', **kwargs: str) -> None:
        """
        Plot a triangle in 2D.

        Parameters
        ----------
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

            >>> triangle.plot_2d(ax, part='points', s=100, zorder=3)
            >>> triangle.plot_2d(ax, part='lines', c='k')

        """
        if part == 'points':
            for point in self.multiple('point', 'ABC'):
                point.plot_2d(ax_2d, **kwargs)

        elif part == 'lines':
            for line in self.multiple('line', 'abc'):
                line.plot_2d(ax_2d, **kwargs)

    def plot_3d(self, ax_3d: Axes3D, part: str = 'points', **kwargs: str) -> None:
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
        if part == 'points':
            for point in self.multiple('point', 'ABC'):
                point.plot_3d(ax_3d, **kwargs)

        elif part == 'lines':
            for line in self.multiple('line', 'abc'):
                line.plot_3d(ax_3d, **kwargs)
