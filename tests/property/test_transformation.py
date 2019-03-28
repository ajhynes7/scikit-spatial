import numpy as np
from hypothesis import given
from numpy.testing import assert_array_almost_equal

from tests.property.strategies import consistent_dim, st_line, st_points


@given(consistent_dim([st_line, st_points]))
def test_transform_points_line(objs):

    line, points = objs

    # Transform the points into 1D coordinates.
    coordinates = line.transform_points(points)

    # Project the points onto the line.
    points_projected = np.apply_along_axis(line.project_point, 1, points)

    # Find the signed distances from the line point to the projected points.
    vectors_to_projections = points_projected - line.point
    direction_unit = line.direction.unit()
    distances_signed = np.apply_along_axis(
        direction_unit.dot, 1, vectors_to_projections
    )

    # The coordinates from the transformation should be equal to the signed distances.
    assert_array_almost_equal(distances_signed, coordinates)
