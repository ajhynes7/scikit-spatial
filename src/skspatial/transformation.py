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


def rotation_matrix_from_axis_and_angle(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / np.sqrt(np.dot(axis, axis))
    a = np.cos(theta / 2.0)
    b, c, d = -axis * np.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                    [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                    [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def rotation_matrix_from_vectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix
