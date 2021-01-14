# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 12:33:58 2020

@author: Dylan Agius
"""

import setuptools


setuptools.setup(
    name="lengmorph-DylanAgius", 
    version="0.0.1",
    author="Dylan Agius",
    author_email="dylan.j.agius@gmail.com",
    description="Create multidimensional arrays to implement length scale modification",
    long_description_content_type="text/markdown",
    url="https://github.com/DylanAgius/LengMorph",
    scripts=['fileconstruct.py','node_increase.py',
             'scrape.py']
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
)
