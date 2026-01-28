#!/usr/bin/python3

import xml.etree.ElementTree as ET
import sys

def add_dbus_graphic(devices):
    dbus = ET.fromstring("""<graphics type='dbus' address='unix:path=/var/run/vdi/bus' />""")
    devices.insert(len(devices), dbus)

def add_dbus_audio(devices):
    dbus = ET.fromstring("""<audio id='1' type='dbus' />""")
    devices.insert(len(devices), dbus)

def enable_dbus(domainxml):
    root = ET.fromstring(domainxml)
    devices = root.find("devices")

    # delete all graphics, we want only dbus
    for graphic in devices.findall("graphics"):
        devices.remove(graphic)

    # delete all audio devices too
    for audio in devices.findall("audio"):
        devices.remove(audio)

    add_dbus_audio(devices)
    add_dbus_graphic(devices)
    ET.dump(root)

if __name__ == "__main__":
    enable_dbus(sys.argv[4])
