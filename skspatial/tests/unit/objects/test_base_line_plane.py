import pytest

from skspatial.objects import Line, Plane


@pytest.mark.parametrize(
    "line_or_plane, repr_expected",
    [
        (
            Line([0, 0], [1, 0]),
            "Line(point=Point([0., 0.]), direction=Vector([1., 0.]))",
        ),
        (
            Plane([0, 0], [1, 0]),
            "Plane(point=Point([0., 0.]), normal=Vector([1., 0.]))",
        ),
        (
            Line([-1, 2, 3], [5, 4, 2]),
            "Line(point=Point([-1.,  2.,  3.]), direction=Vector([5., 4., 2.]))",
        ),
        (
            Plane([-1, 2, 3], [5, 4, 2]),
            "Plane(point=Point([-1.,  2.,  3.]), normal=Vector([5., 4., 2.]))",
        ),
    ],
)
def test_repr(line_or_plane, repr_expected):

    assert repr(line_or_plane) == repr_expected


@pytest.mark.parametrize("class_spatial", [Line, Plane])
@pytest.mark.parametrize(
    "point, vector, dim_expected",
    [([0, 0], [1, 0], 2), ([0, 0, 0], [1, 0, 0], 3), ([0, 0, 0, 0], [1, 0, 0, 0], 4)],
)
def test_get_dimension(class_spatial, point, vector, dim_expected):

    object_spatial = class_spatial(point, vector)
    assert object_spatial.get_dimension() == dim_expected


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
