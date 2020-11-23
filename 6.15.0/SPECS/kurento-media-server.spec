%define commit a6d4800
%define kms_libdir /opt/kms/lib64

Summary: Kurento Media Server
Name: kurento-media-server
Version: 6.15.0
Release: 0%{?dist}
License: Apache 2.0
Group: Applications/Communications
URL: https://github.com/Kurento/kurento-media-server
#Source0: Kurento-kurento-media-server-%{commit}.tar.gz
Source1: kms.service
Source2: kms.sysconfig
#Patch0: loadConfig.cpp.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: kms-core kms-elements kms-libnice kms-jsonrpc kms-usrsctp
Requires: kms-boost
Requires: kms-boost-system kms-boost-filesystem kms-boost-program-options kms-boost-test kms-boost-thread kms-boost-log kms-boost-regex
Requires: kms-libsrtp >= 1.5.2
Requires: opus >= 1.1.0
Requires: openssl-libs
BuildRequires: kms-jsonrpc-devel
# Boost 1.55
BuildRequires: kms-boost
BuildRequires: kms-boost-system kms-boost-filesystem kms-boost-program-options kms-boost-test kms-boost-thread kms-boost-log kms-boost-regex
BuildRequires: libsigc++20-devel
BuildRequires: glibmm24-devel
BuildRequires: libevent-devel >= 2.0
BuildRequires: kms-libsrtp-devel >= 1.5.2
BuildRequires: opus-devel >= 1.1.0
BuildRequires: websocketpp-devel

%description
Kurento Media Server is the Kurento's core element.
It is responsible for media transmission, processing, loading and recording.
It is implemented in low level technologies based on GStreamer to optimize
the resource consumption. It provides the following features:
- Networked streaming protocols, including HTTP, RTP and WebRTC
- Group communications (MCUs and SFUs functionality) supporting both media mixing
  and media routing/dispatching
- Generic support for computational vision and augmented reality filters
- Media storage supporting writing operations for WebM and MP4 and playing
  in all formats supported by GStreamer
- Automatic media transcodification between any of the codecs supported
  by GStreamer including VP8, H.264, H.263, AMR, OPUS, Speex, G.711, etc.

%prep
%setup -c -n %{name}-%{version}-%{commit} -T -D
#%patch0
if [ ! -d .git ]; then
    git clone https://github.com/Kurento/%{name}.git .
    git checkout %{commit}
fi

%build
export PKG_CONFIG_PATH=%{kms_libdir}/pkgconfig
export LD_RUN_PATH=%{kms_libdir}
export LD_LIBRARY_PATH=%{kms_libdir}
export LIBRARY_PATH=%{kms_libdir}

mkdir -p build
cd build

cmake -DBoost_NO_SYSTEM_PATHS=TRUE \
    -DBOOST_ROOT:PATHNAME=/opt/kms \
    -DBoost_NO_BOOST_CMAKE=TRUE \
    -DCMAKE_INSTALL_PREFIX:PATH=/usr \
    -DCMAKE_BUILD_TYPE=Release ..

make %{?_smp_mflags}


%install
export PKG_CONFIG_PATH=%{kms_libdir}/pkgconfig
export LD_RUN_PATH=%{kms_libdir}
export LD_LIBRARY_PATH=%{kms_libdir}
export LIBRARY_PATH=%{kms_libdir}

rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}
mv %{buildroot}/usr/etc %{buildroot}

install -p -D -m 0644 %{SOURCE1} \
    %{buildroot}%{_unitdir}/kms.service

install -p -D -m 0644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/sysconfig/kms

install -p -d -m 0700 %{buildroot}%{_localstatedir}/kurento
install -p -d -m 0700 %{buildroot}%{_localstatedir}/log/kurento

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{kms_libdir}" > %{buildroot}/etc/ld.so.conf.d/kms.conf

%clean
rm -rf %{buildroot}


%post
/sbin/ldconfig
%systemd_post kms.service

%preun
%systemd_preun kms.service

%postun
%systemd_postun kms.service
/sbin/ldconfig

%files
%defattr(-,root,root,-)
#doc ChangeLog.md README.md LICENSE
%doc README.md LICENSE
%config(noreplace) %{_sysconfdir}/kurento
%config(noreplace) %{_sysconfdir}/sysconfig/kms
%config %{_sysconfdir}/ld.so.conf.d/kms.conf
%{_bindir}/*
%{_datadir}/kurento/*
%{_localstatedir}/*
%{_unitdir}/kms.service

%changelog
