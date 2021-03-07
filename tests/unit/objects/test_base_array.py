"""Test functionality of objects based on a NumPy array (Point, Vector, and Points)."""
import numpy as np
import pytest

from skspatial.objects import Point
from skspatial.objects import Points
from skspatial.objects import Vector


@pytest.mark.parametrize("class_spatial", [Point, Vector, Points])
@pytest.mark.parametrize(
    "array",
    [
        [[0], [0, 0]],
        [[0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0]],
    ],
)
def test_failure_from_different_lengths(class_spatial, array):

    message_expected = "The array must not contain sequences with different lengths."

    with pytest.raises(ValueError, match=message_expected):
        class_spatial(array)


@pytest.mark.parametrize("class_spatial", [Point, Vector, Points])
@pytest.mark.parametrize(
    "array",
    [
        [],
        [[]],
        [[], []],
    ],
)
def test_failure_from_empty_array(class_spatial, array):

    message_expected = "The array must not be empty."

    with pytest.raises(ValueError, match=message_expected):
        class_spatial(array)


@pytest.mark.parametrize("class_spatial", [Point, Vector, Points])
@pytest.mark.parametrize(
    "array",
    [
        [np.nan, 0],
        [1, 1, np.nan],
        [1, 1, np.inf],
        [[1, 1], [np.inf, 0]],
    ],
)
def test_failure_from_infinite_values(class_spatial, array):

    message_expected = "The values must all be finite."

    with pytest.raises(ValueError, match=message_expected):
        class_spatial(array)
