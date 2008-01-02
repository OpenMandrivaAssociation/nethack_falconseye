##### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#####
##### Contact me (gc) if you want to change
##### source version of this package, as there are a couple
##### of in-game checks to perform for validation.
#####
##### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
##### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

%define name nethack_falconseye
%define version 3.3.1_jtp_1.9.3
%define release %mkrel 1

Name: %{name}
Summary: Graphical role-playing game based on nethack
Version: %{version}
Release: %{release}
Group: Games/Adventure
License: GPL-like
Source0: %{name}-%{version}.tar.bz2
Source10: nethack.16.png
Source11: nethack.32.png
Source12: nethack.48.png
Patch0: nethack_falconseye-331_jtp_19-make-it-work.patch
URL: http://www.hut.fi/~jtpelto2/nethack.html
BuildRequires: byacc flex tetex-latex tetex-dvips
BuildRequires: libSDL-devel libxaw-devel ncurses-devel popt-devel 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# Author: jaakko.peltonen@hut.fi

%description
NetHack is one of the oldest computer role-playing games still played and
developed. The latest version of the game, NetHack 3.3.1, was released in
August 2000.

Some players may dislike the game's character-based graphics. Newer
versions of NetHack feature tile-based, somewhat prettier graphics, but I
decided to go even further. Thus, I decided to create a new,
graphics-intensive look for NetHack.

Falcon's Eye is a mouse-driven interface for NetHack that enhances the
visuals, audio and accessibility of the game, yet retains all the original
gameplay and game features.

%prep
%setup -q
%patch0 -p0

%build
pushd sys/unix
sh setup.sh
popd
cd src
export CFLAGS="$RPM_OPT_FLAGS -I../include"
# Note that percent-make will not work
make

%install
rm -rf $RPM_BUILD_ROOT
make install
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_gamesbindir}

cp -a compiled/games/lib/nethackdir/* $RPM_BUILD_ROOT/%{_libdir}/%{name}
rm -rf $RPM_BUILD_ROOT/%{_libdir}/%{name}/manual
cp compiled/games/nethack $RPM_BUILD_ROOT/%{_gamesbindir}
cp util/lev_comp util/dgn_comp $RPM_BUILD_ROOT/%{_libdir}/%{name}

find $RPM_BUILD_ROOT/%{_libdir}/* -type d -exec chmod 755 {} \;
chmod -s $RPM_BUILD_ROOT/%{_libdir}/%{name}/nethack
perl -pi -e 's|^HACKDIR=.*|HACKDIR=%{_libdir}/%{name}|' $RPM_BUILD_ROOT/%{_gamesbindir}/nethack
perl -pi -e 's|^fi|fi\nexport NETHACKOPTIONS="windowtype=jtp,time,noshowexp,number_pad,lit_corridor,rest_on_space"|' \
		$RPM_BUILD_ROOT/%{_gamesbindir}/nethack
perl -pi -e 's|^fullscreen=.*|fullscreen=1|' $RPM_BUILD_ROOT/%{_libdir}/%{name}/config/jtp_opts.txt

cd doc
latex Guidebook.tex
dvips Guidebook.dvi -o Guidebook.ps
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man6
rm -f recover.6
cp *.6 $RPM_BUILD_ROOT/%{_mandir}/man6

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
cat > $RPM_BUILD_ROOT/%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=NetHack Falcons Eye
Comment=NetHack Falcons Eye
Exec=%{_gamesbindir}/nethack
Icon=%{name}
Terminal=false
Type=Applications
StartupNotify=true
Categories=Games;RolePlaying;X-MandrivaLinux-MoreApplications-Games-Adventure;
EOF

mkdir -p $RPM_BUILD_ROOT/%{_miconsdir}
mkdir -p $RPM_BUILD_ROOT/%{_liconsdir}
cp %{SOURCE10} $RPM_BUILD_ROOT/%{_miconsdir}
cp %{SOURCE11} $RPM_BUILD_ROOT/%{_iconsdir}
cp %{SOURCE12} $RPM_BUILD_ROOT/%{_liconsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}

%postun
%{clean_menus}

%files
%defattr(-,root,root)
%doc doc/*.txt doc/Guidebook.ps win/jtp/gamedata/manual
%{_gamesbindir}/*
%{_libdir}/%{name}
%{_mandir}/*/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/*.png
%{_iconsdir}/*.png
%{_liconsdir}/*.png


