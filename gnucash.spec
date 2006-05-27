# TODO:
# - make separate subpackages with ofx, hbci, sql (like in included spec)
%include	/usr/lib/rpm/macros.perl
Summary:	GnuCash is an application to keep track of your finances
Summary(ja):	GnuCash - ²È·×Êí¥½¥Õ¥È
Summary(pl):	GnuCash - aplikacja do zarz±dzania twoimi finansami
Summary(pt_BR):	O GnuCash é uma aplicação para acompanhamento de suas finanças
Summary(zh_CN):	GnuCash - ÄúµÄ¸öÈË²ÆÎñ¹ÜÀíÈí¼þ
Name:		gnucash
Version:	1.9.6
Release:	0.1
License:	GPL v2
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/gnucash/%{name}-%{version}.tar.gz
# Source0-md5:	ba5164c17c4c6550f8fa00b2d926c1ad
Source1:	%{name}-icon.png
URL:		http://www.gnucash.org/
BuildRequires:	GConf2-devel >= 2.0
BuildRequires:	aqbanking-devel >= 1.0.0
BuildRequires:	db-devel
BuildRequires:	g-wrap-devel >= 2:1.3.3
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

%description -l ja
GnuCash ¤Ï¸Ä¿Í¸þ¤±²ñ·×¥½¥Õ¥È¤Ç¤¹¡£GUI ¤òÍøÍÑ¤·¤Æ¼ýÆþ¡¦»Ù½Ð¡¦¶ä¹Ô¸ýºÂ¡¦
³ô¼°¤Ê¤É¤Î¼è¤ê°ú¤­¤òµ­Ä¢¤Ç¤­¤Þ¤¹¡£¥¤¥ó¥¿¡¼¥Õ¥§¡¼¥¹¤Ï¥·¥ó¥×¥ë¤Ë¡¢´ÊÃ±¤Ë
ÍøÍÑ¤Ç¤­¤ë¤è¤¦¤ËÀß·×¤·¤Æ¤¤¤Þ¤¹¤¬¡¢Àµ³Î¤µ¤òÄÉµÚ¤·¤Æ¤¤¤ë¤¿¤á¤ËÊ£¼°Êíµ­¤Î
²ñ·×µ¬½à¤òÍøÍÑ¤·¤Æ¤ª¤ê¡¢Ê£¼°Êíµ­¤Ë´Ø¤¹¤ëÃÎ¼±¤¬É¬Í×¤Ç¤¹¡£

%description -l pl
GnuCash jest programem do zarz±dzania finansami osobistymi. Pozwala na
¶ledzenie i wpisywanie zasobów na swoich kontach bankowych, zak³adów.
Daje wgl±d nawet w kursy walut. Interfejs zosta³ zaprojektowany z
my¶l± o prostocie i ³atwo¶ci u¿ycia.

%description -l pt_BR
O GnuCash é um gerenciador de finanças pessoais. Uma interface
parecida com um canhoto de cheques permite que você acompanhe contas
bancárias, ações, salário e mesmo tabelas de câmbio de moedas. A
interface foi projetada para ser simples e fácil de usar, mas tem o
suporte de princípios de contabilidade com entrada dupla para garantir
livros balanceados.

%package devel
Summary:	Header files for GnuCash libraries
Summary(pl):	Pliki nag³ówkowe bibliotek GnuCash
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for GnuCash libraries.

