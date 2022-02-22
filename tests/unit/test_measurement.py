import math

import numpy as np
import pytest

from skspatial.measurement import area_signed
from skspatial.measurement import area_triangle
from skspatial.measurement import volume_tetrahedron
from skspatial.objects import Points


@pytest.mark.parametrize(
    ("array_a", "array_b", "array_c", "area_expected"),
    [
        ([0, 0], [1, 0], [0, 1], 0.5),
        ([0, 0], [1, 1], [2, 0], 1),
        ([0, 0], [1, 10], [2, 0], 10),
        ([0, 0], [1, 0], [2, 0], 0),
        ([0, 0], [-5, -2], [5, 2], 0),
        ([1, 0, 0], [0, 1, 0], [0, 0, 1], math.sin(np.pi / 3)),
        ([2, 0, 0], [0, 2, 0], [0, 0, 2], 4 * math.sin(np.pi / 3)),
    ],
)
def test_area_triangle(array_a, array_b, array_c, area_expected):

    area = area_triangle(array_a, array_b, array_c)
    assert math.isclose(area, area_expected)


@pytest.mark.parametrize(
    ("array_a", "array_b", "array_c", "array_d", "volume_expected"),
    [
        ([0, 0], [2, 0], [1, 1], [10, -7], 0),
        ([0, 0, 0], [2, 0, 0], [1, 1, 0], [0, 0, 1], 1 / 3),
        ([0, 0, 0], [2, 0, 0], [1, 1, 0], [0, 0, -1], 1 / 3),
        ([0, 0, 0], [2, 0, 0], [1, 1, 0], [0, 0, 2], 2 / 3),
        ([0, 0, 0], [2, 0, 0], [1, 1, 0], [0, 0, 3], 1),
        ([0, 0, 0], [2, 0, 0], [1, 1, 0], [-56, 10, 3], 1),
        ([0, 1, 1], [0, 1, 5], [0, -5, 7], [0, 5, 2], 0),
    ],
)
def test_volume_tetrahedron(array_a, array_b, array_c, array_d, volume_expected):

    volume = volume_tetrahedron(array_a, array_b, array_c, array_d)
    assert math.isclose(volume, volume_expected)


@pytest.mark.parametrize(
    ("points", "area_expected"),
    [
        # Counter-clockwise triangle
        ([[2, 2], [6, 2], [4, 5]], 6),
        # Clockwise triangle
        ([[1, 3], [-4, 3], [-3, 4]], -2.5),
        # Counter-clockwise square
        ([[-1, 2], [2, 5], [-1, 8], [-4, 5]], 18),
        # Clockwise irregular convex pentagon
        ([[-2, 2], [-5, 2], [-8, 5], [-4, 8], [-1, 5]], -25.5),
        # Counter-clockwise irregular convex hexagon
        ([[3, -2], [6, -3], [10, -1], [8, 4], [4, 3], [1, 1]], 39.5),
        # Clockwise non-convex polygon
        ([[5, -2], [1, -1], [0, 4], [6, 6], [3, 3]], -22),
        # Self-overlapping polygon
        ([[-4, 4], [-4, 1], [2, 4], [2, 1]], 0),
    ],
)
def test_area_signed(points, area_expected):

    points = Points(points)
    area = area_signed(points)

    assert area == area_expected


@pytest.mark.parametrize(
    ("points", "message_expected"),
    [
        ([[1, 0, 0], [-1, 0, 0], [0, 1, 0]], "The points must be 2D."),
        ([[2, 0], [-2, 0]], "There must be at least 3 points."),
    ],
)
def test_area_signed_failure(points, message_expected):

    with pytest.raises(ValueError, match=message_expected):
        area_signed(points)
