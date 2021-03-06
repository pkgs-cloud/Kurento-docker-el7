Name:           libva
Version:        1.8.3
Release:        1%{?dist}
Summary:        Libva is an implementation for Video Acceleration API

License:        MIT
URL:            https://github.com/intel/libva/
Source0:        https://github.com/intel/libva/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires: autoconf, automake, libtool
BuildRequires: libX11, libX11-devel, libXext, libXext-devel
BuildRequires: libXfixes, libXfixes-devel, libdrm, libdrm-devel
BuildRequires: libwayland-client, libwayland-client-devel, m4
BuildRequires: mesa-libEGL, mesa-libEGL-devel, mesa-libGL, mesa-libGL-devel
BuildRequires: mt-st, xorg-x11-proto-devel

%description
Video Acceleration-API is an open-source library and API specification,
which provides access to graphics hardware acceleration capabilities
for video processing. It consists of a main library and driver-specific
acceleration backends for each supported hardware vendor.

%package       devel
Summary:       Development files for %{name}
Requires:      %{name}%{_isa} = %{version}-%{release}
Requires:      pkgconfig

%description   devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%build
./autogen.sh --disable-static
%configure --disable-static

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build


%install
rm -rf $RPM_BUILD_ROOT
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc NEWS
%license COPYING
%ghost %{_sysconfdir}/libva.conf
%{_libdir}/libva*.so.*

%files devel
%{_includedir}/va
%{_libdir}/libva*.so
%{_libdir}/pkgconfig/libva*.pc

%changelog
* Mon Sep 11 2017 Josef Rikdy <jridky@redhat.com> - 1.8.3-1
- Initial commit
