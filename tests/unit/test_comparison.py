import pytest
from skspatial.objects import Point, Vector, Line


@pytest.mark.parametrize(
    "array_u, array_v, bool_expected",
    [
        ([1, 0], [0, 1], True),
        ([0, 1], [-1, 0], True),
        ([0, 1], [-1, 0], True),
        ([-1, 0], [0, -1], True),
        ([1, 1], [-1, -1], False),
        ([1, 1], [1, 1], False),
        # The zero vector is perpendicular to all vectors.
        ([0, 0], [-1, 5], True),
        ([0, 0, 0], [1, 1, 1], True),
    ],
)
def test_is_perpendicular(array_u, array_v, bool_expected):
    """Test checking if vector u is perpendicular to vector v."""
    vector_u = Vector(array_u)
    vector_v = Vector(array_v)

    assert vector_u.is_perpendicular(vector_v) == bool_expected


@pytest.mark.parametrize(
    "array_u, array_v, bool_expected",
    [
        ([0, 1], [0, 1], True),
        ([0, 1], [0, 5], True),
        ([1, 1], [-1, -1], True),
        ([1, 1], [-5, -5], True),
        ([0, 1], [0, -1], True),
        ([0, 1], [4, 0], False),
        ([0.1, 5, 4], [3, 2, 0], False),
        # The zero vector is parallel to all vectors.
        ([0, 0], [-1, 5], True),
        ([0, 0, 0], [1, 1, 1], True),
    ],
)
def test_is_parallel(array_u, array_v, bool_expected):
    """Test checking if vector u is parallel to vector v."""
    vector_u = Vector(array_u)
    vector_v = Vector(array_v)

    assert vector_u.is_parallel(vector_v) == bool_expected


@pytest.mark.parametrize(
    "array_a, array_b, array_c, bool_expected",
    [
        ([0], [0], [0], True),
        ([1], [1], [1], True),
        ([0, 0], [0, 1], [0, 2], True),
        ([0, 1], [0, 0], [0, 2], True),
        ([0, 0], [-1, 0], [10, 0], True),
        ([0, 0], [0, 1], [1, 2], False),
        ([0, 0, 0], [1, 1, 1], [2, 2, 2], True),
        ([0, 0, 0], [1, 1, 1], [2, 2, 2.5], False),
    ],
)
def test_is_collinear(array_a, array_b, array_c, bool_expected):
    """Test checking if three points are collinear."""
    point_a = Point(array_a)
    point_b = Point(array_b)
    point_c = Point(array_c)

    assert point_a.is_collinear(point_b, point_c) == bool_expected


@pytest.mark.parametrize(
    "arr_point_a, arr_vector_a, arr_point_b, arr_vector_b, bool_expected",
    [
        ([0, 0], [1, 1], [0, 0], [0, 1], True),
        ([-6, 7], [5, 90], [1, 4], [-4, 5], True),
        ([0, 0, 1], [1, 1], [0, 0], [0, 1], False),
        ([0, 0, 1], [1, 1], [0, 0, 1], [0, 1], True),
        ([0, 0, 1], [1, 0, 1], [0, 0, 1], [2, 0, 2], True),
    ],
)
def test_is_coplanar(
    arr_point_a, arr_vector_a, arr_point_b, arr_vector_b, bool_expected
):

    line_a = Line(Point(arr_point_a), Vector(arr_vector_a))
    line_b = Line(Point(arr_point_b), Vector(arr_vector_b))

    assert line_a.is_coplanar(line_b) == bool_expected
