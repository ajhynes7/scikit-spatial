import numpy as np
import pytest
from hypothesis import assume, given

from skspatial.constants import ATOL
from skspatial.objects import Vector
from tests.property.strategies import st_floats, st_point, st_vector, st_vector_nonzero


@given(st_point(), st_point())
def test_from_points(point_a, point_b):

    vector_ab = Vector.from_points(point_a, point_b)

    assert point_a.add(vector_ab).is_close(point_b)


@given(st_vector_nonzero())
def test_unit(vector):

    vector_unit = vector.unit()

    assert np.isclose(vector_unit.magnitude, 1)
    assert vector_unit.scale(vector.magnitude).is_close(vector)

    assert vector_unit.is_parallel(vector)

    angle = vector.angle_between(vector_unit)
    assert np.isclose(angle, 0, atol=ATOL)


@given(st_vector())
def test_add_subtract(vector):

    assert vector.add(vector).subtract(vector).is_close(vector)


@given(st_point(), st_vector_nonzero())
def test_reverse(point, vector):

    vector_reversed = vector.reverse()
    assert vector.add(vector_reversed).is_close(Vector([0]))
    assert vector.is_parallel(vector_reversed)

    assert point.add(vector_reversed).is_close(point.subtract(vector))

    angle = np.degrees(vector.angle_between(vector_reversed))
    assert np.isclose(angle, 180, atol=ATOL)


@given(st_vector_nonzero(), st_floats)
def test_scale(vector, scalar):

    assume(abs(scalar) > ATOL)

    vector_scaled = vector.scale(scalar)

    assert vector.is_parallel(vector_scaled, atol=ATOL)

    angle = np.degrees(vector.angle_between(vector_scaled))

    if scalar > 0:
        assert np.isclose(angle, 0, atol=ATOL)
    else:
        assert np.isclose(angle, 180, atol=ATOL)


@given(st_vector_nonzero(), st_vector_nonzero())
def test_two_vectors(vector_a, vector_b):

    is_perpendicular = vector_a.is_perpendicular(vector_b)
    is_parallel = vector_a.is_parallel(vector_b)

    # Two non-zero vectors cannot be both perpendicular and parallel.
    assert not (is_perpendicular and is_parallel)

    angle = np.degrees(vector_a.angle_between(vector_b))

    assert is_parallel == (np.isclose(angle, 0) or np.isclose(angle, 180))
    assert is_perpendicular == np.isclose(angle, 90)

    # The zero vector is perpendicular and parallel to any other vector.
    vector_zero = Vector([0])
    assert vector_a.is_perpendicular(vector_zero)
    assert vector_a.is_parallel(vector_zero)

    # The angle with the zero vector is undefined.
    with pytest.raises(Exception):
        vector_a.angle_between(vector_zero)

    # The projection of vector B onto A is parallel to A.
    vector_b_projected = vector_a.project_vector(vector_b)
    assert vector_a.is_parallel(vector_b_projected, atol=ATOL)

    # The projection is zero iff vectors A and B are perpendicular.
    assert vector_b_projected.is_zero() == is_perpendicular

    assert (vector_a.dot(vector_b) > 0) == (angle < 90)
