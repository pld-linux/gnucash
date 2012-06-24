%include	/usr/lib/rpm/macros.perl
Summary:	GnuCash is an application to keep track of your finances
Summary(ja):	GnuCash -- �ȷ����ե�
Summary(pl):	GnuCash - aplikacja do zarz�dzania twoimi finansami
Summary(pt_BR):	O GnuCash � uma aplica��o para acompanhamento de suas finan�as
Summary(zh_CN):	GnuCash -- ���ĸ��˲���������
Name:		gnucash
Version:	1.6.6
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://www.gnucash.org/pub/gnucash/sources/stable/%{name}-%{version}.tar.gz
Source1:	%{name}-icon.png
Patch0:		%{name}-am15.patch
Patch1:		%{name}-info.patch
Patch2:		%{name}-ignore_db1.patch
Patch3:		%{name}-libxml_includes_dir.patch
Patch4:		%{name}-guile_1_4_1.patch
URL:		http://www.gnucash.org/
BuildRequires:	GConf-devel
BuildRequires:	Guppi-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bonobo-devel
BuildRequires:	db3-devel
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	g-wrap-devel >= 1.1.9
BuildRequires:	gal-devel
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	gdk-pixbuf-gnome-devel
BuildRequires:	gettext-devel
BuildRequires:	gnome-libs-devel
BuildRequires:	gnome-print-devel
BuildRequires:	gtk+-devel
BuildRequires:	gtkhtml-devel >= 0.8
BuildRequires:	guile-devel
BuildRequires:	libghttp-devel
BuildRequires:	libglade-gnome-devel
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	libxml-devel
BuildRequires:	slib
BuildRequires:	texinfo
Requires:	slib
Requires:	guile >= 1.3.4
Requires:	gnome-print >= 0.21
Requires:	perl
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

%description -l ja
GnuCash �ϸĿ͸�����ץ��եȤǤ���GUI �����Ѥ��Ƽ������ٽС���Ը��¡�
�����ʤɤμ�������Ģ�Ǥ��ޤ������󥿡��ե������ϥ���ץ�ˡ���ñ��
���ѤǤ���褦���߷פ��Ƥ��ޤ��������Τ����ɵڤ��Ƥ��뤿���ʣ������
��׵�������Ѥ��Ƥ��ꡢʣ�����˴ؤ����μ���ɬ�פǤ���

%description -l pl
GnuCash jest mened�erem finans�w osobistych. Pozwala na �ledzenie i
wpisywanie zasob�w na swoich kontach bankowych, zak�ad�w. Daje wgl�d
nawet w kursy walut. Interfejs zosta� zaprojektowany z my�l� o
prostocie i �atwo�ci u�ycia.

%description -l pt_BR
O GnuCash � um gerenciador de finan�as pessoais. Uma interface
parecida com um canhoto de cheques permite que voc� acompanhe contas
banc�rias, a��es, sal�rio e mesmo tabelas de c�mbio de moedas. A
interface foi projetada para ser simples e f�cil de usar, mas tem o
suporte de princ�pios de contabilidade com entrada dupla para garantir
livros balanceados.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
rm -f missing src/guile/Makefile.in
%{__libtoolize}
aclocal -I %{_aclocaldir}/gnome
%{__autoconf}
%{__automake}

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
%doc %{_docdir}/%{name}-%{version}/
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libgncengine.so.*.*.*
%{_mandir}/*/*
%{_infodir}/*info*
%{_applnkdir}/Office/Misc/*
%dir %{_datadir}/gnucash
%{_datadir}/gnucash/[!a]*
%dir %{_datadir}/gnucash/accounts
%{_datadir}/gnucash/accounts/C
%lang(da) %{_datadir}/gnucash/accounts/da
%lang(de) %{_datadir}/gnucash/accounts/de_DE
%lang(es) %{_datadir}/gnucash/accounts/es_ES
%lang(pt) %{_datadir}/gnucash/accounts/pt_PT
%lang(sk) %{_datadir}/gnucash/accounts/sk
%{_datadir}/mime-info/*
%{_pixmapsdir}/%{name}
%{_pixmapsdir}/%{name}-icon.png
%{_sysconfdir}/gnucash
