# globals for x264-0.148-20170521-aaa9aa8.tar.bz2
%global api 148
%global gitdate 20170521
%global gitversion aaa9aa8

%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}
%global branch stable

#global _with_bootstrap 1

%{?_with_bootstrap:
%global _without_gpac 1
%global _without_libavformat 1
%global _without_libswscale  1
}
#Whitelist of arches with dedicated ASM code
%global asmarch x86_64 armv7hl armv7hnl ppc64le aarch64
# list of arches where ASM must be optional
%global simdarch i686 ppc64
%ifnarch %{asmarch}
%global _without_asm 1
%endif
%ifarch i686
%global slibdir %{_libdir}/sse2
%endif
%ifarch ppc64
%global slibdir %{_libdir}/altivec
%endif

Summary: H264/AVC video streams encoder
Name: x264
Version: 0.%{api}
Release: 23%{?gver}%{?_with_bootstrap:_bootstrap}%{?dist}
License: GPLv2+
URL: https://www.videolan.org/developers/x264.html
Source0: %{name}-0.%{api}-%{snapshot}.tar.bz2
Source1: x264-snapshot.sh

# don't remove config.h and don't re-run version.sh
Patch0: x264-nover.patch
# add 10b suffix to high bit depth build
Patch1: x264-10b.patch
Patch10: x264-gpac.patch

%{!?_without_gpac:BuildRequires: gpac-devel zlib-devel openssl-devel libpng-devel libjpeg-devel}
%{!?_without_libavformat:BuildRequires: ffmpeg-devel}
%{?_with_ffmpegsource:BuildRequires: ffmpegsource-devel}
# https://bugzilla.rpmfusion.org/show_bug.cgi?id=3975
%ifarch armv7hl armv7hnl
BuildRequires: execstack
%endif
%ifarch %{asmarch} %{simdarch}
BuildRequires: yasm >= 1.0.0
%endif
BuildRequires: gcc
# we need to enforce the exact EVR for an ISA - not only the same ABI
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

This package contains the frontend.

%package libs
%{?el7:BuildRequires: epel-rpm-macros}
Summary: Library for encoding H264/AVC video streams

%description libs
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

%package devel
Summary: Development files for the x264 library
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

This package contains the development files.

%global x_configure \
%configure \\\
	%{?_without_libavformat:--disable-lavf} \\\
	%{?_without_libswscale:--disable-swscale} \\\
	%{!?_with_ffmpegsource:--disable-ffms} \\\
	--disable-opencl \\\
	--disable-debug \\\
	--enable-shared \\\
	--system-libx264 \\\
	--enable-pic

%prep
%setup -q -c -n %{name}-0.%{api}-%{snapshot}
pushd %{name}-0.%{api}-%{snapshot}
%patch0 -p1 -b .nover
%patch1 -p1 -b .10b
%patch10 -p1 -b .gpac
popd

variants="generic generic10"
%ifarch %{simdarch}
variants="$variants simd simd10"
%endif
for variant in $variants ; do
  rm -rf ${variant}
  cp -pr %{name}-0.%{api}-%{snapshot} ${variant}
done


%build
pushd generic
%{x_configure}\
	%{?_without_asm:--disable-asm}

%make_build
popd

pushd generic10
%{x_configure}\
	%{?_without_asm:--disable-asm}\
	--disable-cli\
	--bit-depth=10

%make_build
popd

%ifarch %{simdarch}
pushd simd
%{x_configure}\
	--libdir=%{slibdir}

%make_build
popd

pushd simd10
%{x_configure}\
	--disable-cli\
	--libdir=%{slibdir}\
	--bit-depth=10

%make_build
popd
%endif

%install
for variant in generic generic10 ; do
pushd ${variant}
%make_install
popd
done
%ifarch %{simdarch}
for variant in simd simd10 ; do
pushd ${variant}
%make_install
rm -f %{buildroot}%{slibdir}/pkgconfig/x264.pc
popd
done
%endif

#Fix timestamp on x264 generated headers
touch -r generic/version.h %{buildroot}%{_includedir}/x264.h %{buildroot}%{_includedir}/x264_config.h

