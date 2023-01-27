import math

import numpy as np
import pytest

from skspatial.objects import Circle
from skspatial.objects import Line
from skspatial.objects import Points

POINT_MUST_BE_2D = "The point must be 2D."
RADIUS_MUST_BE_POSITIVE = "The radius must be positive."

POINTS_MUST_BE_2D = "The points must be 2D."
POINTS_MUST_NOT_BE_COLLINEAR = "The points must not be collinear."

CIRCLE_CENTRES_ARE_COINCIDENT = "The centres of the circles are coincident."
CIRCLES_ARE_SEPARATE = "The circles do not intersect. These circles are separate."
CIRCLE_CONTAINED_IN_OTHER = "The circles do not intersect. One circle is contained within the other."


@pytest.mark.parametrize(
    ("point", "radius", "message_expected"),
    [
        ([0, 0, 0], 1, POINT_MUST_BE_2D),
        ([1, 2, 3], 1, POINT_MUST_BE_2D),
        ([0, 0], 0, RADIUS_MUST_BE_POSITIVE),
        ([0, 0], -1, RADIUS_MUST_BE_POSITIVE),
        ([0, 0], -5, RADIUS_MUST_BE_POSITIVE),
    ],
)
def test_failure(point, radius, message_expected):

    with pytest.raises(ValueError, match=message_expected):
        Circle(point, radius)


@pytest.mark.parametrize(
    ("point_a", "point_b", "point_c", "circle_expected"),
    [
        ([0, -1], [1, 0], [0, 1], Circle([0, 0], 1)),
        ([0, -2], [2, 0], [0, 2], Circle([0, 0], 2)),
        ([1, -1], [2, 0], [1, 1], Circle([1, 0], 1)),
    ],
)
def test_from_points(point_a, point_b, point_c, circle_expected):

    circle = Circle.from_points(point_a, point_b, point_c)

    assert circle.point.is_close(circle_expected.point)
    assert math.isclose(circle.radius, circle_expected.radius)


@pytest.mark.parametrize(
    ("point_a", "point_b", "point_c", "message_expected"),
    [
        ([1, 0, 0], [1, 0], [1, 0], POINTS_MUST_BE_2D),
        ([1, 0], [1, 0, 0], [1, 0], POINTS_MUST_BE_2D),
        ([1, 0], [0, 0], [1, 0, 1], POINTS_MUST_BE_2D),
        ([0, 0], [0, 0], [0, 0], POINTS_MUST_NOT_BE_COLLINEAR),
        ([0, 0], [1, 1], [2, 2], POINTS_MUST_NOT_BE_COLLINEAR),
    ],
)
def test_from_points_failure(point_a, point_b, point_c, message_expected):

    with pytest.raises(ValueError, match=message_expected):
        Circle.from_points(point_a, point_b, point_c)


@pytest.mark.parametrize(
    ("radius", "circumference_expected", "area_expected"),
    [
        (1, 2 * np.pi, np.pi),
        (2, 4 * np.pi, 4 * np.pi),
        (3, 6 * np.pi, 9 * np.pi),
        (4.5, 9 * np.pi, 20.25 * np.pi),
        (10, 20 * np.pi, 100 * np.pi),
    ],
)
def test_circumference_area(radius, circumference_expected, area_expected):

    circle = Circle([0, 0], radius)

    assert math.isclose(circle.circumference(), circumference_expected)
    assert math.isclose(circle.area(), area_expected)


@pytest.mark.parametrize(
    ("circle", "point", "dist_expected"),
    [
        (Circle([0, 0], 1), [0, 0], 1),
        (Circle([0, 0], 1), [0.5, 0], 0.5),
        (Circle([0, 0], 1), [1, 0], 0),
        (Circle([0, 0], 1), [0, 1], 0),
        (Circle([0, 0], 1), [-1, 0], 0),
        (Circle([0, 0], 1), [0, -1], 0),
        (Circle([0, 0], 1), [2, 0], 1),
        (Circle([0, 0], 1), [1, 1], math.sqrt(2) - 1),
        (Circle([1, 1], 1), [0, 0], math.sqrt(2) - 1),
        (Circle([0, 0], 2), [0, 5], 3),
    ],
)
def test_distance_point(circle, point, dist_expected):

    assert math.isclose(circle.distance_point(point), dist_expected)


