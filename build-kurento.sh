#!/bin/bash -i

set -e

yume dyninst

cd /root/rpmbuild/RPMS/boost-1.55

yumi boost-1.55.0-8.el7.x86_64.rpm boost-atomic-1.55.0-8.el7.x86_64.rpm boost-context-1.55.0-8.el7.x86_64.rpm boost-coroutine-1.55.0-8.el7.x86_64.rpm boost-date-time-1.55.0-8.el7.x86_64.rpm boost-devel-1.55.0-8.el7.x86_64.rpm boost-filesystem-1.55.0-8.el7.x86_64.rpm boost-math-1.55.0-8.el7.x86_64.rpm boost-random-1.55.0-8.el7.x86_64.rpm boost-regex-1.55.0-8.el7.x86_64.rpm boost-serialization-1.55.0-8.el7.x86_64.rpm boost-system-1.55.0-8.el7.x86_64.rpm boost-test-1.55.0-8.el7.x86_64.rpm boost-thread-1.55.0-8.el7.x86_64.rpm boost-timer-1.55.0-8.el7.x86_64.rpm boost-chrono-1.55.0-8.el7.x86_64.rpm boost-locale-1.55.0-8.el7.x86_64.rpm boost-log-1.55.0-8.el7.x86_64.rpm boost-python-1.55.0-8.el7.x86_64.rpm boost-graph-1.55.0-8.el7.x86_64.rpm boost-signals-1.55.0-8.el7.x86_64.rpm boost-iostreams-1.55.0-8.el7.x86_64.rpm boost-program-options-1.55.0-8.el7.x86_64.rpm boost-wave-1.55.0-8.el7.x86_64.rpm

cd /root/rpmbuild/RPMS/ffmpeg

yumi ffmpeg-3.1.4-1.el7.x86_64.rpm ffmpeg-devel-3.1.4-1.el7.x86_64.rpm ffmpeg-libs-3.1.4-1.el7.x86_64.rpm libavdevice-3.1.4-1.el7.x86_64.rpm x264-0.148-7.20160614gita5e06b9.el7.x86_64.rpm x264-devel-0.148-7.20160614gita5e06b9.el7.x86_64.rpm x264-libs-0.148-7.20160614gita5e06b9.el7.x86_64.rpm x265-1.9-1.el7.x86_64.rpm x265-devel-1.9-1.el7.x86_64.rpm x265-libs-1.9-1.el7.x86_64.rpm xvidcore-1.3.4-2.el7.x86_64.rpm xvidcore-devel-1.3.4-2.el7.x86_64.rpm fdk-aac-0.1.5-0.1.gita0bd8aa.el7.x86_64.rpm fdk-aac-devel-0.1.5-0.1.gita0bd8aa.el7.x86_64.rpm

cd /root/rpmbuild/SPECS

yumbd automake.spec
rpmbb automake.spec
yumi ../RPMS/noarch/automake-1.15-9.el7.noarch.rpm

yumbd source-highlight.spec
rpmbb source-highlight.spec
yumi ../RPMS/x86_64/source-highlight-3.1.8-10.el7.x86_64.rpm ../RPMS/x86_64/source-highlight-devel-3.1.8-10.el7.x86_64.rpm

yumbd opus.spec kms-libsrtp.spec libde265.spec rtmpdump.spec openh264.spec vo-aacenc.spec vo-amrwbenc.spec openjpeg2.spec gstreamer.spec

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

rpmbb openjpeg2.spec
yumd ../RPMS/x86_64/openjpeg2-2.1.0-7.el7.x86_64.rpm
yumi ../RPMS/x86_64/openjpeg2-devel-2.1.0-7.el7.x86_64.rpm ../RPMS/x86_64/openjpeg2-tools-2.1.0-7.el7.x86_64.rpm

rpmbb kms-jsoncpp.spec
yumi ../RPMS/x86_64/kms-jsoncpp-1.6.3-1.el7.x86_64.rpm ../RPMS/x86_64/kms-jsoncpp-devel-1.6.3-1.el7.x86_64.rpm

rpmbb kms-libsrtp.spec
yumi ../RPMS/x86_64/kms-libsrtp-1.5.2-1.el7.x86_64.rpm ../RPMS/x86_64/kms-libsrtp-devel-1.5.2-1.el7.x86_64.rpm

rpmbb kms-usrsctp.spec
yumi ../RPMS/x86_64/kms-usrsctp-0.9.2-1.el7.x86_64.rpm ../RPMS/x86_64/kms-usrsctp-devel-0.9.2-1.el7.x86_64.rpm

