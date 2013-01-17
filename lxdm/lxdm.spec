Name:           lxdm
Version:        0.4.1
Release:        1%{?dist}
Summary:        Lightweight X11 Display Manager

Group:          User Interface/Desktops
License:        GPLv2+ and LGPLv2+
URL:            http://lxde.org

Source0:        http://downloads.sourceforge.net/sourceforge/lxde/%{name}-%{version}.tar.gz

# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxdm;a=commit;h=19f82a20
Patch0:         lxdm-0.4.1-null-pointer.patch

# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxdm;a=commit;h=bed2fed7
Patch1:         lxdm-0.4.1-missing-semicolons.patch

# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxdm;a=commit;h=14b6c103
Patch2:         lxdm-0.4.1-spelling-mistake.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=794478
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxdm;a=commit;h=d4e41ecb
Patch3:         lxdm-0.4.1-softlockup.patch

# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxdm;a=commit;h=13a92c1d
Patch4:        lxdm-0.4.1-tcp-listen.patch

# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxdm;a=commit;h=f11ae65e
Patch5:         lxdm-0.4.1-exec-dbus.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=635897
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxdm;a=commit;h=a8db292c
Patch6:         lxdm-0.4.1-xauth.patch

# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxdm;a=commit;h=9dc81f33
Patch7:         lxdm-0.4.1-no-password.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=758484
# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxdm;a=commit;h=bd278369
Patch8:         lxdm-0.4.1-GDK_KEY_Escape.patch

# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxdm;a=commit;h=0c6d56ba
Patch9:         lxdm-0.4.1-LXSESSION-variable.patch

# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxdm;a=commit;h=d3a85803
Patch10:         lxdm-0.4.1-old-plymouth.patch

# http://lxde.git.sourceforge.net/git/gitweb.cgi?p=lxde/lxdm;a=patch;h=8c71ffc87
Patch11:        lxdm-0.4.1-restart-xserver-on-logout.patch

## Distro specific patches ##

# Distro artwork, start on vt1
Patch50:        lxdm-0.4.1-config.patch

# SELinux, permit graphical root login etc.
Patch51:        lxdm-0.4.1-pam.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  pkgconfig(gtk+-2.0) >= 2.12.0
BuildRequires:  iso-codes-devel
BuildRequires:  ConsoleKit-devel
BuildRequires:  pam-devel
BuildRequires:  intltool >= 0.40.0
Requires:       pam
Requires:       /sbin/shutdown
Requires:       redhat-logos
# needed for anaconda to boot into runlevel 5 after install
Provides:       service(graphical-login) = lxdm


%description
LXDM is the future display manager of LXDE, the Lightweight X11 Desktop 
environment. It is designed as a lightweight alternative to replace GDM or 
KDM in LXDE distros. It's still in very early stage of development.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .null-pointer
%patch1 -p1 -b .missing-semicolons
%patch2 -p1 -b .spelling-mistake
%patch3 -p1 -b .softlockup
%patch4 -p1 -b .tcp-listen
%patch5 -p1 -b .exec-dbus
%patch6 -p1 -b .xauth
%patch7 -p1 -b .no-password
%patch8 -p1 -b .GDK_KEY_Escape
%patch9 -p1 -b .LXSESSION-variable
%patch10 -p1 -b .old-plymouth
%patch11 -p1 -b .restart-xserver

%patch50 -p1 -b .config
%patch51 -p1 -b .orig


%build
%configure
make %{?_smp_mflags} V=1


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL='install -p'
%find_lang %{name}

# these files are not in the package, but should be owned by lxdm 
touch %{buildroot}%{_sysconfdir}/%{name}/xinitrc
mkdir -p %{buildroot}%{_localstatedir}/run/%{name}
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}
touch %{buildroot}%{_localstatedir}/lib/%{name}.conf

%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
# FIXME add ChangeLog and NEWS if not empty
%doc AUTHORS COPYING README TODO gpl-2.0.txt lgpl-2.1.txt
%dir %{_sysconfdir}/%{name}
%ghost %config(noreplace,missingok) %{_sysconfdir}/%{name}/xinitrc
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/%{name}/Xsession
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/%{name}/LoginReady
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/%{name}/PostLogin
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/%{name}/PostLogout
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/%{name}/PreLogin
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/%{name}/PreReboot
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/%{name}/PreShutdown
%config %{_sysconfdir}/%{name}/lxdm.conf
%config(noreplace) %{_sysconfdir}/pam.d/%{name}

%{_bindir}/%{name}-config
%{_sbindir}/%{name}
%{_sbindir}/lxdm-binary
%{_libexecdir}/lxdm-greeter-gtk
%{_libexecdir}/lxdm-greeter-gdk
%{_libexecdir}/lxdm-numlock
%{_datadir}/%{name}/

%dir %{_localstatedir}/run/%{name}

%dir %{_localstatedir}/lib/%{name}
%ghost %{_localstatedir}/lib/%{name}.conf


%changelog
* Tue Jan 08 2013 Raven <raven_kg@megaline.kg> - 0.4.1-1
- updated to 0.4.1

* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.3.0-1
- Initial packaging for RERemix