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
Summary:	GnuCash is an application to keep track of your finances
Summary(ja.UTF-8):	GnuCash - 家計簿ソフト
Summary(pl.UTF-8):	GnuCash - aplikacja do zarządzania twoimi finansami
Summary(pt_BR.UTF-8):	O GnuCash é uma aplicação para acompanhamento de suas finanças
Summary(zh_CN.UTF-8):	GnuCash - 您的个人财务管理软件
Name:		gnucash
Version:	3.11
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	https://sourceforge.net/projects/gnucash/files/gnucash%20%28stable%29/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	391f07eb0934618154d9e9c7d717d8e6
Source1:	%{name}-icon.png
Source2:	%{name}.sh
Patch0:		lto.patch
URL:		http://www.gnucash.org/
BuildRequires:	GConf2-devel >= 2.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-tools
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
Requires:	dconf
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

%build
install -d build
cd build

#CFLAGS="$CFLAGS -DGLIB_DISABLE_DEPRECATION_WARNINGS" \
%cmake \
  -DCMAKE_INSTALL_DOCDIR:PATH=%{_docdir}/%{name} \
  ../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pixmapsdir}

cd build
%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT \
	gnomeappdir=%{_desktopdir}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}

cd ..

rm -rf $RPM_BUILD_ROOT/usr/share/locale/{kok@latin,mni@bengali}
rm $RPM_BUILD_ROOT/%{_datadir}/glib-2.0/schemas/gschemas.compiled

%find_lang %{name}
# --with-gnome

listfiles() {
  echo "%%defattr(644,root,root,755)" > "$1.files"
  find "${RPM_BUILD_ROOT}$2" -name "$3" -printf '%%h\n' | sort | uniq | \
  awk -v "pref=${RPM_BUILD_ROOT}$2/" \
  '$0 ~ pref {sub(pref,"",$1); n=split($1,A,"/"); s=""; for (i=1;i<=n;i++) { s=s "/" A[i]; B[s]=1;};} 
   END {for (i in B) print i}' | \
  sort | while read d
  do
    echo "%%dir $2$d" >> "$1.files"
  done
  for f in `find "${RPM_BUILD_ROOT}$2" -name "$3" -printf '%%P '`; do
    echo "$2/$f" >> "$1.files"
  done
  cd "$oldd"
  unset oldd
}

listfiles scm "%{_datadir}/%{name}/scm" "*.scm"
listfiles scmcache "%{_libdir}/%{name}/scm/ccache" "*.go"
listfiles icons "%{_datadir}/%{name}/icons" "*.png"

cat scm.files scmcache.files icons.files >> %{name}.lang

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
%{_sysconfdir}/gnucash/environment
%attr(755,root,root) %{_bindir}/gnc-fq-check
%attr(755,root,root) %{_bindir}/gnc-fq-dump
%attr(755,root,root) %{_bindir}/gnc-fq-helper
%attr(755,root,root) %{_bindir}/gnc-fq-update
%attr(755,root,root) %{_bindir}/gnucash
%attr(755,root,root) %{_bindir}/gnucash-valgrind
%attr(755,root,root) %{_libdir}/lib*.so
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so*
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
%{_datadir}/glib-2.0/schemas/org.gnucash.general.finance-quote.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.history.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.warnings.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.window.pages.account.tree.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnucash.window.pages.gschema.xml
%dir %{_datadir}/%{name}/icons
%dir %{_datadir}/%{name}/gtkbuilder
%{_datadir}/%{name}/gtkbuilder/*.glade
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
%{_datadir}/%{name}/tip_of_the_day.list
%{_datadir}/%{name}/ui
%{_datadir}/%{name}/make-prefs-migration-script.xsl
%{_datadir}/metainfo/gnucash.appdata.xml
%{_datadir}/%{name}/migratable-prefs.xml
%dir %{_datadir}/%{name}/scm
%{_datadir}/%{name}/scm/gnucash/report/*.css
%dir %{_libdir}/%{name}/scm
%dir %{_libdir}/%{name}/scm/ccache
%{_mandir}/man1/gnc-fq-dump.1*
%{_mandir}/man1/gnc-fq-helper.1*

%{_mandir}/man1/gnucash.1*
%{_pixmapsdir}/*
%{_iconsdir}/hicolor/*/apps/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
