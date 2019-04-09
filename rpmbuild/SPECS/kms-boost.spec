# Support for documentation installation As the %%doc macro erases the
# target directory ($RPM_BUILD_ROOT%%{_docdir}/%%{name}), manually
# installed documentation must be saved into a temporary dedicated
# directory.
# XXX note that as of rpm 4.9.1, this shouldn't be necessary anymore.
# We should be able to install directly.
%define boost_docdir __tmp_docdir
%define boost_examplesdir __tmp_examplesdir

%{!?compiler: %global compiler gcc}

%ifnarch %{ix86} x86_64
  # Avoid using Boost.Context on non-x86 arches.  s390 is not
  # supported at all and there were _syntax errors_ in PPC code.  This
  # should be enabled on a case-by-case basis as the arches are tested
  # and fixed.
  %bcond_with context
%else
  %bcond_without context
%endif

%global modulefile_path /opt/kms/share/Modules/modulefiles/boost
%global modulefile_path_file %{modulefile_path}/%{version}

Name: kms-boost
%define rname boost
Summary: The free peer-reviewed portable C++ source libraries
Version: 1.55.0
%define _prefix /opt/kms
%define _mandir %{_datadir}/man
%define version_enc 1_55_0
Release: 12%{?dist}
License: Boost and MIT and Python

%define toplev_dirname %{rname}_%{version_enc}
URL: http://www.boost.org
Group: System Environment/Libraries

Source0: http://downloads.sourceforge.net/%{rname}/%{toplev_dirname}.tar.bz2
Source1: ver.py
Source2: libboost_thread.so

# From the version 13 of Fedora, the Boost libraries are delivered
# with sonames equal to the Boost version (e.g., 1.41.0).
%define sonamever %{version}

# boost is an "umbrella" package that pulls in all other boost
# components, except for MPI and Python 3 sub-packages.  Those are
# special in that they are rarely necessary, and it's not a big burden
# to have interested parties install them explicitly.
Requires: %{name}-atomic = %{version}-%{release}
Requires: %{name}-chrono = %{version}-%{release}
%if %{with context}
Requires: %{name}-context = %{version}-%{release}
%endif
Requires: %{name}-coroutine = %{version}-%{release}
Requires: %{name}-date-time = %{version}-%{release}
Requires: %{name}-filesystem = %{version}-%{release}
Requires: %{name}-graph = %{version}-%{release}
Requires: %{name}-iostreams = %{version}-%{release}
Requires: %{name}-locale = %{version}-%{release}
Requires: %{name}-log = %{version}-%{release}
Requires: %{name}-math = %{version}-%{release}
Requires: %{name}-program-options = %{version}-%{release}
Requires: %{name}-python = %{version}-%{release}
Requires: %{name}-random = %{version}-%{release}
Requires: %{name}-regex = %{version}-%{release}
Requires: %{name}-serialization = %{version}-%{release}
Requires: %{name}-signals = %{version}-%{release}
Requires: %{name}-system = %{version}-%{release}
Requires: %{name}-test = %{version}-%{release}
Requires: %{name}-thread = %{version}-%{release}
Requires: %{name}-timer = %{version}-%{release}
Requires: %{name}-wave = %{version}-%{release}

BuildRequires: m4
BuildRequires: libstdc++-devel%{?_isa}
BuildRequires: bzip2-devel%{?_isa}
BuildRequires: zlib-devel%{?_isa}
BuildRequires: python-devel%{?_isa}
BuildRequires: libicu-devel%{?_isa}

# https://svn.boost.org/trac/boost/ticket/6150
Patch4: boost-1.50.0-fix-non-utf8-files.patch

# Add a manual page for bjam, based on the on-line documentation:
# http://www.boost.org/boost-build2/doc/html/bbv2/overview.html
Patch5: boost-1.48.0-add-bjam-man-page.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=781859
# The following tickets have yet to be fixed by upstream.
# https://svn.boost.org/trac/boost/ticket/6413
Patch9: boost-1.55.0-attribute.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=828856
# https://bugzilla.redhat.com/show_bug.cgi?id=828857
Patch15: boost-1.50.0-pool.patch

# https://svn.boost.org/trac/boost/ticket/8844
Patch23: boost-1.54.0-bind-static_assert.patch

# https://svn.boost.org/trac/boost/ticket/8847
Patch24: boost-1.54.0-concept-unused_typedef.patch

# https://svn.boost.org/trac/boost/ticket/5637
Patch25: boost-1.54.0-mpl-print.patch

# https://svn.boost.org/trac/boost/ticket/8859
Patch26: boost-1.54.0-static_warning-unused_typedef.patch

# https://svn.boost.org/trac/boost/ticket/8853
Patch31: boost-1.54.0-tuple-unused_typedef.patch

# https://svn.boost.org/trac/boost/ticket/8854
Patch32: boost-1.54.0-random-unused_typedef.patch

# https://svn.boost.org/trac/boost/ticket/8856
Patch33: boost-1.54.0-date_time-unused_typedef.patch
Patch34: boost-1.54.0-date_time-unused_typedef-2.patch

# https://svn.boost.org/trac/boost/ticket/8870
Patch35: boost-1.54.0-spirit-unused_typedef.patch
Patch36: boost-1.54.0-spirit-unused_typedef-2.patch

# https://svn.boost.org/trac/boost/ticket/8871
Patch37: boost-1.54.0-numeric-unused_typedef.patch

# https://svn.boost.org/trac/boost/ticket/8878
Patch45: boost-1.54.0-locale-unused_typedef.patch

# https://svn.boost.org/trac/boost/ticket/8879
Patch46: boost-1.54.0-property_tree-unused_typedef.patch

# https://svn.boost.org/trac/boost/ticket/8888
Patch49: boost-1.54.0-python-unused_typedef.patch

# https://svn.boost.org/trac/boost/ticket/9038
Patch51: boost-1.54.0-pool-test_linking.patch

# This was already fixed upstream, so no tracking bug.
Patch53: boost-1.54.0-pool-max_chunks_shadow.patch

# https://svn.boost.org/trac/boost/ticket/9041
Patch54: boost-1.55.0-atomic-check_lock_free_flag.patch

%bcond_with tests
%bcond_with docs_generated

%description
Boost provides free peer-reviewed portable C++ source libraries.  The
emphasis is on libraries which work well with the C++ Standard
Library, in the hopes of establishing "existing practice" for
extensions and providing reference implementations so that the Boost
libraries are suitable for eventual standardization. (Some of the
libraries have already been included in the C++ 2011 standard and
others have been proposed to the C++ Standards Committee for inclusion
in future standards.)

%package atomic
Summary: Run-Time component of boost atomic library
Group: System Environment/Libraries

%description atomic

Run-Time support for Boost.Atomic, a library that provides atomic data
types and operations on these data types, as well as memory ordering
constraints required for coordinating multiple threads through atomic
variables.

%package chrono
Summary: Run-Time component of boost chrono library
Group: System Environment/Libraries
Requires: %{name}-system = %{version}-%{release}

%description chrono

Run-Time support for Boost.Chrono, a set of useful time utilities.

%if %{with context}
%package context
Summary: Run-Time component of boost context switching library
Group: System Environment/Libraries

%description context

Run-Time support for Boost.Context, a foundational library that
provides a sort of cooperative multitasking on a single thread.
%endif

%package coroutine
Summary:  Run-Time component of boost coroutine library
Group: System Environment/Libraries

