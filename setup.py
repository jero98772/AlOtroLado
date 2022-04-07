#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
alOtroLado - 2022 - por jero98772
alOtroLado - 2022 - by jero98772
"""
from setuptools import setup, find_packages
setup(
	name='alOtroLado',
	version='1.0.0 beta',
	license='GPLv3',
	author_email='jero98772@protonmail.com',
	author='jero98772',
	description='alOtroLado',
	url='',
	packages=find_packages(),
    install_requires=["Flask","pandas","networkx","pydeck"],
    include_package_data=True,
)