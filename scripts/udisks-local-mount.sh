#!/bin/bash
if [ `id -u` -ne 0 ]; then
	echo "Script must be run with root permissions"
	exit 1
fi
d="/etc/polkit-1/localauthority/50-local.d/"
if [ -d "$d" ]; then
	cat > "$d/90-local-mount.pkla" << EOF
[udisk Permissions]
Identity=unix-user:*
Action=org.freedesktop.udisks*
ResultAny=yes
ResultInactive=yes
ResultActive=yes
EOF
fi
