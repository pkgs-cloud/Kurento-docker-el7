#!/bin/bash -i

set -e

source $(dirname $(realpath $0))/distro-deps.sh

chown -R root:root /root/rpmbuild

cat >/etc/yum.repos.d/kurento.repo <<EOF
[kurento]
name=Kurento
baseurl=file:///root/rpmbuild/RPMS/
gpgcheck=0
enabled=1
EOF

cd /root/rpmbuild/SPECS

for spec in `ls *.spec`; do
    rpmsrc $spec
done

yumi libogg-devel
yumi opus-devel --disablerepo=* --enablerepo=kurento

yumbd opusfile.spec
rpmbb opusfile.spec
yumi ../RPMS/x86_64/opusfile-0.11-3.*.x86_64.rpm ../RPMS/x86_64/opusfile-devel-0.11-3.*.x86_64.rpm

yumbd spandsp.spec
rpmbb spandsp.spec
yumi ../RPMS/x86_64/spandsp3-3.0.0-1.*.x86_64.rpm ../RPMS/x86_64/spandsp3-devel-3.0.0-1.*.x86_64.rpm

yumbd sofia-sip.spec
rpmbb sofia-sip.spec
yumi ../RPMS/x86_64/sofia-sip-1.13.3-1.*.x86_64.rpm ../RPMS/x86_64/sofia-sip-devel-1.13.3-1.*.x86_64.rpm

yumbd freeswitch.spec
rpmbb freeswitch.spec
yumi ../RPMS/x86_64/freeswitch-1.10.5-1.*.x86_64.rpm

yumi createrepo_c --disablerepo=* --enablerepo=kurento
createrepo_c --update --simple-md-filenames /root/rpmbuild/RPMS
yum clean metadata
