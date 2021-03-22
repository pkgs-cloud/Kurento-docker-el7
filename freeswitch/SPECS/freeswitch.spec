%define nonparsedversion 1.10.5.-release
%define version %(echo '%{nonparsedversion}' | sed 's/\.-.*//g')
%define release 1

# disable rpath checking
%define __arch_install_post /usr/lib/rpm/check-buildroot
%define _prefix   /usr
%define prefix    %{_prefix}
%define sysconfdir	/etc/freeswitch
%define _sysconfdir	%{sysconfdir}
%define logfiledir	/var/log/freeswitch
%define _logfiledir	%{logfiledir}
%define runtimedir	/var/run/freeswitch
%define _runtimedir	%{runtimedir}

# Layout of packages FHS (Redhat/SUSE), FS (Standard FreeSWITCH layout using /usr/local), OPT (/opt based layout)
%define packagelayout	FHS

%define	PREFIX		%{_prefix}
%define EXECPREFIX	%{_exec_prefix}
%define BINDIR		%{_bindir}
%define SBINDIR		%{_sbindir}
%define LIBEXECDIR	%{_libexecdir}/%name
%define SYSCONFDIR	%{_sysconfdir}/%name
%define SHARESTATEDIR	%{_sharedstatedir}/%name
%define LOCALSTATEDIR	%{_localstatedir}/lib/%name
%define LIBDIR		%{_libdir}
%define INCLUDEDIR	%{_includedir}
%define _datarootdir	%{_prefix}/share
%define DATAROOTDIR	%{_datarootdir}
%define DATADIR		%{_datadir}
%define INFODIR		%{_infodir}
%define LOCALEDIR	%{_datarootdir}/locale
%define MANDIR		%{_mandir}
%define DOCDIR		%{_defaultdocdir}/%name
%define HTMLDIR		%{_defaultdocdir}/%name/html
%define DVIDIR		%{_defaultdocdir}/%name/dvi
%define PDFDIR		%{_defaultdocdir}/%name/pdf
%define PSDIR		%{_defaultdocdir}/%name/ps
%define LOGFILEDIR	/var/log/%name
%define MODINSTDIR	%{_libdir}/%name/mod
%define RUNDIR		%{_localstatedir}/run/%name
%define DBDIR		%{LOCALSTATEDIR}/db
%define HTDOCSDIR	%{_datarootdir}/%name/htdocs
%define SOUNDSDIR	%{_datarootdir}/%name/sounds
%define GRAMMARDIR	%{_datarootdir}/%name/grammar
%define SCRIPTDIR	%{_datarootdir}/%name/scripts
%define FONTSDIR	%{_datarootdir}/%name/fonts
%define RECORDINGSDIR	%{LOCALSTATEDIR}/recordings
%define PKGCONFIGDIR	%{_datarootdir}/%name/pkgconfig
%define HOMEDIR		%{LOCALSTATEDIR}


Name:         	freeswitch
Summary:      	FreeSWITCH open source telephony platform
License:      	MPL1.1
Group:        	Productivity/Telephony/Servers
Version:	      %{version}
Release:	      %{release}%{?dist}
URL:          	http://www.freeswitch.org/
Packager:     	Ken Rice
Vendor:       	http://www.freeswitch.org/
Source0:        http://files.freeswitch.org/freeswitch-releases/%{name}-%{nonparsedversion}.tar.bz2
Source1:				freeswitch.service
Prefix:        	%{_prefix}

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: bzip2
BuildRequires: curl-devel
BuildRequires: gcc-c++
BuildRequires: gnutls-devel
BuildRequires: libtool >= 1.5.17
BuildRequires: ncurses-devel
BuildRequires: openssl-devel >= 1.0.1e
BuildRequires: sofia-sip-devel >= 1.13.1
BuildRequires: spandsp3-devel >= 3.0
BuildRequires: pcre-devel
BuildRequires: speex-devel
BuildRequires: sqlite-devel
BuildRequires: libedit-devel
BuildRequires: lua-devel
BuildRequires: yasm
BuildRequires: ldns-devel
BuildRequires: pkgconfig
BuildRequires: libxml2-devel
BuildRequires: libsndfile-devel
BuildRequires: opusfile-devel >= 0.5
BuildRequires: opus-devel >= 1.1
BuildRequires: ffmpeg-devel >= 4.2

Requires: curl
Requires: ncurses
Requires: pcre
Requires: speex
Requires: sqlite
Requires: libedit
Requires: ldns
Requires: openssl >= 1.0.1e
Requires: libxml2
Requires: libsndfile
Requires:	opusfile >= 0.5
Requires: opus >= 1.1
Requires: ffmpeg-libs >= 4.2

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
FreeSWITCH is an open source telephony platform designed to facilitate the creation of voice
and chat driven products scaling from a soft-phone up to a soft-switch.  It can be used as a
simple switching engine, a media gateway or a media server to host IVR applications using
simple scripts or XML to control the callflow.

