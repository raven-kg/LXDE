# Review at https://bugzilla.redhat.com/show_bug.cgi?id=579171

Name:           lxpolkit
Version:        0.1.0
Release:        1%{?dist}
Summary:        Simple PolicyKit authentication agent

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://lxde.org/
#VCS: git:git://lxde.git.sourceforge.net/gitroot/lxde/lxpolkit
Source0:        http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel
BuildRequires:  intltool
BuildRequires:  gettext
BuildRequires:  polkit-devel
BuildRequires:  desktop-file-utils
Requires:       polkit >= 0.95
# required to replace polkit-gnome and polkit-kde
Provides:       PolicyKit-authentication-agent

%description
LXPolKit is a simple PolicyKit authentication agent developed for LXDE, the 
Lightweight X11 Desktop Environment.


%prep
%setup -q
# Don't start in Xfce to avoid bugs like
# https://bugzilla.redhat.com/show_bug.cgi?id=616730
sed -i 's/^NotShowIn=GNOME;KDE;/NotShowIn=GNOME;KDE;XFCE;/g' data/lxpolkit.desktop.in.in


%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
%find_lang %{name}
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}.desktop


%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
# FIXME add ChangeLog and NEWS if not empty
%doc AUTHORS COPYING README
%config %{_sysconfdir}/xdg/autostart/lxpolkit.desktop
%{_libexecdir}/%{name}
%{_datadir}/%{name}/


%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.1.0-1
- Initial packaging for RERemix


