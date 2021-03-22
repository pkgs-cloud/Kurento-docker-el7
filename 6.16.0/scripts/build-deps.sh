#!/bin/bash -i

set -e

source $(dirname $(realpath $0))/distro-deps.sh

chown -R root:root /root/rpmbuild

cd /root/rpmbuild/SPECS

for spec in `ls *.spec`; do
    rpmsrc $spec
done

rpmbb opencore-amr.spec
yumi ../RPMS/x86_64/opencore-amr-0.1.3-4.*.x86_64.rpm ../RPMS/x86_64/opencore-amr-devel-0.1.3-4.*.x86_64.rpm

rpmbb vo-aacenc.spec vo-amrwbenc.spec
yumi ../RPMS/x86_64/vo-aacenc-0.1.2-3.*.x86_64.rpm ../RPMS/x86_64/vo-aacenc-devel-0.1.2-3.*.x86_64.rpm ../RPMS/x86_64/vo-amrwbenc-0.1.3-2.*.x86_64.rpm ../RPMS/x86_64/vo-amrwbenc-devel-0.1.3-2.*.x86_64.rpm

yumbd x265.spec
rpmbb x265.spec
yumi ../RPMS/x86_64/x265-libs-2.9-3.*.x86_64.rpm ../RPMS/x86_64/x265-devel-2.9-3.*.x86_64.rpm

rpmbb xvidcore.spec
yumi ../RPMS/x86_64/xvidcore-1.3.4-2.*.x86_64.rpm ../RPMS/x86_64/xvidcore-devel-1.3.4-2.*.x86_64.rpm

rpmbb fdk-aac.spec
yumi ../RPMS/x86_64/fdk-aac-0.1.5-0.1.gita0bd8aa.*.x86_64.rpm ../RPMS/x86_64/fdk-aac-devel-0.1.5-0.1.gita0bd8aa.*.x86_64.rpm

yumbd faad2.spec
rpmbb faad2.spec
yumi ../RPMS/x86_64/faad2-libs-2.7-9.*.x86_64.rpm ../RPMS/x86_64/faad2-devel-2.7-9.*.x86_64.rpm

yumbd x264.spec --define '_with_bootstrap 1'
rpmbb x264.spec --define '_with_bootstrap 1'
yumi ../RPMS/x86_64/x264-libs-0.148-23.20170521gitaaa9aa8_bootstrap.*.x86_64.rpm ../RPMS/x86_64/x264-devel-0.148-23.20170521gitaaa9aa8_bootstrap.*.x86_64.rpm

yumbd libva.spec
rpmbb libva.spec
yumi ../RPMS/x86_64/libva-1.8.3-1.*.x86_64.rpm ../RPMS/x86_64/libva-devel-1.8.3-1.*.x86_64.rpm

yumbd opus.spec
rpmbb opus.spec
yumi ../RPMS/x86_64/opus-1.1.3-1.*.x86_64.rpm ../RPMS/x86_64/opus-devel-1.1.3-1.*.x86_64.rpm

yumbd ffmpeg.spec
rpmbb ffmpeg.spec
yumi ../RPMS/x86_64/ffmpeg-libs-4.2.4-1.*.x86_64.rpm ../RPMS/x86_64/libavdevice-4.2.4-1.*.x86_64.rpm ../RPMS/x86_64/ffmpeg-devel-4.2.4-1.*.x86_64.rpm

yumbd gpac.spec
rpmbb gpac.spec

yumi ../RPMS/x86_64/gpac-libs-0.7.1-8.*.x86_64.rpm ../RPMS/x86_64/gpac-devel-0.7.1-8.*.x86_64.rpm

rpmbb x264.spec
rpm -ev x264-devel x264-libs --nodeps
yumi ../RPMS/x86_64/x264-libs-0.148-23.20170521gitaaa9aa8.*.x86_64.rpm ../RPMS/x86_64/x264-devel-0.148-23.20170521gitaaa9aa8.*.x86_64.rpm

yumbd libde265.spec
rpmbb libde265.spec
yumi ../RPMS/x86_64/libde265-1.0.2-6.*.x86_64.rpm ../RPMS/x86_64/libde265-devel-1.0.2-6.*.x86_64.rpm

