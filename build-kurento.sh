#!/bin/bash -i

set -e

if [[ ! -d $1 ]]; then
  echo "Kurento version $1 folder not found"
  exit 1
fi

docker pull centos:7
docker build -t rpm-build-kurento docker

cd $1

if [[ "$(docker ps -qa -f name=kurento-build-deps)" == "" ]]; then
  docker run -d \
    -v $(pwd)/SPECS:/root/rpmbuild/SPECS \
    -v $(pwd)/RPMS:/root/rpmbuild/RPMS \
    -v $(pwd)/SOURCES:/root/rpmbuild/SOURCES \
    -v $(pwd)/scripts:/root/scripts \
    --name kurento-build-deps -t rpm-build-kurento
fi

docker exec -it kurento-build-deps /root/scripts/build-deps.sh

if [[ "$(docker ps -qa -f name=kurento-build-rpms)" == "" ]]; then
  docker run -d \
    -v $(pwd)/SPECS:/root/rpmbuild/SPECS \
    -v $(pwd)/RPMS:/root/rpmbuild/RPMS \
    -v $(pwd)/SOURCES:/root/rpmbuild/SOURCES \
    -v $(pwd)/scripts:/root/scripts \
    --name kurento-build-rpms -t rpm-build-kurento
fi

docker exec -it kurento-build-rpms /root/scripts/build.sh

docker stop kurento-build-deps kurento-build-rpms
docker rm kurento-build-deps kurento-build-rpms
