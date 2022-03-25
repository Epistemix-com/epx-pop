"""
"""

from .fred import _path_to_fred_pop

__all__ = ["SynthPop"]
__author__ = ["Duncan Campbell"]


class SynthPop(object):
    """
    an abstract class used to represent synthetic populations

    Parameters
    ----------
    country : string
        a country sring

    version : string
        a population version string

    Attributes
    ----------
    path_to_pop : Path
        the abosulte path to the location of the synthetic population
    """

    def __init__(self, country, version, **kwargs) -> None:
        """
        Initialize a SynthPop object
        """
        self.path_to_pop = _path_to_fred_pop(country=country, version=version, **kwargs)
