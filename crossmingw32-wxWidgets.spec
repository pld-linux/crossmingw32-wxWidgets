%define		realname	wxWidgets
Summary:	wxWidgets library - Mingw32 cross version
Summary(pl):	Biblioteka wxWidgets - wersja skro¶na dla Mingw32
Name:		crossmingw32-%{realname}
Version:	2.8.0
Release:	1
License:	wxWidgets Licence (LGPL with exception)
Group:		Development/Libraries
Source0:	http://dl.sourceforge.net/wxwindows/%{realname}-%{version}.tar.bz2
# Source0-md5:	183a1fe136d7caacb60c717bbbef9788
Patch0:		%{realname}-samples.patch
Patch1:		%{realname}-ac.patch
Patch2:		%{realname}-gif0delay.patch
URL:		http://www.wxWidgets.org/
BuildRequires:	autoconf >= 2.58
BuildRequires:	automake
#BuildRequires:	bakefile >= 0.1.9
BuildRequires:	crossmingw32-gcc-c++
BuildRequires:	crossmingw32-libjpeg
BuildRequires:	crossmingw32-libpng
BuildRequires:	crossmingw32-runtime
BuildRequires:	libtool
Requires:	crossmingw32-libjpeg
Requires:	crossmingw32-libpng
Requires:	crossmingw32-runtime
Obsoletes:	crossmingw32-wxMSW
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target		i386-mingw32
%define		target_platform	i386-pc-mingw32
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib		%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		__cc		%{target}-gcc
%define		__cxx		%{target}-g++

%ifarch alpha sparc sparc64 sparcv9
%define		optflags	-O2
%endif

%description
wxWidgets is a free C++ library for cross-platform GUI development.
With wxWidgets, you can create applications for different GUIs (GTK+,
Motif/LessTif, MS Windows, Mac) from the same source code.

%description -l pl
wxWidgets to wolnodostêpna biblioteka napisana w C++ umo¿liwiaj±ca
rozwijanie wieloplatformowych programów GUI. Przy u¿yciu wxWidgets
mo¿na tworzyæ aplikacje dla ró¿nych GUI (GTK+, Motif/LessTif, MS
Windows, Mac) z tego samego kodu ¼ród³owego.

%package dll
Summary:	%{realname} - DLL library for Windows
Summary(pl):	%{realname} - biblioteka DLL dla Windows
Group:		Applications/Emulators

%description dll
%{realname} - DLL libraries for Windows.

%description dll -l pl
%{realname} - biblioteki DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
CC=%{target}-gcc ; export CC
CXX=%{target}-g++ ; export CXX
LD=%{target}-ld ; export LD
AR=%{target}-ar ; export AR
AS=%{target}-as ; export AS
CROSS_COMPILE=1 ; export CROSS_COMPILE
CPPFLAGS="-I%{arch}/include" ; export CPPFLAGS
RANLIB=%{target}-ranlib ; export RANLIB
LDSHARED="%{target}-gcc -shared" ; export LDSHARED
TARGET="%{target}" ; export TARGET

cp -f /usr/share/automake/config.sub .
%{__aclocal} -I build/aclocal
%{__autoconf}

%configure \
	--with-msw \
	--with-opengl \
	--disable-precomp-headers \
	--enable-official-build \
	--enable-std-iostreams \
	--enable-controls \
	--enable-tabdialog \
	--host=%{target} \
	--target=%{target}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{arch}/{bin,include,lib},%{_datadir}/wine/windows/system}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

sed -i  -e 's@includedir="/usr/include"@includedir="%{arch}/include"@' \
	-e 's@libdir="/usr/lib"@libdir="%{arch}/lib"@' \
	$RPM_BUILD_ROOT%{_libdir}/wx/config/*

%if 0%{!?debug:1}
%{target}-strip $RPM_BUILD_ROOT%{_libdir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

cp -r $RPM_BUILD_ROOT%{_libdir}/*.a $RPM_BUILD_ROOT%{arch}/lib
cp -r $RPM_BUILD_ROOT%{_libdir}/*.dll $RPM_BUILD_ROOT%{_datadir}/wine/windows/system
cp -r $RPM_BUILD_ROOT%{_libdir}/wx $RPM_BUILD_ROOT%{arch}/lib/
cp -r $RPM_BUILD_ROOT%{_includedir} $RPM_BUILD_ROOT%{arch}

ln -s %{arch}/lib/wx/config/i386-mingw32-msw-ansi-release-2.8 $RPM_BUILD_ROOT%{_bindir}

rm $RPM_BUILD_ROOT%{_bindir}/wx-config

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/i386-mingw32-*
%{arch}/lib/*.a
%dir %{arch}/lib/wx
%dir %{arch}/lib/wx/config
%attr(755,root,root) %{arch}/lib/wx/config/*
%{arch}/lib/wx/include
%{arch}/include/*

%files dll
%defattr(644,root,root,755)
%{_datadir}/wine/windows/system/*
