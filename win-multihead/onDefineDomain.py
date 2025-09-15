#!/usr/bin/python3

import xml.etree.ElementTree as ET
import sys

NUM_DISPLAYS=2

def set_displays(domainxml):
  root = ET.fromstring(domainxml)
  devices = root.find("devices")

  # Remove any existing video devices.
  for video in devices.findall("video"):
    devices.remove(video)

  # Add requested displays
  for i in range(NUM_DISPLAYS):
    primary = "primary='yes'" if i == 0 else ""
    video = ET.fromstring(
      f"""
    <video>
      <model type='virtio' vram='16384' heads='1' {primary}/>
      <alias name='video{i}'/>
    </video>
""")
    devices.insert(len(devices), video)

  ET.dump(root)

if __name__ == "__main__":
  set_displays(sys.argv[4])
