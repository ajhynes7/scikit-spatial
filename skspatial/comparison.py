from dpcontracts import require

from skspatial.objects import Point, Vector


@require(
    "The inputs must be all points.",
    lambda args: all(
        isinstance(x, Point) for x in [args.point_a, args.point_b, args.point_c]
    ),
)
def are_collinear(point_a, point_b, point_c, **kwargs):
    """
    Check if three points are collinear.

    Points A, B, C are collinear if vector AB is parallel to vector AC.

    Parameters
    ----------
    point_a, point_b, point_c : ndarray
        Input points.
    kwargs : dict, optional
        Additional keywords passed to `np.allclose`.

    Returns
    -------
    bool
        True if points are collinear; false otherwise.

    Examples
    --------
    >>> from skspatial.objects import Point

    >>> are_collinear(Point([0, 1]), Point([1, 0]), Point([1, 2]))
    False

    >>> are_collinear(Point([1, 1]), Point([2, 2]), Point([5, 5]), atol=1e-7)
    True

    """
    vector_ab = Vector.from_points(point_a, point_b)
    vector_ac = Vector.from_points(point_a, point_c)

    return vector_ab.is_parallel(vector_ac, **kwargs)
