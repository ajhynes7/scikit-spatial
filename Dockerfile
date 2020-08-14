FROM python:3.7-slim as base

COPY setup.cfg setup.py README.rst /app/
COPY stubs /app/stubs
COPY requirements /app/requirements

COPY tests /app/tests
COPY src /app/src

WORKDIR /app

FROM base as lint_code
RUN pip install -r requirements/lint_code.txt
CMD ["flake8", "src/"]

FROM base as lint_docs
RUN pip install -r requirements/lint_docs.txt
CMD ["pydocstyle", "--convention=numpy", "--add-ignore=D104,D105", "src/"]

FROM base as types

# Install git to get numpy-stubs package for type checking.
RUN apt-get update &&\
    apt-get install -y --no-install-recommends git &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements/types.txt
CMD ["mypy", "src/"]

FROM base as tests
RUN python setup.py install
RUN pip install -r requirements/tests.txt

FROM tests as doctests
CMD ["pytest", "--doctest-modules", "src/"]

FROM tests as unit_tests
CMD ["pytest", "--cov=skspatial", "tests/unit/"]

FROM tests as property_tests
RUN pip install -r requirements/property_tests.txt
CMD ["pytest", "tests/property/"]
