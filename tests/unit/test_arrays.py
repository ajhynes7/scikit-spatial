import numpy as np
import pytest

from skspatial.objects import Point, Vector


@pytest.mark.parametrize(
    "point_a, point_b",
    [
        (Point([1]), Point([1])),
        (Point([1]), Point([1, 0])),
        (Point([1]), Point([1, 0, 0])),
        (Point([1, 0]), Point((1, 0))),
        (Point([1, 0]), Point(np.array([1, 0]))),
    ],
)
def test_equality(point_a, point_b):

    assert point_a == point_b

    vector_a = Vector(point_a.array)
    vector_b = Vector(point_b.array)

    assert vector_a == vector_b

    assert not point_a == vector_a
    assert not point_b == vector_b


@pytest.mark.parametrize("class_", [Point, Vector])
def test_length(class_):
    """The output point/vector is always 3D."""
    object_1 = class_([1])
    object_2 = class_([1, 1])
    object_3 = class_([1, 1, 1])

    assert all(x.array.size == 3 for x in [object_1, object_2, object_3])


@pytest.mark.parametrize(
    "array", [[], [1, 1, 1, 1], [np.nan], [1, 1, np.nan], [1, 1, np.inf]]
)
@pytest.mark.parametrize("class_", [Point, Vector])
def test_failure(class_, array):

    with pytest.raises(Exception):
        class_(array)


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
def test_unit_vector(array, array_unit_expected):
    """Test computing the unit vector from a vector."""
    vector = Vector(array)
    vector_unit_expected = Vector(array_unit_expected)

    assert np.allclose(vector.unit().array, vector_unit_expected.array)


@pytest.mark.parametrize(
    "array, kwargs, bool_expected",
    [
        ([0], {}, True),
        ([0, 0], {}, True),
        ([0, 0, 0], {}, True),
        ([0, 1], {}, False),
        # The tolerance affects the output.
        ([0, 0, 1e-4], {}, False),
        ([0, 0, 1e-4], {'atol': 1e-3}, True),
    ],
)
def test_is_zero_vector(array, kwargs, bool_expected):
    """Test checking if vector is the zero vector."""
    assert Vector(array).is_zero(**kwargs) == bool_expected
