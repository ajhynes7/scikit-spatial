FROM python:3.7-slim as base

COPY requirements /app/requirements
COPY skspatial /app/skspatial

WORKDIR /app
RUN pip install -r requirements/base.txt

FROM base as base_test
RUN pip install -r requirements/base_test.txt

FROM base_test as unit
CMD ["pytest", "skspatial/tests/unit/", "--cov=skspatial/", "--cov-report=html"]