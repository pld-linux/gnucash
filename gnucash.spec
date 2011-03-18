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
%include	/usr/lib/rpm/macros.perl
Summary:	GnuCash is an application to keep track of your finances
Summary(ja.UTF-8):	GnuCash - 家計簿ソフト
Summary(pl.UTF-8):	GnuCash - aplikacja do zarządzania twoimi finansami
Summary(pt_BR.UTF-8):	O GnuCash é uma aplicação para acompanhamento de suas finanças
Summary(zh_CN.UTF-8):	GnuCash - 您的个人财务管理软件
Name:		gnucash
Version:	2.4.4
Release:	0.1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/gnucash/%{name}-%{version}.tar.bz2
# Source0-md5:	6ae973bf925cde0721c7c465536bc096
Source1:	%{name}-icon.png
URL:		http://www.gnucash.org/
BuildRequires:	GConf2-devel >= 2.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.13.0
BuildRequires:	gtk+2-devel >= 2:2.11.0
BuildRequires:	gtkhtml-devel >= 3.16
BuildRequires:	guile-devel >= 5:1.8.2-2
BuildRequires:	guile-www
BuildRequires:	intltool
BuildRequires:	libglade2-devel >= 2.4
BuildRequires:	libgnome-devel >= 2.19.0
BuildRequires:	libgnomeprint-devel >= 2.2
BuildRequires:	libgnomeprintui-devel >= 2.2
BuildRequires:	libgnomeui-devel >= 2.4
BuildRequires:	libgoffice-devel >= 0.6.0
BuildRequires:	libltdl-devel
BuildRequires:	libofx-devel >= 0.7.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.5.10
BuildRequires:	pango-devel >= 1.8.0
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= 1.5
BuildRequires:	readline-devel
BuildRequires:	rpm-perlprov
BuildRequires:	sed >= 4.0
BuildRequires:	slib >= 2c4
BuildRequires:	texinfo
BuildRequires:	zlib-devel
%if %{with dbi}
BuildRequires:	libdbi-devel
%endif
%if %{with hbci}
BuildRequires:	aqbanking-devel >= 3.8.1
BuildRequires:	gwenhywfar-devel >= 3.6.0
BuildRequires:	ktoblzcheck-devel >= 1.20
%endif
%if %{with webkit}
BuildRequires:	gtk-webkit-devel >= 1.0
%endif
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

%{__sed} -i -e 's/Categories=Application;Office/Categories=GTK;GNOME;Office/' src/gnome/gnucash.desktop.in
cat >> src/gnome/gnucash.desktop.in <<EOF
Encoding=UTF-8
EOF

%build
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-error-on-warning \
	%{?with_hbci:--enable-aqbanking} \
	%{!?with_hbci:--disable-aqbanking} \
	--enable-ofx \
	%{?with_dbi:--enable-dbi --with-dbi-dbd-dir=%{_libdir}/dbd} \
	%{!?with_dbi:--disable-dbi} \
	--with-html-engine=%{?with_webkit:webkit}%{!?with_webkit:gtkhtml} \
	--enable-locale-specific-tax \
	--enable-binreloc-threads \
	--enable-binreloc \
	--disable-python-bindings

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pixmapsdir}

%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT \
	gnomeappdir=%{_desktopdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}

