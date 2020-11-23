%define commit fdbe294
%define kms_libdir /opt/kms/lib64

Summary: Elements for Kurento Media Server
Name: kms-elements
Version: 6.15.0
Release: 0%{?dist}
License: Apache 2.0
Group: Applications/Communications
URL: https://github.com/Kurento/kms-elements
#Source0: Kurento-%{name}-%{commit}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: kms-core kms-openwebrtc-gst-plugins
BuildRequires: kms-core-devel kms-jsonrpc-devel kms-libnice-devel
BuildRequires: kurento-module-creator
BuildRequires: kms-gstreamer1-devel >= 1.8.1, kms-gstreamer1-plugins-base-devel
BuildRequires: kms-openwebrtc-gst-plugins-devel
BuildRequires: kms-boost
BuildRequires: kms-boost-system kms-boost-filesystem kms-boost-program-options kms-boost-test kms-boost-thread kms-boost-log kms-boost-regex
BuildRequires: libsigc++20-devel
BuildRequires: glibmm24-devel
BuildRequires: libevent-devel >= 2.0
BuildRequires: kms-libsrtp-devel >= 1.5.4
BuildRequires: opus-devel >= 1.1.0
BuildRequires: libuuid-devel >= 2.23
BuildRequires: libsoup-devel >= 2.40
BuildRequires: openssl-devel
BuildRequires: gobject-introspection-devel
#BuildRequires: valgrind

%description
The kms-elements project contains elements needed for the Kurento Media Server

%package devel
Summary: Elements for Kurento Media Server
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The kms-elements project contains elements needed for the Kurento Media Server

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
export PKG_CONFIG_PATH=%{kms_libdir}/pkgconfig
export LD_RUN_PATH=%{kms_libdir}
export LD_LIBRARY_PATH=%{kms_libdir}
export LIBRARY_PATH=%{kms_libdir}

rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}
mv %{buildroot}/usr/etc %{buildroot}
mv %{buildroot}/usr/share/cmake-* %{buildroot}/usr/share/cmake

mkdir -p %{buildroot}%{kms_libdir}
mv %{buildroot}%{_libdir}/gstreamer-* %{buildroot}%{kms_libdir}

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
#%doc AUTHORS COPYING ChangeLog NEWS README TODO
%config(noreplace) %{_sysconfdir}/kurento/modules/kurento
%{_libdir}/*.so.*
%{kms_libdir}/gstreamer-*/*.so
%{_libdir}/kurento/modules/*.so
%{_datadir}/kurento/modules/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/cmake/*
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.a
%{_libdir}/*.so


%changelog
