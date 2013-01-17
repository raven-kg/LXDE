# Review: https://bugzilla.redhat.com/show_bug.cgi?id=442270

Name:           lxde-common
Version:        0.5.4
Release:        3%{?dist}
Summary:        Default configuration files for LXDE

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://lxde.sourceforge.net/
#Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-0.5.0.tar.gz
Source1:        lxde-lock-screen.desktop
Source2:        lxde-desktop-preferences.desktop
Source3:        lxde-panel
Source4:        lxde-pcmanfm
Source5:        panel_bg.png
# http://lxde.svn.sourceforge.net/viewvc/lxde/trunk/lxde-common/startlxde.in?r1=1964&r2=2187
Patch0:         lxde-common-0.5.0-fix-session-startup.patch
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxde-common;a=commit;h=847a8e73e658bb9ced5eb7b12242b0064224f49e
Patch1:         lxde-common-0.5.1-Launch-dbus-in-startlxde-when-needed.patch
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxde-common;a=commit;h=34cd793a18138463133a72b713173d2d01d32d66
Patch2:         lxde-common-0.5.1-start-xscreensaver-after-lxpanel-and-pcmanfm.patch
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxde-common;a=commit;h=28309e598478254fa9c918782cf089aea6358abb
Patch3:         lxde-common-0.5.1-Ensure-the-existance-of-the-Desktop-folder.patch
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxde-common;a=commit;h=0f3b683ccd0c208c1f32fae28f628db9e103ccd8
Patch5:         lxde-common-0.5.1-switch-from-pcmanfm-to-pcmanfm2.patch
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxde-common;a=commit;h=fcefd17a7187232d15aca13fdedf47a4b854fc21
Patch7:         lxde-common-0.5.1-Properly-set-XDG_MENU_PREFIX.patch
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxde-common;a=commit;h=bf7093b8c45c7a38a2f42ddb61135fca7566ff5e
Patch8:         lxde-common-0.5.1-Fix-config-file-of-pcmanfm2.patch
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxde-common;a=commit;h=908f14c74766eb237afda780237db67e7798da0b
# pcmanfm 0.9.7 finally re-renamed pcmanfm2 binary to "pcmanfm"
# Adjusting contents in autostart file
# bug 603468
# This patch contains patch-to-patch part for Patch8
Patch9:         lxde-common-0.5.5-pcmanfm2-finally-re-renamed-to-pcmanfm.patch
# Distro specific patches
Patch10:        %{name}-0.4-openbox-menu.patch
Patch11:        %{name}-0.3.2.1-logout-banner.patch
Patch12:        %{name}-0.5.1-pulseaudio.patch
Patch13:        %{name}-0.5.4-icons.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
# because of some patches:
BuildRequires:  automake
Requires:       lxsession >= 0.4.0
Requires:       lxpanel pcmanfm openbox xdg-utils 
Requires:       lxmenu-data
Requires:       simple-icon-theme
# Use vendor's artwork
Requires:       redhat-logos
# needed because of new gdm
Requires:       xorg-x11-utils

Obsoletes:      %{name}-data <= 0.3.2.1-5
# needed because the lxde-common and lxde-common-data 
# required each other with full n-v-r on F-11
# Provides:       %{name} = 0.3.2.1-4.fc11
# Provides:       %{name}-data = 0.3.2.1-4.fc11
BuildArch:      noarch

%description
This package contains the configuration files for LXDE, the Lightweight X11 
Desktop Environment.


%prep
%setup -qn %{name}-0.5.0
%patch0 -p2 -b .session-startup
%patch1 -p1 -b .dbus
%patch2 -p1 -b .xscreensaver
%patch3 -p1 -b .desktop
%patch5 -p1 -b .pcmanfm2
%patch7 -p1 -b .menu-prefix
%patch8 -p1 -b .fix-pcmanfm2
%patch9 -p1 -b .pcmanfm2_2_pcmanfm

%patch10 -p1 -b .orig
%patch11 -p1 -b .logout-banner
%patch12 -p1 -b .pulseaudio
%patch13 -p1 -b .icons

# Calling autotools must be done before executing
# configure if needed
autoreconf -fi

%build
%configure


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
desktop-file-install                                           \
      --remove-key=Encoding                                    \
      --dir=%{buildroot}%{_datadir}/applications               \
      lxde-logout.desktop
desktop-file-install                                           \
      --dir=%{buildroot}%{_datadir}/applications               \
      %{SOURCE1}
# cannot use desktop-file-utils because it is out of date
install -pm 0644 %{SOURCE2} %{buildroot}%{_datadir}/applications/
# making some appearance changes
rm -f %{buildroot}%{_datadir}/lxpanel/profile/LXDE/panels/panel
rm -f %{buildroot}%{_sysconfdir}/xdg/pcmanfm/lxde.conf
install -pm 0644 %{SOURCE3} %{buildroot}%{_datadir}/lxpanel/profile/LXDE/panels/panel
install -pm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/xdg/pcmanfm/lxde.conf
mkdir -p %{buildroot}%{_datadir}/lxpanel/images
install -pm 0644 %{SOURCE5} %{buildroot}%{_datadir}/lxpanel/images/rx_panel_bg.png


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%dir %{_sysconfdir}/xdg/lxsession/LXDE/
%config(noreplace) %{_sysconfdir}/xdg/lxsession/LXDE/autostart
%config(noreplace) %{_sysconfdir}/xdg/lxsession/LXDE/desktop.conf
%dir %{_sysconfdir}/xdg/pcmanfm/
%config(noreplace) %{_sysconfdir}/xdg/pcmanfm/lxde.conf
%{_bindir}/startlxde
%{_bindir}/lxde-logout
%{_bindir}/openbox-lxde
%{_datadir}/lxde/
%{_datadir}/lxpanel/profile/LXDE/
%{_datadir}/lxpanel/images/
%{_mandir}/man1/*.1.gz
%{_datadir}/xsessions/LXDE.desktop
%{_datadir}/applications/lxde-*.desktop


%changelog
* Tue Jan 08 2013 Raven <raven_kg@megaline.kg> - 0.5.4-3
- added default interface settings

* Tue Jan 08 2013 Raven <raven_kg@megaline.kg> - 0.5.4-2
- replaced default icon theme patch for use Simple icon 
  theme as default

* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.5.4-1
- Initial packaging for RERemix