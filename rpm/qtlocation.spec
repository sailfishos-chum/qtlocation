%global qt_version 5.15.9

Summary: Qt5 - Location component
Name: opt-qt5-qtlocation
Version: 5.15.9+kde5
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://www.qt.io
Source0: %{name}-%{version}.tar.bz2

# build failure with gcc10
# various C++ runtime headers indirectly included <string> which in turn
# included <local> and <cerrno>.  Those indirect inclusions have been
# eliminated which in turn forces packages to include the C++ headers they
# actually need.
Patch0: qtlocation-gcc10.patch

# filter plugin/qml provides
%global __provides_exclude_from ^(%{_opt_qt5_archdatadir}/qml/.*\\.so|%{_opt_qt5_plugindir}/.*\\.so)$
%{?opt_qt5_default_filter}

BuildRequires: make
BuildRequires: opt-qt5-qtbase-devel >= %{qt_version}
# QtPositioning core-private
BuildRequires: opt-qt5-qtbase-private-devel
%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}
BuildRequires: opt-qt5-qtdeclarative-devel >= %{qt_version}

BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(libssl)
BuildRequires: pkgconfig(libcrypto)

Requires: opt-qt5-qtbase-gui >= %{qt_version}
Requires: opt-qt5-qtdeclarative >= %{qt_version}

%description
The Qt Location and Qt Positioning APIs gives developers the ability to
determine a position by using a variety of possible sources, including
satellite, or wifi, or text file, and so on.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package pos-geoclue
Summary: Qt Location Positioning Plugin: geoclue
Requires: %{name}%{?_isa} = %{version}-%{release}
%description pos-geoclue
%{summary}.

%package pos-geoclue2
Summary: Qt Location Positioning Plugin: geoclue2
Requires: %{name}%{?_isa} = %{version}-%{release}
%description pos-geoclue2
%{summary}.

%package pos-positionpoll
Summary: Qt Location Positioning Plugin: positionpoll
Requires: %{name}%{?_isa} = %{version}-%{release}
%description pos-positionpoll
%{summary}.


%prep
%autosetup -n %{name}-%{version}/upstream -p1

%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

# no shadow builds until fixed: https://bugreports.qt.io/browse/QTBUG-37417
%{opt_qmake_qt5}

%make_build

%install
make install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_opt_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.GPL* LICENSE.LGPL*
%{_opt_qt5_libdir}/libQt5Location.so.5*
%{_opt_qt5_archdatadir}/qml/QtLocation/
%{_opt_qt5_plugindir}/geoservices/
%{_opt_qt5_libdir}/libQt5Positioning.so.5*
%dir %{_opt_qt5_archdatadir}/qml/QtPositioning
%{_opt_qt5_archdatadir}/qml/QtPositioning/*
%{_opt_qt5_qmldir}/Qt/labs/location/*
%dir %{_opt_qt5_plugindir}/position
%{_opt_qt5_libdir}/libQt5PositioningQuick.so.5*

%files pos-geoclue
%{_opt_qt5_plugindir}/position/libqtposition_geoclue.so

%files pos-geoclue2
%{_opt_qt5_plugindir}/position/libqtposition_geoclue2.so

%files pos-positionpoll
%{_opt_qt5_plugindir}/position/libqtposition_positionpoll.so

%files devel
%{_opt_qt5_headerdir}/QtLocation/
%{_opt_qt5_libdir}/libQt5Location.so
%{_opt_qt5_libdir}/libQt5Location.prl
%{_opt_qt5_headerdir}/QtPositioning/
%{_opt_qt5_libdir}/libQt5Positioning.so
%{_opt_qt5_libdir}/libQt5Positioning.prl
%{_opt_qt5_headerdir}/QtPositioningQuick/
%{_opt_qt5_libdir}/libQt5PositioningQuick.so
%{_opt_qt5_libdir}/libQt5PositioningQuick.prl
%{_opt_qt5_libdir}/pkgconfig/Qt5Location.pc
%dir %{_opt_qt5_libdir}/cmake/Qt5Location
%{_opt_qt5_libdir}/cmake/Qt5Location/Qt5Location*.cmake
%{_opt_qt5_archdatadir}/mkspecs/modules/qt_lib_location*.pri
%{_opt_qt5_libdir}/pkgconfig/Qt5Positioning.pc
%dir %{_opt_qt5_libdir}/cmake/Qt5Positioning
%{_opt_qt5_libdir}/cmake/Qt5Positioning/Qt5Positioning*.cmake
%{_opt_qt5_archdatadir}/mkspecs/modules/qt_lib_positioning*.pri
%{_opt_qt5_libdir}/pkgconfig/Qt5PositioningQuick.pc
%dir %{_opt_qt5_libdir}/cmake/Qt5PositioningQuick/
%{_opt_qt5_libdir}/cmake/Qt5PositioningQuick/Qt5PositioningQuick*.cmake
%{_opt_qt5_archdatadir}/mkspecs/modules/qt_lib_positioning*.pri
