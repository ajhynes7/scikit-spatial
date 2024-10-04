"""Test functionality of objects based on a NumPy array (Point, Vector, and Points)."""

import numpy as np
import pytest
from skspatial.objects import Point, Points, Vector


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
    with pytest.raises(ValueError):  # noqa: PT011
        class_spatial(array)


@pytest.mark.parametrize(
    ("class_spatial", "array", "message_expected"),
    [
        (Point, [], "The array must not be empty."),
        (Vector, [], "The array must not be empty."),
        (Points, [], "The array must be 2D."),
    ],
)
def test_failure_from_empty_array(class_spatial, array, message_expected):
    with pytest.raises(ValueError, match=message_expected):
        class_spatial(array)


@pytest.mark.parametrize(
    ("class_spatial", "array"),
    [
        (Point, [np.nan, 0]),
        (Vector, [np.nan, 0]),
        (Point, [1, np.inf]),
        (Vector, [1, np.inf]),
        (Points, [[1, 1], [1, np.nan]]),
    ],
)
def test_failure_from_infinite_values(class_spatial, array):
    message_expected = "The values must all be finite."

    with pytest.raises(ValueError, match=message_expected):
        class_spatial(array)
