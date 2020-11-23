%define commit f1dc581

Summary: Kurento Module Creator
Name: kurento-module-creator
Version: 6.15.0
Release: 0%{?dist}
License: Apache 2.0
Group: Development/Tools
URL: https://github.com/Kurento/kurento-module-creator
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: cmake >= 2.8
BuildRequires: maven >= 3.0

%description
The kurento-module-creator project contains a processor that will
generate code for RPC between the Kurento Media Server and remote libraries

%prep
%setup -c -n %{name}-%{version}-%{commit} -T -D
if [ ! -d .git ]; then
    git clone https://github.com/Kurento/%{name}.git .
    git checkout %{commit}
fi

%build
mvn package

%install
install -p -d -m 0755 %{buildroot}%{_bindir}
install -p -D -m 0644 -t %{buildroot}%{_bindir} target/kurento-module-creator-jar-with-dependencies.jar
install -p -D -m 0755 -t %{buildroot}%{_bindir} scripts/kurento-module-creator

install -p -d -m 0755 %{buildroot}%{_datadir}/cmake/Modules
install -p -D -m 0644 -t %{buildroot}%{_datadir}/cmake/Modules target/classes/FindKurentoModuleCreator.cmake

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/*

%changelog
