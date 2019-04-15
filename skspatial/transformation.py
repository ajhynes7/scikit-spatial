"""Spatial transformations."""

import numpy as np


def transform_coordinates(points, point_origin, vectors_basis):
    """
    Transform points into a new coordinate system.

    Parameters
    ----------
    points : array_like
        (n, d) array of n points with dimension d.
    point_origin : array_like
        Origin of the new coordinate system.
        (d,) array for one point with dimension d.
    vectors_basis : sequence
        Basis vectors of the new coordinate system.
        Sequence of n_bases vectors.
        Each vector is an array_like with d elements.

    Returns
    -------
    ndarray
        Coordinates in the new coordinate system.
        (n, n_bases) array.

    Examples
    --------
    >>> from skspatial.transformation import transform_coordinates

    >>> points = [[1, 2], [3, 4], [5, 6]]
    >>> vectors_basis = [[1, 0], [1, 1]]

    >>> transform_coordinates(points, [0, 0], vectors_basis)
    array([[ 1.,  3.],
           [ 3.,  7.],
           [ 5., 11.]])

    >>> points = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> vectors_basis = [[1, 0, 0], [-1, 1, 0]]

    >>> transform_coordinates(points, [0, 0, 0], vectors_basis)
    array([[1., 1.],
           [4., 1.],
           [7., 1.]])

    """
    n_points, n_bases = len(points), len(vectors_basis)
    coordinates = np.zeros((n_points, n_bases))

    vectors_to_points = np.subtract(points, point_origin)

    for i, vector_basis in enumerate(vectors_basis):
        coordinates[:, i] = np.apply_along_axis(np.dot, 1, vectors_to_points, vector_basis)

    return coordinates
