"""Module for the Sphere class."""
from __future__ import annotations

import math
from typing import Tuple

import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from skspatial._functions import np_float
from skspatial.objects._base_sphere import _BaseSphere
from skspatial.objects._mixins import _ToPointsMixin
from skspatial.objects.line import Line
from skspatial.objects.point import Point
from skspatial.objects.points import Points
from skspatial.objects.vector import Vector
from skspatial.typing import array_like


class Sphere(_BaseSphere, _ToPointsMixin):
    """
    A sphere in 3D space.

    The sphere is defined by a 3D point and a radius.

    Parameters
    ----------
    point : (3,) array_like
        Center of the sphere.
    radius : {int, float}
        Radius of the sphere.

    Attributes
    ----------
    point : (3,) Point
        Center of the sphere.
    radius : {int, float}
        Radius of the sphere.
    dimension : int
        Dimension of the sphere.

    Raises
    ------
    ValueError
        If the radius is not positive.
        If the point is not 3D.

    Examples
    --------
    >>> from skspatial.objects import Sphere

    >>> sphere = Sphere([1, 2, 3], 5)

    >>> sphere
    Sphere(point=Point([1, 2, 3]), radius=5)

    >>> sphere.dimension
    3

    >>> sphere.surface_area().round(2)
    314.16

    >>> Sphere([0, 0], 0)
    Traceback (most recent call last):
    ...
    ValueError: The radius must be positive.

    >>> Sphere([0, 0, 0, 0], 1)
    Traceback (most recent call last):
    ...
    ValueError: The point must be 3D.

    """

    def __init__(self, point: array_like, radius: float):

        super().__init__(point, radius)

        if self.point.dimension != 3:
            raise ValueError("The point must be 3D.")

    @np_float
    def surface_area(self) -> float:
        r"""
        Return the surface area of the sphere.

        The surface area :math:`A` of a sphere with radius :math:`r` is

        .. math:: A = 4 \pi r ^ 2

        Returns
        -------
        np.float64
            Surface area of the sphere.

        Examples
        --------
        >>> from skspatial.objects import Sphere

        >>> Sphere([0, 0, 0], 1).surface_area().round(2)
        12.57

        >>> Sphere([0, 0, 0], 2).surface_area().round(2)
        50.27

        """
        return 4 * np.pi * self.radius**2

    @np_float
    def volume(self) -> float:
        r"""
        Return the volume of the sphere.

        The volume :math:`V` of a sphere with radius :math:`r` is

        .. math:: V = \frac{4}{3} \pi r ^ 3

        Returns
        -------
        np.float64
            Volume of the sphere.

        Examples
        --------
        >>> from skspatial.objects import Sphere

        >>> Sphere([0, 0, 0], 1).volume().round(2)
        4.19

        >>> Sphere([0, 0, 0], 2).volume().round(2)
        33.51

        """
        return 4 / 3 * np.pi * self.radius**3

    def intersect_line(self, line: Line) -> Tuple[Point, Point]:
        """
        Intersect the sphere with a line.

        A line intersects a sphere at two points.

        Parameters
        ----------
        line : Line
            Input line.

        Returns
        -------
        point_a, point_b : Point
            The two points of intersection.

        Examples
        --------
        >>> from skspatial.objects import Sphere, Line

        >>> sphere = Sphere([0, 0, 0], 1)

        >>> sphere.intersect_line(Line([0, 0, 0], [1, 0, 0]))
        (Point([-1.,  0.,  0.]), Point([1., 0., 0.]))

        >>> sphere.intersect_line(Line([0, 0, 1], [1, 0, 0]))
        (Point([0., 0., 1.]), Point([0., 0., 1.]))

        >>> sphere.intersect_line(Line([0, 0, 2], [1, 0, 0]))
        Traceback (most recent call last):
        ...
        ValueError: The line does not intersect the sphere.

        """
        vector_to_line = Vector.from_points(self.point, line.point)
        vector_unit = line.direction.unit()

        dot = vector_unit.dot(vector_to_line)

        discriminant = dot**2 - (vector_to_line.norm() ** 2 - self.radius**2)

        if discriminant < 0:
            raise ValueError("The line does not intersect the sphere.")

        pm = np.array([-1, 1])  # Array to compute minus/plus.
        distances = -dot + pm * math.sqrt(discriminant)

        point_a, point_b = line.point + distances.reshape(-1, 1) * vector_unit

        return point_a, point_b

    @classmethod
    def best_fit(cls, points: array_like) -> Sphere:
        """
        Return the sphere of best fit for a set of 3D points.

        Parameters
        ----------
        points : array_like
             Input 3D points.

        Returns
        -------
        Sphere
            The sphere of best fit.

        Raises
        ------
        ValueError
            If the points are not 3D.
            If there are fewer than four points.
            If the points lie in a plane.

        Examples
        --------
        >>> import numpy as np

        >>> from skspatial.objects import Sphere

        >>> points = [[1, 0, 1], [0, 1, 1], [1, 2, 1], [1, 1, 2]]
        >>> sphere = Sphere.best_fit(points)

        >>> sphere.point
        Point([1., 1., 1.])

        >>> np.round(sphere.radius, 2)
        1.0

        """
        points = Points(points)

        if points.dimension != 3:
            raise ValueError("The points must be 3D.")

        if points.shape[0] < 4:
            raise ValueError("There must be at least 4 points.")

        if points.affine_rank() != 3:
            raise ValueError("The points must not be in a plane.")

        n = points.shape[0]
        A = np.hstack((2 * points, np.ones((n, 1))))
        b = (points**2).sum(axis=1)

        c, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        center = c[:3]
        radius = float(np.sqrt(np.dot(center, center) + c[3]))

        return cls(center, radius)

    def to_mesh(self, n_angles: int = 30) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Return coordinate matrices for the 3D surface of the sphere.

        Parameters
        ----------
        n_angles: int
            Number of angles used to generate the coordinate matrices.

        Returns
        -------
        X, Y, Z: (n_angles, n_angles) ndarray
            Coordinate matrices.

        Examples
        --------
        >>> from skspatial.objects import Sphere

        >>> X, Y, Z = Sphere([0, 0, 0], 1).to_mesh(5)

        >>> X.round(3)
        array([[ 0.   ,  0.   ,  0.   ,  0.   ,  0.   ],
               [ 0.   ,  0.707,  0.   , -0.707, -0.   ],
               [ 0.   ,  1.   ,  0.   , -1.   , -0.   ],
               [ 0.   ,  0.707,  0.   , -0.707, -0.   ],
               [ 0.   ,  0.   ,  0.   , -0.   , -0.   ]])

        >>> Y.round(3)
        array([[ 0.   ,  0.   ,  0.   ,  0.   ,  0.   ],
               [ 0.707,  0.   , -0.707, -0.   ,  0.707],
               [ 1.   ,  0.   , -1.   , -0.   ,  1.   ],
               [ 0.707,  0.   , -0.707, -0.   ,  0.707],
               [ 0.   ,  0.   , -0.   , -0.   ,  0.   ]])

        >>> Z.round(3)
        array([[ 1.   ,  1.   ,  1.   ,  1.   ,  1.   ],
               [ 0.707,  0.707,  0.707,  0.707,  0.707],
               [ 0.   ,  0.   ,  0.   ,  0.   ,  0.   ],
               [-0.707, -0.707, -0.707, -0.707, -0.707],
               [-1.   , -1.   , -1.   , -1.   , -1.   ]])

        """
        angles_a = np.linspace(0, np.pi, n_angles)
        angles_b = np.linspace(0, 2 * np.pi, n_angles)

        sin_angles_a = np.sin(angles_a)
        cos_angles_a = np.cos(angles_a)

        sin_angles_b = np.sin(angles_b)
        cos_angles_b = np.cos(angles_b)

        X = self.point[0] + self.radius * np.outer(sin_angles_a, sin_angles_b)
        Y = self.point[1] + self.radius * np.outer(sin_angles_a, cos_angles_b)
        Z = self.point[2] + self.radius * np.outer(cos_angles_a, np.ones_like(angles_b))

        return X, Y, Z

    def plot_3d(self, ax_3d: Axes3D, n_angles: int = 30, **kwargs) -> None:
        """
        Plot the sphere in 3D.

        Parameters
        ----------
        ax_3d : Axes3D
            Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
        kwargs : dict, optional
            Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot_surface`.

        Examples
        --------
        .. plot::
            :include-source:

            >>> import matplotlib.pyplot as plt
            >>> from mpl_toolkits.mplot3d import Axes3D

            >>> from skspatial.objects import Sphere

            >>> fig = plt.figure()
            >>> ax = fig.add_subplot(111, projection='3d')

            >>> sphere = Sphere([1, 2, 3], 2)

            >>> sphere.plot_3d(ax, alpha=0.2)
            >>> sphere.point.plot_3d(ax, s=100)

        """
        X, Y, Z = self.to_mesh(n_angles)

        ax_3d.plot_surface(X, Y, Z, **kwargs)
