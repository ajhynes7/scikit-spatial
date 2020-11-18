docker build -t skspatial:docs --target docs .

mkdir docs/build

docker run \
    --mount type=bind,source=$(pwd)/docs/build,target=/app/docs/build \
    skspatial:docs
