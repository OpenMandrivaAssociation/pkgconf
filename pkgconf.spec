%define major 4
%define libname %mklibname %{name}
%define develname %mklibname %{name} -d

Summary:	An API-driven pkg-config replacement
Name:		pkgconf
Version:	2.0.2
Release:	2
License:	GPLv2+
Group:		Development/Other
Url:		https://github.com/pkgconf
Source0:	https://distfiles.dereferenced.org/pkgconf/%{name}-%{version}.tar.xz
# Useful tool to quickly figure out all dependencies, direct
# and indirect
Source1:	recursive-pkg-config-requires
# (fhimpe) Otherwise packages with pc files having
# Requires: pkg-config > X are not installable
Provides:	pkgconfig(pkg-config) = 0.29.2
Provides:	pkgconfig = 0.29.2
Obsoletes:	pkgconfig < 0.29.2
Conflicts:	pkgconfig < 0.29.2
Provides:	%{_bindir}/pkg-config
Provides:	%{_bindir}/%{_target_platform}-pkg-config

%description
pkgconf is a program which helps to configure compiler
and linker flags for development frameworks.

It is similar to pkg-config, but was written from scratch
in the summer of 2011 to replace pkg-config, which for a 
while needed itself to build itself (they have since included 
a 'stripped down copy of glib 2.0') Since then we have worked 
on improving pkg-config for embedded use.

%libpackage %{name} %{major}

%package -n %{develname}
Summary:	Header files and static libraries from %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{develname}
Libraries and includes files for
developing programs based on %{name}.

%prep
%autosetup -p1
%configure \
	--with-system-includedir=%{_includedir} \
	--with-system-libdir=%{_libdir} \
	--with-pkg-config-dir="%{_libdir}/pkgconfig:%{_datadir}/pkgconfig:%{_libdir}/qt6/lib/pkgconfig"

%build
%make_build

%install
%make_install

# (tpg) enable it when we obsolete pkg-config
# these compat links and direcotries are needed
ln -sf %{_bindir}/pkgconf %{buildroot}%{_bindir}/pkg-config
ln -sf %{_bindir}/pkgconf %{buildroot}%{_bindir}/%{_target_platform}-pkg-config

mkdir -p %{buildroot}%{_libdir}/pkgconfig
%if "%{_lib}" != "lib"
mkdir -p %{buildroot}%{_prefix}/lib/pkgconfig
ln -s ../../lib/pkgconfig %{buildroot}%{_libdir}/pkgconfig/32
%endif

mkdir -p %{buildroot}%{_datadir}/pkgconfig

install -c -m 755 %{S:1} %{buildroot}%{_bindir}/

%files
%doc AUTHORS COPYING README.md
%{_bindir}/bomtool
%{_bindir}/pkgconf
%{_bindir}/pkg-config
%{_bindir}/%{_target_platform}-pkg-config
%{_bindir}/recursive-pkg-config-requires
%dir %{_libdir}/pkgconfig
%if "%{_lib}" != "lib"
%dir %{_prefix}/lib/pkgconfig
%{_libdir}/pkgconfig/32
%endif
%dir %{_datadir}/pkgconfig
%{_datadir}/aclocal/pkg.m4
%doc %{_mandir}/man1/pkgconf.1.*
%doc %{_mandir}/man5/pc.*
%doc %{_mandir}/man5/pkgconf-personality.5.*
%doc %{_mandir}/man7/pkg.m4.*

%files -n %{develname}
%dir %{_includedir}/%{name}
%dir %{_includedir}/%{name}/libpkgconf
%{_includedir}/%{name}/libpkgconf/*.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/libpkgconf.pc
