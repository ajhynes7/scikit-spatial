
LineSegment
-----------

A :class:`~skspatial.objects.LineSegment` object is defined by two points, which are the endpoints of the segment.

>>> from skspatial.objects import LineSegment

>>> segment_1 = LineSegment([0, 0], [1, 0])

>>> segment_1
LineSegment(point_a=Point([0, 0]), point_b=Point([1, 0]))


The segment contains the two endpoints, but not points beyond the endpoints on the same line, nor points off the line.

>>> segment_1.contains_point([0, 0])
True
>>> segment_1.contains_point([0.5, 0])
True
>>> segment_1.contains_point([1, 0])
True

>>> segment_1.contains_point([0, 2])
False
>>> segment_1.contains_point([0, 1])
False


The intersection of two segments can be found. An exception will be raised if the segments do not intersect.

>>> segment_2 = LineSegment([0.5, 1], [0.5, -1])

>>> segment_1.intersect_line_segment(segment_2)
Point([0.5, 0. ])