yumbd automake.spec
rpmbb automake.spec
yumi ../RPMS/noarch/automake-1.15-9.*.noarch.rpm

yumbd rtmpdump.spec
rpmbb rtmpdump.spec
yumi ../RPMS/x86_64/librtmp-2.4-7.20160224.gitfa8646d.*.x86_64.rpm ../RPMS/x86_64/librtmp-devel-2.4-7.20160224.gitfa8646d.*.x86_64.rpm

yumbd openh264.spec
rpmbb openh264.spec
yumi ../RPMS/x86_64/openh264-1.5.0-4.*.x86_64.rpm ../RPMS/x86_64/openh264-devel-1.5.0-4.*.x86_64.rpm

yumbd kms-openjpeg2.spec
rpmbb kms-openjpeg2.spec
yumi ../RPMS/x86_64/kms-openjpeg2-2.1.0-7.*.x86_64.rpm ../RPMS/x86_64/kms-openjpeg2-devel-2.1.0-7.*.x86_64.rpm

yumbd kms-boost.spec
rpmbb kms-boost.spec --without python3

cd /root/rpmbuild/RPMS/x86_64
yumi kms-boost-1.55.0-12.*.x86_64.rpm \
  kms-boost-atomic-1.55.0-12.*.x86_64.rpm \
  kms-boost-context-1.55.0-12.*.x86_64.rpm \
  kms-boost-coroutine-1.55.0-12.*.x86_64.rpm \
  kms-boost-date-time-1.55.0-12.*.x86_64.rpm \
  kms-boost-devel-1.55.0-12.*.x86_64.rpm \
  kms-boost-filesystem-1.55.0-12.*.x86_64.rpm \
  kms-boost-math-1.55.0-12.*.x86_64.rpm \
  kms-boost-random-1.55.0-12.*.x86_64.rpm \
  kms-boost-regex-1.55.0-12.*.x86_64.rpm \
  kms-boost-serialization-1.55.0-12.*.x86_64.rpm \
  kms-boost-system-1.55.0-12.*.x86_64.rpm \
  kms-boost-test-1.55.0-12.*.x86_64.rpm \
  kms-boost-thread-1.55.0-12.*.x86_64.rpm \
  kms-boost-timer-1.55.0-12.*.x86_64.rpm \
  kms-boost-chrono-1.55.0-12.*.x86_64.rpm \
  kms-boost-locale-1.55.0-12.*.x86_64.rpm \
  kms-boost-log-1.55.0-12.*.x86_64.rpm \
  kms-boost-python-1.55.0-12.*.x86_64.rpm \
  kms-boost-graph-1.55.0-12.*.x86_64.rpm \
  kms-boost-signals-1.55.0-12.*.x86_64.rpm \
  kms-boost-iostreams-1.55.0-12.*.x86_64.rpm \
  kms-boost-program-options-1.55.0-12.*.x86_64.rpm \
  kms-boost-wave-1.55.0-12.*.x86_64.rpm

cd /root/rpmbuild/SPECS

yumbd websocketpp.spec
rpmbb websocketpp.spec
yumi ../RPMS/noarch/websocketpp-devel-0.8.2-4.*.noarch.rpm

yumi python3-pip python3 python3-setuptools python3-devel python-rpm-macros
yumbd meson.spec
rpmbb meson.spec
yumi ../RPMS/noarch/meson-0.55.1-1.*.noarch.rpm

yumbd drpm.spec
rpmbb drpm.spec
yumi ../RPMS/x86_64/drpm-0.5.0-1.*.x86_64.rpm ../RPMS/x86_64/drpm-devel-0.5.0-1.*.x86_64.rpm

yumbd createrepo_c.spec
rpmbb createrepo_c.spec
yumi ../RPMS/x86_64/createrepo_c-0.17.1-1.*.x86_64.rpm ../RPMS/x86_64/createrepo_c-libs-0.17.1-1.*.x86_64.rpm

createrepo_c --update --simple-md-filenames /root/rpmbuild/RPMS
