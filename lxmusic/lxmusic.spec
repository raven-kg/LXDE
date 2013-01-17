Name:           lxmusic
Version:        0.4.4
Release:        1%{?dist}
Summary:        Lightweight XMMS2 client with simple user interface

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://lxde.org
Source0:        http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
# As long as there are no plugins, disable the Tools menu
Patch0:         lxmusic-0.3.0-no-tools-menu.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel >= 2.12.0 xmms2-devel >= 0.6
BuildRequires:  desktop-file-utils gettext intltool libnotify-devel
Requires:       xmms2 >= 0.7

%description
LXMusic is a very simple gtk+ XMMS2 client written in pure C. It has very few 
functionality, and can do nothing more than play the music. The UI is very 
clean and simple. This is currently aimed to be used as the default music 
player of LXDE (Lightweight X11 Desktop Environment) project.

%prep
%setup -q
%patch0 -p1 -b .no-tools


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
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
%{_datadir}/applications/lxmusic.desktop
%{_datadir}/lxmusic
%{_datadir}/pixmaps/lxmusic.png


%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.4.4-1
- Initial packaging for RERemix