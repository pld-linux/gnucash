%include	/usr/lib/rpm/macros.perl
Summary:	GnuCash is an application to keep track of your finances
Summary(pl):	GnuCash - aplikacja do zarz�dzania twoimi finansami
Name:		gnucash
Version:	1.6.1
Release:	1
License:	GPL
Group:		X11/Applications
Group(de):	X11/Applikationen
Group(pl):	X11/Aplikacje
Source0:	http://www.gnucash.org/pub/gnucash/sources/stable/%{name}-%{version}.tar.gz
URL:		http://www.gnucash.org/
Requires:	slib
Requires:	guile >= 1.3.4
Requires:	g-wrap
Requires:	gnome-print >= 0.21
BuildRequires:	gnome-libs-devel
BuildRequires:	esound-devel
BuildRequires:	libxml-devel
BuildRequires:	g-wrap-static >= 1.1.9
BuildRequires:	bonobo-devel
BuildRequires:	libghttp-devel
BuildRequires:	gtkhtml-devel >= 0.8
BuildRequires:	libtool automake autoconf
BuildRequires:	gnome-print-devel
BuildRequires:	Guppi-devel
BuildRequires:	oaf-devel
BuildRequires:	guile-devel
BuildRequires:	libglade-devel
BuildRequires:	gtk+-devel
BuildRequires:	gal-devel
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	gettext-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _prefix         /usr/X11R6

%description
GnuCash is a personal finance manager. A check-book like register GUI
allows you to enter and track bank accounts, stocks, income and even
currency trades. The interface is designed to be simple and easy to
use, but is backed with double-entry accounting principles to ensure
balanced books.

%description -l pl
GnuCash jest mened�erem finans�w osobistych. Pozwala na �ledzenie i 
wpisywanie zasob�w na swoich kontach bankowych, zak�ad�w. Daje
wgl�d nawet w kursy walut. Interfejs zosta� zaprojektowany z my�l�
o prostocie i �atwo�ci u�ycia.

%prep -q
%setup -q

%build
rm missing
aclocal -I ./macros
libtoolize --copy --force
automake -a -c

%configure2_13

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} DESTDIR=$RPM_BUILD_ROOT \
	GNC_DOC_INSTALL_DIR=%{_docdir}/%{name}-%{version}/ \
	gnomeappdir=%{_applnkdir}/Office/Misc install

gzip -9nfr $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/*

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gnucash
%attr(755,root,root) %{_bindir}/gnc-prices
%{_libdir}/gnucash/perl/*.so*
%{_libdir}/libgncengine.so*
%{_mandir}/man1/*
%{_datadir}/gnucash/html/index.html
%{_datadir}/gnucash/html/gnucash.css
%{_datadir}/gnucash/scm
%{_datadir}/gnucash/perl
%{_sysconfdir}/gnucash/config
%{_applnkdir}/Office/Misc/gnucash.desktop
%doc %{_docdir}/%{name}-%{version}/
