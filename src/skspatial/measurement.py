"""Measurements using spatial objects."""
import numpy as np

from skspatial.objects import Points
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


def area_signed(points: array_like) -> float:
    """
    Return the signed area of a simple polygon given the 2D coordinates of its veritces.

    The signed area is computed using the shoelace algorithm. A positive area is
    returned for a polygon whose vertices are given by a counter-clockwise
    sequence of points.

    Parameters
    ----------
    points : array_like
         Input 2D points.

    Returns
    -------
    area_signed : float
        The signed area of the polygon.

    Raises
    ------
    ValueError
        If the points are not 2D.
        If there are fewer than three points.

    References
    ----------
    https://en.wikipedia.org/wiki/Shoelace_formula
    https://alexkritchevsky.com/2018/08/06/oriented-area.html
    https://rosettacode.org/wiki/Shoelace_formula_for_polygonal_area#Python

    Examples
    --------
    >>> from skspatial.measurement import area_signed

    >>> area_signed([[0, 0], [1, 0], [0, 1]])
    0.5

    >>> area_signed([[0, 0], [0, 1], [1, 0]])
    -0.5

    >>> area_signed([[0, 0], [0, 1], [1, 2], [2, 1], [2, 0]])
    -3.0

    """
    points = Points(points)
    n_points = points.shape[0]

    if points.dimension != 2:
        raise ValueError("The points must be 2D.")

    if n_points < 3:
        raise ValueError("There must be at least 3 points.")

    X = points[:, 0]
    Y = points[:, 1]

    indices = np.arange(n_points)
    indices_offset = indices - 1

    return 0.5 * np.sum(X[indices_offset] * Y[indices] - X[indices] * Y[indices_offset])
