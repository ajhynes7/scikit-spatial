from typing import Union

from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D


class Figure:

    def add_subplot(self, *args, **kwargs) -> Union[Axes, Axes3D]: ...
