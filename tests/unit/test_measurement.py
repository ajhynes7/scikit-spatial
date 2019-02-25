import numpy as np
import pytest

from skspatial.measurement import area_triangle
from skspatial.objects import Point


@pytest.mark.parametrize(
    "array_a, array_b, array_c, area_expected",
    [
        ([0, 0], [1, 0], [0, 1], 0.5),
        ([0, 0], [1, 1], [2, 0], 1),
        ([0, 0], [1, 10], [2, 0], 10),
        ([0, 0], [1, 0], [2, 0], 0),
        ([0, 0], [-5, -2], [5, 2], 0),
        ([1, 0, 0], [0, 1, 0], [0, 0, 1], np.sin(np.pi / 3)),
        ([2, 0, 0], [0, 2, 0], [0, 0, 2], 4 * np.sin(np.pi / 3)),
    ],
)
def test_equality(array_a, array_b, array_c, area_expected):

    point_a = Point(array_a)
    point_b = Point(array_b)
    point_c = Point(array_c)

    area = area_triangle(point_a, point_b, point_c)

    assert np.isclose(area, area_expected)
