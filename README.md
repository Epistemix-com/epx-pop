# epx-pop

epx-pop is a Python package for interacting with [FRED](https://docs.epistemix.com/projects/language/en/latest/) synthetic populations.


## Requirements

In order to use the functions and classes in this package, you will need the following Python packages installed:

- [pandas](https://pandas.pydata.org)


## Installation

epx-pop may be installed from source using [pip](https://pypi.org/project/pip/):

```terminal
$user: git clone git@github.com:Epistemix-com/epx-pop.git
$user: cd epx-pop
$user: pip install .
```

You may then import epx-pop in Python,

```python
>>> import epxpop
```

## Developers

### Local Development

To set up a fresh development environment to to work on `epx-pop`, we
recommend using Python's built in `venv` module to create a fresh virtual
environment. This helps to ensure that if something stops working in the
development environment, the explanation is inside the `epx-pop` repository
itself, rather than because of some other software installed in a general
purpose environment.

Start by activating a Python environment containing a Python
executable with the same version you want to use for package development (e.g.
3.8).

```shell
$ python -m venv .venv
$ source .venv/bin/activate
$ which python
/Users/username/Projects/epx-pop/.venv/bin/python
```

When actively working on this package, it is often convenient to install
epx-exec in an environment in "editable" mode using the `-e` option to `pip`:

```shell
pip install -e .
```

### Release Process

We use [Semantic Versioning](https://semver.org/spec/v2.0.0.html), and keep a
`CHANGELOG.md` file to track changes to `epx-pop`. See below for a walkthrough
of the release process.

Fetch the latest changes from the remote

```shell
git fetch
```

Checkout a new branch based on `origin/main` to prepare the release. For the
following examples we imagine we are preparing the release for version `1.0.0`.

```shell
git checkout -b me/release-1.0.0 origin/main
```

Update the `CHANGELOG.md` file with a description of the changes included in the
release. See the example at [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/) for inspiration of what to
include.

Update version numbers in `epxpop/VERSION`.

Make a commit of all changes including updates to the change log, push them, and
open a PR from `me/release-1.0.0` into `main` on GitHub. When this
merges (after making any changes requested by reviewers and pushing them to
`me/release-1.0.0`), tag the tip of `main` with the version number for
the release.

```shell
git checkout main
git pull
git tag v1.0.0
git push origin v1.0.0
```

Create the release on GitHub. From the `epx-min` [repo
page](https://github.com/Epistemix-com/epx-pop) click:

- 'Releases'
- 'Draft a new release'
- Select `v1.0.0` from the 'Select a tag' dropdown

Name the release something like 'epx-pop v1.0.0', and copy the release notes
from the `CHANGELOG.md` into the description box.
