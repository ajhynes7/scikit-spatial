import pytest

from skspatial.objects import LineSegment
from tests.unit.objects.test_line import LINES_MUST_BE_COPLANAR
from tests.unit.objects.test_line import LINES_MUST_HAVE_SAME_DIMENSION
from tests.unit.objects.test_line import LINES_MUST_NOT_BE_PARALLEL

INTERSECTION_MUST_BE_ON_BOTH_LINE_SEGMENTS = "The line segments do not intersect."


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
        (LineSegment([0, 0], [2, 0]), LineSegment([1, 1], [1, 2]), INTERSECTION_MUST_BE_ON_BOTH_LINE_SEGMENTS),
        (LineSegment([1, 1], [1, 2]), LineSegment([0, 0], [2, 0]), INTERSECTION_MUST_BE_ON_BOTH_LINE_SEGMENTS),
        (LineSegment([0, 0], [2, 0]), LineSegment([1, -1], [1, -2]), INTERSECTION_MUST_BE_ON_BOTH_LINE_SEGMENTS),
        (LineSegment([0, 0], [1, 0]), LineSegment([0, 1], [1, 1]), LINES_MUST_NOT_BE_PARALLEL),
        (LineSegment([0, 0, 0], [1, 0, 0]), LineSegment([0, 0], [1, 0]), LINES_MUST_HAVE_SAME_DIMENSION),
        (LineSegment([0, 0, 0], [1, 1, 1]), LineSegment([0, 1, 0], [-1, 1, 0]), LINES_MUST_BE_COPLANAR),
    ],
)
def test_intersect_line_segment_failure(segment_a, segment_b, message_expected):

    with pytest.raises(ValueError, match=message_expected):
        segment_a.intersect_line_segment(segment_b)
