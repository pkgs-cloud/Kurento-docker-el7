
Name:    websocketpp
Summary: C++ WebSocket Protocol Library
Version: 0.8.2
Release: 4%{?dist}

License: BSD
Url:     https://www.zaphoyd.com/websocketpp
Source0: https://github.com/zaphoyd/websocketpp/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: websocketpp.pc
BuildArch: noarch

# put cmake files in share/cmake instead of lib/cmake
Patch1: websocketpp-0.7.0-cmake_noarch.patch

# Switch from ExactVersion to AnyNewerVersion to improve compatibility
# https://cmake.org/cmake/help/v3.0/module/CMakePackageConfigHelpers.html
# Fixes build failure of tomahawk, which uses "find_package(websocketpp 0.2.99 REQUIRED)"
# PR submitted upstream: https://github.com/zaphoyd/websocketpp/pull/740
# Disable check for same 32/64bit-ness in websocketpp-configVersion.cmake by setting CMAKE_SIZEOF_VOID_P
# PR submitted upstream: https://github.com/zaphoyd/websocketpp/pull/770
Patch2: websocketpp-0.8.1-cmake-configversion-compatibility-anynewerversion.patch

# Disable the following tests, which fail occasionally: test_transport, test_transport_asio_timers
Patch3: websocketpp-0.7.0-disable-test_transport-test_transport_asio_timers.patch


BuildRequires:  kms-boost-devel
BuildRequires:  cmake
BuildRequires:  gcc-c++
# needed for tests mostly
BuildRequires:  pkgconfig(openssl)
BuildRequires:  zlib-devel

%description
WebSocket++ is an open source (BSD license) header only C++ library
that implements RFC6455 The WebSocket Protocol. It allows integrating
WebSocket client and server functionality into C++ programs. It uses
interchangeable network transport modules including one based on C++
iostreams and one based on Boost Asio.

%package devel
Summary:  C++ WebSocket Protocol Library
Requires: kms-boost-devel
%description devel
WebSocket++ is an open source (BSD license) header only C++ library
that implements RFC6455 The WebSocket Protocol. It allows integrating
WebSocket client and server functionality into C++ programs. It uses
interchangeable network transport modules including one based on C++
iostreams and one based on Boost Asio.


%prep
%autosetup -p1


%build
mkdir -p build
cd build
cmake -DBUILD_TESTS:BOOL=OFF \
    -DCMAKE_INSTALL_PREFIX:PATH=/usr \
    -DCMAKE_BUILD_TYPE=Release ..

make %{?_smp_mflags}


%install
cd build
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/pkgconfig
install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pkgconfig/websocketpp.pc

## unpackaged files
rm -rfv %{buildroot}%{_includedir}/test_connection/
#rm -rfv %{buildroot}%{_bindir}/test_*


%check


%files devel
%doc changelog.md readme.md roadmap.md
%license COPYING
%{_includedir}/websocketpp/
%dir %{_datadir}/cmake/
%{_datadir}/cmake/websocketpp/
%{_datadir}/pkgconfig/websocketpp.pc


%changelog
* Mon Aug 03 2020 Wolfgang Stöggl <c72578@yahoo.de> - 0.8.2-4
- Use %%cmake_build and %%cmake_install macros to fix FTBFS

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 20 2020 Wolfgang Stöggl <c72578@yahoo.de> - 0.8.2-1
- New upstream version
- Drop patches (fixed upstream):
  websocketpp-0.8.1-boost_1.70.patch
  websocketpp-0.8.1-fix_CMakeLists.txt_version_number.patch

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 08 2019 Wolfgang Stöggl <c72578@yahoo.de> - 0.8.1-6
- Prepare for Boost 1.70:
  Add websocketpp-0.8.1-boost_1.70.patch

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 07 2018 Wolfgang Stöggl <c72578@yahoo.de> - 0.8.1-4
- Add websocketpp-0.8.1-fix_CMakeLists.txt_version_number.patch

* Wed Nov 07 2018 Wolfgang Stöggl <c72578@yahoo.de> - 0.8.1-3
- Add websocketpp.pc to files

* Wed Oct 31 2018 Wolfgang Stöggl <c72578@yahoo.de> - 0.8.1-2
- Update websocketpp-0.8.1-cmake-configversion-compatibility-anynewerversion.patch
  Disable check for same 32/64bit-ness in websocketpp-configVersion.cmake

* Thu Jul 26 2018 Wolfgang Stöggl <c72578@yahoo.de> - 0.8.1-1
- New upstream version
- Added websocketpp-0.8.1-cmake-configversion-compatibility-anynewerversion.patch
- The following patches are not needed any more and have been removed:
  websocketpp-0.7.0-openssl11.patch
  websocketpp-0.7.0-zlib-permessage-deflate.patch
  websocketpp-0.7.0-minor-adjustments-to-recent-extension-negotiation.patch
- Switch to pkgconfig(openssl) again
- Update version and URL in websocketpp.pc

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 16 2018 Wolfgang Stöggl <c72578@yahoo.de> - 0.7.0-13
- Add BuildRequires: gcc-c++

* Sun Feb 11 2018 Wolfgang Stöggl <c72578@yahoo.de> - 0.7.0-12
- Rebuilt for Boost 1.66

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Jonathan Wakely <jwakely@redhat.com> - 0.7.0-9
- Rebuilt for s390x binutils bug

* Tue Jul 04 2017 Jonathan Wakely <jwakely@redhat.com> - 0.7.0-8
- Rebuilt for Boost 1.64

* Tue Jun 13 2017 Wolfgang Stöggl <c72578@yahoo.de> - 0.7.0-7
- Add patches to fix zlib test failure (test_permessage_deflate)
- Disable tests test_transport, test_transport_asio_timers

* Fri May 26 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.7.0-6
- explicitly use openssl-devel (instead of generic 'pkgconfig(openssl)'

* Mon May 22 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.7.0-5
- adjust openssl patch
- BR: openssl-devel zlib-devel (for tests mostly)

* Wed May 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.7.0-4
- tls.hpp, SSL_R_SHORT_READ undefined in openssl-1.1 (#1449163)
- enable tests

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 0.7.0-2
- Rebuilt for Boost 1.63

* Thu Sep 15 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.7.0-1
- websocketpp-0.7.0 (#1375610)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 16 2016 Jonathan Wakely <jwakely@redhat.com> - 0.4.0-8
- Rebuilt for Boost 1.60

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.4.0-7
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.4.0-5
- rebuild for Boost 1.58

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.4.0-3
- Rebuild for boost 1.57.0

* Thu Nov 13 2014 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-2
- use (upstreamable) cmake_noarch.patch instead of manually moving files around

* Wed Nov 05 2014 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-1
- first try

* Mon Mar 17 2014 prusnak@opensuse.org
- created package (based on a Fedora package by Thomas Sailer)
