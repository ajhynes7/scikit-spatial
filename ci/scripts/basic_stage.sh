stage="$1"

docker build -t skspatial:$stage --target $stage .
docker run skspatial:$stage
