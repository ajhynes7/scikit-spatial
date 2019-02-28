"""Measurements using spatial objects."""

from dpcontracts import ensure, types

from skspatial.objects import Point, Vector, Line


@types(line_a=Line, line_b=Line)
@ensure("The output must be zero or greater.", lambda _, result: result >= 0)
def distance_lines(line_a, line_b):
    """
    Return the shortest distance between two lines.

    Parameters
    ----------
    line_a : Line
        Input line A.
    line_b : Line
        Input line B.

    Returns
    -------
    number
        The distance between the lines.

    Examples
    --------
    >>> from skspatial.objects import Point, Vector, Line

    >>> line_a = Line(Point([0, 0]), Vector([1, 0]))
    >>> line_b = Line(Point([0, 1]), Vector([1, 0]))
    >>> line_c = Line(Point([0, 1]), Vector([1, 1]))
    >>> line_d = Line(Point([0, 5]), Vector([0, 0, 1]))

    The lines are parallel.
    >>> distance_lines(line_a, line_b)
    1.0

    The lines are coplanar and not parallel.
    >>> distance_lines(line_a, line_c)
    0.0

    The lines are skew.
    >>> distance_lines(line_a, line_d)
    5.0

    References
    ----------
    http://mathworld.wolfram.com/Line-LineDistance.html

    """
    if line_a.is_parallel(line_b):
        # The lines are parallel.
        # The distance between the lines is the distance from line point B to line A.
        distance = line_a.distance(line_b.point)

    elif line_a.is_coplanar(line_b):
        # The lines must intersect, since they are coplanar and not parallel.
        distance = 0.0

    else:
        # The lines are skew.
        vector_ab = Vector.from_points(line_a.point, line_b.point)
        vector_cross = line_a.direction.cross(line_b.direction)

        distance = abs(vector_ab.dot(vector_cross)) / vector_cross.magnitude

    return distance


@types(point_a=Point, point_b=Point, point_c=Point)
@ensure("The output must be zero or greater.", lambda _, result: result >= 0)
@ensure("The output must be a float.", lambda _, result: isinstance(result, float))
def area_triangle(point_a, point_b, point_c):
    """
    Return the area of a triangle defined by three points.

    The points are the three vertices of the triangle.

    Parameters
    ----------
    point_a, point_b, point_c : Point
        Input points.

    Returns
    -------
    float
        The area of the triangle.

    Examples
    --------
    >>> from skspatial.objects import Point

    >>> area_triangle(Point([0, 0]), Point([0, 1]), Point([1, 0]))
    0.5

    >>> area_triangle(Point([0, 0]), Point([0, 2]), Point([1, 1]))
    1.0

    References
    ----------
    http://mathworld.wolfram.com/TriangleArea.html

    """
    vector_ab = Vector.from_points(point_a, point_b)
    vector_ac = Vector.from_points(point_a, point_c)

    vector_cross = vector_ab.cross(vector_ac)

    return 0.5 * vector_cross.magnitude


@types(point_a=Point, point_b=Point, point_c=Point, point_d=Point)
@ensure("The output must be zero or greater.", lambda _, result: result >= 0)
@ensure("The output must be a float.", lambda _, result: isinstance(result, float))
def volume_tetrahedron(point_a, point_b, point_c, point_d):
    """
    Return the volume of a tetrahedron defined by four points.

    The points are the four vertices of the tetrahedron.

    Parameters
    ----------
    point_a: Point
        Input point A.
    point_b: Point
        Input point B.
    point_c: Point
        Input point C.
    point_d: Point
        Input point D.

    Returns
    -------
    float
        The volume of the tetrahedron.

    Examples
    --------
    >>> from skspatial.objects import Point

    >>> volume_tetrahedron(Point([0, 0]), Point([3, 2]), Point([-3, 5]), Point([1, 8]))
    0.0

    >>> volume = volume_tetrahedron(Point([0, 0]), Point([2, 0]), Point([1, 1]), Point([0, 0, 1]))
    >>> round(volume, 3)
    0.333

    References
    ----------
    http://mathworld.wolfram.com/Tetrahedron.html

    """
    vector_ab = Vector.from_points(point_a, point_b)
    vector_ac = Vector.from_points(point_a, point_c)
    vector_ad = Vector.from_points(point_a, point_d)

    vector_cross = vector_ac.cross(vector_ad)

    return 1 / 6 * abs(vector_ab.dot(vector_cross))
