import math

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from skspatial.objects import Line


@pytest.mark.parametrize(
    ("array_a", "array_b", "line_expected"),
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
    ("array_a", "array_b"),
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
    ("slope", "y_intercept", "line_expected"),
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
    ("line", "param", "array_expected"),
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


@pytest.mark.parametrize(
    ("array_point", "line", "dist_expected"),
    [
        ([0, 0], Line([0, 0], [1, 0]), 0),
        ([8, 7], Line([0, 0], [1, 0]), 7),
        ([20, -3], Line([0, 0], [1, 0]), 3),
        ([20, -3, 1], Line([0, 0, 0], [1, 0, 0]), math.sqrt(10)),
    ],
)
def test_distance_point(array_point, line, dist_expected):

    assert math.isclose(line.distance_point(array_point), dist_expected)


@pytest.mark.parametrize(
    ("line_a", "line_b", "dist_expected"),
    [
        # The lines intersect.
        (Line([10, 2], [1, 1]), Line([5, -3], [-1, 0]), 0),
        (Line([0, 0], [1, 1]), Line([1, 0], [1, 2]), 0),
        # The lines are parallel.
        (Line([0, 0], [1, 0]), Line([0, 0], [-1, 0]), 0),
        (Line([0, 0], [1, 0]), Line([0, 0], [1, 0]), 0),
        (Line([24, 0], [0, 1]), Line([3, 0], [0, -5]), 21),
        (Line([0, 0], [1, 1]), Line([1, 0], [1, 1]), math.sqrt(2) / 2),
        # The lines are skew.
        (Line([0, 0, 0], [0, 1, 0]), Line([1, 0, 0], [0, -4, 13]), 1),
    ],
)
def test_distance_line(line_a, line_b, dist_expected):

    assert math.isclose(line_a.distance_line(line_b), dist_expected)


@pytest.mark.parametrize(
    ("line_a", "line_b", "array_expected"),
    [
        (Line([0, 0], [1, 0]), Line([0, 0], [1, 1]), [0, 0]),
        (Line([0, 0], [1, 0]), Line([5, 5], [1, 1]), [0, 0]),
        (Line([0, 0], [1, 0]), Line([9, 0], [1, 1]), [9, 0]),
        (Line([0, 0], [1, 1]), Line([4, 0], [1, -1]), [2, 2]),
        (Line([0, 0, 0], [1, 1, 1]), Line([4, 4, 0], [-1, -1, 1]), [2, 2, 2]),
    ],
)
def test_intersect_line(line_a, line_b, array_expected):

    point_intersection = line_a.intersect_line(line_b)
    assert point_intersection.is_close(array_expected)


@pytest.mark.parametrize(
    ("line_a", "line_b"),
    [
        (Line([0, 0], [1, 0]), Line([0, 0], [1, 0])),
        (Line([0, 0], [1, 0]), Line([5, 5], [1, 0])),
        (Line([0, 0], [0, 1]), Line([0, 0], [0, 5])),
        (Line([0, 0], [1, 0]), Line([0, 0], [-1, 0])),
        (Line([0, 0], [1, 0]), Line([5, 5], [-1, 0])),
        (Line([0, 0, 0], [1, 1, 1]), Line([0, 1, 0], [-1, 0, 0])),
    ],
)
def test_intersect_line_failure(line_a, line_b):

    with pytest.raises(Exception):
        line_a.intersect_line(line_b)


@pytest.mark.parametrize(
    ("line", "points", "error_expected"),
    [
        (Line([0, 0], [1, 0]), [[0, 0], [10, 0]], 0),
        (Line([0, 0], [5, 0]), [[0, 0], [0, 1]], 1),
        (Line([0, 0], [1, 0]), [[0, 1], [0, -1]], 2),
        (Line([0, 0], [1, 0]), [[0, 5]], 25),
        (Line([0, 0], [1, 0]), [[0, 3], [0, -2]], 13),
        (Line([0, 0], [-20, 0]), [[1, 3], [2, -2], [3, -5]], 38),
    ],
)
def test_sum_squares(line, points, error_expected):

    error = line.sum_squares(points)
    assert math.isclose(error, error_expected)


@pytest.mark.parametrize(
    ("points", "line_expected"),
    [
        ([[0, 0], [1, 0]], Line([0.5, 0], [1, 0])),
        ([[1, 0], [0, 0]], Line([0.5, 0], [-1, 0])),
        ([[0, 0], [10, 0]], Line([5, 0], [1, 0])),
        ([[0, 0], [-10, 0]], Line([-5, 0], [-1, 0])),
        ([[0, 0], [1, 1], [2, 2]], Line([1, 1], [1, 1])),
        ([[2, 2], [1, 1], [0, 0]], Line([1, 1], [-1, -1])),
        ([[0, 0], [0, 1], [1, 0], [1, 1]], Line([0.5, 0.5], [1, 0])),
    ],
)
def test_best_fit(points, line_expected):

    line_fit = Line.best_fit(np.array(points))

    assert line_fit.is_close(line_expected)
    assert line_fit.point.is_close(line_expected.point)


@pytest.mark.parametrize(
    "points",
    [
        # There are fewer than two points.
        [[]],
        [[0, 0]],
        [[0, 0, 0]],
    ],
)
def test_best_fit_failure(points):

    with pytest.raises(Exception):
        Line.best_fit(points)
