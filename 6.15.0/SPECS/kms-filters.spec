%define commit 6d4bf70
%define kms_libdir /opt/kms/lib64

Summary: Filter elements for Kurento Media Server
Name: kms-filters
Version: 6.15.0
Release: 0%{?dist}
License: Apache 2.0
Group: Applications/Communications
URL: https://github.com/Kurento/kms-filters
#Source0: Kurento-%{name}-%{commit}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: kms-core kms-elements
BuildRequires: kms-core-devel kms-elements-devel
BuildRequires: opencv-devel
BuildRequires: libsoup-devel >= 2.40

%description
The kms-filters project contains filter elements for the Kurento Media Server

%package devel
Summary: Filter elements for Kurento Media Server
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The kms-filters project contains filter elements for the Kurento Media Server

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
mv %{buildroot}%{_datadir}/cmake-* %{buildroot}%{_datadir}/cmake

mkdir -p %{buildroot}%{kms_libdir}
mv %{buildroot}%{_libdir}/gstreamer-1.5 %{buildroot}%{kms_libdir}

%clean
rm -rf %{buildroot}


%post
/sbin/ldconfig
ln -sf /usr/share/OpenCV /usr/share/opencv

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{kms_libdir}/gstreamer-*/*.so
%{_libdir}/kurento/modules/*.so
%{_datadir}/kurento/modules/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_includedir}/*
%{_datadir}/cmake/*
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.a


%changelog
