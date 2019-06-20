"""
2D Point-Line Projection
========================

Project a point onto a line.

"""
from skspatial.objects import Point, Line
from skspatial.plotting import plot_2d


line = Line(point=[0, 0], direction=[1, 1])
point = Point([1, 4])

point_projected = line.project_point(point)
line_projection = Line.from_points(point, point_projected)

fig, ax = plot_2d(
    line.plotter(t2=5, c='k'),
    line_projection.plotter(c='k', linestyle='--'),
    point.plotter(s=75, c='k'),
    point_projected.plotter(c='r', s=75, zorder=3),
)

ax.axis('equal')
fig.show()
