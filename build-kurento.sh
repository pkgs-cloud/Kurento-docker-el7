#!/bin/bash -i

set -e

cd /root/rpmbuild/RPMS/ffmpeg

yumi ffmpeg-3.1.4-1.el7.x86_64.rpm ffmpeg-devel-3.1.4-1.el7.x86_64.rpm ffmpeg-libs-3.1.4-1.el7.x86_64.rpm libavdevice-3.1.4-1.el7.x86_64.rpm x264-0.148-7.20160614gita5e06b9.el7.x86_64.rpm x264-devel-0.148-7.20160614gita5e06b9.el7.x86_64.rpm x264-libs-0.148-7.20160614gita5e06b9.el7.x86_64.rpm x265-1.9-1.el7.x86_64.rpm x265-devel-1.9-1.el7.x86_64.rpm x265-libs-1.9-1.el7.x86_64.rpm xvidcore-1.3.4-2.el7.x86_64.rpm xvidcore-devel-1.3.4-2.el7.x86_64.rpm fdk-aac-0.1.5-0.1.gita0bd8aa.el7.x86_64.rpm fdk-aac-devel-0.1.5-0.1.gita0bd8aa.el7.x86_64.rpm || true

cd /root/rpmbuild/SPECS

yumbd kms-boost.spec
rpmbb kms-boost.spec

cd /root/rpmbuild/RPMS/x86_64

yumi kms-boost-1.55.0-12.el7.x86_64.rpm kms-boost-atomic-1.55.0-12.el7.x86_64.rpm kms-boost-context-1.55.0-12.el7.x86_64.rpm kms-boost-coroutine-1.55.0-12.el7.x86_64.rpm kms-boost-date-time-1.55.0-12.el7.x86_64.rpm kms-boost-devel-1.55.0-12.el7.x86_64.rpm kms-boost-filesystem-1.55.0-12.el7.x86_64.rpm kms-boost-math-1.55.0-12.el7.x86_64.rpm kms-boost-random-1.55.0-12.el7.x86_64.rpm kms-boost-regex-1.55.0-12.el7.x86_64.rpm kms-boost-serialization-1.55.0-12.el7.x86_64.rpm kms-boost-system-1.55.0-12.el7.x86_64.rpm kms-boost-test-1.55.0-12.el7.x86_64.rpm kms-boost-thread-1.55.0-12.el7.x86_64.rpm kms-boost-timer-1.55.0-12.el7.x86_64.rpm kms-boost-chrono-1.55.0-12.el7.x86_64.rpm kms-boost-locale-1.55.0-12.el7.x86_64.rpm kms-boost-log-1.55.0-12.el7.x86_64.rpm kms-boost-python-1.55.0-12.el7.x86_64.rpm kms-boost-graph-1.55.0-12.el7.x86_64.rpm kms-boost-signals-1.55.0-12.el7.x86_64.rpm kms-boost-iostreams-1.55.0-12.el7.x86_64.rpm kms-boost-program-options-1.55.0-12.el7.x86_64.rpm kms-boost-wave-1.55.0-12.el7.x86_64.rpm

cd /root/rpmbuild/SPECS

yumbd automake.spec
rpmbb automake.spec
yumi ../RPMS/noarch/automake-1.15-9.el7.noarch.rpm

yumbd opus.spec libde265.spec rtmpdump.spec openh264.spec vo-aacenc.spec vo-amrwbenc.spec openjpeg2.spec kms-libsrtp.spec kms-gstreamer.spec

rpmbb opus.spec
yumi ../RPMS/x86_64/opus-1.1.3-1.el7.x86_64.rpm ../RPMS/x86_64/opus-devel-1.1.3-1.el7.x86_64.rpm

rpmbb libde265.spec
yumi ../RPMS/x86_64/libde265-1.0.2-2.el7.x86_64.rpm ../RPMS/x86_64/libde265-devel-1.0.2-2.el7.x86_64.rpm

rpmbb rtmpdump.spec
yumi ../RPMS/x86_64/librtmp-2.4-7.20160224.gitfa8646d.el7.x86_64.rpm ../RPMS/x86_64/librtmp-devel-2.4-7.20160224.gitfa8646d.el7.x86_64.rpm

rpmbb openh264.spec
yumi ../RPMS/x86_64/openh264-1.5.0-3.20160606git2610ab1.el7.x86_64.rpm ../RPMS/x86_64/openh264-devel-1.5.0-3.20160606git2610ab1.el7.x86_64.rpm

rpmbb vo-aacenc.spec vo-amrwbenc.spec
yumi ../RPMS/x86_64/vo-aacenc-0.1.2-3.el7.x86_64.rpm ../RPMS/x86_64/vo-aacenc-devel-0.1.2-3.el7.x86_64.rpm ../RPMS/x86_64/vo-amrwbenc-0.1.3-2.el7.x86_64.rpm ../RPMS/x86_64/vo-amrwbenc-devel-0.1.3-2.el7.x86_64.rpm

#rpmbb openjpeg2.spec
#yumd ../RPMS/x86_64/openjpeg2-2.1.0-7.el7.x86_64.rpm
#yumi ../RPMS/x86_64/openjpeg2-devel-2.1.0-7.el7.x86_64.rpm ../RPMS/x86_64/openjpeg2-tools-2.1.0-7.el7.x86_64.rpm

rpmbb kms-jsoncpp.spec
yumi ../RPMS/x86_64/kms-jsoncpp-1.6.3-1.el7.x86_64.rpm ../RPMS/x86_64/kms-jsoncpp-devel-1.6.3-1.el7.x86_64.rpm

