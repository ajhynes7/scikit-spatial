#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as file_readme:
    readme = file_readme.read()


setup(
    author="Andrew Hynes",
    author_email='andrewjhynes@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    description="Spatial objects and computations in 3D.",
    long_description=readme,

    name='scikit-spatial',
    keywords='scikit-spatial',

    packages=find_packages(exclude=['tests*']),

    install_requires=['numpy', 'dpcontracts'],
    setup_requires=['pytest-runner', 'wheel'],
    tests_require=['pytest'],
    test_suite='tests',

    include_package_data=True,
    license="BSD license",
    url='https://github.com/ajhynes7/scikit-spatial',
    version='0.1.0',
    zip_safe=False,
)
