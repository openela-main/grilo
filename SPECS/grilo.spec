# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           grilo
Version:        0.3.6
Release:        3%{?dist}
Summary:        Content discovery framework

License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/Grilo
Source0:        https://download.gnome.org/sources/grilo/%{release_version}/grilo-%{version}.tar.xz
Patch0001:      0001-Include-file-to-build-docs-with-meson.patch
# https://gitlab.gnome.org/GNOME/grilo/-/merge_requests/78
Patch0002:      0002-net-Fix-TLS-cert-validation-not-being-done-for-any-n.patch

BuildRequires:  meson
BuildRequires:  git
BuildRequires:  chrpath
BuildRequires:  gnome-common
BuildRequires:  intltool
BuildRequires:  vala >= 0.27.1
BuildRequires:  gtk-doc
BuildRequires:  gobject-introspection-devel >= 0.9.0
BuildRequires:  libxml2-devel
BuildRequires:  libsoup-devel
BuildRequires:  glib2-devel
# For the test UI
BuildRequires:  gtk3-devel
BuildRequires:  liboauth-devel
BuildRequires:  totem-pl-parser-devel

%description
Grilo is a framework that provides access to different sources of
multimedia content, using a pluggable system.
This package contains the core library and elements.

%package devel
Summary:        Libraries/include files for Grilo framework
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Provide upgrade path for -vala subpackage that was merged into -devel during
# the F23 cycle
Obsoletes:      grilo-vala < 0.2.13

%description devel
Grilo is a framework that provides access to different sources of
multimedia content, using a pluggable system.
This package contains the core library and elements, as well as
general and API documentation.

%prep
%autosetup -p1 -S git

%build
%meson -Denable-gtk-doc=true

%meson_build

%install
%meson_install

mkdir -p $RPM_BUILD_ROOT%{_libdir}/grilo-%{release_version}/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/grilo-%{release_version}/plugins/

# Remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/grl-inspect-%{release_version}
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/grl-launch-%{release_version}
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/grilo-test-ui-%{release_version}
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgrlnet-%{release_version}.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgrlpls-%{release_version}.so

# Remove files that will not be packaged
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_bindir}/grilo-simple-playlist

%find_lang grilo

%ldconfig_scriptlets

%files -f grilo.lang
%license COPYING
%doc AUTHORS NEWS README TODO
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/
%{_bindir}/grl-inspect-%{release_version}
%{_bindir}/grl-launch-%{release_version}
%{_bindir}/grilo-test-ui-%{release_version}
%{_libdir}/grilo-%{release_version}/
%{_datadir}/grilo-%{release_version}/
%{_mandir}/man1/grilo-test-ui-%{release_version}.1*
%{_mandir}/man1/grl-inspect-%{release_version}.1*
%{_mandir}/man1/grl-launch-%{release_version}.1*

