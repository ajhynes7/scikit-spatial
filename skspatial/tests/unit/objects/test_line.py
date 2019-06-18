import pytest
from numpy.testing import assert_array_equal

from skspatial.objects import Line


@pytest.mark.parametrize(
    "array_a, array_b, line_expected",
    [
        ([0, 0], [1, 0], Line([0, 0], [1, 0])),
        ([0, 0], [1, 1], Line([0, 0], [1, 1])),
        ([5, 2], [9, 2], Line([5, 2], [4, 0])),
        ([1, 1], [0, 0], Line([1, 1], [-1, -1])),
        ([0, 0], [5, 0], Line([0, 0], [5, 0])),
        ([0, 5, 9, 2], [4, 0, 0, 0], Line([0, 5, 9, 2], [4, -5, -9, -2])),
    ],
)
def test_from_points(array_a, array_b, line_expected):

    assert Line.from_points(array_a, array_b).is_close(line_expected)


@pytest.mark.parametrize(
    "array_a, array_b",
    [
        # The zero vector cannot be used.
        ([0, 0], [0, 0]),
        ([1, 2], [1, 2]),
        ([-1, 5], [-1, 5]),
        ([5, 2, 9, 3], [5, 2, 9, 3]),
    ],
)
def test_from_points_failure(array_a, array_b):

    with pytest.raises(Exception):
        Line.from_points(array_a, array_b)


@pytest.mark.parametrize(
    "slope, y_intercept, line_expected",
    [
        (0, 0, Line([0, 0], [1, 0])),
        (0, 1, Line([0, 1], [1, 0])),
        (0, 5, Line([0, 5], [1, 0])),
        (1, 0, Line([0, 0], [1, 1])),
        (-5, 0, Line([0, 0], [1, -5])),
        # The slope has the form rise / run.
        (-2 / 7, 0, Line([0, 0], [7, -2])),
        (3 / 4, 0, Line([0, 0], [4, 3])),
        (5 / 4, 0, Line([0, 0], [4, 5])),
    ],
)
def test_from_slope(slope, y_intercept, line_expected):

    assert Line.from_slope(slope, y_intercept).is_close(line_expected)


@pytest.mark.parametrize(
    "line, param, array_expected",
    [
        (Line([0, 0], [1, 0]), 0, [0, 0]),
        (Line([0, 0], [1, 0]), 1, [1, 0]),
        (Line([0, 0], [1, 0]), 5, [5, 0]),
        (Line([0, 0], [1, 0]), -8, [-8, 0]),
        (Line([5, 2, 1], [0, 2, 0]), 0, [5, 2, 1]),
        (Line([5, 2, 1], [0, 9, 0]), 1, [5, 11, 1]),
        (Line([5, 2, 1], [0, -9, 0]), 1, [5, -7, 1]),
        (Line([6, -3, 7, 8], [0, 8, 0, 0]), 1, [6, 5, 7, 8]),
        (Line([6, -3, 7, 8], [0, 8, 0, 0]), -2, [6, -19, 7, 8]),
    ],
)
def test_to_point(line, param, array_expected):

    point = line.to_point(t=param)

    assert_array_equal(point, array_expected)
