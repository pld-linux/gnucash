# TODO:
# - make separate subpackages with ofx and ohbci (like in included spec)
%include	/usr/lib/rpm/macros.perl
Summary:	GnuCash is an application to keep track of your finances
Summary(ja):	GnuCash - ²È·×Êí¥½¥Õ¥È
Summary(pl):	GnuCash - aplikacja do zarz±dzania twoimi finansami
Summary(pt_BR):	O GnuCash é uma aplicação para acompanhamento de suas finanças
Summary(zh_CN):	GnuCash - ÄúµÄ¸öÈË²ÆÎñ¹ÜÀíÈí¼þ
Name:		gnucash
Version:	1.8.9
Release:	0.3
License:	GPL v2
Group:		X11/Applications
Source0:	http://www.gnucash.org/pub/gnucash/sources/stable/%{name}-%{version}.tar.gz
# Source0-md5:	5ad11fbc5c86316632c5f9ec44dba659
Source1:	%{name}-icon.png
Patch0:		%{name}-info.patch
Patch1:		%{name}-am15.patch
Patch2:		%{name}-ignore_db1.patch
Patch3:		%{name}-libxml_includes_dir.patch
Patch4:		%{name}-guile_1_4_1.patch
URL:		http://www.gnucash.org/
BuildRequires:	GConf-devel
BuildRequires:	Guppi-devel >= 0.35.5
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bonobo-devel
BuildRequires:	db3-devel
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	g-wrap-devel >= 1.3.4
BuildRequires:	gal-devel
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	gdk-pixbuf-gnome-devel
BuildRequires:	gettext-devel
BuildRequires:	gnome-libs-devel
BuildRequires:	gnome-print-devel
BuildRequires:	gtk+-devel
BuildRequires:	gtkhtml-devel >= 0.8
BuildRequires:	guile-devel >= 1.3.4
BuildRequires:	libghttp-devel
BuildRequires:	libglade-gnome-devel
BuildRequires:	libltdl-devel
#BuildRequires:	libofx-devel
BuildRequires:	libtool
BuildRequires:	libxml-devel
BuildRequires:	openhbci-devel
BuildRequires:	slib >= 2c4
BuildRequires:	texinfo
Requires:	slib
Requires:	guile >= 1.3.4
Requires:	gnome-print >= 0.21
Requires:	perl
Prereq:		/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_sysconfdir	/etc/X11

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

%prep
%setup -q
%patch0 -p1
#%patch1 -p1
#%patch2 -p1
#%patch3 -p1
#%patch4 -p1

%build
#rm -f missing src/guile/Makefile.in
#%{__libtoolize}
#%{__aclocal} -I %{_aclocaldir}/gnome
#%{__autoconf}
#%{__automake}

export CPPFLAGS="%{rpmcflags} -I%{_prefix}/include"
%configure2_13 \
	--disable-prefer-db1
#	--enable-hbci
#	--enable-ofx

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

#gzip -9nf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/[!e]*

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
%doc AUTHORS ChangeLog* HACKING NEWS README* TODO
%doc doc/*.txt doc/examples doc/README* doc/RAW-NOTES doc/*HOWTO
#%doc %{_docdir}/%{name}-%{version}/
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%dir %attr(755,root,root) %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/libgnc*.so.*.*.*
%attr(755,root,root) %{_libdir}/%{name}/libgw*.so.*.*.*
%dir %attr(755,root,root) %{_libdir}/%{name}/overrides
%attr(755,root,root) %{_libdir}/%{name}/overrides/*
# Dunno if its needed runtime...
%attr(644,root,root) %{_libdir}/*.la
%attr(644,root,root) %{_libdir}/%{name}/*.la
%{_sysconfdir}/gnucash
%dir %{_datadir}/gnucash
%{_datadir}/gnucash/[!a]*
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
%{_datadir}/mime-info/*
%{_applnkdir}/Office/Misc/*
%{_pixmapsdir}/%{name}
%{_pixmapsdir}/%{name}-icon.png
%{_mandir}/*/*
%{_infodir}/*info*

# It's not needed, I think, maybe some devel subpackage?
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
#%{_aclocaldir}/*.m4
