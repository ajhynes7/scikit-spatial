"""Area of spatial objects."""

import numpy as np
from dpcontracts import require, ensure
from numpy.linalg import norm

from .array import Point, Vector


@require(
    "The inputs must be three points.",
    lambda args: all(
        isinstance(x, Point) for x in [args.point_a, args.point_b, args.point_c]
    ),
)
@ensure("The output must be a number.", lambda _, result: isinstance(result, np.number))
def area_triangle(point_a, point_b, point_c):
    """
    Return the area of a triangle defined by three points.

    The points are the three vertices of the triangle.

    References
    ----------
    http://mathworld.wolfram.com/TriangleArea.html

    """
    vector_ab = Vector.from_points(point_a, point_b)
    vector_ac = Vector.from_points(point_a, point_c)

    return 0.5 * norm(vector_ab.cross(vector_ac))
