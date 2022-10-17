import pytest

from skspatial.objects import LineSegment
from skspatial.objects import Point
from tests.unit.objects.test_line import LINES_MUST_BE_COPLANAR
from tests.unit.objects.test_line import LINES_MUST_HAVE_SAME_DIMENSION
from tests.unit.objects.test_line import LINES_MUST_NOT_BE_PARALLEL

LINE_SEGMENTS_MUST_INTERSECT = "The line segments must intersect."


@pytest.mark.parametrize(("point_a", "point_b"), [([0, 0], [1, 0]), ([-1, -1], [2, -1]), ([1, 2, 3], [4, 5, 6])])
def test_initialize(point_a, point_b):

    segment = LineSegment(point_a, point_b)

    assert isinstance(segment.point_a, Point)
    assert isinstance(segment.point_b, Point)

    assert segment.point_a.is_close(point_a)
    assert segment.point_b.is_close(point_b)


@pytest.mark.parametrize(
    ("point_a", "point_b"),
    [([0, 0], [0, 0]), ([-1, -1], [-1, -1]), ([2, 2, 2], [2, 2, 2])],
)
def test_failure(point_a, point_b):

    with pytest.raises(ValueError, match="The endpoints must not be equal."):
        LineSegment(point_a, point_b)


@pytest.mark.parametrize(
    ("segment", "point", "bool_expected"),
    [
        (LineSegment([0, 0], [1, 0]), [0, 0], True),
        (LineSegment([0, 0], [1, 0]), [1, 0], True),
        (LineSegment([0, 0], [1, 0]), [0.5, 0], True),
        (LineSegment([0, 0], [1, 0]), [2, 0], False),
        (LineSegment([0, 0], [1, 0]), [-2, 0], False),
        (LineSegment([0, 0], [1, 0]), [0, 1], False),
        (LineSegment([0, 0], [1, 0]), [1, 1], False),
        (LineSegment([0, 0], [1, 0]), [0.5, 1], False),
        (LineSegment([2, 4], [3, 3]), [2, 4], True),
        (LineSegment([2, 4], [3, 3]), [3, 3], True),
        (LineSegment([2, 4], [3, 3]), [2.5, 3.5], True),
        (LineSegment([2, 4], [3, 3]), [3, 4], False),
    ],
)
def test_contains_point(segment, point, bool_expected):

    assert segment.contains_point(point) == bool_expected


@pytest.mark.parametrize(
    ("segment", "point", "bool_expected"),
    [
        (LineSegment([0, 0], [1, 0]), [1e-3, 0], True),
        (LineSegment([0, 0], [1, 0]), [-1e-3, 0], True),
        (LineSegment([0, 0], [1, 0]), [1, 1e-3], True),
        (LineSegment([0, 0], [1, 0]), [1, -1e-3], True),
        (LineSegment([0, 0], [2, 0]), [1, 1e-3], True),
        (LineSegment([0, 0], [2, 0]), [1, -1e-3], True),
    ],
)
def test_contains_point_with_tolerance(segment, point, bool_expected):

    assert segment.contains_point(point, abs_tol=1e-1) == bool_expected


@pytest.mark.parametrize(
    ("segment_a", "segment_b", "array_expected"),
    [
        (LineSegment([0, 0], [1, 0]), LineSegment([0, 0], [0, 1]), [0, 0]),
        (LineSegment([-1, 0], [1, 0]), LineSegment([0, -1], [0, 1]), [0, 0]),
        (LineSegment([0, 0], [2, 0]), LineSegment([1, 0], [1, 1]), [1, 0]),
    ],
)
def test_intersect_line_segment(segment_a, segment_b, array_expected):

    point_intersection = segment_a.intersect_line_segment(segment_b)
    assert point_intersection.is_close(array_expected)


@pytest.mark.parametrize(
    ("segment_a", "segment_b", "message_expected"),
    [
        (LineSegment([0, 0], [2, 0]), LineSegment([1, 1], [1, 2]), LINE_SEGMENTS_MUST_INTERSECT),
        (LineSegment([1, 1], [1, 2]), LineSegment([0, 0], [2, 0]), LINE_SEGMENTS_MUST_INTERSECT),
        (LineSegment([0, 0], [2, 0]), LineSegment([1, -1], [1, -2]), LINE_SEGMENTS_MUST_INTERSECT),
        (LineSegment([0, 0], [1, 0]), LineSegment([0, 1], [1, 1]), LINES_MUST_NOT_BE_PARALLEL),
        (LineSegment([0, 0, 0], [1, 0, 0]), LineSegment([0, 0], [1, 0]), LINES_MUST_HAVE_SAME_DIMENSION),
        (LineSegment([0, 0, 0], [1, 1, 1]), LineSegment([0, 1, 0], [-1, 1, 0]), LINES_MUST_BE_COPLANAR),
    ],
)
def test_intersect_line_segment_failure(segment_a, segment_b, message_expected):

    with pytest.raises(ValueError, match=message_expected):
        segment_a.intersect_line_segment(segment_b)
