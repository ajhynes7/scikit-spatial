import math
from math import sqrt

import numpy as np
import pytest

from skspatial.objects.line import Line
from skspatial.objects.points import Points
from skspatial.objects.sphere import Sphere


@pytest.mark.parametrize(
    ("point", "radius"),
    [
        # The point must be 3D.
        ([0], 1),
        ([0, 0], 1),
        ([0, 0, 0, 0], 1),
        ([1, 2, 3, 4], 1),
        # The radius must be positive.
        ([0, 0, 0], 0),
        ([0, 0, 0], -1),
        ([0, 0, 0], -5),
    ],
)
def test_failure(point, radius):

    with pytest.raises(Exception):
        Sphere(point, radius)


@pytest.mark.parametrize(
    ("radius", "surface_area_expected", "volume_expected"),
    [
        (1, 4 * np.pi, 4 / 3 * np.pi),
        (2, 16 * np.pi, 32 / 3 * np.pi),
        (3, 36 * np.pi, 36 * np.pi),
        (4.5, 81 * np.pi, 121.5 * np.pi),
        (10, 400 * np.pi, 4000 / 3 * np.pi),
    ],
)
def test_surface_area_volume(radius, surface_area_expected, volume_expected):

    sphere = Sphere([0, 0, 0], radius)

    assert math.isclose(sphere.surface_area(), surface_area_expected)
    assert math.isclose(sphere.volume(), volume_expected)


@pytest.mark.parametrize(
    ("sphere", "point", "dist_expected"),
    [
        (Sphere([0, 0, 0], 1), [0, 0, 0], 1),
        (Sphere([0, 0, 0], 1), [1, 0, 0], 0),
        (Sphere([0, 0, 0], 1), [0, -1, 0], 0),
        (Sphere([0, 0, 0], 2), [0, 0, 0], 2),
        (Sphere([0, 0, 0], 1), [1, 1, 1], math.sqrt(3) - 1),
        (Sphere([0, 0, 0], 2), [1, 1, 1], 2 - math.sqrt(3)),
        (Sphere([1, 0, 0], 2), [0, 0, 0], 1),
    ],
)
def test_distance_point(sphere, point, dist_expected):

    assert math.isclose(sphere.distance_point(point), dist_expected)


@pytest.mark.parametrize(
    ("sphere", "point", "bool_expected"),
    [
        (Sphere([0, 0, 0], 1), [1, 0, 0], True),
        (Sphere([0, 0, 0], 1), [0, 1, 0], True),
        (Sphere([0, 0, 0], 1), [0, 0, 1], True),
        (Sphere([0, 0, 0], 1), [-1, 0, 0], True),
        (Sphere([0, 0, 0], 1), [0, -1, 0], True),
        (Sphere([0, 0, 0], 1), [0, 0, -1], True),
        (Sphere([0, 0, 0], 1), [1, 1, 0], False),
        (Sphere([1, 0, 0], 1), [1, 0, 0], False),
        (Sphere([1, 0, 0], 1), [2, 0, 0], True),
        (Sphere([0, 0, 0], 2), [0, 2, 0], True),
        (Sphere([0, 0, 0], math.sqrt(3)), [1, 1, 1], True),
    ],
)
def test_contains_point(sphere, point, bool_expected):

    assert sphere.contains_point(point) == bool_expected


@pytest.mark.parametrize(
    ("sphere", "point", "point_expected"),
    [
        (Sphere([0, 0, 0], 1), [1, 0, 0], [1, 0, 0]),
        (Sphere([0, 0, 0], 2), [1, 0, 0], [2, 0, 0]),
        (Sphere([0, 0, 0], 0.1), [1, 0, 0], [0.1, 0, 0]),
        (Sphere([-1, 0, 0], 1), [1, 0, 0], [0, 0, 0]),
        (Sphere([0, 0, 0], 1), [1, 1, 1], math.sqrt(3) / 3 * np.ones(3)),
        (Sphere([0, 0, 0], 3), [1, 1, 1], math.sqrt(3) * np.ones(3)),
    ],
)
def test_project_point(sphere, point, point_expected):

    point_projected = sphere.project_point(point)
    assert point_projected.is_close(point_expected)


@pytest.mark.parametrize(
    ("sphere", "point"),
    [
        (Sphere([0, 0, 0], 1), [0, 0, 0]),
        (Sphere([0, 0, 0], 5), [0, 0, 0]),
        (Sphere([5, 2, -6], 5), [5, 2, -6]),
    ],
)
def test_project_point_failure(circle, point):

    with pytest.raises(Exception):
        circle.project_point(point)


