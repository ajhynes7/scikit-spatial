FROM python:3.7-slim

# Install git to get numpy-stubs package for type checking.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install tox==3.19.0

COPY tox.ini setup.cfg setup.py README.rst /app/
COPY stubs /app/stubs
COPY requirements /app/requirements

COPY tests /app/tests
COPY src /app/src

WORKDIR /app

CMD ["tox"]