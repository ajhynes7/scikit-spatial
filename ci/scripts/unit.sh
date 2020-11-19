docker build -t skspatial:unit --target unit .

mkdir htmlcov

docker run \
    --mount type=bind,source=$(pwd)/htmlcov,target=/app/skspatial/htmlcov \
    skspatial:unit
