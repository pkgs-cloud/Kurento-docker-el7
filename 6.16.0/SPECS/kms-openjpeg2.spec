%global upname openjpeg
%global upver 2.1

%global _prefix /opt/kms

# Conformance tests disabled by default since it requires 1 GB of test data
#global runcheck 1

#global optional_components 1

#global master 1

Name:           kms-openjpeg2
Version:        2.1.0
Release:        7%{?dist}
Summary:        C-Library for JPEG 2000

# windirent.h is MIT, the rest is BSD
License:        BSD and MIT
URL:            https://github.com/uclouvain/openjpeg
%if 0%{?master}
Source0:        https://github.com/uclouvain/openjpeg/archive/master.tar.gz
%else
Source0:        https://github.com/uclouvain/openjpeg/archive/version.%{upver}.tar.gz
%endif
%if 0%{?runcheck}
# svn checkout http://openjpeg.googlecode.com/svn/data
Source1: data.tar.xz
%endif

# Remove bundled libraries
Patch0:         openjpeg2_remove-thirdparty.patch
# Bigendian fixes
Patch1:         openjpeg2_bigendian.patch
# Backport fix for use after free vulnerability (#1263359)
Patch2:         940100c28ae28931722290794889cf84a92c5f6f.patch
# Backport fix for possible double-free (#1267983)
Patch3:         0fa5a17c98c4b8f9ee2286f4f0a50cf52a5fccb0.patch

BuildRequires:  cmake
BuildRequires:  zlib-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  lcms2-devel
BuildRequires:  doxygen

%if 0%{?optional_components}
BuildRequires:  java-devel
BuildRequires:  xerces-j2
%endif

%description
The OpenJPEG library is an open-source JPEG 2000 library developed in order to
promote the use of JPEG 2000.

This package contains
* JPEG 2000 codec compliant with the Part 1 of the standard (Class-1 Profile-1
  compliance).
* JP2 (JPEG 2000 standard Part 2 - Handling of JP2 boxes and extended multiple
  component transforms for multispectral and hyperspectral imagery)


%package devel
Summary:        Development files for OpenJPEG 2
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use OpenJPEG 2.


%package devel-docs
Summary:        Developer documentation for OpenJPEG 2
BuildArch:      noarch

%description devel-docs
The %{name}-devel-docs package contains documentation files for developing
applications that use OpenJPEG 2.


%package tools
Summary:        OpenJPEG 2 command line tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
Command line tools for JPEG 2000 file manipulation, using OpenJPEG2:
 * opj2_compress
 * opj2_decompress
 * opj2_dump

%if 0%{?optional_components}
##### MJ2 #####
 
%package mj2
Summary:        OpenJPEG2 MJ2 module
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description mj2
The OpenJPEG library is an open-source JPEG 2000 library developed in order to
promote the use of JPEG 2000.

This package contains the MJ2 module (JPEG 2000 standard Part 3)


%package mj2-devel
Summary:        Development files for OpenJPEG2 MJ2 module
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-mj2%{?_isa} = %{version}-%{release}

%description mj2-devel
Development files for OpenJPEG2 MJ2 module


%package mj2-tools
Summary:        OpenJPEG2 MJ2 module command line tools
Requires:       %{name}-mj2%{?_isa} = %{version}-%{release}

%description mj2-tools
OpenJPEG2 MJ2 module command line tools

##### JPWL #####

%package jpwl
Summary:        OpenJPEG2 JPWL module
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description jpwl
The OpenJPEG library is an open-source JPEG 2000 library developed in order to
promote the use of JPEG 2000.

This package contains the JPWL (JPEG 2000 standard Part 11 - Jpeg 2000 Wireless)


%package jpwl-devel
Summary:        Development files for OpenJPEG2 JPWL module
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-jpwl%{?_isa} = %{version}-%{release}

%description jpwl-devel
Development files for OpenJPEG2 JPWL module


%package jpwl-tools
Summary:        OpenJPEG2 JPWL module command line tools
Requires:       %{name}-jpwl%{?_isa} = %{version}-%{release}

