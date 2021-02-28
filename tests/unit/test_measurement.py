import math

import numpy as np
import pytest

from skspatial.measurement import area_triangle
from skspatial.measurement import volume_tetrahedron


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
