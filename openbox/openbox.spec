Name:		openbox
Version:	3.5.0
Release:	1%{?dist}
Summary:	A highly configurable and standards-compliant X11 window manager

Group:		User Interface/Desktops
License:	GPLv2+
URL:		http://openbox.org
Source0:	http://openbox.org/releases/%{name}-%{version}.tar.gz
Source1:	http://icculus.org/openbox/tools/setlayout.c
Source2:	xdg-menu
Source3:	menu.xml
Source4:	openbox.desktop
Source5:	terminals.menu
Source6:	openbox.gnome-session

Patch1:		openbox-doubleclick.patch
Patch2:		openbox-3.4.11.2-gnomesession.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	%{name}-libs = %{version}-%{release}

# required by xdg-menu and xdg-autostart scripts
Requires:	pyxdg

BuildRequires:	gettext
BuildRequires:	desktop-file-utils
BuildRequires:	pango-devel
BuildRequires:	startup-notification-devel
BuildRequires:	libxml2-devel
BuildRequires:	libXcursor-devel
BuildRequires:	libXt-devel
BuildRequires:	libXrandr-devel
BuildRequires:	libXinerama-devel
BuildRequires:	imlib2-devel
Provides:	firstboot(windowmanager)

%description
Openbox is a window manager designed explicity for standards-compliance and
speed. It is fast, lightweight, and heavily configurable (using XML for its
configuration data). It has many features that make it unique among window
managers: window resistance, chainable key bindings, customizable mouse
actions, multi-head/Xinerama support, and dynamically generated "pipe menus."

For a full list of the FreeDesktop.org standards with which it is compliant,
please see the COMPLIANCE file in the included documentation of this package. 
For a graphical configuration editor, you'll need to install the obconf
package. For a graphical menu editor, you'll need to install the obmenu
package.


%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	pkgconfig
Requires:	pango-devel
Requires:	libxml2-devel
Requires:	glib2-devel

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package	libs
Summary:	Shared libraries for %{name}
Group:		Development/Libraries

%description	libs
The %{name}-libs package contains shared libraries used by %{name}.


%package	gnome
Summary:	GNOME integration for %{name}
Group:		User Interface/Desktops
Requires:	%{name} = %{version}-%{release}
Requires:	gnome-session

%description	gnome
The %{name}-gnome package contains the files needed for using %{name} inside a
GNOME session.


%package	kde
Summary:	KDE integration for %{name}
Group:		User Interface/Desktops
Requires:	%{name} = %{version}-%{release}
Requires:	kdebase-workspace

%description	kde
The %{name}-kde package contains the files needed for using %{name} inside a
KDE session.


%prep
%setup -q
%patch1 -p1 -b .doubleclick
%patch2 -p1 -b .gnome


%build
%configure \
	--disable-static
## Fix RPATH hardcoding.
sed -ie 's|^hardcode_libdir_flag_spec=.*$|hardcode_libdir_flag_spec=""|g' libtool
sed -ie 's|^runpath_var=LD_RUN_PATH$|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

gcc %{optflags} -o setlayout %{SOURCE1} -lX11

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

install setlayout %{buildroot}%{_bindir}
install -p %{SOURCE2} %{buildroot}%{_libexecdir}/openbox-xdg-menu
sed 's|_LIBEXECDIR_|%{_libexecdir}|g' < %{SOURCE3} \
	> %{buildroot}%{_sysconfdir}/xdg/%{name}/menu.xml

desktop-file-install --vendor="" \
        --dir=%{buildroot}%{_datadir}/applications \
        %{SOURCE4}

install -m644 -p %{SOURCE5} %{buildroot}%{_sysconfdir}/xdg/%{name}/terminals.menu
install -m644 -D %{SOURCE6} \
	%{buildroot}%{_datadir}/gnome-session/sessions/gnome-openbox.session

%find_lang %{name}
rm -f %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_datadir}/doc/%{name}


%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG COMPLIANCE COPYING README
%doc data/*.xsd data/menu.xml doc/rc-mouse-focus.xml
%dir %{_sysconfdir}/xdg/%{name}/
%config(noreplace) %{_sysconfdir}/xdg/%{name}/*
%{_bindir}/%{name}
%{_bindir}/%{name}-session
%{_bindir}/obxprop
%{_bindir}/setlayout
%{_libexecdir}/openbox-*
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/themes/*/
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/xsessions/%{name}.desktop
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-session.1*
%{_mandir}/man1/obxprop.1*

%files	libs
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libobrender.so.*
%{_libdir}/libobt.so.*

%files	devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/
%{_libdir}/libobrender.so
%{_libdir}/libobt.so
%{_libdir}/pkgconfig/*.pc

%files  gnome
%defattr(-,root,root,-)
%{_bindir}/gnome-panel-control
%{_bindir}/gdm-control
%{_bindir}/%{name}-gnome-session
%{_datadir}/xsessions/%{name}-gnome.desktop
%{_datadir}/gnome/wm-properties/openbox.desktop
%{_datadir}/gnome-session/sessions/gnome-openbox.session
%{_mandir}/man1/%{name}-gnome-session*.1*

%files  kde
%defattr(-,root,root,-)
%{_bindir}/%{name}-kde-session
%{_datadir}/xsessions/%{name}-kde.desktop
%{_mandir}/man1/%{name}-kde-session*.1*


%post libs -p /sbin/ldconfig


%postun libs -p /sbin/ldconfig


%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 3.5.0-1
- Initial packaging for RERemix