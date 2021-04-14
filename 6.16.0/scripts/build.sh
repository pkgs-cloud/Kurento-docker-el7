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

yumi kms-boost kms-boost-atomic kms-boost-context kms-boost-coroutine kms-boost-date-time kms-boost-devel kms-boost-filesystem kms-boost-math kms-boost-random kms-boost-regex kms-boost-serialization kms-boost-system kms-boost-test kms-boost-thread kms-boost-timer kms-boost-chrono kms-boost-locale kms-boost-log kms-boost-python kms-boost-graph kms-boost-signals kms-boost-iostreams kms-boost-program-options kms-boost-wave

yumi automake --disablerepo=* --enablerepo=kurento
yumi libogg-devel
yumi opus-devel libvpx-devel --disablerepo=* --enablerepo=kurento

cd /root/rpmbuild/SPECS

yumbd kms-jsoncpp.spec
rpmbb kms-jsoncpp.spec
yumi ../RPMS/x86_64/kms-jsoncpp-1.6.3-1.*.x86_64.rpm ../RPMS/x86_64/kms-jsoncpp-devel-1.6.3-1.*.x86_64.rpm

yumbd kms-libsrtp.spec
rpmbb kms-libsrtp.spec
yumi ../RPMS/x86_64/kms-libsrtp-1.6.0-0.*.x86_64.rpm ../RPMS/x86_64/kms-libsrtp-devel-1.6.0-0.*.x86_64.rpm

rpmbb kms-libusrsctp.spec
yumi ../RPMS/x86_64/kms-libusrsctp-0.9.2-1.*.x86_64.rpm ../RPMS/x86_64/kms-libusrsctp-devel-0.9.2-1.*.x86_64.rpm

yumbd kms-gstreamer.spec
rpmbb kms-gstreamer.spec
yumi ../RPMS/x86_64/kms-gstreamer1-1.8.1-2.*.x86_64.rpm ../RPMS/x86_64/kms-gstreamer1-devel-1.8.1-2.*.x86_64.rpm

yumbd kms-gst-plugins-base.spec
rpmbb kms-gst-plugins-base.spec
yumi ../RPMS/x86_64/kms-gstreamer1-plugins-base-1.8.1-2.*.x86_64.rpm ../RPMS/x86_64/kms-gstreamer1-plugins-base-devel-1.8.1-2.*.x86_64.rpm

yumbd kms-gst-plugins-bad.spec
rpmbb kms-gst-plugins-bad.spec
yumi ../RPMS/x86_64/kms-gstreamer1-plugins-bad-1.8.1-5.*.x86_64.rpm ../RPMS/x86_64/kms-gstreamer1-plugins-bad-devel-1.8.1-5.*.x86_64.rpm

yumbd kms-gst-plugins-good.spec
rpmbb kms-gst-plugins-good.spec
yumi ../RPMS/x86_64/kms-gstreamer1-plugins-good-1.8.1-5.*.x86_64.rpm

yumbd kms-gst-plugins-ugly.spec
rpmbb kms-gst-plugins-ugly.spec
yumi ../RPMS/x86_64/kms-gstreamer1-plugins-ugly-1.8.1-1.*.x86_64.rpm

yumbd kms-gst-libav.spec
rpmbb kms-gst-libav.spec
yumi ../RPMS/x86_64/kms-gstreamer1-libav-1.8.1-1.*.x86_64.rpm

yumbd kms-openwebrtc-gst-plugins.spec
rpmbb kms-openwebrtc-gst-plugins.spec
yumi ../RPMS/x86_64/kms-openwebrtc-gst-plugins-0.10.0-1.*.x86_64.rpm ../RPMS/x86_64/kms-openwebrtc-gst-plugins-devel-0.10.0-1.*.x86_64.rpm

yumi python3-pip python3 python3-setuptools python3-devel python-rpm-macros
yumbd meson.spec
rpmbb meson.spec
yumi ../RPMS/noarch/meson-0.55.1-1.*.noarch.rpm

yumbd kms-libnice.spec
rpmbb kms-libnice.spec
yumi ../RPMS/x86_64/kms-libnice-0.1.18-0.*.x86_64.rpm ../RPMS/x86_64/kms-libnice-devel-0.1.18-0.*.x86_64.rpm

yumbd kurento-module-creator.spec
rpmbb kurento-module-creator.spec
yumi ../RPMS/x86_64/kurento-module-creator-6.16.0-0.*.x86_64.rpm

rpmbb kms-cmake-utils.spec
yumi ../RPMS/x86_64/kms-cmake-utils-6.16.0-0.*.x86_64.rpm

rpmbb kms-jsonrpc.spec
yumi ../RPMS/x86_64/kms-jsonrpc-6.16.0-0.*.x86_64.rpm ../RPMS/x86_64/kms-jsonrpc-devel-6.16.0-0.*.x86_64.rpm

yumbd kms-core.spec
rpmbb kms-core.spec
yumi ../RPMS/x86_64/kms-core-6.16.0-0.*.x86_64.rpm ../RPMS/x86_64/kms-core-devel-6.16.0-0.*.x86_64.rpm

yumbd kms-elements.spec
rpmbb kms-elements.spec
yumi ../RPMS/x86_64/kms-elements-6.16.0-0.*.x86_64.rpm ../RPMS/x86_64/kms-elements-devel-6.16.0-0.*.x86_64.rpm

rpmbb kms-filters.spec
yumi ../RPMS/x86_64/kms-filters-6.16.0-0.*.x86_64.rpm ../RPMS/x86_64/kms-filters-devel-6.16.0-0.*.x86_64.rpm

yumi websocketpp-devel --disablerepo=* --enablerepo=kurento

yumbd kurento-media-server.spec
rpmbb kurento-media-server.spec
yumi ../RPMS/x86_64/kurento-media-server-6.16.0-0.*.x86_64.rpm

rpmbb kms.spec
yumi ../RPMS/x86_64/kms-6.16.0-0.*.x86_64.rpm

yumi createrepo_c --disablerepo=* --enablerepo=kurento
createrepo_c --update --simple-md-filenames /root/rpmbuild/RPMS
yum clean metadata

# GST_DEBUG="3,Kurento*:4,kms*:4" GST_DEBUG_NO_COLOR=1 LD_LIBRARY_PATH=/opt/kms/lib64 kurento-media-server -d /var/log/kurento -n 5
#
# GST_DEBUG="3,Kurento*:4,kms*:4" GST_DEBUG_NO_COLOR=1 kurento-media-server -d /var/log/kurento -n 5
