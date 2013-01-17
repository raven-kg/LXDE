# Review:       https://bugzilla.redhat.com/487973

Name:           lxmenu-data
Version:        0.1.1
Release:        1%{?dist}
Summary:        Data files for the LXDE menu

Group:          User Interface/Desktops
License:        LGPLv2+
URL:            http://lxde.org
Source0:        http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
Source1:        lxmenu-data-0.1-COPYING
Patch0:         lxmenu-data-0.1.1-menu.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  intltool >= 0.40.0
Requires:       redhat-menus
BuildArch:      noarch

%description
The lxmenu-data contains files used to build the menu in LXDE according to 
the freedesktop-org menu spec. Currently it's used by LXPanel and LXLauncher.


%prep
%setup -q
%patch0 -p1 -b .orig
# install correct license
rm -f COPYING
cp %{SOURCE1} COPYING


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
#FIXME: add changelog when there is one
%doc AUTHORS COPYING README TODO
%config(noreplace) %{_sysconfdir}/xdg/menus/lxde-applications.menu
%{_datadir}/desktop-directories/lxde-*.directory


%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.1.1-1
- Initial packaging for RERemix