# https://bugzilla.rpmfusion.org/show_bug.cgi?id=3975
%ifarch armv7hl armv7hnl
execstack -c %{buildroot}%{_libdir}/libx264{,10b}.so.%{api}
%endif

install -dm755 %{buildroot}%{_pkgdocdir}
install -pm644 generic/AUTHORS %{buildroot}%{_pkgdocdir}/
cp -a generic/doc %{buildroot}%{_pkgdocdir}/


%ldconfig_scriptlets libs


%files
%{_bindir}/x264

%files libs
%{_pkgdocdir}/
%exclude %{_pkgdocdir}/doc
%license generic/COPYING
%{_libdir}/libx264.so.%{api}
%{_libdir}/libx26410b.so.%{api}
%ifarch %{simdarch}
%{slibdir}/libx264.so.%{api}
%{slibdir}/libx26410b.so.%{api}
%endif

%files devel
%{_pkgdocdir}/doc/
%{_includedir}/x264.h
%{_includedir}/x264_config.h
%{_libdir}/libx264.so
%{_libdir}/libx26410b.so
%{_libdir}/pkgconfig/%{name}.pc
%ifarch %{simdarch}
%{slibdir}/libx264.so
%{slibdir}/libx26410b.so
%endif

%changelog
* Thu Nov 22 2018 Antonio Trande <sagitter@fedoraproject.org> - 0.148-23.20170521gitaaa9aa8
- Rebuild for ffmpeg-3.* on el7
- Rebuild for x265-2.9 on el7
- Set Make macros
- Disable debug builds
- Avoid mixed use of documentation macros

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.148-22.20170521gitaaa9aa8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Sérgio Basto <sergio@serjux.com> - 0.148-21.20170521gitaaa9aa8
- Update x264 to x264-0.148-20170521-aaa9aa8

* Mon May 22 2017 Sérgio Basto <sergio@serjux.com> - 0.148-20.20170519gitd32d7bf
- Update x264 to x264-0.148-20170519-d32d7bf

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.148-19.20170121git97eaef2
- Rebuild for ffmpeg update

* Wed Mar 22 2017 Sérgio Basto <sergio@serjux.com> - 0.148-18.20170121git97eaef2
- Unbootstrap

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.148-17.20170121git97eaef2_bootstrap
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Mar 18 2017 Sérgio Basto <sergio@serjux.com> - 0.148-16.20170121git97eaef2_bootstrap
- Bootstrap for ppc64, ppc64le and aarch64

* Wed Jan 25 2017 Sérgio Basto <sergio@serjux.com> - 0.148-15.20170121git97eaef2
- Update x264 to git stable snapshot of 20170121

* Sat Dec 03 2016 Sérgio Basto <sergio@serjux.com> - 0.148-14.20161201git4d5c8b0
- Update to x264-0.148-20161201-4d5c8b0 stable branch
- Improve x264-snapshot.sh to use date from last commit and print the headers to
  include in x264.spec

* Sat Nov 05 2016 Sérgio Basto <sergio@serjux.com> - 0.148-13.20160924git86b7198
- Rebuilt for new ffmpeg

* Tue Sep 27 2016 Sérgio Basto <sergio@serjux.com> - 0.148-12.20160924git86b7198
- Update to 0.148-20160924-86b7198 version

* Fri Aug 26 2016 Dominik Mierzejewski <rpm@greysector.net> - 0.148-11.20160614gita5e06b9
- rework asm treatment on i686 and ppc64
- fix adding the 10b suffix to the library name
- correct the list of ASM-enabled arches:
  * ppc64 can be Power5, which doesn't have AltiVec
  * ppc64le always has it
  * no implementation for sparc