%description jpwl-tools
OpenJPEG2 JPWL module command line tools

##### JPIP #####

%package jpip
Summary:        OpenJPEG2 JPIP module
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description jpip
The OpenJPEG library is an open-source JPEG 2000 library developed in order to
promote the use of JPEG 2000.

This package contains the JPWL (JPEG 2000 standard Part 9 - Jpeg 2000 Interactive Protocol)


%package jpip-devel
Summary:        Development files for OpenJPEG2 JPIP module
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-jpwl%{?_isa} = %{version}-%{release}

%description jpip-devel
Development files for OpenJPEG2 JPIP module


%package jpip-tools
Summary:        OpenJPEG2 JPIP module command line tools
Requires:       %{name}-jpip%{?_isa} = %{version}-%{release}
Requires:       jpackage-utils
Requires:       java

%description jpip-tools
OpenJPEG2 JPIP module command line tools

##### JP3D #####

%package jp3d
Summary:        OpenJPEG2 JP3D module
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description jp3d
The OpenJPEG library is an open-source JPEG 2000 library developed in order to
promote the use of JPEG 2000.

This package contains the JP3D (JPEG 2000 standard Part 10 - Jpeg 2000 3D)


%package jp3d-devel
Summary:        Development files for OpenJPEG2 JP3D module
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-jp3d%{?_isa} = %{version}-%{release}

%description jp3d-devel
Development files for OpenJPEG2 JP3D module


%package jp3d-tools
Summary:        OpenJPEG2 JP3D module command line tools
Requires:       %{name}-jp3d%{?_isa} = %{version}-%{release}

%description jp3d-tools
OpenJPEG2 JP3D module command line tools
%endif


%prep
%if 0%{?master}
%setup -q -n %{upname}-master %{?runcheck:-a 1}
%else
%setup -q -n %{upname}-version.%{upver} %{?runcheck:-a 1}
%endif
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# Remove all third party libraries just to be sure
rm -rf thirdparty


%build
mkdir %{_target_platform}
pushd %{_target_platform}
# TODO: Consider
# -DBUILD_JPIP_SERVER=ON -DBUILD_JAVA=ON 
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DOPENJPEG_INSTALL_LIB_DIR=%{_lib} \
    %{?optional_components:-DBUILD_MJ2=ON -DBUILD_JPWL=ON -DBUILD_JPIP=ON -DBUILD_JP3D=ON} \
    -DBUILD_DOC=ON \
    %{?runcheck:-DBUILD_TESTING:BOOL=ON -DOPJ_DATA_ROOT=$PWD/../data} \
    ..
popd

make VERBOSE=1 -C %{_target_platform} %{?_smp_mflags}


%install
%make_install -C %{_target_platform}

# Rename to avoid conflicts with openjpeg-1.x
for file in %{buildroot}%{_bindir}/opj_*; do
    mv $file ${file/opj_/opj2_}
done
mv %{buildroot}%{_mandir}/man1/opj_compress.1 %{buildroot}%{_mandir}/man1/opj2_compress.1
mv %{buildroot}%{_mandir}/man1/opj_decompress.1 %{buildroot}%{_mandir}/man1/opj2_decompress.1
mv %{buildroot}%{_mandir}/man1/opj_dump.1 %{buildroot}%{_mandir}/man1/opj2_dump.1

# Docs are installed through %%doc
rm -rf %{buildroot}%{_datadir}/doc/

%if 0%{?optional_components}
# Move the jar to the correct place
mkdir -p %{buildroot}%{_javadir}
mv %{buildroot}%{_datadir}/opj_jpip_viewer.jar %{buildroot}%{_javadir}/opj2_jpip_viewer.jar
cat > %{buildroot}%{_bindir}/opj2_jpip_viewer <<EOF
java -jar %{_javadir}/opj2_jpip_viewer.jar "$@"
EOF
chmod +x %{buildroot}%{_bindir}/opj2_jpip_viewer
%endif


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%check
%if 0%{?runcheck}
make test -C %{_target_platform}
%endif


