Name:           lxtask
Version:        0.1.3
Release:        1%{?dist}
Summary:        Lightweight and desktop independent task manager

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://lxde.sourceforge.net/
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel > 2.6, gettext, intltool, desktop-file-utils

%description
LXTask is a lightweight task manager derived from xfce4 task manager with all
xfce4 dependencies removed, some bugs fixed, and some improvement of UI. 
Although being part of LXDE, the Lightweight X11 Desktop Environment, it's 
totally desktop independent and only requires pure gtk+.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
desktop-file-install --vendor="redhat"                     \
  --delete-original                                        \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications          \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{_bindir}/%{name}
%{_datadir}/applications/redhat-%{name}.desktop


%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.1.3-1
- Initial packaging for RERemix