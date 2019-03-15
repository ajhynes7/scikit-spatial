"""Test features related to both the Line and Plane."""

import pytest

from skspatial.objects import Line, Plane


@pytest.mark.parametrize(
    "point, vector",
    [
        # The point and vector must have the same length.
        ([0], [0, 1]),
        ([5, 4], [6]),
        ([5, 7, 3], [1, 2]),
        # The zero vector cannot be used.
        ([0], [0]),
        ([1, 1], [0, 0]),
        ([1, 1, 1], [0, 0, 0]),
        ([4, 5, 2, 3], [0, 0, 0, 0]),
    ],
)
@pytest.mark.parametrize("class_spatial", [Line, Plane])
def test_init_failure(point, vector, class_spatial):

    with pytest.raises(Exception):
        class_spatial(point, vector)
