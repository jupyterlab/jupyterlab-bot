#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup script for JupyterLab Bot."""
# Standard library imports
import ast
import os

from setuptools import find_packages
from setuptools import setup

# Third party imports

HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(module="jupyterlab_bot"):
    """Get version."""
    with open(os.path.join(HERE, module, "__init__.py"), "r") as f:
        data = f.read()

    lines = data.split("\n")
    for line in lines:
        if line.startswith("VERSION_INFO"):
            version_tuple = ast.literal_eval(line.split("=")[-1].strip())
            version = ".".join(map(str, version_tuple))
            break

    return version


def get_description():
    """Get long description."""
    with open(os.path.join(HERE, "README.md"), "r") as f:
        data = f.read()

    return data


setup(
    name="jupyterlab-bot",
    version=get_version(),
    keywords=[],
    url="https://github.com/jupyterlab/jupyterlab-bot",
    description="jupyterlab-bot.",
    long_description=get_description(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pygithub", "tornado"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
