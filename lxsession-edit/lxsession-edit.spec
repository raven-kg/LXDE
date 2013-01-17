Name:           lxsession-edit
Version:        0.1.1
Release:        1%{?dist}
Summary:        Simple GUI to configure what’s automatically started in LXDE

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://lxde.org
Source0:        http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
Patch0:         %{name}-0.1.1-desktop-file.patch
# http://lxde.svn.sourceforge.net/viewvc/lxde/trunk/lxsession-edit/src/lxsession-edit.c?r1=1797&r2=1812
Patch1:         %{name}-0.1.1-new-config-file.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel, desktop-file-utils, gettext
Requires:       lxsession >= 0.4.0

%description
LXSession-edit is a tool to manage freedesktop.org compliant desktop session 
autostarts. Currently adding and removing applications from the startup list 
is not yet available, but it will be support in the next release.


%prep
%setup -q
%patch0 -p1 -b .fixes
%patch1 -p2 -b .old


%build
%configure
# workaround for FTBFS #539206
touch -r po/Makefile po/stamp-it
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
desktop-file-install                                       \
  --delete-original                                        \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications          \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_bindir}/%{name}
%{_datadir}/applications/lxsession-edit.desktop
%{_datadir}/lxsession-edit/


%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.1.1-1
- Initial packaging for RERemix
