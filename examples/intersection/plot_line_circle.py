"""
Circle-Line Intersection
========================

"""
from skspatial.objects import Circle
from skspatial.objects import Line
from skspatial.plotting import plot_2d


circle = Circle([0, 0], 5)
line = Line([0, 0], [1, 1])

point_a, point_b = circle.intersect_line(line)


_, ax = plot_2d(
    circle.plotter(fill=False),
    line.plotter(t_1=-5, t_2=5, c='k'),
    point_a.plotter(c='r', s=100, edgecolor='k', zorder=3),
    point_b.plotter(c='r', s=100, edgecolor='k', zorder=3),
)

ax.axis('equal')
