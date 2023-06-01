"""
a module used to represent the Epistemix synthetic population (v5)
"""

import os
from pathlib import Path
from typing import Dict, List, Set, Union
import pandas as pd
import numpy as np
from .fred import _path_to_fred_pop

import plotly.express as px

__all__ = ["SynthPop"]
__author__ = ["Claire Dickey"]

## mapping of race column to categories
race_map = {
    -1 : 'Unspecified',
     0 : 'Unknown',
     1 : 'White',
     2 : 'African American',
     3 : 'American Indian',
     4 : 'Alaska Native',
     5 : 'Tribal',
     6 : 'Asian',
     7 : 'Hawaiian Native',
     8 : 'Other Race',
     9 : 'Multiple Races'
}

sex_map = {
    0 : 'Female',
    1 : 'Male',
}


class SynthPop(object):
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
    summarize_demographics :
        return demographic distributions and visualizations
    visualize_households :
        return a geospatial map of households in location

    Examples
    --------
    A ``SynthPop`` object may be instantiated using a version and country:

    >>> from epxpop import SynthPop
    >>> pop = SynthPop(country='usa', version='US_2010.v5')

    will return an object, ``pop``, that provides access to the
    synthetic population data.
    """

    def __init__(self, country="usa", version="US_2010.v5", **kwargs):
        """
        Initialize a SynthPop object
        """
        self.path_to_pop = _path_to_fred_pop(country=country, version=version, **kwargs)

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
        >>> from epxpop import SynthPop
        >>> pop = SynthPop(country='usa', version='US_2010.v5')
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
        >>> from epxpop import SynthPop
        >>> pop = SynthPop()
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
        >>> from epxpop import SynthPop
        >>> pop = SynthPop()
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
        >>> from epxpop import SynthPop
        >>> pop = SynthPop()
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
        >>> from epxpop import SynthPop
        >>> pop = SynthPop()
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
        >>> from epxpop import SynthPop
        >>> pop = SynthPop()
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
        >>> from epxpop import SynthPop
        >>> pop = SynthPop()
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
        >>> from epxpop import SynthPop
        >>> pop = SynthPop()
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

    def summarize_demographics(
        self, location: str, include_visualization : bool = True, 
        include_gq_people: bool = False) -> pd.DataFrame:
        """
        return a dataframe that summarizes the agent demographics
        for the given location.
        
        currently accepts a single location only
        
        Parameters
        ----------
        location : str
        include_visualization : bool
            show bar charts representing distribution of each attribute
        include_gq_people : bool
            include people associated with group quarters
        Returns
        -------
        demographics : pd.DataFrame
            a Pandas DataFrame summarizing demographics. returned dataframe 
            has three columns:
            - attribute [Age, Sex, Race]
            - value [categorical for sex and race, 10 year bins for age]
            - agent counts [number of synthetic agents with the attribute value]
        Examples
        --------
        A DataFrame of demographic distributions can be generated as follows:
        >>> from epxpop import SynthPop
        >>> pop = SynthPop()
        >>> demographics = pop.summarize_demographics(location='Washtenaw_County_MI')
        >>> demographics = pop.summarize_demographics(location='08031')
        """
        if location in self.county_fips_codes:
            loc = location
        else:
            loc = self.locations[location][0]
        df = self.load_people(locations=[loc], include_gq_people=include_gq_people)
        df["agent_counts"] = 1

        demographics = pd.DataFrame()
        counts  = df.groupby("race").agent_counts.sum().to_frame().reset_index()
        counts["value"] = counts.race.map(race_map)
        counts["attribute"] = "Race"
        demographics = pd.concat([demographics, counts.drop(columns=["race"])], ignore_index=True)
        
        counts  = df.groupby("sex").agent_counts.sum().to_frame().reset_index()
        counts["value"] = counts.sex.map(sex_map)
        counts["attribute"] = "Sex"
        demographics = pd.concat([demographics, counts.drop(columns=["sex"])], ignore_index=True)
        
        df["age_bins"] = pd.cut(df.AGE, bins=np.arange(0,101,10))
        counts = df.age_bins.value_counts().to_frame().reset_index().sort_values("age_bins")
        counts = counts.rename(columns={"count":"agent_counts", "age_bins":"value"})
        counts["value"] = counts.value.astype(str)
        counts["attribute"] = "Age"
        demographics = pd.concat([demographics, counts], ignore_index=True)

        if include_visualization:
            fig1 = px.bar(demographics[demographics.attribute=="Race"], x="value", y="agent_counts")
            fig1.update_layout(
                font_family="Epistemix Label",
                yaxis_title="Agent counts",
                xaxis_title="Race",)
            fig1.show()

            fig2 = px.bar(demographics[demographics.attribute=="Sex"], x="value", y="agent_counts")
            fig2.update_layout(
                font_family="Epistemix Label",
                yaxis_title="Agent counts",
                xaxis_title="Sex",)
            fig2.show()

            fig3 = px.bar(demographics[demographics.attribute=="Age"], x="value", y="agent_counts")
            fig3.update_layout(
                font_family="Epistemix Label",
                yaxis_title="Agent counts",
                xaxis_title="Age",)
            fig3.show()

        return demographics

    def visualize_households(self, location, color : str = None):
        """
        return a dataframe that summarizes the agent demographics
        for the given location. For populations over with more than 50k agents, 
        a random subsample will be selected for display to preserve memory.
        Parameters
        ----------
        location : str
        Examples
        --------
        A DataFrame of demographic distributions can be generated as follows:
        >>> from epxpop import SynthPop
        >>> pop = SynthPop()
        >>> pop.visualize_households(location='Washtenaw_County_MI', color="age")
        >>> pop.visualize_households(location='08031', color="race")
        Both fips codes and properly formatted location names are valid inputs.
        """
        valid_attributes = [None, "age", "sex", "race", "household_income"]
        if color not in valid_attributes:
            print(color+" is not a valid attribute.")
            print("Select from: None, 'age', 'sex', 'race', or 'household_income'")
            return

        if location in self.county_fips_codes:
            loc = location
        else:
            loc = self.locations[location][0]

        people = self.load_people([loc], include_gq_people=False)
        households = self.load_households([loc])
        people_households = pd.read_csv(self.path_to_pop+'/'+loc+'/person-household.txt')

        households = households.rename(columns={"ID":"PLACE"}).drop(columns="income")
        people_households = people_households.drop(columns="ROLE")
        people = (people.rename(columns={"ID":"PERSON", "AGE":"age"})
                  .drop(columns="household_relationship"))
        
        people_households = people_households.merge(households, on="PLACE")
        people_households = people_households.merge(people, on="PERSON")

        people_households["race"] = people_households.race.map(race_map)

        if len(people_households)>50000:
            people_households = people_households.sample(50000)
            
        fig = px.scatter_mapbox(people_households, lat="LAT", lon="LON",color=color,height=600, zoom=9.25)

        mapstyle="mapbox://styles/pnowell/cl4n9fic8001i15mnfmozrt8j"
        token="pk.eyJ1IjoicG5vd2VsbCIsImEiOiJja201bHptMXkwZnQyMnZxcnFveTVhM2tyIn0.Pyarp9gHCON4reKvM2fZZg"

        fig.update_layout(mapbox_style=mapstyle, mapbox_accesstoken=token)
        fig.update_layout(margin={"r":10,"t":10,"l":10,"b":10})
        fig.show()
        return