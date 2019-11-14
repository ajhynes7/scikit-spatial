from dataclasses import dataclass
from math import atan, degrees, isclose, radians, sqrt

import pytest

from skspatial.objects import Triangle


@dataclass
class TriangleTester:
    """Triangle object for unit testing."""

    points: tuple

    area: float
    perimeter: float

    lengths: tuple
    angles: tuple

    normal: list
    centroid: list
    orthocenter: list

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
    ),
]


@pytest.mark.parametrize('test_case', list_test_cases)
def test_triangle(test_case):

    triangle = Triangle(*test_case.points)

    assert triangle.area() == test_case.area
    assert triangle.perimeter() == test_case.perimeter

    lengths_a = triangle.multiple('length', 'abc')
    lengths_b = test_case.lengths
    assert all([isclose(a, b) for a, b in zip(lengths_a, lengths_b)])

    angles_a = triangle.multiple('angle', 'ABC')
    angles_b = tuple(map(radians, test_case.angles))
    assert all(isclose(a, b, abs_tol=1e-3) for a, b in zip(angles_a, angles_b))

    assert triangle.normal().is_close(test_case.normal)
    assert triangle.centroid().is_close(test_case.centroid)
    assert triangle.orthocenter().is_close(test_case.orthocenter)

    assert triangle.classify() == test_case.classification
    assert triangle.is_right() == test_case.is_right
