"""
Circle-Circle Intersection
==========================

"""
from skspatial.objects import Circle
from skspatial.plotting import plot_2d


circle_a = Circle([0, 0], 2)
circle_b = Circle([2, 0], 1)

point_a, point_b = circle_a.intersect_circle(circle_b)


_, ax = plot_2d(
    circle_a.plotter(fill=False),
    circle_b.plotter(fill=False),
    point_a.plotter(c='r', s=100, edgecolor='k', zorder=3),
    point_b.plotter(c='r', s=100, edgecolor='k', zorder=3),
)

ax.set_xlim(-4, 4)
ax.set_ylim(-3, 3)
