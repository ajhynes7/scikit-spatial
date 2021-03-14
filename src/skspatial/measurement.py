"""Measurements using spatial objects."""
import numpy as np

from skspatial.objects import Vector
from skspatial.typing import array_like


def area_triangle(point_a: array_like, point_b: array_like, point_c: array_like) -> np.float64:
    """
    Return the area of a triangle defined by three points.

    The points are the vertices of the triangle. They must be 3D or less.

    Parameters
    ----------
    point_a, point_b, point_c : array_like
        The three vertices of the triangle.

    Returns
    -------
    np.float64
        The area of the triangle.

    References
    ----------
    http://mathworld.wolfram.com/TriangleArea.html

    Examples
    --------
    >>> from skspatial.measurement import area_triangle

    >>> area_triangle([0, 0], [0, 1], [1, 0])
    0.5

    >>> area_triangle([0, 0], [0, 2], [1, 1])
    1.0

    >>> area_triangle([3, -5, 1], [5, 2, 1], [9, 4, 2]).round(2)
    12.54

    """
    vector_ab = Vector.from_points(point_a, point_b)
    vector_ac = Vector.from_points(point_a, point_c)

    # Normal vector of plane defined by the three points.
    vector_normal = vector_ab.cross(vector_ac)

    return 0.5 * vector_normal.norm()


def volume_tetrahedron(
    point_a: array_like,
    point_b: array_like,
    point_c: array_like,
    point_d: array_like,
) -> np.float64:
    """
    Return the volume of a tetrahedron defined by four points.

    The points are the vertices of the tetrahedron. They must be 3D or less.

    Parameters
    ----------
    point_a, point_b, point_c, point_d : array_like
        The four vertices of the tetrahedron.

    Returns
    -------
    np.float64
        The volume of the tetrahedron.

    References
    ----------
    http://mathworld.wolfram.com/Tetrahedron.html

    Examples
    --------
    >>> from skspatial.measurement import volume_tetrahedron

    >>> volume_tetrahedron([0, 0], [3, 2], [-3, 5], [1, 8])
    0.0

    >>> volume_tetrahedron([0, 0, 0], [2, 0, 0], [1, 1, 0], [0, 0, 1]).round(3)
    0.333

    >>> volume_tetrahedron([0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]).round(3)
    0.167

    """
    vector_ab = Vector.from_points(point_a, point_b)
    vector_ac = Vector.from_points(point_a, point_c)
    vector_ad = Vector.from_points(point_a, point_d)

    vector_cross = vector_ac.cross(vector_ad)

    # Set the dimension to 3 so it matches the cross product.
    vector_ab = vector_ab.set_dimension(3)

    return 1 / 6 * abs(vector_ab.dot(vector_cross))
