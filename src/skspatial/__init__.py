"""Top-level package for scikit-spatial."""

__author__ = "Andrew Hynes"
__email__ = "andrewjhynes@gmail.com"

try:
    import importlib.metadata as importlib_metadata

except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version("scikit-spatial")
