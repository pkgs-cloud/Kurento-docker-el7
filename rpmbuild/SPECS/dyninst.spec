Summary: An API for Run-time Code Generation
License: LGPLv2+
Name: dyninst
Group: Development/Libraries
Release: 2%{?dist}
URL: http://www.dyninst.org
Version: 9.3.1
# Dyninst only has full support for a few architectures.
# It has some preliminary support for aarch64 and ppc64le,
# but we're waiting for those to be feature-complete.
ExclusiveArch: %{ix86} x86_64 ppc ppc64

Source0: https://github.com/dyninst/dyninst/archive/v%{version}/dyninst-%{version}.tar.gz
# Explicit version since it does not match the source version
Source1: https://github.com/dyninst/testsuite/archive/v9.3.0/testsuite-9.3.0.tar.gz

Patch1: testsuite-9.3.0-junit-nullptr.patch
Patch2: dyninst-9.3.1-Address.patch
Patch3: dyninst-rhbz1441810.patch

%global dyninst_base dyninst-%{version}
# Explicit version since it does not match the source version
%global testsuite_base testsuite-9.3.0

BuildRequires: gcc-c++
BuildRequires: libdwarf-devel >= 20111030
BuildRequires: elfutils-libelf-devel
BuildRequires: boost-devel
BuildRequires: binutils-devel
BuildRequires: cmake

# Extra requires just for the testsuite
BuildRequires: gcc-gfortran glibc-static libstdc++-static nasm

# Testsuite files should not provide/require anything
%{?filter_setup:
%filter_provides_in %{_libdir}/dyninst/testsuite/
%filter_requires_in %{_libdir}/dyninst/testsuite/
%filter_setup
}

%description

Dyninst is an Application Program Interface (API) to permit the insertion of
code into a running program. The API also permits changing or removing
subroutine calls from the application program. Run-time code changes are
useful to support a variety of applications including debugging, performance
monitoring, and to support composing applications out of existing packages.
The goal of this API is to provide a machine independent interface to permit
the creation of tools and applications that use run-time code patching.

%package doc
Summary: Documentation for using the Dyninst API
Group: Documentation
%description doc
dyninst-doc contains API documentation for the Dyninst libraries.

%package devel
Summary: Header files for the compiling programs with Dyninst
Group: Development/System
Requires: dyninst = %{version}-%{release}
Requires: boost-devel

%description devel
dyninst-devel includes the C header files that specify the Dyninst user-space
libraries and interfaces. This is required for rebuilding any program
that uses Dyninst.

%package static
Summary: Static libraries for the compiling programs with Dyninst
Group: Development/System
Requires: dyninst-devel = %{version}-%{release}
%description static
dyninst-static includes the static versions of the library files for
the dyninst user-space libraries and interfaces.

%package testsuite
Summary: Programs for testing Dyninst
Group: Development/System
Requires: dyninst = %{version}-%{release}
Requires: dyninst-devel = %{version}-%{release}
Requires: dyninst-static = %{version}-%{release}
Requires: glibc-static
%description testsuite
dyninst-testsuite includes the test harness and target programs for
making sure that dyninst works properly.

%prep
%setup -q -n %{name}-%{version} -c
%setup -q -T -D -a 1

%patch1 -p0 -b.nullptr
%patch2 -p0 -b.Address
%patch3 -p0 -b.1441810

# cotire seems to cause non-deterministic gcc errors
# https://bugzilla.redhat.com/show_bug.cgi?id=1420551
sed -i.cotire -e 's/USE_COTIRE true/USE_COTIRE false/' \
  %{dyninst_base}/cmake/shared.cmake

%build

cd %{dyninst_base}

%cmake \
 -DENABLE_STATIC_LIBS=1 \
 -DINSTALL_LIB_DIR:PATH=%{_libdir}/dyninst \
 -DINSTALL_INCLUDE_DIR:PATH=%{_includedir}/dyninst \
 -DINSTALL_CMAKE_DIR:PATH=%{_libdir}/cmake/Dyninst \
 -DCMAKE_BUILD_TYPE=None \
 -DCMAKE_SKIP_RPATH:BOOL=YES
%make_build

# Hack to install dyninst nearby, so the testsuite can use it
make DESTDIR=../install install
find ../install -name '*.cmake' -execdir \
  sed -i -e 's!%{_prefix}!../install&!' '{}' '+'

cd ../%{testsuite_base}
%cmake \
 -DDyninst_DIR:PATH=$PWD/../install%{_libdir}/cmake/Dyninst \
 -DINSTALL_DIR:PATH=%{_libdir}/dyninst/testsuite \
 -DCMAKE_BUILD_TYPE:STRING=Debug \
 -DCMAKE_SKIP_RPATH:BOOL=YES
%make_build

%install

cd %{dyninst_base}
%make_install

