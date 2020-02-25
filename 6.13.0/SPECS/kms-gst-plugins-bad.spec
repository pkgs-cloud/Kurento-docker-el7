%define commit 17d48dd

%define majorminor   1.5
%define gstreamer    kms-gstreamer1

%define gst_minver   0.10.30
%define gstpb_minver 0.10.30

%global _prefix /opt/kms

Summary: GStreamer streaming media framework "bad" plug-ins
Name: %{gstreamer}-plugins-bad
Version: 1.8.1
Release: 4%{?dist}
# The freeze and nfs plugins are LGPLv2 (only)
License: LGPLv2+ and LGPLv2
Group: Applications/Multimedia
URL: http://gstreamer.freedesktop.org/
#Source: http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.xz
#Source: gst-plugins-bad-%{kms_version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: %{gstreamer} >= %{gst_minver}
Requires: libde265

#Conflicts:	gstreamer1-plugins-bad

BuildRequires: %{gstreamer}-devel >= %{gst_minver}
BuildRequires: %{gstreamer}-plugins-base-devel >= %{gstpb_minver}

BuildRequires: check
BuildRequires: gettext-devel
BuildRequires: libXt-devel
BuildRequires: gtk-doc

BuildRequires: bzip2-devel
#BuildRequires: exempi-devel
BuildRequires: ladspa-devel
BuildRequires: libass-devel
BuildRequires: bluez-libs-devel
#%ifnarch s390 s390x
#BuildRequires: libdc1394-devel
#%endif
BuildRequires: libde265-devel
#BuildRequires: libdvdnav-devel
BuildRequires: libexif-devel
#BuildRequires: libiptcdata-devel
#BuildRequires: libkate-devel
BuildRequires: libmodplug-devel
BuildRequires: libmpcdec-devel
#BuildRequires: libofa-devel
#BuildRequires: librsvg2-devel
BuildRequires: libsndfile-devel
#BuildRequires: libtimidity-devel
BuildRequires: libvpx-devel
#BuildRequires: mesa-libGLU-devel
BuildRequires: openssl-devel
BuildRequires: orc-devel
BuildRequires: schroedinger-devel
#BuildRequires: SDL-devel
#BuildRequires: slv2-devel
BuildRequires: soundtouch-devel
BuildRequires: wavpack-devel
#BuildRequires: wildmidi-devel
#BuildRequires: zbar-devel
#BuildRequires: libdca-devel
BuildRequires: faad2-devel
BuildRequires: xvidcore-devel
#BuildRequires: libmms-devel
#BuildRequires: mjpegtools-devel
#BuildRequires: twolame-devel
#BuildRequires: libmimic-devel
BuildRequires: kms-libsrtp-devel
#BuildRequires: libgudev1-devel
#BuildRequires: libusb-devel
BuildRequires: openh264-devel
BuildRequires: vo-aacenc-devel
BuildRequires: vo-amrwbenc-devel
BuildRequires: opus-devel >= 1.1.0
BuildRequires: x265-devel
BuildRequires: OpenEXR-devel

BuildRequires: openjpeg-devel
BuildRequires: kms-openjpeg2-devel = 2.1.0
BuildRequires: openal-soft-devel gsm-devel libxml2-devel librtmp-devel
BuildRequires: sbc-devel libbs2b-devel libwebp-devel zvbi-devel
BuildRequires: opencv-devel libvdpau-devel

#Obsoletes: gstreamer-plugins-flumpegdemux < 0.10.15-9
#Provides: gstreamer-plugins-flumpegdemux = %{version}-%{release}
#Obsoletes: gstreamer-plugins-schroedinger < 1.0.9
#Provides: gstreamer-plugins-schroedinger = %{version}-%{release}

#Provides: gstreamer-plugins-farsight = 0.12.12-1
#Obsoletes: gstreamer-plugins-farsight < 0.12.12


%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains plug-ins that aren't tested
well enough, or the code is not of good enough quality.


#%package free
#Summary: Extra GStreamer "bad" plugins (Plugins shipped by default in Fedora)
#Group: Applications/Multimedia
#Requires: %{name} = %{version}-%{release}

#%description free
#GStreamer is a streaming media framework, based on graphs of elements which
#operate on media data.

