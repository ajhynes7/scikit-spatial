import math

import numpy as np
import pytest

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
