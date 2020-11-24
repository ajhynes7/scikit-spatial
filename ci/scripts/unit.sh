docker build -t skspatial:unit --target unit .

mkdir coverage

docker run \
    --mount type=bind,source=$(pwd)/coverage.xml,target=/app/skspatial/coverage.xml \
    skspatial:unit
