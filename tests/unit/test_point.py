import pytest

from skspatial.objects import Point


@pytest.mark.parametrize(
    "array_a, array_b, array_c, bool_expected",
    [
        ([0], [0], [0], True),
        ([1], [1], [1], True),
        ([0, 0], [0, 1], [0, 2], True),
        ([0, 1], [0, 0], [0, 2], True),
        ([0, 0], [-1, 0], [10, 0], True),
        ([0, 0], [0, 1], [1, 2], False),
        ([0, 0, 0], [1, 1, 1], [2, 2, 2], True),
        ([0, 0, 0], [1, 1, 1], [2, 2, 2.5], False),
    ],
)
def test_is_collinear(array_a, array_b, array_c, bool_expected):
    """Test checking if three points are collinear."""
    point_a = Point(array_a)
    point_b = Point(array_b)
    point_c = Point(array_c)

    assert point_a.is_collinear(point_b, point_c) == bool_expected
