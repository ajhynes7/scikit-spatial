import numpy as np
import pytest

from skspatial.objects import Line, Plane, Points


@pytest.mark.parametrize(
    "line, points, error_expected",
    [
        (Line([0, 0], [1, 0]), [[0, 0], [10, 0]], 0),
        (Line([0, 0], [5, 0]), [[0, 0], [0, 1]], 1),
        (Line([0, 0], [1, 0]), [[0, 1], [0, -1]], 2),
        (Line([0, 0], [1, 0]), [[0, 5]], 25),
        (Line([0, 0], [1, 0]), [[0, 3], [0, -2]], 13),
        (Line([0, 0], [-20, 0]), [[1, 3], [2, -2], [3, -5]], 38),
    ],
)
def test_sum_squares_line(line, points, error_expected):

    error = line.sum_squares(points)
    assert np.isclose(error, error_expected)


@pytest.mark.parametrize(
    "plane, points, error_expected",
    [
        (Plane([0, 0, 0], [0, 0, 1]), [[25, 3, 0], [-6, 5, 0]], 0),
        (Plane([25, 9, 0], [0, 0, 1]), [[25, 3, 0], [-6, 5, 0]], 0),
        (Plane([25, 9, -2], [0, 0, 1]), [[25, 3, 0], [-6, 5, 0]], 8),
        (Plane([0, 0, 0], [0, 0, 1]), [[25, 3, 2], [-6, 5, 0]], 4),
        (Plane([0, 0, 0], [0, 0, 5]), [[25, 3, 2], [-6, 5, 0]], 4),
        (Plane([0, 0, 0], [0, 0, -5]), [[25, 3, 2], [-6, 5, 0]], 4),
    ],
)
def test_sum_squares_plane(plane, points, error_expected):

    error = plane.sum_squares(points)
    assert np.isclose(error, error_expected)


@pytest.mark.parametrize(
    "points, line_expected",
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
def test_best_fit_line(points, line_expected):

    line_fit = Line.best_fit(np.array(points))

    assert line_fit.is_close(line_expected)
    assert line_fit.point.is_close(line_expected.point)


@pytest.mark.parametrize(
    "points, plane_expected",
    [
        # The points are coplanar.
        ([[0, 0], [1, 1], [0, 2]], Plane([1 / 3, 1, 0], [0, 0, 1])),
        ([[0, 0], [0, 1], [1, 0], [1, 1]], Plane([0.5, 0.5, 0], [0, 0, 1])),
        ([[0, 0, 0], [1, 0, 0], [0, 0, 1]], Plane([1 / 3, 0, 1 / 3], [0, 1, 0])),
        (
            [[1, 0, 0], [-1, 0, 0], [1, 1, 1], [-1, 1, 1]],
            Plane([0, 0.5, 0.5], [0, 1, -1]),
        ),
        (
            [[1, 0, 1], [1, 1, 1], [-1, 0, -1], [-1, 1, -1]],
            Plane([0, 0.5, 0], [1, 0, -1]),
        ),
        (
            [[1, 0, 1], [1, 1, 1], [-1, 0, -1], [-1, 1, -1], [0, 0, 0]],
            Plane([0, 0.4, 0], [1, 0, -1]),
        ),
        # The points are not coplanar.
        (
            [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]],
            Plane([0.25, 0.25, 0.25], [1, 1, 1]),
        ),
        (
            [
                [0, 0, 0],
                [0, 0, 1],
                [0, 1, 0],
                [0, 1, 1],
                [1, 0, 0],
                [1, 0, 1],
                [1, 1, 0],
                [1, 1, 1],
            ],
            Plane([0.5, 0.5, 0.5], [0, 1, 0]),
        ),
    ],
)
def test_best_fit_plane(points, plane_expected):

    points = Points(points).set_dimension(3)
    plane_fit = Plane.best_fit(points)

    assert plane_fit.is_close(plane_expected)
    assert plane_fit.point.is_close(plane_expected.point)


@pytest.mark.parametrize(
    "points",
    [
        # There are fewer than two points.
        [[]],
        [[0, 0]],
        [[0, 0, 0]],
    ],
)
def test_best_fit_line_failure(points):

    with pytest.raises(Exception):
        Line.best_fit(points)


@pytest.mark.parametrize(
    "points",
    [
        # The points are collinear.
        [[0, 0], [1, 0]],
        [[0, 0], [2, 5]],
        [[0, 0], [1, 0], [1, 0]],
        [[0, 0], [1, 1], [2, 2]],
        [[0, 0, 0], [1, 1, 1], [-10, -10, -10]],
    ],
)
def test_best_fit_plane_failure(points):

    with pytest.raises(Exception):
        Plane.best_fit(points)