We support various communication technologies such as SIP, H.323 and GoogleTalk making
it easy to interface with other open source PBX systems such as sipX, OpenPBX, Bayonne, YATE or Asterisk.

We also support both wide and narrow band codecs making it an ideal solution to bridge legacy
devices to the future. The voice channels and the conference bridge module all can operate
at 8, 16 or 32 kilohertz and can bridge channels of different rates.

FreeSWITCH runs on several operating systems including Windows, Max OS X, Linux, BSD and Solaris
on both 32 and 64 bit platforms.

Our developers are heavily involved in open source and have donated code and other resources to
other telephony projects including sipXecs, OpenSER, Asterisk, CodeWeaver and OpenPBX.

%package devel
Summary:        Development package for FreeSWITCH open source telephony platform
Group:          System/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
FreeSWITCH development files

%prep
%setup -b0 -q -n %{name}-%{nonparsedversion}

#Hotfix for redefined %_sysconfdir
sed -ie 's:confdir="${sysconfdir}/freeswitch":confdir="$sysconfdir":' ./configure.ac

%build
%if 0%{?amzn2}
export CFLAGS="$CFLAGS -Wno-implicit-function-declaration -Wno-expansion-to-defined"
%endif

%if 0%{?fedora_version} >= 8
export QA_RPATHS=$[ 0x0001|0x0002 ]
%endif

APPLICATION_MODULES_AC="applications/mod_av applications/mod_commands applications/mod_conference"

APPLICATION_MODULES_DE="applications/mod_db applications/mod_dptools applications/mod_enum applications/mod_esf \
			applications/mod_expr"

APPLICATION_MODULES_FR="applications/mod_fifo applications/mod_fsv applications/mod_hash applications/mod_httapi"

APPLICATION_MODULES_SZ="applications/mod_sms applications/mod_spandsp \
			applications/mod_valet_parking applications/mod_voicemail"

APPLICATIONS_MODULES="$APPLICATION_MODULES_AC $APPLICATION_MODULES_DE $APPLICATION_MODULES_FR $APPLICATION_MODULES_SZ"
CODECS_MODULES="codecs/mod_amr codecs/mod_b64 codecs/mod_g723_1 codecs/mod_g729 codecs/mod_h26x codecs/mod_opus"
DIALPLANS_MODULES="dialplans/mod_dialplan_asterisk dialplans/mod_dialplan_xml"
DIRECTORIES_MODULES=""
ENDPOINTS_MODULES="endpoints/mod_loopback endpoints/mod_rtc endpoints/mod_skinny endpoints/mod_sofia endpoints/mod_verto"
EVENT_HANDLERS_MODULES="event_handlers/mod_cdr_csv event_handlers/mod_cdr_sqlite event_handlers/mod_event_socket"
FORMATS_MODULES="formats/mod_local_stream formats/mod_native_file formats/mod_opusfile \
                 formats/mod_png formats/mod_sndfile formats/mod_tone_stream"
LANGUAGES_MODULES="languages/mod_lua"
LOGGERS_MODULES="loggers/mod_console loggers/mod_logfile loggers/mod_syslog"
SAY_MODULES="say/mod_say_en"
XML_INT_MODULES="xml_int/mod_xml_cdr xml_int/mod_xml_rpc xml_int/mod_xml_scgi"

MYMODULES="$APPLICATIONS_MODULES $CODECS_MODULES $DIALPLANS_MODULES $DIRECTORIES_MODULES \
$ENDPOINTS_MODULES $EVENT_HANDLERS_MODULES $FORMATS_MODULES $LANGUAGES_MODULES $LOGGERS_MODULES \
$SAY_MODULES $XML_INT_MODULES"

export MODULES=$MYMODULES
test ! -f  modules.conf || rm -f modules.conf
touch modules.conf
for i in $MODULES; do echo $i >> modules.conf; done
export VERBOSE=yes
export DESTDIR=%{buildroot}/
export PKG_CONFIG_PATH=/usr/bin/pkg-config:$PKG_CONFIG_PATH
export ACLOCAL_FLAGS="-I /usr/share/aclocal"

if test -f bootstrap.sh
then
   ./bootstrap.sh
else
   ./rebootstrap.sh
fi

autoreconf --force --install

%configure -C \
--prefix=%{PREFIX} \
--exec-prefix=%{EXECPREFIX} \
--bindir=%{BINDIR} \
--sbindir=%{SBINDIR} \
--libexecdir=%{LIBEXECDIR} \
--sharedstatedir=%{SHARESTATEDIR} \
--localstatedir=%{_localstatedir} \
--libdir=%{LIBDIR} \
--includedir=%{INCLUDEDIR} \
--datadir=%{DATADIR} \
--infodir=%{INFODIR} \
--mandir=%{MANDIR} \
--with-logfiledir=%{LOGFILEDIR} \
--with-modinstdir=%{MODINSTDIR} \
--with-rundir=%{RUNDIR} \
--with-dbdir=%{DBDIR} \
--with-htdocsdir=%{HTDOCSDIR} \
--with-soundsdir=%{SOUNDSDIR} \
--enable-core-libedit-support \
--with-grammardir=%{GRAMMARDIR} \
--with-scriptdir=%{SCRIPTDIR} \
--with-recordingsdir=%{RECORDINGSDIR} \
--with-pkgconfigdir=%{PKGCONFIGDIR} \
--with-openssl \
--disable-core-odbc-support \
--disable-core-pgsql-support \
--without-python \
--without-erlang \
--without-java \
%{?configure_options}

