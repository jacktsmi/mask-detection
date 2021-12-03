#!/usr/bin/env bash
echo "0" > "/sys/bus/usb/devices/usb0/power/autosuspend_delay_ms"
echo "auto" > "/sys/bus/usb/devices/usb0/power/control"

