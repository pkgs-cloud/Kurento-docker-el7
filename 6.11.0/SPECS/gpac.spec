# Todo:  - Add pkg-config support for libs detection.
#        - Add pkg-config support generated form configure for gpac (same as ffmpeg).
#        - Make it support swscaler enabled ffmpeg (at least test it - upstream).
#        - Submit and import patches upstream.
#        - Fix unused-direct-shlib-dependency on libgpac

#global git           20150924

Name:        gpac
Summary:     MPEG-4 multimedia framework
Version:     0.7.1
Release:     8%{?git:.%{git}git}%{?dist}
License:     LGPLv2+
URL:         http://gpac.sourceforge.net/
Source0:     https://github.com/gpac/gpac/archive/v%{version}/gpac-%{version}.tar.gz
# https://github.com/openssl/openssl/issues/1543
# Simply remove the call to SSLeay_add_all_algorithms, the addition is now done automatically and internally in libssl.
Patch0:      openssl-1.1.0.patch
# Upstream commit, fix typo
Patch1:      https://github.com/gpac/gpac/commit/669258a21dcc9827e1496c460af0bff83aa5d654.patch#/fix_typo.patch
# Build fix for ffmpeg-3.5
Patch2:      ffmpeg35_buildfix.patch
#Source9:     gpac-snapshot.sh

BuildRequires:  ImageMagick
BuildRequires:  SDL-devel
BuildRequires:  a52dec-devel
BuildRequires:  librsvg2-devel >= 2.5.0
BuildRequires:  libGLU-devel
BuildRequires:  freeglut-devel
BuildRequires:  freetype-devel >= 2.1.4
BuildRequires:  faad2-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel >= 1.2.5
BuildRequires:  libmad-devel
BuildRequires:  xvidcore-devel >= 1.0.0
BuildRequires:  ffmpeg-devel
BuildRequires:  js-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:  openjpeg-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  zlib-devel
BuildRequires:  libogg-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libtheora-devel
BuildRequires:  libXt-devel
BuildRequires:  libXpm-devel
BuildRequires:  libXv-devel
BuildRequires:  wxGTK-devel
BuildRequires:  xmlrpc-c-devel
BuildRequires:  doxygen graphviz
BuildRequires:  gcc
%{?_with_amr:BuildRequires: amrnb-devel
BuildRequires:  amrwb-devel}
BuildRequires:  gtk+-devel
BuildRequires:  gtk2-devel

%description
GPAC is a multimedia framework based on the MPEG-4 Systems standard developed
from scratch in ANSI C.  The original development goal is to provide a clean,
small and flexible alternative to the MPEG-4 Systems reference software.

GPAC features the integration of recent multimedia standards (SVG/SMIL, VRML,
X3D, SWF, 3GPP(2) tools and more) into a single framework. GPAC also features
MPEG-4 Systems encoders/multiplexers, publishing tools for content distribution
for MP4 and 3GPP(2) files and many tools for scene descriptions
(MPEG4 <-> VRML <-> X3D converters, SWF -> MPEG-4, etc).

%package        libs
Summary:        Library for %{name}

%description    libs
The %{name}-libs package contains library for %{name}.


%package  devel
Summary:  Development libraries and files for %{name}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description  devel
Development libraries and files for gpac.


%package  doc
Summary:  Documentation for %{name}

%description  doc
Documentation for %{name}.


%package  static
Summary:  Development libraries and files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-devel-static < %{version}-%{release}
Provides:  %{name}-devel-static = %{version}-%{release}

%description  static
Static library for gpac.

%prep
%autosetup -p1
rm -r extra_lib/
# Fix encoding warnings
cp -p doc/ipmpx_syntax.bt doc/ipmpx_syntax.bt.origine
iconv -f ISO-8859-1 -t UTF8 doc/ipmpx_syntax.bt.origine >  doc/ipmpx_syntax.bt
touch -r doc/ipmpx_syntax.bt.origine doc/ipmpx_syntax.bt
rm -rf doc/ipmpx_syntax.bt.origine


