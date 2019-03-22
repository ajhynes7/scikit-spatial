import numpy as np
import pytest

from skspatial.objects import Line, Plane


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

    plane_fit = Plane.best_fit(np.array(points))

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
        # The dimension is greater than three.
        [[0, 0, 0, 0], [1, 0, 0, 0], [0, 3, 2, 1]],
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
