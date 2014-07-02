#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from setuptools import setup, find_packages


setup(
    name='Mopidy-Banshee',
    version='0.1.2',
    description='Banshee extension for Mopidy',
    long_description=open('README.rst').read(),
    author='Thomas Amland',
    author_email='thomas.amland@googlemail.com',
    url='http://github.com/tamland/mopidy-banshee',
    license='Apache License, Version 2.0',
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    test_suite='tests',
    tests_require=['pytest'],
    install_requires=['setuptools', 'Mopidy >= 0.14'],
    entry_points={
        'mopidy.ext': [
            'banshee = mopidy_banshee:Extension',
        ],
    },
    keywords='mopidy banshee',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Environment :: No Input/Output (Daemon)',
        'Topic :: Multimedia :: Sound/Audio :: Players',
        'License :: OSI Approved :: Apache Software License',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
