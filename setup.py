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
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
    ],
    description="Spatial objects and computations based on NumPy arrays.",
    long_description=readme,
    name='scikit-spatial',
    keywords='scikit-spatial',
    packages=find_packages(exclude=['tests*']),
    package_data={
        'skspatial': ['py.typed'],  # Needed for distributing type annotations.
    },
    python_requires='>3.7',
    install_requires=[
        'matplotlib>=3,<4',
        'numpy>=1.20,<2',
    ],
    setup_requires=['wheel'],
    include_package_data=True,
    license="BSD license",
    url='https://github.com/ajhynes7/scikit-spatial',
    version='6.0.0',
    zip_safe=False,
)
