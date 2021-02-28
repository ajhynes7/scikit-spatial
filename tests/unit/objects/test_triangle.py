from dataclasses import dataclass
from math import atan
from math import degrees
from math import isclose
from math import radians
from math import sqrt

import pytest

from skspatial.objects import Line
from skspatial.objects import Triangle
from skspatial.typing import array_like


@dataclass
class TriangleTester:
    """Triangle object for unit testing."""

    points: tuple

    area: float
    perimeter: float

    lengths: tuple
    angles: tuple
    altitudes: tuple

    normal: array_like
    centroid: array_like
    orthocenter: array_like

    classification: str
    is_right: bool


list_test_cases = [
    TriangleTester(
        points=[[0, 0], [1, 0], [0, 1]],
        area=0.5,
        perimeter=2 + sqrt(2),
        lengths=(sqrt(2), 1, 1),
        angles=(90, 45, 45),
        centroid=[1 / 3, 1 / 3],
        orthocenter=[0, 0],
        normal=[0, 0, 1],
        classification='isosceles',
        is_right=True,
        altitudes=(Line([0, 0], [0.5, 0.5]), Line([1, 0], [-1, 0]), Line([0, 1], [0, -1])),
    ),
    TriangleTester(
        points=[[0, 0], [1, 1], [2, 0]],
        area=1,
        perimeter=2 + 2 * sqrt(2),
        lengths=(sqrt(2), 2, sqrt(2)),
        angles=(45, 90, 45),
        centroid=[1, 1 / 3],
        orthocenter=[1, 1],
        normal=[0, 0, -2],
        classification='isosceles',
        is_right=True,
        altitudes=(Line([0, 0], [1, 1]), Line([1, 1], [0, -1]), Line([2, 0], [-1, 1])),
    ),
    TriangleTester(
        points=[[0, 0], [1, 0], [0.5, sqrt(3) / 2]],
        area=sqrt(3) / 4,
        perimeter=3,
        lengths=(1, 1, 1),
        angles=(60, 60, 60),
        centroid=[0.5, sqrt(3) / 6],
        orthocenter=[0.5, sqrt(3) / 6],
        normal=[0, 0, sqrt(3) / 2],
        classification='equilateral',
        is_right=False,
        altitudes=(
            Line([0, 0], [0.75, sqrt(3) / 4]),
            Line([1, 0], [-0.75, sqrt(3) / 4]),
            Line([0.5, sqrt(3) / 2], [0, -sqrt(3) / 2]),
        ),
    ),
    TriangleTester(
        points=[[0, 0], [1, 0], [0, 2]],
        area=1,
        perimeter=3 + sqrt(5),
        lengths=(sqrt(5), 2, 1),
        angles=(90, degrees(atan(2)), degrees(atan(1 / 2))),
        centroid=[1 / 3, 2 / 3],
        orthocenter=[0, 0],
        normal=[0, 0, 2],
        classification='scalene',
        is_right=True,
        altitudes=(Line([0, 0], [0.8, 0.4]), Line([1, 0], [-1, 0]), Line([0, 2], [0, -2])),
    ),
    TriangleTester(
        points=[[0, 0], [3, 0], [0, 4]],
        area=6,
        perimeter=12,
        lengths=(5, 4, 3),
        angles=(90, degrees(atan(4 / 3)), degrees(atan(3 / 4))),
        centroid=[1, 4 / 3],
        orthocenter=[0, 0],
        normal=[0, 0, 12],
        classification='scalene',
        is_right=True,
        altitudes=(Line([0, 0], [1.92, 1.44]), Line([3, 0], [-3, 0]), Line([0, 4], [0, -4])),
    ),
]


@pytest.mark.parametrize('test_case', list_test_cases)
def test_triangle(test_case):

    triangle = Triangle(*test_case.points)

    assert triangle.area() == test_case.area
    assert triangle.perimeter() == test_case.perimeter

    points_a = triangle.multiple('point', 'ABC')
    points_b = test_case.points
    assert all(a.is_equal(b) for a, b in zip(points_a, points_b))

    lengths_a = triangle.multiple('length', 'abc')
    lengths_b = test_case.lengths
    assert all(isclose(a, b) for a, b in zip(lengths_a, lengths_b))

    angles_a = triangle.multiple('angle', 'ABC')
    angles_b = tuple(map(radians, test_case.angles))
    assert all(isclose(a, b, abs_tol=1e-3) for a, b in zip(angles_a, angles_b))

    assert triangle.normal().is_close(test_case.normal)
    assert triangle.centroid().is_close(test_case.centroid)
    assert triangle.orthocenter().is_close(test_case.orthocenter)

    altitudes_a = triangle.multiple('altitude', 'ABC')
    altitudes_b = test_case.altitudes
    print(altitudes_a, altitudes_b)
    assert all(a.is_close(b, abs_tol=1e-3) for a, b in zip(altitudes_a, altitudes_b))

    assert triangle.classify() == test_case.classification
    assert triangle.is_right() == test_case.is_right


@pytest.mark.parametrize(
    ("array_a", "array_b", "array_c"),
    [([1], [1, 0], [1, 0]), ([1, 0, 0], [1, 0], [1, 0]), ([1, 0], [1, 0], [1, 0, 0]), ([1, 0, 0], [1, 0], [1, 0, 0])],
)
def test_failure_different_dimensions(array_a, array_b, array_c):

    with pytest.raises(ValueError, match="The points must have the same dimension."):
        Triangle(array_a, array_b, array_c)


@pytest.mark.parametrize(
    ("array_a", "array_b", "array_c"),
    [
        ([1], [2], [3]),
        ([1, 0], [1, 0], [1, 0]),
        ([1, 2, 3], [1, 2, 3], [1, 2, 3]),
        ([1, 2, 3], [1, 2, 3], [2, 3, -10]),  # Two points are the same.
        ([1, 2, 3], [4, 5, 6], [7, 8, 9]),
        ([1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]),
    ],
)
def test_failure_collinear_points(array_a, array_b, array_c):

    with pytest.raises(ValueError, match="The points must not be collinear."):
        Triangle(array_a, array_b, array_c)


@pytest.fixture()
def basic_triangle():

    return Triangle([0, 0], [0, 1], [1, 0])


@pytest.mark.parametrize("string", ['a', 'b', 'c', 'd', 'D'])
def test_failure_point(basic_triangle, string):

    message = "The vertex must be 'A', 'B', or 'C'."

    with pytest.raises(ValueError, match=message):
        basic_triangle.point(string)

    with pytest.raises(ValueError, match=message):
        basic_triangle.angle(string)

    with pytest.raises(ValueError, match=message):
        basic_triangle.altitude(string)


@pytest.mark.parametrize("string", ['A', 'B', 'C', 'D'])
def test_failure_line(basic_triangle, string):

    message = "The side must be 'a', 'b', or 'c'."

    with pytest.raises(ValueError, match=message):
        basic_triangle.line(string)

    with pytest.raises(ValueError, match=message):
        basic_triangle.length(string)
