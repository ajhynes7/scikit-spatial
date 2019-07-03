"""Test features related to both the Line and Plane."""

import pytest

from skspatial.objects import Line, Plane


@pytest.mark.parametrize("class_spatial", [Line, Plane])
@pytest.mark.parametrize(
    "point, vector",
    [
        ([0, 0], [0, 0]),
        ([1, 1], [0, 0]),
        ([1, 1, 1], [0, 0, 0]),
        ([4, 5, 2, 3], [0, 0, 0, 0]),
    ],
)
def test_zero_vector_failure(class_spatial, point, vector):

    with pytest.raises(ValueError, match="The vector must not be the zero vector."):
        class_spatial(point, vector)


@pytest.mark.parametrize("class_spatial", [Line, Plane])
@pytest.mark.parametrize(
    "point, vector", [([0, 0, 1], [1, 1]), ([0, 0], [1]), ([1], [0, 1])]
)
def test_dimension_failure(class_spatial, point, vector):

    with pytest.raises(
        ValueError, match="The point and vector must have the same dimension."
    ):
        class_spatial(point, vector)


@pytest.mark.parametrize(
    "obj_1, obj_2, bool_expected",
    [
        (Line([0, 0], [1, 0]), Line([0, 0], [1, 0]), True),
        (Line([0, 0], [1, 0]), Line([1, 0], [1, 0]), True),
        (Line([0, 0], [1, 0]), Line([-5, 0], [1, 0]), True),
        (Line([0, 0], [1, 0]), Line([-5, 0], [7, 0]), True),
        (Line([0, 0], [1, 0]), Line([-5, 0], [-20, 0]), True),
        (Line([0, 0], [1, 0]), Line([-5, 1], [1, 0]), False),
        (Plane([0, 0, 0], [0, 0, 1]), Plane([0, 0, 0], [0, 0, 1]), True),
        (Plane([0, 0, 0], [0, 0, 1]), Plane([0, 0, 0], [0, 0, 2]), True),
        (Plane([0, 0, 0], [0, 0, 1]), Plane([0, 0, 0], [0, 0, -10]), True),
        (Plane([0, 0, 0], [0, 0, 1]), Plane([0, 0, 0], [1, 0, -10]), False),
        (Line([0, 0], [1, 0]), Plane([0, 0], [1, 0]), None),
        (Plane([0, 0], [1, 0]), Line([0, 0], [1, 0]), None),
    ],
)
def test_is_close(obj_1, obj_2, bool_expected):

    if bool_expected is None:
        with pytest.raises(
            TypeError, match="The input must have the same type as the object."
        ):
            obj_1.is_close(obj_2)

    else:
        assert obj_1.is_close(obj_2) == bool_expected
