.. _docs_and_tutorials:


***************************************
Quickstart Guides and Tutorials
***************************************

This section of the documentation contains both quickstart guides
and detailed usage-tutorials. If you are instead looking for
a quick reference to the API of some
class or function, try looking in the :ref:`genindex`.


Quickstart Guides
=================

.. toctree::
   :maxdepth: 1

   getting_started


Downloading Synthetic Population Data
-------------------------------------

Synthetic populations can be downloaded using a script distributed with this
package. Usage and options can be seen by running passing the ``--help`` flag:

.. code:: console

   $ python ./scripts/download_epx_synth_pop.py --help

The default 2010 RTI population for the Uniited States can be downloaded by:

.. code:: console

   $ python ./scripts/download_epx_synth_pop.py RTI_2010


Tutorials
=========

Tutorials on the use of the epx-pop package are coming soon.

.. toctree::
   :maxdepth: 1

   loading_synth_pops
