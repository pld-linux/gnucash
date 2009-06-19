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
#
%include	/usr/lib/rpm/macros.perl
Summary:	GnuCash is an application to keep track of your finances
Summary(ja.UTF-8):	GnuCash - 家計簿ソフト
Summary(pl.UTF-8):	GnuCash - aplikacja do zarządzania twoimi finansami
Summary(pt_BR.UTF-8):	O GnuCash é uma aplicação para acompanhamento de suas finanças
Summary(zh_CN.UTF-8):	GnuCash - 您的个人财务管理软件
Name:		gnucash
Version:	2.2.9
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://www.gnucash.org/pub/gnucash/sources/stable/%{name}-%{version}.tar.bz2
# Source0-md5:	1d814de8673b4760045bf51b72924d04
Source1:	%{name}-icon.png
URL:		http://www.gnucash.org/
BuildRequires:	GConf2-devel >= 2.0
%if %{with hbci}
BuildRequires:	aqbanking-devel >= 1.6.0
BuildRequires:	aqbanking-devel < 2.9.0
%endif
BuildRequires:	db-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.6.0
BuildRequires:	gtk+2-devel >= 2:2.6.0
BuildRequires:	gtkhtml-devel >= 3.14
BuildRequires:	guile-devel >= 5:1.8.2-2
BuildRequires:	guile-www
BuildRequires:	ktoblzcheck-devel
BuildRequires:	libglade2-devel >= 2.4
BuildRequires:	libgnomeprint-devel >= 2.2
BuildRequires:	libgnomeprintui-devel >= 2.2
BuildRequires:	libgnomeui-devel >= 2.4
BuildRequires:	libgoffice-devel >= 0.3.0
BuildRequires:	libgsf-gnome-devel >= 1.12.2
BuildRequires:	libltdl-devel
BuildRequires:	libofx-devel >= 0.7.0
BuildRequires:	libxml2-devel >= 1:2.5.10
BuildRequires:	pango-devel >= 1.8.0
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= 1.5
BuildRequires:	postgresql-devel
BuildRequires:	readline-devel
BuildRequires:	sed >= 4.0
BuildRequires:	slib >= 2c4
BuildRequires:	texinfo
Requires(post,preun):	/sbin/ldconfig
Requires:	guile >= 5:1.8.2-2
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
	%{?with_hbci:--enable-hbci} \
	%{!?with_hbci:--disable-hbci} \
	--enable-ofx \
	--enable-sql

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pixmapsdir}

%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT \
	gnomeappdir=%{_desktopdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}

