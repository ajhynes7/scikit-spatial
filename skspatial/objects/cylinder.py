"""Module for the Cylinder class."""

from __future__ import annotations

from typing import Tuple

import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from skspatial._base_spatial import _BaseSpatial
from skspatial._functions import np_float
from skspatial.objects.line import Line
from skspatial.objects.plane import Plane
from skspatial.objects.point import Point
from skspatial.objects.vector import Vector
from skspatial.typing import array_like


class Cylinder(_BaseSpatial):
    """
    A cylinder in space.

    The cylinder is defined by a point at its base, a vector along its axis, and a radius.

    Parameters
    ----------
    point : array_like
        Centre of the cylinder base.
    vector : array_like
        Normal vector of the cylinder base (the vector along the cylinder axis).
        The length of the cylinder is the length of this vector.
    radius : {int, float}
        Radius of the cylinder.
        This is the radius of the circular base.

    Attributes
    ----------
    point : Point
        Centre of the cylinder base.
    vector : Vector
        Normal vector of the cylinder base.
    radius : {int, float}
        Radius of the cylinder.
    dimension : int
        Dimension of the cylinder.

    Raises
    ------
    ValueError
        If the point or vector are not 3D,
        if the vector is all zeros,
        or if the radius is zero.

    Examples
    --------
    >>> from skspatial.objects import Cylinder

    >>> Cylinder([0, 0], [1, 0, 0], 1)
    Traceback (most recent call last):
    ...
    ValueError: The point must be 3D.

    >>> Cylinder([0, 0, 0], [1, 0], 1)
    Traceback (most recent call last):
    ...
    ValueError: The vector must be 3D.

    >>> Cylinder([0, 0, 0], [0, 0, 0], 1)
    Traceback (most recent call last):
    ...
    ValueError: The vector must not be the zero vector.

    >>> Cylinder([0, 0, 0], [0, 0, 1], 0)
    Traceback (most recent call last):
    ...
    ValueError: The radius must be positive.

    >>> cylinder = Cylinder([0, 0, 0], [0, 0, 1], 1)

    >>> cylinder
    Cylinder(point=Point([0, 0, 0]), vector=Vector([0, 0, 1]), radius=1)

    >>> cylinder.point
    Point([0, 0, 0])
    >>> cylinder.vector
    Vector([0, 0, 1])
    >>> cylinder.radius
    1
    >>> cylinder.dimension
    3

    """

    def __init__(self, point: array_like, vector: array_like, radius: float):

        self.point = Point(point)
        self.vector = Vector(vector)

        if self.point.dimension != 3:
            raise ValueError("The point must be 3D.")

        if self.vector.dimension != 3:
            raise ValueError("The vector must be 3D.")

        if self.vector.is_zero():
            raise ValueError("The vector must not be the zero vector.")

        self.radius = radius

        if not self.radius > 0:
            raise ValueError("The radius must be positive.")

        self.dimension = self.point.dimension

    def __repr__(self) -> str:

        repr_point = np.array_repr(self.point)
        repr_vector = np.array_repr(self.vector)

        return f"Cylinder(point={repr_point}, vector={repr_vector}," f" radius={self.radius})"

    @classmethod
    def from_points(cls, point_a: array_like, point_b: array_like, radius: float) -> Cylinder:
        """
        Instantiate a cylinder from two points and a radius.

        Parameters
        ----------
        point_a, point_b : array_like
            The centres of the two circular ends.
        radius : float
            The cylinder radius.

        Returns
        -------
        Cylinder
            The cylinder defined by the two points and the radius.

        Examples
        --------
        >>> from skspatial.objects import Cylinder

        >>> Cylinder.from_points([0, 0, 0], [0, 0, 1], 1)
        Cylinder(point=Point([0, 0, 0]), vector=Vector([0, 0, 1]), radius=1)

        >>> Cylinder.from_points([0, 0, 0], [0, 0, 2], 1)
        Cylinder(point=Point([0, 0, 0]), vector=Vector([0, 0, 2]), radius=1)

        """
        vector_ab = Vector.from_points(point_a, point_b)

        return cls(point_a, vector_ab, radius)

    def length(self) -> np.float64:
        """
        Return the length of the cylinder.

        This is the length of the vector used to initialize the cylinder.

        Returns
        -------
        np.float64
            Length of the cylinder.

        Examples
        --------
        >>> from skspatial.objects import Cylinder

        >>> Cylinder([0, 0, 0], [0, 0, 1], 1).length()
        1.0

        >>> Cylinder([0, 0, 0], [0, 0, 2], 1).length()
        2.0

        >>> Cylinder([0, 0, 0], [1, 1, 1], 1).length().round(3)
        1.732

        """
        return self.vector.norm()

    @np_float
    def volume(self) -> float:
        r"""
        Return the volume of the cylinder.

        The volume :math:`V` of a cylinder with radius :math:`r` and length :math:`l` is

        .. math:: V = \pi r^2 l

        Returns
        -------
        np.float64
            Volume of the cylinder.

        Examples
        --------
        >>> from skspatial.objects import Cylinder

        >>> Cylinder([0, 0, 0], [0, 0, 1], 1).volume().round(5)
        3.14159

        The length of the vector sets the length of the cylinder.

        >>> Cylinder([0, 0, 0], [0, 0, 2], 1).volume().round(5)
        6.28319

        """
        return np.pi * self.radius ** 2 * self.length()

    def contains_point(self, point: array_like) -> bool:
        """
        Check if a point is inside the cylinder.

        A point on the surface is also considered to be inside.

        Parameters
        ----------
        point : array_like
            Input point

        Returns
        -------
        bool
            True if the point is inside of the cylinder.

        Examples
        --------
        >>> from skspatial.objects import Cylinder

        >>> cylinder = Cylinder([0, 0, 0], [0, 0, 1], 1)

        >>> cylinder.contains_point([0, 0, 0])
        True
        >>> cylinder.contains_point([0, 0, 1])
        True
        >>> cylinder.contains_point([0, 0, 2])
        False
        >>> cylinder.contains_point([0, 0, -1])
        False
        >>> cylinder.contains_point([1, 0, 0])
        True
        >>> cylinder.contains_point([0, 1, 0])
        True
        >>> cylinder.contains_point([1, 1, 0])
        False

        """
        line_axis = Line(self.point, self.vector)
        distance_to_axis = line_axis.distance_point(point)

        within_radius = distance_to_axis <= self.radius

        plane_base = Plane(self.point, self.vector)
        distance_point_signed = plane_base.distance_point_signed(point)

        within_planes = distance_point_signed <= self.length() and distance_point_signed >= 0

        return within_radius and within_planes

    def to_mesh(self, n_along_axis: int = 100, n_angles: int = 30) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Return coordinate matrices for the 3D surface of the cylinder.

        Parameters
        ----------
        n_along_axis : int
            Number of intervals along the axis of the cylinder.
        n_angles : int
            Number of angles distributed around the circle.

        Returns
        -------
        X, Y, Z: (n_angles, n_angles) ndarray
            Coordinate matrices.

        Examples
        --------
        >>> from skspatial.objects import Cylinder

        >>> X, Y, Z = Cylinder([0, 0, 0], [0, 0, 1], 1).to_mesh(2, 4)

        >>> X.round(3)
        array([[-1. , -1. ],
               [ 0.5,  0.5],
               [ 0.5,  0.5],
               [-1. , -1. ]])

        >>> Y.round(3)
        array([[ 0.   ,  0.   ],
               [ 0.866,  0.866],
               [-0.866, -0.866],
               [-0.   , -0.   ]])

        >>> Z.round(3)
        array([[0., 1.],
               [0., 1.],
               [0., 1.],
               [0., 1.]])

        """
        # Unit vector along the cylinder axis.
        v_axis = self.vector.unit()

        # Arbitrary unit vector in a direction other than the axis.
        # This is used to get a vector perpendicular to the axis.
        v_different_direction = v_axis.different_direction()

        # Two unit vectors that are mutually perpendicular
        # and perpendicular to the cylinder axis.
        # These are used to define the points on the cylinder surface.
        u_1 = v_axis.cross(v_different_direction)
        u_2 = v_axis.cross(u_1)

        # The cylinder surface ranges over t from 0 to length of axis,
        # and over theta from 0 to 2 * pi.
        t = np.linspace(0, self.length(), n_along_axis)
        theta = np.linspace(0, 2 * np.pi, n_angles)

        # use meshgrid to make 2d arrays
        t, theta = np.meshgrid(t, theta)

        X, Y, Z = [
            self.point[i] + v_axis[i] * t + self.radius * np.sin(theta) * u_1[i] + self.radius * np.cos(theta) * u_2[i]
            for i in range(3)
        ]

        return X, Y, Z

    def plot_3d(self, ax_3d: Axes3D, n_along_axis: int = 100, n_angles: int = 30, **kwargs) -> None:
        """
        Plot a 3D cylinder.

        Parameters
        ----------
        ax_3d : Axes3D
            Instance of :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.
        n_along_axis : int
            Number of intervals along the axis of the cylinder.
        n_angles : int
            Number of angles distributed around the circle.
        kwargs : dict, optional
            Additional keywords passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot_surface`.

        Examples
        --------
        .. plot::
            :include-source:

            >>> import matplotlib.pyplot as plt
            >>> from mpl_toolkits.mplot3d import Axes3D

            >>> from skspatial.objects import Cylinder

            >>> fig = plt.figure()
            >>> ax = fig.add_subplot(111, projection='3d')

            >>> cylinder = Cylinder([5, 3, 1], [1, 0, 1], 2)

            >>> cylinder.plot_3d(ax, alpha=0.2)
            >>> cylinder.point.plot_3d(ax, s=100)

        """
        X, Y, Z = self.to_mesh(n_along_axis, n_angles)

        ax_3d.plot_surface(X, Y, Z, **kwargs)
