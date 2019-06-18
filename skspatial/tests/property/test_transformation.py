import hypothesis.strategies as st
import numpy as np
from hypothesis import given
from numpy.testing import assert_array_almost_equal

from skspatial.objects import Points
from skspatial.tests.property.strategies import st_array_fixed, st_line, st_points


@given(st.data())
def test_mean_center(data):

    dim = data.draw(st.integers(min_value=2, max_value=4))
    points = data.draw(st_points(dim))

    points_centered, _ = points.mean_center()

    # The centroid of the centered points should be the origin.
    centroid_new = points_centered.centroid()
    origin = np.zeros(points.dimension)

    assert_array_almost_equal(centroid_new, origin)


@given(st.data())
def test_transform_points_line(data):

    n_points = data.draw(st.integers(min_value=2, max_value=5))
    dim = data.draw(st.integers(min_value=2, max_value=4))

    points = Points([data.draw(st_array_fixed(dim)) for _ in range(n_points)])
    line = data.draw(st_line(dim))

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
