import pytest

from skspatial.objects import Point, Points, Vector, Line, Plane


@pytest.mark.parametrize(
    "class_spatial, objects, objects_expected",
    [
        (
            Point,
            [[0, 0, 0], [1, 1], Vector([1, 2, 3, 4])],
            [Point([0, 0, 0, 0]), Point([1, 1, 0, 0]), Vector([1, 2, 3, 4])],
        ),
        (
            Vector,
            [Plane([0, 0], [1, 1]), Point([1, 0]), [1, 2, 3]],
            [Plane([0, 0, 0], [1, 1, 0]), Point([1, 0, 0]), Vector([1, 2, 3])],
        ),
        (
            Point,
            [Line([0, 0], [1, 0]), [0, 1], Points([[1, 2, 3]])],
            [Line([0, 0, 0], [1, 0, 0]), Point([0, 1, 0]), Points([[1, 2, 3]])],
        ),
        (
            Vector,
            [Points([[1, 2], [3, 4]]), [1, 2, 3, 4]],
            [Points([[1, 2, 0, 0], [3, 4, 0, 0]]), Vector([1, 2, 3, 4])],
        ),
        (
            Points,
            [Points([[1, 2], [3, 4]]), [[1, 2, 3], [1, 2, 3]]],
            [Points([[1, 2, 0], [3, 4, 0]]), Points([[1, 2, 3], [1, 2, 3]])],
        ),
    ],
)
def test_normalize_dimension(class_spatial, objects, objects_expected):

    objects_normalized = class_spatial.normalize_dimension(*objects)

    assert all(
        a.is_close(b) and isinstance(a, type(b))
        for a, b in zip(objects_normalized, objects_expected)
    )
