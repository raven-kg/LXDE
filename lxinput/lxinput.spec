# Review: https://bugzilla.redhat.com/show_bug.cgi?id=498130

Name:           lxinput
Version:        0.3.0
Release:        1%{?dist}
Summary:        Keyboard and mouse settings dialog for LXDE

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://lxde.org/
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel
BuildRequires:  gettext intltool desktop-file-utils
Requires:       lxsession >= 0.4.0

%description
LXInput is a keyboard and mouse configuration utility for LXDE, the 
Lightweight X11 Desktop Environment.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
desktop-file-install                                       \
  --delete-original                                        \
  --add-category=X-LXDE                                    \
  --remove-only-show-in=LXDE                               \
  --add-only-show-in=X-LXDE                                \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications          \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
#FIXME: add ChangeLog and NEWS if there is content
%doc AUTHORS COPYING README
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/%{name}.1.gz


%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.3.0-1
- Initial packaging for RERemix
