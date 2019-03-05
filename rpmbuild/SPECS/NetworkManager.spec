%global dbus_glib_version 0.100

%global wireless_tools_version 1:28-0pre9

%global wpa_supplicant_version 1:1.1

%global ppp_version %(sed -n 's/^#define\\s*VERSION\\s*"\\([^\\s]*\\)"$/\\1/p' %{_includedir}/pppd/patchlevel.h 2>/dev/null | grep . || echo bad)
%global glib2_version %(pkg-config --modversion glib-2.0 2>/dev/null || echo bad)

%global epoch_version 1
%global rpm_version 1.12.0
%global real_version 1.12.0
%global release_version 6
%global snapshot %{nil}
%global git_sha %{nil}

%global obsoletes_device_plugins 1:0.9.9.95-1
%global obsoletes_ppp_plugin     1:1.5.3

%global systemd_dir %{_prefix}/lib/systemd/system
%global nmlibdir %{_prefix}/lib/%{name}
%global nmplugindir %{_libdir}/%{name}/%{version}-%{release}

%global _hardened_build 1

%if x%{?snapshot} != x
%global snapshot_dot .%{snapshot}
%endif
%if x%{?git_sha} != x
%global git_sha_dot .%{git_sha}
%endif

%global snap %{?snapshot_dot}%{?git_sha_dot}

%global real_version_major %(printf '%s' '%{real_version}' | sed -n 's/^\\([1-9][0-9]*\\.[1-9][0-9]*\\)\\.[1-9][0-9]*$/\\1/p')

%global is_devel_build %(printf '%s' '%{real_version}' | sed -n 's/^1\\.\\([0-9]*[13579]\\)\\..*/1/p')

###############################################################################

%bcond_without adsl
%bcond_without bluetooth
%bcond_without wwan
%bcond_without team
%bcond_without wifi
%bcond_with iwd
%bcond_without ovs
%bcond_without ppp
%bcond_without nmtui

# on RHEL we don't regenerate the documentation
%bcond_with    regen_docs

%if 0%{is_devel_build}
%bcond_without debug
%else
%bcond_with    debug
%endif
%bcond_without test
%bcond_with    sanitizer
%if 0%{?fedora} > 28 || 0%{?rhel} > 7
%bcond_with libnm_glib
%else
%bcond_without libnm_glib
%endif
%if 0%{?fedora}
%bcond_without connectivity_fedora
%else
%bcond_with connectivity_fedora
%endif
%if 0%{?rhel} && 0%{?rhel} > 7
%bcond_without connectivity_redhat
%else
%bcond_with connectivity_redhat
%endif
%if 0%{?fedora} > 28 || 0%{?rhel} > 7
%bcond_without crypto_gnutls
%else
%bcond_with crypto_gnutls
%endif

###############################################################################

%if 0%{?fedora}
%global dbus_version 1.9.18
%global dbus_sys_dir %{_datadir}/dbus-1/system.d
%else
%global dbus_version 1.1
%global dbus_sys_dir %{_sysconfdir}/dbus-1/system.d
%endif

%if %{with bluetooth} || %{with wwan}
%global with_modem_manager_1 1
%else
%global with_modem_manager_1 0
%endif

###############################################################################

Name: NetworkManager
Summary: Network connection manager and user applications
Epoch: %{epoch_version}
Version: %{rpm_version}
Release: %{release_version}%{?snap}%{?dist}
Group: System Environment/Base
License: GPLv2+
URL: http://www.gnome.org/projects/NetworkManager/

Source: https://download.gnome.org/sources/NetworkManager/%{real_version_major}/%{name}-%{real_version}.tar.xz
Source1: NetworkManager.conf
Source2: 00-server.conf
Source3: 20-connectivity-fedora.conf
Source4: 20-connectivity-redhat.conf
Source5: 10-slaves-order.conf

# RHEL downstream patches that change behavior from upstream.
# These are not bugfixes, hence they are also relevant after
# the next rebase of the source tarball.
Patch1: 0001-cloned-mac-address-permanent-rh1413312.patch
Patch2: 0002-nm-wait-online-not-require-nm-service-rh1520865.patch
Patch3: 0003-dhclient-no-leading-zero-client-id-rh1556983.patch
Patch4: 0004-device-disable-rp_filter-handling.patch
Patch5: 0005-ibft-cap-sys-admin-rh1371201.patch
Patch6: 0006-support-aes256-private-keys-rh1623798.patch
Patch7: 0007-core-fix-wireless-bitrate-property-name-on-D-Bus-rh1626391.patch
Patch8: 0008-dns-dnsmsaq-avoid-crash-no-rev-domains-rh1628576.patch

Patch1000: 1000-cli-remove-assertion-in-nmc_device_state_to_color.patch
Patch1001: 1001-translations-rh1569438.patch
Patch1002: 1002-cli-fix-reading-vpn.secrets.-from-passwd-file.patch

# The pregenerated docs contain default values and paths that depend
# on the configure options when creating the source tarball.
# As last step, patch the documentation with the proper defaults
# for RHEL.
Patch9999: 9999-fix-pregen-doc.patch

Requires(post): systemd
Requires(post): /usr/sbin/update-alternatives
Requires(preun): systemd
Requires(preun): /usr/sbin/update-alternatives
Requires(postun): systemd

Requires: dbus >= %{dbus_version}
Requires: glib2 >= %{glib2_version}
Requires: %{name}-libnm%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes: dhcdbd
Obsoletes: NetworkManager < %{obsoletes_device_plugins}
Obsoletes: NetworkManager < %{obsoletes_ppp_plugin}
Obsoletes: NetworkManager-wimax < 1.2

# Kept for RHEL to ensure that wired 802.1x works out of the box
Requires: wpa_supplicant >= 1:1.1

Conflicts: NetworkManager-vpnc < 1:0.7.0.99-1
Conflicts: NetworkManager-openvpn < 1:0.7.0.99-1
Conflicts: NetworkManager-pptp < 1:0.7.0.99-1
Conflicts: NetworkManager-openconnect < 0:0.7.0.99-1
Conflicts: kde-plasma-networkmanagement < 1:0.9-0.49.20110527git.nm09

BuildRequires: gcc
BuildRequires: libtool
BuildRequires: pkgconfig
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: intltool
BuildRequires: gettext-devel

BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
%if 0%{?fedora}
BuildRequires: wireless-tools-devel >= %{wireless_tools_version}
%endif
BuildRequires: glib2-devel >= 2.40.0
BuildRequires: gobject-introspection-devel >= 0.10.3
%if %{with ppp}
BuildRequires: ppp-devel >= 2.4.5
%endif
%if %{with crypto_gnutls}
BuildRequires: gnutls-devel >= 2.12
%else
BuildRequires: nss-devel >= 3.11.7
%endif
BuildRequires: dhclient
BuildRequires: readline-devel
BuildRequires: audit-libs-devel
%if %{with regen_docs}
BuildRequires: gtk-doc
%endif
BuildRequires: libudev-devel
BuildRequires: libuuid-devel
BuildRequires: vala-tools
BuildRequires: iptables
BuildRequires: libxslt
%if %{with bluetooth}
BuildRequires: bluez-libs-devel
%endif
BuildRequires: systemd >= 200-3 systemd-devel
%if 0%{?fedora}
BuildRequires: libpsl-devel >= 0.1
%endif
BuildRequires: libcurl-devel
BuildRequires: libndp-devel >= 1.0
%if 0%{?with_modem_manager_1}
BuildRequires: ModemManager-glib-devel >= 1.0
%endif
%if %{with nmtui}
BuildRequires: newt-devel
%endif
BuildRequires: /usr/bin/dbus-launch
%if 0%{?fedora} > 27 || 0%{?rhel} > 7
BuildRequires: python3
BuildRequires: python3-gobject-base
BuildRequires: python3-dbus
%else
BuildRequires: python2
BuildRequires: pygobject3-base
BuildRequires: dbus-python
%endif
BuildRequires: libselinux-devel
BuildRequires: polkit-devel
BuildRequires: jansson-devel
%if %{with sanitizer}
BuildRequires: libasan
%if 0%{?fedora}
BuildRequires: libubsan
%endif
%endif


%description
NetworkManager is a system service that manages network interfaces and
connections based on user or automatic configuration. It supports
Ethernet, Bridge, Bond, VLAN, Team, InfiniBand, Wi-Fi, mobile broadband
(WWAN), PPPoE and other devices, and supports a variety of different VPN
services.


%if %{with adsl}
%package adsl
Summary: ADSL device plugin for NetworkManager
Group: System Environment/Base
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes: NetworkManager < %{obsoletes_device_plugins}
Obsoletes: NetworkManager-atm

%description adsl
This package contains NetworkManager support for ADSL devices.
%endif


%if %{with bluetooth}
%package bluetooth
Summary: Bluetooth device plugin for NetworkManager
Group: System Environment/Base
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: NetworkManager-wwan = %{epoch}:%{version}-%{release}
# No Requires:bluez to prevent it being installed when updating
# to the split NM package
Obsoletes: NetworkManager < %{obsoletes_device_plugins}
Obsoletes: NetworkManager-bt

%description bluetooth
This package contains NetworkManager support for Bluetooth devices.
%endif


%if %{with team}
%package team
Summary: Team device plugin for NetworkManager
Group: System Environment/Base
BuildRequires: teamd-devel
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes: NetworkManager < %{obsoletes_device_plugins}

%description team
This package contains NetworkManager support for team devices.
%endif


%if %{with wifi}
%package wifi
Summary: Wifi plugin for NetworkManager
Group: System Environment/Base
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%if %{with iwd} && (0%{?fedora} > 24 || 0%{?rhel} > 7)
Requires: (wpa_supplicant >= %{wpa_supplicant_version} or iwd)
%else
# Just require wpa_supplicant on platforms that don't support boolean
# dependencies even though the plugin supports both supplicant and
# iwd backend.
Requires: wpa_supplicant >= %{wpa_supplicant_version}
%endif

Obsoletes: NetworkManager < %{obsoletes_device_plugins}

%description wifi
This package contains NetworkManager support for Wifi and OLPC devices.
%endif


%if %{with wwan}
%package wwan
Summary: Mobile broadband device plugin for NetworkManager
Group: System Environment/Base
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
# No Requires:ModemManager to prevent it being installed when updating
# to the split NM package
Obsoletes: NetworkManager < %{obsoletes_device_plugins}

%description wwan
This package contains NetworkManager support for mobile broadband (WWAN)
devices.
%endif


%if %{with ovs}
%package ovs
Summary: Open vSwitch device plugin for NetworkManager
Group: System Environment/Base
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: openvswitch

%description ovs
This package contains NetworkManager support for Open vSwitch bridges.
%endif


%if %{with ppp}
%package ppp
Summary: PPP plugin for NetworkManager
Group: System Environment/Base
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: ppp = %{ppp_version}
Requires: NetworkManager = %{epoch}:%{version}-%{release}
Obsoletes: NetworkManager < %{obsoletes_ppp_plugin}

%description ppp
This package contains NetworkManager support for PPP.
%endif


%package glib
Summary: Libraries for adding NetworkManager support to applications (old API).
Group: Development/Libraries
Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_glib_version}
Conflicts: NetworkManager-libnm < %{epoch}:%{version}-%{release}

%description glib
This package contains the libraries that make it easier to use some
NetworkManager functionality from applications that use glib.  This is
the older NetworkManager API. See also NetworkManager-libnm.


