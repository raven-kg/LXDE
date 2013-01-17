Name:           lxshortcut
Version:        0.1.1
Release:        1%{?dist}
Summary:        Small utility to edit application shortcuts

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://lxde.org
Source0:        http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel, gettext

%description
LXShortcut is a small utility to edit application shortcuts created with 
freedesktop.org Desktop Entry spec. Now editing of application shortcuts 
becomes quite easy.


%prep
%setup -q


%build
%configure
# workaround for FTBFS #539158
touch -r po/Makefile po/stamp-it
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ChangeLog COPYING README
%{_bindir}/%{name}
%{_datadir}/%{name}/


%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.1.1-1
- Initial packaging for RERemix
