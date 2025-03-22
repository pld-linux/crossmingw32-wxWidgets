%define		realname	wxWidgets
Summary:	wxWidgets library - MinGW32 cross version
Summary(pl.UTF-8):	Biblioteka wxWidgets - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	3.2.4
Release:	1
License:	wxWidgets Library Licence 3.1 (LGPL v2+ with exception)
Group:		Development/Libraries
#Source0Download: https://github.com/wxWidgets/wxWidgets/releases
Source0:	https://github.com/wxWidgets/wxWidgets/releases/download/v%{version}/%{realname}-%{version}.tar.bz2
# Source0-md5:	8eada508f5bdf390eeec5b0e0af38f71
Patch0:		%{realname}-samples.patch
Patch1:		%{realname}-ac.patch
Patch2:		%{realname}-gifdelay.patch
URL:		https://www.wxWidgets.org/
BuildRequires:	autoconf >= 2.58
BuildRequires:	automake
#BuildRequires:	bakefile >= 0.2.12
BuildRequires:	crossmingw32-expat
BuildRequires:	crossmingw32-gcc-c++
BuildRequires:	crossmingw32-libjpeg
BuildRequires:	crossmingw32-libpng
BuildRequires:	crossmingw32-libtiff
BuildRequires:	crossmingw32-w32api
BuildRequires:	crossmingw32-zlib >= 1.1.4
BuildRequires:	libtool
Requires:	crossmingw32-expat
Requires:	crossmingw32-libjpeg
Requires:	crossmingw32-libpng
Requires:	crossmingw32-libtiff
Requires:	crossmingw32-w32api
Obsoletes:	crossmingw32-wxMSW < 2.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages	0
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
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld    -Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*
%define		filterout_cxx	-f[-a-z0-9=]*

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
Requires:	crossmingw32-expat-dll
Requires:	crossmingw32-libjpeg-dll
Requires:	crossmingw32-libpng-dll
Requires:	crossmingw32-libtiff-dll
Requires:	crossmingw32-zlib-dll >= 1.1.4

%description dll
%{realname} - DLL libraries for Windows.

%description dll -l pl.UTF-8
%{realname} - biblioteki DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
cp -f /usr/share/automake/config.sub .
%{__aclocal} -I build/aclocal
%{__autoconf}

%configure \
	--host=%{target} \
	--target=%{target} \
	--disable-precomp-headers \
	--enable-calendar \
	--enable-controls \
	--enable-plugins \
	--enable-std-iostreams \
	--enable-vendor=pld \
	--with-msw \
	--with-opengl

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_dlldir},%{_sysbindir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_bindir}/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

ln -sf %{_libdir}/wx/config/i386-mingw32-msw-unicode-3.2 $RPM_BUILD_ROOT%{_sysbindir}/i386-mingw32-wx-msw-unicode-config

# use from native wxWidgets if needed
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{aclocal,bakefile,locale}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sysbindir}/i386-mingw32-wx-msw-unicode-config
%{_libdir}/libwx_baseu-3.2-i386-mingw32.dll.a
%{_libdir}/libwx_baseu_net-3.2-i386-mingw32.dll.a
%{_libdir}/libwx_baseu_xml-3.2-i386-mingw32.dll.a
%{_libdir}/libwx_mswu_adv-3.2-i386-mingw32.dll.a
%{_libdir}/libwx_mswu_aui-3.2-i386-mingw32.dll.a
%{_libdir}/libwx_mswu_core-3.2-i386-mingw32.dll.a
%{_libdir}/libwx_mswu_gl-3.2-i386-mingw32.dll.a
%{_libdir}/libwx_mswu_html-3.2-i386-mingw32.dll.a
%{_libdir}/libwx_mswu_media-3.2-i386-mingw32.dll.a
%{_libdir}/libwx_mswu_propgrid-3.2-i386-mingw32.dll.a
%{_libdir}/libwx_mswu_qa-3.2-i386-mingw32.dll.a
%{_libdir}/libwx_mswu_ribbon-3.2-i386-mingw32.dll.a
%{_libdir}/libwx_mswu_richtext-3.2-i386-mingw32.dll.a
%{_libdir}/libwx_mswu_stc-3.2-i386-mingw32.dll.a
%{_libdir}/libwx_mswu_webview-3.2-i386-mingw32.dll.a
%{_libdir}/libwx_mswu_xrc-3.2-i386-mingw32.dll.a
%dir %{_libdir}/wx
%dir %{_libdir}/wx/config
%attr(755,root,root) %{_libdir}/wx/config/i386-mingw32-msw-unicode-3.2
%{_libdir}/wx/include
%{_includedir}/wx-3.2

%files dll
%defattr(644,root,root,755)
%{_dlldir}/wxbase32u_gcc_pld.dll
%{_dlldir}/wxbase32u_net_gcc_pld.dll
%{_dlldir}/wxbase32u_xml_gcc_pld.dll
%{_dlldir}/wxmsw32u_adv_gcc_pld.dll
%{_dlldir}/wxmsw32u_aui_gcc_pld.dll
%{_dlldir}/wxmsw32u_core_gcc_pld.dll
%{_dlldir}/wxmsw32u_gl_gcc_pld.dll
%{_dlldir}/wxmsw32u_html_gcc_pld.dll
%{_dlldir}/wxmsw32u_media_gcc_pld.dll
%{_dlldir}/wxmsw32u_propgrid_gcc_pld.dll
%{_dlldir}/wxmsw32u_qa_gcc_pld.dll
%{_dlldir}/wxmsw32u_ribbon_gcc_pld.dll
%{_dlldir}/wxmsw32u_richtext_gcc_pld.dll
%{_dlldir}/wxmsw32u_stc_gcc_pld.dll
%{_dlldir}/wxmsw32u_webview_gcc_pld.dll
%{_dlldir}/wxmsw32u_xrc_gcc_pld.dll
