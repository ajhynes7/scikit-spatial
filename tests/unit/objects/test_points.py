import pytest

from skspatial.objects import Points


@pytest.mark.parametrize(
    "array",
    [
        # The array cannot be empty.
        [],
        [[]],
        [[], []],
        # The array cannot be 1D.
        [0],
        [5],
        [0, 1],
        [0, 1, 2],
        # The array cannot have one element.
        [[0]],
        [[5]],
        # The points cannot have different lengths.
        [[0, 1], [0, 1, 0]],
    ],
)
def test_failure(array):

    with pytest.raises(Exception):
        Points(array)
