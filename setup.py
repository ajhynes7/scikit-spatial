#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = []

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

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
    install_requires=requirements,
    license="BSD license",
    long_description=readme,
    include_package_data=True,
    keywords='scikit_spatial',
    name='scikit_spatial',
    packages=find_packages(include=['scikit_spatial']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ajhynes7/scikit_spatial',
    version='0.1.0',
    zip_safe=False,
)
