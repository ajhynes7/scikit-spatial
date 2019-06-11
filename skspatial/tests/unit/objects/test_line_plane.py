"""Test features related to both the Line and Plane."""

import pytest

from skspatial.objects import Line, Plane


@pytest.mark.parametrize("class_spatial", [Line, Plane])
@pytest.mark.parametrize(
    "point, vector",
    [
        # The zero vector cannot be used.
        ([0, 0], [0, 0]),
        ([1, 1], [0, 0]),
        ([1, 1, 1], [0, 0, 0]),
        ([4, 5, 2, 3], [0, 0, 0, 0]),
    ],
)
def test_init_failure(class_spatial, point, vector):

    with pytest.raises(Exception):
        class_spatial(point, vector)
