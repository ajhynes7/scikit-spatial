"""Test features related to both the Line and Plane."""

import pytest

from skspatial.objects import Line, Plane


@pytest.mark.parametrize("class_spatial", [Line, Plane])
@pytest.mark.parametrize(
    "point, vector",
    [
        ([0, 0], [0, 0]),
        ([1, 1], [0, 0]),
        ([1, 1, 1], [0, 0, 0]),
        ([4, 5, 2, 3], [0, 0, 0, 0]),
    ],
)
def test_zero_vector_failure(class_spatial, point, vector):

    with pytest.raises(ValueError, match="The vector must not be the zero vector."):
        class_spatial(point, vector)


@pytest.mark.parametrize("class_spatial", [Line, Plane])
@pytest.mark.parametrize(
    "point, vector",
    [
        ([0, 0, 1], [1, 1]),
        ([0, 0], [1]),
        ([1], [0, 1]),
    ],
)
def test_dimension_failure(class_spatial, point, vector):

    with pytest.raises(ValueError, match="The point and vector must have the same dimension."):
        class_spatial(point, vector)
