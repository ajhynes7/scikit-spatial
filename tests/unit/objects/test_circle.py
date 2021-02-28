import math

import numpy as np
import pytest

from skspatial.objects import Circle


@pytest.mark.parametrize(
    ("point", "radius"),
    [
        # The point must be 2D.
        ([0, 0, 0], 1, "The point must be 2D"),
        ([1, 2, 3], 1, "The point must be 2D"),
        ([0, 0], 0, "The radius must be positive"),
        ([0, 0], -1, "The radius must be positive"),
        ([0, 0], -5, "The radius must be positive"),
    ],
)
def test_failure(point, radius, message_expected):

    with pytest.raises(ValueError, match=message_expected):
        Circle(point, radius)


@pytest.mark.parametrize(
    ("radius", "circumference_expected", "area_expected"),
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

    assert math.isclose(circle.circumference(), circumference_expected)
    assert math.isclose(circle.area(), area_expected)


@pytest.mark.parametrize(
    ("circle", "point", "dist_expected"),
    [
        (Circle([0, 0], 1), [0, 0], 1),
        (Circle([0, 0], 1), [0.5, 0], 0.5),
        (Circle([0, 0], 1), [1, 0], 0),
        (Circle([0, 0], 1), [0, 1], 0),
        (Circle([0, 0], 1), [-1, 0], 0),
        (Circle([0, 0], 1), [0, -1], 0),
        (Circle([0, 0], 1), [2, 0], 1),
        (Circle([0, 0], 1), [1, 1], math.sqrt(2) - 1),
        (Circle([1, 1], 1), [0, 0], math.sqrt(2) - 1),
        (Circle([0, 0], 2), [0, 5], 3),
    ],
)
def test_distance_point(circle, point, dist_expected):

    assert math.isclose(circle.distance_point(point), dist_expected)
