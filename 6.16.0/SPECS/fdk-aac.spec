%global commit0 a0bd8aa3b6339082fbe9d830264839fa50c0a4b7
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           fdk-aac
Version:        0.1.5
Release:        0.1%{?commit0:.git%{shortcommit0}}%{?dist}
Summary:        Fraunhofer FDK AAC Codec Library

License:        FDK-AAC
URL:            https://github.com/mstorsjo/fdk-aac
Source0:        https://github.com/mstorsjo/%{name}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  libtool


%description
The Fraunhofer FDK AAC Codec Library ("FDK AAC Codec") is software that
implements the MPEG Advanced Audio Coding ("AAC") encoding and decoding
scheme for digital audio.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.



%prep
%autosetup -n %{name}-%{?commit0}%{?!commit0:%{version}}
autoreconf -vif


%build
%configure \
  --disable-silent-rules \
  --disable-static

%make_build


%install
%make_install INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc ChangeLog
%license NOTICE
%{_libdir}/*.so.*

%files devel
%doc documentation/*.pdf
%dir %{_includedir}/fdk-aac
%{_includedir}/fdk-aac/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Wed Sep 07 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.1.5-0.1.gita0bd8aa
- Update to github snapshot
- Spec file clean-up

* Fri Nov 06 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.1.4-1
- Update to 1.4

* Sun Jan 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.1.3-1
- Update to 1.3.0

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.1.2-1
- Update to 0.1.2

* Thu Mar 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.1.1-1
- Initial spec

