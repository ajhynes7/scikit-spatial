import numpy as np
from dpcontracts import require, ensure, types

from skspatial.transformation import mean_center
from .base_line_plane import _BaseLinePlane
from .point import Point
from .vector import Vector


class Line(_BaseLinePlane):
    """Line in space."""

    def __init__(self, point=[0, 0], vector=[1, 0]):

        super().__init__(point, vector)

        self.direction = self.vector

    def __repr__(self):

        repr_point = np.array_repr(self.point)
        repr_vector = np.array_repr(self.vector)

        return f"Line(point={repr_point}, direction={repr_vector})"

    @classmethod
    @ensure("The output must be a line.", lambda _, result: isinstance(result, Line))
    def from_points(cls, point_a, point_b):
        """
        Instantiate a line from two points.

        Parameters
        ----------
        point_a : array_like
            Input point A.
        point_b : array_like
            Input point B.

        Returns
        -------
        Line
            Line containing the two input points.

        Examples
        --------
        >>> Line.from_points([0, 0], [1, 0])
        Line(point=Point([0., 0., 0.]), direction=Vector([1., 0., 0.]))

        The order of the points affects the line point and direction vector.

        >>> Line.from_points([1, 0], [0, 0])
        Line(point=Point([1., 0., 0.]), direction=Vector([-1.,  0.,  0.]))

        """
        vector_ab = Vector.from_points(point_a, point_b)

        return cls(point_a, vector_ab)

    @require("The input must have the same type as the object.", lambda args: isinstance(args.other, type(args.self)))
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
        >>> line_a = Line(point=[0, 0], vector=[1, 0])
        >>> line_b = Line([-5, 3], [7, 1])
        >>> line_c = Line([0, 0, 0], [0, 0, 1])

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

    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    def to_point(self, t=1):
        """
        Return a point along the line using a parameter t.

        Computed as line.point + t * line.direction.

        """
        vector_along_line = t * self.direction

        return self.point + vector_along_line

    def contains_point(self, point, **kwargs):
        """Check if this line contains a point."""
        vector_to_point = Vector.from_points(self.point, point)

        return vector_to_point.is_parallel(self.direction, **kwargs)

    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    @ensure("The output must be on the line.", lambda args, result: args.self.contains_point(result))
    def project_point(self, point):
        """
        Project a point onto this line.

        Parameters
        ----------
        point : array_like
            Input point.

        Returns
        -------
        Point
            Projection of the point onto the line.

        Examples
        --------
        >>> line = Line(point=[0, 0], vector=[1, 0])

        >>> line.project_point([5, 5])
        Point([5., 0., 0.])

        """
        # Vector from the point on the line to the point in space.
        vector_to_point = Vector.from_points(self.point, point)

        # Project the vector onto the line.
        vector_projected = self.direction.project(vector_to_point)

        # Add the projected vector to the point on the line.
        return Point(self.point + vector_projected)

    @ensure("The output must be a vector.", lambda _, result: isinstance(result, Vector))
    @ensure("The output must be parallel to the line.", lambda args, result: args.self.direction.is_parallel(result))
    def project_vector(self, vector):
        """Project a vector onto the line."""
        return self.direction.project(vector)

    @require("The input must have the same type as the object.", lambda args: isinstance(args.other, type(args.self)))
    @ensure("The output must be zero or greater.", lambda _, result: result >= 0)
    @ensure("The output must be a numpy scalar.", lambda _, result: isinstance(result, np.number))
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
        >>> from skspatial.objects import Line

        >>> line_a = Line([0, 0], [1, 0])
        >>> line_b = Line([0, 1], [1, 0])
        >>> line_c = Line([0, 1], [1, 1])

        The lines are parallel.
        >>> line_a.distance_line(line_b)
        1.0

        The lines are coplanar and not parallel.
        >>> line_a.distance_line(line_c)
        0.0

        The lines are skew.
        >>> line_a = Line([0, 0, 0], [1, 0, 0])
        >>> line_b = Line([0, 5, 0], [0, 0, 1])
        >>> line_a.distance_line(line_b)
        5.0

        References
        ----------
        http://mathworld.wolfram.com/Line-LineDistance.html

        """
        if self.direction.is_parallel(other.direction):
            # The lines are parallel.
            # The distance between the lines is the distance from line point B to line A.
            distance = self.distance_point(other.point)

        elif self.is_coplanar(other):
            # The lines must intersect, since they are coplanar and not parallel.
            distance = np.float64(0)

        else:
            # The lines are skew.
            vector_ab = Vector.from_points(self.point, other.point)
            vector_cross = self.direction.cross(other.direction)

            distance = abs(vector_ab.dot(vector_cross)) / vector_cross.magnitude

        return distance

    @require("The input must have the same type as the object.", lambda args: isinstance(args.other, type(args.self)))
    @require("The lines must be coplanar.", lambda args: args.self.is_coplanar(args.other))
    @require("The lines must not be parallel.", lambda args: not args.self.direction.is_parallel(args.other.direction))
    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    @ensure(
        "The point must be on both lines.",
        lambda args, result: args.self.contains_point(result) and args.other.contains_point(result),
    )
    def intersect_line(self, other):
        """
        Return the intersection of a line with self.

        The lines must be coplanar and not parallel.

        Parameters
        ----------
        other : Line
            Input line.

        Returns
        -------
        Point
            The point at the intersection.

        Examples
        --------
        >>> from skspatial.objects import Line

        >>> line_a = Line([0, 0], [1, 0])
        >>> line_b = Line([5, 5], [0, 1])

        >>> line_a.intersect_line(line_b)
        Point([5., 0., 0.])

        >>> line_b = Line(Point([0, 1]), Vector([2, 0]))
        >>> line_a.intersect_line(line_b)
        Traceback (most recent call last):
        ...
        dpcontracts.PreconditionError: The lines must not be parallel.

        >>> line_a = Line(Point([1, 2, 3]), Vector([-4, 1, 1]))
        >>> line_b = Line(Point([4, 5, 6]), Vector([3, 1, 5]))

        >>> line_a.intersect_line(line_b)
        Traceback (most recent call last):
        ...
        dpcontracts.PreconditionError: The lines must be coplanar.

        >>> line_a = Line(Point([0, 0, 0]), Vector([1, 1, 1]))
        >>> line_b = Line(Point([5, 5, 0]), Vector([0, 0, -8]))

        >>> line_a.intersect_line(line_b)
        Point([5., 5., 5.])

        References
        ----------
        http://mathworld.wolfram.com/Line-LineIntersection.html

        """
        # Vector from line A to line B.
        vector_ab = Vector.from_points(self.point, other.point)

        # Vector perpendicular to both lines.
        vector_perpendicular = self.direction.cross(other.direction)

        num = vector_ab.cross(other.direction).dot(vector_perpendicular)
        denom = vector_perpendicular.magnitude ** 2

        # Vector along line A to the intersection point.
        vector_a_scaled = num / denom * self.direction

        return self.point + vector_a_scaled