%files devel
%{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{name}-%{release_version}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/
%{_datadir}/vala/

%changelog
* Wed Aug 25 2021 Bastien Nocera <bnocera@redhat.com> - 0.3.6-3
+ grilo-0.3.6-3
- Fix TLS not being validated correctly
- Resolves: rhbz#1997234

* Sat Jul 28 2018 Victor Toso <victortoso@redhat.com> - 0.3.6-2
- Switch to meson build system

* Fri Jul 27 2018 Victor Toso <victortoso@redhat.com> - 0.3.6-1
- Update to 0.3.6

* Wed Jul 18 2018 Victor Toso <victortoso@redhat.com> - 0.3.5-1
- Update to 0.3.5

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.4-2
- Switch to %%ldconfig_scriptlets

* Thu Aug 24 2017 Bastien Nocera <bnocera@redhat.com> - 0.3.4-1
+ grilo-0.3.4-1
- Update to 0.3.4

* Thu Aug 10 2017 Kalev Lember <klember@redhat.com> - 0.3.3-4
- Rebuilt for libtotem-plparser soname bump

* Mon Jul 31 2017 Kalev Lember <klember@redhat.com> - 0.3.3-3
- Rebuilt for libtotem-plparser soname bump

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 14 2017 Kalev Lember <klember@redhat.com> - 0.3.3-1
- Update to 0.3.3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 17 2016 Kalev Lember <klember@redhat.com> - 0.3.2-4
- Stop providing grilo 0.2 ABI compatibility

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 0.3.2-3
- BR vala instead of obsolete vala-tools subpackage

* Wed Sep 21 2016 Bastien Nocera <bnocera@redhat.com> - 0.3.2-2
+ grilo-0.3.2-1
- Take ownership of /usr/share/grilo-0.3 not just its plugins subdir

* Mon Sep 12 2016 Kalev Lember <klember@redhat.com> - 0.3.2-1
- Update to 0.3.2
- Don't set group tags
- Avoid requiring gobject-introspection for directory ownership
- Use make_install macro

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 0.3.1-1
- Update to 0.3.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 18 2015 Kalev Lember <klember@redhat.com> - 0.3.0-1
- Update to 0.3.0
- Update project URL
- Include previous ABI version for temporary binary compatibility

* Wed Sep 09 2015 Kalev Lember <klember@redhat.com> - 0.2.15-1
- Update to 0.2.15

* Tue Sep 08 2015 Kalev Lember <klember@redhat.com> - 0.2.13-1
- Update to 0.2.13
- Merge -vala subpackage into -devel
- Tighten -devel subpackage deps with the _isa macro
- Don't duplicate %%doc-marked files in -devel
- Mark COPYING as %%license

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 19 2015 Richard Hughes <rhughes@redhat.com> - 0.2.12-1
- Update to 0.2.12

* Sun Aug 24 2014 Kalev Lember <kalevlember@gmail.com> - 0.2.11-1
- Update to 0.2.11

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.2.10-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 19 2014 Richard Hughes <rhughes@redhat.com> - 0.2.10-1
- Update to 0.2.10

* Wed Feb 19 2014 Kalev Lember <kalevlember@gmail.com> - 0.2.9-2
- Build with totem-pl-parser and oauth support

* Wed Feb 19 2014 Kalev Lember <kalevlember@gmail.com> - 0.2.9-1
- Update to 0.2.9

* Wed Feb 05 2014 Adam Williamson <awilliam@redhat.com> - 0.2.7-2
- backport some patches from upstream that are needed for totem

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 0.2.7-1
- Update to 0.2.7

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 18 2013 Kalev Lember <kalevlember@gmail.com> - 0.2.6-1
- Update to 0.2.6
- Drop the vala sed hack, 0.2.6 now works with recent vala
- Include man pages

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.2.5-1
- Update to 0.2.5

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 04 2012 Bastien Nocera <bnocera@redhat.com> 0.2.4-1
- Update to 0.2.4

* Tue Nov 13 2012 Kalev Lember <kalevlember@gmail.com> 0.2.3-1
- Update to 0.2.3

* Fri Oct 05 2012 Bastien Nocera <bnocera@redhat.com> 0.2.2-1
- Update to 0.2.2

* Wed Oct 03 2012 Bastien Nocera <bnocera@redhat.com> 0.2.1-1
- Update to 0.2.1

* Fri Aug 31 2012 Debarshi Ray <rishi@fedoraproject.org> 0.2.0-1
- update to 0.2.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 Bastien Nocera <bnocera@redhat.com> 0.1.19-1
- Update to 0.1.19

* Wed Mar  7 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.18-3
- fix build with vala 0.15/0.16

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Bastien Nocera <bnocera@redhat.com> 0.1.18-1
- Update to 0.1.18

* Fri Oct 14 2011 Adam Williamson <awilliam@redhat.com> 0.1.17-1
- update to 0.1.17

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 0.1.16-1
- Update to 0.1.16

* Fri May 20 2011 Bastien Nocera <bnocera@redhat.com> 0.1.15-3
- Own the grilo plugins directories

* Wed Apr 27 2011 Bastien Nocera <bnocera@redhat.com> 0.1.15-2
- Update with review comments

* Thu Apr 21 2011 Bastien Nocera <bnocera@redhat.com> 0.1.15-1
- Fist package, based on upstream work by Juan A.
  Suarez Romero <jasuarez@igalia.com>

