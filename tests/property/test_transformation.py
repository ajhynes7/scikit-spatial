import hypothesis.strategies as st
import numpy as np
from hypothesis import assume
from hypothesis import given
from numpy.testing import assert_array_almost_equal

from tests.property.constants import ATOL
from tests.property.strategies import lines
from tests.property.strategies import multi_points


@given(st.data())
def test_mean_center(data):

    dim = data.draw(st.integers(min_value=2, max_value=5))
    points = data.draw(multi_points(dim))

    points_centered = points.mean_center()

    # The centroid of the centered points should be the origin.
    centroid_new = points_centered.centroid()
    origin = np.zeros(points.dimension)

    assert_array_almost_equal(centroid_new, origin)


@given(st.data())
def test_normalize_distance(data):

    dim = data.draw(st.integers(min_value=2, max_value=5))
    points = data.draw(multi_points(dim))

    assume(not np.all(points == 0))

    points_transformed = points.normalize_distance()
    distances_to_points = np.linalg.norm(points_transformed, axis=1)

    assert np.logical_and(distances_to_points >= 0, distances_to_points <= 1 + ATOL).all()


@given(st.data())
def test_transform_points_line(data):

    dim = data.draw(st.integers(min_value=2, max_value=5))
    points = data.draw(multi_points(dim))

    line = data.draw(lines(dim))

    # Transform the points into 1D coordinates.
    coordinates = line.transform_points(points)

    # Project the points onto the line.
    points_projected = np.apply_along_axis(line.project_point, 1, points)

    # Find the signed distances from the line point to the projected points.
    vectors_to_projections = points_projected - line.point
    direction_unit = line.direction.unit()
    distances_signed = np.apply_along_axis(direction_unit.dot, 1, vectors_to_projections)

    # The coordinates from the transformation should be equal to the signed distances.
    assert_array_almost_equal(distances_signed, coordinates)
