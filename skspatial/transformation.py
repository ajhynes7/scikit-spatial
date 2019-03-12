"""Transformations of spatial entities."""

import numpy as np
from dpcontracts import require, ensure, types

from skspatial.objects import Point


@types(points=np.ndarray)
@require("The input must be a 2D array of points", lambda args: args.points.ndim == 2)
@ensure("The output length must be the input width.", lambda args, result: result.size == args.points.shape[1])
@ensure("The output must be a 1D array of points", lambda _, result: result.ndim == 1)
def get_centroid(points):
    """
    Return the centroid of a set of points.

    Parameters
    ----------
    points : ndarray
         (n, d) array of n points.

    Returns
    -------
    ndarray
        Centroid of the points.

    Examples
    --------
    >>> import numpy as np
    >>> from skspatial.transformation import get_centroid

    >>> points = np.array([[1, 2, 3], [2, 2, 3]])
    >>> get_centroid(points)
    array([1.5, 2. , 3. ])

    """
    return points.mean(axis=0)


@types(points=np.ndarray)
@require("The input must be a 2D array of points", lambda args: args.points.ndim == 2)
@ensure("The centered points must have the input shape", lambda args, result: result[0].shape == args.points.shape)
@ensure(
    "The centroid length must be the dimension of the points.", lambda _, result: result[1].size == result[0].shape[1]
)
@ensure("The centroid must be a 1D array.", lambda _, result: result[1].ndim == 1)
def mean_center(points):
    """
    Mean-center a set of points.

    The centroid of the points is subtracted from the points.

    Parameters
    ----------
    points : ndarray
         (n, d) array of n points.

    Returns
    -------
    points_centered : ndarray
        (n, d) array of mean-centered points.
    centroid : ndarray
        (d,) array.

    Examples
    --------
    >>> import numpy as np
    >>> from skspatial.transformation import mean_center

    >>> points = np.array([[4, 4, 4], [2, 2, 2]])
    >>> points_centered, centroid = mean_center(points)

    >>> points_centered
    array([[ 1.,  1.,  1.],
           [-1., -1., -1.]])

    >>> centroid
    array([3., 3., 3.])

    """
    centroid = get_centroid(points)
    points_centered = points - centroid

    return points_centered, centroid


@ensure("The output is an ndarray.", lambda _, result: isinstance(result, np.ndarray))
def normalize_dimension(seq_points):
    """
    Normalize the dimension of a set of points.

    Each point is converted to a `Point` object.
    The Point objects are then stacked into one ndarray.

    Parameters
    ----------
    seq_points : sequence
         Sequence of array_like objects.

    Returns
    -------
    ndarray
        Each row corresponds to a point in the input sequence.

    Examples
    --------
    >>> from skspatial.transformation import normalize_dimension

    >>> seq_points = ([1], [1, 2], [1, 2, 3])

    >>> normalize_dimension(seq_points)
    array([[1., 0., 0.],
           [1., 2., 0.],
           [1., 2., 3.]])

    """
    list_points = [Point(x) for x in seq_points]

    return np.vstack(list_points)
