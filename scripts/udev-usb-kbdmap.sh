#!/bin/bash
if [ `id -u` -ne 0 ]; then
	echo "Script must be run with root permissions"
	exit 1
fi
d="/etc/udev/rules.d"
if [ -d "$d" ]; then
	# Remap Caps Lock to ESC via udev to support USB Keyboard hotplugging
	cat > "$d/99-usb-keyboard.rules" << EOF
ACTION=="add", KERNEL=="event*", SUBSYSTEMS=="usb", RUN+="keymap $name 0x70039 esc"
EOF
fi

