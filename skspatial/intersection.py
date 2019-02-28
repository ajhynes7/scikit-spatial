"""Intersections of spatial objects."""

import numpy as np

from dpcontracts import require, ensure, types

from skspatial.objects import Point, Vector, Line, Plane


@types(line_a=Line, line_b=Line)
@require("The lines must be coplanar.", lambda args: args.line_a.is_coplanar(args.line_b))
@require("The lines must not be parallel.", lambda args: not args.line_a.is_parallel(args.line_b))
@ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
@ensure(
    "The point must be on both lines.",
    lambda args, result: args.line_a.contains(result) and args.line_b.contains(result),
)
def intersect_lines(line_a, line_b):
    """
    Return the intersection of two lines.

    The lines must be coplanar and not parallel.

    Parameters
    ----------
    line_a : Line
        Input line A.
    line_b : Line
        Input line B.

    Returns
    -------
    Point
        The point at the intersection.

    Examples
    --------
    >>> from skspatial.objects import Point, Vector, Line

    >>> line_a = Line(Point([0, 0]), Vector([1, 0]))
    >>> line_b = Line(Point([5, 5]), Vector([0, 1]))

    >>> intersect_lines(line_a, line_b)
    Point([5. 0. 0.])

    >>> intersect_lines(line_a, line_a)
    Traceback (most recent call last):
    ...
    dpcontracts.PreconditionError: The lines must not be parallel.

    >>> line_a = Line(Point([1, 2, 3]), Vector([-4, 1, 1]))
    >>> line_b = Line(Point([4, 5, 6]), Vector([3, 1, 5]))

    >>> intersect_lines(line_a, line_b)
    Traceback (most recent call last):
    ...
    dpcontracts.PreconditionError: The lines must be coplanar.

    >>> line_a = Line(Point([0, 0, 0]), Vector([1, 1, 1]))
    >>> line_b = Line(Point([5, 5, 0]), Vector([0, 0, -8]))

    >>> intersect_lines(line_a, line_b)
    Point([5. 5. 5.])

    References
    ----------
    http://mathworld.wolfram.com/Line-LineIntersection.html

    """
    # Vector from line A to line B.
    vector_ab = Vector.from_points(line_a.point, line_b.point)

    # Vector perpendicular to both lines.
    vector_perpendicular = line_a.direction.cross(line_b.direction)

    num = vector_ab.cross(line_b.direction).dot(vector_perpendicular)
    denom = vector_perpendicular.magnitude ** 2

    # Vector along line A to the intersection point.
    vector_a_scaled = line_a.direction.scale(num / denom)

    return line_a.point.add(vector_a_scaled)


@types(line=Line, plane=Plane)
@require(
    "The line and plane must not be parallel.",
    lambda args: not args.line.direction.is_perpendicular(args.plane.normal),
)
@ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
@ensure("The point must be on the line.", lambda args, result: args.line.contains(result))
@ensure("The point must be on the plane.", lambda args, result: args.plane.contains(result))
def intersect_line_plane(line, plane):
    """
    Return the intersection of a line and a plane.

    The line and plane must not be parallel.

    Parameters
    ----------
    line : Line
        Input line.
    plane : Plane
        Input plane.

    Returns
    -------
    Point
        The point at the intersection.

    Examples
    --------
    >>> from skspatial.objects import Point, Vector, Line, Plane

    >>> line = Line(Point([0, 0]), Vector([0, 0, 1]))
    >>> plane = Plane(Point([0, 0]), Vector([0, 0, 1]))

    >>> intersect_line_plane(line, plane)
    Point([0. 0. 0.])

    >>> plane = Plane(Point([2, -53, -7]), Vector([0, 0, 1]))
    >>> intersect_line_plane(line, plane)
    Point([ 0.  0. -7.])

    >>> line = Line(Point([0, 1]), Vector([1, 0, 0]))
    >>> intersect_line_plane(line, plane)
    Traceback (most recent call last):
    ...
    dpcontracts.PreconditionError: The line and plane must not be parallel.

    References
    ----------
    http://geomalgorithms.com/a05-_intersect-1.html

    """
    vector_plane_line = Vector.from_points(plane.point, line.point)

    num = - plane.normal.dot(vector_plane_line)
    denom = plane.normal.dot(line.direction)

    # Vector along the line to the intersection point.
    vector_line_scaled = line.direction.scale(num / denom)

    return line.point.add(vector_line_scaled)


@types(plane_a=Plane, plane_b=Plane)
@require("The planes must not be parallel.", lambda args: not args.plane_a.normal.is_parallel(args.plane_b.normal))
@ensure("The output must be a line.", lambda _, result: isinstance(result, Line))
@ensure(
    "The point on the line must be on both planes.",
    lambda args, result: args.plane_a.contains(result.point) and args.plane_b.contains(result.point),
)
def intersect_planes(plane_a, plane_b):
    """
    Return the intersection of two planes.

    The planes must not be parallel.

    Parameters
    ----------
    plane_a : Plane
        Input plane A.
    plane_b : Plane
        Input plane B.

    Returns
    -------
    Line
        The line of intersection.

    Examples
    --------
    >>> from skspatial.objects import Point, Vector, Plane

    >>> plane_a = Plane(Point([0]), Vector([0, 0, 1]))
    >>> plane_b = Plane(Point([0]), Vector([1, 0, 0]))

    >>> intersect_planes(plane_a, plane_b)
    Line(point=Point([0. 0. 0.]), direction=Vector([0. 1. 0.]))

    >>> plane_b = Plane(Point([5, 16, -94]), Vector([1, 0, 0]))
    >>> intersect_planes(plane_a, plane_b)
    Line(point=Point([5. 0. 0.]), direction=Vector([0. 1. 0.]))

    >>> plane_b = Plane(Point([0, 0, 1]), Vector([1, 0, 1]))
    >>> intersect_planes(plane_a, plane_b)
    Line(point=Point([1. 0. 0.]), direction=Vector([0. 1. 0.]))

    >>> plane_b = Plane(Point([0, 0, 5]), Vector([0, 0, -8]))
    >>> intersect_planes(plane_a, plane_b)
    Traceback (most recent call last):
    ...
    dpcontracts.PreconditionError: The planes must not be parallel.

    References
    ----------
    http://tbirdal.blogspot.com/2016/10/a-better-approach-to-plane-intersection.html

    """
    array_normals_stacked = np.vstack((plane_a.normal.array, plane_b.normal.array))

    # Construct a matrix for a linear system.
    array_00 = 2 * np.eye(3)
    array_01 = array_normals_stacked.T
    array_10 = array_normals_stacked
    array_11 = np.zeros((2, 2))
    matrix = np.block([[array_00, array_01], [array_10, array_11]])

    dot_a = np.dot(plane_a.point.array, plane_a.normal.array)
    dot_b = np.dot(plane_b.point.array, plane_b.normal.array)
    array_y = np.array([0, 0, 0, dot_a, dot_b])

    # Solve the linear system.
    solution = np.linalg.solve(matrix, array_y)

    point_line = Point(solution[:3])
    direction_line = plane_a.normal.cross(plane_b.normal)

    return Line(point_line, direction_line)