unset MODULES

%{__make}

%install
%{__make} DESTDIR=%{buildroot} install

# Create a log dir
%{__mkdir} -p %{buildroot}%{prefix}/log
%{__mkdir} -p %{buildroot}%{logfiledir}
%{__mkdir} -p %{buildroot}%{runtimedir}

%{__install} -Dpm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/freeswitch.service
%{__install} -Dpm 0644 build/freeswitch-tmpfiles.conf %{buildroot}%{_tmpfilesdir}/freeswitch.conf

# Add the sysconfiguration file
%{__install} -D -m 644 build/freeswitch.sysconfig %{buildroot}/etc/sysconfig/freeswitch

find %{buildroot}%{MODINSTDIR} -type f | xargs chmod -x

%pre
if ! /usr/bin/id freeswitch &>/dev/null; then
       /usr/sbin/useradd -r -g daemon -s /bin/false -c "The FreeSWITCH Open Source Voice Platform" -d %{LOCALSTATEDIR} freeswitch || \
                %logmsg "Unexpected error adding user \"freeswitch\". Aborting installation."
fi

%post
%{?run_ldconfig:%run_ldconfig}

chown freeswitch:daemon /var/log/freeswitch /var/run/freeswitch

%tmpfiles_create freeswitch
/usr/bin/systemctl -q enable freeswitch.service

%preun
%{?systemd_preun freeswitch.service}

%postun
%{?systemd_postun freeswitch.service}
%{?run_ldconfig:%run_ldconfig}
if [ $1 -eq 0 ]; then
    userdel freeswitch || %logmsg "User \"freeswitch\" could not be deleted."
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)

%dir %attr(0755, freeswitch, daemon) %{sysconfdir}
%dir %attr(0755, freeswitch, daemon) %{LOCALSTATEDIR}
%dir %attr(0755, freeswitch, daemon) %{LOCALSTATEDIR}/images
%dir %attr(0755, freeswitch, daemon) %{DBDIR}
%dir %attr(0755, -, -) %{GRAMMARDIR}
%dir %attr(0755, -, -) %{HTDOCSDIR}
%dir %attr(0755, freeswitch, daemon) %{logfiledir}
%dir %attr(0755, freeswitch, daemon) %{runtimedir}
%dir %attr(0755, -, -) %{SCRIPTDIR}

%dir %attr(0755, freeswitch, daemon) %{sysconfdir}/autoload_configs
%dir %attr(0755, freeswitch, daemon) %{sysconfdir}/dialplan
%dir %attr(0755, freeswitch, daemon) %{sysconfdir}/dialplan/default
%dir %attr(0755, freeswitch, daemon) %{sysconfdir}/dialplan/public
%dir %attr(0755, freeswitch, daemon) %{sysconfdir}/dialplan/skinny-patterns
%dir %attr(0755, freeswitch, daemon) %{sysconfdir}/directory
%dir %attr(0755, freeswitch, daemon) %{sysconfdir}/directory/default
%dir %attr(0755, freeswitch, daemon) %{sysconfdir}/jingle_profiles
%dir %attr(0755, freeswitch, daemon) %{sysconfdir}/lang
%dir %attr(0755, freeswitch, daemon) %{sysconfdir}/mrcp_profiles
%dir %attr(0755, freeswitch, daemon) %{sysconfdir}/sip_profiles
%dir %attr(0755, freeswitch, daemon) %{sysconfdir}/sip_profiles/external
%dir %attr(0755, freeswitch, daemon) %{sysconfdir}/sip_profiles/external-ipv6
%dir %attr(0755, freeswitch, daemon) %{sysconfdir}/skinny_profiles

%config(noreplace) %{sysconfdir}/*
%config(noreplace) %{HTDOCSDIR}/*

%{_unitdir}/freeswitch.service
%{_tmpfilesdir}/freeswitch.conf
%config(noreplace) /etc/sysconfig/freeswitch
%{LOCALSTATEDIR}/images/*

%{FONTSDIR}/*

%attr(0755,-,-) %{prefix}/bin/*
%{LIBDIR}/libfreeswitch*.so*
%{MODINSTDIR}/mod_*.so*

%files devel
%{LIBDIR}/*.a
%{LIBDIR}/*.la
%{PKGCONFIGDIR}/*
%{MODINSTDIR}/*.*a
%{INCLUDEDIR}/*.h
%{INCLUDEDIR}/test/*.h

%changelog
