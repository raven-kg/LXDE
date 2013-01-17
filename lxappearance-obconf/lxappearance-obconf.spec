# Review at https://bugzilla.redhat.com/show_bug.cgi?id=630184

Name:           lxappearance-obconf
Version:        0.2.0
Release:        1%{?dist}
Summary:        Plugin to configure Openbox inside LXAppearance

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://lxde.org/
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel
BuildRequires:  openbox-devel >= 3.5.0
BuildRequires:  lxappearance-devel
BuildRequires:  libSM-devel
BuildRequires:  gettext
BuildRequires:  intltool
Requires:       lxappearance >= 0.5.0
Requires:       openbox >= 3.5.0

%description
This plugin adds an additional tab called "Window Border" to LXAppearance.
It is only visible when the plugin is installed and Openbox is in use.

%prep
%setup -q %{name}


%build
%configure --disable-static
make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
# FIXME add NEWS and TODO if not empty
%doc AUTHORS CHANGELOG COPYING README
%{_libdir}/lxappearance/plugins/obconf.so
%{_datadir}/lxappearance/obconf/


%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.2.0-1
- Initial packaging for RERemix