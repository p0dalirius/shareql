#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : setup.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 12 Aug 2025

import setuptools

long_description = """
"""

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [x.strip() for x in f.readlines()]

setuptools.setup(
    name="shareql",
    version="1.0.0" ,
    description="A Python library and CLI for Share Query Language.",
    url="https://github.com/p0dalirius/shareql",
    author="Podalirius",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="podalirius@protonmail.com",
    packages=["shareql", "shareql.evaluate", "shareql.grammar"],
    package_data={'shareql': ['shareql/evaluate/', 'shareql/grammar/']},
    include_package_data=True,
    license="GPL2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=requirements,
    entry_points={
        'console_scripts': ['shareql=shareql.__main__:main']
    }
)
