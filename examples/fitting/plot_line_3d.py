"""
3D Line of Best Fit
===================

Fit a line to multiple 3D points.

"""
from skspatial.objects import Line, Points
from skspatial.plotting import plot_3d


points = Points(
    [
        [0, 0, 0],
        [1, 1, 0],
        [2, 3, 2],
        [3, 2, 3],
        [4, 5, 4],
        [6, 5, 5],
        [6, 6, 5],
        [7, 6, 7],
    ],
)

line_fit = Line.best_fit(points)


plot_3d(
    line_fit.plotter(t_1=-7, t_2=7, c='k'),
    points.plotter(c='b', depthshade=False),
)
