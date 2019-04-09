%define commit 0951b47
%define kms_libdir /opt/kms/lib64

Summary: Kurento JsonRPC protocol implementation
Name: kms-jsonrpc
Version: 6.10.0
Release: 1%{?dist}
License: GPLv2+
Group: Applications/Communications
URL: https://github.com/Kurento/kms-jsonrpc
#Source0: Kurento-kms-jsonrpc-%{commit}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: kms-jsoncpp
BuildRequires: kms-cmake-utils
BuildRequires: kms-jsoncpp-devel
BuildRequires: kms-boost
BuildRequires: kms-boost-test

%description
Kurento JsonRPC protocol implementation

%package devel
Summary: Kurento JsonRPC protocol implementation
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Kurento JsonRPC protocol implementation

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

mkdir -p build
cd build
cmake -DBoost_NO_SYSTEM_PATHS=TRUE \
    -DBOOST_ROOT:PATHNAME=/opt/kms \
    -DBoost_NO_BOOST_CMAKE=TRUE \
    -DCMAKE_INSTALL_PREFIX:PATH=/usr \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_BUILD_TYPE=Release -G "Unix Makefiles" ..
make %{?_smp_mflags}


%install
export PKG_CONFIG_PATH=%{kms_libdir}/pkgconfig
export LD_RUN_PATH=%{kms_libdir}
export LD_LIBRARY_PATH=%{kms_libdir}
export LIBRARY_PATH=%{kms_libdir}

rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}
mv %{buildroot}/usr/share/cmake-* %{buildroot}/usr/share/cmake

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/*
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.a


%changelog
