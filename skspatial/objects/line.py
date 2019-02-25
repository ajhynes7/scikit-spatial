from dpcontracts import require, ensure, types

from .array import Point, Vector
from .base_classes import _BaseLinePlane


class Line(_BaseLinePlane):
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
