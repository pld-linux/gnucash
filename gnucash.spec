# TODO:
# - make separate subpackages with ofx, hbci, sql (like in included spec)
%include	/usr/lib/rpm/macros.perl
Summary:	GnuCash is an application to keep track of your finances
Summary(ja):	GnuCash - ²È·×Êí¥½¥Õ¥È
Summary(pl):	GnuCash - aplikacja do zarz±dzania twoimi finansami
Summary(pt_BR):	O GnuCash é uma aplicação para acompanhamento de suas finanças
Summary(zh_CN):	GnuCash - ÄúµÄ¸öÈË²ÆÎñ¹ÜÀíÈí¼þ
Name:		gnucash
Version:	1.8.12
Release:	6
License:	GPL v2
Group:		X11/Applications
Source0:	http://www.gnucash.org/pub/gnucash/sources/stable/%{name}-%{version}.tar.gz
# Source0-md5:	81e7c703db56bb203e106664157779cc
Source1:	%{name}-icon.png
Patch0:		%{name}-info.patch
Patch1:		%{name}-types.patch
Patch2:		%{name}-ghttp-ssl.patch
Patch3:		%{name}-build-fix.patch
URL:		http://www.gnucash.org/
BuildRequires:	GConf-devel
BuildRequires:	Guppi-devel >= 0.35.5
BuildRequires:	aqbanking-devel >= 1.0.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bonobo-devel
BuildRequires:	db-devel
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	g-wrap-devel >= 1.3.4
BuildRequires:	gal1-devel
BuildRequires:	gdk-pixbuf-gnome-devel >= 0.2.5
BuildRequires:	gettext-devel
BuildRequires:	gnome-libs-devel
BuildRequires:	gnome-print-devel >= 0.21
BuildRequires:	gtk+-devel
BuildRequires:	gtkhtml1-devel >= 1.1
BuildRequires:	guile-devel >= 1.3.4
BuildRequires:	ktoblzcheck-devel
BuildRequires:	libghttp-devel >= 1:1.0.9-10
BuildRequires:	libglade-gnome-devel
BuildRequires:	libltdl-devel
BuildRequires:	libofx-devel >= 0.7.0
BuildRequires:	libtool
BuildRequires:	libxml-devel
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	postgresql-devel
BuildRequires:	sed >= 4.0
BuildRequires:	slib >= 2c4
BuildRequires:	texinfo
Requires(post,preun):	/sbin/ldconfig
Requires:	gnome-print >= 0.21
Requires:	guile >= 1.3.4
Requires:	libghttp >= 1:1.0.9-10
Requires:	perl
Requires:	slib >= 2c4
Conflicts:	applnk < 1.9.5-20
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# force regeneration after patching types in table.m4
rm -f src/backend/postgres/base-autogen.c

# kill outdated libtool macros
tail -n +3907 acinclude.m4 > acinclude.tmp
mv -f acinclude.tmp acinclude.m4

sed -i -e 's/Terminal=0/Terminal=false/' src/gnome/gnucash.desktop.in
cat >> src/gnome/gnucash.desktop.in <<EOF
Encoding=UTF-8
Categories=GTK;GNOME;Office;Finance;
EOF

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I %{_aclocaldir}/gnome -I macros
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	--disable-prefer-db1 \
	--enable-hbci \
	--enable-ofx \
	--enable-sql

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	gnomeappdir=%{_desktopdir}

sed -i -e 's/=gnome-money.png/=gnucash-icon.png/' \
	$RPM_BUILD_ROOT%{_desktopdir}/gnucash.desktop

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
%doc AUTHORS ChangeLog* HACKING NEWS README* TODO
%doc doc/*.txt doc/examples doc/README* doc/RAW-NOTES doc/*HOWTO
%attr(755,root,root) %{_bindir}/*
# libs
%attr(755,root,root) %{_libdir}/libcore-utils.so.*.*.*
%attr(755,root,root) %{_libdir}/libgnc-app-file-gnome.so.*.*.*
%attr(755,root,root) %{_libdir}/libgncgnome.so.*.*.*
# lt_dlopened modules
%attr(755,root,root) %{_libdir}/libgncmodule.so.*.*.*
%attr(755,root,root) %{_libdir}/libgncmodule.so
%{_libdir}/libgncmodule.la
%attr(755,root,root) %{_libdir}/libgw-core-utils.so.*.*.*
%attr(755,root,root) %{_libdir}/libgw-core-utils.so
%{_libdir}/libgw-core-utils.la
%attr(755,root,root) %{_libdir}/libgw-gnc.so.*.*.*
%attr(755,root,root) %{_libdir}/libgw-gnc.so
%{_libdir}/libgw-gnc.la
%dir %{_libdir}/%{name}
# lt_dlopened modules - need *.la
%attr(755,root,root) %{_libdir}/%{name}/libgnc*.so*
%attr(755,root,root) %{_libdir}/%{name}/libgw-*.so*
%{_libdir}/%{name}/libgnc*.la
%{_libdir}/%{name}/libgw-*.la
%dir %{_libdir}/%{name}/overrides
%attr(755,root,root) %{_libdir}/%{name}/overrides/*
%{_sysconfdir}/gnucash
%dir %{_datadir}/gnucash
%{_datadir}/gnucash/[!af]*
%dir %{_datadir}/gnucash/accounts
%{_datadir}/gnucash/accounts/C
%lang(da) %{_datadir}/gnucash/accounts/da
%lang(de_CH) %{_datadir}/gnucash/accounts/de_CH
%lang(de_DE) %{_datadir}/gnucash/accounts/de_DE
%lang(es_ES) %{_datadir}/gnucash/accounts/es_ES
%lang(el_GR) %{_datadir}/gnucash/accounts/el_GR
%lang(fr_FR) %{_datadir}/gnucash/accounts/fr_FR
%lang(hu_HU) %{_datadir}/gnucash/accounts/hu_HU
%lang(it) %{_datadir}/gnucash/accounts/it
%lang(pt_BR) %{_datadir}/gnucash/accounts/pt_BR
%lang(pt_PT) %{_datadir}/gnucash/accounts/pt_PT
%lang(sk) %{_datadir}/gnucash/accounts/sk
%lang(tr_TR) %{_datadir}/gnucash/accounts/tr_TR
%attr(755,root,root) %{_datadir}/gnucash/f*
%{_datadir}/mime-info/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/%{name}
%{_pixmapsdir}/%{name}-icon.png
%{_mandir}/man1/*.1*
%{_infodir}/*.info*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcore-utils.so
%attr(755,root,root) %{_libdir}/libgnc-app-file-gnome.so
%attr(755,root,root) %{_libdir}/libgncgnome.so
%{_libdir}/libcore-utils.la
%{_libdir}/libgnc-app-file-gnome.la
%{_libdir}/libgncgnome.la
%{_includedir}/gnucash
%{_aclocaldir}/gnucash.m4
