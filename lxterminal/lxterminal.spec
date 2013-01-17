Name:           lxterminal
Version:        0.1.9
Release:        1%{?dist}
Summary:        Desktop-independent VTE-based terminal emulator
Summary(de):    Desktop-unabhängiger VTE-basierter Terminal Emulator

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://lxde.sourceforge.net/
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxterminal;a=commit;h=2cda6d2217f82cc993f4758ed44ef74c61f729ba
Patch0:         lxterminal-0.1.9-fixed-vte-failure-because-of-deprecated-API.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel >= 2.6
BuildRequires:  vte-devel >= 0.20.0
BuildRequires:  desktop-file-utils intltool gettext

%description
LXterminal is a VTE-based terminal emulator with support for multiple tabs. 
It is completely desktop-independent and does not have any unnecessary 
dependencies. In order to reduce memory usage and increase the performance 
all instances of the terminal are sharing a single process.

%description -l de
LXTerminal ist ein VTE-basierter Terminalemulator mit Unterstützung für 
mehrere Reiter. Er ist komplett desktop-unabhängig und hat keine unnötigen 
Abhängigkeiten. Um den Speicherverbrauch zu reduzieren und die Leistung zu
erhöhen teilen sich alle Instanzen des Terminals einen einzigen Prozess.

%prep
%setup -q
%patch0 -p1 -b .deprecated-API


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
desktop-file-install --vendor="redhat"                     \
  --delete-original                                        \
  --remove-category=Utility                                \
  --add-category=System                                    \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications          \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/redhat-%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/man1/%{name}*.1.gz


%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.1.9-1
- Initial packaging for RERemix
