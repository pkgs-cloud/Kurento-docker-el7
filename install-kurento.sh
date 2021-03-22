#!/bin/bash -i

set -e

yum install epel-release -y || amazon-linux-extras install epel -y
#yum update -y
yum install mc wget nano patch git yum-utils deltarpm which -y

cat <<EOF >/etc/yum.repos.d/kurento-local.repo
[kurento-local]
name=Kurento Local Repository
baseurl=file:///root/RPMS
enabled=0
gpgcheck=0
EOF

yum install coturn -y

yum install --disablerepo=* --enablerepo=kurento-local opus -y

yum install --enablerepo=kurento-local kms -y

yum install --enablerepo=kurento-local freeswitch -y
