"""Functions related to dimension reduction."""

from numpy.linalg import matrix_rank

from skspatial.transformation import mean_center


def affine_rank(points):
    """
    Return the affine rank of a set of points.

    The affine rank is the dimension of the smallest affine space that contains the points.
    A rank of 1 means the points are collinear, and a rank of 2 means they are coplanar.

    Parameters
    ----------
    points : ndarray
        Input points.

    Returns
    -------
    int
        Affine rank of the points.

    Examples
    --------
    >>> import numpy as np
    >>> from skspatial.reduction import affine_rank

    >>> points = np.array([[5, 3], [-6, 20]])
    >>> affine_rank(points)
    1

    >>> points = np.array([[0, 0], [1, 1], [2, 2]])
    >>> affine_rank(points)
    1

    >>> points = np.array([[0, 1, 0], [1, 1, 0], [2, 2, 2]])
    >>> affine_rank(points)
    2

    >>> points = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    >>> affine_rank(points)
    2

    >>> points = np.array([[1, 3, 2], [3, 4, 5], [2, 1, 5], [5, 9, 8]])
    >>> affine_rank(points)
    3

    """
    points_centered, _ = mean_center(points)

    return matrix_rank(points_centered)
