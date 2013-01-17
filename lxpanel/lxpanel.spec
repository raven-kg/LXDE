# Review Request:
# https://bugzilla.redhat.com/show_bug.cgi?id=219930

Name:           lxpanel
Version:        0.5.6
Release:        1%{?dist}
Summary:        A lightweight X11 desktop panel

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://lxde.org/
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz
# https://bugzilla.redhat.com/show_bug.cgi?id=564746
Patch0:         lxpanel-0.5.5-dsofix.patch
# http://sourceforge.net/tracker/?func=detail&aid=3033293&group_id=180858&atid=894869
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxpanel;a=commit;h=4a974f2686d2fafdcda4a180b0483a7b17fd2d71
Patch1:         lxpanel-0.5.6-Fix-build-issue-with-symbol-alarm-showing-up-on-F14-.patch 
# distro specific patches
Patch100:       lxpanel-0.5.4-default.patch
Patch101:       lxpanel-0.3.8.1-nm-connection-editor.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  docbook-utils
BuildRequires:  gettext
BuildRequires:  gtk2-devel 
BuildRequires:  intltool
BuildRequires:  libXpm-devel
BuildRequires:  startup-notification-devel
# required for alsa mixer plugin
BuildRequires:  alsa-lib-devel
# required for netstatus plugin
BuildRequires:  wireless-tools-devel
BuildRequires:  menu-cache-devel >= 0.3.0

%description
lxpanel is a lightweight X11 desktop panel. It works with any ICCCM / NETWM 
compliant window manager (eg sawfish, metacity, xfwm4, kwin) and features a 
tasklist, pager, launchbar, clock, menu and sytray.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gtk2-devel 
Requires:       libXpm-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .dsofix
%patch1 -p1 -b .fix-build-issue

%patch100 -p1 -b .default
%patch101 -p1 -b .system-config-network


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_bindir}/lxpanel*
%{_datadir}/lxpanel/
%{_libdir}/lxpanel/
%{_mandir}/man1/lxpanel*

%files devel
%defattr(-,root,root,-)
%{_includedir}/lxpanel/
%{_libdir}/pkgconfig/lxpanel.pc

%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.5.6-1
- Initial packaging for RERemix

