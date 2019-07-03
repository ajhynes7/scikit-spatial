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
