from dpcontracts import require, ensure, types

from .base_line_plane import _BaseLinePlane
from .point import Point
from .vector import Vector


class _Line(_BaseLinePlane):
    """Private parent class for Line."""
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
        point_a : Point
            Input point A.
        point_b : Point
            Input point B.

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


    @types(point=Point)
    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    @ensure("The output must be on the line.", lambda args, result: args.self.contains_point(result))
    def project_point(self, point):
        """
        Project a point onto this line.

        Parameters
        ----------
        point : Point
            Input point.

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

    @types(vector=Vector)
    @ensure("The output must be a vector.", lambda _, result: isinstance(result, Point))
    @ensure("The output must be parallel to the line.", lambda args, result: args.self.direction.is_parallel(result))
    def project_vector(self, vector):

        return self.direction.project(vector)

    @types(point=Point)
    @ensure("The output must be zero or greater.", lambda _, result: result >= 0)
    def distance_point(self, point):

        point_projected = self.project_point(point)

        return point.distance(point_projected)

    @types(other=_Line)
    @ensure("The output must be zero or greater.", lambda _, result: result >= 0)
    def distance_line(self, other):
        """
        Return the shortest distance from an other line to self.

        Parameters
        ----------
        other : Line
            Input line.

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
        if self.is_parallel(other):
            # The lines are parallel.
            # The distance between the lines is the distance from line point B to line A.
            distance = self.distance(other.point)

        elif self.is_coplanar(other):
            # The lines must intersect, since they are coplanar and not parallel.
            distance = 0.0

        else:
            # The lines are skew.
            vector_ab = Vector.from_points(self.point, other.point)
            vector_cross = self.direction.cross(other.direction)

            distance = abs(vector_ab.dot(vector_cross)) / vector_cross.magnitude

        return distance
