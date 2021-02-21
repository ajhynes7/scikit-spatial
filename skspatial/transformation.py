"""Spatial transformations."""
from typing import cast
from typing import Sequence

import numpy as np

from skspatial.typing import array_like


def transform_coordinates(points: array_like, point_origin: array_like, vectors_basis: Sequence) -> np.ndarray:
    """
    Transform points into a new coordinate system.

    Parameters
    ----------
    points : (N, D) array_like
        Array of N points with dimension D.
    point_origin : (D,) array_like
        Origin of the new coordinate system.
        Array for one point with dimension D.
    vectors_basis : sequence
        Basis vectors of the new coordinate system.
        Sequence of N_bases vectors.
        Each vector is an array_like with D elements.

    Returns
    -------
    ndarray
        Coordinates in the new coordinate system.
        (N, N_bases) array.

    Examples
    --------
    >>> from skspatial.transformation import transform_coordinates

    >>> points = [[1, 2], [3, 4], [5, 6]]
    >>> vectors_basis = [[1, 0], [1, 1]]

    >>> transform_coordinates(points, [0, 0], vectors_basis)
    array([[ 1,  3],
           [ 3,  7],
           [ 5, 11]])

    >>> points = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> vectors_basis = [[1, 0, 0], [-1, 1, 0]]

    >>> transform_coordinates(points, [0, 0, 0], vectors_basis)
    array([[1, 1],
           [4, 1],
           [7, 1]])

    """
    vectors_to_points = np.subtract(points, point_origin)
    array_transformed = np.matmul(vectors_to_points, np.transpose(vectors_basis))

    return cast(np.ndarray, array_transformed)
