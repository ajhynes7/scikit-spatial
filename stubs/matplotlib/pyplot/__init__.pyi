from typing import Sequence, Tuple

from matplotlib.axes import Axes
from matplotlib.figure import Figure


class Circle:

    def __init__(self, xy: Sequence, radius: float = 5, **kwargs: str) -> None: ...


def figure(**kwargs: str) -> Figure: ...

def subplots(**kwargs: str) -> Tuple[Figure, Axes]: ...
