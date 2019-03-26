import numpy as np
from dpcontracts import require, ensure

from skspatial.objects.base_line_plane import _BaseLinePlane
from skspatial.objects.point import Point, Points
from skspatial.objects.vector import Vector


class Line(_BaseLinePlane):
    """
    Line in space.

    The line is defined by a point and a direction vector.

    Parameters
    ----------
    point : array_like, optional
        Point on the line.
    direction : array_like, optional
        Direction vector of the line.

    Attributes
    ----------
    point : Point
        Point on the line.
    direction : Vector
        Unit direction vector.
    vector : Vector
        Same as the direction.

    Examples
    --------
    >>> from skspatial.objects import Line

    >>> line = Line(point=[0, 0], direction=[3, 0])

    >>> line
    Line(point=Point([0., 0.]), direction=Vector([3., 0.]))

    >>> line.direction
    Vector([3., 0.])

    The direction can also be accessed with the 'vector' attribute.
    >>> line.vector
    Vector([3., 0.])

    """

    def __init__(self, point, direction):

        super().__init__(point, direction)

        self.direction = self.vector

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
        >>> from skspatial.objects import Line

        >>> Line.from_points([0, 0], [1, 0])
        Line(point=Point([0., 0.]), direction=Vector([1., 0.]))

        The order of the points affects the line point and direction vector.

        >>> Line.from_points([1, 0], [0, 0])
        Line(point=Point([1., 0.]), direction=Vector([-1.,  0.]))

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
            Additional keywords passed to `np.linalg.matrix_rank`.

        Returns
        -------
        bool
            True if the line is coplanar; false otherwise.

        Examples
        --------
        >>> from skspatial.objects import Line

        >>> line_a = Line(point=[0, 0, 0], direction=[1, 0, 0])
        >>> line_b = Line([-5, 3, 0], [7, 1, 0])
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
        point_1 = self.point
        point_2 = self.to_point()
        point_3 = other.point
        point_4 = other.to_point()

        points = Points([point_1, point_2, point_3, point_4])

        return points.are_coplanar(**kwargs)

    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
    def to_point(self, t=1):
        """
        Return a point along the line using a parameter t.

        Computed as line.point + t * line.direction.

        """
        vector_along_line = t * self.direction

        return self.point.add(vector_along_line)

    @ensure("The output must be a point.", lambda _, result: isinstance(result, Point))
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
        >>> from skspatial.objects import Line

        >>> line = Line(point=[0, 0], direction=[8, 0])
        >>> line.project_point([5, 5])
        Point([5., 0.])

        """
        # Vector from the point on the line to the point in space.
        vector_to_point = Vector.from_points(self.point, point)

        # Project the vector onto the line.
        vector_projected = self.direction.project(vector_to_point)

        # Add the projected vector to the point on the line.
        return self.point.add(vector_projected)

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
            vector_perpendicular = self.direction.cross(other.direction)

            distance = abs(vector_ab.dot(vector_perpendicular)) / vector_perpendicular.norm()

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
        Point([5., 0.])

        >>> line_b = Line([0, 1], [2, 0])
        >>> line_a.intersect_line(line_b)
        Traceback (most recent call last):
        ...
        dpcontracts.PreconditionError: The lines must not be parallel.

        >>> line_a = Line([1, 2, 3], [-4, 1, 1])
        >>> line_b = Line([4, 5, 6], [3, 1, 5])

        >>> line_a.intersect_line(line_b)
        Traceback (most recent call last):
        ...
        dpcontracts.PreconditionError: The lines must be coplanar.

        >>> line_a = Line([0, 0, 0], [1, 1, 1])
        >>> line_b = Line([5, 5, 0], [0, 0, -8])

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
        denom = vector_perpendicular.norm() ** 2

        # Vector along line A to the intersection point.
        vector_a_scaled = num / denom * self.direction

        return self.point.add(vector_a_scaled)

    @classmethod
    @require("The points must not be concurrent.", lambda args: not Points(args.points).are_concurrent())
    @ensure("The output must be a line.", lambda _, result: isinstance(result, Line))
    def best_fit(cls, points):
        """
        Return the line of best fit for a set of points.

        Parameters
        ----------
        points : {array_like, sequence}
             Input points.

        Returns
        -------
        Line
            The line of best fit.

        Examples
        --------
        >>> from skspatial.objects import Line

        >>> points = ([1, 0], [2, 0], [3, 0])
        >>> line = Line.best_fit(points)

        >>> line.point
        Point([2., 0.])

        >>> line.direction
        Vector([1., 0.])

        """
        points_centered, centroid = Points(points).mean_center()

        _, _, vh = np.linalg.svd(points_centered)
        direction = Vector(vh[0, :])

        return cls(centroid, direction)

    @require("The points must be all finite.", lambda args: np.isfinite(args.points).all())
    @ensure(
        "There must be one coordinate for each input point.",
        lambda args, result: result.size == Points(args.points).shape[0],
    )
    @ensure("The output must be a 1D array.", lambda _, result: result.ndim == 1)
    @ensure("The coordinates must be all finite.", lambda _, result: np.isfinite(result).all())
    def transform_points(self, points):
        """
        Transform points to a one-dimensional coordinate system defined by a line.

        The point on the line acts as the origin of the coordinate system.

        The line is analagous to an x-axis. The output coordinates represent the
        x-values of points on this line.

        Parameters
        ----------
        points : ndarray
            (n, d) array of n points with dimension d.

        Returns
        -------
        ndarray
            One-dimensional coordinates.

        Examples
        --------
        >>> from skspatial.objects import Line

        >>> line = Line(point=[0, 0], direction=[1, 0])
        >>> points = [[10, 2, 0], [3, 4, 0], [-5, 5, 0]]

        >>> line.transform_points(points)
        array([10.,  3., -5.])

        """
        points = Points(points)
        dim_points = points.get_dimension()

        point_line = self.point.set_dimension(dim_points)
        direction_line = self.direction.set_dimension(dim_points)

        vectors_to_points = points - point_line

        return np.apply_along_axis(np.dot, 1, vectors_to_points, direction_line)
