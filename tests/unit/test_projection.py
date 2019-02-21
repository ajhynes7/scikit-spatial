import numpy as np
import pytest

from skspatial import Vector


@pytest.mark.parametrize(
    "array, array_unit_expected",
    [
        ([1, 0], [1, 0]),
        ([2, 0], [1, 0]),
        ([-1, 0], [-1, 0]),
        ([0, 0, 5], [0, 0, 1]),
        ([1, 1], [np.sqrt(2) / 2, np.sqrt(2) / 2]),
        ([1, 1, 1], [np.sqrt(3) / 3, np.sqrt(3) / 3, np.sqrt(3) / 3]),
    ],
)
def test_unit(array, array_unit_expected):
    """Test converting a vector to its unit vector."""
    vector = Vector(array)
    vector_unit_expected = Vector(array_unit_expected)

    assert np.allclose(vector.unit().array, vector_unit_expected.array)
