import hypothesis.strategies as st
from hypothesis import assume, given

from skspatial.objects import Points, Line, Plane
from .constants import ATOL
from .strategies import st_array_fixed, st_line, st_plane


@given(st.data())
def test_best_fit_line(data):

    n_points = data.draw(st.integers(min_value=2, max_value=5))
    dim = data.draw(st.integers(min_value=2, max_value=4))

    points = Points([data.draw(st_array_fixed(dim)) for _ in range(n_points)])
    assume(not points.are_concurrent(tol=ATOL))

    line = data.draw(st_line(dim))
    line_fit = Line.best_fit(points)

    error_line = line.sum_squares(points)
    error_fit = line_fit.sum_squares(points)

    assert error_fit <= error_line + ATOL


@given(st.data())
def test_best_fit_plane(data):

    n_points = data.draw(st.integers(min_value=3, max_value=5))

    points = Points([data.draw(st_array_fixed(3)) for _ in range(n_points)])
    assume(not points.are_collinear(tol=ATOL))

    plane_fit = Plane.best_fit(points)

    # The best fit plane could have a higher dimension than the points
    # (e.g., 2D points have a 3D plane of best fit).
    # So, we convert the points dimension to that of the best fit plane.
    dim_fit = plane_fit.dimension
    points = points.set_dimension(dim_fit)

    plane = data.draw(st_plane(dim_fit))

    error_plane = plane.sum_squares(points)
    error_fit = plane_fit.sum_squares(points)

    assert error_fit <= error_plane + ATOL
