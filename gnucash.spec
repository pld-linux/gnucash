Name: gnucash
Summary: GnuCash is an application to keep track of your finances.
Version: 1.2.5
Release: 1
Copyright: Free Software Foundation
Group: Applications/Finance
Source: ftp://ftp.gnucash.org/pub/gnucash/sources/stable/gnucash-1.2.5.tar.gz
Packager: Eugene Kanter (eugene@bgs.com)

BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GnuCash is a personal finance manager.  A check-book like
register GUI allows you to enter and track bank accounts,
stocks, income and even currency trades.  The interface is
designed to be simple and easy to use, but is backed with
double-entry accounting principles to ensure balanced books.

%prep
%setup

%build
X_LIBS=-lXp ./configure --prefix=/usr --sysconfdir=/etc
make motif

%install
make prefix=$RPM_BUILD_ROOT/usr sysconfdir=$RPM_BUILD_ROOT/etc GNC_CONFIGDIR=$RPM_BUILD_ROOT/etc/gnucash install
#make prefix=$RPM_BUILD_ROOT/usr sysconfdir=$RPM_BUILD_ROOT/etc GNC_BINDIR=$RPM_BUILD_ROOT/usr/bin GNC_CONFIGDIR=$RPM_BUILD_ROOT/etc/gnucash GNC_DOCDIR=$RPM_BUILD_ROOT/usr/doc/gnucash install
#rm -rf $RPM_BUILD_ROOT/usr/doc/gnucash

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(444,root,root,755)
%attr(555,-,-) /usr/bin/gnucash.motif
/usr/bin/gnucash
/usr/bin/gnc-prices
/usr/lib/gnucash
/usr/share/gnucash

%doc /usr/doc/gnucash
