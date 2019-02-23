"""Distances between spatial objects."""

from dpcontracts import require, ensure

from skspatial.area import area_triangle
from skspatial.objects import Point, Vector, Line, Plane


@require(
    "The inputs must be a point and a line.",
    lambda args: isinstance(args.point, Point) and isinstance(args.line, Line),
)
@ensure("The output must be a float.", lambda _, result: isinstance(result, float))
@ensure("The output must be zero or greater.", lambda _, result: result >= 0)
def dist_point_line(point, line):
    """
    Compute the distance from a point to a line.

    Parameters
    ----------
    point : Point
    line : Line

    Returns
    -------
    float
        Distance from the point to the line.

    Examples
    --------
    >>> from skspatial.objects import Vector

    >>> line = Line(Point([0, 0]), Vector([1, 0]))

    >>> dist_point_line(Point([0, 5]), line)
    5.0

    >>> dist_point_line(Point([10, -6]), line)
    6.0

    References
    ----------
    http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html

    """
    point_a = line.point
    point_b = line.to_point(t=1)

    area = area_triangle(point_a, point_b, point)

    return 2 * area / line.direction.magnitude


@require(
    "The inputs must be a point and a plane.",
    lambda args: isinstance(args.point, Point) and isinstance(args.plane, Plane),
)
@ensure("The output must be a float.", lambda _, result: isinstance(result, float))
def dist_point_plane(point, plane):
    """
    Compute the signed distance from a point to a plane.

    Parameters
    ----------
    point : Point
    line : Plane

    Returns
    -------
    float
        Signed distance from the point to plane.

    Examples
    --------
    >>> from skspatial.objects import Point, Vector, Plane

    >>> plane = Plane(Point([0, 0]), Vector([0, 0, 1]))

    >>> dist_point_plane(Point([5, 2]), plane)
    0.0

    >>> dist_point_plane(Point([5, 2, 1]), plane)
    1.0

    >>> dist_point_plane(Point([5, 2, -4]), plane)
    -4.0

    References
    ----------
    http://mathworld.wolfram.com/Point-PlaneDistance.html

    """
    vector_to_point = Vector.from_points(plane.point, point)

    return plane.normal.dot(vector_to_point)
