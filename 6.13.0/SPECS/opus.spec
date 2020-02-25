Name:          opus
Version:       1.1.3
Release:       1%{?dist}
Summary:       An audio codec for use in low-delay speech and audio communication

Group:         System Environment/Libraries
License:       BSD
URL:           http://www.opus-codec.org/
Source0:       http://downloads.xiph.org/releases/%{name}/%{name}-%{version}.tar.gz
# This is the final IETF Working Group RFC
Source1:       http://tools.ietf.org/rfc/rfc6716.txt 
BuildRequires: doxygen

%description
The Opus codec is designed for interactive speech and audio transmission over 
the Internet. It is designed by the IETF Codec Working Group and incorporates 
technology from Skype's SILK codec and Xiph.Org's CELT codec.

%package devel
Summary: Development package for opus
Group: Development/Libraries
Requires: libogg-devel
Requires: opus = %{version}-%{release}

%description devel
Files for development with opus.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} .

%build
%configure --enable-custom-modes --disable-static

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

# Remove libtool archives and static libs
find %{buildroot} -type f -name "*.la" -delete
rm -rf %{buildroot}%{_datadir}/doc/opus/html

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/libopus.so.*

%files devel
%doc README doc/html rfc6716.txt
%{_includedir}/opus
%{_libdir}/libopus.so
%{_libdir}/pkgconfig/opus.pc
%{_datadir}/aclocal/opus.m4
%{_datadir}/man/man3/opus_*.3.gz

%changelog
* Mon Jul 18 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.3-1
- Update 1.1.3 GA

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.2-1
- Update 1.1.2 GA

* Thu Nov 26 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.1-1
- Update 1.1.1 GA

* Wed Oct 28 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.1-0.4.rc
- Update to 1.1.1 RC (further ARM optimisations)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-0.3.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb  3 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.1-0.2.beta
- Use %%license

* Wed Oct 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.1-0.1.beta
- Update to 1.1.1 beta (SSE, ARM, MIPS optimisations)

* Sun Oct  5 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-5
- Install html docs in devel package

* Fri Oct  3 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-4
- Build developer docs

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Dec  6 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-1
- 1.1 release

* Tue Dec  3 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-0.3rc3
- Update to 1.1-rc3

* Thu Nov 28 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-0.2rc2
- Update to 1.1-rc2

* Tue Nov 26 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-0.1rc
- Update to 1.1-rc

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 14 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.3-1
- 1.0.3 release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.2-2
- Enable extra custom modes API

* Thu Dec  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.2-1
- Official 1.0.2 release

* Wed Sep 12 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.1-1
- Official 1.0.1 release now rfc6716 is stable

* Tue Sep  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.1rc3-0.1
- Update to 1.0.1rc3

* Thu Aug  9 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.0rc1-0.1
- Update to 1.0.0rc1

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 27 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.14-1
- Update to 0.9.14

* Sat May 12 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.10-2
- Add make check - fixes RHBZ # 821128

* Fri Apr 27 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.10-1
- Update to 0.9.10

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov  8 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.8-1
- Update to 0.9.8

* Mon Oct 10 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.6-1
- Initial packaging
