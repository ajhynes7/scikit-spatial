"""Spatial transformations."""

import numpy as np


def transform_coordinates(points, point_origin, vectors_basis):
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

    def yield_columns():
        """Yield each column of points in the new coordinate system."""
        for vector_basis in vectors_basis:
            yield np.apply_along_axis(np.dot, 1, vectors_to_points, vector_basis)

    coordinates = np.column_stack([*yield_columns()])

    return coordinates