## Cleanup
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la
#%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.so.[0-9]
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/doc/*win32-bin.txt

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
%{_sysconfdir}/gnucash/environment
%attr(755,root,root) %{_bindir}/gnc-fq-check
%attr(755,root,root) %{_bindir}/gnc-fq-dump
%attr(755,root,root) %{_bindir}/gnc-fq-helper
%attr(755,root,root) %{_bindir}/gnc-fq-update
%attr(755,root,root) %{_bindir}/gnc-test-env
%attr(755,root,root) %{_bindir}/gnucash
#%%attr(755,root,root) %{_bindir}/gnucash-bin
%attr(755,root,root) %{_bindir}/gnucash-env
#%%attr(755,root,root) %{_bindir}/gnucash-gdb
%attr(755,root,root) %{_bindir}/gnucash-make-guids
#%%attr(755,root,root) %{_bindir}/gnucash-setup-env
%attr(755,root,root) %{_bindir}/gnucash-valgrind
%attr(755,root,root) %{_bindir}/update-gnucash-gconf
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so*
%{_libdir}/%{name}/overrides
%{_desktopdir}/gnucash.desktop
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/accounts
%{_datadir}/%{name}/accounts/C
%lang(cs) %{_datadir}/%{name}/accounts/cs
%lang(da) %{_datadir}/%{name}/accounts/da
%lang(de) %{_datadir}/%{name}/accounts/de_DE
%lang(de_AT) %{_datadir}/%{name}/accounts/de_AT
%lang(de_CH) %{_datadir}/%{name}/accounts/de_CH
%lang(el) %{_datadir}/%{name}/accounts/el_GR
%lang(en_GB) %{_datadir}/%{name}/accounts/en_GB
%lang(es) %{_datadir}/%{name}/accounts/es_ES
%lang(es_MX) %{_datadir}/%{name}/accounts/es_MX
%lang(fi_FI) %{_datadir}/%{name}/accounts/fi_FI
%lang(fr) %{_datadir}/%{name}/accounts/fr_FR
%lang(fr_CA) %{_datadir}/%{name}/accounts/fr_CA
%lang(fr_CH) %{_datadir}/%{name}/accounts/fr_CH
%lang(hu) %{_datadir}/%{name}/accounts/hu_HU
%lang(it) %{_datadir}/%{name}/accounts/it
%lang(ja) %{_datadir}/%{name}/accounts/ja
%lang(ko) %{_datadir}/%{name}/accounts/ko
%lang(lv) %{_datadir}/%{name}/accounts/lv
%lang(nb) %{_datadir}/%{name}/accounts/nb
%lang(nl) %{_datadir}/%{name}/accounts/nl
%lang(pl) %{_datadir}/%{name}/accounts/pl
%lang(pt) %{_datadir}/%{name}/accounts/pt_PT
%lang(pt_BR) %{_datadir}/%{name}/accounts/pt_BR
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
%{_datadir}/%{name}/doc/ChangeLog.2008
%{_datadir}/%{name}/doc/ChangeLog.2009
%{_datadir}/%{name}/doc/DOCUMENTERS
%{_datadir}/%{name}/doc/HACKING
%{_datadir}/%{name}/doc/INSTALL
%{_datadir}/%{name}/doc/LICENSE
%{_datadir}/%{name}/doc/NEWS
%{_datadir}/%{name}/doc/README
%{_datadir}/%{name}/doc/README.francais
%{_datadir}/%{name}/doc/README.german
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
%{_datadir}/%{name}/doc/examples/currency_tree_xml.gnucash
%{_datadir}/%{name}/doc/examples/every.qif
%{_datadir}/%{name}/doc/examples/ms-money.qif
%{_datadir}/%{name}/doc/examples/quicktest.qif
%{_datadir}/%{name}/doc/examples/swipe.qif
%{_datadir}/%{name}/doc/examples/taxreport.gnucash
%{_datadir}/%{name}/doc/examples/web.qif
%dir %{_datadir}/%{name}/glade
%{_datadir}/%{name}/glade/account.glade
%{_datadir}/%{name}/glade/acctperiod.glade
%{_datadir}/%{name}/glade/autoclear.glade
%{_datadir}/%{name}/glade/bi_import.glade
%{_datadir}/%{name}/glade/billterms.glade
%{_datadir}/%{name}/glade/budget.glade
%{_datadir}/%{name}/glade/businessprefs.glade
%{_datadir}/%{name}/glade/choose-owner.glade
%{_datadir}/%{name}/glade/commodities.glade
%{_datadir}/%{name}/glade/commodity.glade
%{_datadir}/%{name}/glade/custom-report-dialog.glade
%{_datadir}/%{name}/glade/customer.glade
%{_datadir}/%{name}/glade/date-close.glade
%{_datadir}/%{name}/glade/dialog-book-close.glade
%{_datadir}/%{name}/glade/dialog-file-access.glade
%{_datadir}/%{name}/glade/dialog-object-references.glade
%{_datadir}/%{name}/glade/dialog-query-list.glade
%{_datadir}/%{name}/glade/dialog-reset-warnings.glade
%{_datadir}/%{name}/glade/druid-gconf-setup.glade
%{_datadir}/%{name}/glade/druid-gnc-xml-import.glade
%{_datadir}/%{name}/glade/druid-provider-multifile.glade
%{_datadir}/%{name}/glade/employee.glade
%{_datadir}/%{name}/glade/exchange-dialog.glade
%{_datadir}/%{name}/glade/fincalc.glade
%{_datadir}/%{name}/glade/generic-import.glade
%{_datadir}/%{name}/glade/gnc-csv-preview-dialog.glade
%{_datadir}/%{name}/glade/gnc-date-format.glade
%{_datadir}/%{name}/glade/gnc-gui-query.glade
%{_datadir}/%{name}/glade/import-provider-format.glade
%{_datadir}/%{name}/glade/invoice.glade
%{_datadir}/%{name}/glade/job.glade
%{_datadir}/%{name}/glade/lots.glade
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
%if %{with hbci}
%{_datadir}/%{name}/glade/aqbanking.glade
%endif
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
%{_datadir}/%{name}/guile-modules/gnucash/printf.scm
%dir %{_datadir}/%{name}/guile-modules/gnucash/report
%{_datadir}/%{name}/guile-modules/gnucash/report/aging.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/balsheet-eg.css
%{_datadir}/%{name}/guile-modules/gnucash/report/balsheet-eg.eguile.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/business-reports.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/customer-summary.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/easy-invoice.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/eguile-gnc.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/eguile-html-utilities.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/eguile-utilities.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/fancy-invoice.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/hello-world.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/invoice.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/job-report.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/locale-specific/de_DE.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/locale-specific/us.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/owner-report.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/payables.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/receivables.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/report-gnome.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/report-system.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/stylesheet-easy.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/stylesheet-fancy.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/stylesheet-footer.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/stylesheet-plain.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/stylesheets.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/taxinvoice.css
%{_datadir}/%{name}/guile-modules/gnucash/report/taxinvoice.eguile.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/taxinvoice.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/taxtxf-de_DE.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/taxtxf.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/utility-reports.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/view-column.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/welcome-to-gnucash.scm
%dir %{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/account-piecharts.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/account-summary.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/advanced-portfolio.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/average-balance.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/balance-sheet.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/balsheet-eg.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/budget-balance-sheet.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/budget-barchart.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/budget-flow.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/budget-income-statement.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/budget.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/cash-flow.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/category-barchart.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/daily-reports.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/equity-statement.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/general-journal.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/general-ledger.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/income-statement.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/net-barchart.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/portfolio.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/price-scatter.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/register.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/sx-summary.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/transaction.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/trial-balance.scm
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
%{_datadir}/%{name}/scm/html-fonts.scm
%{_datadir}/%{name}/scm/html-linechart.scm
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
%if 0
%dir %{_datadir}/%{name}/xml
%dir %{_datadir}/%{name}/xml/qsf
%{_datadir}/%{name}/xml/qsf/pilot-qsf-GnuCashInvoice.xml
%{_datadir}/%{name}/xml/qsf/pilot-qsf-gncCustomer.xml
%{_datadir}/%{name}/xml/qsf/qsf-map.xsd.xml
%{_datadir}/%{name}/xml/qsf/qsf-object.xsd.xml
%endif
%{_infodir}/gnucash-design.info*
#%%{_mandir}/man1/gnc-prices.1*
%{_mandir}/man1/gnucash.1*
%{_pixmapsdir}/*
%if 0
%dir %{_datadir}/xml/%{name}
%dir %{_datadir}/xml/%{name}/xsl
%{_datadir}/xml/%{name}/xsl/README
%{_datadir}/xml/%{name}/xsl/date-time.xsl
%{_datadir}/xml/%{name}/xsl/gnucash-gnccustomer-vcard2.xsl
%{_datadir}/xml/%{name}/xsl/gnucash-std.xsl
%{_datadir}/xml/%{name}/xsl/string.xsl
%{_datadir}/xml/%{name}/xsl/vcard-gnccustomer.pl
%endif
%{_iconsdir}/hicolor/*/apps/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib*.la
%{_includedir}/%{name}
