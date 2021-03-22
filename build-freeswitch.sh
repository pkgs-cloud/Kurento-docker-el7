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

cd freeswitch

if [[ "$(docker ps -qa -f name=freeswitch-build-rpms-$DISTRO)" == "" ]]; then
  docker run -d \
    -v $(pwd)/SPECS:/root/rpmbuild/SPECS \
    -v $(dirname $(pwd))/$1/RPMS.$DISTRO:/root/rpmbuild/RPMS \
    -v $(pwd)/SOURCES:/root/rpmbuild/SOURCES \
    -v $(pwd)/scripts:/root/scripts \
    --name freeswitch-build-rpms-$DISTRO -t rpm-build-kurento-$DISTRO
fi

docker exec -it freeswitch-build-rpms-$DISTRO /root/scripts/build.sh

docker stop freeswitch-build-rpms-$DISTRO
docker rm freeswitch-build-rpms-$DISTRO
