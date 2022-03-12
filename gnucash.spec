# TODO:
# - make separate subpackages with ofx, hbci, sql (like in included spec)
# - when you have gnucash 2.2.0 already instaled you probalby get this error message:
# /usr/lib64/libgnc-backend-file-utils.so.0: undefined reference to `xaccSchedXactionSetFreqSpec'
# /usr/lib64/libgnc-backend-file-utils.so.0: undefined reference to `xaccFreqSpecFree'
# /usr/lib64/libgnc-backend-file-utils.so.0: undefined reference to `xaccFreqSpecMalloc'
# /usr/lib64/libgnc-backend-file-utils.so.0: undefined reference to `xaccFreqSpecSetUIType'
# /usr/lib64/libgnc-backend-file-utils.so.0: undefined reference to `xaccFreqSpecGetUIType'
# uninstall old gnucash before building
#
# Conditional build:
%bcond_without	hbci		# don't build HBCI support
%bcond_without	dbi		# don't build SQL support (via libdbi)
%bcond_without	webkit		# disable WebKit, use GtkHTML
#
%define guile_version 3.0
#
Summary:	GnuCash is an application to keep track of your finances
Summary(ja.UTF-8):	GnuCash - 家計簿ソフト
Summary(pl.UTF-8):	GnuCash - aplikacja do zarządzania twoimi finansami
Summary(pt_BR.UTF-8):	O GnuCash é uma aplicação para acompanhamento de suas finanças
Summary(zh_CN.UTF-8):	GnuCash - 您的个人财务管理软件
Name:		gnucash
Version:	4.9
Release:	3
License:	GPL v2+
Group:		X11/Applications
Source0:	https://sourceforge.net/projects/gnucash/files/gnucash%20%28stable%29/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	50747ca64f90568b9280f8797f2d2512
URL:		http://www.gnucash.org/
BuildRequires:	boost-devel >= 1.60.0
BuildRequires:	cmake >= 3.5
BuildRequires:	doxygen
BuildRequires:	gdk-pixbuf2-devel
BuildRequires:	glib2-devel >= 2.56.1
BuildRequires:	gmock-devel >= 1.8.0
BuildRequires:	gtest-devel >= 1.8.0
BuildRequires:	gtk+3-devel >= 3.10.0
BuildRequires:	guile-devel
BuildRequires:	libatomic_ops-devel
BuildRequires:	libglade2-devel
BuildRequires:	libgnome-keyring-devel >= 0.6
BuildRequires:	libicu-devel
BuildRequires:	libofx-devel >= 0.9.0
BuildRequires:	libsecret-devel >= 0.18
BuildRequires:	libxml2-devel >= 2.7.0
BuildRequires:	libxslt-devel
BuildRequires:	libxslt-progs
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	python3-devel
BuildRequires:	swig >= 3.0.12
BuildRequires:	swig-guile
%if %{with dbi}
BuildRequires:	libdbi-devel >= 0.8.3
BuildRequires:	libdbi-drivers-sqlite3
%endif
%if %{with hbci}
BuildRequires:	aqbanking-devel >= 6.0.0
BuildRequires:	gwenhywfar-devel >= 3.99.20
BuildRequires:	gwenhywfar-gui-gtk3-devel >= 3.99.20
BuildRequires:	ktoblzcheck-devel >= 1.20
%endif
%if %{with webkit}
BuildRequires:	gtk-webkit4-devel
%endif
Requires(post,preun):	/sbin/ldconfig
Recommends:	%{name}-docs
# For translation of currency names
Recommends:	iso-codes
Recommends:	python3-gnucash = %{version}
# Optional perl modules for online price retrieval
Recommends:	perl(Date::Manip)
Recommends:	perl(Finance::Quote)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautostrip	.*\\.go

%description
GnuCash is a personal finance manager. A check-book like register GUI
allows you to enter and track bank accounts, stocks, income and even
currency trades. The interface is designed to be simple and easy to
use, but is backed with double-entry accounting principles to ensure
balanced books.

%description -l ja.UTF-8
GnuCash は個人向け会計ソフトです。GUI を利用して収入・支出・銀行口座・
株式などの取り引きを記帳できます。インターフェースはシンプルに、簡単に
利用できるように設計していますが、正確さを追及しているために複式簿記の 会計規準を利用しており、複式簿記に関する知識が必要です。

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

%package -n python3-gnucash
Summary:	Python bindings for GnuCash
Summary(pl.UTF-8):	Wiązania Pythona 3.x dla GnuCash
Group:		Development/Languages/Python
Requires:	%{name} = %{version}

