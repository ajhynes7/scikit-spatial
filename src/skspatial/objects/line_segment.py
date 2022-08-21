"""Module for the LineSegment class."""
from __future__ import annotations

import math

from skspatial.objects.line import Line
from skspatial.objects.point import Point
from skspatial.objects.vector import Vector
from skspatial.typing import array_like


class LineSegment:
    """
    A line segment in space.

    The line segment is defined by two points.

    Parameters
    ----------
    point_a, point_b : array_like
        The two ends of the line segment.

    Attributes
    ----------
    point_a, point_b : Point
        The two ends of the line segment.

    """

    def __init__(self, point_a: array_like, point_b: array_like):

        self.point_a = point_a
        self.point_b = point_b

    def contains_point(self, point: array_like, **kwargs) -> bool:
        """
        Check if a point is on the line segment.

        Parameters
        ----------
        point : array_like

        Returns
        -------
        bool
            True if the point is on the line segment; false otherwise.

        Examples
        --------
        >>> from skspatial.objects import LineSegment

        >>> segment = LineSegment([0, 0], [1, 0])

        >>> segment.contains_point([0, 0])
        True
        >>> segment.contains_point([0.5, 0])
        True
        >>> segment.contains_point([2, 0])
        False
        >>> segment.contains_point([0, 1])
        False

        """
        vector_a = Vector.from_points(point, self.point_a)
        vector_b = Vector.from_points(point, self.point_b)

        if vector_a.is_zero(**kwargs) or vector_b.is_zero(**kwargs):
            return True

        similarity = vector_a.cosine_similarity(vector_b)

        return math.isclose(similarity, -1, **kwargs)

    def intersect_line_segment(self, other: LineSegment) -> Point:
        """
        Intersect the line segment with another.

        Parameters
        ----------
        other : LineSegment

        Returns
        -------
        Point
            The intersection point of the two line segments.

        Raises
        ------
        ValueError
            If the line segments do not intersect.

        Examples
        --------
        >>> from skspatial.objects import LineSegment

        >>> segment_a = LineSegment([-1, 0], [1, 0])
        >>> segment_b = LineSegment([0, -1], [0, 1])

        >>> segment_a.intersect_line_segment(segment_b)
        Point([0., 0.])

        >>> segment_b = LineSegment([0, 1], [0, 2])

        >>> segment_a.intersect_line_segment(segment_b)
        Traceback (most recent call last):
        ...
        ValueError: The line segments do not intersect.

        """
        line_a = Line.from_points(self.point_a, self.point_b)
        line_b = Line.from_points(other.point_a, other.point_b)

        point_intersection = line_a.intersect_line(line_b)

        point_on_segment_a = self.contains_point(point_intersection)
        point_on_segment_b = other.contains_point(point_intersection)

        if not (point_on_segment_a and point_on_segment_b):
            raise ValueError("The line segments do not intersect.")

        return point_intersection
