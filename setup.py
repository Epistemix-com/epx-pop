"""
"""

from pathlib import Path
import pip
from setuptools import setup, find_packages
import os
from setuptools.command.install import install
from setuptools.command.develop import develop
import sys
import subprocess

if int(pip.__version__.split(".")[0]) < 10:
    from pip import main as pip_main
else:
    # https://github.com/pypa/pip/issues/5080
    from pip._internal import main as pip_main

PACKAGENAME = "epx-pop"


def read(file_name):
    """Read a text file and return the content as a string."""
    with open(
        os.path.join(os.path.dirname(__file__), file_name), encoding="utf-8"
    ) as f:
        return f.read()


VERSION = read("epxpop/VERSION").strip()

dev_requirements = ["tox"]

setup(
    name=PACKAGENAME,
    version=VERSION,
    setup_requires=["pytest-runner"],
    author="Duncan Campbell",
    author_email="duncan.campbell@epistemix.com",
    description="Python tools for interacting with synthetic populations",
    long_description=(
        "A package which contains python tools for interacting "
        "with synthetic populations"
    ),
    install_requires=["pandas", "pytest"],
    extras_require={"dev": dev_requirements},
    packages=find_packages(),
    url="https://github.com/Epistemix-com/epx-pop",
    package_data={
        "epxpop": [
            "VERSION",
            "united_states/data/counties.txt",
            "united_states/data/states.txt",
        ],
        "scripts": [
            "synth_pops.json"
        ]
    },
    cmdclass={},
)
