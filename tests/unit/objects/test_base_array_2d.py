import numpy as np
import pytest

from skspatial.objects import Points


@pytest.mark.parametrize(
    ("array", "dimension"),
    [
        (np.zeros((3, 1)), 0),
        (np.zeros((3, 2)), 1),
        (np.zeros((3, 3)), 2),
    ],
)
def test_dimension_failure(array, dimension):

    message_expected = "The desired dimension cannot be less than the current dimension."

    points = Points(array)

    with pytest.raises(ValueError, match=message_expected):
        points.set_dimension(dimension)
