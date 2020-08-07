"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as file_readme:
    readme = file_readme.read()


setup(
    author="Andrew Hynes",
    author_email='andrewjhynes@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
    ],

    description="Spatial objects and computations based on NumPy arrays.",
    long_description=readme,

    name='scikit-spatial',
    keywords='scikit-spatial',

    package_dir={"": "src"},
    packages=find_packages("src"),

    package_data={
        'skspatial': ['py.typed'],  # Needed for distributing type annotations.
    },

    install_requires=[
        'matplotlib>=3.0.0',
        'numpy>=1.12.0',
    ],

    setup_requires=['pytest-runner', 'wheel'],
    tests_require=['pytest'],
    test_suite='tests',

    include_package_data=True,
    license="BSD license",
    url='https://github.com/ajhynes7/scikit-spatial',
    version='4.0.1',
    zip_safe=False,
)
