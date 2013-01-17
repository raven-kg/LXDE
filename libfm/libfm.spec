# Review: https://bugzilla.redhat.com/show_bug.cgi?id=567257

Name:           libfm
Version:        0.1.12
Release:        1%{?dist}
Summary:        GIO-based library for file manager-like programs

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://pcmanfm.sourceforge.net/
Source0:        http://downloads.sourceforge.net/pcmanfm/%{name}-%{version}.tar.gz
# Fedora specific patches
Patch0:         libfm-0.1.9-pref-apps.patch
# Patches already in git
#
# Patches need discussing with the upstream
# Upstream bug 3009374, sorting by name broken in cs_CZ.UTF-8
Patch1:         libfm-0.1.12-sort-in-cs_CZ.UTF-8.patch
# Upstream bug 3012747, pcmanfm // crashes
Patch2:         libfm-0.1.12-filen-begin-with-slasla.patch
# Fedora bug 607069, pcmanfm --desktop crashes when clicking volume icon
Patch3:         libfm-0.1.12-crash-on-click-on-volume-entry-on-desktop-patch

BuildRequires:  gtk2-devel >= 2.16.0
BuildRequires:  menu-cache-devel >= 0.3.2
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  desktop-file-utils

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig


%description
LibFM is a GIO-based library used to develop file manager-like programs. It is
developed as the core of next generation PCManFM and takes care of all file-
related operations such as copy & paste, drag & drop, file associations or 
thumbnails support. By utilizing glib/gio and gvfs, libfm can access remote 
file systems supported by gvfs.

This package contains the generic non-gui functions of libfm.


%package        gtk
Summary:        File manager-related GTK+ widgets of %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gvfs

%description    gtk
libfm is a GIO-based library used to develop file manager-like programs. It is
developed as the core of next generation PCManFM and takes care of all file-
related operations such as copy & paste, drag & drop, file associations or 
thumbnail support. By utilizing glib/gio and gvfs, libfm can access remote 
file systems supported by gvfs.

This package provides useful file manager-related GTK+ widgets.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        gtk-devel
Summary:        Development files for %{name}-gtk
Group:          Development/Libraries
Requires:       %{name}-gtk = %{version}-%{release}
Requires:       %{name}-devel = %{version}-%{release}

%description    gtk-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}-gtk.


%prep
%setup -q

%patch0 -p1 -b .orig
%patch1 -p1 -b .sort_cs
%patch2 -p1 -b .slasla
%patch3 -p1 -b .desk_vol

# treak rpath
sed -i.libdir_syssearch -e \
  '/sys_lib_dlsearch_path_spec/s|/usr/lib |/usr/lib /usr/lib64 /lib /lib64 |' \
  configure

%build
%configure --disable-static
# To show translation status
make -C po -j1 GMSGFMT="msgfmt --statistics"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

desktop-file-validate %{buildroot}/%{_datadir}/applications/*.desktop

%find_lang %{name}

echo '%%defattr(-,root,root,-)' > base-header.files
echo '%%defattr(-,root,root,-)' > gtk-header.files
for f in $RPM_BUILD_ROOT%_includedir/%name/%name/*.h
do
  bf=$(basename $f)
  for dir in base job
  do
    if [ -f src/$dir/$bf ]
    then
      echo %_includedir/%name/%name/$bf >> base-header.files
    fi
  done
  for dir in gtk
  do
    if [ -f src/$dir/$bf ]
    then
      echo %_includedir/%name/%name/$bf >> gtk-header.files
    fi
  done
done

/usr/lib/rpm/check-rpaths

%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
update-mime-database %{_datadir}/mime &> /dev/null || :


%postun
/sbin/ldconfig
update-mime-database %{_datadir}/mime &> /dev/null || :


%post gtk -p /sbin/ldconfig


%postun gtk -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
# FIXME: Add ChangeLog and NEWS if not empty
%doc AUTHORS COPYING README
%dir %{_sysconfdir}/xdg/libfm/
%config(noreplace) %{_sysconfdir}/xdg/libfm/pref-apps.conf
%config(noreplace) %{_sysconfdir}/xdg/libfm/libfm.conf
%{_libdir}/%{name}.so.*
%{_libdir}/gio/modules/libgiofm.so
%{_datadir}/mime/packages/libfm.xml


%files gtk
%defattr(-,root,root,-)
%{_bindir}/libfm-pref-apps
%{_libdir}/%{name}-gtk.so.*
%dir %{_libdir}/libfm/
%{_libdir}/libfm/gnome-terminal
%{_datadir}/libfm/
%{_datadir}/applications/libfm-pref-apps.desktop


%files devel -f base-header.files
%defattr(-,root,root,-)
%doc TODO
%dir %{_includedir}/libfm/
%dir %{_includedir}/libfm/libfm/
%{_includedir}/libfm/libfm/fm.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/libfm.pc


%files gtk-devel -f gtk-header.files
%defattr(-,root,root,-)
%{_includedir}/libfm/libfm/fm-gtk.h
%{_libdir}/%{name}-gtk.so
%{_libdir}/pkgconfig/libfm-gtk.pc


%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.1.12-1
- Initial packaging for RERemix

