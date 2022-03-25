"""
five-digit Federal Information Processing Standards (FIPS) codes
"""

import os
import re

import numpy as np
from typing import List
from collections import defaultdict
from .divisions import us_state_counties, us_state_abbreviations
from difflib import get_close_matches

__author__ = ["Duncan Campbell"]
__all__ = ["fips_codes", "us_state_fips_codes", "us_county_fips_codes"]

_dir_path = os.path.dirname(os.path.realpath(__file__))
_counties_fname = os.path.join(_dir_path, "data/counties.txt")
_states_fname = os.path.join(_dir_path, "data/states.txt")

fips_codes = defaultdict(dict)
"""
a dictionary relating FIPS codes to locations

:meta hide-value:
"""

_us_county_fips_codes_dict = defaultdict(dict)
"""
a dictionary relating county names to FIPS codes

:meta hide-value:
"""

with open(_counties_fname, "r") as fp:
    line = fp.readline().strip()
    n_lines = 1

    while line:
        place_name, county_ids = line.split("\t", 1)

        county_ids = county_ids.split("\t")
        county_ids = np.array(county_ids).astype("int")
        county_ids = list(county_ids)
        county_name, state_abbr = place_name.rsplit("_", 1)

        # populate `fips_codes`
        for county_id in county_ids:
            fips_codes[county_id] = {"county": county_name, "state": state_abbr}

        # populate `us_county_fips_codes`
        _us_county_fips_codes_dict[place_name.lower()] = county_ids

        line = fp.readline().strip()


def county_fips_string(fips) -> str:
    """
    Return a string representation of a county level FIPS code.

    Parameters
    ----------
    fips : int
        a county level fips code.

    Returns
    -------
    fips_str : string
        a string representation of the county fips code
    """

    fips_str = str(fips).zfill(5)

    if len(fips_str) > 5:
        msg = (
            "county level fips codes must strings composed of "
            "5 integer characters."
        )
        raise ValueError(msg)
    return fips_str


def us_state_fips_codes(state) -> List[str]:
    """
    Return a list of all county FIPS codes within a state or territory of the
    United States.

    Parameters
    ----------
    state : string
         the full name or abbreviation of a US state or territory

    Returns
    -------
    fips_codes : list
        a list of FIPS codes

    Example
    -------
    To return the list of county-level fips codes for the state of
    Pennsylvania:

    >>> from epistemixpy.populations import us_state_fips_codes
    >>> fips = us_state_fips_codes('PA')
    """

    try:
        state_abbv = us_state_abbreviations[state]
    except KeyError:
        state_abbv = state

    if state_abbv not in us_state_counties.keys():
        msg = (
            "`state` not recognized as a valid US state/territory name "
            "or abbreviation."
        )
        raise ValueError(msg)

    counties = us_state_counties[state_abbv]

    fips = []
    for county in counties:
        place_name = county + "_" + state_abbv
        for code in _us_county_fips_codes_dict[place_name.lower()]:
            fips.append(code)

    return fips


def us_county_fips_codes(county, state) -> List[str]:
    """
    Return a list of all FIPS codes associated with a county in the United
    States.

    Parameters
    ----------
    county : string
         the full name of a county within a state or territory of the United
         States, for example, 'Allegheny_County'

    state : string
        the full name or abbreviation of a US state or territory

    Returns
    -------
    fips_codes : list
        a list of FIPS codes

    Example
    -------
    To return the list of fips codes associated with Allegheny County, PA:

    >>> from epistemixpy.populations import us_county_fips_codes
    >>> fips = us_county_fips_codes('Allegheny_County', 'PA')
    """

    try:
        state_abbv = us_state_abbreviations[state]
    except KeyError:
        state_abbv = state.upper()

    county = county.lower()

    if state_abbv not in us_state_counties.keys():
        msg = (
            f"{state_abbv} not recognized as a valid US state/territory "
            "name or abbreviation.".format(state_abbv)
        )
        raise ValueError(msg)

    if county not in us_state_counties[state_abbv]:
        msg = (
            f"{county} not recognized as a valid county name "
            f" within {state}. \n"
            "The closest match is: "
            "{0}".format(get_close_matches(county, us_state_counties[state_abbv], 1)[0])
        )
        raise ValueError(msg)

    place_name = county + "_" + state_abbv
    return _us_county_fips_codes_dict[place_name.lower()]


def safe_name(county) -> str:
    """
    Return a string that removes all characters that are not alphabetical or
    underscores.

    Parameters
    ----------
    county : string
        county name string, e.g. O'Brien_County_IA

    Returns
    -------
    all_lower : string
        county name with unsafe characters removed, e.g. OBrien_County_IA
    """

    keep = re.sub("[^a-zA-Z_]+", "", county)

    return keep
