%include	/usr/lib/rpm/macros.perl
Summary:	GnuCash is an application to keep track of your finances
Summary(pl):	GnuCash - aplikacja do zarz±dzania twoimi finansami
Summary(pt_BR):	O GnuCash é uma aplicação para acompanhamento de suas finanças
Name:		gnucash
Version:	1.6.6
Release:	0.1
License:	GPL
Group:		X11/Applications
Source0:	http://www.gnucash.org/pub/gnucash/sources/stable/%{name}-%{version}.tar.gz
Source1:	%{name}-icon.png
Patch0:		%{name}-am15.patch
Patch1:		%{name}-info.patch
Patch2:		%{name}-ignore_db1.patch
Patch3:		%{name}-libxml_includes_dir.patch
URL:		http://www.gnucash.org/
Requires:	slib
Requires:	guile >= 1.3.4
Requires:	gnome-print >= 0.21
Requires:	perl
BuildRequires:	GConf-devel
BuildRequires:	Guppi-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bonobo-devel
BuildRequires:	db3-devel
BuildRequires:	freetype-devel
BuildRequires:	g-wrap-devel >= 1.1.9
BuildRequires:	gal-devel
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	gettext-devel
BuildRequires:	gnome-libs-devel
BuildRequires:	gnome-print-devel
BuildRequires:	gtk+-devel
BuildRequires:	gtkhtml-devel >= 0.8
BuildRequires:	guile-devel
BuildRequires:	libghttp-devel
BuildRequires:	libglade-devel
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	libxml-devel
BuildRequires:	slib
BuildRequires:	texinfo
Prereq:		/sbin/ldconfig
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
wpisywanie zasobów na swoich kontach bankowych, zak³adów. Daje wgl±d
nawet w kursy walut. Interfejs zosta³ zaprojektowany z my¶l± o
prostocie i ³atwo¶ci u¿ycia.

%description -l pt_BR
O GnuCash é um gerenciador de finanças pessoais. Uma interface
parecida com um canhoto de cheques permite que você acompanhe contas
bancárias, ações, salário e mesmo tabelas de câmbio de moedas. A
interface foi projetada para ser simples e fácil de usar, mas tem o
suporte de princípios de contabilidade com entrada dupla para garantir
livros balanceados.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
rm -f missing src/guile/Makefile.in
libtoolize --copy --force
aclocal -I %{_aclocaldir}/gnome
autoconf
automake -a -c -f

## Kloczek, dont touch this!
#CFLAGS='%{rpmcflags} -I/usr/X11R6/include'
#LDFLAGS='%{rpmldflags} -ldb3'
#export CFLAGS LDFLAGS

%configure \
	--disable-prefer-db1

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GNC_DOC_INSTALL_DIR=%{_docdir}/%{name}-%{version}/ \
	gnomeappdir=%{_applnkdir}/Office/Misc

perl -pi -e 's/=gnome-money.png/=gnucash-icon.png/' \
	$RPM_BUILD_ROOT%{_applnkdir}/Office/Misc/gnucash.desktop

install %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}

gzip -9nf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/[!e]*

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_libdir}/libgncengine.so.*.*.*
%{_mandir}/*/*
%{_infodir}/*info*gz
%{_applnkdir}/Office/Misc/*
%dir %{_datadir}/gnucash
%{_datadir}/gnucash/[!a]*
%dir %{_datadir}/gnucash/accounts
%{_datadir}/gnucash/accounts/C
%lang(da) %{_datadir}/gnucash/accounts/da
%lang(de_DE) %{_datadir}/gnucash/accounts/de_DE
%lang(es_ES) %{_datadir}/gnucash/accounts/es_ES
%lang(pt_PT) %{_datadir}/gnucash/accounts/pt_PT
%lang(sk) %{_datadir}/gnucash/accounts/sk
%{_datadir}/mime-info/*
%{_pixmapsdir}/%{name}
%{_pixmapsdir}/%{name}-icon.png
%{_sysconfdir}/gnucash
%doc %{_docdir}/%{name}-%{version}/
