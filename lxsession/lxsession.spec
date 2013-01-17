# review https://bugzilla.redhat.com/show_bug.cgi?id=502404
# renamed from lxsession-lite. Original review at
# https://bugzilla.redhat.com/show_bug.cgi?id=442268

Name:           lxsession
Version:        0.4.4
Release:        1%{?dist}
Summary:        Lightweight X11 session manager
Summary(de):    Leichtgewichtiger X11 Sitzungsverwalter

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://lxde.sourceforge.net/
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz
Patch0:         lxsession-0.4.1-dsofix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel > 2.6 dbus-glib-devel
BuildRequires:  docbook-utils intltool gettext
Requires:       hal
# name changed back from lxsession-lite to lxsession
Obsoletes:      lxsession-lite <= 0.3.6-6
Provides:       lxsession-lite = %{version}-%{release}
# lxde-settings-daemon was merged into lxsession
Obsoletes:      lxde-settings-daemon <= 0.4.1-2
Provides:       lxde-settings-daemon = 0.4.1-3


%description
LXSession is a standard-compliant X11 session manager with shutdown/
reboot/suspend support via HAL. In connection with gdm it also supports user 
switching.

LXSession is derived from XSM and is developed as default X11 session manager 
of LXDE, the Lightweight X11 Desktop Environment. Though being part of LXDE, 
it's totally desktop-independent and only has few dependencies.

%description -l de
LXSession Lite ist ein Standard konformer X11 Sitzungsverwalter mit 
Unterstützung für Herunterfahren, Neustart und Schlafmodus mittels HAL. 
Zusammen mit GDM unterstützt auch Benutzerwechsel.

LXSession Lite ist von XSM abgeleitet und wird als Sitzungsverwalter von LXDE,
der leichtgewichtigen X11 Desktop Umgebung, entwickelt. Obwohl er Teil von 
LXDE ist, ist er komplett Desktop unabhängig und hat nur wenige 
Abhängigkeiten.


%prep
%setup -q
%patch0 -p1 -b .dsofix


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
%find_lang %{name}
mkdir -p -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/xdg/%{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README desktop.conf.example
%{_bindir}/%{name}
%{_bindir}/%{name}-logout
%{_datadir}/%{name}/
%{_mandir}/man*/%{name}*.*
# we need to own
%dir %{_sysconfdir}/xdg/%{name}

%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.4.4-1
- Initial packaging for RERemix