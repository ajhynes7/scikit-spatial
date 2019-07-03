import hypothesis.strategies as st
import numpy as np
import pytest
from hypothesis import given

from skspatial._constants import ATOL
from skspatial.objects import Vector
from skspatial.tests.property.strategies import (
    DIM_MAX,
    DIM_MIN,
    st_array_fixed,
    st_line,
    st_plane,
)


@pytest.mark.parametrize('name_object', ['line', 'plane'])
@given(data=st.data())
def test_project_point(data, name_object):
    """Test projecting a point onto a line or plane."""

    dim = data.draw(st.integers(min_value=DIM_MIN, max_value=DIM_MAX))

    array = data.draw(st_array_fixed(dim))

    if name_object == 'line':
        line_or_plane = data.draw(st_line(dim))
    elif name_object == 'plane':
        line_or_plane = data.draw(st_plane(dim))

    point_projected = line_or_plane.project_point(array)

    # The projected point should lie on the line/plane.
    assert line_or_plane.contains_point(point_projected, atol=ATOL)

    # The vector from the point to its projection
    # should be perpendicular to the line/plane.
    vector_projection = Vector.from_points(array, point_projected)

    # The distance from the point to its projection
    # should equal the distance to the line/plane.
    distance_projection = vector_projection.norm()
    distance_to_object = abs(line_or_plane.distance_point(array))
    assert np.isclose(distance_to_object, distance_projection)

    # The distance of the projection should be the
    # shortest distance from the point to the object.
    distance_points = line_or_plane.point.distance_point(array)
    assert distance_projection < distance_points or np.isclose(
        distance_projection, distance_points
    )
