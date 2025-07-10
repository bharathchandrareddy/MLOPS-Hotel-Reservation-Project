'''
this file is used to install the package using pip.
its also used to manage the project dependencies.
setup.py turns your code into a deployable, reproducible, dependency-aware Python package — which is essential when shipping production software.
'''
from  setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()
setup(
    name='hotel-reservations-project',
    version='0.1',# Version of the package
    packages=find_packages(), # Automatically find packages in the current directory
    install_requires=required, # List of dependencies from requirements.txt
    author='Bharath chandra reddy',)