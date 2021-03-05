%define commit b33143e

%define majorminor  1.5
%define gstreamer   kms-gstreamer1
%define gst_minver  1.8.1
%define gst_majorminor  1.0

%global _prefix /opt/kms

Name: 		%{gstreamer}-libav
Version: 	1.8.1
Release:	1%{?dist}
Summary: 	GStreamer Streaming-media framework plug-in using libav (FFmpeg).
Group: 		Libraries/Multimedia
License: 	LGPL
URL:		http://gstreamer.net/
Vendor:		GStreamer Backpackers Team <package@gstreamer.net>
#Source:		http://gstreamer.freedesktop.org/src/gst-ffmpeg/gst-ffmpeg/gst-libav-%{version}.tar.xz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:  	%{gstreamer} >= 1.0.0
BuildRequires: 	%{gstreamer}-devel >= 1.0.0
BuildRequires: 	%{gstreamer}-plugins-base-devel >= 1.0.0
BuildRequires:	yasm

%description
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related. Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

This plugin contains the libav (formerly FFmpeg) codecs, containing codecs for most popular
multimedia formats.

%prep
%setup -c -n %{name}-%{version}-%{commit} -T -D
if [ ! -d .git ]; then
    git clone https://github.com/Kurento/gst-libav.git .
    git checkout %{commit}
fi

%build
./autogen.sh --prefix=%{_prefix}
%configure

export XDG_DATA_DIRS=%{_datadir}
export LD_RUN_PATH=%{_libdir}
export LD_LIBRARY_PATH=%{_libdir}

make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
#%doc AUTHORS COPYING README gst-libav.doap
%{_libdir}/gstreamer-%{majorminor}/libgstlibav.so
#%{_datadir}/gtk-doc/html/gst-libav-plugins-%{gst_majorminor}/*

%changelog
* Fri Aug 03 2012 Christian Schaller <uraeus@linuxrising.org>
- update for 1.0 release and libav rename

* Fri Dec 15 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- clean up
- add doap file

* Sat Feb 14 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- Clean up spec file

* Wed Jan 21 2004 Christian Schaller <Uraeus@gnome.org>
- First version of spec