%description coroutine
Boost.Coroutine provides templates for generalized subroutines which allow
multiple entry points for suspending and resuming execution at certain
locations. It preserves the local state of execution and allows re-entering
subroutines more than once (useful if state must be kept across function
calls).

Coroutines can be viewed as a language-level construct providing a special
kind of control flow.

In contrast to threads, which are pre-emptive, coroutine switches are
cooperative (programmer controls when a switch will happen). The kernel is
not involved in the coroutine switches.

%package date-time
Summary: Run-Time component of boost date-time library
Group: System Environment/Libraries

%description date-time

Run-Time support for Boost Date Time, set of date-time libraries based
on generic programming concepts.

%package filesystem
Summary: Run-Time component of boost filesystem library
Group: System Environment/Libraries
Requires: %{name}-system = %{version}-%{release}

%description filesystem

Run-Time support for the Boost Filesystem Library, which provides
portable facilities to query and manipulate paths, files, and
directories.

%package graph
Summary: Run-Time component of boost graph library
Group: System Environment/Libraries
Requires: %{name}-regex = %{version}-%{release}

%description graph

Run-Time support for the BGL graph library.  BGL interface and graph
components are generic, in the same sense as the the Standard Template
Library (STL).

%package iostreams
Summary: Run-Time component of boost iostreams library
Group: System Environment/Libraries

%description iostreams

Run-Time support for Boost.IOStreams, a framework for defining streams,
stream buffers and i/o filters.

%package locale
Summary: Run-Time component of boost locale library
Group: System Environment/Libraries
Requires: %{name}-chrono = %{version}-%{release}
Requires: %{name}-system = %{version}-%{release}
Requires: %{name}-thread = %{version}-%{release}

%description locale

Run-Time support for Boost.Locale, a set of localization and Unicode
handling tools.

%package log
Summary: Run-Time component of boost logging library
Group: System Environment/Libraries

%description log

Boost.Log library aims to make logging significantly easier for the
application developer.  It provides a wide range of out-of-the-box
tools along with public interfaces for extending the library.

%package math
Summary: Math functions for boost TR1 library
Group: System Environment/Libraries

%description math

Run-Time support for C99 and C++ TR1 C-style Functions from math
portion of Boost.TR1.

%package program-options
Summary:  Run-Time component of boost program_options library
Group: System Environment/Libraries

%description program-options

Run-Time support of boost program options library, which allows program
developers to obtain (name, value) pairs from the user, via
conventional methods such as command line and configuration file.

%package python
Summary: Run-Time component of boost python library
Group: System Environment/Libraries

%description python

The Boost Python Library is a framework for interfacing Python and
C++. It allows you to quickly and seamlessly expose C++ classes
functions and objects to Python, and vice versa, using no special
tools -- just your C++ compiler.  This package contains run-time
support for Boost Python Library.

%package random
Summary: Run-Time component of boost random library
Group: System Environment/Libraries

%description random

Run-Time support for boost random library.

%package regex
Summary: Run-Time component of boost regular expression library
Group: System Environment/Libraries

%description regex

Run-Time support for boost regular expression library.

%package serialization
Summary: Run-Time component of boost serialization library
Group: System Environment/Libraries

%description serialization

Run-Time support for serialization for persistence and marshaling.

%package signals
Summary: Run-Time component of boost signals and slots library
Group: System Environment/Libraries

%description signals

Run-Time support for managed signals & slots callback implementation.

%package system
Summary: Run-Time component of boost system support library
Group: System Environment/Libraries

%description system

Run-Time component of Boost operating system support library, including
the diagnostics support that will be part of the C++0x standard
library.

%package test
Summary: Run-Time component of boost test library
Group: System Environment/Libraries

%description test

Run-Time support for simple program testing, full unit testing, and for
program execution monitoring.

%package thread
Summary: Run-Time component of boost thread library
Group: System Environment/Libraries
Requires: %{name}-system = %{version}-%{release}

%description thread

Run-Time component Boost.Thread library, which provides classes and
functions for managing multiple threads of execution, and for
synchronizing data between the threads or providing separate copies of
data specific to individual threads.

%package timer
Summary: Run-Time component of boost timer library
Group: System Environment/Libraries
Requires: %{name}-chrono = %{version}-%{release}
Requires: %{name}-system = %{version}-%{release}

%description timer

"How long does my C++ code take to run?"
The Boost Timer library answers that question and does so portably,
with as little as one #include and one additional line of code.

%package wave
Summary: Run-Time component of boost C99/C++ pre-processing library
Group: System Environment/Libraries
Requires: %{name}-chrono = %{version}-%{release}
Requires: %{name}-date-time = %{version}-%{release}
Requires: %{name}-filesystem = %{version}-%{release}
Requires: %{name}-system = %{version}-%{release}
Requires: %{name}-thread = %{version}-%{release}

%description wave

Run-Time support for the Boost.Wave library, a Standards conforming,
and highly configurable implementation of the mandated C99/C++
pre-processor functionality.

%package devel
Summary: The Boost C++ headers and shared development libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Provides: %{name}-python-devel = %{version}-%{release}
Requires: libicu-devel%{?_isa}

%description devel
Headers and shared object symbolic links for the Boost C++ libraries.

%package static
Summary: The Boost C++ static development libraries
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}
Provides: %{name}-devel-static = %{version}-%{release}

%description static
Static Boost C++ libraries.

%package doc
Summary: HTML documentation for the Boost C++ libraries
Group: Documentation
%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
BuildArch: noarch
%endif
Provides: %{name}-python-docs = %{version}-%{release}

# See the description above.
Provides: odeint-doc = 2.2-5

%description doc
This package contains the documentation in the HTML format of the Boost C++
libraries. The documentation provides the same content as that on the Boost
web page (http://www.boost.org/doc/libs/1_40_0).

%package examples
Summary: Source examples for the Boost C++ libraries
Group: Documentation
%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
BuildArch: noarch
%endif
Requires: %{name}-devel = %{version}-%{release}

%description examples
This package contains example source files distributed with boost.

%package build
Summary: Cross platform build system for C++ projects
Group: Development/Tools
Requires: %{name}-jam
BuildArch: noarch

%description build
Boost.Build is an easy way to build C++ projects, everywhere. You name
your pieces of executable and libraries and list their sources.  Boost.Build
takes care about compiling your sources with the right options,
creating static and shared libraries, making pieces of executable, and other
chores -- whether you're using GCC, MSVC, or a dozen more supported
C++ compilers -- on Windows, OSX, Linux and commercial UNIX systems.

%package jam
Summary: A low-level build tool
Group: Development/Tools

%description jam
Boost.Jam (BJam) is the low-level build engine tool for Boost.Build.
Historically, Boost.Jam is based on on FTJam and on Perforce Jam but has grown
a number of significant features and is now developed independently

%prep
%setup -q -n %{toplev_dirname}

%patch4 -p1
%patch5 -p1
%patch9 -p1
%patch15 -p0
%patch23 -p1
%patch24 -p1
%patch25 -p0
%patch26 -p1
%patch31 -p0
%patch32 -p0
%patch33 -p0
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch45 -p1
%patch46 -p1
%patch49 -p1
%patch51 -p1
%patch53 -p1
%patch54 -p1

# At least python2_version needs to be a macro so that it's visible in
# %%install as well.
%global python2_version %(/usr/bin/python2 %{SOURCE1})

%build
: PYTHON2_VERSION=%{python2_version}

cat >> ./tools/build/v2/user-config.jam << EOF
# There are many strict aliasing warnings, and it's not feasible to go
# through them all at this time.
using gcc : : : <compileflags>-fno-strict-aliasing ;
using mpi ;
EOF

./bootstrap.sh --with-toolset=gcc --with-icu

# N.B. When we build the following with PCH, parts of boost (math
# library in particular) end up being built second time during
# installation.  Unsure why that is, but all sub-builds need to be
# built with pch=off to avoid this.
#
# The "python=2.*" bit tells jam that we want to _also_ build 2.*, not
# just 3.*.  When omitted, it just builds for python 3 twice, once
# calling the library libboost_python and once libboost_python3.  I
# assume this is for backward compatibility for apps that are used to
# linking against -lboost_python, for when 2->3 transition is
# eventually done.

echo ============================= build serial ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--without-mpi --without-graph_parallel --build-dir=serial \
%if !%{with context}
	--without-context --without-coroutine \
%endif
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python2_version} stage

