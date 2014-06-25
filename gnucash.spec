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
Version:	2.6.3
Release:	0.3
License:	GPL v2+
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/gnucash/%{name}-%{version}.tar.bz2
# Source0-md5:	c590a6549be3c1fbbb26b4426bea3ff5
Source1:	%{name}-icon.png
Source2:	%{name}.sh
Patch0:		%{name}-env.patch
Patch1:		%{name}-path.patch
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
BuildRequires:	gwenhywfar-gtk-devel
BuildRequires:	intltool
BuildRequires:	libglade2-devel >= 2.4
BuildRequires:	libgnome-devel >= 2.19.0
BuildRequires:	libgnomeprint-devel >= 2.2
BuildRequires:	libgnomeprintui-devel >= 2.2
BuildRequires:	libgnomeui-devel >= 2.4
BuildRequires:	libgoffice08-devel
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

%patch0 -p1
%patch1 -p1

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
	--enable-gtkmm \
	--disable-python-bindings

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pixmapsdir}

%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT \
	gnomeappdir=%{_desktopdir}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}
mv $RPM_BUILD_ROOT%{_bindir}/gnucash{,-bin}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/gnucash

## Cleanup
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la
%{__rm} $RPM_BUILD_ROOT%{_docdir}/%{name}/*win32-bin.txt

%find_lang %{name}
# --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
%glib_compile_schemas

%preun

%postun
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
if [ "$1" = "0" ]; then
        %glib_compile_schemas
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir %{_sysconfdir}/gnucash
%{_sysconfdir}/gnucash/config
%{_sysconfdir}/gnucash/environment
%attr(755,root,root) %{_bindir}/gnc-fq-check
%attr(755,root,root) %{_bindir}/gnc-fq-dump
%attr(755,root,root) %{_bindir}/gnc-fq-helper
%attr(755,root,root) %{_bindir}/gnc-fq-update
%attr(755,root,root) %{_bindir}/gnucash
%attr(755,root,root) %{_bindir}/gnucash-bin
%attr(755,root,root) %{_bindir}/gnucash-env
%attr(755,root,root) %{_bindir}/gnucash-make-guids
%attr(755,root,root) %{_bindir}/gnucash-valgrind
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so*
%dir %{_libdir}/%{name}/overrides
%attr(755,root,root) %{_libdir}/%{name}/overrides/gnucash-env
%attr(755,root,root) %{_libdir}/%{name}/overrides/gnucash-make-guids
%attr(755,root,root) %{_libdir}/%{name}/overrides/guile
%{_desktopdir}/gnucash.desktop
%{_datadir}//appdata/gnucash.appdata.xml
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
%lang(sv) %{_datadir}/%{name}/accounts/sv_SE
%lang(tr) %{_datadir}/%{name}/accounts/tr_TR
%lang(zh_CN) %{_datadir}/%{name}/accounts/zh_CN
%dir %{_datadir}/%{name}/checks
%{_datadir}/%{name}/checks/*.chk
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/AUTHORS
%{_docdir}/%{name}/COPYING
%{_docdir}/%{name}/ChangeLog
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
%{_docdir}/%{name}/DOCUMENTERS
%{_docdir}/%{name}/HACKING
%{_docdir}/%{name}/INSTALL
%{_docdir}/%{name}/LICENSE
%{_docdir}/%{name}/Money95bank_fr.qif
%{_docdir}/%{name}/Money95invst_fr.qif
%{_docdir}/%{name}/Money95mfunds_fr.qif
%{_docdir}/%{name}/Money95stocks_fr.qif
%{_docdir}/%{name}/NEWS
%{_docdir}/%{name}/README
%{_docdir}/%{name}/README.francais
%{_docdir}/%{name}/README.german
%{_docdir}/%{name}/README.dependencies
%{_docdir}/%{name}/README_invoice
%{_docdir}/%{name}/guile-hackers.txt
%{_docdir}/%{name}/projects.html
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
%{_datadir}/glib-2.0/schemas/org.gnucash.dialogs.business.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.dialogs.checkprinting.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.dialogs.commodities.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.dialogs.export.csv.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.dialogs.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.dialogs.import.csv.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.dialogs.import.generic.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.dialogs.import.hbci.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.dialogs.import.ofx.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.dialogs.import.qif.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.dialogs.reconcile.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.dialogs.sxs.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.dialogs.totd.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.history.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.warnings.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.window.pages.account.tree.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.window.pages.gschema.xml
%dir %{_datadir}/%{name}/gtkbuilder
%{_datadir}/%{name}/gtkbuilder/assistant-ab-initial.glade
%{_datadir}/%{name}/gtkbuilder/assistant-acct-period.glade
%{_datadir}/%{name}/gtkbuilder/assistant-csv-account-import.glade
%{_datadir}/%{name}/gtkbuilder/assistant-csv-export.glade
%{_datadir}/%{name}/gtkbuilder/assistant-csv-trans-import.glade
%{_datadir}/%{name}/gtkbuilder/assistant-hierarchy.glade
%{_datadir}/%{name}/gtkbuilder/assistant-loan.glade
%{_datadir}/%{name}/gtkbuilder/assistant-qif-import.glade
%{_datadir}/%{name}/gtkbuilder/assistant-stock-split.glade
%{_datadir}/%{name}/gtkbuilder/assistant-xml-encoding.glade
%{_datadir}/%{name}/gtkbuilder/business-options-gnome.glade
%{_datadir}/%{name}/gtkbuilder/business-prefs.glade
%{_datadir}/%{name}/gtkbuilder/dialog-ab.glade
%{_datadir}/%{name}/gtkbuilder/dialog-account-picker.glade
%{_datadir}/%{name}/gtkbuilder/dialog-account.glade
%{_datadir}/%{name}/gtkbuilder/dialog-bi-import-gui.glade
%{_datadir}/%{name}/gtkbuilder/dialog-billterms.glade
%{_datadir}/%{name}/gtkbuilder/dialog-book-close.glade
%{_datadir}/%{name}/gtkbuilder/dialog-choose-owner.glade
%{_datadir}/%{name}/gtkbuilder/dialog-commodities.glade
%{_datadir}/%{name}/gtkbuilder/dialog-commodity.glade
%{_datadir}/%{name}/gtkbuilder/dialog-custom-report.glade
%{_datadir}/%{name}/gtkbuilder/dialog-customer-import-gui.glade
%{_datadir}/%{name}/gtkbuilder/dialog-customer.glade
%{_datadir}/%{name}/gtkbuilder/dialog-date-close.glade
%{_datadir}/%{name}/gtkbuilder/dialog-employee.glade
%{_datadir}/%{name}/gtkbuilder/dialog-file-access.glade
%{_datadir}/%{name}/gtkbuilder/dialog-fincalc.glade
%{_datadir}/%{name}/gtkbuilder/dialog-import.glade
%{_datadir}/%{name}/gtkbuilder/dialog-invoice.glade
%{_datadir}/%{name}/gtkbuilder/dialog-job.glade
%{_datadir}/%{name}/gtkbuilder/dialog-lot-viewer.glade
%{_datadir}/%{name}/gtkbuilder/dialog-new-user.glade
%{_datadir}/%{name}/gtkbuilder/dialog-object-references.glade
%{_datadir}/%{name}/gtkbuilder/dialog-options.glade
%{_datadir}/%{name}/gtkbuilder/dialog-order.glade
%{_datadir}/%{name}/gtkbuilder/dialog-payment.glade
%{_datadir}/%{name}/gtkbuilder/dialog-preferences.glade
%{_datadir}/%{name}/gtkbuilder/dialog-price.glade
%{_datadir}/%{name}/gtkbuilder/dialog-print-check.glade
%{_datadir}/%{name}/gtkbuilder/dialog-progress.glade
%{_datadir}/%{name}/gtkbuilder/dialog-query-view.glade
%{_datadir}/%{name}/gtkbuilder/dialog-report.glade
%{_datadir}/%{name}/gtkbuilder/dialog-reset-warnings.glade
%{_datadir}/%{name}/gtkbuilder/dialog-search.glade
%{_datadir}/%{name}/gtkbuilder/dialog-sx.glade
%{_datadir}/%{name}/gtkbuilder/dialog-tax-info.glade
%{_datadir}/%{name}/gtkbuilder/dialog-tax-table.glade
%{_datadir}/%{name}/gtkbuilder/dialog-totd.glade
%{_datadir}/%{name}/gtkbuilder/dialog-transfer.glade
%{_datadir}/%{name}/gtkbuilder/dialog-userpass.glade
%{_datadir}/%{name}/gtkbuilder/dialog-vendor.glade
%{_datadir}/%{name}/gtkbuilder/gnc-date-format.glade
%{_datadir}/%{name}/gtkbuilder/gnc-frequency.glade
%{_datadir}/%{name}/gtkbuilder/gnc-plugin-page-budget.glade
%{_datadir}/%{name}/gtkbuilder/gnc-plugin-page-register.glade
%{_datadir}/%{name}/gtkbuilder/gnc-plugin-page-register2.glade
%{_datadir}/%{name}/gtkbuilder/gnc-recurrence.glade
%{_datadir}/%{name}/gtkbuilder/gnc-tree-view-owner.glade
%{_datadir}/%{name}/gtkbuilder/window-autoclear.glade
%{_datadir}/%{name}/gtkbuilder/window-reconcile.glade
%{_datadir}/%{name}/gnome
%dir %{_datadir}/%{name}/guile-modules
%dir %{_datadir}/%{name}/guile-modules/gnucash
%{_datadir}/%{name}/guile-modules/gnucash/app-utils.scm
%{_datadir}/%{name}/guile-modules/gnucash/business-core.scm
%{_datadir}/%{name}/guile-modules/gnucash/business-gnome.scm
%{_datadir}/%{name}/guile-modules/gnucash/core-utils.scm
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
%{_datadir}/%{name}/guile-modules/gnucash/report/balsheet-eg.scm
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
%dir %{_datadir}/%{name}/guile-modules/gnucash/report/report-system
%{_datadir}/%{name}/guile-modules/gnucash/report/report-system/collectors.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/report-system/list-extras.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/report-system/report-collectors.scm
%{_datadir}/%{name}/guile-modules/gnucash/report/standard-reports/net-linechart.scm
%{_datadir}/%{name}/guile-modules/gnucash/unittest-support.scm
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
%dir %{_datadir}/%{name}/jqplot/
%{_datadir}/%{name}/jqplot/jqplot.BezierCurveRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.barRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.blockRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.bubbleRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.canvasAxisLabelRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.canvasAxisTickRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.canvasTextRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.categoryAxisRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.ciParser.js
%{_datadir}/%{name}/jqplot/jqplot.cursor.js
%{_datadir}/%{name}/jqplot/jqplot.dateAxisRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.donutRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.dragable.js
%{_datadir}/%{name}/jqplot/jqplot.enhancedLegendRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.funnelRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.highlighter.js
%{_datadir}/%{name}/jqplot/jqplot.json2.js
%{_datadir}/%{name}/jqplot/jqplot.logAxisRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.mekkoAxisRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.mekkoRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.meterGaugeRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.ohlcRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.pieRenderer.js
%{_datadir}/%{name}/jqplot/jqplot.pointLabels.js
%{_datadir}/%{name}/jqplot/jqplot.trendline.js
%{_datadir}/%{name}/jqplot/jquery.jqplot.css
%{_datadir}/%{name}/jqplot/jquery.jqplot.js
%{_datadir}/%{name}/jqplot/jquery.min.js
%{_datadir}/%{name}/pixmaps
%dir %{_datadir}/%{name}/scm
%{_datadir}/%{name}/scm/build-config.scm
%{_datadir}/%{name}/scm/business-options.scm
%{_datadir}/%{name}/scm/business-prefs.scm
%{_datadir}/%{name}/scm/c-interface.scm
%{_datadir}/%{name}/scm/commodity-table.scm
%{_datadir}/%{name}/scm/commodity-utilities.scm
%{_datadir}/%{name}/scm/config-var.scm
%{_datadir}/%{name}/scm/date-utilities.scm
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
%{_datadir}/%{name}/make-prefs-migration-script.xsl
%{_datadir}/%{name}/migratable-prefs.xml
%{_datadir}/%{name}/scm/html-jqplot.scm
%{_datadir}/%{name}/scm/migrate-prefs.scm
%{_mandir}/man1/gnc-fq-dump.1*
%{_mandir}/man1/gnc-fq-helper.1*

%{_mandir}/man1/gnucash.1*
%{_pixmapsdir}/*
%{_iconsdir}/hicolor/*/apps/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib*.la
%{_includedir}/%{name}