%build
%configure \
  --enable-debug \
  --extra-cflags="%{optflags} -fPIC -DPIC -D_FILE_OFFSET_BITS=64 -D_LARGE_FILES -D_LARGEFILE_SOURCE=1 -D_GNU_SOURCE=1 $(pkg-config --cflags libavformat)" \
  --X11-path=%{_prefix} \
  --libdir=%{_lib} \
  --disable-oss-audio \
%{?_with_amr:--enable-amr} \
  --disable-static \
  --use-js=no

#Avoid mess with setup.h
cp -p config.h include/gpac

%{make_build} all 
%{make_build} sggen

## kwizart - build doxygen doc for devel
pushd doc
doxygen
popd

%install
%{make_install} install-lib
rm -rf %{buildroot}%{_bindir}/Osmo4

#Install generated sggen binaries
#for b in MPEG4 SVG X3D; do
for b in MPEG4 X3D; do
  pushd applications/generators/${b}
    install -pm 0755 ${b}Gen %{buildroot}%{_bindir}
  popd
done

#Fix doxygen timestamp
touch -r Changelog doc/html-libgpac/*

#config.h like but not only
#Usual multilib bug https://bugzilla.rpmfusion.org/show_bug.cgi?id=270
sed -i -e '/GPAC_CONFIGURATION/d' %{buildroot}%{_includedir}/gpac/configuration.h
touch -r Changelog %{buildroot}%{_includedir}/gpac/*.h
touch -r Changelog %{buildroot}%{_includedir}/gpac/internal/*.h
touch -r Changelog %{buildroot}%{_includedir}/gpac/modules/*.h
rm %{buildroot}%{_includedir}/gpac/config.h


%ldconfig_scriptlets libs

%files
%doc AUTHORS BUGS Changelog README.md TODO
%license COPYING
%{_bindir}/DashCast
%{_bindir}/MP42TS
%{_bindir}/MP4Box
%{_bindir}/MP4Client
%{_bindir}/MPEG4Gen
#{_bindir}/SVGGen
%{_bindir}/X3DGen
%{_datadir}/gpac/
%{_mandir}/man1/*.1.*

%files libs
%{_libdir}/libgpac.so.*
%{_libdir}/gpac/

%files doc
%doc doc/html-libgpac/*

%files devel
%doc doc/CODING_STYLE doc/ipmpx_syntax.bt
%{_includedir}/gpac/
%{_libdir}/libgpac.so

%files static
%{_libdir}/libgpac_static.a


%changelog
* Mon Nov 26 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.7.1-8
- Rename static sub-package

* Sun Nov 25 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.7.1-7
- Remove Group tag
- Add missing isa on Requires
- Drop mozilla support
- Drop osmo support
- Clean up

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.7.1-5
- Rebuilt for new ffmpeg snapshot

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.7.1-3
- Rebuilt for ffmpeg-3.5 git

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.7.1-1
- Update to 0.7.1

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Oct 29 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.6.1-3
- Fix build with openssl-1.1.0

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.6.1-2
- Rebuilt for ffmpeg-3.1.1

* Thu Mar 10 2016 Sérgio Basto <sergio@serjux.com> - 0.6.1-1
- Update to 0.6.1

* Wed Feb 24 2016 Sérgio Basto <sergio@serjux.com> - 0.6.0-1
- Update to 0.6.0
- Remove extra_lib directory from sources, like do gpac-snapshot.sh.
- Add License tag.
- Clean defattr(s).

* Sun Oct 11 2015 Michael Kuhn <suraia@ikkoku.de> - 0.5.2-1
- Update to 0.5.2.

* Sat Dec 06 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.5.1-14.20141206svn
- Update to svn20141206 - last svn rev 5542
- Fix invalid SONAME - rfbz#3365

* Sun Oct 19 2014 Sérgio Basto <sergio@serjux.com> - 0.5.0-13.20140915svn
- Rebuilt for FFmpeg 2.4.3

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.5.0-12.20140915svn
- Rebuilt for FFmpeg 2.4.x

* Mon Sep 15 2014 Sérgio Basto <sergio@serjux.com> - 0.5.0-11.20140915svn
- Update to 20140915
- Some clean ups, fix location of html files.

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 0.5.0-10.20130914svn
- Rebuilt for ffmpeg-2.3

* Tue Mar 25 2014 Sérgio Basto <sergio@serjux.com> - 0.5.0-9.20130914svn
- Rebuilt for ffmpeg-2.2

* Tue Nov 05 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.5.0-8.20130914svn
- Rebuilt for x264/FFmpeg

* Sat Sep 14 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.5.0-7.20130914svn
- Update to 20130914

* Tue Aug 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.5.0-6.20130820svn
- Update to 20130820

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.5.0-5
- Rebuilt for FFmpeg 2.0.x

* Sat May 25 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.5.0-4
- Rebuilt for x264/FFmpeg

* Sun Jan 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.5.0-3
- Rebuilt for FFmpeg/x264

* Sat Nov 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.5.0-2
- Rebuilt for FFmpeg 1.0

* Sat Jun 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.5.0-1
- Update to 0.5.0

* Wed Feb 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.4.6-0.19.svn20110923
- Rebuilt for x264/FFmpeg

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.4.6-0.18.svn20110923
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 03 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.4.6-0.17.svn20110923
- Update gpac-soname.patch

* Fri Sep 23 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.4.6-0.16svn20110923
- Update to 20110923
- Fix svnversion

* Thu Sep 22 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.4.6-0.15svn20110915
- Update to 20110915

* Thu Jul 14 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.4.6-0.14.cvs20100527
- Rebuild

* Sun Jun 05 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.4.6-0.13.cvs20100527
- Rebuild for js update

* Thu Mar 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.4.6-0.12.cvs20100527
- Rebuilt for openjpeg
- Remove usage of --warn-common as LDFLAGS

* Tue Dec 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.6-0.11.cvs20100527
- Fix include - rfbz#1551

* Sun Jul 11 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.6-0.9.cvs20100527
- Fix header installed by misstake - rfbz#270c9

* Sat May 29 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.4.6-0.8.cvs20100527
- Rewrite soname patch that is still needed.
- Allow --with osmo conditional
- Explicitely list binaries.

* Thu May 27 2010 Lucas Jacobs <lucas.jacobs@mines.sdsmt.edu> - 0.4.6-0.6cvs20100527
- Update to 20100527
- Removed upstreamed lib64, soname, OpenJPEG, OpenGL patches
- Update ffmpeg, makefix and amr patches
- Added patch to build osmo4_wx properly

* Sat Mar 13 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.4.6-0.5.cvs20100116
- Fix CFLAGS for large files rfbz#1116

* Sat Feb 27 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.4.6-0.4cvs20100116
- New Attempt to fix rfbz#270

* Sat Jan 16 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.4.6-0.3cvs20100116
- Update to 20100116
- Removed upstreamed patch for system libxml2
- Update ffmpeg patch

* Tue Nov  3 2009 kwizart < kwizart at gmail.com > - 0.4.6-0.2cvs20090919
- Attempt to fix rfbz#270

* Sat Sep 19 2009 kwizart < kwizart at gmail.com > - 0.4.6-0.1cvs20090919
- Update to 0.4.6 pre cvs snapshoot 20090919
- Fix OGL link flag

* Tue Sep  1 2009 kwizart < kwizart at gmail.com > - 0.4.6-0.1cvs20090901
- Update to 0.4.6 pre cvs snapshoot 20090901
- Remove merged patch (1) update old (4)
- Clean static conditional

* Fri Mar 27 2009 kwizart < kwizart at gmail.com > - 0.4.5-7
- Rebuild for faad x264

* Mon Mar 23 2009 kwizart < kwizart at gmail.com > - 0.4.5-6
- Add ffmpeg patch by Rathann (RPM Fusion #454 )
- Fix default defattr

* Wed Feb 11 2009 kwizart < kwizart at gmail.com > - 0.4.5-5
- Rebuild for openssl (#363) - Made possible because the
  circle dependency with gpac/x264 was fixed first (#362)

* Wed Feb 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.4.5-4
- rebuild for new ssl

* Sun Dec 28 2008 kwizart < kwizart at gmail.com > - 0.4.5-3
- Fix -devel doc timestamp which leads to multilib conflict 
  ( RPM Fusion #270 )

* Thu Dec 18 2008 kwizart < kwizart at gmail.com > - 0.4.5-2
- Fix for ppc64

* Wed Dec 17 2008 kwizart < kwizart at gmail.com > - 0.4.5-1
- Update to 0.4.5 (final)
- Drop upstreamed patches - Rewrite some
- Add More BR.
- Conditionalize --with mozilla amr

* Mon Sep  8 2008 kwizart < kwizart at gmail.com > - 0.4.5-0.5.20080217cvs
- Fix for Large File Support (was livna #2075 )

* Mon Feb 25 2008 kwizart < kwizart at gmail.com > - 0.4.5-0.3.20080217cvs
- Enable devel-static
- Conditionalize Osmo4 (buggy).
- Clean the spec

* Sun Feb 17 2008 kwizart < kwizart at gmail.com > - 0.4.5-0.2.20080217cvs
- Update to 20080217.
- Split libs.
- Use the new amr nosrc scheme (need an end-users rebuilt to add support to it).
- Add openjpeg-devel missing BR
- Static patching instead of dyn patch when possible.
- Disable %%{smp_mflags} (it tries to build the bin before the lib is ready)
- Define soname as libgpac.so.0 (instead of libgpac.so.%%version )
- Exclude static lib

* Mon Feb 11 2008 Stewart Adam < s.adam at diffingo.com > - 0.4.5-0.1.20080211cvs
- Use %%{smp_mflags}
- Oops, we're actually 0.4.5
- Fix gpac so filenames
- Only install nposmozilla when %%{with_firefox} is set

* Mon Feb 11 2008 Stewart Adam < s.adam at diffingo.com > - 0.4.4-3.20080211cvs
- Update to 20080211cvs
- Disable osmozilla, doesn't build with xulrunner
- Fix builds with gcc 4.3

* Sat Dec 15 2007 Stewart Adam < s.adam at diffingo.com > - 0.4.4-2
- Rebuild for rawhide

* Tue Oct 16 2007 Stewart Adam < s.adam at diffingo.com > - 0.4.4-1
- Update to v4.4

* Sat May 26 2007 kwizart < kwizart at gmail.com > - 0.4.3-0.1cvs20070526
- Update to cvs 20070526
- Enable conditional build ( 3gpp firefox )

* Wed Apr 11 2007 kwizart < kwizart at gmail.com > - 0.4.3-0.1cvs20070411
- Update to cvs 20070411

* Fri Dec 08 2006 kwizart < kwizart at gmail.com > - 0.4.3-cvs20061208.1.kwizart.fc6
- Update to 20061208
- Uses firefox-devel (since fc6!)
- Drop tutorial
- Use version-DEV-date with libgpac.so
- Disabled osmozilla
- Fix soname 
- Enabled gprof

* Tue Oct 17 2006 kwizart < kwizart at gmail.com > - 0.4.3-cvs20061017.1_FC5
- gpac snapshot.sh
- Revert Patch osmozilla.cpp (v1.17 - build error from gpac/internal/terminal_dev.h)
- TODO: - no-soname make option for libgpac.so
  - static lib in devel - needed ?
  - osmozilla - xpt link problem.
  - Osmo4: segmentation fault on exit.
  - MP4Client: segmentation fault on launch.
  - The program 'Osmo4' received an X Window System error:
  "The error was 'BadMatch (invalid parameter attributes)'.
  (Details: serial 37 error_code 8 request_code 42 minor_code 0)"
  - MP4Box -version display: GPAC version 0.4.3-DEV (try to display cvs )

* Tue Oct 17 2006 kwizart < kwizart at gmail.com > - 0.4.2-rc2.1_FC5
- Update to 0.4.2cvs20061017
- Use DESTDIR=RPM_BUILD_ROOT in various Makefile.
- Enable mozilla plugin: osmozilla.
- Enable AMR_NB_FLOAT and AMR_WB_FLOAT / bundle AMR_NB_FIXED (but not used by default).
- Provide documentation html in doc .
- Provide tutorial from http://www.wildamerica.com/pages/Marty.html
- Various corrections.

* Fri Sep 01 2006 Anssi Hannula <anssi@zarb.org> 0.4.1-0.20060630.2plf2007.0
- lib64 fixes

* Fri Jun 30 2006 Austin Acton <austin@mandriva.org> 0.4.1-0.20060630.1plf2007.0
- initial package