# See boost-1.54.0-thread-link_atomic.patch for where this file comes
# from.
if [ $(find serial -type f -name has_atomic_flag_lockfree \
		-print -quit | wc -l) -ne 0 ]; then
	DEF=D
else
	DEF=U
fi

m4 -${DEF}HAS_ATOMIC_FLAG_LOCKFREE -DVERSION=%{version} \
	%{SOURCE2} > $(basename %{SOURCE2})

echo ============================= build Boost.Build ==================
(cd tools/build/v2
 ./bootstrap.sh --with-toolset=gcc)

%check
:


%install
rm -rf $RPM_BUILD_ROOT
cd %{_builddir}/%{toplev_dirname}

echo ============================= install serial ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--without-mpi --without-graph_parallel --build-dir=serial \
%if !%{with context}
	--without-context --without-coroutine \
%endif
	--prefix=$RPM_BUILD_ROOT%{_prefix} \
	--libdir=$RPM_BUILD_ROOT%{_libdir} \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python2_version} install

# Override DSO symlink with a linker script.  See the linker script
# itself for details of why we need to do this.
[ -f $RPM_BUILD_ROOT%{_libdir}/libboost_thread.so ] # Must be present
rm -f $RPM_BUILD_ROOT%{_libdir}/libboost_thread.so
install -p -m 644 $(basename %{SOURCE2}) $RPM_BUILD_ROOT%{_libdir}/

echo ============================= install Boost.Build ==================
(cd tools/build/v2
 ./b2 --prefix=$RPM_BUILD_ROOT%{_prefix} install
 # Fix some permissions
 chmod -x $RPM_BUILD_ROOT%{_datadir}/boost-build/build/alias.py
 chmod +x $RPM_BUILD_ROOT%{_datadir}/boost-build/tools/doxproc.py
 # We don't want to distribute this
 rm -f $RPM_BUILD_ROOT%{_bindir}/b2
 # Not a real file
 rm -f $RPM_BUILD_ROOT%{_datadir}/boost-build/build/project.ann.py
 # Empty file
 rm -f $RPM_BUILD_ROOT%{_datadir}/boost-build/tools/doxygen/windows-paths-check.hpp
 # Install the manual page
 %{__install} -p -m 644 doc/bjam.1 -D $RPM_BUILD_ROOT%{_mandir}/man1/bjam.1
)

# Install documentation files (HTML pages) within the temporary place
echo ============================= install documentation ==================
# Prepare the place to temporary store the generated documentation
rm -rf %{boost_docdir} && %{__mkdir_p} %{boost_docdir}/html
DOCPATH=%{boost_docdir}
DOCREGEX='.*\.\(html?\|css\|png\|gif\)'

find libs doc more -type f -regex $DOCREGEX \
    | sed -n '/\//{s,/[^/]*$,,;p}' \
    | sort -u > tmp-doc-directories

sed "s:^:$DOCPATH/:" tmp-doc-directories \
    | xargs -P 0 --no-run-if-empty %{__install} -d

cat tmp-doc-directories | while read tobeinstalleddocdir; do
    find $tobeinstalleddocdir -mindepth 1 -maxdepth 1 -regex $DOCREGEX \
    | xargs -P 0 %{__install} -p -m 644 -t $DOCPATH/$tobeinstalleddocdir
done
rm -f tmp-doc-directories
%{__install} -p -m 644 -t $DOCPATH LICENSE_1_0.txt index.htm index.html boost.png rst.css boost.css

echo ============================= install examples ==================
# Fix a few non-standard issues (DOS and/or non-UTF8 files)
sed -i -e 's/\r//g' libs/geometry/example/ml02_distance_strategy.cpp
for tmp_doc_file in flyweight/example/Jamfile.v2 \
 format/example/sample_new_features.cpp multi_index/example/Jamfile.v2 \
 multi_index/example/hashed.cpp serialization/example/demo_output.txt \
 test/example/cla/wide_string.cpp
do
  mv libs/${tmp_doc_file} libs/${tmp_doc_file}.iso8859
  iconv -f ISO8859-1 -t UTF8 < libs/${tmp_doc_file}.iso8859 > libs/${tmp_doc_file}
  touch -r libs/${tmp_doc_file}.iso8859 libs/${tmp_doc_file}
  rm -f libs/${tmp_doc_file}.iso8859
done

# Prepare the place to temporary store the examples
rm -rf %{boost_examplesdir} && mkdir -p %{boost_examplesdir}/html
EXAMPLESPATH=%{boost_examplesdir}
find libs -type d -name example -exec find {} -type f \; \
    | sed -n '/\//{s,/[^/]*$,,;p}' \
    | sort -u > tmp-doc-directories
sed "s:^:$EXAMPLESPATH/:" tmp-doc-directories \
    | xargs -P 0 --no-run-if-empty %{__install} -d
rm -f tmp-doc-files-to-be-installed && touch tmp-doc-files-to-be-installed
cat tmp-doc-directories | while read tobeinstalleddocdir
do
  find $tobeinstalleddocdir -mindepth 1 -maxdepth 1 -type f \
    >> tmp-doc-files-to-be-installed
done
cat tmp-doc-files-to-be-installed | while read tobeinstalledfiles
do
  if test -s $tobeinstalledfiles
  then
    tobeinstalleddocdir=`dirname $tobeinstalledfiles`
    %{__install} -p -m 644 -t $EXAMPLESPATH/$tobeinstalleddocdir $tobeinstalledfiles
  fi
done
rm -f tmp-doc-files-to-be-installed
rm -f tmp-doc-directories
%{__install} -p -m 644 -t $EXAMPLESPATH LICENSE_1_0.txt

# modules!!
mkdir -p $RPM_BUILD_ROOT%{modulefile_path}
cat > $RPM_BUILD_ROOT%{modulefile_path_file} <<ENDMODULEFILE
#%Module

# NOTE: This is an automatically-generated file!  (generated by the
# %{name} rpm).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

proc ModulesHelp { } {
   puts stderr "This module adds %{name} %{version} to various paths"
}

module-whatis   "Sets up %{name} %{version}"

setenv BOOSTHOME "%{_prefix}"
prepend-path PATH "%{_bindir}"
prepend-path LD_LIBRARY_PATH "%{_libdir}"
prepend-path LIBRARY_PATH "%{_libdir}"
append-path -d { } LDFLAGS "-L%{_libdir}"
append-path -d { } INCLUDE "-I%{_includedir}"
append-path CPATH "%{_includedir}"
append-path -d { } LOCAL_LDFLAGS "-L%{_libdir}"
append-path -d { } LOCAL_INCLUDE "-I%{_includedir}"
append-path -d { } LOCAL_CFLAGS "-I%{_includedir}"
append-path -d { } LOCAL_CXXFLAGS "-I%{_includedir}"
ENDMODULEFILE

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%dir %{modulefile_path}
%{modulefile_path_file}

