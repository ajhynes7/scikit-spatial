"""Measurements using spatial objects."""

import numpy as np
from dpcontracts import ensure

from skspatial.objects import Vector


@ensure("The output must be zero or greater.", lambda _, result: result >= 0)
@ensure("The output must be a NumPy scalar.", lambda _, result: isinstance(result, np.number))
def area_triangle(point_a, point_b, point_c):
    """
    Return the area of a triangle defined by three points.

    The points are the three vertices of the triangle.
    The points must be 3D or less.

    Parameters
    ----------
    point_a, point_b, point_c : array_like
        The three vertices of the triangle.

    Returns
    -------
    scalar
        The area of the triangle.

    Examples
    --------
    >>> from skspatial.measurement import area_triangle

    >>> area_triangle([0, 0], [0, 1], [1, 0])
    0.5

    >>> area_triangle([0, 0], [0, 2], [1, 1])
    1.0

    References
    ----------
    http://mathworld.wolfram.com/TriangleArea.html

    """
    vector_ab = Vector.from_points(point_a, point_b)
    vector_ac = Vector.from_points(point_a, point_c)

    # Normal vector of plane defined by the three points.
    vector_normal = vector_ab.cross(vector_ac)

    return 0.5 * vector_normal.norm()


@ensure("The output must be zero or greater.", lambda _, result: result >= 0)
@ensure("The output must be a NumPy scalar.", lambda _, result: isinstance(result, np.number))
def volume_tetrahedron(point_a, point_b, point_c, point_d):
    """
    Return the volume of a tetrahedron defined by four points.

    The points are the four vertices of the tetrahedron.
    The points must be 3D or less.

    Parameters
    ----------
    point_a, point_b, point_c, point_d : array_like
        The four vertices of the tetrahedron.

    Returns
    -------
    scalar
        The volume of the tetrahedron.

    Examples
    --------
    >>> from skspatial.measurement import volume_tetrahedron

    >>> volume_tetrahedron([0, 0], [3, 2], [-3, 5], [1, 8])
    0.0

    >>> volume = volume_tetrahedron([0, 0, 0], [2, 0, 0], [1, 1, 0], [0, 0, 1])
    >>> volume.round(3)
    0.333

    References
    ----------
    http://mathworld.wolfram.com/Tetrahedron.html

    """
    vector_ab = Vector.from_points(point_a, point_b)
    vector_ac = Vector.from_points(point_a, point_c)
    vector_ad = Vector.from_points(point_a, point_d)

    vector_cross = vector_ac.cross(vector_ad)

    # Set the dimension to 3 so it matches the cross product.
    vector_ab = vector_ab.set_dimension(3)

    return 1 / 6 * abs(vector_ab.dot(vector_cross))
