"""Transformations of spatial entities."""

import numpy as np
from dpcontracts import require, types


@types(points=np.ndarray)
@require("The input must be a 2D array of points", lambda args: args.points.ndim == 2)
def get_centroid(points):

    return points.mean(axis=0)


@types(points=np.ndarray)
@require("The input must be a 2D array of points", lambda args: args.points.ndim == 2)
def mean_center(points):

    centroid = get_centroid(points)

    points_centered = points - centroid

    return points_centered, centroid
