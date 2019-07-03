import pytest

from skspatial.objects import Line, Plane


@pytest.mark.parametrize("class_spatial", [Line, Plane])
@pytest.mark.parametrize(
    "point, vector, dim_expected",
    [([0, 0], [1, 0], 2), ([0, 0, 0], [1, 0, 0], 3), ([0, 0, 0, 0], [1, 0, 0, 0], 4)],
)
def test_dimension(class_spatial, point, vector, dim_expected):

    object_spatial = class_spatial(point, vector)
    assert object_spatial.dimension == dim_expected


@pytest.mark.parametrize("class_spatial", [Line, Plane])
@pytest.mark.parametrize(
    "point, vector, dim, point_expected, vector_expected",
    [
        ([0, 0], [1, 0], 2, [0, 0], [1, 0]),
        ([0, 0], [1, 0], 3, [0, 0, 0], [1, 0, 0]),
        ([0, 0], [1, 0], 5, [0, 0, 0, 0, 0], [1, 0, 0, 0, 0]),
    ],
)
def test_set_dimension(
    class_spatial, point, vector, dim, point_expected, vector_expected
):

    object_spatial = class_spatial(point, vector).set_dimension(dim)

    assert object_spatial.point.is_close(point_expected)
    assert object_spatial.vector.is_close(vector_expected)