@pytest.mark.parametrize(
    ("circle", "point", "bool_expected"),
    [
        (Circle([0, 0], 1), [1, 0], True),
        (Circle([0, 0], 1), [0, 1], True),
        (Circle([0, 0], 1), [-1, 0], True),
        (Circle([0, 0], 1), [0, -1], True),
        (Circle([0, 0], 1), [0, 0], False),
        (Circle([0, 0], 1), [1, 1], False),
        (Circle([0, 0], 2), [1, 0], False),
        (Circle([1, 0], 1), [1, 0], False),
        (Circle([0, 0], math.sqrt(2)), [1, 1], True),
    ],
)
def test_contains_point(circle, point, bool_expected):

    assert circle.contains_point(point) == bool_expected


@pytest.mark.parametrize(
    ("circle", "point", "point_expected"),
    [
        (Circle([0, 0], 1), [1, 0], [1, 0]),
        (Circle([0, 0], 1), [2, 0], [1, 0]),
        (Circle([0, 0], 1), [-2, 0], [-1, 0]),
        (Circle([0, 0], 1), [0, 2], [0, 1]),
        (Circle([0, 0], 1), [0, -2], [0, -1]),
        (Circle([0, 0], 5), [0, -2], [0, -5]),
        (Circle([0, 1], 5), [0, -2], [0, -4]),
        (Circle([0, 0], 1), [1, 1], math.sqrt(2) / 2 * np.ones(2)),
        (Circle([0, 0], 2), [1, 1], math.sqrt(2) * np.ones(2)),
    ],
)
def test_project_point(circle, point, point_expected):

    point_projected = circle.project_point(point)
    assert point_projected.is_close(point_expected)


@pytest.mark.parametrize(
    ("circle", "point"),
    [
        (Circle([0, 0], 1), [0, 0]),
        (Circle([0, 0], 5), [0, 0]),
        (Circle([7, -1], 5), [7, -1]),
    ],
)
def test_project_point_failure(circle, point):

    message_expected = "The point must not be the center of the circle or sphere."

    with pytest.raises(ValueError, match=message_expected):
        circle.project_point(point)


@pytest.mark.parametrize(
    ("points", "circle_expected"),
    [
        ([[1, 1], [2, 2], [3, 1]], Circle(point=[2, 1], radius=1)),
        ([[2, 0], [-2, 0], [0, 2]], Circle(point=[0, 0], radius=2)),
        ([[1, 0], [0, 1], [1, 2]], Circle(point=[1, 1], radius=1)),
    ],
)
def test_best_fit(points, circle_expected):

    points = Points(points)
    circle_fit = Circle.best_fit(points)

    assert circle_fit.point.is_close(circle_expected.point, abs_tol=1e-9)
    assert math.isclose(circle_fit.radius, circle_expected.radius)


@pytest.mark.parametrize(
    ("points", "message_expected"),
    [
        ([[1, 0, 0], [-1, 0, 0], [0, 1, 0]], "The points must be 2D."),
        ([[2, 0], [-2, 0]], "There must be at least 3 points."),
        ([[0, 0], [1, 1], [2, 2]], "The points must not be collinear."),
    ],
)
def test_best_fit_failure(points, message_expected):

    with pytest.raises(ValueError, match=message_expected):
        Circle.best_fit(points)