%package glib-devel
Summary: Header files for adding NetworkManager support to applications (old API).
Group: Development/Libraries
Requires: %{name}-glib%{?_isa} = %{epoch}:%{version}-%{release}
Requires: glib2-devel
Requires: pkgconfig
Requires: dbus-glib-devel >= %{dbus_glib_version}
Provides: %{name}-devel = %{epoch}:%{version}-%{release}
Provides: %{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-devel < %{epoch}:%{version}-%{release}

%description glib-devel
This package contains the header and pkg-config files for development
applications using NetworkManager functionality from applications that
use glib.
This is the older NetworkManager API.  See also NetworkManager-libnm-devel.


%package libnm
Summary: Libraries for adding NetworkManager support to applications (new API).
Group: Development/Libraries
Conflicts: NetworkManager-glib < %{epoch}:%{version}-%{release}

%description libnm
This package contains the libraries that make it easier to use some
NetworkManager functionality from applications.  This is the new
NetworkManager API.  See also NetworkManager-glib.


%package libnm-devel
Summary: Header files for adding NetworkManager support to applications (new API).
Group: Development/Libraries
Requires: %{name}-libnm%{?_isa} = %{epoch}:%{version}-%{release}
Requires: glib2-devel
Requires: pkgconfig

%description libnm-devel
This package contains the header and pkg-config files for development
applications using NetworkManager functionality from applications.  This
is the new NetworkManager API. See also NetworkManager-glib-devel.


%if %{with connectivity_fedora}
%package config-connectivity-fedora
Summary: NetworkManager config file for connectivity checking via Fedora servers
Group: System Environment/Base
BuildArch: noarch
Provides: NetworkManager-config-connectivity = %{epoch}:%{version}-%{release}

%description config-connectivity-fedora
This adds a NetworkManager configuration file to enable connectivity checking
via Fedora infrastructure.
%endif


%if %{with connectivity_redhat}
%package config-connectivity-redhat
Summary: NetworkManager config file for connectivity checking via Red Hat servers
Group: System Environment/Base
BuildArch: noarch
Provides: NetworkManager-config-connectivity = %{epoch}:%{version}-%{release}

%description config-connectivity-redhat
This adds a NetworkManager configuration file to enable connectivity checking
via Red Hat infrastructure.
%endif


%package config-server
Summary: NetworkManager config file for "server-like" defaults
Group: System Environment/Base
BuildArch: noarch

%description config-server
This adds a NetworkManager configuration file to make it behave more
like the old "network" service. In particular, it stops NetworkManager
from automatically running DHCP on unconfigured ethernet devices, and
allows connections with static IP addresses to be brought up even on
ethernet devices with no carrier.

This package is intended to be installed by default for server
deployments.


%package dispatcher-routing-rules
Summary: NetworkManager dispatcher file for advanced routing rules
Group: System Environment/Base
BuildArch: noarch
Provides: %{name}-config-routing-rules = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-config-routing-rules < %{epoch}:%{version}-%{release}

%description dispatcher-routing-rules
This adds a NetworkManager dispatcher file to support networking
configurations using "/etc/sysconfig/network-scripts/rule-NAME" files
(eg, to do policy-based routing).


%if 0%{with_nmtui}
%package tui
Summary: NetworkManager curses-based UI
Group: System Environment/Base
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{name}-libnm%{?_isa} = %{epoch}:%{version}-%{release}

%description tui
This adds a curses-based "TUI" (Text User Interface) to
NetworkManager, to allow performing some of the operations supported
by nm-connection-editor and nm-applet in a non-graphical environment.
%endif


%prep
%autosetup -p1 -n NetworkManager-%{real_version}


%build
%if %{with regen_docs}
gtkdocize
%endif
autoreconf --install --force
intltoolize --automake --copy --force
%configure \
	--disable-silent-rules \
	--disable-static \
	--with-dhclient=yes \
	--with-dhcpcd=no \
	--with-dhcpcanon=no \
	--with-config-dhcp-default=dhclient \
%if %{with crypto_gnutls}
	--with-crypto=gnutls \
%else
	--with-crypto=nss \
%endif
%if %{with sanitizer}
	--with-address-sanitizer=exec \
%if 0%{?fedora}
	--enable-undefined-sanitizer \
%endif
%else
	--with-address-sanitizer=no \
	--disable-undefined-sanitizer \
%endif
%if %{with debug}
	--enable-more-logging \
	--with-more-asserts=10000 \
%else
	--disable-more-logging \
	--without-more-asserts \
%endif
	--enable-ld-gc \
	--with-libaudit=yes-disabled-by-default \
%if 0%{?with_modem_manager_1}
	--with-modem-manager-1=yes \
%else
	--with-modem-manager-1=no \
%endif
%if %{with wifi}
	--enable-wifi=yes \
%if 0%{?fedora}
	--with-wext=yes \
%else
	--with-wext=no \
%endif
%else
	--enable-wifi=no \
%endif
%if %{with iwd}
	--with-iwd=yes \
%else
	--with-iwd=no \
%endif
	--enable-vala=yes \
	--enable-introspection \
%if %{with regen_docs}
	--enable-gtk-doc \
%else
	--disable-gtk-doc \
%endif
%if %{with team}
	--enable-teamdctl=yes \
%else
	--enable-teamdctl=no \
%endif
%if %{with ovs}
	--enable-ovs=yes \
%else
	--enable-ovs=no \
%endif
	--with-selinux=yes \
	--enable-polkit=yes \
	--enable-polkit-agent \
	--enable-modify-system=yes \
	--enable-concheck \
%if 0%{?fedora}
	--with-libpsl \
%else
	--without-libpsl \
%endif
	--with-session-tracking=systemd \
	--with-suspend-resume=systemd \
	--with-systemdsystemunitdir=%{systemd_dir} \
	--with-system-ca-path=/etc/pki/tls/cert.pem \
	--with-dbus-sys-dir=%{dbus_sys_dir} \
%if %{with test}
	--with-tests=yes \
%else
	--enable-more-warnings=yes \
	--with-tests=no \
%endif
	--with-valgrind=no \
	--enable-ifcfg-rh=yes \
%if %{with ppp}
	--with-pppd-plugin-dir=%{_libdir}/pppd/%{ppp_version} \
	--enable-ppp=yes \
%endif
	--with-dist-version=%{version}-%{release} \
	--with-config-plugins-default='ifcfg-rh,ibft' \
	--with-config-dns-rc-manager-default=file \
	--with-config-logging-backend-default=syslog \
	--enable-json-validation \
%if %{with libnm_glib}
	--with-libnm-glib
%else
	--without-libnm-glib
%endif

make %{?_smp_mflags}


%install
# install NM
make install DESTDIR=%{buildroot}

cp %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/

cp %{SOURCE2} %{buildroot}%{nmlibdir}/conf.d/

%if %{with connectivity_fedora}
cp %{SOURCE3} %{buildroot}%{nmlibdir}/conf.d/
%endif

%if %{with connectivity_redhat}
cp %{SOURCE4} %{buildroot}%{nmlibdir}/conf.d/
%endif

cp %{SOURCE5} %{buildroot}%{nmlibdir}/conf.d/

cp examples/dispatcher/10-ifcfg-rh-routes.sh %{buildroot}%{_sysconfdir}/%{name}/dispatcher.d/
ln -s ../no-wait.d/10-ifcfg-rh-routes.sh %{buildroot}%{_sysconfdir}/%{name}/dispatcher.d/pre-up.d/
ln -s ../10-ifcfg-rh-routes.sh %{buildroot}%{_sysconfdir}/%{name}/dispatcher.d/no-wait.d/

%find_lang %{name}

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/pppd/%{ppp_version}/*.la
rm -f %{buildroot}%{nmplugindir}/*.la

# Ensure the documentation timestamps are constant to avoid multilib conflicts
find %{buildroot}%{_datadir}/gtk-doc -exec touch --reference configure.ac '{}' \+

%if 0%{?__debug_package}
mkdir -p %{buildroot}%{_prefix}/src/debug/NetworkManager-%{real_version}
cp valgrind.suppressions %{buildroot}%{_prefix}/src/debug/NetworkManager-%{real_version}
%endif

touch %{buildroot}%{_sbindir}/ifup %{buildroot}%{_sbindir}/ifdown


%check
%if %{with test}
make %{?_smp_mflags} check
%endif


%pre
if [ -f "%{systemd_dir}/network-online.target.wants/NetworkManager-wait-online.service" ] ; then
    # older versions used to install this file, effectively always enabling
    # NetworkManager-wait-online.service. We no longer do that and rely on
    # preset.
    # But on package upgrade we must explicitly enable it (rh#1455704).
    systemctl enable NetworkManager-wait-online.service || :
fi


%post
/usr/bin/udevadm control --reload-rules || :
/usr/bin/udevadm trigger --subsystem-match=net || :

%systemd_post NetworkManager.service NetworkManager-wait-online.service NetworkManager-dispatcher.service

%triggerin -- initscripts
if [ -f %{_sbindir}/ifup -a ! -L %{_sbindir}/ifup ]; then
    # initscripts package too old, won't let us set an alternative
    /usr/sbin/update-alternatives --remove ifup %{_libexecdir}/nm-ifup >/dev/null 2>&1 || :
else
    /usr/sbin/update-alternatives --install %{_sbindir}/ifup ifup %{_libexecdir}/nm-ifup 50 \
        --slave %{_sbindir}/ifdown ifdown %{_libexecdir}/nm-ifdown
fi


%preun
if [ $1 -eq 0 ]; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable NetworkManager.service >/dev/null 2>&1 || :

    # Don't kill networking entirely just on package remove
    #/bin/systemctl stop NetworkManager.service >/dev/null 2>&1 || :

    /usr/sbin/update-alternatives --remove ifup %{_libexecdir}/nm-ifup >/dev/null 2>&1 || :
fi
%systemd_preun NetworkManager-wait-online.service NetworkManager-dispatcher.service


%postun
/usr/bin/udevadm control --reload-rules || :
/usr/bin/udevadm trigger --subsystem-match=net || :

%systemd_postun


%post   glib -p /sbin/ldconfig
%postun glib -p /sbin/ldconfig

%post   libnm -p /sbin/ldconfig
%postun libnm -p /sbin/ldconfig


%files
%{dbus_sys_dir}/org.freedesktop.NetworkManager.conf
%{dbus_sys_dir}/nm-dispatcher.conf
%{dbus_sys_dir}/nm-ifcfg-rh.conf
%{_sbindir}/%{name}
%{_bindir}/nmcli
%{_datadir}/bash-completion/completions/nmcli
%dir %{_sysconfdir}/%{name}/
%dir %{_sysconfdir}/%{name}/dispatcher.d
%dir %{_sysconfdir}/%{name}/dispatcher.d/pre-down.d
%dir %{_sysconfdir}/%{name}/dispatcher.d/pre-up.d
%dir %{_sysconfdir}/%{name}/dispatcher.d/no-wait.d
%dir %{_sysconfdir}/%{name}/dnsmasq.d
%dir %{_sysconfdir}/%{name}/dnsmasq-shared.d
%config(noreplace) %{_sysconfdir}/%{name}/NetworkManager.conf
%{nmlibdir}/conf.d/10-slaves-order.conf
%{_bindir}/nm-online
%{_libexecdir}/nm-ifup
%ghost %attr(755, root, root) %{_sbindir}/ifup
%{_libexecdir}/nm-ifdown
%ghost %attr(755, root, root) %{_sbindir}/ifdown
%{_libexecdir}/nm-dhcp-helper
%{_libexecdir}/nm-dispatcher
%{_libexecdir}/nm-iface-helper
%dir %{_libdir}/%{name}
%dir %{nmplugindir}
%{nmplugindir}/libnm-settings-plugin*.so
%if %{with nmtui}
%exclude %{_mandir}/man1/nmtui*
%endif
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/conf.d
%dir %{nmlibdir}
%dir %{nmlibdir}/conf.d
%dir %{nmlibdir}/VPN
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/nmcli-examples.7*
%{_mandir}/man8/*
%dir %{_localstatedir}/lib/NetworkManager
%dir %{_sysconfdir}/NetworkManager/system-connections
%{_datadir}/dbus-1/system-services/org.freedesktop.NetworkManager.service
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_dispatcher.service
%{_datadir}/polkit-1/actions/*.policy
%{_prefix}/lib/udev/rules.d/*.rules
# systemd stuff
%{systemd_dir}/NetworkManager.service
%{systemd_dir}/NetworkManager-wait-online.service
%{systemd_dir}/NetworkManager-dispatcher.service
%dir %{_datadir}/doc/NetworkManager/examples
%{_datadir}/doc/NetworkManager/examples/server.conf
%doc NEWS AUTHORS README CONTRIBUTING TODO
%license COPYING


%if %{with adsl}
%files adsl
%{nmplugindir}/libnm-device-plugin-adsl.so
%else
%exclude %{nmplugindir}/libnm-device-plugin-adsl.so
%endif


%if %{with bluetooth}
%files bluetooth
%{nmplugindir}/libnm-device-plugin-bluetooth.so
%endif


%if %{with team}
%files team
%{nmplugindir}/libnm-device-plugin-team.so
%endif


%if %{with wifi}
%files wifi
%{nmplugindir}/libnm-device-plugin-wifi.so
%endif


%if %{with wwan}
%files wwan
%{nmplugindir}/libnm-device-plugin-wwan.so
%{nmplugindir}/libnm-wwan.so
%endif


%if %{with ovs}
%files ovs
%{nmplugindir}/libnm-device-plugin-ovs.so
%{systemd_dir}/NetworkManager.service.d/NetworkManager-ovs.conf
%{_mandir}/man7/nm-openvswitch.7*
%endif


%if %{with ppp}
%files ppp
%{_libdir}/pppd/%{ppp_version}/nm-pppd-plugin.so
%{nmplugindir}/libnm-ppp-plugin.so
%endif


%if %{with libnm_glib}
%files glib -f %{name}.lang
%{_libdir}/libnm-glib.so.*
%{_libdir}/libnm-glib-vpn.so.*
%{_libdir}/libnm-util.so.*
%{_libdir}/girepository-1.0/NetworkManager-1.0.typelib
%{_libdir}/girepository-1.0/NMClient-1.0.typelib
%endif


%if %{with libnm_glib}
%files glib-devel
%doc docs/api/html/*
%dir %{_includedir}/libnm-glib
%dir %{_includedir}/%{name}
%{_includedir}/libnm-glib/*.h
%{_includedir}/%{name}/%{name}.h
%{_includedir}/%{name}/NetworkManagerVPN.h
%{_includedir}/%{name}/nm-setting*.h
%{_includedir}/%{name}/nm-connection.h
%{_includedir}/%{name}/nm-utils-enum-types.h
%{_includedir}/%{name}/nm-utils.h
%{_includedir}/%{name}/nm-version.h
%{_includedir}/%{name}/nm-version-macros.h
%{_libdir}/pkgconfig/libnm-glib.pc
%{_libdir}/pkgconfig/libnm-glib-vpn.pc
%{_libdir}/pkgconfig/libnm-util.pc
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/libnm-glib.so
%{_libdir}/libnm-glib-vpn.so
%{_libdir}/libnm-util.so
%{_datadir}/gir-1.0/NetworkManager-1.0.gir
%{_datadir}/gir-1.0/NMClient-1.0.gir
%dir %{_datadir}/gtk-doc/html/libnm-glib
%{_datadir}/gtk-doc/html/libnm-glib/*
%dir %{_datadir}/gtk-doc/html/libnm-util
%{_datadir}/gtk-doc/html/libnm-util/*
%{_datadir}/vala/vapi/libnm-*.deps
%{_datadir}/vala/vapi/libnm-*.vapi
%endif


%files libnm -f %{name}.lang
%{_libdir}/libnm.so.*
%{_libdir}/girepository-1.0/NM-1.0.typelib


%files libnm-devel
%doc docs/api/html/*
%dir %{_includedir}/libnm
%{_includedir}/libnm/*.h
%{_libdir}/pkgconfig/libnm.pc
%{_libdir}/libnm.so
%{_datadir}/gir-1.0/NM-1.0.gir
%dir %{_datadir}/gtk-doc/html/libnm
%{_datadir}/gtk-doc/html/libnm/*
%dir %{_datadir}/gtk-doc/html/NetworkManager
%{_datadir}/gtk-doc/html/NetworkManager/*
%{_datadir}/vala/vapi/libnm.deps
%{_datadir}/vala/vapi/libnm.vapi
%{_datadir}/dbus-1/interfaces/*.xml


%if %{with connectivity_fedora}
%files config-connectivity-fedora
%dir %{nmlibdir}
%dir %{nmlibdir}/conf.d
%{nmlibdir}/conf.d/20-connectivity-fedora.conf
%endif


%if %{with connectivity_redhat}
%files config-connectivity-redhat
%dir %{nmlibdir}
%dir %{nmlibdir}/conf.d
%{nmlibdir}/conf.d/20-connectivity-redhat.conf
%endif


%files config-server
%dir %{nmlibdir}
%dir %{nmlibdir}/conf.d
%{nmlibdir}/conf.d/00-server.conf


%files dispatcher-routing-rules
%{_sysconfdir}/%{name}/dispatcher.d/10-ifcfg-rh-routes.sh
%{_sysconfdir}/%{name}/dispatcher.d/no-wait.d/10-ifcfg-rh-routes.sh
%{_sysconfdir}/%{name}/dispatcher.d/pre-up.d/10-ifcfg-rh-routes.sh


%if %{with nmtui}
%files tui
%{_bindir}/nmtui
%{_bindir}/nmtui-edit
%{_bindir}/nmtui-connect
%{_bindir}/nmtui-hostname
%{_mandir}/man1/nmtui*
%endif


%changelog
* Sat Sep 15 2018 Beniamino Galvani <bgalvani@redhat.com> - 1:1.12.0-6
- dns: dnsmasq: avoid crash when no reverse domains exist (rh #1628576)
- initscripts: fix ownership of ifup/ifdown executables (rh #1626517)
- cli: fix parsing vpn secrets from password file (rh #1628946)

* Fri Sep  7 2018 Beniamino Galvani <bgalvani@redhat.com> - 1:1.12.0-5
- core: fix wireless bitrate property name on D-Bus (rh #1626391)

* Thu Aug 30 2018 Beniamino Galvani <bgalvani@redhat.com> - 1:1.12.0-4
- libnm-core: support private keys encrypted with AES-{192,256}-CBC (rh #1623798)

* Sun Aug 19 2018 Lubomir Rintel <lrintel@redhat.com> - 1:1.12.0-3
- cli: remove assertion in nmc_device_state_to_color() (rh #1614691)
- po: import Japanese translation (rh #1569438)

* Wed Jul  4 2018 Beniamino Galvani <bgalvani@redhat.com> - 1:1.12.0-2
- device: disable rp_filter handling (rh #1593194)
- ibft: grant required CAP_SYS_ADMIN capabilities (rh#1596954)

* Sun Jul  1 2018 Thomas Haller <thaller@redhat.com> - 1:1.12.0-1
- Update to upstream 1.12.0 release (rh #1592311)
- device: improve MTU handling for VLAN (rh #1586191)

* Wed Jun 20 2018 Beniamino Galvani <bgalvani@redhat.com> - 1:1.12.0-0.2
- dhcp: preserve old behavior and don't add leading zero to printable client-id (rh #1556983)

* Mon Jun 18 2018 Thomas Haller <thaller@redhat.com> - 1:1.12.0-0.1
- Update to upstream release 1.11.90 (release candidate) (rh #1592311)
- libnm: properly handle cancelling of async operations (rh #1555281)
- libnm: support handling checkpoints (rh #1496739)
- core: fix blocking/not-blocking autoconnect related to missing secrets (rh #1553113)
- core: rework and improve IPv4 address collission detection (rh #1507864)
- wifi: fix timeout handling for supplicant when no secrets provided (rh #1575501)
- macsec: enable sending SCI by default and make it configurable (rh #1588041)
- ethernet: support announcing duplex/speed in combination with autonegotiation (rh #1487477)
- wwan: improve failure reason for unsupported IP methods (rh #1459529)
- tun: use netlink kernel API for tun devices if available (rh #1547213)
- ovs: fix assertion during shutdown of NetworkManager (rh #1543871)
- dhcp: improve handling DHCP timeouts (rh #1573780)
- dhcp: support specifying ipv6.dhcp-duid (rh #1414093)
- dhcp: support generating ipv4.dhcp-client-id based on MAC/stable-id
- dns: avoid updating resolv.conf when exiting (rh #1541031)
- ifcfg-rh: fix IPv4 settings in combination with method "shared" (rh #1519299)
- ifcfg-rh: fix handling unset Wi-Fi mode (rh #1549972)
- iface-helper: fix invalid reentrant call to platform (rh #1546656)
- doc: various improvments to documentation (rh #1543832)

* Fri Jun 15 2018 Thomas Haller <thaller@redhat.com> - 1:1.10.2-16
- device: fix crash during reapply of connection settings (rh #1591631)

* Wed Jun  6 2018 Beniamino Galvani <bgalvani@redhat.com> - 1:1.10.2-15
- device: start IP configuration when master carrier goes up (rh #1576254)

* Mon Apr 23 2018 Beniamino Galvani <bgalvani@redhat.com> - 1:1.10.2-14
- manager: retry activating devices when the parent becomes managed (rh #1553595)
- manager: allow autoconnect-slaves to reconnect the same connection (rh #1548265)
- manager: fix starting teamd after service restart (rh #1551958)

* Tue Feb 20 2018 Francesco Giudici <fgiudici@redhat.com> - 1:1.10.2-13
- dhcp: better handle DHCP outages and retry DHCP indefinitely (rh #1503587)

* Thu Feb 8 2018 Beniamino Galvani <bgalvani@redhat.com> - 1:1.10.2-12
- ppp: don't start IPv6 configuration on the device (rh #1515829)
- device: avoid setting the IPv4 rp_filter (rh #1492472)
- nmcli: team: clear runner-tx-hash before adding new hashes (rh #1541922)

* Fri Feb 2 2018 Lubomir Rintel <lrintel@redhat.com> - 1:1.10.2-11
- ovs-interface: avoid starting ip configuration twice (rh #1540063)
- libnm-core: ensure alignment of team.config and other team properties (rh #1533830)
- nmcli: clear link-watchers before adding the new ones (rh #1533926)
- libnm-core: update team.runner description (rh #1533799)
- libnm-core: team: fix runner sys_prio default value (rh #1533810)
- libnm: avoid a symbol clash with json-glib (rh #1535905)
- libnm-core: team: add support to runner "random" (rh #1538699)

* Fri Jan 19 2018 Beniamino Galvani <bgalvani@redhat.com> - 1:1.10.2-10
- device: skip IP configuration phase for external devices (rh #1530288)
- platform: fix crash during route-get call (rh #1534721)

* Fri Jan 19 2018 Lubomir Rintel <lrintel@redhat.com> - 1:1.10.2-9
- ifcfg: don't forget master of ovs interfaces (rh #1519179)

* Wed Jan 17 2018 Lubomir Rintel <lrintel@redhat.com> - 1:1.10.2-7
- po: import translations (rh #1481186)
- device: increase carrier wait time to 6 seconds (rh #1520826)

* Mon Jan 15 2018 Thomas Haller <thaller@redhat.com> - 1:1.10.2-6
- core: use distinct route-metric to keep connectivity on first activated device (rh #1505893)
- core: fix enabling connectivity-check-enabled via D-Bus (rh #1534477)
- core: fix invalid assertion deleting volatile connection (rh #1506552)

* Tue Jan  9 2018 Beniamino Galvani <bgalvani@redhat.com> - 1:1.10.2-5
- wwan: add default route even if modem didn't return a gateway (rh #1527934)
- dhcp: fix assertion failure for dhcp-client-id (rh #1531173)

* Fri Jan  5 2018 Beniamino Galvani <bgalvani@redhat.com> - 1:1.10.2-4
- settings: clear unsaved flag on new connections (rh #1525078)
- platform-linux: reload qdiscs and tfilters after removing them (rh #1527197)

* Tue Dec 12 2017 Thomas Haller <thaller@redhat.com> - 1:1.10.2-3
- all: various bug fixes found by coverity

* Tue Dec 12 2017 Lubomir Rintel <lrintel@redhat.com> - 1:1.10.2-2
- po: import translations (rh #1481186)

* Tue Dec 12 2017 Beniamino Galvani <bgalvani@redhat.com> - 1:1.10.2-1
- Update to upstream release 1.10.2
- all: added support for onlink route attribute (rh #1428334)
- device: don't necessarily fail the connection when ipv4 DAD fails (rh #1508001)
- device: update device mtu from ip interface platform when required (rh #1460217)
- device: extend carrier lost defer time after MTU change (rh #1487702)
- ifcfg-rh: persist the wep key type (rh #1518177)
- settings: introduce an Update2() D-Bus method (rh #1401515)

* Fri Dec  8 2017 Thomas Haller <thaller@redhat.com> - 1:1.10.0-2
- core: don't let NetworkManager-wait-online service require NetworkManager (rh #1520865)

* Fri Nov 10 2017 Beniamino Galvani <bgalvani@redhat.com> - 1:1.10.0-1
- Update to upstream release 1.10.0

* Wed Nov  8 2017 Beniamino Galvani <bgalvani@redhat.com> - 1:1.10.0-0.2.rc1
- Update to first Release Candidate of NetworkManager 1.10
- added basic OpenVSwitch support (rh #1470282)
- fixed race condition in the nmcli secret agent (rh #1438476)

* Fri Oct 27 2017 Beniamino Galvani <bgalvani@redhat.com> - 1:1.10.0-0.1.git20171024.b16c853b
- Update to a 1.10.0 snapshot:
- core: fix connection auto-activation after slave failure (rh #1310676)
- bridge: introduce a bridge.group-forward-mask connection property (rh #1358615)
- ifcfg-rh: fix write of 802.1X EAP-LEAP connections (rh #1374660)
- vlan: fix setting MTU value (rh #1414901)
- core: support multiple routing tables (rh #1436531)
- ipv6: support multiple default routes (rh #1445417)
- core: extend D-Bus API to better export active connection state (rh #1454883)
- nmcli: fix crash (rh #1458311)
- device: avoid touching IPv6 on external connections without IPv6 conf (rh #1462260)
- core: downgrade warning messages about missing parent devices (rh #1490157)
- device: fix delay startup complete for unrealized devices (rh #1498807)
- device: fix frozen notify signals on unrealize error path (rh #1498755)
- tui: improve tracking of activation state (rh #1500651)
- ifcfg-rh: allow updates to connections with routing rule files (rh #1384799)
- core: fix taking over external connection on modification (rh #1462223)
- bond: ignore miimon option only when it is zero (rh #1463077)
- core: don't re-add routes that already exist (rh #1470930)
- tui: guess the prefix length (netmask) based on network class (rh #1474295)
- dhcp: fix dhcp over Infiniband when using the internal client (rh #1477678)
- device: extend wait time for carrier after MTU change (rh #1487702)
- cli: wifi: connect with PSK when the AP supports WPA-PSK and WPA-EAP (rh #1492064)
- core: fixed memory leak in dhcp code (rh #1461643)

* Fri Oct  6 2017 Thomas Haller <thaller@redhat.com> - 1:1.8.0-11
- core: fix wrongly delaying startup-complete for unrealized devices (rh#1498807)
- core: fix unfreezing signals when unrealizing device fails (rh#1498755)

* Tue Sep 12 2017 Beniamino Galvani <bgalvani@redhat.com> - 1:1.8.0-10
- core: fix for MAC change after master reactivation (rh #1490741)

* Tue Jun 13 2017 Thomas Haller <thaller@redhat.com> - 1:1.8.0-9
- device: don't change MTU unless explicitly configured (rh #1460760)
- core: don't remove external IPv4 addresses (rh #1459813)

* Mon Jun 12 2017 Beniamino Galvani <bgalvani@redhat.com> - 1:1.8.0-8
- cli: fix output of iface in overview output (rh#1460219)
- ppp: unexport NMPPPManager instance on dispose (rh#1459579)
- cli: remove spurious device names from wifi subcommands output (rh#1460527)

* Fri Jun  9 2017 Thomas Haller <thaller@redhat.com> - 1:1.8.0-7
- bond: fix crash comparing mode while generating bond connection (rh #1459580)
- connectivity: fix route penalty if WWAN and BT device using ip-ifindex (rh #1459932)
- device: persist nm-owned in run state (rh #1376199)
- device: fix assuming master device on restart (rh #1452062)
- device: apply route metric penality only when the default route exists (rh #1459604)

* Tue Jun  6 2017 Thomas Haller <thaller@redhat.com> - 1:1.8.0-6
- connectivity: fix periodic connectivity check (rh #1458399)
- bond: improve option matching on daemon restart (rh #1457909)
- device: fix touching device after external activation (rh #1457242)

* Fri Jun  2 2017 Thomas Haller <thaller@redhat.com> - 1:1.8.0-5
- ifcfg-rh: fix writing legacy NETMASK value (rh #1445414)
- tui: fix crash during connect (rh #1456826)
- libnm: fix libnm rejecting VLAN ID 4095 (rh #1456911)

* Mon May 22 2017 Beniamino Galvani <bgalvani@redhat.com> - 1:1.8.0-4
- device: update external configuration before commit (rh #1449873)
- bluetooth: fix crash on connecting to a NAP (rh #1454385)
- device: release removed devices from master on cleanup (rh #1448907)
- core: activate slaves using ifindex order by default (rh #1452585)
- nmcli: fix crash when setting 802-1x.password-raw (rh #1456362)
- po: update translations (rh #1382625)

* Fri May 19 2017 Thomas Haller <thaller@redhat.com> - 1:1.8.0-3
- dhcp: don't add route to DHCP4 server (rh #1448987)
- libnm: fix NUL termination of device's description (rh #1443114)
- libnm, core: ensure valid UTF-8 in device properties (rh #1443114)
- core: fix device's UDI property on D-Bus (rh #1443114)
- ifcfg-rh: omit empty next hop for routes in legacy format (rh #1452648)

* Tue May 16 2017 Thomas Haller <thaller@redhat.com> - 1:1.8.0-2
- core: fix persisting managed state of device (rh #1440171)
- proxy: fix use-after-free (rh #1450459)
- device: don't wrongly delay startup complete waiting for carrier (rh #1450444)

* Wed May 10 2017 Thomas Haller <thaller@redhat.com> - 1:1.8.0-1
- Update to upstream release 1.8.0
- device: support dummy devices (rh#1398932)
- core: support attaching user-data to connection profiles (rh#1421429)
- core: fix allowing FQDN in dhcp-hostname setting (rh#1443437)
- core: fix configuring firewall while device is activating (rh#1445242)
- core: don't block activation without carrier for IPv6 DAD (rh#1446367)
- tui: force writing master key to ifcfg file when editing connection (rh#1425409)

* Thu Apr 20 2017 Lubomir Rintel <lrintel@redhat.com> - 1:1.8.0-0.4.rc3
- Update to third Release Candidate of NetworkManager 1.8
- device: fix regressions in assuming devices on carryover from initrd (rh #1443878)
- device: add support for SRIOV num_vfs (rh #1398934)
- device: leave device up when setting it as unmanaged by user (rh #1371433)
- core: properly track manager, route manager and default route manager references (rh #1440089)
- route: properly deal with routes with non-empty host parts (rh #1439376)
- vpn: fix a crash on disconnect (rh #1442064)
- cli: fix hang on connection down (rh #1422786)
- cli: fix interactive edit of bond slaves (rh #1440957)
- vpn: fix early error handling on failed activations (rh #1440077)
- core: only persist explicit managed state in device's state file (rh #1440171)

* Thu Apr  6 2017 Lubomir Rintel <lrintel@redhat.com> - 1:1.8.0-0.4.rc2
- Update to second Release Candidate of NetworkManager 1.8
- device: don't update disconnected devices routes after connectivity check (rh #1436978)
- ifcfg-rh: also check BONDING_OPTS to determine the connection type (rh #1434555)
- nmcli: fix nmcli con edit crash (rh #1436993)
- nmcli: fix nmcli con down (rh #1436990)

* Tue Mar 28 2017 Lubomir Rintel <lrintel@redhat.com> - 1:1.8.0-0.4.rc1
- Update to first Release Candidate of NetworkManager 1.8
- nmcli: speedup with large numbers of VLANs (rh #1231526)
- dns: avoid cleaning resolv.conf on exit if not needed (rh #1344303, rh #1426748)
- device: bond: implement connection reapply (rh #1348198)
- platform: add support for some route options (rh #1373698)
- core: add mtu property to cdma and gsm settings (rh #1388613)
- nmcli: fix output in terse mode (rh #1391170)
- improve handling of unmanaged/assumed devices (rh #1394579)
- policy: make DHCP hostname behaviour configurable (rh #1405275)
- manager: ensure proper disposal of unrealized devices (rh #1433303)
- nmcli: fix connection down (rh #1433883)
- libnm-glib: fix memory leak (rh #1433912)
- device: deal with non-existing IP settings in get_ip_config_may_fail() (rh #1436601)
- nmcli: make --ask and --show-secrets global options (rh #1351263)
- nmcli: improve error handling (rh #1394334)
- device: apply a loose IPv4 rp_filter when it would interfere with multihoming (rh #1394344)
- core: make connectivity checking per-device (rh #1394345)
- manager: sort slaves to be autoconnected by device name (rh #1420708)
- policy: add support to configurable hostname mode (rh #1422610)
- team: support the ethernet.cloned-mac-address property (rh #1424641)
- ifcfg-rh: fix reading team slave types of vlan type (rh #1427482)
- default-route-manager: alyways force a sync of the default route (rh #1431268)
- device: fail DHCPv6 if a link-local address is not present (rh #1432251)

* Mon Mar  6 2017 Thomas Haller <thaller@redhat.com> - 1:1.8.0-0.3.git20170215.1d40c5f4
- Revert default behavior for clone-mac-address to permanent (rh #1413312)

* Wed Feb 15 2017 Francesco Giudici <fgiudici@redhat.com> - 1:1.8.0-0.2.git20170215.1d40c5f4
- Update to a 1.7.1 snapshot:
- rebase NetworkManger package to new upstream 1.8.x version (rh #1414103)
- device: introduce support to ipv6.method=shared (rh #1256822)
- device: add support to vlan on virtual devices (rh #1312359)
- core/supplicant: introduce support to MACsec connections (rh #1337997)
- core: allow enforcing of 802-3 link properties (rh #1353612)
- manager: allow a slave connection which has slaves to autoactivate them (rh #1360386)
- cli: check the active-connection state to detect activation failure (rh #1367752, rh #1384937)
- cli: remove the separate thread when in editor mode to fix races (rh #1368353)
- ifcfg-rh: write the master device name even if the master property is an UUID (rh #1369008)
- ifcfg-rh: higly improved parsing of ifcfg files (rh #1369380)
- checkpoint: improved the checkpoint/rollback functionality (rh #1369716)
- core: core: don't unmanage devices on shutdown (rh #1371126, rh #1378418)
- cli: properly set multiple addresses in questionnaire mode (rh #1380165)
- manager: keep scheduling connectivity check if there is a default active connection (rh #1386106)
- device: allow custom MAC address on bond and bridge interfaces (rh #1386872)
- core: avoid race reading permanent MAC address before udev initialized (rh #1388286)
- ifcfg-rh: fix import of 802.1x connections with empty EAP-TLS identity (rh #1391477)
- libnm-core: remove INFERRABLE flag from dhcp-hostname property (rh #1393997)
- platform: preserve the order when multiple ip addresses are present (rh #1394500)
- device: avoid a crash when both IPv4 and IPv6 configurations fail (rh #1404148)
- dns: export dns state to DBUS (rh #1404594)
- ppp: moved PPP support into a separate package (rh #1404598)
- dns: don't apply DNS configuration coming from non-active devices (rh #1405431)
- vlan: inherit default MTU from parent device (rh #1414186)
- bond: fix crash when reading from sysfs 'NULL' (rh #1420244)
- build: rebuild with correct hardening flags (rh #1420771)
- platform: downgrade warning about failure to detect kernel support to debug (rh #1421019)
- dns: change behavior for "rc-manager=symlink" to preserve "/etc/resolv.conf" as file (rh #1367551)
- libnm: order the property updates (rh #1417292)

* Mon Jan 16 2017 Lubomir Rintel <lrintel@redhat.com> - 1:1.4.0-13.3
- ifcfg-rh: write the master device name even if the master property is an UUID (rh#1369091)

* Tue Dec 13 2016 Thomas Haller <thaller@redhat.com> - 1:1.4.0-13.1
- core: avoid race reading permanent MAC address before udev initialized (rh#1388286)

* Wed Nov  2 2016 Thomas Haller <thaller@redhat.com> - 1:1.4.0-13
- core: don't unmanage devices on shutdown (rh#1371126)

* Mon Sep 26 2016 Lubomir Rintel <lrintel@redhat.com> - 1:1.4.0-12
- device: consider a device with slaves configured (rh#1333983)

* Fri Sep 23 2016 Thomas Haller <thaller@redhat.com> - 1:1.4.0-11
- build: add RPM dependency for exact glib2 version (rh#1378809)

* Thu Sep 22 2016 Thomas Haller <thaller@redhat.com> - 1:1.4.0-10
- device: improve connection matching for assuming bond and infiniband (rh#1375558)

* Thu Sep 15 2016 Beniamino Galvani <bgalvani@redhat.com> - 1:1.4.0-9
- clients: handle secret requests only for current connection (rh#1351272)
- device: fix crash reapplying connection to slave devices (rh#1376784)
- cli: fix autocompletion after ifname (rh#1375933)

* Tue Sep 13 2016 Thomas Haller <thaller@redhat.com> - 1:1.4.0-8
- libnm: fix crash in nm_vpn_plugin_info_list_get_service_types() (rh#1374526)
- device: wait for MAC address change before setting up interface (rh#1371623, rh#1374023)

* Thu Sep  8 2016 Thomas Haller <thaller@redhat.com> - 1:1.4.0-7
- wifi: another fix activation failure due to error changing MAC address (rh#1371623, rh#1374023)
- dhcp: fix race condition that may cause lost lease events and DHCP timeouts (rh#1373276)

* Tue Sep  6 2016 Lubomir Rintel <lrintel@redhat.com> - 1:1.4.0-6
- po: add translations (rh#1276476)

* Tue Sep  6 2016 Thomas Haller <thaller@redhat.com> - 1:1.4.0-5
- libnm,nmtui: fix handling empty cloned-mac-address property (rh#1372799)
- ibft: grant required CAP_SYS_ADMIN capabilities (rh#1371201)

* Fri Sep  2 2016 Thomas Haller <thaller@redhat.com> - 1:1.4.0-4
- core: really fix wrong source interface for PropertiesChanged D-Bus signal (rh#1371920)

* Wed Aug 31 2016 Thomas Haller <thaller@redhat.com> - 1:1.4.0-3
- wifi: fix activation failure due to error changing MAC address (rh#1371623)
- core: fix wrong source interface for PropertiesChanged D-Bus signal (rh#1371920)
- team: restore validation of JSON configuration (rh#1371967)
- device: manage firewall zone for assumed persistent connections (rh#1366288)
- device: don't let external changes cause a release of the slave (rh#1357738)

* Tue Aug 30 2016 Thomas Haller <thaller@redhat.com> - 1:1.4.0-2
- ifcfg-rh: clear IP settings for slave connections (rh#1368761)
- ifcfg-rh: accept TEAM connections also without DEVICETYPE setting (rh#1367180)

* Wed Aug 24 2016 Lubomir Rintel <lrintel@redhat.com> - 1:1.4.0-1
- Update to 1.4.0 release
- cli: show username when interactively connecting to a wireless network (rh #1351272)
- ifcfg-rh: ensure master is cleared when updating a connection (rh #1355656)
- policy: always try to update kernel hostname (rh #1362542)
- cli: return sane error message for D-Bus policy permission errors (rh #1362542)
- device: don't flush addresses when unmanaging assumed devices (rh #1364393)
- team: be more tolerant when handling invalid or empty configuration (rh #1366300)
- act-request: queue failing the slave when master fails (rh #1367702)
- vpn: fix ipv6 configuration of VPNs without a separate interface (rh #1368354)
- vpn: properly discard routes with invalid prefix length (rh #1368355)

* Thu Aug 18 2016 Thomas Haller <thaller@redhat.com> - 1:1.4.0-0.6.beta1
- logging: default to syslog (rh #1358335)

* Tue Aug  9 2016 Beniamino Galvani <bgalvani@redhat.com> - 1:1.4.0-0.5.beta1
- Update to 1.4-beta1 release
- core: fix setting hostname from DHCP (rh #1356015)
- vlan: honor the REORDER_HDR flag (rh #1312281)
- device: apply MTU setting also to devices without IPv4 configuration (rh #1364275)
- bond: improved connection matching (rh #1304641)
- team: check return value of g_dbus_connection_call_sync() (rh #1349749)

* Wed Jul 27 2016 Lubomir Rintel <lrintel@redhat.com> - 1:1.4.0-0.4.git20160727.9446481f
- Rebuild for fixed documentation directory in redhat-rpm-macros

* Wed Jul 27 2016 Lubomir Rintel <lrintel@redhat.com> - 1:1.4.0-0.3.git20160727.9446481f
- Update to a more recent 1.4.0 snapshot:
- bond: fix defaults and be more liberal in accepting different formats of option values (rh #1352131)
- bond: fix setting of "lp_interval" option (rh #1348573)
- device: don't try to generate ipv6ll address for disconnected devices (rh #1351633)
- device: make sure we update system hostname when DHCP configuration changes (rh #1356015)
- device: tune down warning about failure to set userspace IPv6LL on non-existing device (rh #1323571)
- nmcli: add "nmcli device modify" subcommand to do runtime configuration changes (rh #998000)
- nmcli: crash on connection delete/down timeout (rh $1355740)
- nmcli: fix 8021x settings tab-completion (rh #1301226)
- secrets: increase timeout for getting the secrets from the agent (rh #1349740)
- team: keep device config property up to date with actual configuration (rh #1310435)
- team: make synchronization with teamd more robust (rh #1257237)
- vpn: don't merge DNS properties into parent device's configuration (rh #1348901)

* Fri Jul 08 2016 Lubomir Rintel <lrintel@redhat.com> - 1:1.4.0-0.3.git20160621.072358da
- Do not regenerate gtk-doc. Together with parallel make it may cause multilib conflicts

* Wed Jun 22 2016 Beniamino Galvani <bgalvani@redhat.com> - 1:1.4.0-0.2.git20160621.072358da
- enable JSON validation configure option
- Update to a more recent 1.3.0 snapshot:
- team: check return value of g_dbus_connection_call_sync() (rh #1347015)

* Mon Jun 06 2016 Beniamino Galvani <bgalvani@redhat.com> - 1:1.4.0-0.1.git20160606.b769b4df
- Update to a 1.3.0 snapshot:
- cli: hide secret certificate blobs unless --show-secrets set (rh #1184530)
- dns: add support for specifying dns priorities (rh #1228707)
- core: wait for IPv6 DAD before completing activation (rh #1243958)
- device: take care of default route of DHCP generated-assumed connections (rh #1265239)
- team: improve matching of team connection upon service restart (rh #1294728)
- device: apply MTU setting also to devices without IPv4 configuration (rh #1303968)
- device: reconfigure IP addressing after bringing up device (rh #1309899)
- team: expose current device configuration through D-Bus and nmcli (rh #1310435)
- systemd: add "After=dbus.service" to NetworkManager.service (rh #1311988)
- cli: handle device failure when activating (rh #1312726)
- core,libnm: remove gateway from connection if never-default is set (rh #1313091)
- platform: remove padding for IP address lifetimes (rh #1318945)
- manager: run dispatcher scripts on suspend/sleep (rh #1330694)
- device: remove pending dhcp actions also in IP_DONE state (rh #1330893)
- wwan: fixed multiple crashes (rh #1331395)
- nmcli: fix tab completion for libreswan import (rh #1337300)

* Wed Jun 01 2016 Thomas Haller <thaller@redhat.com> - 1:1.2.0-2
- write /etc/resolv.conf as file by default instead of symlink (rh#1337222)
- rename package config-routing-rules to dispatcher-routing-rules (rh #1334876)

* Wed Apr 27 2016 Lubomir Rintel <lrintel@redhat.com> - 1:1.2.0-1
- Update to NetworkManager 1.2.0 release
- vlan: keep the hardware address synchronized with parent device (rh #1325752)
- bond: add more options (rh #1299103)

* Tue Mar 29 2016 Lubomir Rintel <lrintel@redhat.com> - 1:1.2.0-0.1.beta3
- Update to a more recent 1.2.0 snapshot

* Sat Mar 05 2016 Lubomir Rintel <lrintel@redhat.com> - 1:1.2.0-0.1.beta2
- Update to a 1.2.0 snapshot:
- core: add a connection defaults section to NetworkManager.conf (rh #1164677)
- dhcp: make timeout configurable (rh #1262922)
- pppoe: set the firewall zone on the correct ip interface (rh #1110465)
- device: properly roll back the device activation attempt on failure (rh #1270814)
- nmcli: add monitor command (rh #1034158)
- nmcli: fix shell completion of bluetooth device names (rh #1271271)
- ipv4: add an option to send full FQDN in DHCP requests (rh #1255507)
- core: fix a use-after-free() when activating a secondary VPN connection (rh #1277247)
- wifi: fix bssid cache updating (rh #1094298)
- vlan: honor the reorder-header flag (rh #1250225)
- ipv4: do a duplicate address detection (rh #1259063)
- core: add LLDP listener to the daemon and utilities (rh #1142898)
- vpn: don't fail activation when plugin supports interactive mode, but the VPN daemon does not (rh #1298732)
- ipv6: readd the address when the MAC address changes (rh #1286105)
- core: avoid generating excessively long names for virtual devices (rh #1300755)
- nmcli: add connection import and export (rh #1034105)
- vlan: fix matching of connections on assumption (rh #1276343)
- core: fix matching of static route metrics on connection assumption (rh #1302532)
- core: work around broken device drivers (AWS ENI) that initially have zero MAC address (rh #1288110)
- infiniband: set the link down when changing mode, some drivers need that (rh #1281301)
- infiniband: retry autoactivation of partitions when parent device changes (rh #1275875)

* Tue Feb 16 2016 Thomas Haller <thaller@redhat.com> - 1:1.0.6-28
- wifi: fix crash due to missing BSSID (rh #1276426)

* Mon Oct 26 2015 Thomas Haller <thaller@redhat.com> - 1:1.0.6-27
- build: update vala-tools build requirement (rh #1274000)

* Sat Oct 24 2015 Jiří Klimeš <jklimes@redhat.com> - 1:1.0.6-26
- wifi: emit NEW_BSS on ScanDone to update APs in Wi-Fi device (rh #1267327)

* Fri Oct 23 2015 Lubomir Rintel <lrintel@redhat.com> - 1:1.0.6-25
- vpn: cancel the secrets request on agent timeout (rh #1272023)
- vpn: cancel the connect timer when vpn reconnects (rh #1272023)

* Wed Oct 21 2015 Jiří Klimeš <jklimes@redhat.com> - 1:1.0.6-24
- device: fix problem in not managing software devices (rh #1273879)

* Tue Oct 20 2015 Beniamino Galvani <bgalvani@redhat.com> - 1:1.0.6-23
- wake-on-lan: ignore by default existing settings (rh #1270194)

* Mon Oct 19 2015 Thomas Haller <thaller@redhat.com> - 1:1.0.6-22
- platform: fix detection of s390 CTC device (rh #1272974)
- core: fix queuing activation while waiting for carrier (rh #1079353)

* Mon Oct 12 2015 Thomas Haller <thaller@redhat.com> - 1:1.0.6-21
- core: fix invalid assertion in nm_clear_g_signal_handler() (rh #1183444)

* Mon Oct 12 2015 Thomas Haller <thaller@redhat.com> - 1:1.0.6-20
- rebuild package

* Fri Oct  9 2015 Thomas Haller <thaller@redhat.com> - 1:1.0.6-19
- device: fix race wrongly managing external-down device (2) (rh #1269199)

* Fri Oct  9 2015 Beniamino Galvani <bgalvani@redhat.com> - 1:1.0.6-18
- device/vlan: update VLAN MAC address when parent's one changes

* Thu Oct  8 2015 Thomas Haller <thaller@redhat.com> - 1:1.0.6-17
- dhcp6: destroy the lease when destroying a client (rh #1260727)
- device: fix race wrongly managing external-down device (rh #1269199)

* Wed Oct  7 2015 Lubomir Rintel <lrintel@redhat.com> - 1:1.0.6-16
- device: silence spurious errors about activation schedule (rh #1269520)

* Tue Oct  6 2015 Thomas Haller <thaller@redhat.com> - 1:1.0.6-15
- core: really fix enslaving team device to bridge (rh #1183444)

* Wed Sep 30 2015 Thomas Haller <thaller@redhat.com> - 1:1.0.6-14
- platform: updating link cache when moving link to other netns (rh #1264361)
- nmtui: fix possible crash during secret request (rh #1267672)
- vpn: increase the plugin inactivity quit timer (rh #1268030)
- core: fix enslaving team device to bridge (rh #1183444)

* Tue Sep 29 2015 Lubomir Rintel <lrintel@redhat.com> - 1:1.0.6-13
- vpn-connection: set the MTU for the VPN IP interface (rh #1267004)
- modem-broadband: update modem's supported-ip-families (rh #1263959)
- wifi: fix a crash in on_bss_proxy_acquired() (rh #1267462)

* Fri Sep 25 2015 Dan Williams <dcbw@redhat.com> - 1:1.0.6-12
- core: increase IPv6LL DAD timeout to 15 seconds (rh #1101809)

* Thu Sep 24 2015 Thomas Haller <thaller@redhat.com> - 1:1.0.6-11
- platform: better handle devices without permanent address (rh #1264024)

* Thu Sep 24 2015 Thomas Haller <thaller@redhat.com> - 1:1.0.6-10
- dhcp: fix crash in internal DHCP client (rh #1260727)

* Tue Sep 22 2015 Jiří Klimeš <jklimes@redhat.com> - 1:1.0.6-9
- build: fix installing language files (rh #1265117)

* Mon Sep 21 2015 Jiří Klimeš <jklimes@redhat.com> - 1:1.0.6-8
- nmcli: allow creating ADSL connections with 'nmcli connection add' (rh #1264089)

* Thu Sep 17 2015 Jiří Klimeš <jklimes@redhat.com> - 1:1.0.6-7
- ifcfg-rh: ignore GATEWAY from network file for DHCP connections (rh #1262972)

* Wed Sep 16 2015 Beniamino Galvani <bgalvani@redhat.com> - 1:1.0.6-6
- device: retry DHCP after timeout/expiration for assumed connections (rh #1246496)
- device: retry creation of default connection after link is initialized (rh #1254089)

* Mon Sep 14 2015 Thomas Haller <thaller@redhat.com> - 1:1.0.6-5
- config: add code comments to NetworkManager.conf file
- iface-helper: enabled slaac/dhcp4 based on connection setting only (rh #1260243)
- utils: avoid generation of duplicated assumed connection for veth devices (rh #1256430)
- nmcli: improve handling of wake-on-lan property (rh #1260584)

* Wed Sep  9 2015 Thomas Haller <thaller@redhat.com> - 1:1.0.6-4
- config: fix config-changed signal for s390x and ppc64 archs (rh #1062301)
- device: fix handling ignore-auto-dns for IPv6 nameservers (rh #1261428)

* Tue Sep  8 2015 Lubomir Rintel <lrintel@redhat.com> - 1:1.0.6-3
- vpn: fix the tunelled VPN setup (rh #1238840)

* Sat Aug 29 2015 Lubomir Rintel <lrintel@redhat.com> - 1:1.0.6-2
- nmcli: fix argument parsing for config subcommand

* Thu Aug 27 2015 Lubomir Rintel <lrintel@redhat.com> - 1:1.0.6-1
- Align with the upstream 1.0.6 release:
- device: add support for configuring Wake-On-Lan (rh #1141417)
- device: don't disconnect after DHCP failure when there's static addresses  (rh #1168388)
- device: provide information about metered connections (rh #1200452)
- device: fix an assert fail when cleaning up a slave connection (rh #1243371)
- team: add support for setting MTU (rh #1255927)
- config: avoid premature exit with configure-and-quit option (rh #1256772)

* Fri Aug 21 2015 Jiří Klimeš <jklimes@redhat.com> - 1:1.0.4-10
- supplicant: fix passing freq_list option to wpa_supplicant (rh #1254461)

* Wed Aug 19 2015 Thomas Haller <thaller@redhat.com> - 1:1.0.4-9
- udev: fix call to ethtool in udev rules (rh #1247156)

* Tue Aug 18 2015 Beniamino Galvani <bgalvani@redhat.com> - 1:1.0.4-8
- device: accept multiple addresses in a DHCPv6 lease (rh #1244293)

* Fri Aug 14 2015 Lubomir Rintel <lrintel@redhat.com> - 1:1.0.4-7
- device: fix a crash when unconfiguring a device (rh #1253744)

* Wed Aug 12 2015 Jiří Klimeš <jklimes@redhat.com> - 1:1.0.4-6
- ifcfg-rh: respect DEVTIMEOUT if link is not announced by udev yet (rh #1192633)

* Tue Aug  4 2015 Thomas Haller <thaller@redhat.com> - 1:1.0.4-5
- core: avoid ethtool to autoload kernel module (rh #1247156)

* Tue Aug  4 2015 Lubomir Rintel <lrintel@redhat.com> - 1:1.0.4-4
- device: fix setting of a MTU (rh #1250019)

* Wed Jul 22 2015 Lubomir Rintel <lrintel@redhat.com> - 1:1.0.4-3
- daemon,libnm: fix handling of default routes for assumed connections (rh #1245648)

* Fri Jul 17 2015 Jiří Klimeš <jklimes@redhat.com> - 1:1.0.4-2
- cli: fix verifying flag-based properties (rh #1244048)

* Tue Jul 14 2015 Lubomir Rintel <lrintel@redhat.com> - 1:1.0.4-1
- Align with the upstream 1.0.4 release
- Fix the libreswan plugin (rh #1238840)

* Tue Jul 14 2015 Jiří Klimeš <jklimes@redhat.com> - 1:1.0.4-0.2.git20150713.38bf2cb0
- vpn: send firewall zone to firewalld also for VPN connections (rh #1238124)

* Mon Jul 13 2015 Lubomir Rintel <lrintel@redhat.com> - 1:1.0.4-0.1.git20150713.38bf2cb0
- Update to a bit newer 1.0.4 git snapshot, to fix test failures
- device: restart ping process when it exits with an error (rh #1128581)

* Wed Jul  1 2015 Thomas Haller <thaller@redhat.com> - 1:1.0.3-2.git20150624.f245b49a
- config: allow rewriting resolv.conf on SIGUSR1 (rh #1062301)

* Wed Jun 24 2015 Lubomir Rintel <lrintel@redhat.com> - 1:1.0.3-1.git20150624.f245b49a
- Update to a bit newer 1.0.4 git snapshot, to fix test failures

* Mon Jun 22 2015 Lubomir Rintel <lrintel@redhat.com> - 1:1.0.3-1.git20150622.9c83d18d
- Update to a 1.0.4 git snapshot:
- bond: add support for setting a MTU (rh #1177860)
- core: delay initialization of the connection for devices without carrier at startup (rh #1079353)
- route-manager: ensure the routes are set up properly with multiple interface in the same subnet (rh #1164441)
- config: add support for reloading configuration (rh #1062301)
- device: disallow ipv6.method=shared connections early during activation (rh #1183015)
- device: don't save the newly added connection for a device until activation succeeds (rh #1174164)
- rdisc: prevent solicitation loop for expiring DNS information (rh #1207730)
- wifi: Indicate support of wireless radio bands (rh #1200451)
- nmcli: Fix client hang upon multiple deletion attempts of the same connection (rh #1168657)
- nmcli: Fix documentation for specifying a certificate path (rh #1182575)
- device: add support for auto-connecting slave connection when activating a master (rh #1158529)
- nmtui: Fix a crash when attempting an activation with no connection present (rh #1197203)
- nmcli: Add auto-completion and hints for valid values in enumeration properties (rh #1034126)
- core: load the the libnl library from the correct location (rh #1211859)
- config: avoid duplicate connection UUIDs (rh #1171751)
- device: enable IPv6 privacy extensions by default (rh #1187525)
- device: fix handling if DHCP hostname for configure-and-quit (rh #1201497)
- manager: reuse the device connection is active on when reactivating it (rh #1182085)
- device: reject incorrect MTU settings from an IPv6 RA (rh #1194007)
- default-route: allow preventing the connection to override externally configured default route (rh #1205405)
- manager: reduce logging for interface activation (rh #1212196)
- device: don't assume a connection for interfaces that only have an IPv6 link-local address (rh #1138426)
- device: reject hop limits that are too low (CVE-2015-2924) (rh #1217090)

* Wed Apr 29 2015 Beniamino Galvani <bgalvani@redhat.com> - 1:1.0.0-17.git20150121.b4ea599c
- dhclient: use fqdn.fqdn for server DDNS updates (rh #1212597)

* Wed Apr 15 2015 Dan Williams <dcbw@redhat.com> - 1:1.0.0-16.git20150121.b4ea599c
- core: use dev_id when calculating interface IID (rh #1101809)

* Fri Mar 27 2015 Dan Williams <dcbw@redhat.com> - 1:1.0.0-15.git20150121.b4ea599c
- core: respawn teamd instead of failing when it exits unexpectedly (rh #1145988)

* Thu Jan 29 2015 Dan Winship <danw@redhat.com> - 1:1.0.0-14.git20150121.b4ea599c
- dispatcher: split routing rules script into a subpackage (rh #1160013)

* Wed Jan 28 2015 Dan Williams <dcbw@redhat.com> - 1:1.0.0-13.git20150121.b4ea599c
- core: remove IPv6LL address when deactivating managed devices (rh #1184997)
- core: recognize external IP config earlier on startup
- core: fix bridge default metric

* Wed Jan 28 2015 Dan Winship <danw@redhat.com> - 1:1.0.0-12.git20150121.b4ea599c
- dispatcher: fix policy-based-routing script to run on "down" as well (rh #1160013)

* Tue Jan 27 2015 Jiří Klimeš <jklimes@redhat.com> - 1:1.0.0-11.git20150121.b4ea599c
- build: really install dispatcher script to support policy based routing (rh #1160013)

* Thu Jan 22 2015 Dan Winship <danw@redhat.com> - 1:1.0.0-10.git20150121.b4ea599c
- team: fix bug in team device activation (rh #1184923)

* Wed Jan 21 2015 Dan Williams <dcbw@redhat.com> - 1:1.0.0-9.git20150121.b4ea599c
- build: fix NetworkManager-libnm and old NetworkManager-glib conflict (rh #1066690)
- core: accept numeric bond options (rh #1171009) (rh #1133544)
- core/libnm: better validate setting properties (rh #1182567)
- core: add dispatcher script to support policy based routing (rh #1160013)

* Thu Jan 15 2015 Jiří Klimeš <jklimes@redhat.com> - 1:1.0.0-8.git20150107.1ea95cd3
- ifcfg-rh: read custom IP address for shared connections (rh #1174632)

* Tue Jan 13 2015 Thomas Haller <thaller@redhat.com> - 1:1.0.0-7.git20150107.1ea95cd3
- platform: fix handling of routes with special metric (rh #1172780)
- ifcfg-rh: add reading and writing of route-metric property

* Tue Jan 13 2015 Lubomir Rintel <lrintel@redhat.com> - 1:1.0.0-6.git20150107.1ea95cd3
- platform: fix draining of the event queue with old libnl (rh #1180773)

* Fri Jan  9 2015 Dan Williams <dcbw@redhat.com> - 1:1.0.0-5.git20150107.1ea95cd3
- build: remove -bluetooth and -wwan Requires to prevent unwanted updates (rh #1066690)
- build: remove erroneous libnm/libnm-devel dependencies

* Fri Jan  9 2015 Dan Winship <danw@redhat.com> - 1:1.0.0-4.git20150107.1ea95cd3
- build: fix NetworkManager-bluetooth dep on NetworkManager-wwan

* Fri Jan  9 2015 Dan Winship <danw@redhat.com> - 1:1.0.0-3.git20150107.1ea95cd3
- ifcfg-rh: handle DEVTIMEOUT property (rh #1171917)

* Thu Jan 08 2015 Dan Williams <dcbw@redhat.com> - 1:1.0.0-2.git20150107.1ea95cd3
- core: re-enable hardware plugins on s390 (rh #1066690)

* Wed Jan 07 2015 Dan Williams <dcbw@redhat.com> - 1:1.0.0-1.git20150107.1ea95cd3
- Update to 1.0 release
- core: split device support into sub-packages (rh #1066690)
- core: don't touch externally created software interfaces until IFF_UP (rh #1030947)
- tui: fix handling of "Available to all users" checkbox (rh #1176042)

* Fri Dec 12 2014 Dan Williams <dcbw@redhat.com> - 1:0.995.0.0-1
- core: fix DHCP lease expiry/nak during lease acquisition
- core: don't step on external team interfaces when teamd appears

* Thu Dec 11 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.11.0-10.git20141211.9337a13a
- core: fix managed slave attachment

* Thu Dec 11 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.11.0-9.git20141211.da4a98bf
- core: recognize layer-2 connections (rh #1141266)
- core: don't tear down assumed connections that fail (rh #1141264)
- core: clean up IP operations when restarting them after re-authentication
- core: fix some VPN issues with secrets and routing
- core: fix regression parsing gateway from addresses (rh #1170199)
- core: don't release slaves on exit (rh #1169936)
- tui: fix deletion of slaves with master (rh #1131574)
- cli: fix regression deactivating multiple connections (rh #1168383)

* Thu Dec  4 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.11.0-8.git20141125.f32075d2
- core: don't bounce disable_ipv6 when assuming connections (rh #1170530)

* Fri Nov 28 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.11.0-7.git20141125.f32075d2
- device: fix crash on S390(x) when setting subchannels (rh #1168764)

* Tue Nov 25 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.11.0-6.git20141125.f32075d2
- tui: fix missing IPv4/IPv6 method popup (rh #1167710)
- core: inherit parent managed state for VLAN devices (rh #1114681)

* Tue Nov 18 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.11.0-5.git20141118.646f335d
- cli: fix showing secrets when editing connections
- cli: ignore timestamp when comparing connections (rh #1122995)
- core: fix a few issues with the internal DHCP client (rh #1066700)

* Fri Nov 14 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.11.0-4.git20141114.669f74b8
- core: wait for IPv6LL address before starting DHCPv6-only configurations
- core: fix race with kernel IPv6LL when deactiving connections that ignored IPv6
- cli: fix waiting for activation success/failure
- core: silence warning about bad ifindex for non-netdev devices
- core: fix default route ordering issues
- core: don't change firewall zone for assumed devices (rh #1098281)
- libnm: fix translations in clients and non-UTF-8 encodings
- tui: fix unsetting the gateway (rh #1163896)
- cli/tui: only handle secrets for connection being activated

* Mon Nov 10 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.11.0-3.git20141110.gitb75dfc62
- core: fix DHCP PID and platform route loop issues
- cli: fix timeout disconnecting device

* Fri Nov  7 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.11.0-2.git20141107.git14537c71
- core: add fast, lightweight internal DHCP client (rh #1066700)
- rpm: specfile cleanups

* Fri Nov  7 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.11.0-1.git20141107.git289f7881
- core: DHCP address lifetime expires before it can be updated (rh #1139326)
- core: apply static IPv6 configuration while waiting for an RA (rh #1101809)
- core: fix activation of IP configurations on unmanaged interfaces (rh #1067299)
- core: serialize dispatcher state changes (rh #1061212)
- core: increased dispatcher timeout and blocking events (rh #1048345)
- core: add support for "lacp_rate" bonding option (rh #1061702)
- core: better handle slave state changes done externally (rh #1066706)
- core: fix checking whether NM is running for root clients (rh #1096772)
- ifcfg-rh: ignore tailing spaces (rh #1100336)
- cli: fix warning setting DCB application priority (rh #1080510)
- tui: fix inverted 'Require IPvX addressing' checkbox (rh #1108839)
- tui: fix entry of some IP address formats (rh #1090422)
- tui: fix disabled <Add> button in IP configuration (rh #1131434)

* Fri Oct 17 2014 Florian Müllner <fmuellner@redhat.com> - 1:0.9.9.1-47.git20140326
- remote-settings: Fix asynchronous initialization when using private bus

* Fri Oct 10 2014 Lubomir Rintel <lrintel@redhat.com> - 1:0.9.9.1-46.git20140326
- tui: Fix up bond primary option validation (rh #1142864)

* Fri Oct 10 2014 Lubomir Rintel <lrintel@redhat.com> - 1:0.9.9.1-45.git20140326
- bluetooth: don't consider bnep devices separate from the BT devices (rh #1147700)

* Wed Oct  8 2014 Dan Winship <danw@redhat.com> - 1:0.9.9.1-44.git20140326
- tui: fix master/slave deletion issues (rh #1131574)

* Wed Oct 08 2014 Lubomir Rintel <lrintel@redhat.com> - 1:0.9.9.1-43.git20140326
- bluetooth: fix connection timeouts (rh #1147700)

* Fri Sep 26 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.9.1-42.git20140326
- core: do not clear existing secrets on Update() without secrets (rh #1080628)

* Tue Sep 23 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.9.1-41.git20140326
- tui: require non-empty primary option for active-backup bonding mode (rh #1142864)

* Mon Sep 22 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.9.1-40.git20140326
- cli: create a connection if none exist in 'nmcli dev connect' (rh #1113941)

* Mon Sep 22 2014 Lubomir Rintel <lrintel@redhat.com> - 1:0.9.9.1-39.git20140326
- platform: Increase NL buffer size for systems with a lot of interfaces (rh #1141256)
- tui: Remove primary option if bond mode is not active-backup (rh #1142864)

* Wed Sep 17 2014 Dan Winship <danw@redhat.com> - 1:0.9.9.1-38.git20140326
- tui: fix password handling (rh #1133967)
- tui: save LEAP username correctly (rh #1133967)
- tui: fix a crash when dismissing password dialog (rh #1132612)

* Wed Sep 17 2014 Lubomir Rintel <lrintel@redhat.com> - 1:0.9.9.1-37.git20140326
- platform: fix setting preferred time for address (rh #1083283)

* Tue Sep 16 2014 Dan Winship <danw@redhat.com> - 1:0.9.9.1-36.git20140326
- tui: add support for editing DSL connections (rh #1105753)

* Fri Sep 12 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.9.1-35.git20140326
- core: don't generate a connection for unmanaged devices (rh #1136843)
- bluetooth: don't crash when switching off bluetooth (rh #1136387)
- dhcp: fix dhclient abnormal exit due to SIGPIPE (rh #1136836)

* Thu Sep 11 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.1-34.git20140326
- core: allow IPv6 configuration of interfaces when inactive (rh #1083133) (rh #1098319)

* Fri Sep  5 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.9.1-33.git20140326
- cli: fix nmcli connection add (rh #1138303)

* Thu Sep 04 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.1-32.git20140326
- core, ifcfg-rh, ibft: add support for iBFT VLAN connections (rh #990480)

* Thu Aug 21 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.9.1-31.git20140326
- core, cli: D-Bus Delete() call; 'nmcli device delete <ifname>' for SW devices (rh #1034150)
- cli: use readline library throughout nmcli when asking for input (rh #1007365)

* Wed Aug 20 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.9.1-30.git20140326
- ifcfg-rh: fix a crash on setting hostname with SELinux disabled (rh #1122826)
- cli: fix 'nmcli device wifi' crash with multiple wifi devices (rh #1131042)
- policy: don't use default (localhost) hostname as configured hostname (rh #1110436)
- ifcfg-rh: write GATEWAY instead of GATEWAY0 to be ifup-compatible (rh #1105770)
- libnm-util, cli: make explicit that we only allow VPN as secondaries (rh #1094296)

* Wed Jul 30 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.1-29.git20140326
- build: fix issues with multilib upgrades (rh #1112367)

* Fri Jul 25 2014 Dan Winship <danw@redhat.com> - 1:0.9.9.1-28.git20140326
- core: better PPPoE connection termination handling (rh #1061641)

* Tue Jul 15 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.1-27.git20140326
- core: update translations (rh #1046891)

* Mon Jul  7 2014 Thomas Haller <thaller@redhat.com> - 1:0.9.9.1-26.git20140326
- core: fix crash when calling DBUS function GetConnectionByUuid() (rh #1113508)

* Tue Jul  1 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.9.1-25.git20140326
- core: fix MTU handling while merging/subtracting IP configs (rh #1093231)

* Mon Jun 23 2014 Thomas Haller <thaller@redhat.com> - 1:0.9.9.1-24.git20140326
- core: fix crash on failure of reading bridge sysctl values (rh #1112020)

* Thu Jun 12 2014 Thomas Haller <thaller@redhat.com> - 1:0.9.9.1-23.git20140326
- core: fix crash on device removal with active connection (rh #1108167)

* Wed Jun  4 2014 Thomas Haller <thaller@redhat.com> - 1:0.9.9.1-22.git20140326
- core: fix ZONE_CONFLICT error when setting firewall zone (rh #1103782)

* Tue Jun  3 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.9.1-21.git20140326
- tui: fix a crash when editing IPv6 routes (rh #1103702)
- tui: fix setting Cloned MAC address

* Mon Jun  2 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.9.1-20.git20140326
- tui: fix a crash when editing IPv6 addresses (rh #1103702)

* Fri May 30 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.9.1-19.git20140326
- core: allow matching IPv6 'auto' connection to 'ignore' profile (rh #1083196)

* Thu May 29 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.9.1-18.git20140326
- core: sort connections in descending timestamp order on take-over (rh #1067712)

* Thu May 29 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.9.1-17.git20140326
- core: fix connection matching generally and for s390 as well (rh #1083196)
- dhcp: fix DHCPv6 address lifetime handling (rh #1086237)

* Wed May 28 2014 Jiří Klimeš <jklimes@redhat.com> - 1:0.9.9.1-16.git20140326
- cli: allow arbitrary VPN types when creating connections (rh #1100750)

* Thu May 22 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.1-15.git20140326
- Rebuild for Z-stream update

* Mon May 12 2014 Dan Winship <danw@redhat.com> - 1:0.9.9.1-14.git20140326
- core: fix connection matching with IPv6 routes (rh #1086237)
- core: wait with startup-complete for dynamic IPv4 and IPv6 addresses (rh #1096063, rh #1086906)

* Thu May  1 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.1-13.git20140326
- core: ignore IPv6 cache routes to fix initial connection generation (rh #1083153)
- core: ensure slow DHCP emits 'dhcp4-change' and 'dhcp6-change' dispatcher events (rh #1091296)

* Mon Apr  7 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.1-12.git20140326
- core: fix master interface DHCP handling if ignore-carrier is set (rh #1083624)
- core: fix startup state not finishing correctly (rh #1084554)

* Wed Apr  2 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.1-11.git20140326
- core: additional fixes for Data Center Bridging (DCB) (rh #799241) (rh #1081991)
- core: ensure /etc/resolv.conf has the right SELinux label (rh #1070829)

* Thu Mar 27 2014 Dan Winship <danw@redhat.com> - 1:0.9.9.1-10.git20140326
- core: update NMManager:devices before emitting notify::devices (rh #1078720)

* Wed Mar 26 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.1-9.git20140326
- core: fix an issue with alias support touching non-alias address labels (rh #1067170)

* Wed Mar 26 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.1-8.git20140326
- core: fix management of some static configurations from initramfs (rh #1077743)
- ifcfg-rh: add support for alias files (rh #1067170)
- core: additional fixes for Data Center Bridging (DCB) (rh #799241)

* Tue Mar 25 2014 Dan Winship <danw@redhat.com> - 1:0.9.9.1-7.git20140313
- ifcfg-rh: give a better error on "permission denied" (rh #1070617)
- tui: allow cancelling with "Esc" from "nmtui connect" (rh #1080059)

* Fri Mar 21 2014 Dan Winship <danw@redhat.com> - 1:0.9.9.1-6.git20140313
- tui: misc fixes (rh #1078281)

* Fri Mar 21 2014 Dan Winship <danw@redhat.com> - 1:0.9.9.1-5.git20140313
- devices: send ARPs when configuring static IPv4 addresses (rh #1073447)

* Mon Mar 17 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.1-4.git20140313
- core: fix startup auto-activation of slow carrier detect interfaces (rh #1076592)
- core: align default bridge priority with kernel defaults (rh #1073664)

* Thu Mar 13 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.1-3.git20140313
- core: read and assume team port configuration (rh #1035859)
- core: looser IPv6 existing configuration assumption (rh #1073824)
- core: follow network interface renames (rh #907836)
- core: add support for VXLAN interfaces (rh #1066705)
- wifi: fix connections to hidden SSIDs (rh #1069844)
- cli: allow using master connection name when creating slaves (rh #1057494)
- ifcfg-rh: fix reading and writing of Team port configurations (rh #1074160)

* Fri Mar  7 2014 Jiří Klimeš <jklimes@redhat.com> -  1:0.9.9.1-2.git20140228
- core: fix adding gateway route for IPv6 (rh #1072410)
- core: unschedule deletion of sw device when activating request (rh #1073015)
- cli: fix a crash when trying to set a white-space string as IP (rh #1071394)
- core: correctly handle pre-activation dependency failure (rh #1069695)
- libnm-util, libnm-glib: Add master/slave-matching utils (rh #1045203)
- rdisc: set the expiration timer correctly (rh #1073560)
- core,libnm-glib: support 'type', 'id' properties in NMActiveConnection (rh #1061822)
- core: reenable auto activation for slave connections with a matching UUID master
- core: implement function nm_active_connection_get_uuid()
- core: rename function nm_active_connection_get_name() to nm_active_connection_get_id()
- libnm-glib: fix a double free in NMDeviceVlan
- platform: fix converting address flags in nm_platform_ip6_address_to_string()
- core: postpone non-static master IP configuration until carrier
- core: match IPv4 'disabled' method to 'auto' when device has no link
- core: refactor connection matching and add testcase
- policy: fix crash caused by calling functions on connection==NULL

* Tue Mar  4 2014 Dan Winship <danw@redhat.com> - 1:0.9.9.1-1.git20140228
- rdisc: obey rtr_solicitations and rtr_solicitation_interval (rh #1071446)

* Thu Feb 27 2014 Thomas Haller <thaller@redhat.com> - 1:0.9.9.1-0.git20140228
- new snapshot version 0.9.9.1
- cli: show warning when setting band/channel for infrastructure mode wifi (rh #1000096)
- cli: better checking of WEP key types in interactive editor (rh #1040964)
- core: fix crash while wrongly switching device to state NEED_AUTH (rh #1058308)
- core: fix crash during re-activation with pending activation request (rh #1058843)
- cli: support set/appending container types in modify command and interactive editor (rh #1044027)

* Wed Feb 19 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.0-39.git20140131
- core: fix startup tracking (rh #1030583)

* Fri Jan 31 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.0-38.git20140131
- core: fix crash getting secrets in libnm-glib

* Fri Jan 31 2014 Dan Winship <danw@redhat.com> - 1:0.9.9.0-37.git20140131
- dbus: kill at_console usage in permissions (rh #979416)
- policy: allow inactive (remote/SSH) sessions to perform some actions (rh #979416)
- cli: consolidate active and configured connections (rh #997999)
- core/rdisc: add support for IPv6 privacy (rh #1003859)
- core/platform: revise failure to activate connection on error of setting route (rh #1005416)
- core/platform: sort routes before adding them in nm_platform_ipX_route_sync() (rh #1005416)
- vpn: handle missing tunnel interface for IP-based VPNs (rh #1030068)
- core: make NMDeviceTun 'mode' immutable and set at construct time (rh #1034737)
- core/rdisc: add autoconf addresses as /64 (instead of /128) (rh #1044590)
- ifcfg-rh: unescape Team configuration (rh #1051517)
- core: fix a crash with autoconnect masters with autoconnect slaves (rh #1054194)
- libnm-glib: additional functions to get nameservers (rh #1056146)

* Mon Jan 27 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.0-36.git20140127
- core: fix managing IPv6 connections without disruption on startup (rh #1052157)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1:0.9.9.0-35.git20140122
- Mass rebuild 2014-01-24

* Thu Jan 23 2014 Dan Winship <danw@redhat.com> - 1:0.9.9.0-34.git20140122
- core: various fixes to autoconnect retry handling (rh #1029480)

* Wed Jan 22 2014 Dan Winship <danw@redhat.com> - 1:0.9.9.0-33.git20140122
- platform: fix physical_port_id handling (rh #804527)

* Wed Jan 22 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.0-32.git20140122
- core: add host route for DHCPv4 server if outside assigned subnet (rh #983325)
- core: set classful prefix length for DHCPv4 static routes
- core: only request wired 802.1x secrets during initial connection
- cli: fix crash when edited connection removed by another client (rh #1011942)
- cli: add help for second-level commands (rh #1034119)

* Thu Jan 16 2014 Dan Winship <danw@redhat.com> - 1:0.9.9.0-31.git20140108
- tui: various bugfixes (rh #1025021)

* Wed Jan  8 2014 Dan Williams <dcbw@redhat.com> - 1:0.9.9.0-30.git20130108
- core: ignore public-suffix search domains like ".com" or ".net" (#851521)
- core: don't touch virtual devices on suspend/resume (rh #1038158)
- core: fix handling of local nameservers in resolv.conf on startup (rh #1035861)
- core: fix race with 'network' service at boot (rh #1034983)
- core: fix stale information in dispatcher DHCP lease change events
- cli: more compact 'nmcli dev' output format (rh #998003)
- cli: make some mandatory parameters actually mandatory (rh #953397)
- cli: enhance help documentation and bash completion (rh #1036545)
- cli: show VPN connection information (rh #1036132)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:0.9.9.0-29.git20131212
- Mass rebuild 2013-12-27

* Thu Dec 12 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-28.git20131212
- core: fix auto-activation after deactivation (rh #1033187)
- core: delay startup complete for initial carrier (rh #1030583)
- wifi: fix possible crashes checking associated AP (rh #1025371)
- core: fix sending of hostname to DHCP server (rh #1001529)
- core: don't retry a failed connection indefinitely (rh #1040528)
- core: add reconnect delay for PPPoE connections (rh #1023503)
- core: fix handling of routes with gateway in keyfiles (bgo #719851)
- core: fix wierd profile doubling on restart (rh #1029859)
- core: ensure software connections can be auto-activated after creationg (rh #1035814)
- core: fix setting broadcast address (rh #1032819)
- core: fix handling of PtP addresses for VPNs (rh #1018317)
- cli: fix help command for connection object (rh #1036545)
- core: fix connection auto-activation based on timestamp order (rh #1029854)
- core: fix connecting VLAN interfaces without a specific interface name (rh #1034908)
- core: fix crash canceling secrets requests (rh #922855)
- libnm-glib: fix crash when connections are deleted remotely (rh #1030403)
- cli: add "nmcli con load file..." (bgo #709830)
- core: use disable_ipv6 in the right situations (rh #1004255)
- cli: fix crash on editing 'lo' connection (rh #1030395)
- core: ignore RA-provided IPv6 default routes (rh #1042402)
- core: fix various issues found by Coverity (rh #1025894)
- cli: add bash completion for hostname commands (rh #1018510)
- core: require secondary connections to be VPNs (rh #997039)
- core: don't crash if ethernet device has no MAC address (rh #1029053)

* Tue Dec  3 2013 Dan Winship <danw@redhat.com> - 0.9.9.0-27.git20131108
- nmtui: update to latest snapshot

* Mon Nov 25 2013 Dan Winship <danw@redhat.com> - 0.9.9.0-26.git20131108
- cli: add "nmcli con load" to fix ifup (rh #1022256)

* Thu Nov 21 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-25.git20131108
- core: stop touching the loopback device (rh #1031794)

* Tue Nov 19 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-24.git20131108
- core: read DNS information when reading initial interface configurations (rh #1031763)

* Tue Nov 19 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-23.git20131108
- core: run reverse-DNS hostname lookups even if IP config has no DNS servers (rh #1031763)

* Wed Nov 13 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-22.git20131108
- core: allow same connection reactivations on the same device (rh #997998)

* Wed Nov 13 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-21.git20131108
- core: fix default wired connection changes causing disconnection (rh #1029464)

* Fri Nov  8 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-20.git20131108
- core: fix possible crash with WiFi (rh #1025371)
- core: fix crash cleaning up Team devices

* Fri Nov  8 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-19.git20131108
- core: fix various issues with ignore-carrier configuration (rh #1018403)
- core: improve handling of NPAR/SRIOV devices in bonds (rh #804527)
- ifcfg-rh: fix crash when reading connection (rh #1025007)
- core: better handling of unrecognized connections (rh #1022256)
- cli: add 'nmcli dev connect eth0' functionality (rh #961543)
- core: add support for DCB/FCoE configuration (rh #799241)
- cli: add 'activate' menu command for interactive editor (rh #1004883)
- core: fix segfault when setting default IPv6 route for VPNs (rh #1019021)
- core: track autoconnect for software devices that are removed (rh #1005913)
- ifcfg-rh: always read and write static IP addresses (rh #998135)
- cli: copy remove connection to local one on save (rh #997958)
- core: don't crash when no DHCP client is available (rh #1015809)
- libnm-glib: fix crash in nm_client_new() (rh #1010288)

* Tue Nov  5 2013 Dan Winship <danw@redhat.com> - 0.9.9.0-18.git20131011
- Add an explicit versioned NM-glib requirement to NM-tui, per rpmdiff

* Wed Oct 30 2013 Dan Winship <danw@redhat.com> - 0.9.9.0-17.git20131011
- Add NetworkManager-tui package with the (still-alpha) curses UI (rh #1025021)

* Fri Oct 11 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-16.git20131011
- core: fix IPv4 addressing when IPv6 is disabled at boot time (rh #1012151)
- ifcfg-rh: fix handling of default routes in route6 files (rh #991807)
- core: fix PropertiesChanged signals for IP-related properties
- ifcfg-rh: make minimal ifcfg file handling consistent with initscripts

* Fri Oct  4 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-15.git20131004
- core: add support for 'primary' bond option (rh #1013727)
- cli: fix creation of Dynamic WEP configurations (rh #1005171)

* Thu Oct  3 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-14.git20131003
- core: fix DHCPv6 address prefix length (rh #1013583)
- cli: enhance bonding questionaire (rh #1007355)
- core: fix crash with Bluez5 if PAN connection is not defined (rh #1014770)
- libnm-glib: fix various memory leaks that could cause UIs to mis-report state
- core: fix issues with mis-configured IPv6 router advertisements (rh #1008104)
- cli: fix potential crash editing connections (rh #1011942)
- core: fix crash deactivating team devices (rh #1013593)

* Tue Oct  1 2013 Dan Winship <danw@redhat.com> - 0.9.9.0-13.git20131001
- core: fix bridge device creation (#1012532)
- core,settings: do not call functions with connection==NULL (rh #1008151)
- cli: accept gateway in the IP questionnaire of 'nmcli -a con add' (rh #1007368)
- cli: always print success message (not only in --pretty mode) (rh #1006444)
- cli: fix bond questionnaire to be able to set miimon (rh #1007355)
- ifcfg-rh: if IPv4 is disabled put DNS domains (DOMAIN) into IPv6 (rh #1004866)
- platform: fix a crash when nm_platform_sysctl_get() returns NULL (rh #1010522)
- platform: fix InfiniBand partition handling (rh #1008568)
- infiniband: only check the last 8 bytes when doing hwaddr matches (rh #1008566)
- bluez: merge adding support for BlueZ 5 (bgo #701078)
- api: clarify lifetime and behavior of ActiveConnection's SpecificObject property (rh #1012309)
- vpn: fix connecting to VPN (bgo #708255) (rh #1014716)
- rdisc: do not crash on NDP init failures (rh #1012151)
- cli: be more verbose when adding IP addresses in questionnaire (rh #1006450)
- team: chain up parent dispose() in NMDeviceTeam dispose() (rh #1013593)
- translation updates

* Fri Sep 20 2013 Bill Nottingham <notting@redhat.com> - 0.9.9.0-12.git20130913
- drop wimax subpackage

* Fri Sep 13 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-11.git20130913
- core: actually enable ModemManager 1.0 support
- libnm-glib: fix nm_remote_connection_delete() not calling callback (rh #997568)
- cli: ensure terminal is reset after quitting
- cli: set wep-key-type properly when editing (rh #1003945)
- man: fix typo in nmcli examples manpage (rh #1004117)
- core: fix setting VLAN ingress/egress mappings
- core: allow creating VLANs from interfaces other than Ethernet (rh #1003180)
- cli: fix input/output format conversion (rh #998929)

* Fri Sep  6 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-10.git20130906
- core: fix bug which disallowed deleting connections (rh #997568)
- core: add support for Team devices
- core: enable NetworkManager-wait-online by default (rh #816655)
- core: fix crash when 'gre' and 'macvlan' links change (rh #997396)
- core: fail activation when invalid static routes are configured (rh #999544)
- core: enhance connectivity checking to include portal detection
- core: allow hyphens for MAC addresses (rh #1002553)
- core: remove NetworkManager-created software devices when they are deactivated (rh #953300)
- core: fix handling of some DHCP client identifiers (rh #999503)
- core: correctly handle Open vSwitch interfaces as generic interfaces (rh #1004356)
- core: better handle Layer-2-only connections (rh #979288)
- cli: enhanced bash completion
- cli: make the 'describe' command more visible (rh #998002)
- cli: fix bug rejecting changes to Wi-Fi channels (rh #999999)
- cli: update bash completion to suggest connection names (rh #997997)
- cli: fix tab completion for aliases in edit mode
- cli: ask whether to switch IP method to 'auto' when all addresses are deleted (rh #998137)
- cli: request missing information when --ask is passed (rh #953291)
- cli: add 'remove' command to edit mode
- cli: fix creation of secure Wi-Fi connections (rh #997969) (rh #997555)
- cli: default autoconnect to no and ask whether to activate on save (rh #953296)
- man: clarify manpage text (rh #960071) (rh #953299)
- man: fix errors in the nmcli help output and manpage (rh #997566)
- ifcfg-rh: only write IPV6_DEFAULTGW when there's actually a default gateway (rh #997759)
- ifcfg-rh: fix handling of legacy-format routes file with missing gateway

* Wed Aug  7 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-9.git20130807
- core: fix assert on multi-hop routes (rh #989022)
- core: fix dispatcher systemd unit enabling (rh #948433)
- ifcfg-rh: ignore emacs temporary lockfiles (rh #987629)
- core: fix various routing issues and interaction with kernel events
- cli: confirm saving connections when autoconnect is enabled (rh #953296)
- cli: automatically change method when static IP addresses are added
- core: preserve externally added IPv4 routes and addresses

* Thu Jul 25 2013 Dan Winship <danw@redhat.com> - 0.9.9.0-8.git20130724
- Create NetworkManager-config-server package

* Wed Jul 24 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-7.git20130724
- Update to git snapshot

* Tue Jul  2 2013 Dan Winship <danw@redhat.com> - 0.9.9.0-6
- Belatedly update udev directory for UsrMove
- Fix incorrect dates in old changelog entries to avoid rpm warnings

* Wed Jun 26 2013 Dan Winship <danw@redhat.com> - 0.9.9.0-5
- build support for connectivity checking (rh #810457)

* Tue Jun 25 2013 Jiří Klimeš <jklimes@redhat.com> - 0.9.9.0-4.git20130603
- disable building WiMax for RHEL

* Mon Jun  3 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-3.git20130603
- Update to new 0.9.10 snapshot

* Wed May 15 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-2.git20130515
- Update for systemd network-online.target (rh #787314)
- Add system service for the script dispatcher (rh #948433)

* Tue May 14 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-1.git20130514
- Enable hardened build
- Update to 0.9.10 snapshot
- cli: new capabilities and somewhat re-arranged syntax
- core: generic interface support
- core: split config support; new "server mode" options
- core: allow locking connections to interface names

* Tue May  7 2013 Dan Williams <dcbw@redhat.com> - 0.9.8.1-2.git20130507
- core: fix issue with UI not showing disconnected on rfkill
- core: memory leak fixes
- core: silence warning about failure reading permanent MAC address (rh #907912)
- core: wait up to 120s for slow-connecting modems
- core: don't crash on PPPoE connections without a wired setting
- core: ensure the AvailableConnections property is always correct
- keyfile: ensure all-default VLAN connections are read correctly
- core: suppress kernel's automatic creation of bond0 (rh #953466)
- libnm-glib: make NMSecretAgent usable with GObject Introspection
- libnm-util: fix GObject Introspection annotations of nm_connection_need_secrets()
- core: documentation updates

* Wed Mar 27 2013 Dan Williams <dcbw@redhat.com> - 0.9.8.1-1.git20130327
- Update to 0.9.8.2 snapshot
- core: fix VLAN parent handling when identified by UUID
- core: quiet warning about invalid interface index (rh #920145)
- core: request 'static-routes' from DHCP servers (rh #922558)
- core: fix crash when dbus-daemon is restarted (rh #918273)
- core: copy leasefiles from /var/lib/dhclient to fix netboot (rh #916233)
- core: memory leak and potential crash fixes
- ifcfg-rh: ensure missing STP property is interpreted as off (rh #922702)

* Wed Feb 27 2013 Jiří Klimeš <jklimes@redhat.com> - 0.9.8.0-1
- Update to the 0.9.8.0 release
- cli: fix a possible crash

* Sat Feb  9 2013 Dan Williams <dcbw@redhat.com> - 0.9.7.997-2
- core: use systemd for suspend/resume, not upower

* Fri Feb  8 2013 Dan Williams <dcbw@redhat.com> - 0.9.7.997-1
- Update to 0.9.8-beta2
- core: ignore bridges managed by other tools (rh #905035)
- core: fix libnl assert (rh #894653)
- wifi: always use Proactive Key Caching with WPA Enterprise (rh #834444)
- core: don't crash when Internet connection sharing fails to start (rh #883142)

* Fri Jan  4 2013 Dan Winship <danw@redhat.com> - 0.9.7.0-12.git20121004
- Set correct systemd KillMode to fix anaconda shutdown hangs (rh #876218)

* Tue Dec 18 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-11.git20121004
- ifcfg-rh: write missing IPv6 setting as IPv6 with "auto" method (rh #830434)

* Wed Dec  5 2012 Dan Winship <danw@redhat.com> - 0.9.7.0-10.git20121004
- Build vapi files and add them to the devel package

* Wed Dec  5 2012 Dan Winship <danw@redhat.com> - 0.9.7.0-9.git20121004
- Apply patch from master to read hostname from /etc/hostname (rh #831735)

* Tue Nov 27 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-8.git20121004
- Apply patch from master to update hostname (rh #875085)
- spec: create /etc/NetworkManager/dnsmasq.d (rh #873621)

* Tue Nov 27 2012 Daniel Drake <dsd@laptop.org> - 0.9.7.0-7.git20121004
- Don't bring up uninitialized devices (fd #56929)

* Mon Oct 15 2012 Dan Winship <danw@redhat.com> - 0.9.7.0-6.git20121004
- Actually apply the patch from the previous commit...

* Mon Oct 15 2012 Dan Winship <danw@redhat.com> - 0.9.7.0-5.git20121004
- Apply patch from master to fix a crash (rh #865009)

* Sat Oct  6 2012 Dan Winship <danw@redhat.com> - 0.9.7.0-4.git20121004
- Apply patch from master so connections finish connecting properly (bgo #685581)

* Fri Oct  5 2012 Dan Williams <dcbw@redhat.com> - 0.9.7.0-3.git20121004
- Forward-port some forgotten fixes from F17
- Fix networked-filesystem systemd dependencies (rh #787314)
- Don't restart NM on upgrade, don't stop NM on uninstall (rh #811200)

* Thu Oct  4 2012 Dan Winship <danw@redhat.com> - 0.9.7.0-2.git20121004
- Update to git snapshot

* Tue Aug 21 2012 Dan Winship <danw@redhat.com> - 0.9.7.0-1.git20120820
- Update to 0.9.7.0 snapshot

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.5.96-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 23 2012 Dan Williams <dcbw@redhat.com> - 0.9.5.96-1
- Update to 0.9.6-rc2
- core: fix race between parallel DHCP client invocations
- core: suppress a useless warning (rh #840580)
- ifcfg-rh: fix segfault with malformed values (rh #841391)
- ifcfg-rh: ignore IP config on bond slave configurations (rh #838907)

* Fri Jul 13 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.5.95-1.git20120713
- Update to 0.9.5.95 (0.9.6-rc1) snapshot
- core: add autoconnect, driver-versioni and firmware-version properties to NMDevice
- core: various IPv6 improvements
- core: reduce number of changes made to DNS information during connection setup
- core: add Vala language bindings
- vpn: support IPv6 over VPNs
- wifi: add on-demand WiFi scan support

* Mon May 21 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.4-5.git20120521
- Update to git snapshot

* Tue May  8 2012 Dan Winship <danw@redhat.com> - 0.9.4-4.git20120502
- NM no longer uses /var/run/NetworkManager, so don't claim to own it.
  (rh #656638)

* Wed May  2 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.4-3.git20120502
- Update to git snapshot

* Wed Mar 28 2012 Colin Walters <walters@verbum.org> - 1:0.9.4-2.git20120328_2
- Add _isa for internal requires; otherwise depsolving may pull in an
  arbitrary architecture.

* Wed Mar 28 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.4-1.git20120328_2
- Update to 0.9.4

* Mon Mar 19 2012 Dan Williams <dcbw@redhat.com> - 0.9.3.997-2
- libnm-glib: updated for new symbols the applet wants

* Mon Mar 19 2012 Dan Williams <dcbw@redhat.com> - 0.9.3.997-1
- applet: move to network-manager-applet RPM
- editor: move to nm-connection-editor RPM
- libnm-gtk: move to libnm-gtk RPM

* Mon Mar 19 2012 Dan Williams <dcbw@redhat.com> - 0.9.3.997-0.7
- Update to 0.9.3.997 (0.9.4-rc1)
- core: fix possible WiFi hang when connecting to Ad-Hoc networks
- core: enhanced IPv6 compatibility
- core: proxy DNSSEC data when using the 'dnsmasq' caching nameserver plugin
- core: allow VPNs to specify multiple domain names given by the server
- core: fix an issue creating new InfiniBand connections
- core/applet/editor: disable WiFi Ad-Hoc WPA connections until kernel bugs are fixed

* Wed Mar 14 2012 Dan Williams <dcbw@redhat.com> - 0.9.3.995-0.6
- core: fix issue with carrier changes not being recognized (rh #800690)
- editor: warn user if CA certificate is left blank

* Tue Mar 13 2012 Dan Williams <dcbw@redhat.com> - 0.9.3.995-0.5
- core: fix a crash with ipw2200 devices and adhoc networks
- core: fix IPv6 addressing on newer kernels
- core: fix issue with VPN plugin passwords (rh #802540)
- cli: enhancements for Bonding, VLAN, and OLPC mesh devices
- ifcfg-rh: fix quoting WPA passphrases that include quotes (rh #798102)
- libnm-glib: fix some issues with duplicate devices shown in menus

* Fri Mar  2 2012 Dan Williams <dcbw@redhat.com> - 0.9.3.995-0.4
- Update to 0.9.3.995 (0.9.4-beta1)
- core: add support for bonding and VLAN interfaces
- core: add support for Internet connectivity detection
- core: add support for IPv6 Privacy Extensions
- core: fix interaction with firewalld restarts

* Thu Mar  1 2012 Dan Horák <dan[at]danny.cz> - 0.9.3-0.3
- disable WiMAX plugin on s390(x)

* Thu Feb 16 2012 Dan Williams <dcbw@redhat.com> - 0.9.3-0.2
- Put WiMAX plugin files in the right subpackage

* Wed Feb 15 2012 Dan Williams <dcbw@redhat.com> - 0.9.3-0.1
- Update to 0.9.4 snapshot
- wimax: enable optional support for Intel WiMAX devices
- core: use nl80211 for WiFi device control
- core: add basic support for Infiniband IP interfaces
- core: add basic support for bonded interfaces
- core: in-process IP configuration no longer blocks connected state

* Thu Jan 19 2012 Matthias Clasen <mclasen@redhat.com> - 0.9.2-4
- Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 24 2011 Daniel Drake <dsd@laptop.org> - 0.9.2-2
- Rebuild for libgnome-bluetooth.so.9

* Wed Nov 09 2011 Dan Williams <dcbw@redhat.com> - 0.9.2-1
- core: fix possible crash when talking to ModemManager
- core: improve handling of rfkill on some machines (eeepc 1005HA and others)
- ifcfg-rh: don't use spaces in ifcfg file names (rh #742273)
- core: accept IPv6 Router Advertisements when forwarding is on
- core: bump dnsmasq cache size to 400 entries
- core: ensure IPv6 static routes are flushed when device is deactivated
- ifcfg-rh: fix changing WPA connections to WEP
- core: fix setting hostname from DHCP (rh #719100)
- libnm-glib: fix various GObject introspection issues (rh #747302)
- core: don't change routing or DNS if no devices are managed
- core: ensure IPv6 RA-provided routes are honored

* Wed Nov  9 2011 Adam Williamson <awilliam@redhat.com> - 1:0.9.1.90-5.git20110927
- Rebuilt for glibc (rh #747377)
- core: fix setting hostname from DHCP options (rh #719100)
- skip a release to keep up with F16

* Tue Sep 27 2011 Dan Williams <dcbw@redhat.com> - 0.9.1.90-3.git20110927
- core: fix location of wifi.ui (rh #741448)

* Tue Sep 27 2011 Jiří Klimeš <jklimes@redhat.com> - 0.9.1.90-2.git20110927
- core: ifcfg-rh: remove newlines when writing to ifcfg files (CVE-2011-3364) (rh #737338)
- core: change iscsiadm path to /sbin/iscsiadm in ifcfg-rh plugin (rh #740753)
- core: fix refcounting when deleting a default wired connection (lp:797868)

* Mon Sep 19 2011 Dan Williams <dcbw@redhat.com> - 0.9.1.90-1
- Update to 0.9.1.90 (0.9.2-beta1)
- core: fix IPv6 link-local DNS servers in the dnsmasq DNS plugin
- cli: add ability to delete connections
- keyfile: fix an issue with duplicated keyfile connections
- core: ensure the 'novj' option is passed through to pppd
- core: store timestamps for VPN connections too (rh #725353)

* Fri Sep  9 2011 Tom Callaway <spot@fedoraproject.org> - 0.9.0-2
- fix systemd scriptlets and trigger

* Tue Aug 23 2011 Dan Williams <dcbw@redhat.com> - 0.9.0-1
- Update to 0.9 release
- core: fix issue where scan results could be ignored
- core: ensure agent secrets are preserved when updating connections
- core: don't autoconnect disabled modems
- core: fix race when checking modem enabled/disabled status after disabling
- core: ensure newly installed VPN plugins can actually talk to NM
- core: add support for 802.1X certificate subject matching
- libnm-glib: various introspection fixes
- applet/editor: updated translations

* Fri Aug 05 2011 Ray Strode <rstrode@redhat.com> 0.8.9997-7.git20110721
- Add some patches for some blocker (rh #727501)

* Thu Jul 21 2011 Dan Williams <dcbw@redhat.com> - 0.8.9997-6.git20110721
- core: updated Russian translation (rh #652904)
- core: fix possible crash if secrets are missing
- core: append interface name for IPv6 link-local DNS server addresses (rh #720001)
- core: fix setting hostname from DHCP options (rh #719100)
- libnm-util: GObject introspection annotation fixes
- libnm-util: ensure IP address/route prefixes are valid
- ifcfg-rh: read anonymous identity for 802.1x PEAP connections (rh #708436)
- applet: show notifications on CDMA home/roaming changes
- applet: fix various issues saving VPN secrets
- editor: allow exporting VPN secrets
- editor: default to IPv6 "automatic" addressing mode

* Sat Jul  2 2011 Dan Williams <dcbw@redhat.com> - 0.8.9997-5.git20110702
- core: ensure users are authorized for shared wifi connections (CVE-2011-2176) (rh #715492)
- core: retry failed connections after 5 minute timeout
- core: immediately request new 802.1x 'always ask' passwords if they fail
- core: add MAC blacklisting capability for WiFi and Wired connections
- core: retry failed connections when new users log in (rh #706204)
- applet: updated translations
- core: drop compat interface now that KDE bits are updated to NM 0.9 API

* Mon Jun 20 2011 Dan Williams <dcbw@redhat.com> - 0.8.9997-4.git20110620
- core: don't cache "(none)" hostname at startup (rh #706094)
- core: fix handling of VPN connections with only system-owned secrets
- core: fix optional waiting for networking at startup behavior (rh #710502)
- ifcfg-rh: fix possible crashes in error cases
- ifcfg-rh: fix various IPv4 and IPv6 handling issues
- applet: add notifications of GSM mobile broadband registration status
- editor: move secrets when making connections available to all users or private
- applet: don't show irrelevant options when asking for passwords

* Mon Jun 13 2011 Dan Williams <dcbw@redhat.com> - 0.8.9997-3.git20110613
- keyfile: better handling of missing certificates/private keys
- core: fix issues handling "always-ask" wired and WiFi 802.1x connections (rh #703785)
- core: fix automatic handling of hidden WiFi networks (rh #707406)
- editor: fix possible crash after reading network connections (rh #706906)
- editor: make Enter/Return key close WiFi password dialogs (rh #708666)

* Fri Jun  3 2011 Dan Williams <dcbw@redhat.com> - 0.8.9997-2.git20110531
- Bump for CVE-2011-1943 (no changes, only a rebuild)

* Tue May 31 2011 Dan Williams <dcbw@redhat.com> - 0.8.9997-1.git20110531
- editor: fix resizing of UI elements (rh #707269)
- core: retry wired connections when cable is replugged
- core: fix a few warnings and remove some left-over debugging code

* Thu May 26 2011 Dan Williams <dcbw@redhat.com> - 0.8.999-3.git20110526
- compat: fix activation/deactivation of VPN connections (rh #699786)
- core: fix autodetection of previously-used hidden wifi networks
- core: silence error if ConsoleKit database does not yet exist (rh #695617)
- core: fix Ad-Hoc frequency handling (rh #699203)
- core: fixes for migrated OpenConnect VPN plugin connections
- core: various fixes for VPN connection secrets handling
- core: send only short hostname to DHCP servers (rh #694758)
- core: better handling of PKCS#8 private keys
- core: fix dispatcher script interface name handling
- editor: fix potential crash when connection is invalid (rh #704848)
- editor: allow _ as a valid character for GSM APNs

* Mon May  9 2011 Dan Williams <dcbw@redhat.com> - 0.8.999-2.git20110509
- core: fix possible crash when connections are deleted
- core: fix exported symbols in libnm-util and libnm-glib
- core/applet: updated translations

* Tue May  3 2011 Dan Williams <dcbw@redhat.com> - 0.8.999-1
- core: ensure DER format certificates are correctly recognized (rh #699591)
- core: fix WINS server handling in client helper libraries
- core: enhance dispatcher script environment to include IPv6 and VPN details
- applet: migrate openswan connections to 0.9
- editor: improve usability of editing IP addresses (rh #698199)

* Wed Apr 27 2011 Dan Williams <dcbw@redhat.com> - 0.8.998-4.git20110427
- core: enable optimized background roaming for WPA Enterprise configs
- core: better handling of WiFi and WiMAX rfkill (rh #599002)
- applet: fix crash detecting Bluetooth DUN devices a second time
- ifcfg-rh: fix managed/unmanaged changes when removing connections (rh #698202)

* Tue Apr 19 2011 Dan Williams <dcbw@redhat.com> - 0.8.998-3.git20110419
- core: systemd and startup enhancements for NFS mounts
- core: more efficient startup process
- core: fix handling of multiple logins when one is inactive
- core: fix handling of S390/Hercules CTC network interfaces (rh #641986)
- core: support Easytether interfaces for Android phones
- core: fix handling of WWAN enable/disable states
- ifcfg-rh: harmonize handling if IPADDR/PREFIX/NETMASK with initscripts (rh #658907)
- applet: fix connection to WPA Enterprise networks (rh #694765)

* Wed Apr 06 2011 Dan Williams <dcbw@redhat.com> - 0.8.998-2.git20110406
- core: fix handling of infinite IPv6 RDNSS timeouts (rh #689291)

* Mon Apr 04 2011 Dan Williams <dcbw@redhat.com> - 0.8.998-1
- Update to 0.8.998 (0.9.0-rc1)
- core: fix near-infinite requests for passwords (rh #692783)
- core: fix handling of wired 802.1x connections
- core: ignore Nokia PC-Suite ethernet devices we can't use yet
- applet: migrate 0.8 OpenVPN passwords to 0.9 formats

* Thu Mar 31 2011 Dan Williams <dcbw@redhat.com> - 0.8.997-8.git20110331
- core: resurrect default VPN username
- core: don't stomp on crypto library users by de-initing the crypto library

* Wed Mar 30 2011 Dan Williams <dcbw@redhat.com> - 0.8.997-7.git20110330
- core: fix creation of default wired connections
- core: fix requesting new secrets when old ones fail (ex changing WEP keys)
- editor: ensure all pages are sensitive after retrieving secrets
- editor: fix crash when scrolling through connection lists (rh #693446)
- applet: fix crash after using the wifi or wired secrets dialogs (rh #693446)

* Mon Mar 28 2011 Christopher Aillon <caillon@redhat.com> - 0.8.997-6.git20110328
- Fix trigger to enable the systemd service for upgrades (rh #678553)

* Mon Mar 28 2011 Dan Williams <dcbw@redhat.com> - 0.8.997-5.git20110328
- core: fix connection deactivation on the compat interface
- core: give default wired connections a more friendly name
- core: fix base type of newly created wired connections
- applet: many updated translations

* Fri Mar 25 2011 Dan Williams <dcbw@redhat.com> - 0.8.997-4.git20110325
- core: fix possible libnm-glib crash when activating connections
- applet: fix various naming and dialog title issues

* Thu Mar 24 2011 Dan Williams <dcbw@redhat.com> - 0.8.997-3.git20110324
- nm-version.h should be in NetworkManager-devel, not -glib-devel (rh #685442)

* Thu Mar 24 2011 Dan Williams <dcbw@redhat.com> - 0.8.997-2.git20110324
- core: add compatibility layer for KDE Plasma network infrastructure

* Mon Mar 21 2011 Dan Williams <dcbw@redhat.com> - 0.8.997-1
- Update to 0.8.997 (0.9-beta3)
- ifcfg-rh: fix reading and writing of Dynamic WEP connections using LEAP as the eap method
- wifi: fix signal strength for scanned access points with some drivers
- applet: translation updates

* Thu Mar 10 2011 Dan Williams <dcbw@redhat.com> - 0.8.996-1
- Update to 0.8.996 (0.9-beta2)

* Wed Mar  9 2011 Dan Williams <dcbw@redhat.com> - 0.8.995-4.git20110308
- applet: fix bus name more

* Wed Mar  9 2011 Dan Williams <dcbw@redhat.com> - 0.8.995-3.git20110308
- applet: fix bus name

* Tue Mar  8 2011 Matthias Clasen <mclasen@redhat.com> - 0.8.995-2.git20110308
- Fix systemd requires

* Mon Mar  7 2011 Dan Williams <dcbw@redhat.com> - 0.8.995-1.git20110308
- Update to NetworkManager 0.9-beta1
- core: consolidate user and system settings services into NM itself
- core: add WiMAX support
- applet: support Fast User Switching

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 0.8.2-8.git20101117
- Rebuild against newer gtk

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.2-7.git20101117
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.8.2-6.git20101117
- Rebuild against new gtk

* Tue Feb  1 2011 Dan Williams <dcbw@redhat.com> - 0.8.2-5.git20101117
- Handle modem IP interface changes after device is recognized

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.8.2-4.git20101117
- Rebuild against new gtk3

* Tue Dec 21 2010 Dan Horák <dan[at]danny.cz> - 0.8.2-3.git20101117
- use --force in autoreconf to fix FTBFS

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 0.8.2-2.git20101117
- Rebuild against newer gtk

* Sat Nov 27 2010 Dan Williams <dcbw@redhat.com> - 0.8.2-1.git20101117
- Update to 0.8.2

* Wed Nov  3 2010 Matthias Clasen <mclasen@redhat.com> - 0.8.1-10.1
- Rebuild against libnotify 0.7
- misc gtk build fixes

* Mon Nov  1 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-10
- core: preserve WiFi Enabled state across reboot and suspend/resume

* Fri Oct 15 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-9
- core: fix suspend/resume regression (rh #638640)
- core: fix issue causing some nmcli requests to be ignored

* Thu Oct  7 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-8
- core: preserve custom local-mapped hostnames in /etc/hosts (rh #627269)

* Thu Oct  7 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-7
- core: remove stale /etc/hosts mappings (rh #630146)

* Tue Aug 31 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-6
- core: add dispatcher events on DHCPv4 and DHCPv6 lease changes
- core: enforce access permissions when enabling/disabling WiFi and WWAN (rh #626337)
- core: listen for UPower suspend/resume signals
- applet: fix disabled Enable Networking and Enable Wireless menu items (rh #627365)
- applet: updated translations
- applet: obscure Mobile Broadband PIN in secondary unlock dialog

* Wed Aug 18 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-5
- core: fix some systemd interaction issues

* Tue Aug 17 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-4
- core: rebuild to fix polkit 0.97 build issue
- applet: updated translations

* Fri Aug 13 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-3
- core: rebuild to fix dbus-glib security issue (CVE-2010-1172) (rh #585394)

* Fri Aug 13 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-2
- core: quiet annoying warnings (rh #612991)
- core: fix retrieval of various IP options in libnm-glib (rh #611141)
- core: ship NetworkManager.conf instead of deprecated nm-system-settings.conf (rh #606160)
- core: add short hostname to /etc/hosts too (rh #621910)
- core: recheck autoactivation when new system connections appear
- core: enable DHCPv6-only configurations (rh #612445)
- core: don't fail connection immediately if DHCP lease expires (rh #616084) (rh #590874)
- core: fix editing of PPPoE system connections
- core: work around twitchy frequency reporting of various wifi drivers
- core: don't tear down user connections on console changes (rh #614556)
- cli: wait a bit for NM's permissions check to complete (rh #614866)
- ifcfg-rh: ignore BRIDGE and VLAN configs and treat as unmanaged (rh #619863)
- man: add manpage for nm-online
- applet: fix crash saving ignore-missing-CA-cert preference (rh #619775)
- applet: hide PIN/PUK by default in the mobile PIN/PUK dialog (rh #615085)
- applet: ensure Enter closes the PIN/PUK dialog (rh #611831)
- applet: fix another crash in ignore-CA-certificate handling (rh #557495)
- editor: fix handling of Wired/s390 connections (rh #618620)
- editor: fix crash when canceling editing in IP address pages (rh #610891)
- editor: fix handling of s390-specific options
- editor: really fix crash when changing system connections (rh #603566)

* Thu Jul 22 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-1
- core: read nm-system-settings.conf before NetworkManager.conf (rh #606160)
- core: fix editing system DSL connections when using keyfile plugin
- core: work around inconsistent proprietary driver associated AP reporting
- core: ensure empty VPN secrets are not used (rh #587784)
- core: don't request WiFi scans when connection is locked to a specific BSSID
- cli: show IPv6 settings and configuration
- applet: updated translations
- editor: fix a PolicyKit-related crash editing connections (rh #603566)
- applet: fix saving the ignore-missing-CA-cert preference (rh #610084)
- editor: fix listing connections on PPC64 (rh #608663)
- editor: ensure editor windows are destroyed when closed (rh #572466)

* Thu Jul  1 2010 Matthias Clasen <mclasen@redhatcom> - 0.8.1-0.5
- Rebuild against new gnome-bluetooth

* Fri Jun 25 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-0.4
- Update to 0.8.1 release candidate
- core: fix WWAN hardware enable state tracking (rh #591622)
- core: fix Red Hat initscript return value on double-start (rh #584321)
- core: add multicast route entry for IPv4 link-local connections
- core: fix connection sharing in cases where a dnsmasq config file exists
- core: fix handling of Ad-Hoc wifi connections to indicate correct network
- core: ensure VPN interface name is passed to dispatcher when VPN goes down
- ifcfg-rh: fix handling of ASCII WEP keys
- ifcfg-rh: fix double-quoting of some SSIDs (rh #606518)
- applet: ensure deleted connections are actually forgotten (rh #618973)
- applet: don't crash if the AP's BSSID isn't availabe (rh #603236)
- editor: don't crash on PolicyKit events after windows are closed (rh #572466)

* Wed May 26 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-0.3
- core: fix nm-online crash (rh #593677)
- core: fix failed suspend disables network (rh #589108)
- core: print out missing firmware errors (rh #594578)
- applet: fix device descriptions for some mobile broadband devices
- keyfile: bluetooth fixes
- applet: updated translations (rh #589230)

* Wed May 19 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-0.2.git20100519
- core: use GIO in local mode only (rh #588745)
- core: updated translations (rh #589230)
- core: be more lenient in IPv6 RDNSS server expiry (rh #590202)
- core: fix headers to be C++ compatible (rh #592783)
- applet: updated translations (rh #589230)
- applet: lock connections with well-known SSIDs to their specific AP

* Mon May 10 2010 Dan Williams <dcbw@redhat.com> - 0.8.1-0.1.git20100510
- core: fix handling of IPv6 RA flags when router goes away (rh #588560)
- bluetooth: fix crash configuring DUN connections from the wizard (rh #590666)

* Sun May  9 2010 Dan Williams <dcbw@redhat.com> - 0.8-13.git20100509
- core: restore initial accept_ra value for IPv6 ignored connections (rh #588619)
- bluetooth: fix bad timeout on PAN connections (rh #586961)
- applet: updated translations

* Tue May  4 2010 Dan Williams <dcbw@redhat.com> - 0.8-12.git20100504
- core: treat missing IPv6 configuration as ignored (rh #588814)
- core: don't flush IPv6 link-local routes (rh #587836)
- cli: update output formatting

* Mon May  3 2010 Dan Williams <dcbw@redhat.com> - 0.8-11.git20100503
- core: allow IP configuration as long as one method completes (rh #567978)
- core: don't prematurely remove IPv6 RDNSS nameservers (rh #588192)
- core: ensure router advertisements are only used when needed (rh #588613)
- editor: add IPv6 gateway editing capability

* Sun May  2 2010 Dan Williams <dcbw@redhat.com> - 0.8-10.git20100502
- core: IPv6 autoconf, DHCP, link-local, and manual mode fixes
- editor: fix saving IPv6 address in user connections

* Thu Apr 29 2010 Dan Williams <dcbw@redhat.com> - 0.8-9.git20100429
- core: fix crash when IPv6 is enabled and interface is deactivated

* Mon Apr 26 2010 Dan Williams <dcbw@redhat.com> - 0.8-8.git20100426
- core: fix issues with IPv6 router advertisement mishandling (rh #530670)
- core: many fixes for IPv6 RA and DHCP handling (rh #538499)
- core: ignore WWAN ethernet devices until usable (rh #585214)
- ifcfg-rh: fix handling of WEP passphrases (rh #581718)
- applet: fix crashes (rh #582938) (rh #582428)
- applet: fix crash with multiple concurrent authorization requests (rh #585405)
- editor: allow disabling IPv4 on a per-connection basis
- editor: add support for IPv6 DHCP-only configurations

* Thu Apr 22 2010 Dan Williams <dcbw@redhat.com> - 0.8-7.git20100422
- core: fix crash during install (rh #581794)
- wifi: fix crash when supplicant segfaults after resume (rh #538717)
- ifcfg-rh: fix MTU handling for wired connections (rh #569319)
- applet: fix display of disabled mobile broadband devices

* Thu Apr  8 2010 Dan Williams <dcbw@redhat.com> - 0.8-6.git20100408
- core: fix automatic WiFi connections on resume (rh #578141)

* Thu Apr  8 2010 Dan Williams <dcbw@redhat.com> - 0.8-5.git20100408
- core: more flexible logging
- core: fix crash with OLPC mesh devices after suspend
- applet: updated translations
- applet: show mobile broadband signal strength and technology in the icon
- applet: fix continuous password requests for 802.1x connections (rh #576925)
- applet: many updated translations

* Thu Mar 25 2010 Dan Williams <dcbw@redhat.com> - 0.8-4.git20100325
- core: fix modem enable/disable
- core: fix modem default route handling

* Tue Mar 23 2010 Dan Williams <dcbw@redhat.com> - 0.8-3.git20100323
- core: don't exit early on non-fatal state file errors
- core: fix Bluetooth connection issues (rh #572340)
- applet: fix some translations (rh #576056)
- applet: better feedback when wrong PIN/PUK is entered
- applet: many updated translations
- applet: PIN2 unlock not required for normal modem functionality
- applet: fix wireless secrets dialog display

* Wed Mar 17 2010 Dan Williams <dcbw@redhat.com> - 0.8-2.git20100317
- man: many manpage updates
- core: determine classful prefix if non is given via DHCP
- core: ensure /etc/hosts is always up-to-date and correct (rh #569914)
- core: support GSM network and roaming preferences
- applet: startup speed enhancements
- applet: better support for OTP/token-based WiFi connections (rh #526383)
- applet: show GSM and CDMA registration status and signal strength when available
- applet: fix zombie GSM and CDMA devices in the menu
- applet: remove 4-character GSM PIN/PUK code limit
- applet: fix insensitive WiFi Create... button (rh #541163)
- applet: allow unlocking of mobile devices immediately when plugged in

* Fri Feb 19 2010 Dan Williams <dcbw@redhat.com> - 0.8-1.git20100219
- core: update to final 0.8 release
- core: fix Bluetooth DUN connections when secrets are needed
- ifcfg-rh: add helper for initscripts to determine ifcfg connection UUIDs
- applet: fix Bluetooth connection secrets requests
- applet: fix rare conflict with other gnome-bluetooth plugins

* Thu Feb 11 2010 Dan Williams <dcbw@redhat.com> - 0.8-0.4.git20100211
- core: fix mobile broadband PIN handling (rh #543088) (rh #560742)
- core: better handling of /etc/hosts if hostname was already added by the user
- applet: crash less on D-Bus property errors (rh #557007)
- applet: fix crash entering wired 802.1x connection details (rh #556763)

* Tue Feb 09 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.8-0.3.git20100129
- core: validate the autostart .desktop file
- build: fix nmcli for the stricter ld (fixes FTBFS)
- build: fix nm-connection-editor for the stricter ld (fixes FTBFS)
- applet: don't autostart in KDE on F13+ (#541353)

* Fri Jan 29 2010 Dan Williams <dcbw@redhat.com> - 0.8-0.2.git20100129
- core: add Bluetooth Dial-Up Networking (DUN) support (rh #136663)
- core: start DHCPv6 on receipt of RA 'otherconf'/'managed' bits
- nmcli: allow enable/disable of WiFi and WWAN

* Fri Jan 22 2010 Dan Williams <dcbw@redhat.com> - 0.8-0.1.git20100122
- ifcfg-rh: read and write DHCPv6 enabled connections (rh #429710)
- nmcli: update

* Thu Jan 21 2010 Dan Williams <dcbw@redhat.com> - 0.7.999-2.git20100120
- core: clean NSS up later to preserve errors from crypto_init()

* Wed Jan 20 2010 Dan Williams <dcbw@redhat.com> - 0.7.999-1.git20100120
- core: support for managed-mode DHCPv6 (rh #429710)
- ifcfg-rh: gracefully handle missing PREFIX/NETMASK
- cli: initial preview of command-line client
- applet: add --help to explain what the applet is (rh #494641)

* Wed Jan  6 2010 Dan Williams <dcbw@redhat.com> - 0.7.998-1.git20100106
- build: fix for new pppd (rh #548520)
- core: add WWAN enable/disable functionality
- ifcfg-rh: IPv6 addressing and routes support (rh #523288)
- ifcfg-rh: ensure connection is updated when route/key files change
- applet: fix crash when active AP isn't found (rh #546901)
- editor: fix crash when editing connections (rh #549579)

* Mon Dec 14 2009 Dan Williams <dcbw@redhat.com> - 0.7.997-2.git20091214
- core: fix recognition of standalone 802.1x private keys
- applet: clean notification text to ensure it passes libnotify validation

* Mon Dec  7 2009 Dan Williams <dcbw@redhat.com> - 0.7.997-1
- core: remove haldaemon from initscript dependencies (rh #542078)
- core: handle PEM certificates without an ending newline (rh #507315)
- core: fix rfkill reporting for ipw2x00 devices
- core: increase PPPoE timeout to 30 seconds
- core: fix re-activating system connections with secrets
- core: fix crash when deleting automatically created wired connections
- core: ensure that a VPN's DNS servers are used when sharing the VPN connection
- ifcfg-rh: support routes files (rh #507307)
- ifcfg-rh: warn when device will be managed due to missing HWADDR (rh #545003)
- ifcfg-rh: interpret DEFROUTE as never-default (rh #528281)
- ifcfg-rh: handle MODE=Auto correctly
- rpm: fix rpmlint errors
- applet: don't crash on various D-Bus and other errors (rh #545011) (rh #542617)
- editor: fix various PolicyKit-related crashes (rh #462944)
- applet+editor: notify user that private keys must be protected

* Fri Nov 13 2009 Dan Williams <dcbw@redhat.com> - 0.7.996-7.git20091113
- nm: better pidfile handing (rh #517362)
- nm: save WiFi and Networking enabled/disabled states across reboot
- nm: fix crash with missing VPN secrets (rh #532084)
- applet: fix system connection usage from the "Connect to hidden..." dialog
- applet: show Bluetooth connections when no other devices are available (rh #532049)
- applet: don't die when autoconfigured connections can't be made (rh #532680)
- applet: allow system administrators to disable the "Create new wireless network..." menu item
- applet: fix missing username connecting to VPNs the second time
- applet: really fix animation stuttering
- editor: fix IP config widget tooltips
- editor: allow unlisted countries in the mobile broadband wizard (rh #530981)
- ifcfg-rh: ignore .rpmnew files (rh #509621)

* Wed Nov 04 2009 Dan Williams <dcbw@redhat.com> - 0.7.996-6.git20091021
- nm: fix PPPoE connection authentication (rh #532862)

* Wed Oct 21 2009 Dan Williams <dcbw@redhat.com> - 0.7.996-5.git20091021
- install: better fix for (rh #526519)
- install: don't build Bluetooth bits on s390 (rh #529854)
- nm: wired 802.1x connection activation fixes
- nm: fix crash after modifying default wired connections like "Auto eth0"
- nm: ensure VPN secrets are requested again after connection failure
- nm: reset 'accept_ra' to previous value after deactivating IPv6 connections
- nm: ensure random netlink events don't interfere with IPv6 connection activation
- ifcfg-rh: fix writing out LEAP connections
- ifcfg-rh: recognize 'static' as a valid BOOTPROTO (rh #528068)
- applet: fix "could not find required resources" error (rh #529766)

* Fri Oct  2 2009 Dan Williams <dcbw@redhat.com> - 0.7.996-4.git20091002
- install: fix -gnome package pre script failures (rh #526519)
- nm: fix failures validating private keys when using the NSS crypto backend
- applet: fix crashes when clicking on menu but not associated (rh #526535)
- editor: fix crash editing wired 802.1x settings
- editor: fix secrets retrieval when editing connections

* Mon Sep 28 2009 Dan Williams <dcbw@redhat.com> - 0.7.996-3.git20090928
- nm: fix connection takeover when carrier is not on
- nm: handle certificate paths (CA chain PEM files are now fully usable)
- nm: defer action for 4 seconds when wired carrier drops
- ifcfg-rh: fix writing WPA passphrases with odd characters
- editor: fix editing of IPv4 settings with new connections (rh #525819)
- editor: fix random crashes when editing due to bad widget refcounting
- applet: debut reworked menu layout (not final yet...)

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> - 0.7.996-3.git20090921
- Install GConf schemas

* Mon Sep 21 2009 Dan Williams <dcbw@redhat.com> - 0.7.996-2.git20090921
- nm: allow disconnection of all device types
- nm: ensure that wired connections are torn down when their hardware goes away
- nm: fix crash when canceling a VPN's request for secrets
- editor: fix issues changing connections between system and user scopes
- editor: ensure changes are thrown away when editing is canceled
- applet: ensure connection changes are noticed by NetworkManager
- applet: fix crash when creating new connections
- applet: actually use wired 802.1x secrets after they are requested

* Wed Aug 26 2009 Dan Williams <dcbw@redhat.com> - 0.7.996-1.git20090826
- nm: IPv6 zeroconf support and fixes
- nm: port to polkit (rh #499965)
- nm: fixes for ehea devices (rh #511304) (rh #516591)
- nm: work around PPP bug causing bogus nameservers for mobile broadband connections
- editor: fix segfault with "Unlisted" plans in the mobile broadband assistant

* Thu Aug 13 2009 Dan Williams <dcbw@redhat.com> - 0.7.995-3.git20090813
- nm: add iSCSI support
- nm: add connection assume/takeover support for ethernet (rh #517333)
- nm: IPv6 fixes
- nm: re-add OLPC XO-1 mesh device support (removed with 0.7.0)
- applet: better WiFi dialog focus handling

* Tue Aug 11 2009 Bastien Nocera <bnocera@redhat.com> 0.7.995-2.git20090804
- Add patch to fix service detection on phones

* Tue Aug  4 2009 Dan Williams <dcbw@redhat.com> - 0.7.995-1.git20090804
- nm: IPv6 support for manual & router-advertisement modes

* Sun Aug  2 2009 Matthias Clasen <mclasen@redhat.com> - 0.7.995-1.git20090728
- Move some big docs to -devel to save space

* Tue Jul 28 2009 Dan Williams <dcbw@redhat.com> - 0.7.995-0.git20090728
- Update to upstream 'master' branch
- Use modem-manager for better 3G modem support
- Integrated system settings with NetworkManager itself
- Use udev instead of HAL

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7.1-9.git20090708
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  9 2009 Dan Williams <dcbw@redhat.com> - 0.7.1-8.git20090708
- applet: fix certificate validation in hidden wifi networks dialog (rh #508207)

* Wed Jul  8 2009 Dan Williams <dcbw@redhat.com> - 0.7.1-7.git20090708
- nm: fixes for ZTE/Onda modem detection
- nm: prevent re-opening serial port when the SIM has a PIN
- applet: updated translations
- editor: show list column headers

* Thu Jun 25 2009 Dan Williams <dcbw@redhat.com> - 0.7.1-6.git20090617
- nm: fix serial port settings

* Wed Jun 17 2009 Dan Williams <dcbw@redhat.com> - 0.7.1-5.git20090617
- nm: fix AT&T Quicksilver modem connections (rh #502002)
- nm: fix support for s390 bus types (rh #496820)
- nm: fix detection of some CMOtech modems
- nm: handle unsolicited wifi scans better
- nm: resolv.conf fixes when using DHCP and overriding search domains
- nm: handle WEP and WPA passphrases (rh #441070)
- nm: fix removal of old APs when none are scanned
- nm: fix Huawei EC121 and EC168C detection and handling (rh #496426)
- applet: save WEP and WPA passphrases instead of hashed keys (rh #441070)
- applet: fix broken notification bubble actions
- applet: default to WEP encryption for Ad-Hoc network creation
- applet: fix crash when connection editor dialogs are canceled
- applet: add a mobile broadband provider wizard

* Tue May 19 2009 Karsten Hopp <karsten@redhat.com> 0.7.1-4.git20090414.1
- drop ExcludeArch s390 s390x, we need at least the header files

* Tue May 05 2009 Adam Jackson <ajax@redhat.com> 1:0.7.1-4.git20090414
- nm-save-the-leases.patch: Use per-connection lease files, and don't delete
  them on interface deactivate.

* Thu Apr 16 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.1-3.git20090414
- ifcfg-rh: fix problems noticing changes via inotify (rh #495884)

* Tue Apr 14 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.1-2.git20090414
- ifcfg-rh: enable write support for wired and wifi connections

* Sun Apr 12 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.1-1
- nm: update to 0.7.1
- nm: fix startup race with HAL causing unmanaged devices to sometimes be managed (rh #494527)

* Wed Apr  8 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.100-2.git20090408
- nm: fix recognition of Option GT Fusion and Option GT HSDPA (nozomi) devices (rh #494069)
- nm: fix handling of spaces in DHCP 'domain-search' option
- nm: fix detection of newer Option 'hso' devices
- nm: ignore low MTUs returned by broken DHCP servers

* Sun Apr  5 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.100-1
- Update to 0.7.1-rc4
- nm: use PolicyKit for system connection secrets retrieval
- nm: correctly interpret errors returned from chmod(2) when saving keyfile system connections
- editor: use PolicyKit to get system connection secrets

* Thu Mar 26 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.99-5
- nm: fix crashes with out-of-tree modules that provide no driver link (rh #492246)
- nm: fix USB modem probing on recent udev versions

* Tue Mar 24 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.99-4
- nm: fix communication with Option GT Max 3.6 mobile broadband cards
- nm: fix communication with Huawei mobile broadband cards (rh #487663)
- nm: don't look up hostname when HOSTNAME=localhost unless asked (rh #490184)
- nm: fix crash during IP4 configuration (rh #491620)
- nm: ignore ONBOOT=no for minimal ifcfg files (f9 & f10 only) (rh #489398)
- applet: updated translations

* Wed Mar 18 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.99-3.5
- nm: work around unhandled device removals due to missing HAL events (rh #484530)
- nm: improve handling of multiple modem ports
- nm: support for Sony Ericsson F3507g / MD300 and Dell 5530
- applet: updated translations

* Mon Mar  9 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.99-3
- Missing ONBOOT should actually mean ONBOOT=yes (rh #489422)

* Mon Mar  9 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.99-2
- Fix conflict with NetworkManager-openconnect (rh #489271)
- Fix possible crash when resynchronizing devices if HAL restarts

* Wed Mar  4 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.99-1
- nm: make default wired "Auto ethX" connection modifiable if an enabled system settings
    plugin supports modifying connections (rh #485555)
- nm: manpage fixes (rh #447233)
- nm: CVE-2009-0365 - GetSecrets disclosure
- applet: CVE-2009-0578 - local users can modify the connection settings
- applet: fix inability to choose WPA Ad-Hoc networks from the menu
- ifcfg-rh: add read-only support for WPA-PSK connections

* Wed Feb 25 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.98-1.git20090225
- Fix getting secrets for system connections (rh #486696)
- More compatible modem autodetection
- Better handle minimal ifcfg files

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7.0.97-6.git20090220
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.97-5.git20090220
- Use IFF_LOWER_UP for carrier detect instead of IFF_RUNNING
- Add small delay before probing cdc-acm driven mobile broadband devices

* Thu Feb 19 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.97-4.git20090219
- Fix PEAP version selection in the applet (rh #468844)
- Match hostname behavior to 'network' service when hostname is localhost (rh #441453)

* Thu Feb 19 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.97-2
- Fix 'noreplace' for nm-system-settings.conf

* Wed Feb 18 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0.97-1
- Update to 0.7.1rc1
- nm: support for Huawei E160G mobile broadband devices (rh #466177)
- nm: fix misleading routing error message (rh #477916)
- nm: fix issues with 32-character SSIDs (rh #485312)
- nm: allow root to activate user connections
- nm: automatic modem detection with udev-extras
- nm: massive manpage rewrite
- applet: fix crash when showing the CA certificate ignore dialog a second time
- applet: clear keyring items when deleting a connection
- applet: fix max signal strength calculation in menu (rh #475123)
- applet: fix VPN export (rh #480496)

* Sat Feb  7 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0-2.git20090207
- applet: fix blank VPN connection message bubbles
- applet: better handling of VPN routing on update
- applet: silence pointless warning (rh #484136)
- applet: desensitize devices in the menu until they are ready (rh #483879)
- nm: Expose WINS servers in the IP4Config over D-Bus
- nm: Better handling of GSM Mobile Broadband modem initialization
- nm: Handle DHCP Classless Static Routes (RFC 3442)
- nm: Fix Mobile Broadband and PPPoE to always use 'noauth'
- nm: Better compatibility with older dual-SSID AP configurations (rh #445369)
- nm: Mark nm-system-settings.conf as config (rh #465633)
- nm-tool: Show VPN connection information
- ifcfg-rh: Silence message about ignoring loopback config (rh #484060)
- ifcfg-rh: Fix issue with wrong gateway for system connections (rh #476089)

* Fri Jan  2 2009 Dan Williams <dcbw@redhat.com> - 1:0.7.0-1.git20090102
- Update to 0.7.1 pre-release
- Allow connections to be ignored when determining the default route (rh #476089)
- Own /usr/share/gnome-vpn-properties (rh #477155)
- Fix log flooding due to netlink errors (rh #459205)
- Pass connection UUID to dispatcher scripts via the environment
- Fix possible crash after deactivating a VPN connection
- Fix issues with editing wired 802.1x connections
- Fix issues when using PKCS#12 certificates with 802.1x connections

* Fri Nov 21 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.12.svn4326
- API and documentation updates
- Fix PIN handling on 'hso' mobile broadband devices

* Tue Nov 18 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.12.svn4296
- Fix PIN/PUK issues with high-speed Option HSDPA mobile broadband cards
- Fix desensitized OK button when asking for wireless keys

* Mon Nov 17 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.12.svn4295
- Fix issues reading ifcfg files
- Previously fixed:
- Doesn't send DHCP hostname (rh #469336)
- 'Auto eth0' forgets settings (rh #468612)
- DHCP renewal sometimes breaks VPN (rh #471852)
- Connection editor menu item in the wrong place (rh #471495)
- Cannot make system-wide connections (rh #471308)

* Fri Nov 14 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.12.svn4293
- Update to NetworkManager 0.7.0 RC2
- Handle gateways on a different subnet from the interface
- Clear VPN secrets on connection failure to ensure they are requested again (rh #429287)
- Add support for PKCS#12 private keys (rh #462705)
- Fix mangling of VPN's default route on DHCP renew
- Fix type detection of qemu/kvm network devices (rh #466340)
- Clear up netmask/prefix confusion in the connection editor
- Make the secrets dialog go away when it's not needed
- Fix inability to add system connections (rh #471308)

* Mon Oct 27 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4229
- More reliable mobile broadband card initialization
- Handle mobile broadband PINs correctly when PPP passwords are also used
- Additional PolicyKit integration for editing system connections
- Close the applet menu if a keyring password is needed (rh #353451)

* Tue Oct 21 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4201
- Fix issues with hostname during anaconda installation (rh #461933)
- Fix Ad-Hoc WPA connections (rh #461197)
- Don't require gnome-panel or gnome-panel-devel (rh #427834)
- Fix determination of WPA encryption capabilities on some cards
- Fix conflicts with PPTP and vpnc plugins
- Allow .cer file extensions when choosing certificates

* Sat Oct 11 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4175
- Fix conflicts for older PPTP VPN plugins

* Sat Oct 11 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4174
- Ensure that mobile broadband cards are powered up before trying to use them
- Hostname changing support (rh #441453)
- Fix mobile broadband secret requests to happen less often
- Better handling of default devices and default routes
- Better information in tooltips and notifications
- Various UI cleanups; hide widgets that aren't used (rh #465397, rh #465395)
- Accept different separators for DNS servers and searches
- Make applet's icon accurately reflect signal strength of the current AP

* Wed Oct  1 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4022.4
- Fix connection comparison that could cause changes to get overwritten (rh #464417)

* Tue Sep 30 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4022.3
- Fix handling of VPN settings on upgrade (rh #460730, bgo #553465)

* Thu Sep 11 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4022.2
- Fix hang when reading system connections from ifcfg files

* Thu Sep  4 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4022.1
- Fix WPA Ad-Hoc connections

* Wed Aug 27 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn4022
- Fix parsing of DOMAIN in ifcfg files (rh #459370)
- Fix reconnection to mobile broadband networks after an auth failure
- Fix recognition of timeouts of PPP during mobile broadband connection
- More compatible connection sharing (rh #458625)
- Fix DHCP in minimal environments without glibc locale information installed
- Add support for Option mobile broadband devices (like iCON 225 and iCON 7.2)
- Add IP4 config information to dispatcher script environment
- Merge WEP ASCII and Hex key types for cleaner UI
- Pre-fill PPPoE password when authentication fails
- Fixed some changes not getting saved in the connection editor
- Accept both prefix and netmask in the conection editor's IPv4 page

* Mon Aug 11 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn3930
- Fix issue with mobile broadband connections that don't require authentication

* Mon Aug 11 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn3927
- Expose DHCP-returned options over D-Bus and to dispatcher scripts
- Add support for customized static routes
- Handle multiple concurrent 3G or PPPoE connections
- Fix GSM/CDMA username and password issues
- Better handling of unmanaged devices from ifcfg files
- Fix timeout handling of errors during 3G connections
- Fix some routing issues (rh #456685)
- Fix applet crashes after removing a device (rh #457380)

* Thu Jul 24 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn3846
- Convert stored IPv4 static IP addresses to new prefix-based scheme automatically
- Fix pppd connections to some 3G providers (rh #455348)
- Make PPPoE "Show Password" option work
- Hide IPv4 config options that don't make sense in certain configurations

* Fri Jul 18 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.11.svn3830
- Expose server-returned DHCP options via D-Bus
- Use avahi-autoipd rather than old built-in IPv4LL implementation
- Send hostname to DHCP server if provided (DHCP_HOSTNAME ifcfg option)
- Support sending DHCP Client Identifier to DHCP server
- Allow forcing 802.1x PEAP Label to '0'
- Make connection sharing more robust
- Show status for shared and Ad-Hoc connections if no other connection is active

* Fri Jul 11 2008 Matthias Clasen <mclasen@redhat.com> - 1:0.7.0-0.10.svn3801
- Drop explicit hal dep in -gnome

* Wed Jul 02 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.10.svn3801
- Move VPN configuration into connection editor
- Fix mobile broadband username/password issues
- Fix issues with broken rfkill setups (rh #448889)
- Honor APN setting for GSM mobile broadband configurations
- Fix adding CDMA connections in the connection editor

* Wed Jun 11 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.10.svn3747
- Update to latest SVN
- Enable connection sharing
- Respect VPN-provided routes

* Wed Jun  4 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.4.svn3675
- Move NM later in the shutdown process (rh #449070)
- Move libnm-util into a subpackage to allow NM to be removed more easily (rh #351101)

* Mon May 19 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.3.svn3675
- Read global gateway from /etc/sysconfig/network if missing (rh #446527)
- nm-system-settings now terminates when dbus goes away (rh #444976)

* Wed May 14 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.3.svn3669
- Fix initial carrier state detection on devices that are already up (rh #134886)

* Tue May 13 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.3.svn3667
- Restore behavior of marking wifi devices as "down" when disabling wireless
- Fix a crash on resume when a VPN was active when going to sleep

* Tue May 13 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.3.svn3665
- Fix issues with the Fedora plugin not noticing changes made by
    system-config-network (rh #444502)
- Allow autoconnection of GSM and CDMA connections
- Multiple IP address support for user connections
- Fixes for Mobile Broadband cards that return line speed on connect
- Implement PIN entry for GSM mobile broadband connections
- Fix crash when editing unencrypted WiFi connections in the connection editor

* Wed Apr 30 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.3.svn3623
- Clean up the dispatcher now that it's service is gone (rh #444798)

* Wed Apr 30 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3623
- Fix asking applets for the GSM PIN/PUK

* Wed Apr 30 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3622
- Guess WEP key type in applet when asking for new keys
- Correct OK button sensitivity in applet when asking for new WEP keys

* Wed Apr 30 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3620
- Fix issues with Mobile Broadband connections caused by device init race patch

* Tue Apr 29 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3619
- Fix device initialization race that caused ethernet devices to get stuck on
    startup
- Fix PPPoE connections not showing up in the applet
- Fix disabled OK button in connection editor some wireless and IP4 settings
- Don't exit if HAL isn't up yet; wait for it
- Fix a suspend/resume crash

* Sun Apr 27 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3614
- Don't ask for wireless keys when the driver sends disconnect events during
	association; wait until the entire assocation times out
- Replace dispatcher daemon with D-Bus activated callout
- Fix parsing of DNS2 and DNS3 ifcfg file items
- Execute dispatcher scripts in alphabetical order
- Be active at runlevel 2
- Hook up MAC address widgets for wired & wireless; and BSSID widget for wireless
- Pre-populate anonymous identity and phase2 widgets correctly
- Clear out unused connection keys from GConf

* Tue Apr 22 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3590
- Don't select devices without a default gateway as the default route (rh #437338)
- Fill in broadcast address if not specified (rh #443474)
- Respect manual VPN IPv4 configuration options
- Show Connection Information for the device with the default route only

* Fri Apr 18 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3578
- Add dbus-glib-devel BuildRequires for NetworkManager-glib-devel (rh #442978)
- Add PPP settings page to connection editor
- Fix a few crashes with PPPoE
- Fix active connection state changes that confused clients 

* Thu Apr 17 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3571
- Fix build in pppd-plugin

* Thu Apr 17 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3570
- PPPoE authentication fixes
- More robust handing of mobile broadband device communications

* Wed Apr 16 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.2.svn3566
- Honor options from /etc/sysconfig/network for blocking until network is up

* Wed Apr 16 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3566
- Turn on Add/Edit in the connection editor
- Don't flush or change IPv6 addresses or routes
- Enhance nm-online tool
- Some serial communication fixes for mobile broadband

* Wed Apr  9 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3549
- Fix issues with VPN passwords not getting found

* Tue Apr  8 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3548
- Fix builds due to glib2 breakage of GStaticMutex with gcc 4.3

* Tue Apr  8 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3547
- Fix WEP key index handling in UI
- Fix handling of NM_CONTROLLED in ifcfg files
- Show device managed state in applet menu
- Show wireless enabled state in applet menu
- Better handling of default DHCP connections for wired devices
- Fix loading of connection editor on KDE (rh #435344)

* Wed Apr  2 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3527
- Honor MAC address locking for wired & wireless devices

* Mon Mar 31 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3521
- Show VPN failures
- Support Static WEP key indexes
- Fix parsing of WEP keys from ifcfg files
- Pre-fill wireless security UI bits in connection editor and applet

* Tue Mar 18 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3476
- Grab system settings from /etc/sysconfig/network-scripts, not from profiles

* Tue Mar 18 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3473
- Fix crashes when returning VPN secrets from the applet to NM

* Tue Mar 18 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3472
- Fix crashes on suspend/resume and exit (rh #437426)
- Ensure there's always an option to chose the wired device
- Never set default route via an IPv4 link-local addressed device (rh #437338)

* Wed Mar 12 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3440
- Fix DHCP rebind behavior
- Preliminary PPPoE support

* Mon Mar 10 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.9.1.svn3417
- Fix gnome-icon-theme Requires, should be on gnome subpackage

* Mon Mar 10 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3417
- Honor DHCP rebinds
- Multiple active device support
- Better error handling of mobile broadband connection failures
- Allow use of interface-specific dhclient config files
- Recognize system settings which have no TYPE item

* Sun Mar  2 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3370
- Fix crash of nm-system-settings on malformed ifcfg files (rh #434919)
- Require gnome-icon-theme to pick up lock.png (rh #435344)
- Fix applet segfault after connection removal via connection editor or GConf

* Fri Feb 29 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3369
- Don't create multiple connections for hidden access points
- Fix scanning behavior

* Thu Feb 14 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3319
- Rework connection editor connection list

* Tue Feb 12 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3312
- Better handling of changes in the profile directory by the system settings
	serivce

* Thu Feb  7 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3302
- Enable system settings service
- Allow explicit disconnection of mobile broadband devices
- Fix applet memory leaks (rh #430178)
- Applet Connection Information dialog tweaks (gnome.org #505899)
- Filter input characters to passphrase/key entry (gnome.org #332951)
- Fix applet focus stealing prevention behavior

* Mon Jan 21 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3261
- Add CDMA mobile broadband support (if supported by HAL)
- Rework applet connection and icon handling
- Enable connection editor (only for deleting connections)

* Fri Jan 11 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3235
- Fix crash when activating a mobile broadband connection
- Better handling of non-SSID-broadcasting APs on kernels that support it
    (gnome.org #464215) (rh #373841)
- Honor DHCP-server provided MTU if present (gnome.org #332953)
- Use previous DNS settings if the VPN concentrator doesn't provide any
    (gnome.org #346833)

* Fri Jan  4 2008 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3204
- Fix WPA passphrase hashing on big endian (PPC, Sparc, etc) (rh #426233)

* Tue Dec 18 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3181
- Fixes to work better with new libnl (rh #401761)

* Tue Dec 18 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3180
- Fix WPA/WPA2 Enterprise Phase2 connections (rh #388471)

* Wed Dec  5 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3138
- Fix applet connection comparison which failed to send connection updated
    signals to NM in some cases
- Make VPN connection applet more robust against plugin failures

* Tue Dec  4 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3134
- 64-bit -Wall compile fixes

* Tue Dec  4 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.8.svn3133
- Fix applet crash when choosing to ignore the CA certificate (rh #359001)
- Fix applet crash when editing VPN properties and VPN connection failures (rh #409351)
- Add file filter name in certificate file picker dialog (rh #410201)
- No longer start named when starting NM (rh #381571)

* Tue Nov 27 2007 Jeremy Katz <katzj@redhat.com> - 1:0.7.0-0.8.svn3109
- Fix upgrading from an earlier rawhide snap

* Mon Nov 26 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.6.svn3109
- Fix device descriptions shown in applet menu

* Mon Nov 26 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.5.svn3109
- Fix crash when deactivating VPN connections

* Mon Nov 19 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.5.svn3096
- Fix crash and potential infinite nag dialog loop when ignoring CA certificates

* Mon Nov 19 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.4.svn3096
- Fix crash when ignoring CA certificate for EAP-TLS, EAP-TTLS, and EAP-PEAP

* Mon Nov 19 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.3.svn3096
- Fix connections when picking a WPA Enterprise AP from the menu
- Fix issue where applet would provide multiple same connections to NM

* Thu Nov 15 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.3.svn3094
- Add support for EAP-PEAP (rh #362251)
- Fix EAP-TLS private key handling

* Tue Nov 13 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.2.svn3080
- Clarify naming of WPA & WPA2 Personal encryption options (rh #374861, rh #373831)
- Don't require a CA certificate for applicable EAP methods (rh #359001)
- Fix certificate and private key handling for EAP-TTLS and EAP-TLS (rh #323371)
- Fix applet crash with USB devices (rh #337191)
- Support upgrades from NM 0.6.x GConf settings

* Thu Nov  1 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.6.1.svn3030
- Fix applet crash with USB devices that don't advertise a product or vendor
    (rh #337191)

* Sat Oct 27 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.5.svn3030
- Fix crash when getting WPA secrets (rh #355041)

* Fri Oct 26 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.4.svn3030
- Bring up ethernet devices by default if no connections are defined (rh #339201)
- Fix crash when switching networks or bringing up secrets dialog (rh #353091)
- Fix crash when editing VPN connection properties a second time
- Fix crash when cancelling the secrets dialog if another connection was
    activated in the mean time
- Fix disembodied notification bubbles (rh #333391)

* Thu Oct 25 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.4.svn3020
- Handle PEM certificates
- Hide WPA-PSK Type combo since it's as yet unused
- Fix applet crash when AP security options changed and old secrets are still
    in the keyring
- Fix applet crash connecting to unencrypted APs via the other network dialog

* Wed Oct 24 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn3020
- Fix WPA Enterprise connections that use certificates
- Better display of SSIDs in the menu

* Wed Oct 24 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn3016
- Fix getting current access point
- Fix WPA Enterprise connections
- Wireless dialog now defaults to sensible choices based on the connection
- Tell nscd to restart if needed, don't silently kill it

* Tue Oct 23 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn3014
- Suppress excessive GConf updates which sometimes caused secrets to be cleared
    at the wrong times, causing connections to fail
- Various EAP and LEAP related fixes

* Tue Oct 23 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn3008
- Make WPA-EAP and Dynamic WEP options connect successfully
- Static IPs are now handled correctly in NM itself

* Mon Oct 22 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2995
- Add Dynamic WEP as a supported authentication/security option

* Sun Oct 21 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2994
- Re-enable "Connect to other network"
- Switch to new GUI bits for wireless security config and password entry

* Tue Oct 16 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2983
- Add rfkill functionality
- Fix applet crash when choosing wired networks from the menu

* Wed Oct 10 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2970
- Fix segfault with deferred connections
- Fix default username with vpnc VPN plugin
- Hidden SSID fixes

* Tue Oct  9 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2962
- Fix merging of non-SSID-broadcasting APs into a device's scan list
- Speed up opening of the applet menu

* Tue Oct  9 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2961
- New snapshot
	- Add timestamps to networks to connect to last used wireless network
	- Turn autoconnect on in the applet
	- Hidden SSID support
	- Invalidate failed or cancelled connections again
	- Fix issues with reactivation of the same device
	- Handle connection updates in the applet (ex. find new VPN connections)
	- Fix vertical sizing of menu items
	- Fix AP list on wireless devices other than the first device in the applet
	- Fix matching of current AP with the right menu item

* Fri Sep 28 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2914
- New snapshot
	- Add WPA passphrase support to password dialog
	- Applet now reflects actual VPN behavior of one active connection
	- Applet now notices VPN active connections on startup
	- Fix connections with some WPA and WEP keys

* Thu Sep 27 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2907
- New snapshot
	- VPN support (only vpnc plugin ported at this time)

* Tue Sep 25 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2886
- New snapshot
	- Make wired device carrier state work in the applet
	- Fix handling of errors with unencrypted APs
	- Fix "frozen" applet icon by reporting NM state better
	- Fix output of AP frequency in nm-tool

* Tue Sep 25 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2880
- New snapshot
	- Fix applet icon sizing on start (mclasen)
	- Fix nm-tool installation (mclasen)
	- Fix 'state' method call return (#303271)
	- Fix 40-bit WEP keys (again)
	- Fix loop when secrets were wrong/invalid
	- Fix applet crash when clicking Cancel in the password dialog
	- Ensure NM doesn't get stuck waiting for the supplicant to re-appear
		if it crashes or goes away
	- Make VPN properties applet work again
	- Increase timeout for network password entry

* Fri Sep 21 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2852
- New snapshot (fix unencrypted & 40 bit WEP)

* Fri Sep 21 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2849
- New snapshot

* Fri Sep 21 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.3.svn2844
- New snapshot

* Thu Sep 20 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.2.svn2833
- New SVN snapshot of 0.7 that sucks less

* Thu Aug 30 2007 Dan Williams <dcbw@redhat.com> - 1:0.7.0-0.1.svn2736
- Update to SVN snapshot of 0.7

* Mon Aug 13 2007 Christopher Aillon <caillon@redhat.com> 1:0.6.5-9
- Update the license tag

* Wed Aug  8 2007 Christopher Aillon <caillon@redhat.com> 1:0.6.5-8
- Own /etc/NetworkManager/dispatcher.d and /etc/NetworkManager/VPN (#234004)

* Wed Jun 27 2007 Dan Williams <dcbw@redhat.com> 1:0.6.5-7
- Fix Wireless Enabled checkbox when no killswitches are present

* Thu Jun 21 2007 Dan Williams <dcbw@redhat.com> 1:0.6.5-6
- Update to stable branch snapshot:
    - More fixes for ethernet link detection (gnome #354565, rh #194124)
    - Support for HAL-detected rfkill switches

* Sun Jun 10 2007 Dan Williams <dcbw@redhat.com> 1:0.6.5-5
- Fix applet crash on 64-bit platforms when choosing
    "Connect to other wireless network..." (gnome.org #435036)
- Add debug output for ethernet device link changes

* Thu Jun  7 2007 Dan Williams <dcbw@redhat.com> 1:0.6.5-4
- Fix ethernet link detection (gnome #354565, rh #194124)
- Fix perpetual credentials request with private key passwords in the applet
- Sleep a bit before activating wireless cards to work around driver bugs

* Mon Jun  4 2007 Dan Williams <dcbw@redhat.com> 1:0.6.5-3
- Don't spawn wpa_supplicant with -o

* Wed Apr 25 2007 Christopher Aillon <caillon@redhat.com> 1:0.6.5-2
- Fix requires macro (237806)

* Thu Apr 19 2007 Christopher Aillon <caillon@redhat.com> 1:0.6.5-1
- Update to 0.6.5 final
- Don't lose scanned security information

* Mon Apr  9 2007 Dan Williams <dcbw@redhat.com> - 1:0.6.5-0.7.svn2547
- Update from trunk
	* Updated translations
	* Cleaned-up VPN properties dialogs
	* Fix 64-bit kernel leakage issues in WEXT
	* Don't capture and redirect wpa_supplicant log output

* Wed Mar 28 2007 Matthew Barnes  <mbarnes@redhat.com> 1:0.6.5-0.6.svn2474
- Close private D-Bus connections. (#232691)

* Sun Mar 25 2007 Matthias Clasen <mclasen@redhat.com> 1:0.6.5-0.5.svn2474
- Fix a directory ownership issue.  (#233763)

* Thu Mar 15 2007 Dan Williams <dcbw@redhat.com> - 1:0.6.5-0.4.svn2474
- Update to pre-0.6.5 snapshot

* Thu Feb  8 2007 Christopher Aillon <caillon@redhat.com> - 1:0.6.5-0.3.cvs20061025
- Guard against D-Bus LimitExceeded messages

* Fri Feb  2 2007 Christopher Aillon <caillon@redhat.com> - 1:0.6.5-0.2.cvs20061025
- Move .so file to -devel package

* Sat Nov 25 2006 Matthias Clasen <mclasen@redhat.com> 
- Own the /etc/NetworkManager/dispatcher.d directory
- Require pkgconfig for the -devel packages
- Fix compilation with dbus 1.0

* Wed Oct 25 2006 Dan Williams <dcbw@redhat.com> - 1:0.6.5-0.cvs20061025
- Update to a stable branch snapshot
    - Gnome applet timeout/redraw suppression when idle
    - Backport of LEAP patch from HEAD (from Thiago Bauermann)
    - Backport of asynchronous scanning patch from HEAD
    - Make renaming of VPN connections work (from Tambet Ingo)
    - Dial down wpa_supplicant debug spew
    - Cleanup of key/passphrase request scenarios (from Valentine Sinitsyn)
    - Shut down VPN connections on logout (from Robert Love)
    - Fix WPA passphrase hashing on PPC

* Thu Oct 19 2006 Christopher Aillon <caillon@redhat.com> - 1:0.6.4-6
- Own /usr/share/NetworkManager and /usr/include/NetworkManager

* Mon Sep  4 2006 Christopher Aillon <caillon@redhat.com> - 1:0.6.4-5
- Don't wake up to redraw if NM is inactive (#204850)

* Wed Aug 30 2006 Bill Nottingham <notting@redhat.com> - 1:0.6.4-4
- add epochs in requirements

* Wed Aug 30 2006 Dan Williams <dcbw@redhat.com> - 1:0.6.4-3
- Fix FC-5 buildreqs

* Wed Aug 30 2006 Dan Williams <dcbw@redhat.com> - 1:0.6.4-2
- Revert FC6 to latest stable NM
- Update to stable snapshot
- Remove bind/caching-nameserver hard requirement

* Tue Aug 29 2006 Christopher Aillon <caillon@redhat.com> - 0.7.0-0.cvs20060529.7
- BuildRequire wireless-tools-devel and perl-XML-Parser
- Update the BuildRoot tag

* Wed Aug 16 2006 Ray Strode <rstrode@redhat.com> - 0.7.0-0.cvs20060529.6
- add patch to make networkmanager less verbose (bug 202832)

* Wed Aug  9 2006 Ray Strode <rstrode@redhat.com> - 0.7.0-0.cvs20060529.5
- actually make the patch in 0.7.0-0.cvs20060529.4 apply

* Fri Aug  4 2006 Ray Strode <rstrode@redhat.com> - 0.7.0-0.cvs20060529.4
- Don't ever elect inactive wired devices (bug 194124).

* Wed Jul 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.7.0-0.cvs20060529.3
- Add patch to fix deprecated dbus functions

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.7.0-0.cvs20060529.2
- Add BR for dbus-glib-devel

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.7.0-0.cvs20060529.1.1
- rebuild

* Mon May 29 2006 Dan Williams <dcbw@redhat.com> - 0.7.0-0.cvs20060529
- Update to latest CVS
	o Gnome.org #333420: dialog do not have window icons
	o Gnome.org #336913: HIG tweaks for vpn properties pages
	o Gnome.org #336846: HIG tweaks for nm-vpn-properties
	o Gnome.org #336847: some bugs in nm-vpn-properties args parsing
	o Gnome.org #341306: nm-vpn-properties crashes on startup
	o Gnome.org #341263: Version 0.6.2-0ubuntu5 crashes on nm_device_802_11_wireless_get_type
	o Gnome.org #341297: displays repeated keyring dialogs on resume from suspend
	o Gnome.org #342400: Building libnm-util --without-gcrypt results in linker error
	o Gnome.org #342398: Eleminate Gnome dependency for NetworkManager
	o Gnome.org #336532: declaration of 'link' shadows a global declaration
- Specfile fixes (#rh187489#)

* Sun May 21 2006 Dan Williams <dcbw@redhat.com> - 0.7.0-0.cvs20060521
- Update to latest CVS
- Drop special-case-madwifi.patch, since WEXT code is in madwifi-ng trunk now

* Fri May 19 2006 Bill Nottingham <notting@redhat.com> - 0.6.2-3.fc6
- use the same 0.6.2 tarball as FC5, so we have the same VPN interface
  (did he fire ten args, or only nine?)

* Thu Apr 27 2006 Jeremy Katz <katzj@redhat.com> - 0.6.2-2.fc6
- use the hal device type instead of poking via ioctl so that wireless 
  devices are properly detected even if the kill switch has been used

* Thu Mar 30 2006 Dan Williams <dcbw@redhat.com> - 0.6.2-1
- Update to 0.6.2:
	* Fix various WPA-related bugs
	* Clean up leaks
	* Increased DHCP timeout to account for slow DHCP servers, or STP-enabled
		switches
	* Allow applet to reconnect on dbus restarts
	* Add "Dynamic WEP" support
	* Allow hiding of password/key entry text
	* More responsive connection switching

* Tue Mar 14 2006 Peter Jones <pjones@redhat.com> - 0.6.0-3
- Fix device bringup on resume

* Mon Mar  6 2006 Dan Williams <dcbw@redhat.com> 0.6.0-2
- Don't let wpa_supplicant perform scanning with non-WPA drivers

* Mon Mar  6 2006 Dan Williams <dcbw@redhat.com> 0.6.0-1
- Update to 0.6.0 release
- Move autostart file to /usr/share/gnome/autostart

* Thu Mar  2 2006 Jeremy Katz <katzj@redhat.com> - 0.5.1-18.cvs20060302
- updated cvs snapshot.  seems to make airo much less neurotic

* Thu Mar  2 2006 Christopher Aillon <caillon@redhat.com>
- Move the unversioned libnm_glib.so to the -devel package

* Wed Mar  1 2006 Dan Williams <dcbw@redhat.com> 0.5.1-18.cvs20060301
- Fix VPN-related crash
- Fix issue where NM would refuse to activate a VPN connection once it had timed out
- Log wpa_supplicant output for better debugging

* Tue Feb 28 2006 Christopher Aillon <caillon@redhat.com> 0.5.1-17.cvs20060228
- Tweak three-scan-prune.patch

* Mon Feb 27 2006 Christopher Aillon <caillon@redhat.com> 0.5.1-16.cvs20060227
- Don't prune networks until they've gone MIA for three scans, not one.

* Mon Feb 27 2006 Christopher Aillon <caillon@redhat.com> 0.5.1-15.cvs20060227
- Update snapshot, which fixes up the libnotify stuff.

* Fri Feb 24 2006 Dan Williams <dcbw@redhat.coM> 0.5.1-14.cvs20060221
- Move libnotify requires to NetworkManager-gnome, not core NM package

* Tue Feb 21 2006 Dan Williams <dcbw@redhat.com> 0.5.1-13.cvs20060221
- Add BuildRequires: libnl-devel (#rh179438#)
- Fix libnm_glib to not clobber an application's existing dbus connection
	(#rh177546#, gnome.org #326572)
- libnotify support
- AP compatibility fixes

* Mon Feb 13 2006 Dan Williams <dcbw@redhat.com> 0.5.1-12.cvs20060213
- Minor bug fixes
- Update to VPN dbus API for passing user-defined routes to vpn service

* Sun Feb 12 2006 Christopher Aillon <caillon@redhat.com> 0.5.1-11.cvs20060205
- Rebuild

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 0.5.1-10.cvs20060205.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sun Feb  5 2006 Dan Williams <dcbw@redhat.com> 0.5.1-10.cvs20060205
- Workarounds for madwifi/Atheros cards
- Do better with non-SSID-broadcasting access points
- Fix hangs when access points change settings

* Thu Feb  2 2006 Dan Williams <dcbw@redhat.com> 0.5.1-9.cvs20060202
- Own /var/run/NetworkManager, fix SELinux issues

* Tue Jan 31 2006 Dan Williams <dcbw@redhat.com> 0.5.1-8.cvs20060131
- Switch to autostarting the applet instead of having it be session-managed
- Work better with non-broadcasting access points
- Add more manufacturer default SSIDs to the blacklist

* Tue Jan 31 2006 Dan Williams <dcbw@redhat.com> 0.5.1-7.cvs20060131
- Longer association timeout
- Fix some SELinux issues
- General bug and cosmetic fixes

* Fri Jan 27 2006 Dan Williams <dcbw@redhat.com> 0.5.1-6.cvs20060127
- Snapshot from CVS
- WPA Support!  Woohoo!

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec 01 2005 John (J5) Palmieri <johnp@redhat.com> - 0.5.1-5
- rebuild for new dbus

* Fri Nov 18 2005 Peter Jones <pjones@redhat.com> - 0.5.1-4
- Don't kill the network connection when you upgrade the package.

* Fri Oct 21 2005 Christopher Aillon <caillon@redhat.com> - 0.5.1-3
- Split out the -glib subpackage to have a -glib-devel package as well
- Add epoch to version requirements for bind and wireless-tools
- Update URL of project

* Wed Oct 19 2005 Christopher Aillon <caillon@redhat.com> - 0.5.1-2
- NetworkManager 0.5.1

* Mon Oct 17 2005 Christopher Aillon <caillon@redhat.com> - 0.5.0-2
- NetworkManager 0.5.0

* Mon Oct 10 2005 Dan Williams <dcbw@redaht.com> - 0.4.1-5.cvs20051010
- Fix automatic wireless connections
- Remove usage of NMLoadModules callout, no longer needed
- Try to fix deadlock when menu is down and keyring dialog pops up

* Sun Oct 09 2005 Dan Williams <dcbw@redhat.com> - 0.4.1-4.cvs20051009
- Update to latest CVS
	o Integrate connection progress with applet icon (Chris Aillon)
	o More information in "Connection Information" dialog (Robert Love)
	o Shorten time taken to sleep
	o Make applet icon wireless strength levels a bit more realistic
	o Talk to named using DBUS rather than spawning our own
		- You need to add "-D" to the OPTIONS line in /etc/sysconfig/named
		- You need to set named to start as a service on startup

* Thu Sep 22 2005 Dan Williams <dcbw@redhat.com> - 0.4.1-3.cvs20050922
- Update to current CVS to fix issues with routing table and /sbin/ip

* Mon Sep 12 2005 Jeremy Katz <katzj@redhat.com> - 0.4.1-2.cvs20050912
- update to current CVS and rebuild (workaround for #168120)

* Fri Aug 19 2005 Dan Williams <dcbw@redhat.com> - 0.4.1-2.cvs20050819
- Fix occasional hang in NM caused by the applet

* Wed Aug 17 2005 Dan Williams <dcbw@redhat.com> - 0.4.1
- Update to NetworkManager 0.4.1

* Tue Aug 16 2005 Dan Williams <dcbw@redhat.com> - 0.4-36.cvs20050811
- Rebuild against new cairo/gtk

* Thu Aug 11 2005 Dan Williams <dcbw@redhat.com> - 0.4-35.cvs20050811
- Update to latest CVS
	o Use DHCP server address as gateway address if the DHCP server doesn't give
		us a gateway address #rh165698#
	o Fixes to the applet (Robert Love)
	o Better caching of information in the applet (Bill Moss)
	o Generate automatic suggested Ad-Hoc network name from machine's hostname
		(Robert Love)
	o Update all network information on successfull connect, not just 
		authentication method

* Fri Jul 29 2005 Ray Strode  <rstrode@redhat.com> - 0.4-34.cvs20050729
- Update to latest CVS to get fix for bug 165683.

* Mon Jul 11 2005 Dan Williams <dcbw@redhat.com> - 0.4-34.cvs20050629
- Move pkgconfig file to devel package (#162316, thanks to Michael Schwendt)

* Wed Jun 29 2005 David Zeuthen <davidz@redhat.com> - 0.4-33.cvs20050629
- Update to latest CVS to get latest VPN interface settings to satisfy
  BuildReq for NetworkManager-vpnc in Fedora Extras Development
- Latest CVS also contains various bug- and UI-fixes

* Fri Jun 17 2005 Dan Williams <dcbw@redhat.com> - 0.4-32.cvs20050617
- Update to latest CVS
	o VPN connection import/export capability
	o Fix up some menu item names
- Move nm-vpn-properties.glade to the gnome subpackage

* Thu Jun 16 2005 Dan Williams <dcbw@redhat.com> - 0.4-31.cvs20050616
- Update to latest CVS
	o Clean up wording in Wireless Network Discovery menu
	o Robert Love's applet beautify patch

* Wed Jun 15 2005 Dan Williams <dcbw@redhat.com> - 0.4-30.cvs20050615
- Update to latest CVS

* Mon May 16 2005 Dan Williams <dcbw@redhat.com> - 0.4-15.cvs30050404
- Fix dispatcher and applet CFLAGS so they gets compiled with FORTIFY_SOURCE

* Mon May 16 2005 Dan Williams <dcbw@redhat.com> - 0.4-14.cvs30050404
- Fix segfault in NetworkManagerDispatcher, add an initscript for it

* Mon May 16 2005 Dan Williams <dcbw@redhat.com> - 0.4-13.cvs30050404
- Fix condition that may have resulted in DHCP client returning success
	when it really timed out

* Sat May 14 2005 Dan Williams <dcbw@redhat.com> - 0.4-12.cvs20050404
- Enable OK button correctly in Passphrase and Other Networks dialogs when
	using ASCII or Hex WEP keys

* Thu May  5 2005 Dan Williams <dcbw@redhat.com> - 0.4-11.cvs20050404
- #rh154391# NetworkManager dies on startup (don't force-kill nifd)

* Wed May  4 2005 Dan Williams <dcbw@redhat.com> - 0.4-10.cvs20050404
- Fix leak of a socket in DHCP code

* Wed May  4 2005 Dan Williams <dcbw@redhat.com> - 0.4-9.cvs20050404
- Fix some memory leaks (Tom Parker)
- Join to threads rather than spinning for their completion (Tom Parker)
- Fix misuse of a g_assert() (Colin Walters)
- Fix return checking of an ioctl() (Bill Moss)
- Better detection and matching of hidden access points (Bill Moss)
- Don't use varargs, and therefore don't crash on PPC (Peter Jones)

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 0.4-8.cvs20050404
- fix build with newer dbus

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 0.4-7.cvs20050404
- silence %%post

* Mon Apr  4 2005 Dan Williams <dcbw@redhat.com> 0.4-6.cvs20050404
- #rh153234# NetworkManager quits/cores just as a connection is made

* Sat Apr  2 2005 Dan Williams <dcbw@redhat.com> 0.4-5.cvs20050402
- Update from latest CVS HEAD

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com> 0.4-4.cvs20050315
- Update the GTK+ theme icon cache on (un)install

* Tue Mar 15 2005 Ray Strode <rstrode@redhat.com> 0.4-3.cvs20050315
- Pull from latest CVS HEAD

* Tue Mar 15 2005 Ray Strode <rstrode@redhat.com> 0.4-2.cvs20050315
- Upload new source tarball (woops)

* Tue Mar 15 2005 Ray Strode <rstrode@redhat.com> 0.4-1.cvs20050315
- Pull from latest CVS HEAD (hopefully works again)

* Mon Mar  7 2005 Ray Strode <rstrode@redhat.com> 0.4-1.cvs20050307
- Pull from latest CVS HEAD
- Commit broken NetworkManager to satisfy to dbus dependency

* Fri Mar  4 2005 Dan Williams <dcbw@redhat.com> 0.3.4-1.cvs20050304
- Pull from latest CVS HEAD
- Rebuild for gcc 4.0

* Tue Feb 22 2005 Dan Williams <dcbw@redhat.com> 0.3.3-2.cvs20050222
- Update from CVS

* Mon Feb 14 2005 Dan Williams <dcbw@redhat.com> 0.3.3-2.cvs20050214.x.1
- Fix free of invalid pointer for multiple search domains

* Mon Feb 14 2005 Dan Williams <dcbw@redhat.com> 0.3.3-2.cvs20050214
- Never automatically choose a device that doesn't support carrier detection
- Add right-click menu to applet, can now "Pause/Resume" scanning through it
- Fix DHCP Renew/Rebind timeouts
- Fix frequency cycling problem on some cards, even when scanning was off
- Play better with IPv6
- Don't send kernel version in DHCP packets, and ensure DHCP packets are at
	least 300 bytes in length to work around broken router
- New DHCP options D-BUS API by Dan Reed
- Handle multiple domain search options in DHCP responses

* Wed Feb  2 2005 Dan Williams <dcbw@redhat.com> 0.3.3-1.cvs20050202
- Display wireless network name in applet tooltip
- Hopefully fix double-default-route problem
- Write out valid resolv.conf when we exit
- Make multi-domain search options work
- Rework signal strength code to be WEXT conformant, if strength is
	still wierd then its 95% surely a driver problem
- Fix annoying instances of suddenly dropping and reactivating a
	wireless device (Cisco cards were worst offenders here)
- Fix some instances of NetworkManager not remembering your WEP key
- Fix some races between NetworkManager and NetworkManagerInfo where
	NetworkManager wouldn't recognize changes in the allowed list
- Don't shove Ad-Hoc Access Point MAC addresses into GConf

* Tue Jan 25 2005 Dan Williams <dcbw@redhat.com> 0.3.3-1.cvs20050125
- Play nice with dbus 0.23
- Update our list of Allowed Wireless Networks more quickly

* Mon Jan 24 2005 Dan Williams <dcbw@redhat.com> 0.3.3-1.cvs20050124
- Update to latest CVS
- Make sure we start as late as possible so that we ensure dbus & HAL
	are already around
- Fix race in initial device activation

* Mon Jan 24 2005 Than Ngo <than@redhat.com> 0.3.3-1.cvs20050112.4
- rebuilt against new wireless tool

* Fri Jan 21 2005 <dcbw@redhat.com> - 0.3.3-1.cvs20050118
- Fix issue where NM wouldn't recognize that access points were
	encrypted, and then would try to connect without encryption
- Refine packaging to put client library in separate package
- Remove bind+caching-nameserver dep for FC-3, use 'nscd -i hosts'
	instead.  DNS queries may timeout now right after device
	activation due to this change.

* Wed Jan 12 2005 <dcbw@redhat.com> - 0.3.3-1.cvs20050112
- Update to latest CVS
- Fixes to DHCP code
- Link-Local (ZeroConf/Rendezvous) support
- Use bind in "caching-nameserver" mode to work around stupidity
	in glibc's resolver library not recognizing resolv.conf changes
- #rh144818# Clean up the specfile (Patch from Matthias Saou)
- Ad-Hoc mode support with Link-Local addressing only (for now)
- Fixes for device activation race conditions
- Wireless scanning in separate thread

* Wed Dec  8 2004 <dcbw@redhat.com> - 0.3.2-4.3.cvs20041208
- Update to CVS
- Updates to link detection, DHCP code
- Remove NMLaunchHelper so we start up faster and don't
	block for a connection.  This means services that depend
	on the network may fail if they start right after NM
- Make sure DHCP renew/rebinding works

* Wed Nov 17 2004 <dcbw@redhat.com> - 0.3.2-3.cvs20041117
- Update to CVS
- Fixes to link detection
- Better detection of non-ESSID-broadcasting access points
- Don't dialog-spam the user if a connection fails

* Thu Nov 11 2004 <dcbw@redhat.com> - 0.3.2-2.cvs20041115
- Update to CVS
- Much better link detection, works with Open System authentication
- Blacklist wireless cards rather than whitelisting them

* Fri Oct 29 2004 <dcbw@redhat.com> - 0.3.2-2.cvs20041029
- #rh134893# NetworkManagerInfo and the panel-icon life-cycle
- #rh134895# Status icon should hide when in Wired-only mode
- #rh134896# Icon code needs rewrite
- #rh134897# "Other Networks..." dialog needs implementing
- #rh135055# Menu highlights incorrectly in NM
- #rh135648# segfault with cipsec0
- #rh135722# NetworkManager will not allow zaurus to sync via usb0
- #rh135999# NetworkManager-0.3.1 will not connect to 128 wep
- #rh136866# applet needs tooltips
- #rh137047# lots of applets, yay!
- #rh137341# Network Manager dies after disconnecting from wired network second time
- Better checking for wireless devices
- Fix some memleaks
- Fix issues with dhclient declining an offered address
- Fix an activation thread deadlock
- More accurately detect "Other wireless networks" that are encrypted
- Don't bring devices down as much, won't hotplug-spam as much anymore
	about firmware
- Add a "network not found" dialog when the user chooses a network that could
	not be connected to

* Tue Oct 26 2004 <dcbw@redhat.com> - 0.3.1-2
- Fix escaping of ESSIDs in gconf

* Tue Oct 19 2004  <jrb@redhat.com> - 0.3.1-1
- minor point release to improve error handling and translations

* Fri Oct 15 2004 Dan Williams <dcbw@redhat.com> 0.3-1
- Update from CVS, version 0.3

* Tue Oct 12 2004 Dan Williams <dcbw@redhat.com> 0.2-4
- Update from CVS
- Improvements:
	o Better link checking on wireless cards
	o Panel applet now a Notification Area icon
	o Static IP configuration support

* Mon Sep 13 2004 Dan Williams <dcbw@redhat.com> 0.2-3
- Update from CVS

* Sat Sep 11 2004 Dan Williams <dcbw@redhat.com> 0.2-2
- Require gnome-panel, not gnome-panel-devel
- Turn off by default

* Thu Aug 26 2004 Dan Williams <dcbw@redhat.com> 0.2-1
- Update to 0.2

* Thu Aug 26 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- spec-changes to req glib2 instead of glib

* Fri Aug 20 2004 Dan Williams <dcbw@redhat.com> 0.1-3
- First public release
