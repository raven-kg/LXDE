Name:		lxsplit
Version:	0.2.4
Release:	1%{?dist}
Summary:	File split / merge utility

Group:		Applications/File
License:	GPLv2+
URL:		http://lxsplit.sourceforge.net/
Source:		http://downloads.sourceforge.net/lxsplit/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)	

%description
lxSplit is a simple tool for splitting files and joining the splitted files 
on linux and unix-like platforms. Splitting is done without compression and 
large files (> 4 GB) are supported. lxSplit is fully compatible with the 
HJSplit utility which is available for other operating systems.



%prep
%setup -q

%build
%{__make}  CFLAGS="$RPM_OPT_FLAGS" %{?_smp_flags}

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}/%{_bindir}
%{__install} -D -m755 lxsplit %{buildroot}/%{_bindir}/lxsplit

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog README COPYING
%{_bindir}/lxsplit

%changelog
* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 0.2.4-1
- Initial packaging for RERemix

