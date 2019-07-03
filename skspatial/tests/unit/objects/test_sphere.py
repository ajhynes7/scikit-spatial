import numpy as np
import pytest

from skspatial.objects import Sphere


@pytest.mark.parametrize(
    "point, radius",
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
    "radius, surface_area_expected, volume_expected",
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

    assert np.isclose(sphere.surface_area(), surface_area_expected)
    assert np.isclose(sphere.volume(), volume_expected)