@pytest.mark.parametrize(
    ("circle_a", "circle_b", "point_a_expected", "point_b_expected"),
    [
        (Circle([0, 0], 1), Circle([2, 0], 1), [1, 0], [1, 0]),
        (Circle([1, 0], 1), Circle([3, 0], 1), [2, 0], [2, 0]),
        (Circle([0, 0], 2), Circle([1, 0], 1), [2, 0], [2, 0]),
        (Circle([0, 0], 2), Circle([3, 0], 1), [2, 0], [2, 0]),
        (Circle([0, 0], 1), Circle([0, 2], 1), [0, 1], [0, 1]),
        (Circle([0, 0], 2), Circle([2, 0], 1), [1.75, math.sqrt(0.9375)], [1.75, -math.sqrt(0.9375)]),
        (Circle([0, 0], 1), Circle([1, 0], 1), [0.5, math.sqrt(3) / 2], [0.5, -math.sqrt(3) / 2]),
    ],
)
def test_intersect_circle(circle_a, circle_b, point_a_expected, point_b_expected):

    point_a, point_b = circle_a.intersect_circle(circle_b)

    assert point_a.is_close(point_a_expected)
    assert point_b.is_close(point_b_expected)


@pytest.mark.parametrize(
    ("circle_a", "circle_b", "message_expected"),
    [
        (Circle([0, 0], 1), Circle([0, 0], 1), CIRCLE_CENTRES_ARE_COINCIDENT),
        (Circle([0, 0], 1), Circle([0, 0], 2), CIRCLE_CENTRES_ARE_COINCIDENT),
        (Circle([4, -3], 1), Circle([4, -3], 1), CIRCLE_CENTRES_ARE_COINCIDENT),
        (Circle([0, 0], 3), Circle([1, 0], 1), CIRCLE_CONTAINED_IN_OTHER),
        (Circle([0, 0], 1), Circle([0, 3], 1), CIRCLES_ARE_SEPARATE),
        (Circle([1, 1], 1), Circle([5, 0], 1), CIRCLES_ARE_SEPARATE),
    ],
)
def test_intersect_circle_failure(circle_a, circle_b, message_expected):

    with pytest.raises(ValueError, match=message_expected):
        circle_a.intersect_circle(circle_b)


@pytest.mark.parametrize(
    ("circle", "line", "point_a_expected", "point_b_expected"),
    [
        (Circle([0, 0], 1), Line([0, 0], [1, 0]), [-1, 0], [1, 0]),
        (Circle([0, 0], 1), Line([0, 0], [0, 1]), [0, -1], [0, 1]),
        (Circle([0, 0], 1), Line([0, 1], [1, 0]), [0, 1], [0, 1]),
        (
            Circle([0, 0], 1),
            Line([0, 0.5], [1, 0]),
            [-math.sqrt(3) / 2, 0.5],
            [math.sqrt(3) / 2, 0.5],
        ),
        (Circle([1, 0], 1), Line([0, 0], [1, 0]), [0, 0], [2, 0]),
        (Circle([1.5, 0], 1), Line([0, 0], [1, 0]), [0.5, 0], [2.5, 0]),
    ],
)
def test_intersect_line(circle, line, point_a_expected, point_b_expected):

    point_a, point_b = circle.intersect_line(line)

    assert point_a.is_close(point_a_expected)
    assert point_b.is_close(point_b_expected)


@pytest.mark.parametrize(
    ("circle", "line"),
    [
        (Circle([0, 0], 1), Line([0, 2], [1, 0])),
        (Circle([0, 0], 1), Line([0, -2], [1, 0])),
        (Circle([0, 0], 1), Line([2, 0], [0, 1])),
        (Circle([0, 0], 1), Line([3, 0], [1, 1])),
        (Circle([0, 0], 0.5), Line([0, 1], [1, 1])),
        (Circle([0, 1], 0.5), Line([0, 0], [1, 0])),
        (Circle([5, 2], 1), Line([2, -1], [1, 0])),
    ],
)
def test_intersect_line_failure(circle, line):

    message_expected = "The line does not intersect the circle."

    with pytest.raises(ValueError, match=message_expected):
        circle.intersect_line(line)
