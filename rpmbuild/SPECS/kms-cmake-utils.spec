%define		commit b5cbdf8

Summary: Kurento cmake utilities
Name: kms-cmake-utils
Version: 6.9.1
Release: 1%{?dist}
License: GPLv2+
Group: Development/Libraries
URL: https://github.com/Kurento/kms-cmake-utils
#Source0: Kurento-%{name}-%{commit}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: cmake >= 2.8
BuildRequires: cmake >= 2.8

%description
Common CMake utilities for Kurento projects

%prep
%setup -c -n %{name}-%{version}-%{commit} -T -D
if [ ! -d .git ]; then
    git clone https://github.com/Kurento/%{name}.git .
    git checkout %{commit}
fi

%build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=Release ..


%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}
mv %{buildroot}%{_datadir}/cmake-* %{buildroot}%{_datadir}/cmake


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_datadir}/cmake/*


%changelog