#This package contains plug-ins that aren't tested
#well enough, or the code is not of good enough quality.


#%package extras
#Summary: Extra GStreamer "bad" plugins (less often used "bad" plugins)
#Group: Applications/Multimedia
#Requires: %{name} = %{version}-%{release}
#Obsoletes: gstreamer-plugins-bad-extras < %{version}-%{release}
#Provides: gstreamer-plugins-bad-extras = %{version}-%{release}

#%description extras
#GStreamer is a streaming media framework, based on graphs of elements which
#operate on media data.

#gstreamer-plugins-bad contains plug-ins that aren't
#tested well enough, or the code is not of good enough quality.

#This package (gstreamer-plugins-bad-extras) contains extra "bad" plugins for
#sources, sinks (jack) and effects (pitch) which are not used
#very much and require additional libraries to be installed.


%package devel
Summary: Development files for the GStreamer media framework "bad" plug-ins
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{gstreamer}-plugins-base-devel
#Obsoletes: gstreamer-plugins-bad-devel < %{version}-%{release}
Provides: %{gstreamer}-plugins-bad-devel = %{version}-%{release}

#Conflicts: gstreamer1-plugins-bad-devel

%description devel
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development files for the plug-ins that
aren't tested well enough, or the code is not of good enough quality.


#%package devel-docs
#Summary: Development documentation for the GStreamer "bad" plug-ins
#Group: Development/Libraries
#Requires: %{name}-devel = %{version}-%{release}
#Obsoletes: gstreamer-plugins-bad-devel-docs < %{version}-%{release}
#Provides: gstreamer-plugins-bad-devel-docs = %{version}-%{release}

#%description devel-docs
#GStreamer is a streaming media framework, based on graphs of elements which
#operate on media data.

#This package contains the development documentation for the plug-ins that
#aren't tested well enough, or the code is not of good enough quality.


%prep
%setup -c -n %{name}-%{version}-%{commit} -T -D
if [ ! -d .git ]; then
    git clone https://github.com/Kurento/gst-plugins-bad.git .
    git checkout %{commit}
fi

%build
./autogen.sh --prefix=%{_prefix}
%configure \
    --with-package-name="Kurento gstreamer-plugins-bad package" \
    --with-package-origin="http://gstreamer.freedesktop.org" \
    --enable-debug --disable-static --enable-experimental
# --enable-gtk-doc

export XDG_DATA_DIRS=%{_datadir}
export LD_RUN_PATH=%{_libdir}
export LD_LIBRARY_PATH=%{_libdir}
export CPATH=%{_includedir}
export CPPFLAGS=-I%{_includedir}
export LDFLAGS=-L%{_libdir}

# %{__make} %{?_smp_mflags}
make ERROR_CFLAGS='' ERROR_CXXFLAGS=''

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%find_lang gst-plugins-bad-%{majorminor}