%description -n python3-gnucash
This package provides the Python 3 bindings for development of
GnuCash, a personal finance manager.

%description -n python3-gnucash -l pt_BR.UTF-8
Ten pakiet zawiera powiązania Pythona 3 do programowania GnuCash,
menedżera finansów osobistych.

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
#%patch0 -p1

%build
install -d build
cd build

%cmake \
  -DCMAKE_INSTALL_DOCDIR:PATH=%{_docdir}/%{name} \
  -DWITH_PYTHON=ON \
  ../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

cd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd ..

rm -rf $RPM_BUILD_ROOT%{_localedir}/{kok@latin,mni@bengali}
rm $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/gschemas.compiled

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir %{_sysconfdir}/gnucash
%{_sysconfdir}/gnucash/environment
%attr(755,root,root) %{_bindir}/gnc-fq-check
%attr(755,root,root) %{_bindir}/gnc-fq-dump
%attr(755,root,root) %{_bindir}/gnc-fq-helper
%attr(755,root,root) %{_bindir}/gnc-fq-update
%attr(755,root,root) %{_bindir}/gnucash
%attr(755,root,root) %{_bindir}/gnucash-cli
%attr(755,root,root) %{_bindir}/gnucash-valgrind
%attr(755,root,root) %{_libdir}/lib*.so
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so*
%dir %{_libdir}/guile/%{guile_version}/site-ccache
%{_libdir}/guile/%{guile_version}/site-ccache/%{name}
%{_desktopdir}/gnucash.desktop
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/accounts
%{_datadir}/%{name}/accounts/C
%lang(ca) %{_datadir}/%{name}/accounts/ca
%lang(cs) %{_datadir}/%{name}/accounts/cs
%lang(da) %{_datadir}/%{name}/accounts/da
%lang(de) %{_datadir}/%{name}/accounts/de_DE
%lang(de_AT) %{_datadir}/%{name}/accounts/de_AT
%lang(de_CH) %{_datadir}/%{name}/accounts/de_CH
%lang(el) %{_datadir}/%{name}/accounts/el_GR
%lang(en_GB) %{_datadir}/%{name}/accounts/en_GB
%lang(en_IN) %{_datadir}/%{name}/accounts/en_IN
%lang(es) %{_datadir}/%{name}/accounts/es_ES
%lang(es_MX) %{_datadir}/%{name}/accounts/es_MX
%lang(fi_FI) %{_datadir}/%{name}/accounts/fi_FI
%lang(fr) %{_datadir}/%{name}/accounts/fr_FR
%lang(fr_BE) %{_datadir}/%{name}/accounts/fr_BE
%lang(fr_CA) %{_datadir}/%{name}/accounts/fr_CA
%lang(fr_CH) %{_datadir}/%{name}/accounts/fr_CH
%lang(he) %{_datadir}/%{name}/accounts/he
%lang(hr) %{_datadir}/%{name}/accounts/hr
%lang(hu) %{_datadir}/%{name}/accounts/hu
%lang(it) %{_datadir}/%{name}/accounts/it
%lang(ja) %{_datadir}/%{name}/accounts/ja
%lang(ko) %{_datadir}/%{name}/accounts/ko
%lang(lt) %{_datadir}/%{name}/accounts/lt
%lang(lv) %{_datadir}/%{name}/accounts/lv
%lang(nb) %{_datadir}/%{name}/accounts/nb
%lang(nl) %{_datadir}/%{name}/accounts/nl
%lang(pl) %{_datadir}/%{name}/accounts/pl
%lang(pt) %{_datadir}/%{name}/accounts/pt_PT
%lang(pt_BR) %{_datadir}/%{name}/accounts/pt_BR
%lang(ru) %{_datadir}/%{name}/accounts/ru
%lang(sk) %{_datadir}/%{name}/accounts/sk
%lang(sv_AX) %{_datadir}/%{name}/accounts/sv_AX
%lang(sv_FI) %{_datadir}/%{name}/accounts/sv_FI
%lang(sv) %{_datadir}/%{name}/accounts/sv_SE
%lang(tr) %{_datadir}/%{name}/accounts/tr_TR
%lang(zh_CN) %{_datadir}/%{name}/accounts/zh_CN
%lang(zh_HK) %{_datadir}/%{name}/accounts/zh_HK
%lang(zh_TW) %{_datadir}/%{name}/accounts/zh_TW
%dir %{_datadir}/%{name}/checks
%{_datadir}/%{name}/checks/*.chk
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/AUTHORS
%{_docdir}/%{name}/ChangeLog
%{_docdir}/%{name}/ChangeLog.1999
%{_docdir}/%{name}/ChangeLog.2000
%{_docdir}/%{name}/ChangeLog.2001
%{_docdir}/%{name}/ChangeLog.2002
%{_docdir}/%{name}/ChangeLog.2003
%{_docdir}/%{name}/ChangeLog.2004
%{_docdir}/%{name}/ChangeLog.2005
%{_docdir}/%{name}/ChangeLog.2006
%{_docdir}/%{name}/ChangeLog.2007
%{_docdir}/%{name}/ChangeLog.2008
%{_docdir}/%{name}/ChangeLog.2009
%{_docdir}/%{name}/ChangeLog.2010
%{_docdir}/%{name}/ChangeLog.2011
%{_docdir}/%{name}/ChangeLog.2012
%{_docdir}/%{name}/ChangeLog.2013
%{_docdir}/%{name}/ChangeLog.2014
%{_docdir}/%{name}/ChangeLog.2015
%{_docdir}/%{name}/ChangeLog.2016
%{_docdir}/%{name}/ChangeLog.2017
%{_docdir}/%{name}/ChangeLog.2018
%{_docdir}/%{name}/ChangeLog.2019
%{_docdir}/%{name}/ChangeLog.2020
%{_docdir}/%{name}/DOCUMENTERS
%{_docdir}/%{name}/HACKING
%{_docdir}/%{name}/LICENSE
%{_docdir}/%{name}/Money95bank_fr.qif
%{_docdir}/%{name}/Money95invst_fr.qif
%{_docdir}/%{name}/Money95mfunds_fr.qif
%{_docdir}/%{name}/Money95stocks_fr.qif
%{_docdir}/%{name}/NEWS
%{_docdir}/%{name}/README
%{_docdir}/%{name}/README.dependencies
%{_docdir}/%{name}/README_invoice
%{_docdir}/%{name}/gtk-3.0.css
%{_docdir}/%{name}/abc-all.qif
%{_docdir}/%{name}/abc.qif
%{_docdir}/%{name}/bogus.qif
%{_docdir}/%{name}/cbb-export.qif
%{_docdir}/%{name}/currency_tree_xml.%{name}
%{_docdir}/%{name}/every.qif
%{_docdir}/%{name}/invoice.csv
%{_docdir}/%{name}/ms-money.qif
%{_docdir}/%{name}/quicktest.qif
%{_docdir}/%{name}/swipe.qif
%{_docdir}/%{name}/taxreport.%{name}
%{_docdir}/%{name}/web.qif
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.deprecated.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.dialogs.business.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.dialogs.checkprinting.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.dialogs.commodities.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.dialogs.export.csv.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.dialogs.flicker.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.dialogs.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.dialogs.import.csv.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.dialogs.import.generic.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.dialogs.import.hbci.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.dialogs.import.ofx.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.dialogs.import.qif.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.dialogs.reconcile.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.dialogs.sxs.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.dialogs.totd.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.general.finance-quote.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.history.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.warnings.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.window.pages.account.tree.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.GnuCash.window.pages.gschema.xml
%dir %{_datadir}/%{name}/icons
%{_datadir}/%{name}/icons/hicolor
%dir %{_datadir}/%{name}/gtkbuilder
%{_datadir}/%{name}/gtkbuilder/*.glade
%dir %{_datadir}/%{name}/chartjs
%{_datadir}/%{name}/chartjs/*.js
%{_datadir}/%{name}/tip_of_the_day.list
%{_datadir}/%{name}/ui
%{_datadir}/%{name}/pixmaps
%{_datadir}/metainfo/gnucash.appdata.xml
%{_datadir}/%{name}/pref_transformations.xml
%dir %{_datadir}/guile/site/%{guile_version}
%{_datadir}/guile/site/%{guile_version}/%{name}
%{_mandir}/man1/gnc-fq-dump.1*
%{_mandir}/man1/gnc-fq-helper.1*
%{_mandir}/man1/gnucash.1*
%{_mandir}/man1/gnucash-cli.1*
%{_iconsdir}/hicolor/*/apps/*

%files -n python3-gnucash
%defattr(644,root,root,755)
%{_datadir}/gnucash/python
%dir %{py3_sitedir}/gnucash
%{py3_sitedir}/gnucash

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
