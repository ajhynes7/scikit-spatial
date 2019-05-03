"""
2D Line of Best Fit
===================

Fit a line to multiple 3D points.

"""
import matplotlib.pyplot as plt

from skspatial.objects import Points, Line


points = Points([
    [0, 0],
    [0, 1],
    [1, 2],
    [3, 3],
    [4, 3],
    [6, 5],
    [5, 6],
    [7, 8],
])

line_fit = Line.best_fit(points)


_, ax = plt.subplots()

line_fit.plot_2d(ax, t_1=-7, t_2=7, c='k')
points.plot_2d(ax, c='k')

plt.show()
