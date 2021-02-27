import hypothesis.strategies as st
from hypothesis import assume
from hypothesis import given

from skspatial.objects import Line
from skspatial.objects import Plane
from skspatial.objects import Points
from tests.property.constants import ATOL
from tests.property.strategies import arrays_fixed
from tests.property.strategies import lines
from tests.property.strategies import planes


@given(st.data())
def test_best_fit_line(data):

    n_points = data.draw(st.integers(min_value=2, max_value=5))
    dim = data.draw(st.integers(min_value=2, max_value=4))

    points = Points([data.draw(arrays_fixed(dim)) for _ in range(n_points)])
    assume(not points.are_concurrent(tol=ATOL))

    line = data.draw(lines(dim))
    line_fit = Line.best_fit(points)

    error_line = line.sum_squares(points)
    error_fit = line_fit.sum_squares(points)

    assert error_fit <= error_line + ATOL


@given(st.data())
def test_best_fit_plane(data):

    n_points = data.draw(st.integers(min_value=3, max_value=5))

    points = Points([data.draw(arrays_fixed(3)) for _ in range(n_points)])
    assume(not points.are_collinear(tol=ATOL))

    plane_fit = Plane.best_fit(points)

    # The best fit plane could have a higher dimension than the points
    # (e.g., 2D points have a 3D plane of best fit).
    # So, we convert the points dimension to that of the best fit plane.
    dim_fit = plane_fit.dimension
    points = points.set_dimension(dim_fit)

    plane = data.draw(planes(dim_fit))

    error_plane = plane.sum_squares(points)
    error_fit = plane_fit.sum_squares(points)

    assert error_fit <= error_plane + ATOL
