#!/bin/bash -i

set -e

# Versions
KMS=6.9.1-1
GST=1.8.1-1
JSONCPP=1.6.3-1
LIBNICE=0.1.15-1
LIBSRTP=1.5.2-1
OPENWEBRTC=0.10.0-1
USRSCTP=0.9.2-1
OPUS=1.1.3-1
FAAD=2.7-6
BOOST=1.55.0-8
LIBDE265=1.0.2-2
LIBRTMP=2.4-7.20160224.gitfa8646d
OPENCOREAMR=0.1.3-4
OPENCV=2.4.7-6
OPENH264=1.5.0-3.20160606git2610ab1
RTMPDUMP=2.4-7.20160224.gitfa8646d
VOAAC=0.1.2-3
VOAMRWB=0.1.3-2

# Kurento Packages
PACKAGES=(
    kms-$KMS
    kurento-media-server-$KMS
    kms-cmake-utils-$KMS
    kms-core-$KMS
    kms-elements-$KMS
    kms-filters-$KMS
    kms-jsonrpc-$KMS
    kms-jsoncpp-$JSONCPP
    kms-libnice-$LIBNICE
    kms-libsrtp-$LIBSRTP
    kms-openwebrtc-gst-plugins-$OPENWEBRTC
    kms-usrsctp-$USRSCTP
    kms-gstreamer1-$GST
    kms-gstreamer1-libav-$GST
    kms-gstreamer1-plugins-bad-$GST
    kms-gstreamer1-plugins-base-$GST
    kms-gstreamer1-plugins-good-$GST
    kms-gstreamer1-plugins-ugly-$GST
    opus-$OPUS
    faad2-libs-$FAAD
    libde265-$LIBDE265
    librtmp-$LIBRTMP
    opencore-amr-$OPENCOREAMR
    opencv-$OPENCV
    opencv-core-$OPENCV
    openh264-$OPENH264
    rtmpdump-$RTMPDUMP
    vo-aacenc-$VOAAC
    vo-amrwbenc-$VOAMRWB
)

pkgs=""
for pkg in "${PACKAGES[@]}"; do
    pkgs="$pkgs RPMS/x86_64/$pkg.el7.x86_64.rpm"
done

#Boost Packages
PACKAGES=(
    boost-filesystem
    boost-chrono
    boost-log
    boost-wave
    boost-graph
    boost-atomic
    boost-iostreams
    boost-test
    boost-date-time
    boost-timer
    boost-random
    boost-system
    boost-regex
    boost-program-options
    boost-coroutine
    boost-locale
    boost-math
    boost-python
    boost-thread
    boost-context
    boost-signals
    boost-serialization
    boost
)

for pkg in "${PACKAGES[@]}"; do
    pkgs="$pkgs RPMS/boost-1.55/$pkg-$BOOST.el7.x86_64.rpm"
done

# Other Packages
PACKAGES=(
    x264-libs-0.148-7.20160614gita5e06b9
    x265-libs-1.9-1
)

for pkg in "${PACKAGES[@]}"; do
    pkgs="$pkgs RPMS/ffmpeg/$pkg.el7.x86_64.rpm"
done

yum install epel-release -y
yum update -y
yum install mc wget nano patch yum-utils deltarpm which aspell-en -y

yum install $pkgs
