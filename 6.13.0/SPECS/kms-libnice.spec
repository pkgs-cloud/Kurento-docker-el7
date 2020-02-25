%define         commit a5b5069

%global		_prefix /opt/kms

Name:           kms-libnice
Version:        0.1.15
Release:        3%{?dist}
Summary:        Kurento GLib ICE implementation

Group:          System Environment/Libraries
License:        LGPLv2 and MPLv1.1
URL:            https://github.com/Kurento/libnice
#Source0:        Kurento-libnice-%{commit}.tar.gz

BuildRequires:	glib2-devel >= 2.44
BuildRequires:  kms-gstreamer1-devel
BuildRequires:	kms-gstreamer1-plugins-base-devel
BuildRequires:  kms-gstreamer1-devel >= 0.11.91
BuildRequires:	kms-gstreamer1-plugins-base-devel >= 0.11.91
BuildRequires:	gupnp-igd-devel >= 0.1.2
BuildRequires:  gtk-doc
BuildRequires:  openssl-devel

%description
%{name} is an implementation of the IETF's draft Interactive Connectivity
Establishment standard (ICE). ICE is useful for applications that want to
establish peer-to-peer UDP data streams. It automates the process of traversing
NATs and provides security against some attacks. Existing standards that use
ICE include the Session Initiation Protocol (SIP) and Jingle, XMPP extension
for audio/video calls.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:	glib2-devel >= 2.44
Requires:	pkgconfig


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -c -n %{name}-%{version}-%{commit} -T -D
if [ ! -d .git ]; then
    git clone https://github.com/Kurento/libnice.git .
    git checkout %{commit}
fi

for p in $(cat debian/patches/series); do
    if ! patch -R -p1 -s -f --dry-run <debian/patches/$p; then
	patch -p1 <debian/patches/$p
    fi
done

%check
#make check


%build
./autogen.sh --disable-static --with-gstreamer-1.5 --prefix=%{_prefix}
#configure --disable-static --with-crypto-library=openssl --with-gstreamer-1.5
%configure --disable-static --with-gstreamer-1.5
#sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
#sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

export XDG_DATA_DIRS=%{_datadir}
export LD_RUN_PATH=%{_libdir}
export LD_LIBRARY_PATH=%{_libdir}

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
#mv $RPM_BUILD_ROOT/usr/lib64/gstreamer-1.0 $RPM_BUILD_ROOT/usr/lib64/gstreamer-1.5


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
#%doc NEWS README COPYING COPYING.LGPL COPYING.MPL
%{_bindir}/*
%{_libdir}/gstreamer-1.5/*.so
%{_libdir}/*.so.*


%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/nice.pc
%{_libdir}/girepository-1.0/*
%{_datadir}/gir-1.0/*

%changelog
