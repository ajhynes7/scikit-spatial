"""Projection of spatial objects."""

from dpcontracts import require, ensure

from .objects import Point, Vector, Line, Plane


@require(
    "The inputs must be two vectors.",
    lambda args: all(isinstance(x, Vector) for x in [args.vector_u, args.vector_v]),
)
@ensure("The output must be a vector.", lambda _, result: isinstance(result, Vector))
def project_vector(vector_u, vector_v):
    """
    Project vector u onto vector v.

    Parameters
    ----------
    vector_u, vector_v : Vector
        Input vectors.

    Returns
    -------
    Vector
        Projection of vector u onto vector v.

    Examples
    --------
    >>> project_vector(Vector([2, 1]), Vector([0, 1]))
    Vector([0. 1. 0.])

    >>> project_vector(Vector([2, 1]), Vector([0, 100]))
    Vector([0. 1. 0.])

    >>> project_vector(Vector([9, 5]), Vector([0, 1]))
    Vector([0. 5. 0.])

    >>> project_vector(Vector([9, 5]), Vector([0, 100]))
    Vector([0. 5. 0.])

    """
    unit_v = vector_v.unit()

    # Scalar projection of u onto v.
    scalar_projection = vector_u.dot(unit_v)

    return unit_v.scale(scalar_projection)


@require(
    "The inputs must be a point and a line.",
    lambda args: isinstance(args.point, Point) and isinstance(args.line, Line),
)
@ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
def project_point_line(point, line):
    """
    Project a point onto a line.

    Parameters
    ----------
    point : Point
    line : Line

    Returns
    -------
    Point
        Projection of the point onto the line.

    Examples
    --------
    >>> point = Point([5, 5])
    >>> line = Line(Point([0, 0]), Vector([1, 0]))

    >>> project_point_line(point, line)
    Point([5. 0. 0.])

    """
    # Vector from the point on the line to the point in space.
    vector_to_point = Vector.from_points(line.point, point)

    # Project the vector onto the line.
    vector_projected = project_vector(vector_to_point, line.direction)

    # Add the projected vector to the point on the line.
    return line.point.add(vector_projected)


@require(
    "The inputs must be a point and a plane.",
    lambda args: isinstance(args.point, Point) and isinstance(args.plane, Plane),
)
@ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
def project_point_plane(point, plane):
    """
    Project a point onto a plane.

    Parameters
    ----------
    point : Point
    plane : Plane

    Returns
    -------
    Point
        Projection of the point onto the plane.

    Examples
    --------
    >>> point = Point([10, 2, 5])
    >>> plane = Plane(Point([0, 0, 0]), Vector([0, 0, 1]))

    >>> project_point_plane(point, plane)
    Point([10.  2.  0.])

    """
    # Vector from the point in space to the point on the plane.
    vector_to_plane = Vector.from_points(point, plane.point)

    # Perpendicular vector from the point in space to the plane.
    vector_projected = project_vector(vector_to_plane, plane.normal)

    return point.add(vector_projected)
