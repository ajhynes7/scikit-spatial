import numpy as np
import pytest

from skspatial.objects import Circle


@pytest.mark.parametrize(
    "point, radius",
    [
        # The point must be 2D.
        ([0], 1),
        ([0, 0, 0], 1),
        ([1, 2, 3], 1),
        ([0, 0, 0, 0], 1),
        # The radius must be positive.
        ([0, 0], 0),
        ([0, 0], -1),
        ([0, 0], -5),
    ],
)
def test_failure(point, radius):

    with pytest.raises(Exception):
        Circle(point, radius)


@pytest.mark.parametrize(
    "radius, circumference_expected, area_expected",
    [
        (1, 2 * np.pi, np.pi),
        (2, 4 * np.pi, 4 * np.pi),
        (3, 6 * np.pi, 9 * np.pi),
        (4.5, 9 * np.pi, 20.25 * np.pi),
        (10, 20 * np.pi, 100 * np.pi),
    ],
)
def test_circumference_area(radius, circumference_expected, area_expected):

    circle = Circle([0, 0], radius)

    assert np.isclose(circle.circumference(), circumference_expected)
    assert np.isclose(circle.area(), area_expected)
