import numpy as np
import pytest
from hypothesis import given

from tests.property.strategies import st_point, st_vector


@given(st_point(), st_vector())
def test_add_subtract(point, vector):

    # Cannot add or subtract a point.
    with pytest.raises(Exception):
        point.add(point)

    with pytest.raises(Exception):
        point.subtract(point)

    point_2 = point.add(vector)
    assert np.isclose(point.distance_point(point_2), vector.magnitude)

    point_3 = point_2.subtract(vector)
    assert point.is_close(point_3)
