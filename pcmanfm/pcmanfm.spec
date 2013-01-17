Name:		pcmanfm
Version:	0.9.7
Release:	1%{?dist}
Summary:	Extremly fast and lightweight file manager

Group:		User Interface/Desktops
License:	GPLv2+
URL:		http://pcmanfm.sourceforge.net/
Source0:	http://downloads.sourceforge.net/pcmanfm/%{name}/%{name}-%{version}.tar.gz

BuildRequires:	libfm-gtk-devel
BuildRequires:	menu-cache-devel

BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool

# For compatibility
BuildRequires:	lxde-icon-theme

# Still needed for removable media - still now really?
Requires:	hal-storage-addon

# Write explicitly
Requires:	libfm >= %{libfm_minver}

%description
PCMan File Manager is an extremly fast and lightweight file manager 
which features tabbed browsing and user-friendly interface.

%prep
%setup -q

# permission fix
chmod 0644 [A-Z]*

%build
%configure

make -C po -j1 GMSGFMT="msgfmt --statistics"
make  %{?_smp_mflags} -k

%install
rm -rf $RPM_BUILD_ROOT
make install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="install -p"

desktop-file-install \
	--delete-original \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
	--remove-category 'Application' \
	--vendor 'redhat' \
	$RPM_BUILD_ROOT%{_datadir}/applications/%{name}*.desktop

# compatibility
mkdir %{buildroot}%{_datadir}/pixmaps
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/xdg/%{name}
# No link but copy so that non-LXDE user won't require
# LXDE stuff
cp -p %{_datadir}/icons/nuoveXT2/128x128/apps/system-file-manager.png \
	%{buildroot}%{_datadir}/pixmaps/%{name}.png

%find_lang %{name}

%{_prefix}/lib/rpm/check-rpaths

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database &> /dev/null
exit 0

%postun
update-desktop-database &> /dev/null
exit 0

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc	AUTHORS
%doc	COPYING
%doc	README

%{_bindir}/%{name}

%{_datadir}/%{name}/
%{_datadir}/applications/redhat-%{name}.desktop
%config(noreplace) %{_sysconfdir}/xdg/%{name}/

%{_datadir}/pixmaps/%{name}.png


%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.9.7-1
- Initial packaging for RERemix


