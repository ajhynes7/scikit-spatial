"""Test functionality of objects based on a NumPy array (Point, Vector, and Points)."""

import numpy as np
import pytest
from skspatial.objects import Point, Points, Vector


@pytest.mark.parametrize("class_spatial", [Point, Vector, Points])
@pytest.mark.parametrize("dtype", [np.float32, np.float64, np.int64])
@pytest.mark.parametrize("decimals", [-1, 0, 1, 3])
@pytest.mark.parametrize("readonly", [False, True])
def test_round_preserves_original(class_spatial, dtype, decimals, readonly):
    array = np.array([[1.234, -12.345, 23.456], [34.567, 45.678, -56.789]], dtype=dtype)
    if class_spatial is not Points:
        array = array[0]
    expected_original = array.copy()
    array.flags.writeable = not readonly
    spatial = class_spatial(array)

    rounded = spatial.round(decimals)

    assert isinstance(rounded, class_spatial)
    assert rounded.dtype == array.dtype
    np.testing.assert_array_equal(rounded, np.round(expected_original, decimals))
    np.testing.assert_array_equal(spatial, expected_original)
    np.testing.assert_array_equal(array, expected_original)
    assert not np.shares_memory(rounded, spatial)


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
