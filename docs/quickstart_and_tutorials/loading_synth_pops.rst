.. _reading_variables:

****************************************************
Loading an Example Synthetic Population with epx-pop
****************************************************

``epx-pop`` provides a Python interface to retrieve FRED compatible synthetic
population data as ``pandas.DataFrame`` objects. This is provided by methods
attached to the :class:`epxpop.SynthPop` object. First instantiate a
:class:`epxpop.SynthPop` object representing your synthetic population. In this
example, we will load the RTI 2010 (version 4) population:

.. code-block:: python

    >>> from epxpop import RTISynthPop
    >>> pop = RTISynthPop()

.. note::
   Synthetic population data is located using the ``FRED_DATA`` environmental
   variable. If this is not set in your environment, you can pass it as a
   keyword argument to the ``RTISynthPop`` constructor e.g.

   .. code-block:: python

      >>> FRED_DATA = '~/fred/data'
      >>> pop = RTISynthPop(FRED_DATA=FRED_DATA)

For a given set of locations, a table of associated "people" can be loaded:

.. code-block:: python

    >>> locations = ['Allegheny_County_PA','Jefferson_County_PA']
    >>> people = pop.load_people(locations=locations)
    >>> people
             sp_id    sp_hh_id  age   sex  race  relate  school_id      work_id     sp_gq_id
    0    164091696  14350288.0   24  b'M'   1.0     0.0        NaN  513967705.0          NaN
    1    164091697  14354678.0   24  b'M'   1.0     0.0        NaN  513980750.0          NaN
    2    164091698  14367662.0   24  b'M'   1.0     0.0        NaN  513949983.0          NaN
    3    164091701  14487997.0   24  b'M'   1.0     0.0        NaN  513977007.0          NaN
    4    164091704  14494399.0   24  b'M'   1.0     0.0        NaN  513965846.0          NaN
    ..         ...         ...  ...   ...   ...     ...        ...          ...          ...
    719  940086670         NaN   85  b'F'   NaN     NaN        NaN          NaN  450042411.0
    720  940086671         NaN   90  b'F'   NaN     NaN        NaN          NaN  450042411.0
    721  940086675         NaN   92  b'F'   NaN     NaN        NaN          NaN  450042411.0
    722  940086673         NaN   87  b'F'   NaN     NaN        NaN          NaN  450042411.0
    723  940086674         NaN   85  b'F'   NaN     NaN        NaN          NaN  450042411.0

    [1264013 rows x 9 columns]