%files atomic
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_atomic.so.%{sonamever}

%files chrono
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_chrono.so.%{sonamever}

%if %{with context}
%files context
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_context.so.%{sonamever}
%endif

%files coroutine
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_coroutine.so.%{sonamever}

%files date-time
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_date_time.so.%{sonamever}

%files filesystem
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_filesystem.so.%{sonamever}

%files graph
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_graph.so.%{sonamever}

%files iostreams
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_iostreams.so.%{sonamever}

%files locale
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_locale.so.%{sonamever}

%files log
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_log.so.%{sonamever}
%{_libdir}/libboost_log_setup.so.%{sonamever}

%files math
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_math_c99.so.%{sonamever}
%{_libdir}/libboost_math_c99f.so.%{sonamever}
%{_libdir}/libboost_math_c99l.so.%{sonamever}
%{_libdir}/libboost_math_tr1.so.%{sonamever}
%{_libdir}/libboost_math_tr1f.so.%{sonamever}
%{_libdir}/libboost_math_tr1l.so.%{sonamever}

%files test
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_prg_exec_monitor.so.%{sonamever}
%{_libdir}/libboost_unit_test_framework.so.%{sonamever}

%files program-options
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_program_options.so.%{sonamever}

%files python
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_python.so.%{sonamever}

%files random
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_random.so.%{sonamever}

%files regex
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_regex.so.%{sonamever}

%files serialization
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_serialization.so.%{sonamever}
%{_libdir}/libboost_wserialization.so.%{sonamever}

%files signals
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_signals.so.%{sonamever}

%files system
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_system.so.%{sonamever}

%files thread
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_thread.so.%{sonamever}

%files timer
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_timer.so.%{sonamever}

%files wave
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/libboost_wave.so.%{sonamever}

