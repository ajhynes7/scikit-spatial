mkdir htmlcov

docker run \
    --mount type=bind,source=$(pwd)/htmlcov,target=/app/skspatial/htmlcov \
    skspatial:unit
