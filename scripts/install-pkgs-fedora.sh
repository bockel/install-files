#!/bin/bash

while read line; do
	yum erase -y "$line"
done << EOF
smolt*
iok
empathy
cheese
gnome-games
gnumeric
goffice
EOF

yum update -y

while read line; do
	yum install -y "$line"
done <<EOF
zsh
vim-X11
libxml2
libxml2-devel
libxslt
libxslt-devel
libpng-devel
pcre-devel
krb5-workstation
rxvt-unicode
git
python-devel
python-pip
gvfs
gvfs-smb
acpi
gnome-keyring
w3m
curl
wget
powertop
htmldoc
ImageMagick
ImageMagick-devel
font-manager
libXinerama-devel
keepassx
gimp
dia
inkscape
graphviz
optipng
pavucontrol
terminus-fonts
terminus-fonts-console
liberation-*
dejavu-*
bitstream-*
google-droid-*-fonts
tlomt-*-fonts
mplus-*-fonts
mgopen-*-fonts
aajohan-comfortaa-fonts
abattis-cantarell-fonts
libreoffice-writer
libreoffice-draw
libreoffice-impress
libreoffice-graphicfilter
libreoffice-langpack-en
xchat-gnome
audit
audit-libs-devel
redhat-lsb
libXScrnSaver
gnupg
gnupg2
jing
speex
speex-tools
ffmpeg
audacity
gnome-tweak-tool
gnome-mplayer
dconf-editor
tmux
policycoreutils-gui
soundconverter
EOF

yum groupinstall -y 'Development Tools'

systemctl disable iscsi.service
systemctl disable iscsid.service
systemctl disable atd.service
systemctl disable cron.service
systemctl disable abrt.service
systemctl disable avahi-daemon.service
systemctl disable mdmonitor-takeover.service
systemctl disable sendmail.service
# systemctl disable NetworkManager.service

# Install misc codec support

yum --nogpgcheck -y install http://rpm.livna.org/livna-release.rpm http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-stable.noarch.rpm http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-stable.noarch.rpm
yum install -y totem-mozplugin gstreamer-plugins-ugly gstreamer-plugins-bad gstreamer-plugins-bad-free gstreamer-plugins-bad-nonfree gstreamer-ffmpeg libdvdcss libdvdnav gstreamer-ffmpeg ffmpeg

yum install -y alsa-plugins-* sox sox-plugins-* mjpegtools

# Install Google chrome

echo "yum install complete..."
echo "Oracle Java, google-chrome, and flash packages must be manually installed"
