%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: Text based document generation
Name: asciidoc
Version: 8.4.5
Release: 4.1%{?dist}
# The python code does not specify a version.
# The javascript example code is GPLv2+.
License: GPL+ and GPLv2+
Group: Applications/System
URL: http://www.methods.co.nz/asciidoc/
Source0: http://www.methods.co.nz/asciidoc/%{name}-%{version}.tar.gz
# http://groups.google.com/group/asciidoc/browse_thread/thread/7f7a633c5b11ddc3
Patch0: asciidoc-8.4.5-datadir.patch
# https://bugzilla.redhat.com/506953
Patch1: asciidoc-8.4.5-use-unsafe-mode-by-default.patch
BuildRequires: python >= 2.4
Requires: python >= 2.4
Requires: docbook-style-xsl
Requires: libxslt
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
AsciiDoc is a text document format for writing short documents,
articles, books and UNIX man pages. AsciiDoc files can be translated
to HTML and DocBook markups using the asciidoc(1) command.

%prep
%setup -q
%patch0 -p1 -b .datadir
%patch1 -p1 -b .use-unsafe-mode-by-default

# Fix line endings on COPYRIGHT file
sed -i "s/\r//g" COPYRIGHT

# Convert CHANGELOG and README to utf-8
for file in CHANGELOG README; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%build
%configure

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# real conf data goes to sysconfdir, rest to datadir; symlinks so asciidoc works
for d in dblatex docbook-xsl images javascripts stylesheets ; do
    mv %{buildroot}%{_sysconfdir}/asciidoc/$d \
        %{buildroot}%{_datadir}/asciidoc
    ln -s %{_datadir}/asciidoc/$d %{buildroot}%{_sysconfdir}/asciidoc/
done

# Python API
install -Dpm 644 asciidocapi.py %{buildroot}%{python_sitelib}/asciidocapi.py

# Make it easier to %exclude these with both rpm < and >= 4.7
for file in %{buildroot}{%{_bindir},%{_datadir}/asciidoc/filters/*}/*.py ; do
    touch ${file}{c,o}
done


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%config(noreplace) %{_sysconfdir}/asciidoc
%exclude %{_bindir}/*.py[co]
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/asciidoc/
%exclude %{_datadir}/asciidoc/filters/*/*.py[co]
%{python_sitelib}/asciidocapi.py*
%doc README BUGS CHANGELOG COPYRIGHT

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 8.4.5-4.1
- Rebuilt for RHEL 6

* Tue Sep  8 2009 Ville Skyttä <ville.skytta@iki.fi> - 8.4.5-4
- Remaining improvements from #480288:
- Add dependencies on libxslt and docbook-style-xsl.
- Install dblatex style sheets.
- Exclude unneeded *.py[co].
- Install python API.
- Specfile cleanups.

* Thu Aug 13 2009 Todd Zullinger <tmz@pobox.com> - 8.4.5-3
- Use 'unsafe' mode by default (bug 506953)
- Install filter scripts in %%{_datadir}/asciidoc
- Convert spec file, CHANGELOG, and README to utf-8
- Preserve timestamps on installed files, where feasible
- s/$RPM_BUILD_ROOT/%%{buildroot} and drop duplicated /'s
- Fix rpmlint mixed-use-of-spaces-and-tabs and end-of-line-encoding warnings

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 19 2009 Dave Airlie <airlied@redhat.com> 8.4.5-1
- new upstream version 8.4.5 - required by X.org libXi to build

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 8.2.5-3
- fix license tag

* Wed Dec 05 2007 Florian La Roche <laroche@redhat.com> - 8.2.5-2
- remove doc/examples from filelist due to dangling symlinks

* Tue Nov 20 2007 Florian La Roche <laroche@redhat.com> - 8.2.5-1
- new upstream version 8.2.5

* Mon Oct 22 2007 Florian La Roche <laroche@redhat.com> - 8.2.3-1
- new upstream version 8.2.3

* Sat Sep 01 2007 Florian La Roche <laroche@redhat.com> - 8.2.2-1
- new upstream version 8.2.2

* Mon Mar 19 2007 Chris Wright <chrisw@redhat.com> - 8.1.0-1
- update to asciidoc 8.1.0

* Thu Sep 14 2006 Chris Wright <chrisw@redhat.com> - 7.0.2-3
- rebuild for Fedora Extras 6

* Tue Feb 28 2006 Chris Wright <chrisw@redhat.com> - 7.0.2-2
- rebuild for Fedora Extras 5

* Mon Aug 29 2005 Chris Wright <chrisw@osdl.org> - 7.0.2-1
- convert spec file to UTF-8
- Source should be URL
- update to 7.0.2

* Fri Aug 19 2005 Chris Wright <chrisw@osdl.org> - 7.0.1-3
- consistent use of RPM_BUILD_ROOT

* Thu Aug 18 2005 Chris Wright <chrisw@osdl.org> - 7.0.1-2
- Update BuildRoot
- use _datadir
- use config and _sysconfdir

* Wed Jun 29 2005 Terje Røsten <terje.rosten@ntnu.no> - 7.0.1-1
- 7.0.1
- Drop patch now upstream
- Build as noarch (Petr Klíma)

* Sat Jun 11 2005 Terje Røsten <terje.rosten@ntnu.no> - 7.0.0-0.3
- Add include patch 

* Fri Jun 10 2005 Terje Røsten <terje.rosten@ntnu.no> - 7.0.0-0.2
- Fix stylesheets according to Stuart

* Fri Jun 10 2005 Terje Røsten <terje.rosten@ntnu.no> - 7.0.0-0.1
- Initial package
- Based on Debian package, thx!
