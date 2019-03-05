import hypothesis.strategies as st
import numpy as np
import pytest
from hypothesis import given

from skspatial.constants import ATOL
from skspatial.objects import Vector
from tests.property.strategies import st_point, st_line, st_plane


@pytest.mark.parametrize('name_object', ['line', 'plane'])
@given(data=st.data())
def test_project_point(data, name_object):
    """Test projecting a point onto a line or plane."""
    point = data.draw(st_point())

    if name_object == 'line':
        line_or_plane = data.draw(st_line())
    elif name_object == 'plane':
        line_or_plane = data.draw(st_plane())

    point_projected = line_or_plane.project_point(point)

    # The projected point should lie on the line/plane.
    assert line_or_plane.contains_point(point_projected, atol=ATOL)

    # The vector from the point to its projection
    # should be perpendicular to the line/plane.
    vector_projection = Vector.from_points(point, point_projected)

    # The distance from the point to its projection
    # should equal the distance to the line/plane.
    distance_projection = vector_projection.magnitude
    distance_to_object = abs(line_or_plane.distance_point(point))
    assert np.isclose(distance_to_object, distance_projection)

    # The distance to the line/plane is zero <==> The point is on the line/plane.
    is_distance_zero = np.isclose(distance_to_object, 0)
    assert is_distance_zero == line_or_plane.contains_point(point)

    # The distance of the projection should be the
    # shortest distance from the point to the object.
    distance_points = point.distance_point(line_or_plane.point)
    assert distance_projection < distance_points or np.isclose(
        distance_projection, distance_points
    )
