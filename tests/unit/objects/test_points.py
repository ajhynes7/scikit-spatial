import pytest

from skspatial.objects import Points


@pytest.mark.parametrize("array", [[[0]], [[0], [0]], [[0], [1], [3]]])
def test_failure(array):

    with pytest.raises(Exception):
        Points(array)
