"""Functions to make plotting spatial objects more convienient."""

from typing import Any, Union, Callable, Tuple, cast

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D

from skspatial.plotting.plotting_2d import plot_2d
from skspatial.plotting.plotting_3d import plot_3d


def plotter(obj: Any, **kwargs) -> Union[Callable[[Axes], None], Callable[[Axes3D], None]]:
    """Return a function that plots the object when passed a matplotlib axes object."""

    def _plot_on_axes_2d(ax: Axes) -> None:
        return plot_2d(obj, ax, **kwargs)

    def _plot_on_axes_3d(ax: Axes3D) -> None:
        return plot_3d(obj, ax, **kwargs)

    if obj.dimension == 2:
        return _plot_on_axes_2d

    if obj.dimension == 3:
        return _plot_on_axes_3d

    raise ValueError("The dimension must be 2 or 3.")


def plot_all_2d(*plotters: Callable[[Axes], None]) -> Tuple:
    """Plot multiple spatial objects in 2D."""
    fig, ax = plt.subplots()

    for plotter in plotters:
        plotter(ax)

    return fig, ax


def plot_all_3d(*plotters: Callable[[Axes3D], None]) -> Tuple:
    """Plot multiple spatial objects in 3D."""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Just added to satisfy mypy.
    ax = cast(Axes3D, ax)

    for plotter in plotters:
        plotter(ax)

    return fig, ax