%description devel -l pl
Pliki nag³ówkowe bibliotek GnuCash.

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
install -d $RPM_BUILD_ROOT/%{_pixmapsdir}

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
%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_business_common.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_commodities.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_common.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_hbci.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_prices.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_print_checks.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_reconcile.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_dialog_totd.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_general.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_history.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_import_generic_matcher.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_warnings.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_window_pages_account_tree.schemas
%{_sysconfdir}/gconf/schemas/apps_gnucash_window_pages_register.schemas
%dir %{_sysconfdir}/gnucash
%{_sysconfdir}/gnucash/config
%attr(755,root,root) %{_bindir}/gnc-fq-check
%attr(755,root,root) %{_bindir}/gnc-fq-dump
%attr(755,root,root) %{_bindir}/gnc-fq-helper
%attr(755,root,root) %{_bindir}/gnc-fq-update
%attr(755,root,root) %{_bindir}/gnc-test-env
%attr(755,root,root) %{_bindir}/gnucash
%attr(755,root,root) %{_bindir}/gnucash-bin
%attr(755,root,root) %{_bindir}/gnucash-config
%attr(755,root,root) %{_bindir}/gnucash-env
%attr(755,root,root) %{_bindir}/gnucash-make-guids
%attr(755,root,root) %{_bindir}/gnucash-valgrind
%attr(755,root,root) %{_bindir}/update-gnucash-gconf
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so.*
%{_libdir}/%{name}/overrides
%{_aclocaldir}/gnucash.m4
%{_desktopdir}/gnucash.desktop
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/accounts
%{_datadir}/%{name}/accounts/C
%lang(da) %{_datadir}/%{name}/accounts/da
%lang(de_CH) %{_datadir}/%{name}/accounts/de_CH
%lang(de_DE) %{_datadir}/%{name}/accounts/de_DE
%lang(el_GR) %{_datadir}/%{name}/accounts/el_GR
%lang(es_ES) %{_datadir}/%{name}/accounts/es_ES
%lang(fr_FR) %{_datadir}/%{name}/accounts/fr_FR
%lang(hu_HU) %{_datadir}/%{name}/accounts/hu_HU
%lang(de_AT) %{_datadir}/%{name}/accounts/de_AT
%lang(fr_CH) %{_datadir}/%{name}/accounts/fr_CH
%lang(it) %{_datadir}/%{name}/accounts/it
%lang(nb) %{_datadir}/%{name}/accounts/nb
%lang(pt_BR) %{_datadir}/%{name}/accounts/pt_BR
%lang(pt_PT) %{_datadir}/%{name}/accounts/pt_PT
%lang(sk) %{_datadir}/%{name}/accounts/sk
%lang(tr_TR) %{_datadir}/%{name}/accounts/tr_TR
%dir %{_datadir}/%{name}/doc
%{_datadir}/%{name}/doc/AUTHORS
%{_datadir}/%{name}/doc/COPYING
%{_datadir}/%{name}/doc/ChangeLog
%{_datadir}/%{name}/doc/ChangeLog.2003
%{_datadir}/%{name}/doc/ChangeLog.2004
%{_datadir}/%{name}/doc/ChangeLog.2005
%{_datadir}/%{name}/doc/DOCUMENTERS
%{_datadir}/%{name}/doc/HACKING
%{_datadir}/%{name}/doc/INSTALL
%{_datadir}/%{name}/doc/LICENSE
%{_datadir}/%{name}/doc/NEWS
%{_datadir}/%{name}/doc/README
%{_datadir}/%{name}/doc/README.francais
%{_datadir}/%{name}/doc/README.german
%{_datadir}/%{name}/doc/README.patches
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
%dir %{_datadir}/%{name}/glade
%{_datadir}/%{name}/glade/account.glade
%{_datadir}/%{name}/glade/acctperiod.glade
%{_datadir}/%{name}/glade/billterms.glade
%{_datadir}/%{name}/glade/binary-import.glade
%{_datadir}/%{name}/glade/budget.glade
%{_datadir}/%{name}/glade/businessprefs.glade
%{_datadir}/%{name}/glade/chart-export.glade
%{_datadir}/%{name}/glade/choose-owner.glade
%{_datadir}/%{name}/glade/commodities.glade
%{_datadir}/%{name}/glade/commodity.glade
%{_datadir}/%{name}/glade/customer.glade
%{_datadir}/%{name}/glade/date-close.glade
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
%{_datadir}/%{name}/glade/hbci.glade
%{_datadir}/%{name}/glade/hbcipass.glade
%{_datadir}/%{name}/glade/hbciprefs.glade
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
%dir %{_datadir}/%{name}/guile-modules
%dir %{_datadir}/%{name}/guile-modules/g-wrapped
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-app-utils-spec.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-app-utils.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-business-core-spec.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-business-core.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-business-gnome-spec.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-business-gnome.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-core-utils-spec.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-core-utils.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-dialog-tax-table-spec.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-dialog-tax-table.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-engine-spec.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-engine.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-gnc-module-spec.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-gnc-module.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-gnc-spec.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-gnc.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-gnome-utils-spec.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-gnome-utils.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-kvp-spec.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-kvp.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-register-core-spec.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-register-core.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-report-gnome-spec.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-report-gnome.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-report-system-spec.scm
%{_datadir}/%{name}/guile-modules/g-wrapped/gw-report-system.scm
%dir %{_datadir}/%{name}/guile-modules/gnucash
%{_datadir}/%{name}/guile-modules/gnucash/app-utils.scm
%{_datadir}/%{name}/guile-modules/gnucash/business-core.scm
%{_datadir}/%{name}/guile-modules/gnucash/business-gnome.scm
%{_datadir}/%{name}/guile-modules/gnucash/business-utils.scm
%{_datadir}/%{name}/guile-modules/gnucash/dialog-tax-table.scm
%{_datadir}/%{name}/guile-modules/gnucash/engine.scm
%{_datadir}/%{name}/guile-modules/gnucash/gnc-module.scm
%{_datadir}/%{name}/guile-modules/gnucash/gnome-utils.scm
%dir %{_datadir}/%{name}/guile-modules/gnucash/import-export
%{_datadir}/%{name}/guile-modules/gnucash/import-export/qif-import.scm
%{_datadir}/%{name}/guile-modules/gnucash/main.scm
%{_datadir}/%{name}/guile-modules/gnucash/price-quotes.scm
%dir %{_datadir}/%{name}/guile-modules/gnucash/printing
%{_datadir}/%{name}/guile-modules/gnucash/printing/number-to-words.scm
%{_datadir}/%{name}/guile-modules/gnucash/process.scm
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
%{_datadir}/%{name}/guile-modules/gnucash/report/test-graphing.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/transaction.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/trial-balance.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/utility-reports.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/view-column.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/welcome-to-gnucash.scm
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
%{_datadir}/%{name}/scm/help-topics-index.scm
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
%{_datadir}/%{name}/scm/kvp-option-registry.scm
%{_datadir}/%{name}/scm/main-window.scm
%{_datadir}/%{name}/scm/options-utilities.scm
%{_datadir}/%{name}/scm/options.scm
%{_datadir}/%{name}/scm/prefs.scm
%dir %{_datadir}/%{name}/scm/printing
%{_datadir}/%{name}/scm/printing/print-check.scm
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
%{_datadir}/mime-info/gnucash.keys
%{_datadir}/mime-info/gnucash.mime
%{_pixmapsdir}/*
%dir %{_datadir}/xml/%{name}
%dir %{_datadir}/xml/%{name}/xsl
%{_datadir}/xml/%{name}/xsl/README
%{_datadir}/xml/%{name}/xsl/date-time.xsl
%{_datadir}/xml/%{name}/xsl/gnucash-gnccustomer-vcard2.xsl
%{_datadir}/xml/%{name}/xsl/gnucash-std.xsl
%{_datadir}/xml/%{name}/xsl/string.xsl
%{_datadir}/xml/%{name}/xsl/vcard-gnccustomer.pl

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/%{name}
