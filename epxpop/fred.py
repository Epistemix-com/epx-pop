"""
"""

import os
from warnings import warn as warning

__all__ = []
__author__ = ["Duncan Campbell"]


def _path_to_fred_pop(country="usa", version="US_2010.v4", **params) -> str:
    """
    Return the full path to the reuqested FRED population data.

    Parameters
    ----------
    country : string

    version : string

    Returns
    -------
    PATH_TO_POP : string
        full path to the requested population data
    """

    PATH_TO_POP = None

    if "FRED_DATA" in params.keys():
        FRED_DATA = params["FRED_DATA"]
    else:
        FRED_DATA = os.getenv("FRED_DATA")
        if FRED_DATA is None:
            msg = "FRED_DATA is not set."
            warning(msg)

            if "FRED_HOME" in params.keys():
                FRED_HOME = params["FRED_HOME"]
            else:
                FRED_HOME = os.getenv("FRED_HOME")

            if FRED_HOME is None:
                msg = "FRED_HOME is not set."
                warning(msg)
            else:
                FRED_DATA = os.path.join(FRED_HOME, "data")

    if not os.path.isdir(FRED_DATA):
        msg = f"FRED_DATA={FRED_DATA} is not a valid directory."
        raise FileNotFoundError(msg)

    PATH_TO_COUNTRY = os.path.join(FRED_DATA, f"country/{country}")
    if not os.path.isdir(PATH_TO_COUNTRY):
        msg = f"country={country} not found in {FRED_DATA}."
        raise FileNotFoundError(msg)

    PATH_TO_POP = os.path.join(PATH_TO_COUNTRY, f"{version}")
    if not os.path.isdir(PATH_TO_POP):
        msg = f"version={version} not found in {PATH_TO_COUNTRY}."
        raise FileNotFoundError(msg)

    return os.path.abspath(PATH_TO_POP)
