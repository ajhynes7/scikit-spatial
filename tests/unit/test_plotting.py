import pytest

from skspatial.objects import Plane, Sphere


@pytest.mark.parametrize(
    "plane, points_expected",
    [
        (Plane([0, 0, 0], [0, 0, 1]), [[-1, -1, 0], [1, -1, 0], [-1, 1, 0], [1, 1, 0]]),
        (Plane([1, 0, 0], [0, 0, 1]), [[0, -1, 0], [2, -1, 0], [0, 1, 0], [2, 1, 0]]),
        (Plane([0, 0, 0], [0, 0, -1]), [[-1, -1, 0], [1, -1, 0], [-1, 1, 0], [1, 1, 0]]),
        (Plane([0, 0, 0], [0, 0, 5]), [[-1, -1, 0], [1, -1, 0], [-1, 1, 0], [1, 1, 0]]),
        (Plane([0, 0, 0], [0, 1, 0]), [[-1, 0, -1], [1, 0, -1], [-1, 0, 1], [1, 0, 1]]),
        (Plane([0, 0, 0], [1, 0, 0]), [[0, -1, -1], [0, 1, -1], [0, -1, 1], [0, 1, 1]]),
        (Plane([0, 0, 0], [1, 1, 0]), [[-1, 1, -1], [1, -1, -1], [-1, 1, 1], [1, -1, 1]]),
    ],
)
def test_plane_points(plane, points_expected):

    points = plane.to_points()

    assert points.is_close(points_expected)


@pytest.mark.parametrize(
    "sphere, n_angles, points_expected",
    [
        (Sphere([0, 0, 0], 1), 1, [[0, 0, 1]]),
        (Sphere([0, 0, 0], 1), 2, [[0, 0, -1], [0, 0, 1]]),
        (Sphere([0, 0, 0], 1), 3, [[0, -1, 0], [0, 0, -1], [0, 0, 1], [0, 1, 0]]),
        (Sphere([0, 0, 0], 2), 3, [[0, -2, 0], [0, 0, -2], [0, 0, 2], [0, 2, 0]]),
        (Sphere([1, 0, 0], 1), 3, [[1, -1, 0], [1, 0, -1], [1, 0, 1], [1, 1, 0]]),
        (Sphere([1, 1, 1], 1), 3, [[1, 0, 1], [1, 1, 0], [1, 1, 2], [1, 2, 1]]),
    ],
)
def test_sphere_points(sphere, n_angles, points_expected):

    points = sphere.to_points(n_angles).round(3).unique()

    assert points.is_close(points_expected)
