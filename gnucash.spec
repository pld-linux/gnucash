Name:		gnucash
Summary:	GnuCash is an application to keep track of your finances.
Version:	1.4.0
Release:	0
Copyright:	Free Software Foundation
Group:		Applications/Finance
Source0:	http://www.gnucash.org/pub/gnucash/sources/stable/%{name}-%{PACKAGE_VERSION}.tar.gz
Patch0:		gnucash-destdir.patch
URL:		Http://www.gnucash.org
Requires:	slib
Requires:	guile >= 1.3
Requires:	g-wrap
BuildRequires:	gnome-libs-devel
BuildRequires:	esound-devel
BuildRequires:	libxml-devel
BuildRequires:	g-wrap-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GnuCash is a personal finance manager. A check-book like register GUI
allows you to enter and track bank accounts, stocks, income and even
currency trades. The interface is designed to be simple and easy to use,
but is backed with double-entry accounting principles to ensure balanced
books.

%prep
%setup -q
%patch0 -p1

%build
automake
%configure 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT GNC_DOC_INSTALL_DIR=%{_docdir}/%{name}-%{version}/ \
gnomeappdir=%{_applnkdir}/Applications install

strip --strip-unneed $RPM_BUILD_ROOT%{_libdir}/libgncengine.so.0.1.1
strip --strip-unneed $RPM_BUILD_ROOT%{_libdir}/gnucash/perl/libgncswig.so.0.1.1

gzip -9nfr $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/* $RPM_BUILD_ROOT%{_mandir}/man1/*

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gnucash
%attr(755,root,root) %{_bindir}/gnc-prices
%{_libdir}/gnucash/perl/*.so*
%{_libdir}/libgncengine.so*
%{_mandir}/man1/*
%{_datadir}/gnucash/html/C
%lang(fr) %{_datadir}/gnucash/html/fr
%{_datadir}/gnucash/html/index.html
%{_datadir}/gnucash/html/gnucash.css
%{_datadir}/gnucash/scm
%{_datadir}/gnucash/perl
%{_sysconfdir}/gnucash/config
%{_applnkdir}/Applications/gnucash.desktop
%doc %{_docdir}/%{name}-%{version}/
