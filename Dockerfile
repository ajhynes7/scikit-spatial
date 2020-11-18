FROM python:3.7-slim as base

WORKDIR /app

COPY requirements requirements
RUN pip install -r requirements/base.txt

COPY setup.cfg setup.cfg
COPY skspatial skspatial

FROM base as lint_code
RUN pip install -r requirements/lint_code.txt
CMD ["flake8", "skspatial/"]

FROM base as lint_docs
RUN pip install -r requirements/lint_docs.txt
CMD ["pydocstyle", "skspatial/", "--convention=numpy", "--add-ignore=D104,D105"]

FROM base as base_test
RUN pip install -r requirements/base_test.txt

FROM base_test as unit
CMD ["pytest", "skspatial/tests/unit/", "--cov=skspatial/", "--cov-report=html"]

FROM base_test as property
RUN pip install -r requirements/property.txt
CMD ["pytest", "skspatial/tests/property/"]

FROM base as docs
RUN pip install -r requirements/docs.txt
COPY docs/source docs/source
COPY examples examples
CMD ["sphinx-build", "-b", "doctest", "docs/source/", "docs/build/"]