- force non-executable stack on armv7 (#3975)
- explicitly disable OpenCL support, it's dlopened at the moment
  and not working without ocl-icd-devel
- drop doc and license from main package, libs already contain it
- update URL

* Thu Aug 18 2016 Sérgio Basto <sergio@serjux.com> - 0.148-10.20160614gita5e06b9
- Add license tag also to x264-libs

* Mon Aug 01 2016 Sérgio Basto <sergio@serjux.com> - 0.148-9.20160614gita5e06b9
- Enable asm in build with 10bit on i686

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.148-8.20160614gita5e06b9
- Rebuilt for ffmpeg-3.1.1

* Tue Jun 21 2016 Sérgio Basto <sergio@serjux.com> - 0.148-7.20160614gita5e06b9
- Update to last stable version upstream.

* Tue Apr 19 2016 Sérgio Basto <sergio@serjux.com> - 0.148-6.20160412gitfd2c324
- Update x264 to 0.148-20160412-fd2c324

* Wed Jan 20 2016 Sérgio Basto <sergio@serjux.com> - 0.148-5.20160118git5c65704
- Fix enable-asm #2

* Tue Jan 19 2016 Sérgio Basto <sergio@serjux.com> - 0.148-4.20160118git5c65704
- Fix enable-asm

* Mon Jan 18 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.148-3.20160118git5c65704
- Restore explicit dependency on -libs - enforce %%{_isa}
- Expand arm arches where asm is available.
- Restore asm only on sse2 and later capable i686

* Mon Jan 18 2016 Sérgio Basto <sergio@serjux.com> - 0.148-2.20151020gita0cd7d3
- Update x264 to 0.148-20160118-5c65704

* Fri Nov 27 2015 Simone Caronni <negativo17@gmail.com>
- Remove obsolete SPEC file tags, defattr were also breaking file permissions,
  all libraries were not executable.
- Enable optimizations in RHEL, they are working since RHEL 6:
  https://bugzilla.rpmfusion.org/show_bug.cgi?id=3260
- Add license and make_install macro as per packaging guidelines.
- Use the default configure macro and remove redundant parameters. Optimizations
  (build flags) are now added by default.

* Wed Oct 21 2015 Sérgio Basto <sergio@serjux.com> - 0.148-1.20151020gita0cd7d3
- Update to x264-0.148, soname bump, git a0cd7d3, date 20151020 .

* Sat Jun 06 2015 Sérgio Basto <sergio@serjux.com> - 0.144-1.20150225gitc8a773e
- Update to x264-0.144, soname bump, git c8a773e from date 20150225 .

* Mon Jun 01 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0.142-12.20141221git6a301b6
- Added patch to make it build on AArch64.

* Mon Dec 22 2014 Sérgio Basto <sergio@serjux.com> - 0.142-11.20141221git6a301b6
- Update x264-0.142 to git 6a301b6

* Sun Oct 19 2014 Sérgio Basto <sergio@serjux.com> - 0.142-10.20140826git021c0dc
- Rebuilt for FFmpeg 2.4.3

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.142-9.20140826git021c0dc
- Rebuilt for FFmpeg 2.4.x

* Mon Sep 15 2014 Sérgio Basto <sergio@serjux.com> - 0.142-7.20140826git021c0dc
- Update x264-0.142 to git 021c0dc

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 0.142-6.20140728gitaf8e768
- Rebuilt for ffmpeg-2.3

* Mon Jul 28 2014 Sérgio Basto <sergio@serjux.com> - 0.142-5.20140728gitaf8e768
- Update x264-0.142 to git af8e768

* Wed Apr 23 2014 Sérgio Basto <sergio@serjux.com> - 0.142-4.20140423gite260ea5
- Update to git e260ea5 (stable branch)

* Tue Mar 25 2014 Sérgio Basto <sergio@serjux.com> - 0.142-3.20140314gitaff928d
- Rebuilt for ffmpeg-2.2

* Sun Mar 23 2014 Sérgio Basto <sergio@serjux.com> - 0.142-2.20140314gitaff928d
- Un-bootstrap

* Fri Mar 14 2014 Sérgio Basto <sergio@serjux.com> - 0.142-1.20140314gitaff928d_bootstrap
- Update to 0.142 git aff928d (stable branch) and bootstrap

* Mon Mar 10 2014 Sérgio Basto <sergio@serjux.com> - 0.140-3.20140122gitde0bc36
- Un-boostrap

* Wed Mar 05 2014 Sérgio Basto <sergio@serjux.com> - 0.140-2.20140122gitde0bc36
- bootstrap x264 to avoid: 
  /usr/bin/ld: warning: libx264.so.138, needed by
  /usr/lib/gcc/x86_64-redhat-linux/4.8.2/../../../../lib64/libavcodec.so, may conflict with
  libx264.so.140

* Wed Jan 22 2014 Sérgio Basto <sergio@serjux.com> - 0.140-1.20140122gitde0bc36
- Update to 0.140 git de0bc36 (stable branch)
- drop visualize options, ./configure doesn't have --enable-visualize or --disable-visualize, 
anymore

* Tue Nov 05 2013 Sérgio Basto <sergio@serjux.com> - 0.138-2.20131030-c628e3b
- Unbootstrap.

* Sat Nov 02 2013 Sérgio Basto <sergio@serjux.com> - 0.138-1.20131030-c628e3b
- Update to 0.138 git c628e3b (stable branch) and bootstrap for new ffmpeg.

* Fri Oct 18 2013 Sérgio Basto <sergio@serjux.com> - 0.136-1.20131005git3361d59
- Update to 0.136 git 3361d59 (stable branch).

* Mon Sep 30 2013 Sérgio Basto <sergio@serjux.com> - 0.133-3.20130709git585324f
- Fix gpac detection.

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.133-2.20130709git585324f
- Rebuilt for FFmpeg 2.0.x

* Tue Jul 09 2013 Sérgio Basto <sergio@serjux.com> - 0.133-1.20130709git585324f
- Update to git 585324fee380109acd9986388f857f413a60b896 (HEAD of stable branch).

* Sat May 25 2013 Sérgio Basto <sergio@serjux.com> - 0.130-3.20130502git1db4621
- Build without bootstrap for F19.

* Fri May 24 2013 Sérgio Basto <sergio@serjux.com> - 0.130-2.20130502git1db4621
- Build with bootstrap for F19.

* Thu May 02 2013 Sérgio Basto <sergio@serjux.com> - 0.130-1.20130502git1db4621
- Update to git 1db4621

* Tue Mar 05 2013 Sérgio Basto <sergio@serjux.com> - 0.129-3.20130305gite403db4
- Update to git e403db4f9079811f5a1f9a1339e7c85b41800ca7

* Sun Jan 20 2013 Sérgio Basto <sergio@serjux.com> - 0.129-2.20130119git9c4ba4b
- Rebuild for ffmpeg-1.1.1 .

* Sat Jan 19 2013 Sérgio Basto <sergio@serjux.com> - 0.129-1.20130119git9c4ba4b
- Update to 9c4ba4bde8965571159eae2d79f85cabbb47416c, soname bump.
- Changed branch name by api number, is more readable.
- Drop upstreamed patch.

* Fri Nov 23 2012 Sérgio Basto <sergio@serjux.com> - 0.128-2.20121118gitf6a8615
- unbootstrap on F18.

* Mon Nov 19 2012 Sérgio Basto <sergio@serjux.com> - 0.128-1.20121118gitf6a8615
- Update to f6a8615ab0c922ac2cb5c82c9824f6f4742b1725.

* Sat Oct 06 2012 Sérgio Basto <sergio@serjux.com> - 0.125-4.20121006git68dfb7b
- Note: no source update.
- Just add git tag to package name, for faster check upstream.
- Add git tag in x264-snapshot.sh .
- Convert all defines in global. 

* Sun Sep 09 2012 Sérgio Basto <sergio@serjux.com> - 0.125-4.20120909
- unbootstrap on F18.

* Sun Sep 09 2012 Sérgio Basto <sergio@serjux.com> - 0.125-3.20120909
- update x264-0.125 from r2201 to r2209.

* Thu Sep 06 2012 Sérgio Basto <sergio@serjux.com> - 0.125-2.20120904
- unbootstrap

* Tue Sep 04 2012 Sérgio Basto <sergio@serjux.com> - 0.125-1.20120904
- Pulled latest stable patches, which bump version to 0.125.

* Mon Jun 25 2012 Sérgio Basto <sergio@serjux.com> - 0.124-5.20120616
- Fixed detection of gf_malloc and gf_free

* Sun Jun 24 2012 Sérgio Basto <sergio@serjux.com> - 0.124-4.20120616
- unbootstrap.

* Sat Jun 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.124-3.20120616
- Rework alternatives build
- Fix SONAME for x26410b

* Sun Jun 17 2012 Sérgio Basto <sergio@serjux.com> - 0.124-2.20120616
- use _libdir to fix build on x86_64.

* Sun Jun 17 2012 Sérgio Basto <sergio@serjux.com> - 0.124-1.20120616
- Update to 20120616
- Add one build with --bit-depth=10
- Enabled bootstrap, after rebuild ffmpeg, we rebuild x264 without bootstrap.

* Tue May 01 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.120-5.20120303
- Forward rhel patch
- Disable ASM on armv5tel armv6l
- Add --with bootstrap conditional
- Use %%{_isa} for devel requires

* Tue Mar 6 2012 Sérgio Basto <sergio@serjux.com> - 0.120-2.20120303
- Enable libavformat , after compile ffmeg with 0.120-1

* Sat Mar 3 2012 Sérgio Basto <sergio@serjux.com> - 0.120-1.20120303
- Change release number, upstream have release numbers at least on stable branch and as ffmpeg
  reported.
- Update to 20120303
- Update x264-nover.patch, as suggest by Joseph D. Wagner <joe@josephdwagner.info> 
- Dropped obsolete Buildroot and Clean.
- add BuildRequires: zlib-devel to enable gpac.

* Wed Feb 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-0.34.20120125
- Rebuilt for F-17 inter branch

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-0.33.20120125
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-0.32.20120125
- Update to 20120125

* Mon Aug 22 2011 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.31.20110811
- 20110811 snapshot (ABI 116)
- fix snapshot script to include version.h properly
- link x264 binary to the shared library

* Thu Jul 14 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-0.30.20110714
- Update to 20110714 stable branch (ABI 115)
- Convert x264-snapshot to git (based on ffmpeg script).
- New Build Conditionals --with ffmpegsource libavformat
- Remove shared and strip patches - undeeded anymore
- Remove uneeded convertion of AUTHORS

* Mon Jan 10 2011 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.29.20110227
- 20110227 snapshot (ABI bump)

* Tue Jul 06 2010 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.28.20100706gitd058f37
- 20100706 snapshot (ABI bump)
- drop old Obsoletes:

* Thu Apr 29 2010 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.27.20100429gitd9db8b3
- 20100429 snapshot
- s/%%{ix86}/i686 (rfbz #1075)
- ship more docs in -devel

* Sat Jan 16 2010 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.26.20100116git3d0f110
- 20100116 snapshot (SO version bump)
- don't remove config.h and don't re-run version.sh
- link x264 binary to the shared library
- really don't strip if debug is enabled

* Mon Oct 26 2009 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.26.20091026gitec46ace7
- 20091026 snapshot

* Thu Oct 15 2009 kwizart <kwizart at gmail.com > -  0.0.0-0.25.20091007git496d79d
- Update to 20091007git
- Move simd to %%{_libdir}/sse2

* Thu Mar 26 2009 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.24.20090319gitc109c8
- 20090319 snapshot
- build with static gpac
- fix build on ppc

* Tue Feb 10 2009 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.23.20090119git451ba8d
- 20090119 snapshot
- fix BRs for build-time options

* Sat Dec 20 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.22.20081213git9089d21
- rebuild against new gpac

* Sat Dec 13 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.21.20081213git9089d21
- fix the libs split on x86

* Sat Dec 13 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.20.20081213git9089d21
- 20081213 snapshot
- drop the libs split on x86, it doesn't work right for P3/AthlonXP
- drop obsolete patch

* Thu Dec 04 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.19.20081202git71d34b4.1
- fix compilation on ppc

* Tue Dec 02 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.19.20081202git71d34b4
- 20081202 snapshot
- bring back asm optimized/unoptimized libs split
- rebase and improve patch
- GUI dropped upstream
- dropped redundant BRs

* Mon Nov 17 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.18.20080905
- partially revert latest changes (the separate sse2 libs part) until selinux
  policy catches up

* Fri Nov 07 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.17.20080905
- build libs without asm optimizations for less capable x86 CPUs (livna bug #2066)
- fix missing 0 in Obsoletes version (never caused any problems)

* Fri Sep 05 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.16.20080905
- 20080905 snapshot
- use yasm on all supported arches
- include mp4 output support via gpac by default
- drop/move obsolete fixups from %%prep
- fix icon filename in desktop file

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.0.0-0.15.20080613
- rebuild

* Sat Jun 14 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.14.20080613
- 20080613 snapshot (.so >= 59 is required by current mencoder)

* Mon May 05 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.13.20080420
- 20080420 snapshot
- split libs into a separate package
- svn -> git
- drop obsolete execstack patch
- fixed summaries and descriptions

* Wed Feb 27 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.12.20080227
- 20080227 snapshot
- fix build with gpac

* Tue Nov 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.0.0-0.11.20070819
- Merge freshrpms spec into livna spec for rpmfusion:
- Change version from 0 to 0.0.0 so that it is equal to the freshrpms versions,
  otherwise we would be older according to rpm version compare.
- Add Provides and Obsoletes x264-gtk to x264-gui for upgrade path from
  freshrpms
- Fix icon cache update scripts

* Sun Sep 30 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0-0.10.20070819
- Fix use of execstack on i386, closes livna bug #1659

* Sun Aug 19 2007 Dominik Mierzejewski <rpm@greysector.net> 0-0.9.20070819
- 20070819 snapshot, closes bug #1560

* Thu Nov 09 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.8.20061028
- use PIC on all platforms, fixes bug #1243

* Sun Oct 29 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.7.20061028
- fix desktop entry categories for devel

* Sun Oct 29 2006 Ville Skyttä <ville.skytta at iki.fi> - 0-0.6.20061028
- fix BRs
- handle menu icon properly

* Sat Oct 28 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.5.20061028
- fix bad patch chunk
- fix 32bit build on x86_64

* Sat Oct 28 2006 Ville Skyttä <ville.skytta at iki.fi> - 0-0.4.20061028
- Don't let ./configure to guess arch, pass it ourselves.
- Drop X-Livna desktop entry category.

* Sat Oct 28 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.3.20061028
- added GUI (based on kwizart's idea)
- latest snapshot
- added some docs to -devel

* Sun Oct 01 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.2.20061001
- add snapshot generator script
- fix make install
- make nasm/yasm BRs arch-dependent
- configure is not autoconf-based, call it directly

* Sat Sep 30 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.569
- Updated to latest SVN trunk
- specfile cleanups

* Mon Sep 04 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.558
- Updated to latest SVN trunk
- FE compliance

* Sun Mar 12 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.467
- Updated to latest SVN trunk
- Build shared library
- mp4 output requires gpac

* Mon Jan 02 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.394
- Updated to latest SVN trunk
- Change versioning scheme

* Sun Nov 27 2005 Dominik Mierzejewski <rpm@greysector.net> 0.0.375-1
- Updated to latest SVN trunk
- Added pkgconfig file to -devel

* Tue Oct  4 2005 Matthias Saou <http://freshrpms.net/> 0.0.315-1
- Update to svn 315.
- Disable vizualize since otherwise programs trying to link without -lX11 will
  fail (cinelerra in this particular case).

* Mon Aug 15 2005 Matthias Saou <http://freshrpms.net/> 0.0.285-1
- Update to svn 285.
- Add yasm build requirement (needed on x86_64).
- Replace X11 lib with lib/lib64 to fix x86_64 build.

* Tue Aug  2 2005 Matthias Saou <http://freshrpms.net/> 0.0.281-1
- Update to svn 281.

* Mon Jul 11 2005 Matthias Saou <http://freshrpms.net/> 0.0.273-1
- Initial RPM release.