%files doc
%defattr(-, root, root, -)
%doc %{boost_docdir}/*

%files examples
%defattr(-, root, root, -)
%doc %{boost_examplesdir}/*

%files devel
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_includedir}/boost
%{_libdir}/libboost_atomic.so
%{_libdir}/libboost_chrono.so
%if %{with context}
%{_libdir}/libboost_context.so
%endif
%{_libdir}/libboost_coroutine.so
%{_libdir}/libboost_date_time.so
%{_libdir}/libboost_filesystem.so
%{_libdir}/libboost_graph.so
%{_libdir}/libboost_iostreams.so
%{_libdir}/libboost_locale.so
%{_libdir}/libboost_log.so
%{_libdir}/libboost_log_setup.so
%{_libdir}/libboost_math_tr1.so
%{_libdir}/libboost_math_tr1f.so
%{_libdir}/libboost_math_tr1l.so
%{_libdir}/libboost_math_c99.so
%{_libdir}/libboost_math_c99f.so
%{_libdir}/libboost_math_c99l.so
%{_libdir}/libboost_prg_exec_monitor.so
%{_libdir}/libboost_unit_test_framework.so
%{_libdir}/libboost_program_options.so
%{_libdir}/libboost_python.so
%{_libdir}/libboost_random.so
%{_libdir}/libboost_regex.so
%{_libdir}/libboost_serialization.so
%{_libdir}/libboost_wserialization.so
%{_libdir}/libboost_signals.so
%{_libdir}/libboost_system.so
%{_libdir}/libboost_thread.so
%{_libdir}/libboost_timer.so
%{_libdir}/libboost_wave.so

%files static
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_libdir}/*.a
%if %{with mpich}
%{_libdir}/mpich/lib/*.a
%endif

%files build
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_datadir}/boost-build/

%files jam
%defattr(-, root, root, -)
%doc LICENSE_1_0.txt
%{_bindir}/bjam
%{_mandir}/man1/bjam.1*

%changelog
* Sat Apr 6 2019 pkgs.cloud - 1.55.0-12
- Rebuild for Kurento

* Wed Feb 12 2014 Petr Machata <pmachata@redhat.com> - 1.54.0-11
- Rebuild for ICU soname bump.

* Thu Jan  9 2014 Petr Machata <pmachata@redhat.com> - 1.54.0-10
- Add ppc64le to the list of arches that OpenMPI and MPICH don't
  support.

* Wed Dec 18 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.54.0-9
- Enable MPICH and OpenMPI support on ARM as it's long had them both

* Fri Dec 13 2013 Petr Machata <pmachata@redhat.com> - 1.54.0-8
- Add aarch64 into the list of arches that OpenMPI doesn't support.

* Sun Dec  1 2013 Petr Machata <pmachata@redhat.com> - 1.54.0-7
- Fix shameful blunders in implementation of the previous fix: don't
  hard-code path to has_atomic_flag_lockfree binary; use m4 instead of
  cpp, cpp in F19+ prefixes output with a bunch of comments.

* Wed Nov 27 2013 Petr Machata <pmachata@redhat.com> - 1.54.0-6
- Add libboost_atomic.so.* to the libboost_thread.so linker script on
  architectures that need it.

* Thu Aug 29 2013 Petr Machata <pmachata@redhat.com> - 1.54.0-5
- Fix atomic_cas32 (thanks Jaroslav Škarvada for figuring out where
  the problem is) (boost-1.54.0-interprocess-atomic_cas32-ppc.patch)

* Fri Aug 23 2013 Petr Machata <pmachata@redhat.com> - 1.54.0-4
- Fix compilation of Boost.Pool test cases
  (boost-1.54.0-pool-test_linking.patch)
- Fix -Wshadow warnings in Boost.Pool
  (boost-1.54.0-pool-max_chunks_shadow.patch)
- -Wshadow warnings in Boost.Thread
  (boost-1.54.0-thread-cond_variable_shadow.patch)
- libboost_thread.so.* lacks DT_NEEDED on libboost_atomic.so.* on
  s390.  (boost-1.54.0-thread-link_atomic.patch)

* Mon Aug 19 2013 Petr Machata <pmachata@redhat.com> - 1.54.0-3
- Bump odeint obsoletes and provides a notch to cover a build that
  sneaked into rawhide (bug 892850).

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 1.54.0-2
- Fix detection of availability of 128-bit integers in
  Boost.LexicalCast (boost-1.54.0-lexical_cast-int128.patch)

* Fri Jul 26 2013 Petr Machata <pmachata@redhat.com> - 1.54.0-1
- Rebase to 1.54.0
  - Add new sub-package boost-log
  - Boost.Coroutine is only enabled if Boost.Context is
  - Drop boost-1.53-context.patch (interesting parts now upstream)
  - Drop boost-1.50.0-foreach.patch (#define foreach now discouraged)
  - Drop several unused typedef patches that are now upstream.
    (boost-1.53.0-static_assert-unused_typedef.patch,
    boost-1.53.0-fpclassify-unused_typedef.patch,
    boost-1.53.0-math-unused_typedef-3.patch,
    boost-1.53.0-lexical_cast-unused_typedef.patch,
    boost-1.53.0-regex-unused_typedef.patch,
    boost-1.53.0-thread-unused_typedef.patch)
  - Add release notes patches (001-coroutine.patch,
    002-date-time.patch, 003-log.patch)
  - Add additional unused typedefs in Boost.Math
    (boost-1.54.0-math-unused_typedef-2.patch)
- Drop symlinks from libboost_{thread,locale,atomic}.so -> *-mt.so,
  which we don't need anymore, as we ditched the tagged layout.

* Fri Jul 26 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-12
- There's no physical difference between single-threaded and
  multi-threaded builds, except some libraries are only built in
  multi-threaded mode.  So build everything in multi-threaded mode,
  and ditch tagged layout, which we don't need anymore.
  https://bugzilla.redhat.com/show_bug.cgi?id=971956

* Fri Jul 26 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-11
- Add Obsoletes for odeint (bug 892850)

* Thu Jul 25 2013 Deji Akingunola <dakingun@gmail.com> - 1.53.0-10
- Add Provides and Obsoletes for the mpich2->mpich renames

* Wed Jul 24 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-9
- Add explicit dependencies between some of the boost sub-packages

* Tue Jul 23 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-8
- MPICH2 became MPICH -- rename subpackages, dependencies and
  conditionals.
- Install supporting files (images etc.) for documentation
  (courtesy Marcel Metz, bug 985593)
- Add many patches for silencing unused local typedef warnings
  (boost-1.53.0-static_assert-unused_typedef.patch,
  boost-1.54.0-bind-static_assert.patch,
  boost-1.54.0-concept-unused_typedef.patch,
  boost-1.54.0-static_warning-unused_typedef.patch,
  boost-1.54.0-math-unused_typedef.patch,
  boost-1.54.0-math-unused_typedef-2.patch,
  boost-1.53.0-fpclassify-unused_typedef.patch,
  boost-1.54.0-math-unused_typedef-3.patch,
  boost-1.54.0-tuple-unused_typedef.patch,
  boost-1.54.0-random-unused_typedef.patch,
  boost-1.54.0-date_time-unused_typedef.patch,
  boost-1.54.0-date_time-unused_typedef-2.patch,
  boost-1.54.0-spirit-unused_typedef.patch,
  boost-1.54.0-spirit-unused_typedef-2.patch,
  boost-1.54.0-numeric-unused_typedef.patch,
  boost-1.54.0-multiprecision-unused_typedef.patch,
  boost-1.53.0-lexical_cast-unused_typedef.patch,
  boost-1.53.0-regex-unused_typedef.patch,
  boost-1.53.0-thread-unused_typedef.patch,
  boost-1.54.0-unordered-unused_typedef.patch,
  boost-1.54.0-algorithm-unused_typedef.patch,
  boost-1.53.0-graph-unused_typedef.patch,
  boost-1.54.0-locale-unused_typedef.patch,
  boost-1.54.0-property_tree-unused_typedef.patch,
  boost-1.54.0-xpressive-unused_typedef.patch,
  boost-1.54.0-mpi-unused_typedef.patch,
  boost-1.54.0-python-unused_typedef.patch)
- Add a patch to turn off execstack in Boost.Context
  (boost-1.54.0-context-execstack.patch)
- Fix boost::mpl::print on GCC (boost-1.54.0-mpl-print.patch)
- Add symlinks for /usr/lib/libboost_{thread,locale}.so -> *-mt.so

* Wed Jun 26 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-7
- Fix detection of availability of {,u}int64_t in glibc headers.
  (boost-1.53.0-__GLIBC_HAVE_LONG_LONG.patch)

* Wed Mar  6 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-6
- libboost_context.so must be guarded by conditional in the expanded
  filelist at boost-devel.

* Tue Mar  5 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-5
- Split off Python 3 DSO symlink to a separate subpackage
  boost-python3-devel.  This makes it possible to install
  boost-devel separately, without Python 3 support.
- Build with -fno-strict-aliasing

* Wed Feb 27 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-4
- Make Boost.Context support conditional

* Mon Feb 11 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-3
- Fix Boost.Context on ppc64
- Future-proof the linker script boost_thread-mt.so

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.53.0-2
- Fixed the libboost_thread-mt.so script (which wrongly referred to Boost-1.50)

* Fri Feb  8 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-1
- Upstream 1.53.0 beta1
  - Drop boost-1.50.0-signals-erase.patch
  - Port boost-1.50.0-attribute.patch
  - Drop boost-1.50.0-polygon.patch
  - New sub-packages boost-atomic and boost-context

* Sat Jan 26 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.50.0-7
- Rebuild for icu soname bump

* Sat Nov 03 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.50.0-6
- Rebuild for the new MPICH2 (and libmpich2 soname bump)

* Thu Aug 16 2012 Petr Machata <pmachata@redhat.com> - 1.50.0-5
- Update %%description to reflect current state of C++
  standardization.  Courtesy of Jonathan Wakely.  (#837813)

* Wed Aug 15 2012 Petr Machata <pmachata@redhat.com> - 1.50.0-4
- Override boost_thread-mt.so with a linker script that brings in
  Boost.System DSO as well.

* Wed Aug  8 2012 Petr Machata <pmachata@redhat.com> - 1.50.0-3
- boost-python3 shouldn't be under the overall boost umbrella

* Tue Aug  7 2012 Petr Machata <pmachata@redhat.com> - 1.50.0-2
- Enable Python 3 builds.  This is still disabled in Boost MPI, which
  doesn't seem to support Python 3

* Thu Jul 26 2012 Petr Machata <pmachata@redhat.com> - 1.50.0-1
- Upstream 1.50
  - boost-cmake-soname.patch drop, upstream handles soname well, and
    we haven't been doing manual numbering for several years now
  - boost-1.48.0-cmakeify-full.patch drop, not necessary for bjam
  - Rebase many patches, port others, courtesy of Denis Arnaud:
    - boost-1.48.0-exceptions.patch drop
    - boost-1.48.0-lexical_cast-incomplete.patch drop
    - boost-1.48.0-gcc47-pthreads.patch drop
    - boost-1.48.0-long-double.patch drop
    - boost-1.48.0-xtime.patch drop
    - boost-1.48.0-locale.patch drop
    - boost-1.48.0-signals-erase.patch port
    - boost-1.48.0-fix-non-utf8-files.patch port
    - boost-1.48.0-foreach.patch port
    - boost-1.48.0-attribute.patch port
    - boost-1.48.0-long-double-1.patch port
    - boost-1.48.0-polygon.patch port
    - boost-1.48.0-pool.patch port

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-16
- Build Boost.Locale backends
- Resolves: #832265

* Wed Jun  6 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-15
- In Boost.Pool, be careful not to overflow allocated chunk size.
- Resolves: #828857

* Thu May 24 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-14
- Don't attempt to install Python 3 portions of boost when given
  --without python3
- glibc newly defines a macro TIME_UTC, which collides with
  boost::TIME_UTC.  We can't avoid expanding that macro, but the value
  happens to be the same as that of boost::TIME_UTC.  So drop enum
  xtime_clock_types.  Update boost to use macro TIME_UTC instead of
  the scoped enum value.  External clients will have to do the same.
- Resolves: #824810
- BR on hwloc-devel shouldn't be required anymore (see #814798)

* Wed May  2 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-13
- Support building boost-python against Python 3
- Resolves: #807780

* Sun Apr 22 2012 Robert Scheck <robert@fedoraproject.org> - 1.48.0-12
- Included -math subpackage into umbrella package
- Added missing /sbin/ldconfig for -math subpackage

* Fri Apr 20 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-11
- Add hwloc-devel BR to work around a probable bug in openmpi-devel
  which fails to pull it in

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48.0-10
- Rebuilt for c++ ABI breakage

* Wed Jan 25 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-9
- Only build the long double math libraries on arches that support
  long double.
- ARM was considered unsupporting, because libc defines
  __NO_LONG_DOUBLE_MATH.  Ignore this setting, ARM has perfectly
  working long double that just happens to be only as long as double.
- Resolves: #783660
- Add a missing sort adaptor include to boost polygon
- Resolves: #784654

* Mon Jan 16 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-8
- Add underscores around several uses of __attribute__((X)) to prevent
  interactions with user-defined macro X
- Resolves: #781859

* Sat Jan 14 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.48.0-7
- Added source source files for mingw cross-compilation of Boost.Locale.
- Resolves: #781751

* Sat Jan  7 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.48.0-6
- Added the Boost.Timer sub-package. Resolves: #772397

* Wed Jan  4 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.48.0-5
- Integrated into "upstream" (CMake-ified Boost) the Boost.TR1/Math patch.

* Wed Jan  4 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-4
- Build math portion of Boost.TR1, package DSOs in boost-math.
- Resolves: #771370

* Tue Jan  3 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-3
- Add an upstream patch for BOOST_ENABLE_THREADS

* Tue Nov 29 2011 Petr Machata <pmachata@redhat.com> - 1.48.0-2
- Add an upstream patch for BOOST_FOREACH declaration issue #756005
- Add a proposed patch for error in boost lexical_cast #757385

* Sat Nov 19 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.48.0-1
- Upgrade to Boost-1.48.0, adding two new header-only components
  (Container and Move) and a new library (Locale).
- Resolves: #754865
- Added a patch with a manual page for the bjam executable.
- Added a patch to fix the non-UTF8-encoded example source file.
- Re-worked a little bit the example section, so as to fix the
  DOS-formatted and the ISO-8859-encoded files.

* Thu Nov  3 2011 Petr Machata <pmachata@redhat.com> - 1.47.0-7
- Use <boost/tr1/tuple> instead of C++11 header <tuple> in boost math.
- Resolves: #751210

* Fri Sep  9 2011 Petr Machata <pmachata@redhat.com> - 1.47.0-6
- Rebuild for libicu soname bump
- Hack /bin back to PATH after MPI module unload
- Resolves: #736890

* Tue Aug 30 2011 Petr Machata <pmachata@redhat.com> - 1.47.0-4
- Drop BR bzip2-libs, which is brought it via bzip2-devel
- Source->Source0
- Drop unnecessary BuildRoot tag
- Update License tag to include all licenses that are found in
  sources.  Python license is at the main package, not to the python
  sub-package, because python22_fixed.h is in -devel.
  - Related: #673839
- Resolves: #225622

* Tue Jul 26 2011 Petr Machata <pmachata@redhat.com> - 1.47.0-3
- Package examples
- Resolves: #722844

* Fri Jul 22 2011 Petr Machata <pmachata@redhat.com> - 1.47.0-2
- Convert two throws in boost/numeric/conversion to
  boost::throw_exception to allow compilation with -fno-exception
- Resolves: #724015

* Thu Jul 14 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.47.0-1
- Upgrade to Boost-1.47.0, adding three new header-only components
  (Geometry, Phoenix, Ratio) and a new library (Chrono).

* Sat Jun 18 2011 Peter Robinson <pbrobinson@gmail.com> - 1.46.1-4
- Fix compile on ARM platforms

* Mon Apr  4 2011 Petr Machata <pmachata@redhat.com> - 1.46.1-3
- Yet another way to pass -DBOOST_LIB_INSTALL_DIR to cmake.  Passing
  via CMAKE_CXX_FLAGS for some reason breaks when rpm re-quotes the
  expression as a result of %%{optflags} expansion.
- Related: #667294

* Wed Mar 30 2011 Deji Akingunola <dakingun@gmail.com> - 1.46.1-2
- Rebuild for mpich2 soname bump

* Sun Mar 13 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.46.1-1
- Merged the latest changes from the bug-fix release of Boost-1.46

* Mon Mar 07 2011 Caolán McNamara <caolanm@redhat.com> - 1.46.0-0.5
- rebuild for icu 4.6

* Thu Feb 24 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.46.0-0.4
- Merged the latest changes from the now final release of Boost-1.46

* Tue Feb  8 2011 Petr Machata <pmachata@redhat.com> - 1.46.0-0.3.beta1
- spirit.patch: Fix a problem in using boost::spirit with utf-8
  strings.  Thanks to Hicham HAOUARI for digging up the fix.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46.0-0.2.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Petr Machata <pmachata@redhat.com> - 1.46.0-0.1.beta1
- Package 1.46.0-beta1
- Reintroduce the soname patch
- unordered-cctor.patch: Add copy constructors and assignment
  operators when using rvalue references
- signals-erase.patch: Pass const_iterator to map::erase to avoid
  ambigous overload vs. templatized value_type ctor
- Related: #656410

* Mon Jan 10 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.44.0-7
- Integrated Petr's work to fix missing Boost.Filesystem V3 issue
- Resolves: #667740

* Thu Jan  6 2011 Petr Machata <pmachata@redhat.com> - 1.44.0-6
- Don't override CXXFLAGS with -DBOOST_IOSTREAMS_USE_DEPRECATED
- Resolves: #667294

* Mon Jan  3 2011 Petr Machata <pmachata@redhat.com> - 1.44.0-5
- Add boost-random DSOs
- Resolves: #665679

* Wed Dec  8 2010 Petr Machata <pmachata@redhat.com> - 1.44.0-4
- Build with support for iostreams deprecated functions
- Resolves: #654480

* Fri Dec  3 2010 Tom "spot" Callaway <spot@fedoraproject.org> - 1.44.0-3
- also package build-system.jam in boost-build

* Tue Nov 30 2010 Tom "spot" Callaway <spot@fedoraproject.org> - 1.44.0-2
- add boost-build, boost-jam subpackages

* Sat Oct 23 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.44.0-1.1
- Rebuild.

* Sat Aug 21 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.44.0-1
- Split the CMake-buildable tar-ball into pristine upstream tar-ball
  and CMake framework patch

* Mon Aug 16 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.44.0-0.6
- Merged the latest changes from the now final release of Boost-1.44

* Fri Aug  6 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.44.0-0.5
- Patched header file in boost/random/detail. Resolves: #621631

* Sat Jul 31 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.44.0-0.4
- Added missing header files in boost/random/detail. Resolves: #619869

* Tue Jul 27 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.44.0-0.3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 27 2010 Benjamin Kosnik <bkoz@redhat.com> - 1.44.0-0.2
- Rebuild.

* Fri Jul 23 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.44.0-0.1
- Upstream update: Boost-1.44 with CMake enabled
- Resolves: #607615

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.41.0-13
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jun  4 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-12
- Turn on mpich2 on s390.  Add arm to the list of arches that openmpi
  doesn't support.

* Fri Jun  4 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-12
- Don't distribute cmake support files.
- Related: #597020

* Wed Jun  2 2010 Dan Horák <dan[at]danny.cz> - 1.41.0-11
- don't build with mpich2/openmpi on s390/s390x

* Mon May 10 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-10
- Add an upstream patch that fixes computation of CRC in zlib streams.
- Resolves: #590205

* Wed May 05 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.41.0-9
- -devel: own %%{_datadir}/cmake/%%{name}/
- -devel: Requires: cmake (for %%{_datadir}/cmake ownership)

* Fri Apr 02 2010 Caolán McNamara <caolanm@redhat.com> - 1.41.0-8
- rebuild for icu

* Mon Feb 22 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-7
- Add a patch for serialization of shared pointers to non polymorphic
  types

* Tue Feb  2 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-6
- More subpackage interdependency adjustments
  - boost doesn't bring in the MPI stuff.  Instead, $MPI-devel does.
    It needs to, so that the symbolic links don't dangle.
  - boost-graph-$MPI depends on boost-$MPI so that boost-mpich2
    doesn't satisfy the SONAME dependency of boost-graph-openmpi.
- Resolves: #559009

* Mon Feb  1 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.41.0-5
- Various fixes on the specification
- Resolves: #559009

* Fri Jan 29 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-5
- Introduce support for both OpenMPI and MPICH2
- Resolves: #559009

* Mon Jan 25 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-4
- Add a patch to build mapnik
- Resolves: #558383

* Tue Jan 19 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-3
- Generalize the soname selection

* Mon Jan 18 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.41.0-2.2
- Further split the Boost.MPI sub-package into boost-mpi and
  boost-mpi-python
- Changed the description of Boost.MPI according to the actual
  dependency (MPICH2 rather than OpenMPI)
- Added a few details on the generation of the mpi.so library

* Thu Jan 14 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-2
- Replace a boost-math subpackage with a stub
- Drop _cmake_lib_suffix and CMAKE_INSTALL_PREFIX magic, the rpm macro
  does that for us
- Drop LICENSE from the umbrella package
- Drop obsolete Obsoletes: boost-python and boost-doc <= 1.30.2

* Tue Jan 12 2010 Benjamin Kosnik <bkoz@redhat.com> - 1.41.0-1
- Don't package generated debug libs, even with 
  (-DCMAKE_BUILD_TYPE=RelWithDebInfo | Release).
- Update and include boost-cmake-soname.patch.
- Uncomment ctest.
- Fix up --with tests to run tests.

* Sat Dec 19 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.41.0-0.7
- Switched off the delivery into a versioned sub-directory

* Thu Dec 17 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.41.0-0.6
- Boost-CMake upstream integration

* Wed Dec 16 2009 Benjamin Kosnik <bkoz@redhat.com> - 1.41.0-0.5
- Rebase to 1.41.0
- Set build type to RelWithDebInfo
- Resolves: #533922

* Mon Nov 16 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.40.0-1
- Add support for the Boost.MPI sub-package
- Build with CMake (https://svn.boost.org/trac/boost/wiki/CMake)
- Resolves: #529563

* Mon Nov 16 2009 Petr Machata <pmachata@redhat.com> - 1.39.0-11
- Move comment in Patch13 out of line

* Mon Nov 16 2009 Petr Machata <pmachata@redhat.com> - 1.39.0-10
- translate_exception.hpp misses a include
- Related: #537612

* Thu Oct 15 2009 Petr Machata <pmachata@redhat.com> - 1.39.0-9
- Package index.html in the -doc subpackage
- Resolves: #529030

* Wed Oct 14 2009 Petr Machata <pmachata@redhat.com> - 1.39.0-8
- Several fixes to support PySide
- Resolves: #520087
- GCC 4.4 name resolution fixes for GIL
- Resolves: #526834

* Sun Oct 11 2009 Jitesh Shah <jiteshs@marvell.com> 1.39.0-7
- Disable long double support for ARM

* Tue Sep 08 2009 Karsten Hopp <karsten@redhat.com> 1.39.0-6
- bump release and rebuild as the package was linked with an old libicu
  during the mass rebuild on s390x

* Wed Aug 26 2009 Tomas Mraz <tmraz@redhat.com> - 1.39.0-5
- Make it to be usable with openssl-1.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.39.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  2 2009 Petr Machata <pmachata@redhat.com> - 1.39.0-3
- Drop file list for main "boost" package, which was inadvertently left in.
- Add thread sub-package to capture omitted boost_thread.
- Add upstream patch to make boost_filesystem compatible with C++0x.
- Resolves: #496188
- Resolves: #509250

* Mon May 11 2009 Benjamin Kosnik <bkoz@redhat.com> - 1.39.0-2
- Apply patch from Caolan McNamara
- Resolves: #500030 function_template bug is back...

* Thu May 07 2009 Benjamin Kosnik <bkoz@redhat.com> - 1.39.0-1
- Update release.

* Wed May 06 2009 Benjamin Kosnik <bkoz@redhat.com> - 1.39.0-0.3
- Fixes for rpmlint.

* Wed May 06 2009 Petr Machata <pmachata@redhat.com> - 1.39.0-0.2
- Split up boost package to sub-packages per library
- Resolves: #496188

* Wed May 06 2009 Benjamin Kosnik <bkoz@redhat.com> - 1.39.0-0.1
- Rebase to 1.39.0.
- Add --with docs_generated.
- #225622: Substitute optflags at prep time instead of RPM_OPT_FLAGS.

* Mon May 04 2009 Benjamin Kosnik <bkoz@redhat.com> - 1.37.0-7
- Rebuild for libicu bump.

* Mon Mar 23 2009 Petr Machata <pmachata@redhat.com> - 1.37.0-6
- Apply a SMP patch from Stefan Ring
- Apply a workaround for "cannot appear in a constant-expression" in
  dynamic_bitset library.
- Resolves: #491537

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 12 2009 Petr Machata <pmachata@redhat.com> - 1.37.0-3
- Apply a unneccessary_iostreams patch from Caolan McNamara
- Fix soname patch so that it applies with fuzz=0.  Use fuzz=0 option
  in spec file just like ordinary patches do.
- Resolves: #479409

* Fri Dec 19 2008 Petr Machata <pmachata@redhat.com> - 1.37.0-2
- Apply a function_template patch from Caolan McNamara
- Resolves: #477131

* Tue Dec 16 2008 Benjamin Kosnik <bkoz@redhat.com> - 1.37.0-1
- Fix rpmlint rpath errors.
- Fix rpmlint warnings on tabs and spaces.
- Bump SONAME to 4

* Mon Nov 17 2008 Benjamin Kosnik <bkoz@redhat.com> - 1.37.0-0.1
- Rebase to 1.37.0.

* Tue Oct 21 2008 Benjamin Kosnik <bkoz@redhat.com> - 1.36.0-1
- Rebase to 1.36.0.

* Mon Oct  6 2008 Petr Machata <pmachata@redhat.com> - 1.34.1-17
- Fix gcc43 patch to apply cleanly under --fuzz=0
- Resolves: #465003

* Mon Aug 11 2008 Petr Machata <pmachata@redhat.com> - 1.36.0-0.1.beta1
- Rebase to 1.36.0.beta1
  - Drop boost-regex.patch and portions of boost-gcc43.patch, port the rest
  - Automate SONAME tracking and bump SONAME to 4
  - Adjust boost-configure.patch to include threading=single,multi explicitly

* Thu Jun 12 2008 Petr Machata <pmachata@redhat.com> - 1.34.1-16
- Fix "changes meaning of keywords" in boost date_time
- Related: #450718

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.34.1-15
- fix license tag

* Thu Mar 27 2008 Petr Machata <pmachata@redhat.com> - 1.34.1-14
- Change devel-static back to static.
- Related: #225622

* Wed Mar 26 2008 Petr Machata <pmachata@redhat.com> - 1.34.1-13
- Install library doc files
- Revamp %%install phase to speed up overall build time
- Some cleanups per merge review
- Resolves: #437032

* Thu Feb 14 2008 Petr Machata <pmachata@redhat.com> - 1.34.1-12
- Fix "changes meaning of keywords" in boost python
- Resolves: #432694

* Wed Feb 13 2008 Petr Machata <pmachata@redhat.com> - 1.34.1-11
- Fix "changes meaning of special_values_parser" in boost date_time
- Resolves: #432433

* Wed Feb  6 2008 Petr Machata <pmachata@redhat.com> - 1.34.1-10
- Fixes for GCC 4.3
- Resolves: #431609

* Mon Jan 14 2008 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-7
- Fixes for boost.regex (rev 42674).

* Wed Sep 19 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-5
- (#283771: Linking against boost libraries fails).

* Tue Aug 21 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-4
- Rebuild.

* Wed Aug 08 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-3
- Rebuild for icu 3.8 bump.

* Thu Aug 02 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-2
- SONAME to 3.

* Tue Jul 31 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-1
- Update to boost_1_34_1.
- Source via http.
- Philipp Thomas <pth.suse.de> fix for RPM_OPT_FLAGS
- Philipp Thomas <pth.suse.de> fix for .so sym links.
- (#225622) Patrice Dumas review comments.

* Tue Jun 26 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1.rc1-0.1
- Update to boost_1_34_1_RC1.

* Mon Apr 02 2007 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-13
- (#225622: Merge Review: boost)
  Change static to devel-static.

* Mon Mar 26 2007 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-12
- (#233523: libboost_python needs rebuild against python 2.5)
  Use patch.

* Mon Mar 26 2007 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-11
- (#225622: Merge Review: boost)
  Source to http.
  BuildRoot to preferred value.
  PreReq to post/postun -p
  Clarified BSL as GPL-Compatible, Free Software License.
  Remove Obsoletes.
  Add Provides boost-python.
  Remove mkdir -p $RPM_BUILD_ROOT%%{_docdir}
  Added periods for decription text.
  Fix Group field.
  Remove doc Requires boost.
  Preserve timestamps on install.
  Use %%defattr(-, root, root, -)
  Added static package for .a libs.
  Install static libs with 0644 permissions.
  Use %%doc for doc files.

* Mon Jan 22 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.0-0.5
- Update to boost.RC_1_34_0 snapshot as of 2007-01-19.
- Modify build procedures for boost build v2.
- Add *-mt variants for libraries, or at least variants that use
  threads (regex and thread).

* Thu Nov 23 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-10
- (#182414: boost: put tests in %%check section) via Rex Dieter
- Fix EVR with %%{?dist} tag via Gianluca Sforna

* Wed Nov 15 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-9
- (#154784: boost-debuginfo package is empty)

* Tue Nov 14 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-8
- (#205866: Revert scanner.hpp change.)

* Mon Nov 13 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-7
- (#205866: boost::spirit generates warnings with -Wshadow)
- (#205863: serialization lib generates warnings)
- (#204326: boost RPM missing dependencies)
- (#193465: [SIGNAL/BIND] Regressions with GCC 4.1)
- BUILD_FLAGS, add, to see actual compile line.
- REGEX_FLAGS, add, to compile regex with ICU support.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.33.1-6.1
- rebuild

* Tue May 16 2006 Karsten Hopp <karsten@redhat.de> 1.33.1-6
- buildrequire python-devel for Python.h

* Thu Feb 16 2006 Florian La Roche <laroche@redhat.com> - 1.33.1-5
- use the real version number to point to the shared libs

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.33.1-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.33.1-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 05 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-4
- Fix symbolic links.

* Wed Jan 04 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-3
- Update to boost-1.33.1.
- (#176485: Missing BuildRequires)
- (#169271: /usr/lib/libboost*.so.? links missing in package)

* Thu Dec 22 2005 Jesse Keating <jkeating@redhat.com> 1.33.1-2
- rebuilt

* Mon Nov 14 2005 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-1
- Update to boost-1.33.1 beta.
- Run testsuite, gather results.

* Tue Oct 11 2005 Nils Philippsen <nphilipp@redhat.com> 1.33.0-4
- build require bzip2-devel and zlib-devel

* Tue Aug 23 2005 Benjamin Kosnik <bkoz@redhat.com> 1.33.0-3
- Create doc package again.
- Parts of the above by Neal Becker <ndbecker2@gmail.com>.

* Fri Aug 12 2005 Benjamin Kosnik <bkoz@redhat.com> 1.33.0-1
- Update to boost-1.33.0, update SONAME to 2 due to ABI changes.
- Simplified PYTHON_VERSION by Philipp Thomas <pth@suse.de>

* Tue May 24 2005 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-6
- (#153093: boost warns that gcc 4.0.0 is an unknown compiler)
- (#152205: development .so symbolic links should be in -devel subpackage)
- (#154783: linker .so symbolic links missing from boost-devel package)

* Fri Mar 18 2005 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-5
- Revert boost-base.patch to old behavior.
- Use SONAMEVERSION instead of dllversion.

* Wed Mar 16 2005 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-4
- (#142612: Compiling Boost 1.32.0 Failed in RHEL 3.0 on Itanium2)
- (#150069: libboost_python.so is missing)
- (#141617: bad patch boost-base.patch)
- (#122817: libboost_*.so symbolic links missing)
- Re-add boost-thread.patch.
- Change boost-base.patch to show thread tags.
- Change boost-gcc-tools.patch to use SOTAG, compile with dllversion.
- Add symbolic links to files.
- Sanity check can compile with gcc-3.3.x, gcc-3.4.2, gcc-4.0.x., gcc-4.1.x.

* Thu Dec 02 2004 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-3
- (#122817: libboost_*.so symbolic links missing)
- (#141574: half of the package is missing)
- (#141617: bad patch boost-base.patch)

* Wed Dec 01 2004 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-2
- Remove bogus Obsoletes.

* Mon Nov 29 2004 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-1
- Update to 1.32.0

* Wed Sep 22 2004 Than Ngo <than@redhat.com> 1.31.0-9
- cleanup specfile
- fix multiarch problem

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 05 2004 Warren Togami <wtogami@redhat.com> 1.31.0-7
- missing Obsoletes boost-python

* Mon May 03 2004 Benjamin Kosnik <bkoz@redhat.com>
- (#121630: gcc34 patch needed)

* Wed Apr 21 2004 Warren Togami <wtogami@redhat.com>
- #121415 FC2 BLOCKER: Obsoletes boost-python-devel, boost-doc
- other cleanups

* Tue Mar 30 2004 Benjamin Kosnik <bkoz@redhat.com>
- Remove bjam dependency. (via Graydon).
- Fix installed library names.
- Fix SONAMEs in shared libraries.
- Fix installed header location.
- Fix installed permissions.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 09 2004 Benjamin Kosnik <bkoz@redhat.com> 1.31.0-2
- Update to boost-1.31.0

* Thu Jan 22 2004 Benjamin Kosnik <bkoz@redhat.com> 1.31.0-1
- Update to boost-1.31.0.rc2
- (#109307:  Compile Failure with boost libraries)
- (#104831:  Compile errors in apps using Boost.Python...)
- Unify into boost, boost-devel rpms.
- Simplify installation using bjam and prefix install.

* Tue Sep 09 2003 Nalin Dahyabhai <nalin@redhat.com> 1.30.2-2
- require boost-devel instead of devel in subpackages which require boost-devel
- remove stray Prefix: tag

* Mon Sep 08 2003 Benjamin Kosnik <bkoz@redhat.com> 1.30.2-1
- change license to Freely distributable
- verify installation of libboost_thread
- more boost-devel removals
- deal with lack of _REENTRANT on ia64/s390
- (#99458) rpm -e fixed via explict dir additions
- (#103293) update to 1.30.2

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 13 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- remove packager, change to new Group:

* Tue May 06 2003 Tim Powers <timp@redhat.com> 1.30.0-3
- add deffattr's so we don't have unknown users owning files
