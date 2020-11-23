%define commit 514f411
%define kms_libdir /opt/kms/lib64

Summary: Core library of Kurento Media Server
Name: kms-core
Version: 6.15.0
Release: 0%{?dist}
License: GPLv2+
Group: Applications/Communications
URL: https://github.com/Kurento/kms-core
#Source0: Kurento-%{name}-%{commit}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: kms-jsonrpc kms-jsoncpp
BuildRequires: kms-jsonrpc-devel kms-jsoncpp-devel kms-cmake-utils kurento-module-creator
BuildRequires: kms-gstreamer1-devel >= 1.8.1, kms-gstreamer1-plugins-base-devel
BuildRequires: kms-openwebrtc-gst-plugins-devel
BuildRequires: kms-cmake-utils
BuildRequires: kms-boost
BuildRequires: kms-boost-system kms-boost-filesystem kms-boost-program-options kms-boost-test kms-boost-thread kms-boost-log kms-boost-regex
BuildRequires: libsigc++20-devel
BuildRequires: glibmm24-devel
BuildRequires: libuuid-devel >= 2.23
BuildRequires: libvpx-devel >= 1.3.0

%description
The kms-core project contains core elements needed for the Kurento Media Server

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Development files for %{name}

%prep
%setup -c -n %{name}-%{version}-%{commit} -T -D
if [ ! -d .git ]; then
    git clone https://github.com/Kurento/%{name}.git .
    git checkout %{commit}
fi

%build
export PKG_CONFIG_PATH=%{kms_libdir}/pkgconfig
export LD_RUN_PATH=%{kms_libdir}
export LD_LIBRARY_PATH=%{kms_libdir}
export LIBRARY_PATH=%{kms_libdir}
export CPATH=/opt/kms/include

mkdir -p build
cd build
cmake -DBOOST_ROOT:PATHNAME=/opt/kms \
    -DBoost_NO_BOOST_CMAKE=TRUE \
    -DCMAKE_INSTALL_PREFIX:PATH=/usr \
    -DCMAKE_BUILD_TYPE=Release ..

make %{?_smp_mflags}


%install
export PKG_CONFIG_PATH={kms_libdir}/pkgconfig
export LD_RUN_PATH=%{kms_libdir}
export LD_LIBRARY_PATH=%{kms_libdir}
export LIBRARY_PATH=%{kms_libdir}

rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}
mv %{buildroot}/usr/etc %{buildroot}
mv %{buildroot}%{_datadir}/cmake-* %{buildroot}%{_datadir}/cmake

mkdir -p %{buildroot}%{kms_libdir}
mv %{buildroot}%{_libdir}/gstreamer-* %{buildroot}%{kms_libdir}

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_sysconfdir}/kurento/modules/kurento
%{_libdir}/*.so.*
%{kms_libdir}/gstreamer-*/*.so
%{_libdir}/kurento/modules/*.so

%{_datadir}/kurento/modules/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/cmake/*
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.a


%changelog