# It doesn't install docs the way we want, so remove them.
# We'll just grab the pdfs later, directly from the build dir.
rm -v %{buildroot}%{_docdir}/*-%{version}.pdf

cd ../%{testsuite_base}
%make_install

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{_libdir}/dyninst" > %{buildroot}/etc/ld.so.conf.d/%{name}-%{_arch}.conf

# Ugly hack to mask testsuite files from debuginfo extraction.  Running the
# testsuite requires debuginfo, so extraction is useless.  However, debuginfo
# extraction is still nice for the main libraries, so we don't want to disable
# it package-wide.  The permissions are restored by attr(755,-,-) in files.
find %{buildroot}%{_libdir}/dyninst/testsuite/ \
  -type f '!' -name '*.a' -execdir chmod 644 '{}' '+'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%dir %{_libdir}/dyninst
%{_libdir}/dyninst/*.so.*

%doc %{dyninst_base}/COPYRIGHT
%doc %{dyninst_base}/LGPL

%config(noreplace) /etc/ld.so.conf.d/*

%files doc
%doc %{dyninst_base}/dataflowAPI/doc/dataflowAPI.pdf
%doc %{dyninst_base}/dynC_API/doc/dynC_API.pdf
%doc %{dyninst_base}/dyninstAPI/doc/dyninstAPI.pdf
%doc %{dyninst_base}/instructionAPI/doc/instructionAPI.pdf
%doc %{dyninst_base}/parseAPI/doc/parseAPI.pdf
%doc %{dyninst_base}/patchAPI/doc/patchAPI.pdf
%doc %{dyninst_base}/proccontrol/doc/proccontrol.pdf
%doc %{dyninst_base}/stackwalk/doc/stackwalk.pdf
%doc %{dyninst_base}/symtabAPI/doc/symtabAPI.pdf

%files devel
%{_includedir}/dyninst
%{_libdir}/dyninst/*.so
%dir %{_libdir}/cmake
%{_libdir}/cmake/Dyninst

%files static
%{_libdir}/dyninst/*.a

%files testsuite
%{_bindir}/parseThat
%dir %{_libdir}/dyninst/testsuite/
# Restore the permissions that were hacked out above, during install.
%attr(755,root,root) %{_libdir}/dyninst/testsuite/*[!a]
%attr(644,root,root) %{_libdir}/dyninst/testsuite/*.a

%changelog
* Thu Jun 07 2018 Stan Cox <scox@redhat.com> - 9.3.1-2
- rhbz1441810: Handle regions with no disk backing for ppc static instrumenting

* Mon Mar 06 2017 Stan Cox <scox@redhat.com> - 9.3.1-1
- Update to 9.3.1

* Mon Oct 20 2014 Josh Stone <jistone@redhat.com> - 8.2.0-2
- rhbz1152270: enable bug workaround for syscall pc rewind on ppc

* Fri Sep 05 2014 Josh Stone <jistone@redhat.com> - 8.2.0-1
- rebase to 8.2.0, using upstream tag "v8.2.0.1"

* Mon Feb 10 2014 Josh Stone <jistone@redhat.com> 8.1.2-6
- rhbz1063447: squash testsuite g++ optimization
- rhbz1030969: backported additional patch to silence new warnings

* Thu Jan 16 2014 Josh Stone <jistone@redhat.com> 8.1.2-5
- rhbz1030969: backported upstream patches for image::findMain

* Tue Jan 07 2014 Josh Stone <jistone@redhat.com> 8.1.2-4
- rhbz1040652: backported upstream patches for mid-syscall PTRACE_EVENTs

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 8.1.2-3
- Mass rebuild 2013-12-27

* Fri Oct 25 2013 Josh Stone <jistone@redhat.com> 8.1.2-2
- rhbz1007500: Fix DYNINST_index_lock state and ppc64 writeFunctionPtr

* Tue Jun 18 2013 Josh Stone <jistone@redhat.com> 8.1.2-1
- Update to release 8.1.2.

* Fri Mar 15 2013 Josh Stone <jistone@redhat.com> 8.1.1-1
- Update to release 8.1.1.
- Drop the backported dyninst-test2_4-kill-init.patch.
- Drop the now-upstreamed dyninst-unused_vars.patch.
- Update other patches for context.
- Patch the installed symlinks to be relative, not $(DEST) filled.

* Tue Feb 26 2013 Josh Stone <jistone@redhat.com> 8.0-7
- testsuite: Require dyninst-devel for the libdyninstAPI_RT.so symlink

* Tue Feb 26 2013 Josh Stone <jistone@redhat.com> 8.0-6
- Fix the testsuite path to include libtestlaunch.so

* Mon Feb 25 2013 Josh Stone <jistone@redhat.com> 8.0-5
- Add a dyninst-testsuite package.
- Patch test2_4 to protect against running as root.
- Make dyninst-static require dyninst-devel.

* Thu Feb 14 2013 Josh Stone <jistone@redhat.com> 8.0-4
- Patch make.config to ensure rpm build flags are not discarded.

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 8.0-3
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 8.0-2
- Rebuild for Boost-1.53.0

* Tue Nov 20 2012 Josh Stone <jistone@redhat.com>
- Tweak the configure/make commands
- Disable the testsuite via configure.
- Set the private includedir and libdir via configure.
- Set VERBOSE_COMPILATION for make.
- Use DESTDIR for make install.

* Mon Nov 19 2012 Josh Stone <jistone@redhat.com> 8.0-1
- Update to release 8.0.
- Updated "%files doc" to reflect renames.
- Drop the unused BuildRequires libxml2-devel.
- Drop the 7.99.x version-munging patch.

* Fri Nov 09 2012 Josh Stone <jistone@redhat.com> 7.99.2-0.29
- Rebase to git e99d7070bbc39c76d6d528db530046c22681c17e

* Mon Oct 29 2012 Josh Stone <jistone@redhat.com> 7.99.2-0.28
- Bump to 7.99.2 per abi-compliance-checker results

* Fri Oct 26 2012 Josh Stone <jistone@redhat.com> 7.99.1-0.27
- Rebase to git dd8f40b7b4742ad97098613876efeef46d3d9e65
- Use _smp_mflags to enable building in parallel.

* Wed Oct 03 2012 Josh Stone <jistone@redhat.com> 7.99.1-0.26
- Rebase to git 557599ad7417610f179720ad88366c32a0557127

* Thu Sep 20 2012 Josh Stone <jistone@redhat.com> 7.99.1-0.25
- Rebase on newer git tree.
- Bump the fake version to 7.99.1 to account for ABI differences.
- Enforce the minimum libdwarf version.
- Drop the upstreamed R_PPC_NUM patch.

* Wed Aug 15 2012 Karsten Hopp <karsten@redhat.com> 7.99-0.24
- check if R_PPC_NUM is defined before using it, similar to R_PPC64_NUM

* Mon Jul 30 2012 Josh Stone <jistone@redhat.com> 7.99-0.23
- Rebase on newer git tree.
- Update license files with upstream additions.
- Split documentation into -doc subpackage.
- Claim ownership of %{_libdir}/dyninst.

* Fri Jul 27 2012 William Cohen <wcohen@redhat.com> - 7.99-0.22
- Correct requires for dyninst-devel.

* Wed Jul 25 2012 Josh Stone <jistone@redhat.com> - 7.99-0.21
- Rebase on newer git tree
- Update context in dyninst-git.patch
- Drop dyninst-delete_array.patch
- Drop dyninst-common-makefile.patch

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.99-0.20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 William Cohen <wcohen@redhat.com> - 7.99-0.19
- Patch common/i386-unknown-linux2.4/Makefile to build.

* Fri Jul 13 2012 William Cohen <wcohen@redhat.com> - 7.99-0.18
- Rebase on newer git tree the has a number of merges into it.
- Adjust spec file to allow direct use of git patches
- Fix to eliminate unused varables.
- Proper delete for array.

* Thu Jun 28 2012 William Cohen <wcohen@redhat.com> - 7.99-0.17
- Rebase on newer git repo.

* Thu Jun 28 2012 William Cohen <wcohen@redhat.com> - 7.99-0.16
- Eliminate dynptr.h file use with rebase on newer git repo.

* Mon Jun 25 2012 William Cohen <wcohen@redhat.com> - 7.99-0.14
- Rebase on newer git repo.

* Tue Jun 19 2012 William Cohen <wcohen@redhat.com> - 7.99-0.12
- Fix static library and header file permissions.
- Use sources from the dyninst git repositories.
- Fix 32-bit library versioning for libdyninstAPI_RT_m32.so.

* Wed Jun 13 2012 William Cohen <wcohen@redhat.com> - 7.99-0.11
- Fix library versioning.
- Move .so links to dyninst-devel.
- Remove unneded clean section.

* Fri May 11 2012 William Cohen <wcohen@redhat.com> - 7.0.1-0.9
- Clean up Makefile rules.

* Sat May 5 2012 William Cohen <wcohen@redhat.com> - 7.0.1-0.8
- Clean up spec file.

* Wed May 2 2012 William Cohen <wcohen@redhat.com> - 7.0.1-0.7
- Use "make install" and do staged build.
- Use rpm configure macro.

* Thu Mar 15 2012 William Cohen <wcohen@redhat.com> - 7.0.1-0.5
- Nuke the bundled boost files and use the boost-devel rpm instead.

* Mon Mar 12 2012 William Cohen <wcohen@redhat.com> - 7.0.1-0.4
- Initial submission of dyninst spec file.
