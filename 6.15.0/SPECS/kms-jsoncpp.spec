%define commit 15940be

%global _prefix /opt/kms

Summary: Kurento JSON library
Name: kms-jsoncpp
Version: 1.6.3
Release: 1%{?dist}
License: MIT
Group: Applications/Communications
URL: https://github.com/Kurento/jsoncpp
#Source0: Kurento-jsoncpp-%{commit}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: cmake


%description
JsonCpp is a C++ library that allows manipulating JSON values,
including serialization and deserialization to and from strings.
It can also preserve existing comment in unserialization/serialization
steps, making it a convenient format to store user input files.

%package devel
Summary: Kurento JSON library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -c -n %{name}-%{version}-%{commit} -T -D
if [ ! -d .git ]; then
    git clone https://github.com/Kurento/jsoncpp.git .
    git checkout %{commit}
fi

%build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DBUILD_SHARED_LIBS=ON -DBUILD_STATIC_LIBS=ON -DLIB_SUFFIX=64 -DCMAKE_BUILD_TYPE=Release -G "Unix Makefiles" ..
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}


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
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.a


%changelog
