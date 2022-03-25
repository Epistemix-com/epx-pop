"""
political divisions of the United States
"""

import os
import numpy as np
from collections import defaultdict


_dir_path = os.path.dirname(os.path.realpath(__file__))
_counties_fname = os.path.join(_dir_path, "data/counties.txt")
_states_fname = os.path.join(_dir_path, "data/states.txt")


us_state_counties = defaultdict(list)
"""
A dictionary of counties for US states and territories
Keys are string state and territory abbreviations.
Values are lists of county names.

:meta hide-value:
"""


us_state_abbreviations = {}
"""
A dictionary of US state and territory abbreviations
Keys are string state and territory names.
Values are string abbrevaitions.

:meta hide-value:
"""


# populate `us_state_counties` dictionary
with open(_counties_fname, "r") as fp:
    line = fp.readline().strip()
    n_lines = 1

    while line:
        place_name, county_ids = line.split("\t", 1)

        county_ids = county_ids.split("\t")
        county_ids = np.array(county_ids).astype("int")
        county_ids = list(county_ids)

        county_name, state_abbr = place_name.rsplit("_", 1)

        us_state_counties[state_abbr].append(county_name.lower())

        line = fp.readline().strip()


# populate `us_state_abbreviations` dictionary
with open(_states_fname, "r") as fp:
    line = fp.readline().strip()
    n_lines = 1

    while line:
        name, abbv = line.split("\t", 1)
        us_state_abbreviations[name] = abbv
        line = fp.readline().strip()
