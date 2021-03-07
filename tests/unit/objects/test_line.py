import math

import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal
from numpy.testing import assert_array_equal

from skspatial.objects import Line
from skspatial.objects import Plane
from skspatial.objects import Point

INPUT_MUST_ALSO_BE_LINE = "The input must also be a line."
POINTS_MUST_NOT_BE_CONCURRENT = "The points must not be concurrent."
ARRAY_MUST_NOT_BE_EMPTY = "The array must not be empty."
LINES_MUST_HAVE_SAME_DIMENSION = "The lines must have the same dimension."
DIMENSION_MUST_NOT_BE_MORE_THAN_3D = "The line dimension cannot be greater than 3."
LINES_MUST_BE_COPLANAR = "The lines must be coplanar."
LINES_MUST_NOT_BE_PARALLEL = "The lines must not be parallel."


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
        ([0, 0], [0, 0]),
        ([1, 2], [1, 2]),
        ([-1, 5], [-1, 5]),
        ([5, 2, 9, 3], [5, 2, 9, 3]),
    ],
)
def test_from_points_failure(array_a, array_b):

    message_expected = "The vector must not be the zero vector."

    with pytest.raises(ValueError, match=message_expected):
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
    ("line_a", "line_b", "bool_expected"),
    [
        (Line([0, 0], [1, 1]), Line([0, 0], [0, 1]), True),
        (Line([-6, 7], [5, 90]), Line([1, 4], [-4, 5]), True),
        (Line([0, 0, 1], [1, 1, 0]), Line([0, 0, 0], [0, 1, 0]), False),
        (Line([0, 0, 1], [1, 1, 0]), Line([0, 0, 1], [0, 1, 0]), True),
        (Line([0, 0, 1], [1, 0, 1]), Line([0, 0, 1], [2, 0, 2]), True),
    ],
)
def test_is_coplanar(line_a, line_b, bool_expected):

    assert line_a.is_coplanar(line_b) == bool_expected


@pytest.mark.parametrize(
    ("line_a", "line_b"),
    [
        (Line([0, 0], [1, 1]), Point([0, 0])),
        (Line([0, 0, 0], [1, 1, 0]), Plane([0, 0, 0], [0, 0, 1])),
    ],
)
def test_is_coplanar_failure(line_a, line_b):

    message_expected = "The input must also be a line."

    with pytest.raises(TypeError, match=message_expected):
        line_a.is_coplanar(line_b)


@pytest.mark.parametrize(
    ("point", "point_line", "vector_line", "point_expected", "dist_expected"),
    [
        ([0, 5], [0, 0], [0, 1], [0, 5], 0),
        ([0, 5], [0, 0], [0, 100], [0, 5], 0),
        ([1, 5], [0, 0], [0, 100], [0, 5], 1),
        ([0, 1], [0, 0], [1, 1], [0.5, 0.5], math.sqrt(2) / 2),
        ([1, 0], [0, 0], [1, 1], [0.5, 0.5], math.sqrt(2) / 2),
        ([0, 2], [0, 0], [1, 1], [1, 1], math.sqrt(2)),
        ([-15, 5], [0, 0], [0, 100], [0, 5], 15),
        ([50, 10], [1, -5], [0, 3], [1, 10], 49),
    ],
)
def test_project_point(point, point_line, vector_line, point_expected, dist_expected):

    line = Line(point_line, vector_line)

    point_projected = line.project_point(point)
    distance = line.distance_point(point)

    assert point_projected.is_close(point_expected)
    assert math.isclose(distance, dist_expected)


@pytest.mark.parametrize(
    ("line", "vector", "vector_expected"),
    [
        (Line([0, 0], [1, 0]), [1, 1], [1, 0]),
        (Line([-56, 72], [1, 0]), [1, 1], [1, 0]),
        (Line([-56, 72], [200, 0]), [5, 9], [5, 0]),
        (Line([-56, 72], [200, 0]), [-5, 9], [-5, 0]),
    ],
)
def test_project_vector(line, vector, vector_expected):

    vector_projected = line.project_vector(vector)
    assert vector_projected.is_close(vector_expected)


