"""Module for the Cylinder class."""

import numpy as np

from skspatial._functions import np_float
from skspatial.objects.line import Line
from skspatial.objects.plane import Plane
from skspatial.objects.point import Point
from skspatial.objects.vector import Vector
from skspatial.typing import array_like


class Cylinder:
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
