FROM python:3.7-slim as base

WORKDIR /app

COPY requirements requirements
RUN pip install -r requirements/base.txt

COPY skspatial skspatial


FROM base as base_test
RUN pip install -r requirements/base_test.txt

FROM base_test as unit
CMD ["pytest", "skspatial/tests/unit/", "--cov=skspatial/", "--cov-report=html"]

FROM base as docs
RUN pip install -r requirements/docs.txt
COPY docs/source docs/source
COPY examples examples
CMD ["sphinx-build", "-b", "doctest", "docs/source/", "docs/build/"]