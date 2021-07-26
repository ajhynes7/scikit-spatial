class _PlotterMixin:

    dimension: int

    def plotter(self, **kwargs):
        """Return a function that plots the object when passed a matplotlib axes."""
        if self.dimension == 2:

            if not hasattr(self, 'plot_2d'):
                raise ValueError("The object cannot be plotted in 2D.")

            return lambda ax: self.plot_2d(ax, **kwargs)

        if self.dimension == 3:

            if not hasattr(self, 'plot_3d'):
                raise ValueError("The object cannot be plotted in 3D.")

            return lambda ax: self.plot_3d(ax, **kwargs)

        raise ValueError("The dimension must be 2 or 3.")


class _BaseSpatial(_PlotterMixin):
    """Private base class for all spatial objects."""

    ...
