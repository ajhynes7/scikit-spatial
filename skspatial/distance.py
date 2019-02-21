"""Distances between spatial objects."""

import numpy as np
from dpcontracts import require, ensure
from numpy.linalg import norm

from skspatial import Point, Line
from .area import area_triangle


@require(
    "The inputs must be a point and a line.",
    lambda args: isinstance(args.point, Point) and isinstance(args.line, Line),
)
@ensure("The output must be a number.", lambda _, result: isinstance(result, np.number))
def dist_point_line(point, line):
    """
    Compute the shortest distance from a point to a line.

    Parameters
    ----------
    point : Point
    line : Line

    Returns
    -------
    number
        The shortest distance from the point to the line.

    References
    ----------
    http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html

    Examples
    --------
    >>> from skspatial import Vector

    >>> line = Line(Point([0, 0]), Vector([1, 0]))

    >>> dist_point_line(Point([0, 5]), line)
    5.0

    >>> dist_point_line(Point([10, -6]), line)
    6.0

    """
    point_a = line.point
    point_b = line.to_point(t=1)

    num = 2 * area_triangle(point_a, point_b, point)
    denom = norm(line.direction.array)

    return num / denom