@pytest.mark.parametrize(
    ("line", "point", "value_expected"),
    [
        (Line([0, 0], [0, 1]), [0, 0], 0),
        (Line([0, 0], [0, 1]), [1, 0], 1),
        (Line([0, 0], [0, 1]), [1, 1], 1),
        (Line([0, 0], [0, 1]), [1, 10], 1),
        (Line([0, 0], [0, 1]), [1, -10], 1),
        (Line([0, 0], [0, 1]), [-1, 0], -1),
        (Line([0, 0], [0, 1]), [-1, 1], -1),
        (Line([0, 0], [0, 1]), [-1, -25], -1),
    ],
)
def test_side_point(line, point, value_expected):

    assert line.side_point(point) == value_expected


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
    ("line_a", "line_b", "message_expected"),
    [
        (
            Line([0, 0], [1, 0]),
            Line([0, 0, 0], [1, 0, 0]),
            LINES_MUST_HAVE_SAME_DIMENSION,
        ),
        (Line([0], [1]), Line([0, 0], [0, 1]), LINES_MUST_HAVE_SAME_DIMENSION),
        (
            Line([0, 0], [1, 0]),
            Line(4 * [0], [1, 0, 0, 0]),
            LINES_MUST_HAVE_SAME_DIMENSION,
        ),
        (
            Line(4 * [0], [1, 0, 0, 0]),
            Line(4 * [0], [1, 0, 0, 0]),
            DIMENSION_MUST_NOT_BE_MORE_THAN_3D,
        ),
        (Line([0, 0], [1, 0]), Line([0, 0], [1, 0]), LINES_MUST_NOT_BE_PARALLEL),
        (Line([0, 0], [1, 0]), Line([5, 5], [1, 0]), LINES_MUST_NOT_BE_PARALLEL),
        (Line([0, 0], [0, 1]), Line([0, 0], [0, 5]), LINES_MUST_NOT_BE_PARALLEL),
        (Line([0, 0], [1, 0]), Line([0, 0], [-1, 0]), LINES_MUST_NOT_BE_PARALLEL),
        (Line([0, 0], [1, 0]), Line([5, 5], [-1, 0]), LINES_MUST_NOT_BE_PARALLEL),
        (
            Line([0, 0, 0], [1, 1, 1]),
            Line([0, 1, 0], [-1, 0, 0]),
            LINES_MUST_BE_COPLANAR,
        ),
    ],
)
def test_intersect_line_failure(line_a, line_b, message_expected):

    with pytest.raises(ValueError, match=message_expected):
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
    ("points", "message_expected"),
    [
        ([[]], ARRAY_MUST_NOT_BE_EMPTY),
        ([[0, 0]], POINTS_MUST_NOT_BE_CONCURRENT),
        ([[0, 0, 0]], POINTS_MUST_NOT_BE_CONCURRENT),
        ([[1, 2], [1, 2], [1, 2]], POINTS_MUST_NOT_BE_CONCURRENT),
    ],
)
def test_best_fit_failure(points, message_expected):

    with pytest.raises(ValueError, match=message_expected):
        Line.best_fit(points)


@pytest.mark.parametrize(
    ("line", "points", "coords_expected"),
    [
        (Line([0, 0], [1, 0]), [[1, 0], [2, 0], [3, 0], [4, 0]], [1, 2, 3, 4]),
        # The point on the line acts as the origin.
        (Line([3, 0], [1, 0]), [[1, 0], [2, 0], [3, 0], [4, 0]], [-2, -1, 0, 1]),
        (
            Line([0, 0], [1, 1]),
            [[1, 0], [2, 0], [3, 0], [0, 1], [0, 2], [0, 3]],
            math.sqrt(2) * np.array([0.5, 1, 1.5, 0.5, 1, 1.5]),
        ),
        # The magnitude of the direction vector is irrelevant.
        (
            Line([0, 0], [3, 3]),
            [[1, 0], [2, 0], [3, 0], [0, 1], [0, 2], [0, 3]],
            math.sqrt(2) * np.array([0.5, 1, 1.5, 0.5, 1, 1.5]),
        ),
        (
            Line([0, 0, 0], [1, 0, 0]),
            [[1, 20, 3], [2, -5, 8], [3, 59, 100], [4, 0, 14]],
            [1, 2, 3, 4],
        ),
        (
            Line([0, 0, 0], [0, 1, 0]),
            [[1, 20, 3], [2, -5, 8], [3, 59, 100], [4, 0, 14]],
            [20, -5, 59, 0],
        ),
    ],
)
def test_transform_points(line, points, coords_expected):

    coordinates = line.transform_points(points)
    assert_array_almost_equal(coordinates, coords_expected)