rpmbb kms-libsrtp.spec
yumi ../RPMS/x86_64/kms-libsrtp-1.5.2-1.el7.x86_64.rpm ../RPMS/x86_64/kms-libsrtp-devel-1.5.2-1.el7.x86_64.rpm

rpmbb kms-usrsctp.spec
yumi ../RPMS/x86_64/kms-usrsctp-0.9.2-1.el7.x86_64.rpm ../RPMS/x86_64/kms-usrsctp-devel-0.9.2-1.el7.x86_64.rpm

rpmbb kms-gstreamer.spec
yumi ../RPMS/x86_64/kms-gstreamer1-1.8.1-1.el7.x86_64.rpm ../RPMS/x86_64/kms-gstreamer1-devel-1.8.1-1.el7.x86_64.rpm

yumbd kms-gst-plugins-base.spec
rpmbb kms-gst-plugins-base.spec
yumi ../RPMS/x86_64/kms-gstreamer1-plugins-base-1.8.1-1.el7.x86_64.rpm ../RPMS/x86_64/kms-gstreamer1-plugins-base-devel-1.8.1-1.el7.x86_64.rpm

yumbd opencv.spec
rpmbb opencv.spec
yumi ../RPMS/x86_64/opencv-2.4.7-6.el7.x86_64.rpm ../RPMS/x86_64/opencv-core-2.4.7-6.el7.x86_64.rpm ../RPMS/x86_64/opencv-devel-2.4.7-6.el7.x86_64.rpm

yumbd faad2.spec
rpmbb faad2.spec
yumi ../RPMS/x86_64/faad2-2.7-6.el7.x86_64.rpm ../RPMS/x86_64/faad2-libs-2.7-6.el7.x86_64.rpm ../RPMS/x86_64/faad2-devel-2.7-6.el7.x86_64.rpm

rpmbb opencore-amr.spec
yumi ../RPMS/x86_64/opencore-amr-0.1.3-4.el7.x86_64.rpm ../RPMS/x86_64/opencore-amr-devel-0.1.3-4.el7.x86_64.rpm

yumbd kms-gst-plugins-bad.spec kms-gst-plugins-good.spec kms-gst-plugins-ugly.spec kms-gst-libav.spec kms-openwebrtc-gst-plugins.spec kms-libnice.spec

rpmbb kms-gst-plugins-bad.spec
yumi ../RPMS/x86_64/kms-gstreamer1-plugins-bad-1.8.1-2.el7.x86_64.rpm ../RPMS/x86_64/kms-gstreamer1-plugins-bad-devel-1.8.1-2.el7.x86_64.rpm

rpmbb kms-gst-plugins-good.spec
yumi ../RPMS/x86_64/kms-gstreamer1-plugins-good-1.8.1-2.el7.x86_64.rpm

rpmbb kms-gst-plugins-ugly.spec
yumi ../RPMS/x86_64/kms-gstreamer1-plugins-ugly-1.8.1-1.el7.x86_64.rpm

rpmbb kms-gst-libav.spec
yumi ../RPMS/x86_64/kms-gstreamer1-libav-1.8.1-1.el7.x86_64.rpm

rpmbb kms-openwebrtc-gst-plugins.spec
yumi ../RPMS/x86_64/kms-openwebrtc-gst-plugins-0.10.0-1.el7.x86_64.rpm ../RPMS/x86_64/kms-openwebrtc-gst-plugins-devel-0.10.0-1.el7.x86_64.rpm

rpmbb kms-libnice.spec
yumi ../RPMS/x86_64/kms-libnice-0.1.15-3.el7.x86_64.rpm ../RPMS/x86_64/kms-libnice-devel-0.1.15-3.el7.x86_64.rpm

yumbd kurento-module-creator.spec
rpmbb kurento-module-creator.spec
yumi ../RPMS/x86_64/kurento-module-creator-6.10.0-1.el7.x86_64.rpm

rpmbb kms-cmake-utils.spec
yumi ../RPMS/x86_64/kms-cmake-utils-6.10.0-1.el7.x86_64.rpm

rpmbb kms-jsonrpc.spec
yumi ../RPMS/x86_64/kms-jsonrpc-6.10.0-1.el7.x86_64.rpm ../RPMS/x86_64/kms-jsonrpc-devel-6.10.0-1.el7.x86_64.rpm

yumbd kms-core.spec
rpmbb kms-core.spec
yumi ../RPMS/x86_64/kms-core-6.10.0-1.el7.x86_64.rpm ../RPMS/x86_64/kms-core-devel-6.10.0-1.el7.x86_64.rpm

yumbd kms-elements.spec
rpmbb kms-elements.spec
yumi ../RPMS/x86_64/kms-elements-6.10.0-1.el7.x86_64.rpm ../RPMS/x86_64/kms-elements-devel-6.10.0-1.el7.x86_64.rpm

rpmbb kms-filters.spec
yumi ../RPMS/x86_64/kms-filters-6.10.0-1.el7.x86_64.rpm ../RPMS/x86_64/kms-filters-devel-6.10.0-1.el7.x86_64.rpm

rpmbb kurento-media-server.spec
yumi ../RPMS/x86_64/kurento-media-server-6.10.0-1.el7.x86_64.rpm

rpmbb kms.spec

yumbd createrepo_c.spec
rpmbb createrepo_c.spec
yumi ../RPMS/x86_64/createrepo_c-0.12.2-1.el7.x86_64.rpm ../RPMS/x86_64/createrepo_c-libs-0.12.2-1.el7.x86_64.rpm

createrepo_c --update --simple-md-filenames /root/rpmbuild/RPMS
