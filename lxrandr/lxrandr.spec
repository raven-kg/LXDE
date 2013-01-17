Name:           lxrandr
Version:        0.1.1
Release:        1%{?dist}
Summary:        Simple monitor configuration tool

Group:          User Interface/Desktops
License:        GPLv3+
URL:            http://lxde.org/
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel libXrandr-devel gettext desktop-file-utils
Requires:       xorg-x11-server-utils

%description
LXRandR is a simple monitor configuration tool utilizing X RandR extension. 
It's a GUI frontend of the command line program xrandr and manages screen 
resolution and external monitors. When you run LXRandR with an external 
monitor or projector connected, its GUI will change and show you some options 
to quickly configure the external device.

LXRandR is the standard screen manager of LXDE, the Lightweight X11 Desktop 
Environment, but can be used in other desktop environments as well.


%prep
%setup -q
# quick fix for the icon
echo "Icon=video-display" >> data/%{name}.desktop.in

%build
%configure
# workaround for FTBFS #538905
touch -r po/Makefile po/stamp-it
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
desktop-file-install                                       \
  --delete-original                                        \
  --add-category="HardwareSettings;GTK;"                   \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications          \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/%{name}.1.gz


%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.1.1-1
- Initial packaging for RERemix

