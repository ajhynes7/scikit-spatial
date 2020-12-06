from math import isclose, sqrt, pi

import pytest

from skspatial.objects import Cylinder


@pytest.mark.parametrize(
    "point, vector, radius, message_expected",
    [
        ([0, 0], [1, 0, 0], 1, "The point must be 3D."),
        ([0, 0, 0], [1, 0], 1, "The vector must be 3D."),
        ([0, 0, 0], [0, 0, 0], 1, "The vector must not be the zero vector."),
        ([0, 0, 0], [0, 0, 1], 0, "The radius must be positive."),
    ],
)
def test_failure(point, vector, radius, message_expected):

    with pytest.raises(ValueError, match=message_expected):
        Cylinder(point, vector, radius)


@pytest.mark.parametrize(
    "cylinder, length_expected, volume_expected",
    [
        (Cylinder([0, 0, 0], [0, 0, 1], 1), 1, pi),
        (Cylinder([0, 0, 0], [0, 0, 1], 2), 1, 4 * pi),
        (Cylinder([0, 0, 0], [0, 0, 2], 1), 2, 2 * pi),
        (Cylinder([0, 0, 0], [0, 0, 2], 2), 2, 8 * pi),
        (Cylinder([1, 1, 1], [0, 0, 2], 2), 2, 8 * pi),
        (Cylinder([0, 0, 0], [0, 1, 1], 1), sqrt(2), sqrt(2) * pi),
        (Cylinder([0, 0, 0], [1, 1, 1], 1), sqrt(3), sqrt(3) * pi),
        (Cylinder([0, 0, 0], [5, 5, 5], 2), 5 * sqrt(3), 20 * sqrt(3) * pi),
    ],
)
def test_properties(cylinder, length_expected, volume_expected):

    assert isclose(cylinder.length(), length_expected)
    assert isclose(cylinder.volume(), volume_expected)
