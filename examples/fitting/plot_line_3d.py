"""
3D Line of Best Fit
===================

Fit a line to multiple 2D points.

"""
import matplotlib.pyplot as plt

from skspatial.objects import Points, Line


points = Points([
    [0, 0, 0],
    [1, 1, 0],
    [2, 3, 2],
    [3, 2, 3],
    [4, 5, 4],
    [6, 5, 5],
    [6, 6, 5],
    [7, 6, 7],
])

line_fit = Line.best_fit(points)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

line_fit.plot_3d(ax, t_1=-7, t_2=7, c='k')
points.plot_3d(ax, c='b', depthshade=False)

plt.show()
