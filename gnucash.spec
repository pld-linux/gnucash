# TODO:
# - make separate subpackages with ofx, hbci, sql (like in included spec)
%include	/usr/lib/rpm/macros.perl
Summary:	GnuCash is an application to keep track of your finances
Summary(ja.UTF-8):	GnuCash - 家計簿ソフト
Summary(pl.UTF-8):	GnuCash - aplikacja do zarządzania twoimi finansami
Summary(pt_BR.UTF-8):	O GnuCash é uma aplicação para acompanhamento de suas finanças
Summary(zh_CN.UTF-8):	GnuCash - 您的个人财务管理软件
Name:		gnucash
Version:	2.1.2
Release:	0.1
License:	GPL v2
Group:		X11/Applications
Source0:	http://www.gnucash.org/pub/gnucash/sources/unstable/2.1.x/%{name}-%{version}.tar.gz
# Source0-md5:	4f2e59d3d746162721aa17ac314cfef9
Source1:	%{name}-icon.png
URL:		http://www.gnucash.org/
BuildRequires:	GConf2-devel >= 2.0
BuildRequires:	aqbanking-devel >= 1.0.0
BuildRequires:	db-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.6.0
BuildRequires:	gtk+2-devel >= 2:2.6.0
BuildRequires:	gtkhtml-devel >= 3.8
BuildRequires:	guile-devel >= 5:1.6
BuildRequires:	guile-www
BuildRequires:	ktoblzcheck-devel
BuildRequires:	libglade2-devel >= 2.4
BuildRequires:	libgnomeprint-devel >= 2.2
BuildRequires:	libgnomeprintui-devel >= 2.2
BuildRequires:	libgnomeui-devel >= 2.4
BuildRequires:	libgoffice-devel >= 0.0.4
BuildRequires:	libgsf-gnome-devel >= 1.12.2
BuildRequires:	libltdl-devel
BuildRequires:	libofx-devel >= 0.7.0
BuildRequires:	libxml2-devel >= 1:2.5.10
BuildRequires:	pango-devel >= 1.8.0
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= 1.5
BuildRequires:	postgresql-devel
BuildRequires:	qof-devel >= 0.6.2
BuildRequires:	sed >= 4.0
BuildRequires:	slib >= 2c4
BuildRequires:	texinfo
Requires(post,preun):	/sbin/ldconfig
Requires:	guile-www
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GnuCash is a personal finance manager. A check-book like register GUI
allows you to enter and track bank accounts, stocks, income and even
currency trades. The interface is designed to be simple and easy to
use, but is backed with double-entry accounting principles to ensure
balanced books.

%description -l ja.UTF-8
GnuCash は個人向け会計ソフトです。GUI を利用して収入・支出・銀行口座・
株式などの取り引きを記帳できます。インターフェースはシンプルに、簡単に
利用できるように設計していますが、正確さを追及しているために複式簿記の
会計規準を利用しており、複式簿記に関する知識が必要です。

%description -l pl.UTF-8
GnuCash jest programem do zarządzania finansami osobistymi. Pozwala na
śledzenie i wpisywanie zasobów na swoich kontach bankowych, zakładów.
Daje wgląd nawet w kursy walut. Interfejs został zaprojektowany z
myślą o prostocie i łatwości użycia.

%description -l pt_BR.UTF-8
O GnuCash é um gerenciador de finanças pessoais. Uma interface
parecida com um canhoto de cheques permite que você acompanhe contas
bancárias, ações, salário e mesmo tabelas de câmbio de moedas. A
interface foi projetada para ser simples e fácil de usar, mas tem o
suporte de princípios de contabilidade com entrada dupla para garantir
livros balanceados.

%package devel
Summary:	Header files for GnuCash libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek GnuCash
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for GnuCash libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek GnuCash.

%prep
%setup -q

# force regeneration after patching types in table.m4
rm -f src/backend/postgres/base-autogen.c

sed -i -e 's/Categories=Application;Office/Categories=GTK;GNOME;Office/' src/gnome/gnucash.desktop.in
cat >> src/gnome/gnucash.desktop.in <<EOF
Encoding=UTF-8
EOF

%build
%configure \
	--disable-prefer-db1 \
	--enable-hbci \
	--enable-ofx \
	--enable-sql

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pixmapsdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	gnomeappdir=%{_desktopdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}

%find_lang %{name}
# --with-gnome

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
%{_sysconfdir}/gconf/schemas/*.schemas
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/gnucash/config
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/lib*.so
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so*
%{_libdir}/%{name}/overrides
%{_desktopdir}/gnucash.desktop
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/accounts
%{_datadir}/%{name}/accounts/C
%lang(da) %{_datadir}/%{name}/accounts/da
%lang(de_AT) %{_datadir}/%{name}/accounts/de_AT
%lang(de_CH) %{_datadir}/%{name}/accounts/de_CH
%lang(de_DE) %{_datadir}/%{name}/accounts/de_DE
%lang(el_GR) %{_datadir}/%{name}/accounts/el_GR
%lang(en_GB) %{_datadir}/%{name}/accounts/en_GB
%lang(es_ES) %{_datadir}/%{name}/accounts/es_ES
%lang(fr_CA) %{_datadir}/%{name}/accounts/fr_CA
%lang(fr_CH) %{_datadir}/%{name}/accounts/fr_CH
%lang(fr_FR) %{_datadir}/%{name}/accounts/fr_FR
%lang(hu_HU) %{_datadir}/%{name}/accounts/hu_HU
%lang(it) %{_datadir}/%{name}/accounts/it
%lang(nb) %{_datadir}/%{name}/accounts/nb
%lang(pt_BR) %{_datadir}/%{name}/accounts/pt_BR
%lang(pt_PT) %{_datadir}/%{name}/accounts/pt_PT
%lang(sk) %{_datadir}/%{name}/accounts/sk
%lang(tr_TR) %{_datadir}/%{name}/accounts/tr_TR
%{_datadir}/%{name}/checks
%{_datadir}/%{name}/doc
%{_datadir}/%{name}/glade
%{_datadir}/%{name}/guile-modules
%{_datadir}/%{name}/pixmaps
%{_datadir}/%{name}/scm
%{_datadir}/%{name}/tip_of_the_day.list
%{_datadir}/%{name}/ui
%{_datadir}/%{name}/xml
%{_infodir}/gnucash-design.info*
%{_mandir}/man1/gnc-prices.1*
%{_mandir}/man1/gnucash.1*
%{_pixmapsdir}/*
%{_datadir}/xml/%{name}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/%{name}/*.la
%{_includedir}/%{name}
