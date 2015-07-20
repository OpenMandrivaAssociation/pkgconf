Summary:	An API-driven pkg-config replacement
Name:		pkgconf
Version:	0.9.12
Release:	1
License:	GPLv2+
Group:		Development/Other
Url:		https://github.com/pkgconf
Source0:	http://rabbit.dereferenced.org/~nenolod/distfiles/%{name}-%{version}.tar.bz2
# (fhimpe) Otherwise packages with pc files having
# Requires: pkg-config > X are not installable
#Provides:	pkgconfig(pkg-config) = %{version}

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


%install
%makeinstall_std

%check
%make check

%files
%doc AUTHORS COPYING README.md