## Cleanup
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.so.[0-9]
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/doc/*win32-bin.txt

%find_lang %{name}
# --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
%gconf_schema_install apps_gnucash_dialog_business_common.schemas
%gconf_schema_install apps_gnucash_dialog_commodities.schemas
%gconf_schema_install apps_gnucash_dialog_common.schemas
%{?with_hbci:%gconf_schema_install apps_gnucash_dialog_hbci.schemas}
%gconf_schema_install apps_gnucash_dialog_prices.schemas
%gconf_schema_install apps_gnucash_dialog_print_checks.schemas
%gconf_schema_install apps_gnucash_dialog_reconcile.schemas
%gconf_schema_install apps_gnucash_dialog_totd.schemas
%gconf_schema_install apps_gnucash_general.schemas
%gconf_schema_install apps_gnucash_history.schemas
%gconf_schema_install apps_gnucash_import_generic_matcher.schemas
%gconf_schema_install apps_gnucash_import_qif.schemas
%gconf_schema_install apps_gnucash_warnings.schemas
%gconf_schema_install apps_gnucash_window_pages_account_tree.schemas
%gconf_schema_install apps_gnucash_window_pages_register.schemas
%gconf_schema_install apps_gnucash_dialog_scheduled_transctions.schemas

%preun
%gconf_schema_uninstall apps_gnucash_dialog_business_common.schemas
%gconf_schema_uninstall apps_gnucash_dialog_commodities.schemas
%gconf_schema_uninstall apps_gnucash_dialog_common.schemas
%{?with_hbci:%gconf_schema_uninstall apps_gnucash_dialog_hbci.schemas}
%gconf_schema_uninstall apps_gnucash_dialog_prices.schemas
%gconf_schema_uninstall apps_gnucash_dialog_print_checks.schemas
%gconf_schema_uninstall apps_gnucash_dialog_reconcile.schemas
%gconf_schema_uninstall apps_gnucash_dialog_totd.schemas
%gconf_schema_uninstall apps_gnucash_general.schemas
%gconf_schema_uninstall apps_gnucash_history.schemas
%gconf_schema_uninstall apps_gnucash_import_generic_matcher.schemas
%gconf_schema_uninstall apps_gnucash_import_qif.schemas
%gconf_schema_uninstall apps_gnucash_warnings.schemas
%gconf_schema_uninstall apps_gnucash_window_pages_account_tree.schemas
%gconf_schema_uninstall apps_gnucash_window_pages_register.schemas
%gconf_schema_uninstall apps_gnucash_dialog_scheduled_transctions.schemas

%postun
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_business_common.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_commodities.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_common.schemas
%{?with_hbci:%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_hbci.schemas}
%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_prices.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_print_checks.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_reconcile.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_totd.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_general.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_history.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_import_generic_matcher.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_import_qif.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_warnings.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_window_pages_account_tree.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_window_pages_register.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_scheduled_transctions.schemas
%dir %{_sysconfdir}/gnucash
%{_sysconfdir}/gnucash/config
%attr(755,root,root) %{_bindir}/gnc-fq-check
%attr(755,root,root) %{_bindir}/gnc-fq-dump
%attr(755,root,root) %{_bindir}/gnc-fq-helper
%attr(755,root,root) %{_bindir}/gnc-fq-update
%attr(755,root,root) %{_bindir}/gnc-test-env
%attr(755,root,root) %{_bindir}/gnucash
%attr(755,root,root) %{_bindir}/gnucash-bin
%attr(755,root,root) %{_bindir}/gnucash-env
%attr(755,root,root) %{_bindir}/gnucash-make-guids
%attr(755,root,root) %{_bindir}/gnucash-valgrind
%attr(755,root,root) %{_bindir}/update-gnucash-gconf
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
%lang(de) %{_datadir}/%{name}/accounts/de_DE
%lang(el) %{_datadir}/%{name}/accounts/el_GR
%lang(en_GB) %{_datadir}/%{name}/accounts/en_GB
%lang(es) %{_datadir}/%{name}/accounts/es_ES
%lang(es_MX) %{_datadir}/%{name}/accounts/es_MX
%lang(fi_FI) %{_datadir}/%{name}/accounts/fi_FI
%lang(fr_CA) %{_datadir}/%{name}/accounts/fr_CA
%lang(fr_CH) %{_datadir}/%{name}/accounts/fr_CH
%lang(fr) %{_datadir}/%{name}/accounts/fr_FR
%lang(hu) %{_datadir}/%{name}/accounts/hu_HU
%lang(it) %{_datadir}/%{name}/accounts/it
%lang(ja) %{_datadir}/%{name}/accounts/ja
%lang(nb) %{_datadir}/%{name}/accounts/nb
%lang(nl) %{_datadir}/%{name}/accounts/nl
%lang(pt_BR) %{_datadir}/%{name}/accounts/pt_BR
%lang(pt) %{_datadir}/%{name}/accounts/pt_PT
%lang(ru) %{_datadir}/%{name}/accounts/ru
%lang(sk) %{_datadir}/%{name}/accounts/sk
%lang(tr) %{_datadir}/%{name}/accounts/tr_TR
%lang(zh_CN) %{_datadir}/%{name}/accounts/zh_CN
%dir %{_datadir}/%{name}/checks
%{_datadir}/%{name}/checks/*.chk
%dir %{_datadir}/%{name}/doc
%{_datadir}/%{name}/doc/AUTHORS
%{_datadir}/%{name}/doc/COPYING
%{_datadir}/%{name}/doc/ChangeLog
%{_datadir}/%{name}/doc/ChangeLog.2003
%{_datadir}/%{name}/doc/ChangeLog.2004
%{_datadir}/%{name}/doc/ChangeLog.2005
%{_datadir}/%{name}/doc/ChangeLog.2006
%{_datadir}/%{name}/doc/ChangeLog.2007
%{_datadir}/%{name}/doc/DOCUMENTERS
%{_datadir}/%{name}/doc/HACKING
%{_datadir}/%{name}/doc/INSTALL
%{_datadir}/%{name}/doc/LICENSE
%{_datadir}/%{name}/doc/NEWS
%{_datadir}/%{name}/doc/README
%{_datadir}/%{name}/doc/README.francais
%{_datadir}/%{name}/doc/README.german
%{_datadir}/%{name}/doc/README.patches
%{_datadir}/%{name}/doc/README.dependencies
%{_datadir}/%{name}/doc/guile-hackers.txt
%{_datadir}/%{name}/doc/projects.html
%dir %{_datadir}/%{name}/doc/examples
%{_datadir}/%{name}/doc/examples/Money95bank_fr.qif
%{_datadir}/%{name}/doc/examples/Money95invst_fr.qif
%{_datadir}/%{name}/doc/examples/Money95mfunds_fr.qif
%{_datadir}/%{name}/doc/examples/Money95stocks_fr.qif
%{_datadir}/%{name}/doc/examples/README
%{_datadir}/%{name}/doc/examples/abc-all.qif
%{_datadir}/%{name}/doc/examples/abc.qif
%{_datadir}/%{name}/doc/examples/bogus.qif
%{_datadir}/%{name}/doc/examples/cbb-export.qif
%{_datadir}/%{name}/doc/examples/currency.xac
%{_datadir}/%{name}/doc/examples/currency_tree_xml.xac
%{_datadir}/%{name}/doc/examples/every.qif
%{_datadir}/%{name}/doc/examples/ms-money.qif
%{_datadir}/%{name}/doc/examples/quicktest.qif
%{_datadir}/%{name}/doc/examples/splitdemo.xac
%{_datadir}/%{name}/doc/examples/swipe.qif
%{_datadir}/%{name}/doc/examples/taxreport.xac
%{_datadir}/%{name}/doc/examples/test.xac
%{_datadir}/%{name}/doc/examples/test2.xac
%{_datadir}/%{name}/doc/examples/test3.xac
%{_datadir}/%{name}/doc/examples/test4.xac
%{_datadir}/%{name}/doc/examples/trading.xac
%{_datadir}/%{name}/doc/examples/trading2.xac
%{_datadir}/%{name}/doc/examples/web.qif
%{_datadir}/%{name}/doc/examples/xfer.xac
%dir %{_datadir}/%{name}/glade
%{_datadir}/%{name}/glade/account.glade
%{_datadir}/%{name}/glade/acctperiod.glade
%{_datadir}/%{name}/glade/billterms.glade
%{_datadir}/%{name}/glade/budget.glade
%{_datadir}/%{name}/glade/businessprefs.glade
%{_datadir}/%{name}/glade/chart-export.glade
%{_datadir}/%{name}/glade/choose-owner.glade
%{_datadir}/%{name}/glade/commodities.glade
%{_datadir}/%{name}/glade/commodity.glade
%{_datadir}/%{name}/glade/customer.glade
%{_datadir}/%{name}/glade/date-close.glade
%{_datadir}/%{name}/glade/dialog-book-close.glade
%{_datadir}/%{name}/glade/dialog-query-list.glade
%{_datadir}/%{name}/glade/dialog-reset-warnings.glade
%{_datadir}/%{name}/glade/druid-gconf-setup.glade
%{_datadir}/%{name}/glade/druid-gnc-xml-import.glade
%{_datadir}/%{name}/glade/druid-provider-multifile.glade
%{_datadir}/%{name}/glade/employee.glade
%{_datadir}/%{name}/glade/exchange-dialog.glade
%{_datadir}/%{name}/glade/fincalc.glade
%{_datadir}/%{name}/glade/generic-import.glade
%{_datadir}/%{name}/glade/gnc-date-format.glade
%{_datadir}/%{name}/glade/gnc-gui-query.glade
%if %{with hbci}
%{_datadir}/%{name}/glade/hbci.glade
%{_datadir}/%{name}/glade/hbcipass.glade
%{_datadir}/%{name}/glade/hbciprefs.glade
%endif
%{_datadir}/%{name}/glade/import-provider-format.glade
%{_datadir}/%{name}/glade/invoice.glade
%{_datadir}/%{name}/glade/job.glade
%{_datadir}/%{name}/glade/lots.glade
%{_datadir}/%{name}/glade/merge.glade
%{_datadir}/%{name}/glade/newuser.glade
%{_datadir}/%{name}/glade/order.glade
%{_datadir}/%{name}/glade/payment.glade
%{_datadir}/%{name}/glade/preferences.glade
%{_datadir}/%{name}/glade/price.glade
%{_datadir}/%{name}/glade/print.glade
%{_datadir}/%{name}/glade/progress.glade
%{_datadir}/%{name}/glade/qif.glade
%{_datadir}/%{name}/glade/reconcile.glade
%{_datadir}/%{name}/glade/register.glade
%{_datadir}/%{name}/glade/report.glade
%{_datadir}/%{name}/glade/sched-xact.glade
%{_datadir}/%{name}/glade/search.glade
%{_datadir}/%{name}/glade/stocks.glade
%{_datadir}/%{name}/glade/tax-tables.glade
%{_datadir}/%{name}/glade/tax.glade
%{_datadir}/%{name}/glade/totd.glade
%{_datadir}/%{name}/glade/transfer.glade
%{_datadir}/%{name}/glade/userpass.glade
%{_datadir}/%{name}/glade/vendor.glade
%{_datadir}/%{name}/gnome
%dir %{_datadir}/%{name}/guile-modules
%dir %{_datadir}/%{name}/guile-modules/gnucash
%{_datadir}/%{name}/guile-modules/gnucash/app-utils.scm
%{_datadir}/%{name}/guile-modules/gnucash/business-core.scm
%{_datadir}/%{name}/guile-modules/gnucash/business-gnome.scm
%{_datadir}/%{name}/guile-modules/gnucash/business-utils.scm
%{_datadir}/%{name}/guile-modules/gnucash/core-utils.scm
%{_datadir}/%{name}/guile-modules/gnucash/dialog-tax-table.scm
%{_datadir}/%{name}/guile-modules/gnucash/engine.scm
%{_datadir}/%{name}/guile-modules/gnucash/gnc-module.scm
%{_datadir}/%{name}/guile-modules/gnucash/gnome-utils.scm
%dir %{_datadir}/%{name}/guile-modules/gnucash/import-export
%{_datadir}/%{name}/guile-modules/gnucash/import-export/qif-import.scm
%{_datadir}/%{name}/guile-modules/gnucash/main.scm
%{_datadir}/%{name}/guile-modules/gnucash/price-quotes.scm
%dir %{_datadir}/%{name}/guile-modules/gnucash/report
%{_datadir}/%{name}/guile-modules/gnucash/report/account-piecharts.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/account-summary.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/advanced-portfolio.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/aging.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/average-balance.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/balance-sheet.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/budget.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/business-reports.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/cash-flow.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/category-barchart.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/daily-reports.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/easy-invoice.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/equity-statement.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/fancy-invoice.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/general-journal.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/general-ledger.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/hello-world.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/income-statement.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/invoice.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/locale-specific/de_DE.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/locale-specific/us.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/net-barchart.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/owner-report.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/payables.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/portfolio.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/price-scatter.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/receivables.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/register.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/report-gnome.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/report-system.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/stylesheet-easy.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/stylesheet-fancy.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/stylesheet-plain.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/stylesheets.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/taxtxf-de_DE.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/taxtxf.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/transaction.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/trial-balance.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/utility-reports.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/view-column.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/welcome-to-gnucash.scm
%dir %{_datadir}/%{name}/guile-modules/gnucash/report/locale-specific
%dir %{_datadir}/%{name}/guile-modules/gnucash/tax
%{_datadir}/%{name}/guile-modules/gnucash/tax/de_DE.scm
%{_datadir}/%{name}/guile-modules/gnucash/tax/us.scm
%{_datadir}/%{name}/pixmaps
%dir %{_datadir}/%{name}/scm
%{_datadir}/%{name}/scm/build-config.scm
%{_datadir}/%{name}/scm/business-options.scm
%{_datadir}/%{name}/scm/business-prefs.scm
%{_datadir}/%{name}/scm/c-interface.scm
%{_datadir}/%{name}/scm/command-line.scm
%{_datadir}/%{name}/scm/commodity-table.scm
%{_datadir}/%{name}/scm/commodity-utilities.scm
%{_datadir}/%{name}/scm/config-var.scm
%{_datadir}/%{name}/scm/date-utilities.scm
%{_datadir}/%{name}/scm/doc.scm
%{_datadir}/%{name}/scm/engine-interface.scm
%{_datadir}/%{name}/scm/engine-utilities.scm
%{_datadir}/%{name}/scm/fin.scm
%{_datadir}/%{name}/scm/gnc-menu-extensions.scm
%{_datadir}/%{name}/scm/gnc-numeric.scm
%dir %{_datadir}/%{name}/scm/gnumeric
%{_datadir}/%{name}/scm/gnumeric/gnumeric-utilities.scm
%{_datadir}/%{name}/scm/gnumeric/table-utils.scm
%{_datadir}/%{name}/scm/hooks.scm
%{_datadir}/%{name}/scm/html-acct-table.scm
%{_datadir}/%{name}/scm/html-barchart.scm
%{_datadir}/%{name}/scm/html-document.scm
%{_datadir}/%{name}/scm/html-piechart.scm
%{_datadir}/%{name}/scm/html-scatter.scm
%{_datadir}/%{name}/scm/html-style-info.scm
%{_datadir}/%{name}/scm/html-style-sheet.scm
%{_datadir}/%{name}/scm/html-table.scm
%{_datadir}/%{name}/scm/html-text.scm
%{_datadir}/%{name}/scm/html-utilities.scm
%{_datadir}/%{name}/scm/main-window.scm
%{_datadir}/%{name}/scm/options-utilities.scm
%{_datadir}/%{name}/scm/options.scm
%{_datadir}/%{name}/scm/prefs.scm
%dir %{_datadir}/%{name}/scm/qif-import
%{_datadir}/%{name}/scm/qif-import/qif-dialog-utils.scm
%{_datadir}/%{name}/scm/qif-import/qif-file.scm
%{_datadir}/%{name}/scm/qif-import/qif-guess-map.scm
%{_datadir}/%{name}/scm/qif-import/qif-import.scm
%{_datadir}/%{name}/scm/qif-import/qif-merge-groups.scm
%{_datadir}/%{name}/scm/qif-import/qif-objects.scm
%{_datadir}/%{name}/scm/qif-import/qif-parse.scm
%{_datadir}/%{name}/scm/qif-import/qif-to-gnc.scm
%{_datadir}/%{name}/scm/qif-import/qif-utils.scm
%{_datadir}/%{name}/scm/report-utilities.scm
%{_datadir}/%{name}/scm/report.scm
%{_datadir}/%{name}/scm/simple-obj.scm
%{_datadir}/%{name}/scm/string.scm
%{_datadir}/%{name}/scm/substring-search.scm
%{_datadir}/%{name}/scm/txf-de_DE.scm
%{_datadir}/%{name}/scm/txf-help-de_DE.scm
%{_datadir}/%{name}/scm/txf-help.scm
%{_datadir}/%{name}/scm/txf.scm
%{_datadir}/%{name}/scm/xml-generator.scm
%{_datadir}/%{name}/tip_of_the_day.list
%{_datadir}/%{name}/ui
%dir %{_datadir}/%{name}/xml
%dir %{_datadir}/%{name}/xml/qsf
%{_datadir}/%{name}/xml/qsf/pilot-qsf-GnuCashInvoice.xml
%{_datadir}/%{name}/xml/qsf/pilot-qsf-gncCustomer.xml
%{_datadir}/%{name}/xml/qsf/qsf-map.xsd.xml
%{_datadir}/%{name}/xml/qsf/qsf-object.xsd.xml
%{_infodir}/gnucash-design.info*
%{_mandir}/man1/gnc-prices.1*
%{_mandir}/man1/gnucash.1*
%{_pixmapsdir}/*
%dir %{_datadir}/xml/%{name}
%dir %{_datadir}/xml/%{name}/xsl
%{_datadir}/xml/%{name}/xsl/README
%{_datadir}/xml/%{name}/xsl/date-time.xsl
%{_datadir}/xml/%{name}/xsl/gnucash-gnccustomer-vcard2.xsl
%{_datadir}/xml/%{name}/xsl/gnucash-std.xsl
%{_datadir}/xml/%{name}/xsl/string.xsl
%{_datadir}/xml/%{name}/xsl/vcard-gnccustomer.pl
%{_iconsdir}/hicolor/*/apps/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib*.la
%{_includedir}/%{name}
