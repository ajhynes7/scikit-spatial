import numpy as np

from .array import Vector


def is_zero_vector(vector, **kwargs):
    """
    Check if a vector is the zero vector.

    The zero vector in n dimensions is the vector containing n zeros.

    Parameters
    ----------
    vector : array_like
        Input vector.
    kwargs : dict, optional
        Additional keywords passed to `np.allclose`.

    Returns
    -------
    bool
        True if vector is the zero vector; false otherwise.

    Examples
    --------
    >>> is_zero_vector(Vector([0, 0]))
    True
    >>> is_zero_vector(Vector([1, 0]))
    False

    >>> is_zero_vector(Vector([0, 0, 1e-4]))
    False
    >>> is_zero_vector(Vector([0, 0, 1e-4]), atol=1e-3)
    True

    """
    return np.allclose(vector.array, 0, **kwargs)


def are_perpendicular(vector_u, vector_v, **kwargs):
    """
    Check if two vectors are perpendicular.

    Vectors u and v are perpendicular <==> Dot product of u and v is zero.

    Parameters
    ----------
    vector_u, vector_v : array_like
        Input vectors
    kwargs : dict, optional
        Additional keywords passed to `np.isclose`.

    Returns
    -------
    bool
        True if vectors are perpendicular; false otherwise.

    Examples
    --------
    >>> are_perpendicular(Vector([0, 1]), Vector([1, 0]))
    True

    >>> are_perpendicular(Vector([-1, 5]), Vector([3, 4]))
    False

    >>> are_perpendicular(Vector([2, 0, 0]), Vector([0, 0, 2]))
    True

    The zero vector is perpendicular to all vectors.

    >>> are_perpendicular(Vector([0, 0, 0]), Vector([1, 2, 3]))
    True

    """
    return np.isclose(vector_u.dot(vector_v), 0, **kwargs)


def are_parallel(vector_u, vector_v, **kwargs):
    """
    Check if two vectors are parallel.

    Parameters
    ----------
    vector_u, vector_v : array_like
        Input vectors
    kwargs : dict, optional
        Additional keywords passed to `is_zero_vector`.

    Returns
    -------
    bool
        True if vectors are parallel; false otherwise.

    Examples
    --------
    >>> are_parallel(Vector([0, 1]), Vector([1, 0]))
    False

    >>> are_parallel(Vector([-1, 5]), Vector([2, -10]))
    True

    >>> are_parallel(Vector([1, 2, 3]), Vector([3, 6, 9]))
    True

    >>> are_parallel(Vector([0, 0, 0]), Vector([3, 4, -1]))
    True

    >>> are_parallel(Vector([1, 2, 3]), Vector([2, 4, 6]))
    True

    """
    vector_cross = Vector(vector_u.cross(vector_v))

    return is_zero_vector(vector_cross, **kwargs)


def are_collinear(point_a, point_b, point_c, **kwargs):
    """
    Check if three points are collinear.

    Points A, B, C are collinear if vector AB is parallel to vector AC.

    Parameters
    ----------
    point_a, point_b, point_c : ndarray
        Input points.
    kwargs : dict, optional
        Additional keywords passed to `are_parallel`.

    Returns
    -------
    bool
        True if points are collinear; false otherwise.

    Examples
    --------
    >>> from skspatial import Point

    >>> are_collinear(Point([0, 1]), Point([1, 0]), Point([1, 2]))
    False

    >>> are_collinear(Point([1, 1]), Point([2, 2]), Point([5, 5]), atol=1e-7)
    True

    """
    vector_ab = Vector.from_points(point_a, point_b)
    vector_ac = Vector.from_points(point_a, point_c)

    return are_parallel(vector_ab, vector_ac, **kwargs)
