%include	/usr/lib/rpm/macros.perl
Summary:	GnuCash is an application to keep track of your finances
Summary(pl):	GnuCash - aplikacja do zarz±dzania twoimi finansami
Name:		gnucash
Version:	1.6.4
Release:	1
License:	GPL
Group:		X11/Applications
Group(de):	X11/Applikationen
Group(pl):	X11/Aplikacje
Source0:	http://www.gnucash.org/pub/gnucash/sources/stable/%{name}-%{version}.tar.gz
URL:		http://www.gnucash.org/
Requires:	slib
Requires:	guile >= 1.3.4
Requires:	gnome-print >= 0.21
Requires:	perl
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bonobo-devel
BuildRequires:	db1-devel
BuildRequires:	gal-devel
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	gettext-devel
BuildRequires:	gnome-libs-devel
BuildRequires:	gnome-print-devel
BuildRequires:	gtk+-devel
BuildRequires:	gtkhtml-devel >= 0.8
BuildRequires:	guile-devel
BuildRequires:	Guppi-devel
BuildRequires:	g-wrap-devel >= 1.1.9
BuildRequires:	libghttp-devel
BuildRequires:	libglade-devel
BuildRequires:	libtool
BuildRequires:	libxml-devel
# Test for Guppi needs it
BuildRequires:	readline-devel
BuildRequires:	python-devel
BuildRequires:	libwrap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_sysconfdir	/etc/X11

%description
GnuCash is a personal finance manager. A check-book like register GUI
allows you to enter and track bank accounts, stocks, income and even
currency trades. The interface is designed to be simple and easy to
use, but is backed with double-entry accounting principles to ensure
balanced books.

%description -l pl
GnuCash jest mened¿erem finansów osobistych. Pozwala na ¶ledzenie i 
wpisywanie zasobów na swoich kontach bankowych, zak³adów. Daje
wgl±d nawet w kursy walut. Interfejs zosta³ zaprojektowany z my¶l±
o prostocie i ³atwo¶ci u¿ycia.

%prep -q
%setup -q

%build
#rm -f missing src/guile/Makefile.in
#aclocal -I ./macros
#libtoolize --copy --force
#automake -a -c
#autoconf

CFLAGS='%{rpmcflags} -L/usr/X11R6/lib -I/usr/X11R6/include'
export CFLAGS
%configure2_13

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GNC_DOC_INSTALL_DIR=%{_docdir}/%{name}-%{version}/ \
	gnomeappdir=%{_applnkdir}/Office/Misc

gzip -9nf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/[!e]*

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_libdir}/libgncengine.so.*.*.*
%{_mandir}/*/*
%{_infodir}/*
%{_applnkdir}/Office/Misc/*
%{_datadir}/%{name}
%{_datadir}/mime-info/*
%{_pixmapsdir}/%{name}
%{_sysconfdir}/gnucash
%doc %{_docdir}/%{name}-%{version}/
