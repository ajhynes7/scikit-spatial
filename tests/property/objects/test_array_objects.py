"""Test behaviour of points with vectors."""

import numpy as np
import pytest
from hypothesis import given

from skspatial.objects import Point, Vector
from tests.property.strategies import st_arrays, st_point, st_vector


@given(st_arrays)
def test_length(array):

    if len(array) <= 3:

        point = Point(array)
        vector = Vector(array)

        assert point != vector
        assert point.array.size == vector.array.size == 3
        assert np.allclose(point.array, vector.array)

    else:

        with pytest.raises(Exception):
            Point(array)
        with pytest.raises(Exception):
            Vector(array)


@given(st_point(), st_vector())
def test_add(point, vector):
    """Test adding points and vectors."""

    # Add and subtract the vector to obtain the same point.
    assert point.add(vector).subtract(vector).is_close(point)

    with pytest.raises(Exception):
        point.add(point)

    with pytest.raises(Exception):
        vector.add(point)


@given(st_point())
def test_is_close(point):

    vector = Vector(point.array)

    assert point.is_close(point)
    assert vector.is_close(vector)

    with pytest.raises(Exception):
        assert point.is_close(vector)

    with pytest.raises(Exception):
        assert vector.is_close(point)
