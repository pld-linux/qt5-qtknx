#
# Conditional build:
%bcond_without	doc	# Documentation

%define		orgname		qtknx
%define		qtbase_ver	%{version}
%define		qttools_ver	%{version}
Summary:	The Qt5 Knx library
Summary(pl.UTF-8):	Biblioteka Qt5 Knx
Name:		qt5-%{orgname}
Version:	5.15.7
Release:	1
License:	GPL v3+ or commercial
Group:		Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	c4ccf455d10a3b72c4c3ca16e7425093
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Network-devel >= %{qtbase_ver}
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	openssl-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.016
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Knx library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 Knx.

%package -n Qt5Knx
Summary:	The Qt5 Knx library
Summary(pl.UTF-8):	Biblioteka Qt5 Knx
Group:		Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Network >= %{qtbase_ver}

%description -n Qt5Knx
The Qt KNX module implements the client side of a connection between a
client and a KNXnet/IP server. This connection can be used to send
messages to the KNX bus and to control the functionalities of the KNX
devices.

%description -n Qt5Knx -l pl.UTF-8
Moduł Qt KNX implementuje stronę kliencką połączenia między klientem a
serwerem KNXnet/IP. Połączenie może być używane do wysyłania
komunikatów do szyny KNX oraz sterowania funkcjami urządzeń KNX.

%package -n Qt5Knx-devel
Summary:	Qt5 Knx library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Knx - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Knx = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Network-devel >= %{qtbase_ver}

%description -n Qt5Knx-devel
Qt5 Knx library - development files.

%description -n Qt5Knx-devel -l pl.UTF-8
Biblioteka Qt5 Knx - pliki programistyczne.

%package doc
Summary:	Qt5 Knx documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Knx w formacie HTML
License:	FDL v1.3
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc
Qt5 Knx documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Knx w formacie HTML.

%package doc-qch
Summary:	Qt5 Knx documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Knx w formacie QCH
License:	FDL v1.3
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 Knx documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Knx w formacie QCH.

%package examples
Summary:	Qt5 Knx examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 Knx
License:	BSD or commercial
Group:		Development/Libraries
BuildArch:	noarch

%description examples
Qt5 Knx examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 Knx.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}

%build
%{qmake_qt5}
%{__make}
%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/knx

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Knx -p /sbin/ldconfig
%postun	-n Qt5Knx -p /sbin/ldconfig

%files -n Qt5Knx
%defattr(644,root,root,755)
%doc LICENSE.GPL3-EXCEPT dist/changes-*
# R: Qt5Core Qt5Network
%attr(755,root,root) %{_libdir}/libQt5Knx.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Knx.so.5

%files -n Qt5Knx-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Knx.so
%{_libdir}/libQt5Knx.prl
%{_includedir}/qt5/QtKnx
%{_pkgconfigdir}/Qt5Knx.pc
%{_libdir}/cmake/Qt5Knx
%{qt5dir}/mkspecs/modules/qt_lib_knx.pri
%{qt5dir}/mkspecs/modules/qt_lib_knx_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtknx

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtknx.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
