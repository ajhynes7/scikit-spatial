"""Transformations of spatial objects."""

import numpy as np
from dpcontracts import ensure, types


@ensure("The output must be an ndarray.", lambda _, result: isinstance(result, np.ndarray))
@ensure("The output must have a row for each object.", lambda args, result: result.shape[0] == len(args.objects))
def objects_to_array(objects):
    """
    Convert single-array objects (Point/Vector) to a numpy array.

    Parameters
    ----------
    objects : sequence
        Sequence of objects, such as points or vectors.

    Returns
    -------
    ndarray
        Each row corresponds to an object in the input sequence.

    Examples
    --------
    >>> from skspatial.objects import Point, Vector
    >>> from skspatial.transformation import objects_to_array

    >>> points = [Point([1, 1]), Point([2, 3]), Point([5, 3])]
    >>> array = objects_to_array(points)

    >>> array
    array([[1., 1., 0.],
           [2., 3., 0.],
           [5., 3., 0.]])

    >>> array.shape
    (3, 3)

    >>> vectors = [Vector([5, 2]), Vector([1, 5])]
    >>> array = objects_to_array(vectors)

    >>> array
    array([[5., 2., 0.],
           [1., 5., 0.]])

    >>> array.shape
    (2, 3)

    """
    return np.stack([obj.array for obj in objects])


@types(array=np.ndarray, class_spatial=type)
def array_to_objects(array, class_spatial):
    """
    Convert a numpy array to single-array spatial objects (Point/Vector).

    Parameters
    ----------
    array : ndarray
        Input numpy array.
    class_spatial : type
        Class of spatial object (Point or Vector)

    Yields
    ------
        Spatial object (point or vector).
        Each spatial object corresponds to a row of the input array.

    Examples
    --------
    >>> from skspatial.objects import Point, Vector
    >>> import numpy as np

    >>> array = np.array([[1, 2, 3], [4, 5, 6]])
    >>> list(array_to_objects(array, Point))
    [Point([1. 2. 3.]), Point([4. 5. 6.])]

    >>> list(array_to_objects(array, Vector))
    [Vector([1. 2. 3.]), Vector([4. 5. 6.])]

    """
    for row in array:
        yield class_spatial(row)
