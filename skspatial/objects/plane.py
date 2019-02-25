from dpcontracts import require, ensure

from .array import Point, Vector
from .base_line_plane import _BaseLinePlane


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
        lambda args: not args.point_a.is_collinear(args.point_b, args.point_c),
    )
    @ensure("The output must be a plane.", lambda _, result: isinstance(result, Plane))
    def from_points(cls, point_a, point_b, point_c):
        """Define a plane from three 3D points."""
        vector_ab = Vector.from_points(point_a, point_b)
        vector_ac = Vector.from_points(point_a, point_c)

        vector_normal = vector_ab.cross(vector_ac)

        return cls(point_a, vector_normal)

    @require("The input must be a point.", lambda args: isinstance(args.point, Point))
    def contains(self, point, **kwargs):
        """Check if this plane contains a point."""
        vector_to_point = Vector.from_points(self.point, point)

        return vector_to_point.is_perpendicular(self.normal, **kwargs)

    @require("The input must be a point.", lambda args: isinstance(args.point, Point))
    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    def project(self, point):
        """
        Project a point onto this plane.

        Parameters
        ----------
        point : Point

        Returns
        -------
        Point
            Projection of the point onto the plane.

        Examples
        --------
        >>> point = Point([10, 2, 5])
        >>> plane = Plane(Point([0, 0, 0]), Vector([0, 0, 1]))

        >>> plane.project(point)
        Point([10.  2.  0.])

        """
        # Vector from the point in space to the point on the plane.
        vector_to_plane = Vector.from_points(point, self.point)

        # Perpendicular vector from the point in space to the plane.
        vector_projected = self.normal.project(vector_to_plane)

        return point.add(vector_projected)

    def distance_signed(self, point):
        """
        Compute the signed distance from a point to this plane.

        Parameters
        ----------
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
