from dpcontracts import require, ensure

from skspatial.comparison import are_parallel, are_perpendicular, are_collinear
from .array import Point, Vector


class _BaseLinePlane:
    """Private parent class for Line and Plane."""

    @require(
        "The inputs must be a point and a vector.",
        lambda args: isinstance(args.point, Point) and isinstance(args.vector, Vector),
    )
    def __init__(self, point, vector):

        self.point = point
        self.vector = vector.unit()

    def __eq__(self, other):

        return vars(self) == vars(other)

    @require(
        "The input must have the same type as the object.",
        lambda args: isinstance(args.other, type(args.self)),
    )
    def is_close(self, other, **kwargs):

        close_point = self.point.is_close(other.point, **kwargs)
        close_vector = self.vector.is_close(other.vector, **kwargs)

        return close_point and close_vector

    def distance(self, point):
        """Compute the distance from a point to this object."""
        point_projected = self.project(point)

        return point.distance(point_projected)


class Line(_BaseLinePlane):
    def __init__(self, point, vector):

        super().__init__(point, vector)

        self.direction = self.vector

    def __repr__(self):

        return f"Line(point={self.point}, direction={self.direction})"

    @classmethod
    @require(
        "The inputs must be two points.",
        lambda args: all(isinstance(x, Point) for x in args[1:]),
    )
    @require("The points must be different.", lambda args: args.point_a != args.point_b)
    @ensure("The output must be a line.", lambda _, result: isinstance(result, Line))
    def from_points(cls, point_a, point_b):
        """Define a line from two points."""
        vector_ab = Vector.from_points(point_a, point_b)

        return cls(point_a, vector_ab)

    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    def to_point(self, t=1):
        """
        Return a point along the line using a parameter t.

        Computed as line.point + t * line.direction.

        """
        vector_along_line = self.direction.scale(t)
        return self.point.add(vector_along_line)

    @require("The input must be a point.", lambda args: isinstance(args.point, Point))
    def contains(self, point, **kwargs):
        """Check if this line contains a point."""
        vector_to_point = Vector.from_points(self.point, point)

        return are_parallel(vector_to_point, self.direction, **kwargs)

    def project(self, point):
        """Project a point onto this line."""
        return project_point_line(point, self)


class Plane(_BaseLinePlane):
    def __init__(self, point, vector):

        super().__init__(point, vector)

        self.normal = self.vector

    def __repr__(self):

        return f"Plane(point={self.point}, normal={self.normal})"

    @classmethod
    @require(
        "The inputs must be three points.",
        lambda args: all(isinstance(x, Point) for x in args[1:]),
    )
    @require(
        "The points must not be collinear.",
        lambda args: not are_collinear(args.point_a, args.point_b, args.point_c),
    )
    @ensure("The output must be a plane.", lambda _, result: isinstance(result, Plane))
    def from_points(cls, point_a, point_b, point_c):
        """Define a plane from three 3D points."""
        vector_ab = Vector.from_points(point_a, point_b)
        vector_ac = Vector.from_points(point_a, point_c)

        vector_normal = vector_ab.cross(vector_ac)

        return cls(point_a, vector_normal)

    def contains(self, point, **kwargs):
        """Check if this plane contains a point."""
        vector_to_point = Vector.from_points(self.point, point)

        return are_perpendicular(vector_to_point, self.normal, **kwargs)

    def project(self, point):
        """Project a point onto this plane."""
        return project_point_plane(point, self)

    def distance_signed(self, point):
        """
        Compute the signed distance from a point to this plane.

        Parameters
        ----------
        self : Plane
        point : Point

        Returns
        -------
        float
            Signed distance from the point to plane.

        Examples
        --------
        >>> plane = Plane(Point([0, 0]), Vector([0, 0, 1]))

        >>> plane.distance_signed(Point([5, 2]))
        0.0

        >>> plane.distance_signed(Point([5, 2, 1]))
        1.0

        >>> plane.distance_signed(Point([5, 2, -4]))
        -4.0

        References
        ----------
        http://mathworld.wolfram.com/Point-PlaneDistance.html

        """
        vector_to_point = Vector.from_points(self.point, point)

        return self.normal.dot(vector_to_point)


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
    vector_projected = line.direction.project(vector_to_point)

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
    vector_projected = plane.normal.project(vector_to_plane)

    return point.add(vector_projected)
