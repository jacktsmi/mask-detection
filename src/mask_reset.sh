#!/usr/bin/env bash
#
# power cycle hub 1.1
#
# how to reset:
# https://tomlankhorst.nl/unresponsive-usb-unbind-bind-linux
# https://superuser.com/questions/176319/hard-reset-usb-in-ubuntu-10-04
# how to elevate to root without staying as root:
# https://stackoverflow.com/questions/1988249/how-do-i-use-su-to-execute-the-rest-of-the-bash-script-as-that-user


sudo -i -u root bash << EOF
echo 1.1 > /sys/bus/pci/drivers/usb/unbind
sleep 3
echo 1.1 > /sys/bus/pci/drivers/usb/bind
EOF
