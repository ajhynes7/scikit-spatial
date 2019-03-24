import hypothesis.strategies as st
import pytest
from hypothesis import given

from skspatial.objects import Point, Points, Plane
from tests.property.strategies import st_array_fixed


@given(st.data())
def test_from_points(data):

    dim = data.draw(st.sampled_from([2, 3]))

    array_a = data.draw(st_array_fixed(dim))
    array_b = data.draw(st_array_fixed(dim))
    array_c = data.draw(st_array_fixed(dim))

    arrays = [array_a, array_b, array_c]

    if not Points(arrays).are_collinear():

        # The plane must contain each point.
        plane = Plane.from_points(array_a, array_b, array_c)

        for array in arrays:

            point = Point(array).set_dimension(plane.get_dimension())
            assert plane.contains_point(point)

    else:
        # The points are collinear, so the plane is undefined.

        with pytest.raises(Exception):
            Plane.from_points(array_a, array_b, array_c)
