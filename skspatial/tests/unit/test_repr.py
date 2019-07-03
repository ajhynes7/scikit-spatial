import numpy as np
import pytest

from skspatial.objects import Point, Vector, Points, Line, Plane, Circle, Sphere


@pytest.mark.parametrize(
    "obj_spatial, repr_expected",
    [
        (Point([0]), "Point([0])"),
        (Point([0, 0]), "Point([0, 0])"),
        (Point([0, 0]), "Point([0, 0])"),
        (Point([0.5, 0]), "Point([0.5, 0. ])"),
        (Point([-11, 0]), "Point([-11,   0])"),
        (Vector([-11, 0]), "Vector([-11,   0])"),
        (Vector([-11.0, 0.0]), "Vector([-11.,   0.])"),
        (Vector([0, 0]), "Vector([0, 0])"),
        (Vector([0.5, 0]), "Vector([0.5, 0. ])"),
        (Points([[1.5, 2], [5, 3]]), "Points([[1.5, 2. ],\n        [5. , 3. ]])"),
        (Line([0, 0], [1, 0]), "Line(point=Point([0, 0]), direction=Vector([1, 0]))"),
        (
            Line([-1, 2, 3], [5, 4, 2]),
            "Line(point=Point([-1,  2,  3]), direction=Vector([5, 4, 2]))",
        ),
        (
            Line(np.zeros(2), [1, 0]),
            "Line(point=Point([0., 0.]), direction=Vector([1, 0]))",
        ),
        (Plane([0, 0], [1, 0]), "Plane(point=Point([0, 0]), normal=Vector([1, 0]))"),
        (
            Plane([-1, 2, 3], [5, 4, 2]),
            "Plane(point=Point([-1,  2,  3]), normal=Vector([5, 4, 2]))",
        ),
        (Circle([0, 0], 1), "Circle(point=Point([0, 0]), radius=1)"),
        (Circle([0, 0], 2.5), "Circle(point=Point([0, 0]), radius=2.5)"),
        (Sphere([0, 0, 0], 1), "Sphere(point=Point([0, 0, 0]), radius=1)"),
    ],
)
def test_repr(obj_spatial, repr_expected):

    assert repr(obj_spatial) == repr_expected
