#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.2.3
%define		qtver		5.15.2
%define		kf6ver		5.19.0
%define		kpname		kscreenlocker
Summary:	kscreenlocker
Name:		kp6-%{kpname}
Version:	6.2.3
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	888ef82d656558bb3304bea88c9c0ce6
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Network-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gettext-devel
BuildRequires:	kf6-kcmutils-devel >= %{kf6ver}
BuildRequires:	kf6-kcrash-devel >= %{kf6ver}
BuildRequires:	kf6-kdeclarative-devel >= %{kf6ver}
BuildRequires:	kf6-kglobalaccel-devel >= %{kf6ver}
BuildRequires:	kf6-kidletime-devel >= %{kf6ver}
BuildRequires:	kp6-layer-shell-qt-devel >= %{kdeplasmaver}
BuildRequires:	kp6-libkscreen-devel >= %{kdeplasmaver}
BuildRequires:	ninja
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xcb-util-keysyms-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
Obsoletes:	kp5-%{kpname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
kscreenlocker

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	kp5-%{kpname}-devel < %{version}

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname}6 --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kpname}6.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/libexec/kscreenlocker_greet
%ghost %{_libdir}/libKScreenLocker.so.6
%attr(755,root,root) %{_libdir}/libKScreenLocker.so.*.*
%{_datadir}/dbus-1/interfaces/kf6_org.freedesktop.ScreenSaver.xml
%{_datadir}/dbus-1/interfaces/org.kde.screensaver.xml
%{_datadir}/knotifications6/ksmserver.notifyrc
%dir %{_datadir}/ksmserver
%dir %{_datadir}/ksmserver/screenlocker
%dir %{_datadir}/ksmserver/screenlocker/org.kde.passworddialog
%{_datadir}/ksmserver/screenlocker/org.kde.passworddialog/metadata.desktop
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_screenlocker.so
%{_desktopdir}/kcm_screenlocker.desktop
%{_datadir}/qlogging-categories6/kscreenlocker.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KScreenLocker
%{_libdir}/cmake/KScreenLocker
%dir %{_libdir}/cmake/ScreenSaverDBusInterface
%{_libdir}/cmake/ScreenSaverDBusInterface/ScreenSaverDBusInterfaceConfig.cmake
%{_libdir}/libKScreenLocker.so
