.. _step_by_step_install:

********************
Package Installation
********************

To install epx-pop, you can either use pip or clone the repo from GitHub and
build the source code. Either way, be sure to read the
:ref:`epxpop_dependencies` section prior to installation.

Using pip
====================

This package is not yet availabe on PyPI. Please check back in the future for
instructions on how to install epx-pop using pip. Currently, the only way to
install epx-pop is :ref:`from source <install_from_source>`.

.. _install_from_source:

Building from source
====================

If you don't install the latest release using pip, you can instead clone the
source code and call the setup file. This is the most common way to install
epx-pop if you want versions of the code that have been updated since the
latest official release. In this case, after installation it is particularly
important that you follow the instructions in the
:ref:`verifying_your_installation` section below.

Before installation, be sure you have installed the package dependencies
described in the :ref:`epxpop_dependencies` section. If you will be
:ref:`installing_epxpop_with_virtualenv`, activate the environment before
following the instructions below. The first step is to clone the epx-pop
repository::

	git clone git@github.com:Epistemix-com/epx-pop.git
	cd epx-pop


Installing one of the official releases
------------------------------------------

All official releases of the code are tagged with their version name, e.g.,
v0.0.0. To install a particular release::

	git checkout v0.0.0
	pip install .

This will install the v0.0.0 release of the code. Other official release
versions (e.g., v1.1.0) can be installed similarly.


Installing the most recent main branch
------------------------------------------

If you prefer to use the most recent version of the code::

	git checkout main
	pip install .

This will install the main branch of the code that is currently under
development. While the features in the official releases have a stable API, new
features being developed in the main branch may not. However, the main branch
may have new features and/or performance enhancements that you may wish to use
for your science application. A concerted effort is made to ensure that only
thoroughly tested and documented code appears in the public main branch, though
epx-pop users should be aware of the distinction between the bleeding edge
version in main and the official release version available through pip.


.. _installing_epxpop_with_virtualenv:

Installing epx-pop using a virtual environment
----------------------------------------------------
If you use `conda <https://docs.conda.io/en/latest/>`_ to manage your Python
distribution and package dependencies, it is easy to create a virtual
environment that will automatically have compatible versions of the necessary
dependencies required by epx-pop. By installing into a virtual environment, you
will not change any of the packages that are already installed system-wide on
your machine. In the example below, we will use conda to create a virtual
environment with all the dependencies handled automatically::


	conda create -n epx python=3.8 pandas


In order to activate this environment::


	conda activate epx


Then install epx-pop into this environment::

	pip install epxpop


Or, alternatively, you can install the latest main branch by following the
:ref:`install from source <install_from_source>` instructions.

Any additional packages you install into the epx virtual environment will not
impact your system-wide environment. Whenever you want work with epx-pop, just
activate the environment and import the code. When you are done and wish to
return to your normal system environment::

	conda deactivate


.. _epxpop_dependencies:

Dependencies
============

If you install epx-pop using pip, then most of your dependencies will be
handled for you automatically.

- `Pandas <https://pandas.pydata.org>`_


.. _verifying_your_installation:

Verifying your installation
==============================

After installing the code and its dependencies, fire up a Python interpreter
and check that the version number matches what you expect:

.. code:: python

	import epxpop
	print(epxpop.__version__)

If the version number is not what it should be, this likely means you have a
previous installation that is superseding the version you tried to install.
This *should* be accomplished by doing `pip uninstall epxpop` before your new
installation, but you may need to uninstall the previous build "manually". Like
all Python packages, you can find the installation location as follows:

.. code:: python

	import epxpop
	print(epxpop.__file__)

This will show where your active version is located on your machine. You can
manually delete this copy of epxpop prior to your new installation to avoid
version conflicts. (There may be multiple copies of epxpop in this location,
depending on how may times you have previously installed the code - all such
copies may be deleted prior to reinstallation).

Once you have installed the package, see :ref:`getting_started` for
instructions on how to get up and running.

Testing your installation
=========================

To verify that your epx-pop installation runs properly, navigate to some new
working directory and execute the test suite. If you installed epx-pop into a
virtual environment, activate the environment before spawning a Python session
and executing the code below.

The full testing suite can be run by executing:

.. code:: python

	import epxpop
	epxpop.test()


Whether you installed the main branch or a release branch, the message that
concludes the execution of the test suite should not indicate that there were
any errors or failures. If you encounter problems when running the test suite,
please be sure you have installed the package dependencies first before
raising a Github Issue and/or contacting the epx-pop developers.
