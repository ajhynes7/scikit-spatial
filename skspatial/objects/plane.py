import numpy as np
from dpcontracts import require, ensure, types

from .base_line_plane import _BaseLinePlane, _Line, _Plane
from .point import Point
from .vector import Vector


class Plane(_Plane):
    def __init__(self, point, vector):

        super().__init__(point, vector)

        self.normal = self.vector

    def __repr__(self):

        return f"Plane(point={self.point}, normal={self.normal})"

    @classmethod
    @types(point_a=Point, point_b=Point, point_c=Point)
    @require(
        "The points must not be collinear.",
        lambda args: not args.point_a.is_collinear(args.point_b, args.point_c),
    )
    @ensure("The output must be a plane.", lambda _, result: isinstance(result, Plane))
    def from_points(cls, point_a, point_b, point_c):
        """
        Instantiate a plane from three points.

        Parameters
        ----------
        point_a : Point
            Input point A.
        point_b : Point
            Input point B.
        point_c : Point
            Input point C.

        Returns
        -------
        Plane
            Plane containing the three input points.

        Examples
        --------
        >>> Plane.from_points(Point([0, 0]), Point([1, 0]), Point([3, 3]))
        Plane(point=Point([0. 0. 0.]), normal=Vector([0. 0. 1.]))

        The order of the points affects the direction of the normal vector.

        >>> Plane.from_points(Point([0, 0]), Point([3, 3]), Point([1, 0]))
        Plane(point=Point([0. 0. 0.]), normal=Vector([ 0.  0. -1.]))

        """
        vector_ab = Vector.from_points(point_a, point_b)
        vector_ac = Vector.from_points(point_a, point_c)

        vector_normal = vector_ab.cross(vector_ac)

        return cls(point_a, vector_normal)

    @types(point=Point)
    def contains_point(self, point, **kwargs):
        """Check if this plane contains a point."""
        vector_to_point = Vector.from_points(self.point, point)

        return vector_to_point.is_perpendicular(self.normal, **kwargs)

    @types(point=Point)
    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    def project_point(self, point):
        """
        Project a point onto self.

        Parameters
        ----------
        point : Point
            Input point.

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

    @types(point=Point)
    @ensure("The output must be a float.", lambda _, result: isinstance(result, float))
    def distance_point(self, point):
        """
        Return the signed distance from a point to self.

        Parameters
        ----------
        point : Point
            Input point.

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

    @types(other=_Plane)
    @require("The planes must not be parallel.", lambda args: not args.self.normal.is_parallel(args.other.normal))
    @ensure("The output must be a line.", lambda _, result: isinstance(result, Line))
    @ensure(
        "The point on the line must be on both planes.",
        lambda args, result: args.self.contains_point(result.point) and args.other.contains_point(result.point),
    )
    def intersect_plane(self, other):
        """
        Return the intersection of two planes.

        The planes must not be parallel.

        Parameters
        ----------
        self : Plane
            Input plane A.
        other : Plane
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
        array_normals_stacked = np.vstack((self.normal.array, other.normal.array))

        # Construct a matrix for a linear system.
        array_00 = 2 * np.eye(3)
        array_01 = array_normals_stacked.T
        array_10 = array_normals_stacked
        array_11 = np.zeros((2, 2))
        matrix = np.block([[array_00, array_01], [array_10, array_11]])

        dot_a = np.dot(self.point.array, self.normal.array)
        dot_b = np.dot(other.point.array, other.normal.array)
        array_y = np.array([0, 0, 0, dot_a, dot_b])

        # Solve the linear system.
        solution = np.linalg.solve(matrix, array_y)

        point_line = Point(solution[:3])
        direction_line = self.normal.cross(other.normal)

        return _Line(point_line, direction_line)
