"""Spatial transformations."""

import numpy as np


def transform_coordinates(points, point_origin, vectors_basis):

    n_points, n_bases = len(points), len(vectors_basis)
    coordinates = np.zeros((n_points, n_bases))

    vectors_to_points = np.subtract(points, point_origin)

    for i, vector_basis in enumerate(vectors_basis):
        coordinates[:, i] = np.apply_along_axis(np.dot, 1, vectors_to_points, vector_basis)

    return coordinates
