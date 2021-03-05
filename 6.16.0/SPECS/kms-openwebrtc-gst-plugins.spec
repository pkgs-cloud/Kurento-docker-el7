%define		commit 6a0d22d

%global		_prefix /opt/kms

Name:           kms-openwebrtc-gst-plugins
Version:        0.10.0
Release:        1%{?dist}
Summary:        OpenWebRTC specific GStreamer plugins

Group:          System Environment/Libraries
License:        LGPLv2 and MPLv1.1
URL:            https://github.com/Kurento/openwebrtc-gst-plugins
#Source0:        %{kms_name}-%{kms_version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Requires:       kms-libusrsctp
BuildRequires:  kms-libusrsctp-devel
BuildRequires:	glib2-devel >= 2.44
BuildRequires:  kms-gstreamer1-devel
BuildRequires:	kms-gstreamer1-plugins-base-devel
#BuildRequires:  gstreamer1-devel >= 0.11.91
#BuildRequires:	gstreamer1-plugins-base-devel >= 0.11.91
BuildRequires:	gupnp-igd-devel >= 0.1.2
#Provides:       %{kms_name}

%description
OpenWebRTC specific GStreamer plugins


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
#Requires:	glib2-devel >= 2.44
Requires:	pkgconfig
Provides:	%{name}-devel


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -c -n %{name}-%{version}-%{commit} -T -D
if [ ! -d .git ]; then
    git clone https://github.com/Kurento/openwebrtc-gst-plugins.git .
    git checkout %{commit}
fi

%check
#make check


%build
export XDG_DATA_DIRS=%{_datadir}
export LD_RUN_PATH=%{_libdir}
export LD_LIBRARY_PATH=%{_libdir}
export CPATH=%{_includedir}
export CPPFLAGS=-I%{_includedir}
export LDFLAGS=-L%{_libdir}

./autogen.sh --prefix=%{_prefix}

%configure --disable-static
#./configure --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu --program-prefix= --disable-dependency-tracking --prefix=/usr \
#    --exec-prefix=/usr --bindir=/usr/bin --sbindir=/usr/sbin --sysconfdir=/etc --datadir=/usr/share --includedir=/usr/include --libdir=/usr/lib64 \
#    --libexecdir=/usr/libexec --localstatedir=/var --sharedstatedir=/var/lib --mandir=/usr/share/man --infodir=/usr/share/info



#make %{?_smp_mflags}
make all


%install
export XDG_DATA_DIRS=%{_datadir}
export LD_RUN_PATH=%{_libdir}
export LD_LIBRARY_PATH=%{_libdir}
export CPATH=%{_includedir}
export CPPFLAGS=-I%{_includedir}
export LDFLAGS=-L%{_libdir}

rm -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%{_libdir}/gstreamer-1.5/*.so
%{_libdir}/*.so.*


%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
#%{_libdir}/girepository-1.0/*
#%{_datadir}/gir-1.0/*

%changelog
