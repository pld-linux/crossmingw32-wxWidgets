%define		realname	wxWidgets
Summary:	wxWidgets library - Mingw32 cross version
Summary(pl.UTF-8):	Biblioteka wxWidgets - wersja skrośna dla Mingw32
Name:		crossmingw32-%{realname}
Version:	2.8.7
Release:	1
License:	wxWidgets Licence (LGPL v2+ with exception)
Group:		Development/Libraries
Source0:	http://ftp.wxwidgets.org/pub/%{version}/%{realname}-%{version}.tar.bz2
# Source0-md5:	e3455083afdf6404a569a8bf0701cf13
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

%define		target			i386-mingw32
%define		target_platform		i386-pc-mingw32

%define		_sysprefix		/usr
%define		_sysbindir		%{_sysprefix}/bin
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif

%description
wxWidgets is a free C++ library for cross-platform GUI development.
With wxWidgets, you can create applications for different GUIs (GTK+,
Motif/LessTif, MS Windows, Mac) from the same source code.

%description -l pl.UTF-8
wxWidgets to wolnodostępna biblioteka napisana w C++ umożliwiająca
rozwijanie wieloplatformowych programów GUI. Przy użyciu wxWidgets
można tworzyć aplikacje dla różnych GUI (GTK+, Motif/LessTif, MS
Windows, Mac) z tego samego kodu źródłowego.

%package dll
Summary:	%{realname} - DLL library for Windows
Summary(pl.UTF-8):	%{realname} - biblioteka DLL dla Windows
Group:		Applications/Emulators

%description dll
%{realname} - DLL libraries for Windows.

%description dll -l pl.UTF-8
%{realname} - biblioteki DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_libdir}/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

ln -s %{_libdir}/wx/config/i386-mingw32-msw-ansi-release-2.8 $RPM_BUILD_ROOT%{_sysbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sysbindir}/i386-mingw32-msw-ansi-release-*
%{_libdir}/libwx_*.dll.a
%dir %{_libdir}/wx
%dir %{_libdir}/wx/config
%attr(755,root,root) %{_libdir}/wx/config/*
%{_libdir}/wx/include
%{_includedir}/wx-*

%files dll
%defattr(644,root,root,755)
%{_dlldir}/wx*_gcc.dll
