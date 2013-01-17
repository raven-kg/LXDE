Name:           lxde-icon-theme
Version:        0.4.2
Release:        1%{?dist}
Summary:        Default icon theme for LXDE

Group:          User Interface/Desktops
License:        LGPLv3
URL:            http://nuovext.pwsp.net/
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/lxde-common-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       filesystem
BuildArch:      noarch
Provides:       nuoveXT2-icon-theme = 2.2

%description
nuoveXT2 is a very complete set of icons for several operating systems. It is 
also the default icon-theme of LXDE, the Lightweight X11 Desktop Environment.


%prep
%setup -qn lxde-common-%{version}

%build
%configure


%install
rm -rf $RPM_BUILD_ROOT
# we only install the icon theme
cd icon-theme
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
touch $RPM_BUILD_ROOT%{_datadir}/icons/nuoveXT2/icon-theme.cache


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/nuoveXT2 &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/nuoveXT2 &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/nuoveXT2 &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/nuoveXT2 &>/dev/null || :


%files
%defattr(-,root,root,-)
%doc icon-theme/AUTHORS icon-theme/COPYING
%dir %{_datadir}/icons/nuoveXT2/
%{_datadir}/icons/nuoveXT2/*/*
%{_datadir}/icons/nuoveXT2/index.theme
%ghost %{_datadir}/icons/nuoveXT2/icon-theme.cache


%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.4.2-2
- Initial packaging for RERemix
