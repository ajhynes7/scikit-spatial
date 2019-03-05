#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as file_readme:
    readme = file_readme.read()

requirements_install = ['numpy', 'dpcontracts']
requirements_setup = ['pytest-runner', 'wheel']
requirements_test = ['pytest']

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
    install_requires=requirements_install,
    license="BSD license",
    long_description=readme,
    include_package_data=True,
    keywords='scikit-spatial',
    name='scikit-spatial',
    packages=find_packages(exclude=['doc', 'tests']),
    setup_requires=requirements_setup,
    test_suite='tests',
    tests_require=requirements_test,
    url='https://github.com/ajhynes7/scikit-spatial',
    version='0.1.0',
    zip_safe=False,
)
