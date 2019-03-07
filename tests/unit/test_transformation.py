import numpy as np
import pytest

from skspatial.objects import Point, Vector
from skspatial.transformation import array_to_objects, objects_to_array


@pytest.mark.parametrize(
    "list_arrays, array_expected",
    [
        ([[0]], np.array([[0, 0, 0]])),
        ([[0, 1], [5.3, 2, -1]], np.array([[0, 1, 0], [5.3, 2, -1]])),
        (
            [[-1.1], [10.5, 2, 3], [5, 2, 1]],
            np.array([[-1.1, 0, 0], [10.5, 2, 3], [5, 2, 1]]),
        ),
    ],
)
@pytest.mark.parametrize("class_spatial", [Point, Vector])
def test_objects_to_array(list_arrays, class_spatial, array_expected):

    # Convert each array to a Point or Vector.
    objects = [class_spatial(x) for x in list_arrays]

    # Convert sequence of objects to a single numpy array.
    array = objects_to_array(objects)
    assert np.array_equal(array, array_expected)

    # Convert back to sequence of objects
    assert objects == list(array_to_objects(array, class_spatial))
