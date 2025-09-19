#!/usr/bin/python3

import xml.etree.ElementTree as ET
import sys

def add_isa_debug(domainxml):
  root = ET.fromstring(domainxml)
  devices = root.find("devices")

  # Bail if already added
  next_port=0
  for serial in devices.findall("serial"):
    t = serial.get('type')
    if t is not None and t == 'null':
      sys.stderr.write("Already inserted.")
      sys.stderr.write(ET.tostring(serial).decode("utf-8"))
      ET.dump(root)
      return

    target = serial.find("target")
    if target is None:
      continue

    port = target.get('port')
    if port is None or int(port) < next_port:
      continue

    next_port = int(port) + 1

  null_serial = ET.fromstring(
    f"""
  <serial type='null'>
    <log file='/tmp/fw.log' append='off'/>
    <target type='isa-debug' port='{next_port}'>
      <model name='isa-debugcon'/>
    </target>
    <address type='isa' iobase='0x402'/>
  </serial>""")

  pty_serial = ET.fromstring(
    f"""
  <serial type='pty'>
    <log file='/tmp/serial.log' append='off'/>
    <target type='isa-serial' port='{next_port + 1}'>
      <model name='isa-serial'/>
    </target>
  </serial>""")

  devices.insert(len(devices), null_serial)
  devices.insert(len(devices), pty_serial)
  ET.dump(root)

if __name__ == "__main__":
  add_isa_debug(sys.argv[4])
