"""Test properties of spatial objects."""

import numpy as np
import pytest
from hypothesis import assume, given
from numpy.testing import assert_array_equal, assert_allclose

from skspatial.objects import Point, Vector, Line
from ..strategies import st_arrays, st_point, st_vector, st_vector_nonzero


@given(st_arrays)
def test_length(array):

    if len(array) <= 3:

        point = Point(array)
        vector = Vector(array)

        assert point != vector
        assert point.array.size == vector.array.size == 3
        assert_array_equal(point.array, vector.array)

    else:

        with pytest.raises(Exception):
            Point(array)
        with pytest.raises(Exception):
            Vector(array)


@given(st_point(), st_vector())
def test_add(point, vector):
    """Test adding points and vectors."""

    # Add and subtract the vector.
    assert point.add(vector).subtract(vector).is_close(point)
    assert vector.add(vector).subtract(vector).is_close(vector)

    with pytest.raises(Exception):
        point.add(point)

    with pytest.raises(Exception):
        vector.add(point)


@given(st_vector_nonzero())
def test_unit_vector(vector):

    unit_vector = vector.unit()

    assert np.isclose(unit_vector.magnitude, 1)
    assert_allclose(vector.magnitude * unit_vector.array, vector.array)


@given(st_point())
def test_is_close(point):

    vector = Vector(point.array)

    assert point.is_close(point)
    assert vector.is_close(vector)

    with pytest.raises(Exception):
        assert point.is_close(vector)

    with pytest.raises(Exception):
        assert vector.is_close(point)


@given(st_point(), st_vector())
def test_line(point, vector):

    assume(not vector.is_zero())

    point_2 = point.add(vector)

    line_1 = Line(point, vector)
    line_2 = Line.from_points(point, point_2)

    assert line_1.is_close(line_2)

    # A point and vector are not interchangeable.
    with pytest.raises(Exception):
        Line(vector, point)