%files
%{!?_licensedir:%global license %doc}
%license LICENSE
%doc AUTHORS NEWS README THANKS
%{_libdir}/libopenjp2.so.*
%{_mandir}/man3/libopenjp2.3*

%files devel
%dir %{_includedir}/openjpeg-2.1/
%{_includedir}/openjpeg-2.1/openjpeg.h
%{_includedir}/openjpeg-2.1/opj_config.h
%{_includedir}/openjpeg-2.1/opj_stdint.h
%{_libdir}/libopenjp2.so
%{_libdir}/openjpeg-2.1/
%{_libdir}/pkgconfig/libopenjp2.pc

%files devel-docs
%doc %{_target_platform}/doc/html

%files tools
%{_bindir}/opj2_compress
%{_bindir}/opj2_decompress
%{_bindir}/opj2_dump
%{_mandir}/man1/opj2_compress.1*
%{_mandir}/man1/opj2_decompress.1*
%{_mandir}/man1/opj2_dump.1*

%if 0%{?optional_components}
%files mj2
%{_libdir}/libopenmj2.so.*

%files mj2-devel
%{_libdir}/libopenmj2.so

%files mj2-tools
%{_bindir}/opj2_mj2*

%files jpwl
%{_libdir}/libopenjpwl.so.*

%files jpwl-devel
%{_libdir}/libopenjpwl.so
%{_libdir}/pkgconfig/libopenjpwl.pc

%files jpwl-tools
%{_bindir}/opj2_jpwl*

%files jpip
%{_libdir}/libopenjpip.so.*

%files jpip-devel
%{_libdir}/libopenjpip.so
%{_libdir}/pkgconfig/libopenjpip.pc

%files jpip-tools
%{_bindir}/opj2_jpip*
%{_bindir}/opj2_dec_server
%{_javadir}/opj2_jpip_viewer.jar

%files jp3d
%{_libdir}/libopenjp3d.so.*

%files jp3d-devel
%{_includedir}/openjpeg-2.0/openjp3d.h
%{_libdir}/libopenjp3d.so
%{_libdir}/pkgconfig/libopenjp3d.pc

%files jp3d-tools
%{_bindir}/opj2_jp3d*
%endif


%changelog
* Thu Oct 01 2015 Sandro Mani <manisandro@gmail.com> - 2.1.0-7
- Backport fix for possible double-free (#1267983)

* Tue Sep 15 2015 Sandro Mani <manisandro@gmail.com> - 2.1.0-6
- Backport fix for use after free vulnerability (#1263359)

* Thu Jun 25 2015 Sandro Mani <manisandro@gmail.com> - 2.1.0-5
- Add openjpeg2_bigendian.patch (#1232739)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Sandro Mani <manisandro@gmail.com> - 2.1.0-1
- Update to 2.1.0

* Wed Apr 16 2014 Sandro Mani <manisandro@gmail.com> - 2.0.0-5
- Switch to official 2.0 release and backport pkg-config patch

* Thu Apr 10 2014 Sandro Mani <manisandro@gmail.com> - 2.0.0-4.svn20140403
- Replace define with global
- Fix #define optional_components 1S typo
- Fix %%(pwd) -> $PWD for test data
- Added some BR for optional components
- Include opj2_jpip_viewer.jar in %%files

* Wed Apr 09 2014 Sandro Mani <manisandro@gmail.com> - 2.0.0-3.svn20140403
- Fix source url
- Fix mixed tabs and spaces
- Fix description too long

* Wed Apr 09 2014 Sandro Mani <manisandro@gmail.com> - 2.0.0-2.svn20140403
- Remove thirdparty libraries folder in prep
- Own %%{_libdir}/openjpeg-2.0/
- Fix Requires
- Add missing ldconfig
- Add possibility to run conformance tests if desired
 
* Thu Apr 03 2014 Sandro Mani <manisandro@gmail.com> - 2.0.0-1.svn20140403
- Initial package
