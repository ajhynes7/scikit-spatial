"""Projection of spatial objects."""

from dpcontracts import require, ensure

from .objects import Point, Vector, Line


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
    >>> project_vector(Vector([1, 1]), Vector([0, 1]))
    Vector([0. 1. 0.])

    >>> project_vector(Vector([5, 5]), Vector([0, 1]))
    Vector([0. 5. 0.])

    """
    unit_v = vector_v.unit()

    # Scalar projection of u onto v.
    scalar_projection = vector_u.dot(vector_v)

    return Vector(scalar_projection * unit_v.array)


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
    return Point(line.point.array + vector_projected.array)
