Name:           lxlauncher
Version:        0.2.1
Release:        1%{?dist}
Summary:        Open source replacement for Launcher on the EeePC

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://lxde.org/
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxlauncher;a=commit;h=cb99b126dd90a8460c5bd4a837fdb7505658ba52
Patch0:         lxlauncher-0.2.1-fix-SUSE-lint-warnings.patch
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxlauncher;a=commit;h=a7dad81b883a783bc1ac4f8092a1571b7f843914
Patch1:         lxlauncher-0.2.1-fix-for-the-new-behavior-of-libmenu-cache-0.3-series.patch
# fixes https://bugzilla.redhat.com/show_bug.cgi?id=565072
Patch2:         lxlauncher-0.2.1-dsofix.patch
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxlauncher;a=commit;h=b1ec4b856582467b3c287e443213c9f97a1dc38e
# fixes https://bugzilla.redhat.com/show_bug.cgi?id=539147
Patch3:         lxlauncher-0.2.1-fix-build-loop.patch
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxlauncher;a=commit;h=5c74d1d5ee35b527dedbe46f013be19c3ae20abe
Patch4:         lxlauncher-0.2.1-fix-segfault-from-window-manager.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel >= 2.12 startup-notification-devel
BuildRequires:  menu-cache-devel >= 0.3.2
BuildRequires:  gettext intltool

%description
LXLauncher is designed as an open source replacement for the Asus Launcher
included in their EeePC. It is desktop-independent and follows 
freedesktop.org specs, so newly added applications will automatically show 
up in the launcher, and vice versa for the removed ones.
LXLauncher is part of LXDE, the Lightweight X11 Desktop Environment.

%prep
%setup -q
%patch0 -p1 -b .suse-lint
%patch1 -p1 -b .menu-cache-0.3.0
%patch2 -p1 -b .dsofix
%patch3 -p1 -b .loop
%patch4 -p1 -b .fix-segfault-from-window-manager


%build
%configure
# workaround for FTBFS #539147 and #661008
touch -r po/Makefile po/stamp-it
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
mkdir -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
mkdir -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/backgrounds
mkdir -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%dir %{_sysconfdir}/xdg/lxlauncher/
%config(noreplace) %{_sysconfdir}/xdg/lxlauncher/gtkrc
%config(noreplace) %{_sysconfdir}/xdg/lxlauncher/settings.conf
%config(noreplace) %{_sysconfdir}/xdg/menus/lxlauncher-applications.menu
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/desktop-directories/lxde-*.directory


%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.2.1-1
- Initial packaging for RERemix