# Clean out files that should not be part of the rpm.
%{__rm} -f %{buildroot}%{_libdir}/gstreamer-%{majorminor}/*.la
%{__rm} -f %{buildroot}%{_libdir}/*.la


%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f gst-plugins-bad-%{majorminor}.lang
# Plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstdvdspu.so

# Plugins with external dependencies
#%{_libdir}/gstreamer-%{majorminor}/libgstdtsdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstfaad.so
#%{_libdir}/gstreamer-%{majorminor}/libgstmms.so
#%{_libdir}/gstreamer-%{majorminor}/libgstmpeg2enc.so
#%{_libdir}/gstreamer-%{majorminor}/libgstmplex.so
#%{_libdir}/gstreamer-%{majorminor}/libgstfaac.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegpsmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstdecklink.so
%{_libdir}/gstreamer-%{majorminor}/libgstopenal.so
%{_libdir}/gstreamer-%{majorminor}/libgstopenjpeg.so
#%{_libdir}/gstreamer-%{majorminor}/libgstwaylandsink.so
#%{_libdir}/gstreamer-%{majorminor}/libgstwildmidi.so

%{_libdir}/gstreamer-%{majorminor}/libgstbluez.so
%{_libdir}/gstreamer-%{majorminor}/libgstcompositor.so
%{_libdir}/gstreamer-%{majorminor}/libgstdtls.so
%{_libdir}/gstreamer-%{majorminor}/libgstgsm.so
%{_libdir}/gstreamer-%{majorminor}/libgstnetsim.so
%{_libdir}/gstreamer-%{majorminor}/libgstopusparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtponvif.so
%{_libdir}/gstreamer-%{majorminor}/libgstvcdsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstvdpau.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoframe_audiolevel.so
%{_libdir}/gstreamer-%{majorminor}/libgstx265.so
%{_libdir}/gstreamer-%{majorminor}/libgstsrtp.so
%{_libdir}/gstreamer-%{majorminor}/libgstopenh264.so
%{_libdir}/gstreamer-%{majorminor}/libgstvoamrwbenc.so

%{_libdir}/gstreamer-%{majorminor}/libgstopencv.so
%{_libdir}/gstreamer-%{majorminor}/libgstopenexr.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtmp.so

#%{_libdir}/gstreamer-%{majorminor}/libgstflite.so
%{_libdir}/gstreamer-%{majorminor}/libgstsbc.so
#%{_libdir}/gstreamer-%{majorminor}/libgstuvch264.so
%{_libdir}/gstreamer-%{majorminor}/libgstbs2b.so

%{_libdir}/gstreamer-%{majorminor}/libgstteletextdec.so

%{_datadir}/gstreamer-%{majorminor}/presets/*

#%files free
#%defattr(-,root,root,-)
#%doc AUTHORS COPYING README REQUIREMENTS
#%{_datadir}/gstreamer-%{majorminor}
#%{_libdir}/libgstphotography-%{majorminor}.so.*
#%{_libdir}/libgstcodecparsers-%{majorminor}.so.*
#%{_libdir}/libgstinsertbin-%{majorminor}.so.*

# Plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstadpcmdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstadpcmenc.so
%{_libdir}/gstreamer-%{majorminor}/libgstautoconvert.so
%{_libdir}/gstreamer-%{majorminor}/libgstbayer.so
%{_libdir}/gstreamer-%{majorminor}/libgstdataurisrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstjpegformat.so
#%{_libdir}/gstreamer-%{majorminor}/libgstliveadder.so
%{_libdir}/gstreamer-%{majorminor}/libgstpcapparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstpnm.so
%{_libdir}/gstreamer-%{majorminor}/libgstsegmentclip.so
%{_libdir}/gstreamer-%{majorminor}/libgstrawparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstshm.so
%{_libdir}/gstreamer-%{majorminor}/libgstsdpelem.so
%{_libdir}/gstreamer-%{majorminor}/libgstsmooth.so
%{_libdir}/gstreamer-%{majorminor}/libgstspeed.so
%{_libdir}/gstreamer-%{majorminor}/libgstcamerabin2.so
#%{_libdir}/gstreamer-%{majorminor}/libgstcurl.so
%{_libdir}/gstreamer-%{majorminor}/libgstgdp.so
%{_libdir}/gstreamer-%{majorminor}/libgstaccurip.so
%{_libdir}/gstreamer-%{majorminor}/libgstfieldanalysis.so
%{_libdir}/gstreamer-%{majorminor}/libgstmxf.so
%{_libdir}/gstreamer-%{majorminor}/libgstsubenc.so
%{_libdir}/gstreamer-%{majorminor}/libgstaiff.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiofxbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstdashdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstfbdevsink.so
%{_libdir}/gstreamer-%{majorminor}/libgstfreeverb.so
%{_libdir}/gstreamer-%{majorminor}/libgstivtc.so
%{_libdir}/gstreamer-%{majorminor}/libgstmidi.so
%{_libdir}/gstreamer-%{majorminor}/libgstrfbsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstsmoothstreaming.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideofiltersbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstyadif.so
%{_libdir}/gstreamer-%{majorminor}/libgstsiren.so

%{_libdir}/gstreamer-%{majorminor}/libgstdvbsuboverlay.so
%{_libdir}/gstreamer-%{majorminor}/libgsthls.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoparsersbad.so
%{_libdir}/gstreamer-%{majorminor}/libgsty4mdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiovisualizers.so
%{_libdir}/gstreamer-%{majorminor}/libgstinter.so
%{_libdir}/gstreamer-%{majorminor}/libgstremovesilence.so
%{_libdir}/gstreamer-%{majorminor}/libgstasfmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstcoloreffects.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvb.so
%{_libdir}/gstreamer-%{majorminor}/libgstfestival.so
%{_libdir}/gstreamer-%{majorminor}/libgstgaudieffects.so
%{_libdir}/gstreamer-%{majorminor}/libgstgeometrictransform.so
%{_libdir}/gstreamer-%{majorminor}/libgstid3tag.so
%{_libdir}/gstreamer-%{majorminor}/libgstinterlace.so
#%{_libdir}/gstreamer-%{majorminor}/libgstmimic.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegpsdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegtsdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegtsmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstsoundtouch.so



# System (Linux) specific plugins
# %{_libdir}/gstreamer-%{majorminor}/libgstdvb.so
# %{_libdir}/gstreamer-%{majorminor}/libgstvcdsrc.so

# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstassrender.so
%{_libdir}/gstreamer-%{majorminor}/libgstbz2.so
#%{_libdir}/gstreamer-%{majorminor}/libgstopus.so
#%ifnarch s390 s390x
#%{_libdir}/gstreamer-%{majorminor}/libgstdc1394.so
#%endif
# %{_libdir}/gstreamer-%{majorminor}/libgstgsm.so
#%{_libdir}/gstreamer-%{majorminor}/libgstkate.so
%{_libdir}/gstreamer-%{majorminor}/libgstladspa.so
%{_libdir}/gstreamer-%{majorminor}/libgstlibde265.so
%{_libdir}/gstreamer-%{majorminor}/libgstmodplug.so
#%{_libdir}/gstreamer-%{majorminor}/libgstofa.so
#%{_libdir}/gstreamer-%{majorminor}/libgstresindvd.so
#%{_libdir}/gstreamer-%{majorminor}/libgstrsvg.so
%{_libdir}/gstreamer-%{majorminor}/libgstschro.so
%{_libdir}/gstreamer-%{majorminor}/libgstfrei0r.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiomixer.so
#%{_libdir}/gstreamer-%{majorminor}/libgstopencv.so
%{_libdir}/gstreamer-%{majorminor}/libgstivfparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstjp2kdecimator.so
%{_libdir}/gstreamer-%{majorminor}/libgstopengl.so
%{_libdir}/gstreamer-%{majorminor}/libgstsndfile.so
%{_libdir}/gstreamer-%{majorminor}/libgststereo.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideosignal.so
%{_libdir}/gstreamer-%{majorminor}/libgstvmnc.so
%{_libdir}/gstreamer-%{majorminor}/libgstwebp.so
%{_libdir}/gstreamer-%{majorminor}/libgstvoaacenc.so
#%{_libdir}/gstreamer-%{majorminor}/libgstspandsp.so

%{_datadir}/gst-plugins-bad/1.5/opencv_haarcascades/fist.xml
%{_datadir}/gst-plugins-bad/1.5/opencv_haarcascades/palm.xml

#%{_libdir}/libgstbasecamerabinsrc-*
#%{_libdir}/libgstmpegts-*
#%{_libdir}/libgsturidownloader*
%{_libdir}/*.so.*

#debugging plugin
%{_libdir}/gstreamer-%{majorminor}/libgstdebugutilsbad.so

#data for plugins
# %{_datadir}/glib-2.0/schemas/org.freedesktop.gstreamer-0.11.default-elements.gschema.xml

#%files extras
#%defattr(-,root,root,-)
# Plugins with external dependencies
# %{_libdir}/gstreamer-%{majorminor}/libgstjack.so
# %{_libdir}/gstreamer-%{majorminor}/libgstsdl.so
# %{_libdir}/gstreamer-%{majorminor}/libgstsoundtouch.so
# %{_libdir}/gstreamer-%{majorminor}/libgsttimidity.so
# %{_libdir}/gstreamer-%{majorminor}/libgstwildmidi.so
# %{_libdir}/gstreamer-%{majorminor}/libgstzbar.so
# %{_libdir}/gstreamer-%{majorminor}/libgstmultifdsink.so

# Linux specific plugins
# %{_libdir}/gstreamer-%{majorminor}/libgstfbdevsink.so

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so

%{_includedir}/gstreamer-%{majorminor}/*


#%{_libdir}/libgst*-%{majorminor}.so*

# pkg-config files
%{_libdir}/pkgconfig/*

%{_libdir}/girepository-1.0/*
%{_datadir}/gir-1.0/*

%{_libdir}/gstreamer-%{majorminor}/include/gst/gl/gstglconfig.h


#%files devel-docs
#%defattr(-,root,root,-)
#%doc %{_datadir}/gtk-doc/html/gst-plugins-bad-plugins-%{majorminor}
#%doc %{_datadir}/gtk-doc/html/gst-plugins-bad-libs-%{majorminor}

%changelog
* Thu May 19 2011 Christian Schaller <christian.schaller@collabora.co.uk>
- Merge in upstread Fedora RPM into git master one

* Wed Sep 15 2010 Hans de Goede <hdegoede@redhat.com> 0.10.20-3
- Rebuild for new wildmidi

* Mon Sep 13 2010 Dan Horák <dan[at]danny.cz> 0.10.20-2
- no Firewire on s390(x)

* Mon Sep 06 2010 Benjamin Otte <otte@redhat.com> 0.10.20-1
- Update to 0.10.20
- Reenable celt

* Fri Aug 06 2010 Benjamin Otte <otte@redhat.com> 0.10.19-6
- Disable NAS now that it's obsolete

* Thu Jun 17 2010 Benjamin Otte <otte@redhat.com> 0.10.19-4
- Move zbar to -extras. It pulls in too many deps and is not really useful.

* Tue Jun 01 2010 Benjamin Otte <otte@redhat.com> 0.10.19-3
- Put back accidentally deleted make command

* Tue Jun  1 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.10.19-2
- Rebuild.

* Mon May 31 2010 Benjamin Otte <otte@redhat.com> 0.10.19-1
- Update to 0.10.19

* Thu Apr 15 2010 Benjamin Otte <otte@redhat.com> 0.10.18-2
- Include cog plugin

* Mon Mar 08 2010 Benjamin Otte <otte@redhat.com> 0.10.18-1
- Update to 0.10.18

* Thu Mar 04 2010 Benjamin Otte <otte@redhat.com> 0.10.17.4-1
- Update pre-release

* Mon Mar 01 2010 Benjamin Otte <otte@redhat.com> 0.10.17.3-2
- Fix Obsoletes and add Provides for extras/devel/docs

* Thu Feb 25 2010 Benjamin Otte <otte@redhat.com> 0.10.17.3-1
- Update to pre-release

* Fri Feb 19 2010 Benjamin Otte <otte@redhat.com> 0.10.17.2-1
- Update to prerelease

* Sun Feb 14 2010 Benjamin Otte <otte@redhat.com> 0.10.17-7
- Fix compilation problems with DSO linking (#565015)

* Thu Feb 04 2010 Bastien Nocera <bnocera@redhat.com> 0.10.17-6
- Obsolete third-party packages, for upgrade purposes

* Tue Feb 02 2010 Bastien Nocera <bnocera@redhat.com> 0.10.17-5
- Another try at obsolete problems with flumpegdemux and
  schroedinger (#560987)

* Mon Feb 01 2010 Bastien Nocera <bnocera@redhat.com> 0.10.17-4
- Add versioned provides for flumpegdemux and schroedinger plugins

* Wed Jan 27 2010 Bastien Nocera <bnocera@redhat.com> 0.10.17-3
- Modify original sources with a script to remove problematic
  elements, and remove those from the filelist

* Fri Dec 04 2009 Bastien Nocera <bnocera@redhat.com> 0.10.17-2
- Add LADSPA plugins

* Tue Nov 17 2009 Bastien Nocera <bnocera@redhat.com> 0.10.17-1
- Update to 0.10.17

* Tue Nov 10 2009 Bastien Nocera <bnocera@redhat.com> 0.10.16-2
- Add schroedinger plugin (#530835)

* Sat Nov 07 2009 Bastien Nocera <bnocera@redhat.com> 0.10.16-1
- First version with -free name, updated to 0.10.16

