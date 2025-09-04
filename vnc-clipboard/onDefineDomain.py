#!/usr/bin/python3

import xml.etree.ElementTree as ET
import sys

def add_source(channel):
    source = ET.fromstring(
        """
<source>
    <mouse mode='client'/>
    <clipboard copypaste='yes'/>
</source>
      """
    )
    channel.insert(len(channel), source)


def add_channel(devices):
    channel = ET.fromstring(
        """
    <channel type='qemu-vdagent'>
      <target type='virtio' name='com.redhat.spice.0'/>
      <address type='virtio-serial' controller='1' bus='0' port='3'/>
      <source>
        <mouse mode='client'/>
        <clipboard copypaste='yes'/>
      </source>
    </channel>
"""
    )
    devices.insert(len(devices), channel)

def add_client_clipboard(domainxml):
    root = ET.fromstring(domainxml)
    devices = root.find("devices")
    for channel in devices.findall("channel"):
        ctype = channel.attrib.get("type")
        if ctype is None or ctype != "qemu-vdagent":
            continue

        # There is already qemu-vdagent channel definition
        source = channel.find("source")
        if source is not None:
            # Source already exists. Delete its content and
            # Add content with clipboard enabled.
            channel.remove(source)

        add_source(channel)
        ET.dump(root)
        return

    add_channel(devices)
    ET.dump(root)

if __name__ == "__main__":
    add_client_clipboard(sys.argv[4])
