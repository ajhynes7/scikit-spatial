import numpy as np
import pytest

from skspatial.objects import Point, Vector, Line


@pytest.mark.parametrize(
    "array_point, array_point_line, array_vector_line, \
     array_point_expected, dist_expected",
    [
        ([0, 5], [0, 0], [0, 1], [0, 5], 0),
        ([0, 5], [0, 0], [0, 100], [0, 5], 0),
        ([1, 5], [0, 0], [0, 100], [0, 5], 1),
        ([0, 1], [0, 0], [1, 1], [0.5, 0.5], np.sqrt(2) / 2),
        ([1, 0], [0, 0], [1, 1], [0.5, 0.5], np.sqrt(2) / 2),
        ([0, 2], [0, 0], [1, 1], [1, 1], np.sqrt(2)),
        ([-15, 5], [0, 0], [0, 100], [0, 5], 15),
        ([50, 10], [1, -5], [0, 3], [1, 10], 49),
    ],
)
def test_point_line(
    array_point,
    array_point_line,
    array_vector_line,
    array_point_expected,
    dist_expected,
):
    """Test functions related to a point and a line."""
    point = Point(array_point)
    point_expected = Point(array_point_expected)

    line = Line(Point(array_point_line), Vector(array_vector_line))

    point_projected = line.project_point(point)
    distance = line.distance_point(point)

    assert point_projected.is_close(point_expected)
    assert np.isclose(distance, dist_expected)
