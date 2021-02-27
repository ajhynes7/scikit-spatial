from hypothesis import given

from tests.property.strategies import triangles


@given(triangles(2))
def test_orthocenter(triangle):

    point_orthocenter = triangle.orthocenter()

    alt_a = triangle.altitude('A')
    alt_b = triangle.altitude('B')
    alt_c = triangle.altitude('C')

    assert all(alt.contains_point(point_orthocenter, abs_tol=0.1) for alt in [alt_a, alt_b, alt_c])
