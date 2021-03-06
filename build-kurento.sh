#!/bin/bash -i

set -e

DISTRO=${2:-el7}

case $DISTRO in
  el7)
    IMAGE="centos:7"
    CONTEXT=Dockerfile
    ;;
  amzn2)
    IMAGE="amazonlinux:2"
    CONTEXT=Dockerfile.amzn2
    ;;
  *)
    echo Unknown distro $DISTRO
    exit 1
    ;;
esac

if [[ ! -d $1 ]]; then
  echo "Kurento version $1 folder not found"
  exit 1
fi

docker pull $IMAGE
docker build -t rpm-build-kurento-$DISTRO -f docker/$CONTEXT docker

cd $1

if [[ "$(docker ps -qa -f name=kurento-build-deps-$DISTRO)" == "" ]]; then
  docker run -d \
    -v $(pwd)/SPECS:/root/rpmbuild/SPECS \
    -v $(pwd)/RPMS.$DISTRO:/root/rpmbuild/RPMS \
    -v $(pwd)/SOURCES:/root/rpmbuild/SOURCES \
    -v $(pwd)/scripts:/root/scripts \
    --name kurento-build-deps-$DISTRO -t rpm-build-kurento-$DISTRO
fi

docker exec -it kurento-build-deps-$DISTRO /root/scripts/build-deps.sh

if [[ "$(docker ps -qa -f name=kurento-build-rpms-$DISTRO)" == "" ]]; then
  docker run -d \
    -v $(pwd)/SPECS:/root/rpmbuild/SPECS \
    -v $(pwd)/RPMS.$DISTRO:/root/rpmbuild/RPMS \
    -v $(pwd)/SOURCES:/root/rpmbuild/SOURCES \
    -v $(pwd)/scripts:/root/scripts \
    --name kurento-build-rpms-$DISTRO -t rpm-build-kurento-$DISTRO
fi

docker exec -it kurento-build-rpms-$DISTRO /root/scripts/build.sh

docker stop kurento-build-deps-$DISTRO kurento-build-rpms-$DISTRO
docker rm kurento-build-deps-$DISTRO kurento-build-rpms-$DISTRO
