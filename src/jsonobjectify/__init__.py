from importlib.metadata import version

from .jsonpath import JsonPath

__version__ = version("jsonobjectify")

__all__ = ["JsonPath","__version__"]