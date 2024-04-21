Summary:	AdvancePAC - unofficial PacMAME version with advanced video support
Summary(pl.UTF-8):	AdvancePAC - nieoficjalna wersja PacMAME z rozszerzoną obsługą obrazu
Name:		advancepac
Version:	0.58.0
Release:	1
License:	GPL v2+
Group:		Applications/Emulators
Source0:	https://downloads.sourceforge.net/advancemame/%{name}-%{version}.zip
# Source0-md5:	30653288d988dc9ae863d203d9dda19c
# https://www.zophar.net/mame/pacmame.html /0.58
Source1:	https://www.zophar.net/fileuploads/1/1624xbgak/pmsource58.zip
# Source1-md5:	243d4d9444f9c97eeadfae369bbe4d6b
Patch0:		%{name}-format.patch
Patch1:		%{name}-no-common.patch
Patch2:		%{name}-includes.patch
Patch3:		%{name}-link.patch
URL:		http://www.advancemame.it/
BuildRequires:	gcc >= 2.95.3
BuildRequires:	libstdc++-devel
BuildRequires:	make >= 1:3.79.1
BuildRequires:	nasm >= 0.98
BuildRequires:	rpmbuild(macros) >= 1.674
BuildRequires:	sed >= 4.0
BuildRequires:	slang-devel >= 1.4.3
BuildRequires:	svgalib-devel >= 1.9.14
BuildRequires:	zlib-devel >= 1.1.3
Requires:	slang >= 1.4.3
Requires:	svgalib >= 1.9.14
Requires:	zlib >= 1.1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AdvancePAC is unofficial PacMAME version for DOS and Linux with an
advanced video support for helping the use with TVs, Arcade Monitors,
Fixed Frequencies Monitors and also for PC Monitors.

%description -l pl.UTF-8
AdvancePAC to nieoficjalna wersja PacMAME dla DOS-a i Linuksa z
rozszerzoną obsługą obrazu, pozwalająca na korzystanie z monitorów
gier zręcznościowych, monitorów o stałych częstotliwościach, a także
monitorów PC.

%prep
%setup -q -c -a1

%{__mv} src srcpac
%undos srcpac/*.[ch] srcpac/*.mak srcpac/cpu/z80/*.c srcpac/sound/*.c
%undos srcpac/cpu/m68000/*.[ch]
patch -p1 -d srcpac < advance/advpac.dif
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# src/*.h paths in advance/osd/mame2.h
ln -s srcpac src

%build
%{__make} \
%ifarch i586
	ARCH=i586 \
%endif
%ifarch i686
	ARCH=i686 \
%endif
%ifarch k6
	ARCH=k6 \
%endif
%ifarch athlon
	ARCH=athlon \
%endif
%ifnarch i586 i686 k6 athlon
	ARCH=lsb \
%endif
	TARGET=pac \
	CC="%{__cc}" \
	CFLAGS_OPTIMIZE="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	COMPRESS= \
	%{?with_svga:USE_SVGALIB=1}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} install \
	INSTALL_PROGRAM_DIR="install -d -m755" \
	INSTALL_MAN_DIR="install -d -m755" \
	INSTALL_DATA_DIR="install -d -m755" \
	INSTALL_PROGRAM="install -m755" \
	INSTALL_MAN="install -m644" \
	INSTALL_DATA="install -m644" \
	PREFIX=$RPM_BUILD_ROOT%{_prefix}

# main binary omitted by make install???
install advpac $RPM_BUILD_ROOT%{_bindir}

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/{advcfg,advj,advk,advline,advm,advs,advv,authors,faq,history,license,readme,release,script,tips}.txt
%attr(755,root,root) %{_bindir}/advcfg
%attr(755,root,root) %{_bindir}/advj
%attr(755,root,root) %{_bindir}/advk
%attr(755,root,root) %{_bindir}/advline
%attr(755,root,root) %{_bindir}/advm
%attr(755,root,root) %{_bindir}/advpac
%attr(755,root,root) %{_bindir}/advs
%attr(755,root,root) %{_bindir}/advv
%dir %{_datadir}/advance
%dir %{_datadir}/advance/artwork
%dir %{_datadir}/advance/rom
%dir %{_datadir}/advance/sample
%{_datadir}/advance/safequit.dat
