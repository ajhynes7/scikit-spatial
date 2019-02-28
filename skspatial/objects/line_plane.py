"""Classes for the Line and Plane spatial objects."""

from dpcontracts import require, ensure, types
from .array import Point, Vector


class _BaseLinePlane:
    """Private parent class for Line and Plane."""

    @types(point=Point, vector=Vector)
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

    @types(point=Point)
    @ensure("The output must zero or greater.", lambda _, result: result >= 0)
    def distance(self, point):
        """Compute the distance from a point to this object."""
        point_projected = self.project(point)

        return point.distance(point_projected)


class _Line(_BaseLinePlane):
    """Private parent class for Line."""
    def __init__(self, point, vector):
        super().__init__(point, vector)


class _Plane(_BaseLinePlane):
    """Private parent class for Plane."""
    def __init__(self, point, vector):
        super().__init__(point, vector)


class Line(_Line):
    def __init__(self, point, vector):

        super().__init__(point, vector)

        self.direction = self.vector

    def __repr__(self):

        return f"Line(point={self.point}, direction={self.direction})"

    @classmethod
    @types(point_a=Point, point_b=Point)
    @require("The points must be different.", lambda args: args.point_a != args.point_b)
    @ensure("The output must be a line.", lambda _, result: isinstance(result, Line))
    def from_points(cls, point_a, point_b):
        """
        Instantiate a plane from three points.

        Parameters
        ----------
        point_a, point_b : Point
            Input points.

        Returns
        -------
        Line
            Line containing the two input points.

        Examples
        --------
        >>> Line.from_points(Point([0, 0]), Point([1, 0]))
        Line(point=Point([0. 0. 0.]), direction=Vector([1. 0. 0.]))

        The order of the points affects the line point and direction vector.

        >>> Line.from_points(Point([1, 0]), Point([0, 0]))
        Line(point=Point([1. 0. 0.]), direction=Vector([-1.  0.  0.]))

        """
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

    @types(point=Point)
    def contains(self, point, **kwargs):
        """Check if this line contains a point."""
        vector_to_point = Vector.from_points(self.point, point)

        return vector_to_point.is_parallel(self.direction, **kwargs)

    @types(point=Point)
    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    def project(self, point):
        """
        Project a point onto this line.

        Parameters
        ----------
        point : Point

        Returns
        -------
        Point
            Projection of the point onto the line.

        Examples
        --------
        >>> point = Point([5, 5])
        >>> line = Line(Point([0, 0]), Vector([1, 0]))

        >>> line.project(point)
        Point([5. 0. 0.])

        """
        # Vector from the point on the line to the point in space.
        vector_to_point = Vector.from_points(self.point, point)

        # Project the vector onto the line.
        vector_projected = self.direction.project(vector_to_point)

        # Add the projected vector to the point on the line.
        return self.point.add(vector_projected)

    @types(other=_Line)
    def is_parallel(self, other, **kwargs):
        """
        Check if the line is parallel to another.

        Two lines are parallel iff their direction vectors are parallel.

        Parameters
        ----------
        other : Line
            Input line.
        kwargs : dict, optional
            Additional keywords passed to `np.isclose`.

        Returns
        -------
        bool
            True if the line is coplanar; false otherwise.

        Examples
        --------
        >>> line_a = Line(Point([0, 0]), Vector([1, 0]))
        >>> line_b = Line(Point([5, 10]), Vector([3, 0]))
        >>> line_c = Line(Point([0, 0]), Vector([0, 0, 1]))

        >>> line_a.is_parallel(line_b)
        True

        >>> line_b.is_parallel(line_c)
        False

        >>> line_a.is_parallel(line_c)
        False

        """
        return self.direction.is_parallel(other.direction)


    @types(other=_Line)
    def is_coplanar(self, other, **kwargs):
        """
        Check if the line is coplanar with another.

        Parameters
        ----------
        other : Line
            Input line.
        kwargs : dict, optional
            Additional keywords passed to `np.isclose`.

        Returns
        -------
        bool
            True if the line is coplanar; false otherwise.

        Examples
        --------
        >>> line_a = Line(Point([0, 0]), Vector([1, 0]))
        >>> line_b = Line(Point([-5, 3]), Vector([7, 1]))
        >>> line_c = Line(Point([0, 0]), Vector([0, 0, 1]))

        >>> line_a.is_coplanar(line_b)
        True

        >>> line_a.is_coplanar(line_c)
        True

        >>> line_b.is_coplanar(line_c)
        False

        References
        ----------
        http://mathworld.wolfram.com/Coplanar.html

        """
        vector_ab = Vector.from_points(self.point, other.point)
        vector_cross = self.direction.cross(other.direction)

        return vector_cross.is_perpendicular(vector_ab, **kwargs)


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
        point_a, point_b, point_c : Point
            Input points.

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
    def contains(self, point, **kwargs):
        """Check if this plane contains a point."""
        vector_to_point = Vector.from_points(self.point, point)

        return vector_to_point.is_perpendicular(self.normal, **kwargs)

    @types(point=Point)
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

    @types(point=Point)
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