rpmbb gstreamer.spec
yumi ../RPMS/x86_64/kms-gstreamer1-1.8.1-1.el7.x86_64.rpm ../RPMS/x86_64/kms-gstreamer1-devel-1.8.1-1.el7.x86_64.rpm

yumbd gst-plugins-base.spec
rpmbb gst-plugins-base.spec
yumi ../RPMS/x86_64/kms-gstreamer1-plugins-base-1.8.1-1.el7.x86_64.rpm ../RPMS/x86_64/kms-gstreamer1-plugins-base-devel-1.8.1-1.el7.x86_64.rpm

yumbd opencv.spec
rpmbb opencv.spec
yumi ../RPMS/x86_64/opencv-2.4.7-6.el7.x86_64.rpm ../RPMS/x86_64/opencv-core-2.4.7-6.el7.x86_64.rpm ../RPMS/x86_64/opencv-devel-2.4.7-6.el7.x86_64.rpm

yumbd faad2.spec
rpmbb faad2.spec
yumi ../RPMS/x86_64/faad2-2.7-6.el7.x86_64.rpm ../RPMS/x86_64/faad2-libs-2.7-6.el7.x86_64.rpm ../RPMS/x86_64/faad2-devel-2.7-6.el7.x86_64.rpm

rpmbb opencore-amr.spec
yumi ../RPMS/x86_64/opencore-amr-0.1.3-4.el7.x86_64.rpm ../RPMS/x86_64/opencore-amr-devel-0.1.3-4.el7.x86_64.rpm

yumbd gst-plugins-bad.spec gst-plugins-good.spec gst-plugins-ugly.spec gst-libav.spec kms-openwebrtc-gst-plugins.spec kms-libnice.spec

rpmbb gst-plugins-bad.spec
yumi ../RPMS/x86_64/kms-gstreamer1-plugins-bad-1.8.1-1.el7.x86_64.rpm ../RPMS/x86_64/kms-gstreamer1-plugins-bad-devel-1.8.1-1.el7.x86_64.rpm

rpmbb gst-plugins-good.spec
yumi ../RPMS/x86_64/kms-gstreamer1-plugins-good-1.8.1-1.el7.x86_64.rpm

rpmbb gst-plugins-ugly.spec
yumi ../RPMS/x86_64/kms-gstreamer1-plugins-ugly-1.8.1-1.el7.x86_64.rpm

rpmbb gst-libav.spec
yumi ../RPMS/x86_64/kms-gstreamer1-libav-1.8.1-1.el7.x86_64.rpm

rpmbb kms-openwebrtc-gst-plugins.spec
yumi ../RPMS/x86_64/kms-openwebrtc-gst-plugins-0.10.0-1.el7.x86_64.rpm ../RPMS/x86_64/kms-openwebrtc-gst-plugins-devel-0.10.0-1.el7.x86_64.rpm

rpmbb kms-libnice.spec
yumi ../RPMS/x86_64/kms-libnice-0.1.15-1.el7.x86_64.rpm ../RPMS/x86_64/kms-libnice-devel-0.1.15-1.el7.x86_64.rpm

yumbd kurento-module-creator.spec
rpmbb kurento-module-creator.spec
yumi ../RPMS/x86_64/kurento-module-creator-6.9.1-1.el7.x86_64.rpm

rpmbb kms-cmake-utils.spec
yumi ../RPMS/x86_64/kms-cmake-utils-6.9.1-1.el7.x86_64.rpm

rpmbb kms-jsonrpc.spec
yumi ../RPMS/x86_64/kms-jsonrpc-6.9.1-1.el7.x86_64.rpm ../RPMS/x86_64/kms-jsonrpc-devel-6.9.1-1.el7.x86_64.rpm

yumbd kms-core.spec
rpmbb kms-core.spec
yumi ../RPMS/x86_64/kms-core-6.9.1-1.el7.x86_64.rpm ../RPMS/x86_64/kms-core-devel-6.9.1-1.el7.x86_64.rpm

yumbd kms-elements.spec
rpmbb kms-elements.spec
yumi ../RPMS/x86_64/kms-elements-6.9.1-1.el7.x86_64.rpm ../RPMS/x86_64/kms-elements-devel-6.9.1-1.el7.x86_64.rpm

rpmbb kms-filters.spec
yumi ../RPMS/x86_64/kms-filters-6.9.1-1.el7.x86_64.rpm ../RPMS/x86_64/kms-filters-devel-6.9.1-1.el7.x86_64.rpm

rpmbb kurento-media-server.spec

rpmbb kms.spec
