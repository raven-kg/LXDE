# review at https://bugzilla.redhat.com/show_bug.cgi?id=442269

Name:           lxappearance
Version:        0.5.1
Release:        1%{?dist}
Summary:        Feature-rich GTK+ theme switcher for LXDE

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://lxde.org/
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel > 2.6, gettext, intltool, desktop-file-utils
Requires:       lxsession >= 0.4.0

%description
LXAppearance is a new GTK+ theme switcher developed for LXDE, the Lightweight 
X11 Desktop Environment. It is able to change GTK+ themes, icon themes, and 
fonts used by applications. All changes done by the users can be seen 
immediately in the preview area. After clicking the "Apply" button, the 
settings will be written to gtkrc, and all running programs will be asked to 
reload their themes.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains header files for developing plug-ins 
for LXAppearance.


%prep
%setup -q %{name}


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
%doc AUTHORS COPYING
%{_bindir}/%{name}
%{_datadir}/applications/redhat-%{name}.desktop
%{_datadir}/%{name}/
%{_mandir}/man1/%{name}*.1.gz


%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.5.1-1
- Initial packaging for RERemix