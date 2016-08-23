Summary:	An API-driven pkg-config replacement
Name:		pkgconf
Version:	0.9.12
Release:	2
License:	GPLv2+
Group:		Development/Other
Url:		https://github.com/pkgconf
Source0:	http://rabbit.dereferenced.org/~nenolod/distfiles/%{name}-%{version}.tar.bz2
# (fhimpe) Otherwise packages with pc files having
# Requires: pkg-config > X are not installable
Provides:	pkgconfig(pkg-config) = %{version}
Provides:	pkgconfig(pkg-config) = 0.29.1-2
Provides:	pkgconfig = 0.29.1-2
Obsoletes:	pkgconfig <= 0.29.1-1

%description
pkgconf is a program which helps to configure compiler
and linker flags for development frameworks.

It is similar to pkg-config, but was written from scratch
in the summer of 2011 to replace pkg-config, which for a 
while needed itself to build itself (they have since included 
a 'stripped down copy of glib 2.0') Since then we have worked 
on improving pkg-config for embedded use.

%prep
%setup -q

%build
%configure \
	--with-system-includedir=%{_includedir} \
	--with-system-libdir=%{_libdir} \
	--with-pkg-config-dir="%{_libdir}/pkgconfig:%{_datadir}/pkgconfig"

%make

%check
make check

%install
%makeinstall_std

# (tpg) enable it when we obsolete pkg-config
# these compat links and direcotries are needed
ln -sf %{_bindir}/pkgconf %{buildroot}%{_bindir}/pkg-config
ln -sf %{_bindir}/pkgconf %{buildroot}%{_bindir}/%{_target}-pkg-config

mkdir -p %{buildroot}%{_libdir}/pkgconfig
%if "%{_lib}" != "lib"
mkdir -p %{buildroot}%{_prefix}/lib/pkgconfig
ln -s ../../lib/pkgconfig %{buildroot}%{_libdir}/pkgconfig/32
%endif

mkdir -p %{buildroot}%{_datadir}/pkgconfig

%files
%doc AUTHORS COPYING README.md
%{_bindir}/pkgconf
%{_bindir}/pkg-config
%{_libdir}/pkgconfig
%if "%{_lib}" != "lib"
%{_prefix}/lib/pkgconfig
%{_libdir}/pkgconfig/32
%endif
%{_datadir}/pkgconfig
%{_datadir}/aclocal/pkg.m4
%{_mandir}/man1/pkgconf.1.*
