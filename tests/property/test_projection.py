import hypothesis.strategies as st
import numpy as np
import pytest
from hypothesis import given

from skspatial.objects import Vector
from tests.strategies import st_point, st_line, st_plane, TOLERANCE


@pytest.mark.parametrize('name_object', ['line', 'plane'])
@given(data=st.data())
def test_point_line_plane(data, name_object):

    point = data.draw(st_point())

    if name_object == 'line':
        object_ = data.draw(st_line())
    elif name_object == 'plane':
        object_ = data.draw(st_plane())

    point_projected = object_.project(point)

    # The projected point should lie on the line/plane.
    assert object_.contains(point_projected, atol=TOLERANCE)

    # The vector from the point to its projection
    # should be perpendicular to the line/plane.
    vector_projection = Vector.from_points(point, point_projected)

    # The distance from the point to its projection
    # should equal the distance to the line/plane.
    distance_projection = vector_projection.magnitude

    distance_to_object = object_.distance(point)
    assert np.isclose(distance_to_object, distance_projection)

    # The distance to the line/plane is zero <==> The point is on the line/plane.
    distance_is_zero = np.isclose(distance_to_object, 0)

    assert distance_is_zero == object_.contains(point)
