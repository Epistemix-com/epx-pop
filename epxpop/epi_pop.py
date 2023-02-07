"""
a module used to represent the Epistemix synthetic population (v5)
"""

import os
from pathlib import Path
from typing import Dict, List, Set, Union
import pandas as pd
import numpy as np
from .pop import SynthPop
from .utils import read_csv, line_count

__all__ = ["EpiSynthPop"]
__author__ = ["Claire Dickey"]

class EpiSynthPop(SynthPop):
    """
    A class that represents the Epistemix synthetic population

    Parameters
    ----------
    country : string
        a country sring
    version : string
        a population version string

    Attributes
    ----------
    available_locations : dict
        a dictionary of available locations and corresponding FIPS codes
    locations : dict
        a dictonary of all valid locations and associated directories
    county_fips_codes : set[str]
        the set of all county FIPS codes

    Methods
    -------
    load_people :
        load a DataFrame of people
    load_gq_people :
        load a DataFrame of people associated with group quarters
    population_count :
        return the total population count
    gq_population_count :
        return the population count of people associated with group quarters
    load_schools :
        load a DataFrame of schools
    load_workplaces :
        load a DataFrame of workplaces
    load_households :
        load a DataFrame of households

    Examples
    --------
    A ``EpiSynthPop`` object may be instantiated using a version and country:

    >>> from epxpop import EpiSynthPop
    >>> pop = EpiSynthPop(country='usa', version='US_2010.v5')

    will return an object, ``pop``, that provides access to the
    synthetic population data.
    """

    def __init__(self, country="usa", version="US_2010.v5", **kwargs):
        """
        Initialize a EpiSynthPop object
        """
        super().__init__(country=country, version=version, **kwargs)

    @property
    def available_locations(self) -> Dict[str, List[str]]:
        """
        a list of available FIPS code locations in the synthetic population
        """
        PATH_TO_POP_COUNTRY = Path(self.path_to_pop)
        fips = os.listdir(PATH_TO_POP_COUNTRY)
        fips.remove('metadata')
        
        available_locations = {}
        for i in fips:
            key = self.return_location_name(i)
            available_locations[key] = [i]
        self._available_locations = available_locations
        
        return self._available_locations

    @property
    def locations(self) -> Dict[str, List[str]]:
        """
        a dictionary of locations which can be used to select subpopulations
        """
    
        locations = {}
        locations_fname = "metadata/locations.txt"
        PATH_TO_POP_COUNTRY = Path(self.path_to_pop)
        
        available_locations = os.listdir(PATH_TO_POP_COUNTRY)
        available_locations.remove('metadata')
        
        with open(os.path.join(PATH_TO_POP_COUNTRY, "metadata/locations.txt")) as f:
            for line in f:
                key, value = line.split(" ", 1)
                key = key.strip()
                dirs = value.strip().split()
                for i in dirs:
                    if i in available_locations:
                        locations[key] = dirs
                        
        self._locations = locations
        return self._locations

    def return_location_name(self, fips_codes: Union[str, List[str]]) -> str:
        """
        Return a location name associated with a list of FIPS codes.
        Parameters
        ----------
        fips : list or string
            a list of county fips code. Alternatively, a single fips code can
            be passed.
        Returns
        -------
        location_name : string
            a location name
        Example
        -------
        >>> from epxpop import EpiSynthPop
        >>> pop = EpiSynthPop(country='usa', version='US_2010.v5')
        >>> pop.return_location_name(['55061'])
        'Kewaunee_County_WI'
        """

        # process FIPS codes
        if type(fips_codes) is list:
            fips_codes = [str(e).zfill(5) for e in fips_codes]
        elif type(fips_codes) is str:
            # allow single FIPS code as argument
            fips_codes = [fips_codes.zfill(5)]

        # sort FIPS codes into an expected order
        fips_codes.sort()

        # lists are not hashable, so we convert the list to a string
        reversed_locations = {
            "-".join(value): key for (key, value) in self.locations.items()
        }

        try:
            return reversed_locations["-".join(fips_codes)]
        except KeyError:
            msg = f"No location defined by the FIPS codes: {fips_codes}"
            raise ValueError(msg)

    @property
    def county_fips_codes(self) -> Set[str]:
        """
        a set of county FIPS codes which can be used to select subpopulations
        """
        self._county_fips_codes = set(sum(self.locations.values(), []))
        return self._county_fips_codes


    def load_people(
        self, locations: List[str], include_gq_people: bool = True
    ) -> pd.DataFrame:
        """
        Return a DataFrame of people associated with `locations`.
        Parameters
        ----------
        locations : list
            a list of locations
        include_gq_people : bool
            include people associated with group quarters
        Returns
        -------
        people : pd.DataFrame
            a Pandas DataFrame of people associated with `locations`
        Examples
        --------
        A DataFrame of people can be loaded for two counties as:
        >>> from epxpop import EpiSynthPop
        >>> pop = EpiSynthPop()
        >>> people_df = pop.load_people(locations=['Loving_County_TX', 'Jefferson_County_PA'])
        """

        dirs = self._locations_to_dirs(locations)

        # generate an empty people data frame
        #types = {key: people_cols[key][1] for key in people_cols.keys()}
        #people = pd.DataFrame(columns=people_cols.keys()).astype(types)
        people = pd.DataFrame()

        # loop over directories, loading people.txt into a data frame
        for dir in dirs:
            PATH_TO_PEOPLE = os.path.join(self.path_to_pop, dir, "person.txt")
            #df = read_csv(
            #    PATH_TO_PEOPLE, people_cols, header=0, na_values=['X']
            #)
            df = pd.read_csv(PATH_TO_PEOPLE)
            people = pd.concat((people, df), ignore_index=True)

        if include_gq_people:
            people = pd.concat((people, self.load_gq_people(locations=locations)), ignore_index=True)

        return people

    
    def load_gq_people(self, locations: List[str]) -> pd.DataFrame:
        """
        Return a DataFrame of people in group quaters associated with
        `locations`.
        Parameters
        ----------
        locations : list
            a list of locations
        Returns
        -------
        gq_people : pd.DataFrame
            a Pandas DataFrame of people in group quaters associated with
            `locations`
        Examples
        --------
        A DataFrame of people associated with group quaters can be loaded for
        two counties as:
        >>> from epxpop import EpiSynthPop
        >>> pop = EpiSynthPop()
        >>> gq_people_df = pop.load_gq_people(locations=['Loving_County_TX', 'Jefferson_County_PA'])
        """

        dirs = self._locations_to_dirs(locations)

        # generate an empty people data frame
        #types = {key: gq_people_cols[key][1] for key in gq_people_cols.keys()}
        #gq_people = pd.DataFrame(columns=gq_people_cols.keys()).astype(types)
        gq_people = pd.DataFrame()

        # loop over directories, loading gq_people.txt into a data frame
        for dir in dirs:
            PATH_TO_PEOPLE = os.path.join(self.path_to_pop, dir, "gq_person.txt")
            #df = read_csv(PATH_TO_PEOPLE, gq_people_cols, header=0)
            df = pd.read_csv(PATH_TO_PEOPLE)
            gq_people = pd.concat((gq_people, df), ignore_index=True)

        return gq_people

    
    def population_count(
        self, locations: List[str], include_gq_people: bool = True
    ) -> int:
        """
        Return an integer count of total people in `locations`.
        Parameters
        ----------
        locations : list
            a list of locations
        include_gq_people : bool
            include people associated with group quarters
        Returns
        -------
        n : int
            the total number of people in `locations`
        Examples
        --------
        The total population of a county can be returned as:
        >>> from epxpop import EpiSynthPop
        >>> pop = EpiSynthPop()
        >>> tot_pop = pop.population_count(locations=['Kewaunee_County_WI'])
        >>> tot_pop
        20399
        """

        dirs = self._locations_to_dirs(locations)

        n = 0
        for dir in dirs:
            PATH_TO_PEOPLE = os.path.join(self.path_to_pop, dir, "person.txt")
            n = n + len(pd.read_csv(PATH_TO_PEOPLE))

        if include_gq_people:
            n = n + self.gq_population_count(locations)

        return n
    
    def gq_population_count(self, locations: List[str]) -> int:
        """
        Return an integer count of total people associated with group quaters
        in `locations`.
        Parameters
        ----------
        locations : list
            a list of locations
        include_gq_people : bool
            include people associated with group quarters
        Returns
        -------
        n : int
            the total number of people associated group quaters in `locations`
        Examples
        --------
        The total group quarters population of a county can be returned as:
        >>> from epxpop import EpiSynthPop
        >>> pop = EpiSynthPop()
        >>> tot_gq_pop = pop.gq_population_count(locations=['Kewaunee_County_WI'])
        >>> tot_gq_pop
        140
        """

        dirs = self._locations_to_dirs(locations)

        n = 0
        for dir in dirs:
            PATH_TO_GQ_PEOPLE = os.path.join(self.path_to_pop, dir, "gq_person.txt")
            n = n + len(pd.read_csv(PATH_TO_GQ_PEOPLE))

        return n


    def load_schools(self, locations: List[str]) -> pd.DataFrame:
        """
        Return a DataFrame of schools in `locations`.
        Parameters
        ----------
        locations : list
            a list of locations
        Returns
        -------
        schools : pd.DataFrame
            a Pandas DataFrame of schools in `locations`
        Examples
        --------
        A DataFrame of schools in a county can be loaded as:
        >>> from epxpop import EpiSynthPop
        >>> pop = EpiSynthPop()
        >>> schools_df = pop.load_schools(locations=['Jefferson_County_PA'])
        """

        dirs = self._locations_to_dirs(locations)

        # generate an empty people data frame
        #types = {key: school_cols[key][1] for key in school_cols.keys()}
        #schools = pd.DataFrame(columns=school_cols.keys()).astype(types)
        schools = pd.DataFrame()

        # loop over directories, loading schools.txt into a data frame
        for dir in dirs:
            PATH_TO_SCHOOLS = os.path.join(self.path_to_pop, dir, "school.txt")
            #df = read_csv(PATH_TO_SCHOOLS, school_cols, header=0)
            df = pd.read_csv(PATH_TO_SCHOOLS)
            schools = pd.concat((schools, df), ignore_index=True)

        return schools.drop_duplicates()
    

    def load_workplaces(self, locations: List[str]) -> pd.DataFrame:
        """
        Return a DataFrame of workplaces in `locations`.
        Parameters
        ----------
        locations : list
            a list of locations
        Returns
        -------
        workplaces : pd.DataFrame
            a Pandas DataFrame of workplaces in `locations`
        Examples
        --------
        A DataFrame of workplaces in a county can be loaded as:
        >>> from epxpop import EpiSynthPop
        >>> pop = EpiSynthPop()
        >>> workplaces_df = pop.load_workplaces(locations=['Jefferson_County_PA'])
        """

        dirs = self._locations_to_dirs(locations)

        # generate an empty people data frame
        #types = {key: workplaces_cols[key][1] for key in workplaces_cols.keys()}
        #workplaces = pd.DataFrame(columns=workplaces_cols.keys()).astype(types)
        workplaces = pd.DataFrame()

        # loop over directories, loading workplaces.txt into a data frame
        for dir in dirs:
            PATH_TO_WORKPLACES = os.path.join(self.path_to_pop, dir, "workplace.txt")
            #df = read_csv(PATH_TO_WORKPLACES, workplaces_cols, header=0)
            df = pd.read_csv(PATH_TO_WORKPLACES)
            workplaces = pd.concat((workplaces, df), ignore_index=True)

        return workplaces.drop_duplicates()
    

    def load_households(self, locations: List[str]) -> pd.DataFrame:
        """
        Return a DataFrame of households in `locations`.
        Parameters
        ----------
        locations : list
            a list of locations
        Returns
        -------
        households : pd.DataFrame
            a Pandas DataFrame of households in `locations`
        Examples
        --------
        A DataFrame of households in a county can be loaded as:
        >>> from epxpop import EpiSynthPop
        >>> pop = EpiSynthPop()
        >>> households_df = pop.load_households(locations=['Jefferson_County_PA'])
        """

        dirs = self._locations_to_dirs(locations)

        # generate an empty people data frame
        #types = {key: household_cols[key][1] for key in household_cols.keys()}
        #households = pd.DataFrame(columns=household_cols.keys()).astype(types)
        households = pd.DataFrame()

        # loop over directories, loading households.txt into a data frame
        for dir in dirs:
            PATH_TO_HOUSEHOLDS = os.path.join(self.path_to_pop, dir, "household.txt")
            #df = read_csv(PATH_TO_HOUSEHOLDS, household_cols, header=0)
            df = pd.read_csv(PATH_TO_HOUSEHOLDS)
            households = pd.concat((households, df), ignore_index=True)

        return households
    
    def _locations_to_dirs(self, locations: List[str]) -> Set[str]:
        """
        return the directory or directories associated with the `locations`.
        Parameters
        ----------
        locations : List[str]
            a list of locations
        """

        dirs = set()
        for loc in locations:
            if loc in self.county_fips_codes:
                dirs.update([loc])
            else:
                dirs.update(set(self.locations[loc]))

        return dirs
