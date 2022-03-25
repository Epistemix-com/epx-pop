:orphan:

.. _getting_started:

****************************
Getting started with epx-pop
****************************

This 10-minute guide gives an overview of the functionality of epx-pop
and each of its sub-packages. You can find links to more detailed information
in each of the subsections below. This getting-started guide assumes you have
already followed the :ref:`step_by_step_install` section of the documentation
to get the package and its dependencies set up on your machine.


Importing epx-pop
=================

After installing epx-pop you can open up a Python terminal and load the
entire package by:

    >>> import epxpop


.. _first_steps:

First steps with epx-pop
========================

Running the test suite
----------------------

After installing the code and its dependencies, navigate to some new working
directory and execute the test suite. (This only needs to be done once per
installed version.)

.. code:: python

    import epxpop
    epxpop.test()

See :ref:`verifying_your_installation` for details about the message that
prints after you run the test suite.