@pytest.mark.parametrize(
    ("points", "sphere_expected"),
    [
        ([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, 0, 1]], Sphere(point=[0, 0, 0], radius=1)),
        ([[2, 0, 0], [-2, 0, 0], [0, 2, 0], [0, 0, 2]], Sphere(point=[0, 0, 0], radius=2)),
        ([[1, 0, 1], [0, 1, 1], [1, 2, 1], [1, 1, 2]], Sphere(point=[1, 1, 1], radius=1)),
    ],
)
def test_best_fit(points, sphere_expected):

    points = Points(points)
    sphere_fit = Sphere.best_fit(points)

    assert sphere_fit.point.is_close(sphere_expected.point, abs_tol=1e-9)
    assert math.isclose(sphere_fit.radius, sphere_expected.radius)


@pytest.mark.parametrize(
    ("points", "message_expected"),
    [
        ([[1, 0], [-1, 0], [0, 1], [0, 0]], "The points must be 3D."),
        ([[2, 0, 0], [-2, 0, 0], [0, 2, 0]], "There must be at least 4 points."),
        ([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]], "The points must not be in a plane."),
    ],
)
def test_best_fit_failure(points, message_expected):

    with pytest.raises(ValueError, match=message_expected):
        Sphere.best_fit(points)


@pytest.mark.parametrize(
    ("sphere", "line", "point_a_expected", "point_b_expected"),
    [
        (Sphere([0, 0, 0], 1), Line([0, 0, 0], [1, 0, 0]), [-1, 0, 0], [1, 0, 0]),
        (
            Sphere([0, 0, 0], 1),
            Line([0, 0, 0], [1, 1, 0]),
            -sqrt(2) / 2 * np.array([1, 1, 0]),
            sqrt(2) / 2 * np.array([1, 1, 0]),
        ),
        (
            Sphere([0, 0, 0], 1),
            Line([0, 0, 0], [1, 1, 1]),
            -sqrt(3) / 3 * np.ones(3),
            sqrt(3) / 3 * np.ones(3),
        ),
        (Sphere([1, 0, 0], 1), Line([0, 0, 0], [1, 0, 0]), [0, 0, 0], [2, 0, 0]),
        (Sphere([0, 0, 0], 1), Line([1, 0, 0], [0, 0, 1]), [1, 0, 0], [1, 0, 0]),
    ],
)
def test_intersect_line(sphere, line, point_a_expected, point_b_expected):

    point_a, point_b = sphere.intersect_line(line)

    assert point_a.is_close(point_a_expected)
    assert point_b.is_close(point_b_expected)


@pytest.mark.parametrize(
    ("sphere", "line"),
    [
        (Sphere([0, 0, 0], 1), Line([0, 0, 2], [1, 0, 0])),
        (Sphere([0, 0, 0], 1), Line([0, 0, -2], [1, 0, 0])),
        (Sphere([0, 2, 0], 1), Line([0, 0, 0], [1, 0, 0])),
        (Sphere([0, -2, 0], 1), Line([0, 0, 0], [1, 0, 0])),
        (Sphere([5, 0, 0], 1), Line([0, 0, 0], [1, 1, 1])),
    ],
)
def test_intersect_line_failure(sphere, line):

    with pytest.raises(Exception):
        sphere.intersect_line(line)


@pytest.mark.parametrize(
    ("sphere", "n_angles", "points_expected"),
    [
        (Sphere([0, 0, 0], 1), 1, [[0, 0, 1]]),
        (Sphere([0, 0, 0], 1), 2, [[0, 0, -1], [0, 0, 1]]),
        (Sphere([0, 0, 0], 1), 3, [[0, -1, 0], [0, 0, -1], [0, 0, 1], [0, 1, 0]]),
        (Sphere([0, 0, 0], 2), 3, [[0, -2, 0], [0, 0, -2], [0, 0, 2], [0, 2, 0]]),
        (Sphere([1, 0, 0], 1), 3, [[1, -1, 0], [1, 0, -1], [1, 0, 1], [1, 1, 0]]),
        (Sphere([1, 1, 1], 1), 3, [[1, 0, 1], [1, 1, 0], [1, 1, 2], [1, 2, 1]]),
    ],
)
def test_to_points(sphere, n_angles, points_expected):

    array_rounded = sphere.to_points(n_angles=n_angles).round(3)
    points_unique = Points(array_rounded).unique()

    assert points_unique.is_close(points_expected)
