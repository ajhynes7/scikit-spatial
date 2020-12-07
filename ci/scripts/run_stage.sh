stage="$1"
python_version="$2"

tag=${stage}_$python_version

docker build -t skspatial:$tag \
    --build-arg PYTHON_VERSION=$python_version \
    --target $stage .

if [ $stage = "unit" ]; then
    touch coverage.xml
    docker run \
        --mount type=bind,source=$(pwd)/coverage.xml,target=/app/coverage.xml \
        skspatial:$tag
else
    docker run skspatial:$tag
fi
